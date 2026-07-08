# -*- coding: utf-8 -*-
"""
diagnose_matching.py — Run this to find out EXACTLY why 105/108 names
failed to match anywhere in the corpus (only Allāh, Al-Ḥaqq, Al-Ḥayy
matched — see the session's root-cause analysis in README.md "Known bug").

Prints, for a handful of verses KNOWN to contain a real dyad (from
extraction_log.txt, already verified against the master dataset), the raw
CAMeL Tools analysis output for each token, side by side with what our
normalize_for_matching() produces for both the token's lemma AND the
master-list name it should match — so the exact character-level mismatch
becomes visible instead of guessed at.

LEADING HYPOTHESIS (needs this script's output to confirm): our master CSV
stores names WITH the definite article attached (e.g. الْمَلِك = "Al-Malik",
because that's the conventional way divine Names are written/cited), but
CAMeL Tools' morphological lemma output strips the definite article as a
separate clitic (standard Arabic morphological analysis treats "ال" as a
bound prefix, not part of the lemma/citation form) — so a successfully-
analyzed token's lemma would be "ملك", which never equals our master
entry's normalized "الملك". Allāh matches because it's an atomic proper
noun CAMeL doesn't decompose; Al-Ḥaqq/Al-Ḥayy matching at low, likely-
partly-spurious rates is also consistent with this — see the notes this
script prints for those specific cases too.

USAGE:
    python diagnose_matching.py
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))

from camel_tools.tokenizers.word import simple_word_tokenize
from camel_tools.morphology.database import MorphologyDB
from camel_tools.morphology.analyzer import Analyzer

from config import CAMEL_DB_NAME
from morphology import normalize_for_matching, strip_diacritics
from names_loader import load_divine_names

# Known-good test verses (from extraction_log.txt, already cross-checked
# against the v2.1 master dataset this session — the DYAD in each of these
# is certain; if it doesn't match, the pipeline is at fault, not the data).
TEST_VERSES = [
    ("Q2:129", "وَابْعَثْ فِيهِمْ رَسُولًا مِّنْهُمْ يَتْلُو عَلَيْهِمْ آيَاتِكَ وَيُعَلِّمُهُمُ الْكِتَابَ وَالْحِكْمَةَ وَيُزَكِّيهِمْ ۚ إِنَّكَ أَنتَ الْعَزِيزُ الْحَكِيمُ",
     ["Al-'Azīz", "Al-Ḥakīm"]),
    ("Q2:37", "فَتَلَقَّىٰ آدَمُ مِن رَّبِّهِ كَلِمَاتٍ فَتَابَ عَلَيْهِ ۚ إِنَّهُ هُوَ التَّوَّابُ الرَّحِيمُ",
     ["Al-Tawwāb", "Al-Raḥīm"]),
    ("Q2:255 (partial)", "اللَّهُ لَا إِلَٰهَ إِلَّا هُوَ الْحَيُّ الْقَيُّومُ",
     ["Allāh", "Al-Ḥayy", "Al-Qayyūm"]),
]


def main():
    print("Loading master names list...")
    names = load_divine_names()
    name_by_translit = {n.transliteration: n for n in names}

    print(f"Loading CAMeL Tools DB ({CAMEL_DB_NAME})...\n")
    db = MorphologyDB.builtin_db(CAMEL_DB_NAME)
    analyzer = Analyzer(db)

    for verse_ref, verse_text, expected_names in TEST_VERSES:
        print("=" * 90)
        print(f"{verse_ref}: {verse_text}")
        print(f"Expected names in this verse: {expected_names}")
        print("-" * 90)

        tokens = simple_word_tokenize(verse_text)
        for tok in tokens:
            analyses = analyzer.analyze(tok)
            our_norm = normalize_for_matching(tok)

            print(f"\n  TOKEN (raw):        {tok}")
            print(f"  TOKEN (our normalize_for_matching, i.e. the no-analysis fallback path): {our_norm}")

            if not analyses:
                print(f"  CAMeL analysis:      ** NONE FOUND ** (falls back to raw-token matching)")
            else:
                best = analyses[0]
                lex = best.get("lex", "?")
                bw = best.get("bw", "?")
                pos = best.get("pos", "?")
                lex_normalized = normalize_for_matching(lex)
                print(f"  CAMeL 'lex' (lemma, raw):        {lex}")
                print(f"  CAMeL 'lex' normalized (our fn): {lex_normalized}")
                print(f"  CAMeL 'bw' (buckwalter tag):     {bw}")
                print(f"  CAMeL 'pos':                     {pos}")
                print(f"  Number of candidate analyses:    {len(analyses)}")

        print()
        for expected in expected_names:
            n = name_by_translit.get(expected)
            if n:
                print(f"  Master list '{expected}': raw={n.arabic!r}  normalized={n.normalized_arabic!r}")
            else:
                print(f"  Master list '{expected}': NOT FOUND in divine_names_master.csv (check transliteration spelling)")
        print()

    print("=" * 90)
    print("READ THIS: for each verse above, look for the expected name's token.")
    print("Compare 'CAMeL lex normalized' (when an analysis WAS found) against")
    print("'Master list normalized'. If they differ ONLY by a leading 'ال', that")
    print("confirms the definite-article hypothesis — the fix in names_loader.py")
    print("(strip leading 'ال' from BOTH sides before indexing/matching) should be")
    print("applied. If the mismatch is something else entirely (e.g. sense-number")
    print("suffix like '_1', different diacritic residue, etc.), paste this output")
    print("back for a precise fix rather than the article-stripping guess.")


if __name__ == "__main__":
    main()
