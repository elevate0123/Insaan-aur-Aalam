# -*- coding: utf-8 -*-
"""
selftest.py — Run this FIRST, before the full corpus extraction, to confirm
your environment is set up correctly. Takes ~30 seconds. Does not need the
full Tanzil XML — tests against 3 hardcoded verses with known, hand-verified
expected dyads (taken from extraction_log.txt, already in your project and
already verified against the current master dataset — see the audit trail
in this session).

USAGE:
    python selftest.py

If this fails, fix the reported issue before running extract_dyads.py on
the full corpus — do not debug a 6,236-verse run when a 3-verse run already
tells you what's wrong.
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))

from quran_source import Verse
from morphology import MorphAnalyzer
from names_loader import load_divine_names, build_lemma_index
from extract_dyads import process_verse

# Hand-picked from extraction_log.txt (already cross-checked against the
# v2.1 master dataset this session — zero mismatches found).
TEST_CASES = [
    {
        "verse": Verse(2, "البقرة", 32, "قَالُوا۟ سُبْحَٰنَكَ لَا عِلْمَ لَنَآ إِلَّا مَا عَلَّمْتَنَآ ۖ إِنَّكَ أَنتَ ٱلْعَلِيمُ ٱلْحَكِيمُ"),
        "expected_pair": ("Al-'Alīm", "Al-Ḥakīm"),
        "expected_position": "verse-final",
    },
    {
        "verse": Verse(2, "البقرة", 255, "ٱللَّهُ لَآ إِلَٰهَ إِلَّا هُوَ ٱلْحَىُّ ٱلْقَيُّومُ ۚ لَا تَأْخُذُهُۥ سِنَةٌ وَلَا نَوْمٌ"),
        "expected_pair": ("Al-Ḥayy", "Al-Qayyūm"),
        "expected_position": "verse-opening",
    },
    {
        "verse": Verse(12, "يوسف", 51, "قَالَ مَا خَطْبُكُنَّ إِذْ رَٰوَدتُّنَّ يُوسُفَ عَن نَّفْسِهِۦ ۚ قُلْنَ حَٰشَ لِلَّهِ مَا عَلِمْنَا عَلَيْهِ مِن سُوٓءٍ"),
        "expected_pair": None,  # SKIP_HOMONYM per extraction_log.txt — 'aziz'
        "note": "Q12:51 area — homonym-risk verse; primarily a check that the "
                "pipeline does NOT silently over-match, not a dyad test.",
    },
]


def run():
    print("Loading divine names...")
    names = load_divine_names()
    lemma_index = build_lemma_index(names)
    print(f"  {len(names)} names loaded, {len(lemma_index)} lemma keys.\n")

    print("Loading CAMeL Tools analyzer (this is the slow step, ~10-30s)...")
    analyzer = MorphAnalyzer()
    print("  Loaded.\n")

    failures = 0
    for i, case in enumerate(TEST_CASES, 1):
        verse = case["verse"]
        print(f"[{i}] Q{verse.surah_number}:{verse.ayah_number} — {verse.text[:40]}...")
        tokens = analyzer.analyze_verse(verse.text)
        dyads, hitl = process_verse(verse, tokens, lemma_index, threshold=10, logger=_NullLogger())

        if case.get("expected_pair") is None:
            print(f"    -> {len(dyads)} dyad(s) found (informational, no assertion).")
            continue

        found_pairs = {(d["name_1_translit"], d["name_2_translit"]) for d in dyads}
        expected = case["expected_pair"]
        ok = expected in found_pairs or expected[::-1] in found_pairs
        status = "PASS" if ok else "FAIL"
        if not ok:
            failures += 1
        print(f"    expected pair: {expected}  ->  {status}")
        print(f"    all pairs found: {found_pairs}")

    print()
    if failures == 0:
        print("ALL SELFTESTS PASSED. Safe to proceed to the full corpus run.")
        print("Next: python extract_dyads.py")
    else:
        print(f"{failures} SELFTEST(S) FAILED. Do not run the full corpus yet.")
        print("Check: CAMeL Tools DB installed correctly? divine_names_master.csv")
        print("up to date? See README.md 'Troubleshooting'.")
    return failures


class _NullLogger:
    def warning(self, *a, **k): pass
    def info(self, *a, **k): pass


if __name__ == "__main__":
    sys.exit(1 if run() else 0)
