# -*- coding: utf-8 -*-
"""
run_sensitivity.py — Runs the extraction at every threshold in
config.SENSITIVITY_THRESHOLDS and reports which findings are stable across
them, per Dossier §5.7/§5.8 and Appendix A.2.17 ("arbitrary 10-word
threshold" critique — this is the fix).

USAGE:
    python run_sensitivity.py

Produces output/sensitivity_analysis.csv with one row per threshold showing:
  - total dyad count
  - top-10 most frequent (name_1, name_2) pairs at that threshold
  - whether the top-10 set is IDENTICAL to the primary-threshold top-10

This does NOT re-run CAMeL Tools analysis per threshold (expensive/redundant
— morphology doesn't change with distance threshold). It re-runs only the
distance-filtering + pairing step against a single cached tokenization pass.
"""

import csv
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from config import SENSITIVITY_THRESHOLDS, PRIMARY_DISTANCE_THRESHOLD, SENSITIVITY_OUTPUT_CSV
from quran_source import load_verses, load_meccan_medinan
from morphology import MorphAnalyzer
from names_loader import load_divine_names, build_lemma_index
from extract_dyads import process_verse, setup_logging


def main():
    logger = setup_logging()
    logger.info("=== Sensitivity analysis run ===")

    names = load_divine_names()
    lemma_index = build_lemma_index(names)
    verses = load_verses()
    verses = load_meccan_medinan(verses)
    analyzer = MorphAnalyzer()

    logger.info(f"Tokenizing + analyzing {len(verses)} verses once (reused across all thresholds)...")
    verse_tokens = []
    for i, verse in enumerate(verses):
        verse_tokens.append((verse, analyzer.analyze_verse(verse.text)))
        if (i + 1) % 1000 == 0:
            logger.info(f"  ...{i+1}/{len(verses)}")

    max_threshold = max(SENSITIVITY_THRESHOLDS)
    results_by_threshold = {}
    for threshold in SENSITIVITY_THRESHOLDS:
        all_dyads = []
        for verse, tokens in verse_tokens:
            dyads, _ = process_verse(verse, tokens, lemma_index, threshold, logger)
            all_dyads.extend(dyads)
        pair_counts = Counter(
            (d["name_1_serial"], d["name_2_serial"]) for d in all_dyads
        )
        results_by_threshold[threshold] = {
            "total_dyads": len(all_dyads),
            "unique_pairs": len(pair_counts),
            "top10": pair_counts.most_common(10),
        }
        logger.info(f"  threshold={threshold}: {len(all_dyads)} dyads, {len(pair_counts)} unique pairs")

    primary_top10_set = set(p for p, _ in results_by_threshold[PRIMARY_DISTANCE_THRESHOLD]["top10"])

    rows = []
    for threshold in SENSITIVITY_THRESHOLDS:
        r = results_by_threshold[threshold]
        this_top10_set = set(p for p, _ in r["top10"])
        rows.append({
            "threshold": threshold,
            "total_dyads": r["total_dyads"],
            "unique_pairs": r["unique_pairs"],
            "top10_pairs": "; ".join(f"{a}-{b}({c})" for (a, b), c in r["top10"]),
            "top10_identical_to_primary": (this_top10_set == primary_top10_set),
            "top10_overlap_count_with_primary": len(this_top10_set & primary_top10_set),
        })

    SENSITIVITY_OUTPUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    with open(SENSITIVITY_OUTPUT_CSV, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

    logger.info(f"Wrote sensitivity table -> {SENSITIVITY_OUTPUT_CSV}")
    logger.info("Review this table before choosing the primary threshold for the final")
    logger.info("published dataset. Per Dossier §5.7, report this table in Paper 0")
    logger.info("supplementary materials regardless of which threshold you keep.")


if __name__ == "__main__":
    main()
