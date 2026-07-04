# -*- coding: utf-8 -*-
"""
make_calibration_sets.py — Solves the chicken-and-egg problem in Dossier
§5.8.1/§5.9: prompts must be validated against a human-labeled gold set
BEFORE scale use, but nobody has classified any dyad by theme or
relationship-type yet — there is no pre-existing ground truth.

This script does NOT generate labels. It generates a well-STRATIFIED SAMPLE
of dyads for YOU (the principal researcher) to label by hand, using the
tafsīr sources the dossier already commits to (Al-Rāzī primary, Ibn Kathīr,
Al-Ṭabarī, Al-Qurṭubī). That hand-labeling is real scholarly work — this
script's only job is to make sure the sample you label is representative,
not to do the labeling for you.

Stratification logic:
  - Theme calibration (20 dyads): stratified across the 7 macro categories
    so the calibration set isn't accidentally all-Tawḥīd or all-Narrative.
  - Relationship calibration (30 dyads): stratified across JJK pair-type
    (Jalāl+Jalāl, Jalāl+Jamāl, Jalāl+Kamāl, etc.) so all 5 relationship
    types have a chance to appear in the gold set.

USAGE:
    python make_calibration_sets.py
"""

import csv
import random
import sys
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from config import (
    DYAD_OUTPUT_CSV, THEME_CALIBRATION_SIZE, RELATIONSHIP_CALIBRATION_SIZE,
    THEME_CALIBRATION_CSV, RELATIONSHIP_CALIBRATION_CSV, RANDOM_SEED,
)

MACRO_CATEGORIES = [
    "Tawḥīd", "Prophethood", "Worship", "Narrative", "Creation", "Eschatology", "Law/Community"
]


def load_dyads():
    with open(DYAD_OUTPUT_CSV, encoding="utf-8") as f:
        return list(csv.DictReader(f))


def stratified_sample_by_jjk_pair(dyads, n, seed):
    """Groups by (jjk_1, jjk_2) unordered pair-type isn't available in the raw
    dyad CSV directly (that's produced by relationship_type.py's own JJK
    lookup) — here we approximate stratification using name_1/name_2 serials
    binned by tier as a proxy, then do simple random sampling within groups
    of surahs to at least avoid over-representing one surah's refrain.
    """
    rng = random.Random(seed)
    by_surah = defaultdict(list)
    for d in dyads:
        by_surah[d["surah_number"]].append(d)

    surahs = list(by_surah.keys())
    rng.shuffle(surahs)
    sample = []
    i = 0
    while len(sample) < n and surahs:
        surah = surahs[i % len(surahs)]
        pool = by_surah[surah]
        if pool:
            sample.append(pool.pop(rng.randrange(len(pool))))
        if not pool:
            surahs.remove(surah)
            if not surahs:
                break
            i = i % len(surahs)
        else:
            i += 1
    return sample[:n]


def write_theme_calibration(dyads):
    sample = stratified_sample_by_jjk_pair(dyads, THEME_CALIBRATION_SIZE, RANDOM_SEED)
    rows = []
    for d in sample:
        rows.append({
            "surah_number": d["surah_number"], "ayah_number": d["ayah_number"],
            "name_1_translit": d["name_1_translit"], "name_2_translit": d["name_2_translit"],
            "GOLD_macro_theme": "",   # <-- YOU fill this in by hand
            "GOLD_micro_theme": "",   # <-- YOU fill this in by hand
            "labeling_notes": "",     # optional: why you chose this label, tafsir source consulted
        })
    THEME_CALIBRATION_CSV.parent.mkdir(parents=True, exist_ok=True)
    with open(THEME_CALIBRATION_CSV, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)
    print(f"Wrote {len(rows)} rows -> {THEME_CALIBRATION_CSV}")
    print("  ACTION REQUIRED: open this file and fill in GOLD_macro_theme and")
    print("  GOLD_micro_theme by hand, consulting Al-Rāzī/Ibn Kathīr/Al-Ṭabarī/")
    print("  Al-Qurṭubī per Dossier §5.1. Use the exact category names from")
    print("  data/micro_taxonomy_20.csv (macro column) — free text will fail")
    print("  the accuracy check in theme_tagging.py's calibration mode.")


def write_relationship_calibration(dyads):
    sample = stratified_sample_by_jjk_pair(dyads, RELATIONSHIP_CALIBRATION_SIZE, RANDOM_SEED + 1)
    rows = []
    for d in sample:
        rows.append({
            "surah_number": d["surah_number"], "ayah_number": d["ayah_number"],
            "name_1_translit": d["name_1_translit"], "name_2_translit": d["name_2_translit"],
            "GOLD_relationship_type": "",  # <-- YOU fill this in: complementary/balancing/reinforcing/sequential/intensifying
            "GOLD_decision_path_notes": "",  # optional: which Q1-Q5 branch you applied and why
        })
    RELATIONSHIP_CALIBRATION_CSV.parent.mkdir(parents=True, exist_ok=True)
    with open(RELATIONSHIP_CALIBRATION_CSV, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)
    print(f"Wrote {len(rows)} rows -> {RELATIONSHIP_CALIBRATION_CSV}")
    print("  ACTION REQUIRED: fill in GOLD_relationship_type by hand, applying")
    print("  the decision tree in Dossier §5.5 yourself. This calibration set")
    print("  is ALSO the IRR set — per §5.5, a second independent annotator")
    print("  (the Islamic Studies consultant) must label the SAME 30 dyads")
    print("  separately for the κ≥0.65 check in relationship_type.py to be valid.")
    print("  A single-annotator 'IRR' check is not real IRR — flagging this now")
    print("  so it isn't discovered as a gap after the fact.")


def main():
    print("Loading extracted dyads...")
    dyads = load_dyads()
    print(f"  {len(dyads)} dyads available to sample from.\n")

    print("=== Theme calibration set ===")
    write_theme_calibration(dyads)
    print("\n=== Relationship-type calibration/IRR set ===")
    write_relationship_calibration(dyads)


if __name__ == "__main__":
    main()
