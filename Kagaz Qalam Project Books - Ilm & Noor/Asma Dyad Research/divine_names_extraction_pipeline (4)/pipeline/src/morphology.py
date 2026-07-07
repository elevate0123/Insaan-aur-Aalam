# -*- coding: utf-8 -*-
"""
morphology.py — Thin wrapper around CAMeL Tools for the extraction pipeline.

Responsibilities:
  1. Tokenize a verse into words.
  2. Run morphological analysis on each word.
  3. Return a normalized lemma + a set of morphological flags per token:
       - definite article present? (Dossier §5.3 step 4)
       - syntactic role guess (nominal predicate / adjective / proper noun)
       - analyzer confidence score

This module intentionally does ONE thing (morphology) so extract_dyads.py
stays readable. If you swap analyzers later (e.g. add a Quranic-specific
one), this is the only file that should need to change.
"""

import re
import unicodedata
from dataclasses import dataclass
from typing import List, Optional

from camel_tools.tokenizers.word import simple_word_tokenize
from camel_tools.morphology.database import MorphologyDB
from camel_tools.morphology.analyzer import Analyzer

from config import CAMEL_DB_NAME, MIN_ANALYSIS_CONFIDENCE

# Arabic diacritics (tashkīl) — stripped before lemma comparison so that a
# fully-vocalized Quranic token and a bare-consonant master-list entry can
# still match. We do NOT strip diacritics before storing the raw token text
# (we want the original Uthmani spelling preserved in output).
_DIACRITICS = re.compile(
    r"[\u0610-\u061A\u064B-\u065F\u06D6-\u06DC\u06DF-\u06E8\u06EA-\u06ED\u0670]"
)
_TATWEEL = "\u0640"


def strip_diacritics(text: str) -> str:
    """Remove Arabic diacritical marks and the elongation character (tatweel)."""
    text = _DIACRITICS.sub("", text)
    text = text.replace(_TATWEEL, "")
    return text


def normalize_alef_ya(text: str) -> str:
    """
    Normalize common Quranic/Uthmani orthographic variants to a single form,
    ONLY for matching purposes (never for display). This handles cases like
    alef maksura vs ya, hamza-seat variation, etc. that would otherwise
    cause false-negative name matches.
    """
    text = re.sub("[إأآا]", "ا", text)   # alef variants -> bare alef
    text = re.sub("ى", "ي", text)         # alef maksura -> ya
    text = text.replace("ة", "ه")          # ta marbuta -> ha (matching only)
    text = text.replace("ؤ", "و")
    text = text.replace("ئ", "ي")
    return text


_LEMMA_SENSE_SUFFIX = re.compile(r"_\d+$")
_LEADING_DEFINITE_ARTICLE = re.compile(r"^(ال)")

# Forms that must NEVER have a leading "ال" stripped, even though they start
# with those two characters — "الله" is NOT orthographically al+"له"
# ("to him"); it is a single indivisible proper noun. Stripping it would
# silently corrupt the single most important match in the whole corpus.
# Checked BEFORE stripping, against the ALREADY-diacritic-stripped/alef-
# normalized form, so add variants here in that same normalized shape.
_ARTICLE_STRIP_EXCEPTIONS = {"الله", "اللّه"}


def strip_lemma_sense_suffix(text: str) -> str:
    """
    CAMeL Tools' 'lex' field sometimes carries a homograph/sense-disambiguation
    suffix in the form '<lemma>_<N>' (e.g. a lemma rendered as 'ملك_1' to
    distinguish it from a different root/meaning sharing the same spelling).
    Strip it before comparison — added after the first real corpus run
    surfaced near-total match failure; this is one of two suspected causes
    alongside the definite-article mismatch below. Run diagnose_matching.py
    to confirm which (or both) were actually in play before assuming this
    fixed it.
    """
    return _LEMMA_SENSE_SUFFIX.sub("", text)


