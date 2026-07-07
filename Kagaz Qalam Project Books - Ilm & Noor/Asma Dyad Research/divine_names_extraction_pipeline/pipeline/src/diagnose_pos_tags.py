# -*- coding: utf-8 -*-
"""
diagnose_pos_tags.py — Run this to find the EXACT part-of-speech tag CAMeL
Tools returns for the 'ʿalā' (على, "upon/on") preposition — the confirmed
cause of Al-'Alī's 1241 false matches in the first successful extraction
run (all other names were plausible; this one alone was 13x higher than
Allāh's nearest legitimate high-frequency name).

Also checks a genuine Al-'Alī divine-name occurrence for comparison, so you
can see the POS tag DIFFERS between the two usages (if it doesn't differ,
POS-tag filtering won't solve this and homonym-flag-based HITL routing,
already applied to this name, is the correct/only mitigation).

USAGE:
    python diagnose_pos_tags.py

Then add whatever tag(s) print under "PREPOSITION case" to
config.SUSPICIOUS_POS_TAGS, and re-run extract_dyads.py.
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))

from camel_tools.tokenizers.word import simple_word_tokenize
from camel_tools.morphology.database import MorphologyDB
from camel_tools.morphology.analyzer import Analyzer

from config import CAMEL_DB_NAME
from morphology import normalize_for_matching

TEST_CASES = [
    ("Q2:20 (partial) — 'inna Allaha 'ala kulli shay'in Qadir' (Allah is over/upon all things Powerful)",
     "إِنَّ اللَّهَ عَلَىٰ كُلِّ شَيْءٍ قَدِيرٌ",
     "PREPOSITION case — 'ʿalā' should NOT match Al-'Alī here"),
    ("Q2:255 (partial) — 'wa huwa al-'Aliyyu al-'Azim' (He is the Most High, the Most Great)",
     "وَهُوَ الْعَلِيُّ الْعَظِيمُ",
     "GENUINE divine-name case — 'Al-'Alī' SHOULD match here"),
]


def main():
    print(f"Loading CAMeL Tools DB ({CAMEL_DB_NAME})...\n")
    db = MorphologyDB.builtin_db(CAMEL_DB_NAME)
    analyzer = Analyzer(db)

    for label, verse_text, expectation in TEST_CASES:
        print("=" * 90)
        print(label)
        print(f"Expectation: {expectation}")
        print("-" * 90)
        tokens = simple_word_tokenize(verse_text)
        for tok in tokens:
            norm = normalize_for_matching(tok)
            if norm not in ("علي",):  # only print the token(s) relevant to this collision
                continue
            analyses = analyzer.analyze(tok)
            print(f"\n  TOKEN: {tok}  (normalized: {norm})")
            if not analyses:
                print("  No analysis found.")
                continue
            for i, a in enumerate(analyses[:5]):  # show up to 5 candidate analyses
                print(f"  Candidate {i+1}: lex={a.get('lex')}  pos={a.get('pos')}  bw={a.get('bw')}")
        print()

    print("=" * 90)
    print("ACTION: find the 'pos' value shown for the PREPOSITION case above.")
    print("Add it to SUSPICIOUS_POS_TAGS in config.py, e.g.:")
    print('    SUSPICIOUS_POS_TAGS = {"prep"}   # <- use whatever actually printed above')
    print("Confirm it does NOT also appear for the GENUINE divine-name case — if it")
    print("does, POS-tagging can't cleanly separate these two, and the homonym-flag")
    print("HITL routing (already active for Al-'Alī) is the correct primary mitigation,")
    print("not a POS filter.")


if __name__ == "__main__":
    main()