def strip_leading_definite_article(text: str) -> str:
    """
    HYPOTHESIS FIX, not confirmed — see diagnose_matching.py. Standard Arabic
    morphological analysis treats 'ال' as a bound clitic, stripped from the
    lemma/citation form. Our master list stores names WITH the article
    attached (conventional citation form, e.g. 'Al-Malik'), which would never
    match a post-analysis lemma unless both sides are normalized the same
    way. This strips a GENUINE LEADING article only (regex anchors at ^, so
    embedded 'ال' inside compound names like Dhū al-Jalāl wa'l-Ikrām, which
    does not itself start with 'ال', is untouched).

    SAFETY: never strips 'الله' (Allāh) — see _ARTICLE_STRIP_EXCEPTIONS.
    """
    if text in _ARTICLE_STRIP_EXCEPTIONS:
        return text
    return _LEADING_DEFINITE_ARTICLE.sub("", text, count=1)


def normalize_for_matching(text: str) -> str:
    text = unicodedata.normalize("NFC", text)
    text = strip_lemma_sense_suffix(text)
    text = strip_diacritics(text)
    text = normalize_alef_ya(text)
    text = strip_leading_definite_article(text)
    return text.strip()


@dataclass
class TokenAnalysis:
    surface_form: str            # original token as it appears in the verse
    lemma: str                   # CAMeL Tools lemma, diacritics stripped
    normalized: str              # fully normalized form used for name matching
    has_definite_article: bool
    pos_guess: Optional[str]     # 'noun', 'adj', 'pron', etc. (CAMeL 'pos' tag)
    confidence: float            # top analysis score, 0.0 if no analysis found
    position_in_verse: int       # 0-indexed token position


class MorphAnalyzer:
    """Loads the CAMeL Tools DB once; reuse a single instance across the run."""

    def __init__(self, db_name: str = CAMEL_DB_NAME):
        db = MorphologyDB.builtin_db(db_name)
        self._analyzer = Analyzer(db)

    def analyze_verse(self, verse_text: str) -> List[TokenAnalysis]:
        tokens = simple_word_tokenize(verse_text)
        results = []
        for i, tok in enumerate(tokens):
            results.append(self._analyze_token(tok, i))
        return results

    def _analyze_token(self, token: str, position: int) -> TokenAnalysis:
        analyses = self._analyzer.analyze(token)

        if not analyses:
            # No morphological analysis available (rare for Quranic forms
            # with an MSA-trained analyzer — expect a handful per surah).
            # Fall back to the surface form itself so the token still
            # participates in name-matching; confidence=0 forces HITL review
            # of anything that matches a divine name via this fallback path.
            norm = normalize_for_matching(token)
            return TokenAnalysis(
                surface_form=token,
                lemma=norm,
                normalized=norm,
                has_definite_article=norm.startswith("ال"),
                pos_guess=None,
                confidence=0.0,
                position_in_verse=position,
            )

        # CAMeL Tools returns multiple candidate analyses ranked implicitly;
        # take the first (highest-prior) one. If you want full disambiguation
        # using sentence context instead of per-token top-1, swap this for
        # camel_tools.disambig.mle.MLEDisambiguator — slower, more accurate,
        # recommended once the pipeline is validated on a sample and you're
        # ready to run the full corpus for the final dataset.
        best = analyses[0]
        lemma_raw = best.get("lex", token)
        lemma_norm = normalize_for_matching(lemma_raw)

        return TokenAnalysis(
            surface_form=token,
            lemma=lemma_norm,
            normalized=lemma_norm,
            has_definite_article=("Al+" in best.get("bw", "") or lemma_norm.startswith("ال")),
            pos_guess=best.get("pos"),
            confidence=1.0,  # camel-tools analyze() doesn't score candidates;
                              # =1.0 marks "an analysis was found" vs the 0.0
                              # no-analysis fallback above. Swap to MLEDisambiguator
                              # (see note above) if you need real probability scores.
            position_in_verse=position,
        )
