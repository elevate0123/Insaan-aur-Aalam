# -*- coding: utf-8 -*-
"""
npmi_stats.py — NPMI (Normalized Pointwise Mutual Information) with
bootstrap confidence intervals, per Dossier §5.6 and Appendix A.2.11.

WHY bootstrap CIs matter here (Appendix A.2.11 critique): at n=1,2,3
occurrences, NPMI point estimates have very wide true uncertainty. Ranking
pairs by raw NPMI without a CI produces false precision — this script
exists specifically to prevent that mistake. Downstream scripts/papers MUST
restrict comparative claims ("pair X has stronger bond than pair Y") to
cases where the 95% CIs do NOT overlap. This script computes the CIs; it
does not enforce the comparison rule for you — that discipline belongs in
whatever writes the paper text.

INPUT:  output/dyad_dataset_raw.csv, output/verse_name_occurrences.csv
OUTPUT: output/npmi_with_ci.csv

USAGE:
    python npmi_stats.py
"""

import csv
import sys
import math
import random
import argparse
from collections import Counter, defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from config import (
    DYAD_OUTPUT_CSV, VERSE_NAMES_CSV, NPMI_OUTPUT_CSV,
    BOOTSTRAP_RESAMPLES, RANDOM_SEED,
)
from filters import load_dyads as filtered_load_dyads, load_verse_names as filtered_load_verse_names, print_filter_report


def load_dyads(path=DYAD_OUTPUT_CSV, confident_only=True):
    rows, n_excl, n_total = filtered_load_dyads(path, confident_only)
    print_filter_report("npmi_stats", n_excl, n_total, confident_only)
    return rows


def load_verse_names(path=VERSE_NAMES_CSV, confident_only=True):
    rows, n_excl, n_total = filtered_load_verse_names(path, confident_only)
    return rows


def compute_npmi(pair_count: int, name_a_count: int, name_b_count: int, total_verses: int) -> float:
    """
    NPMI = PMI(a,b) / -log(p(a,b))
    p(a,b), p(a), p(b) estimated over the verse corpus (total_verses as N).
    Returns a value in [-1, 1]; +1 = perfect co-occurrence, -1 = perfect
    avoidance, 0 = independence.
    """
    if pair_count == 0:
        return float("nan")
    p_ab = pair_count / total_verses
    p_a = name_a_count / total_verses
    p_b = name_b_count / total_verses
    if p_a == 0 or p_b == 0 or p_ab == 0:
        return float("nan")
    pmi = math.log(p_ab / (p_a * p_b))
    denom = -math.log(p_ab)
    if denom == 0:
        return float("nan")
    return pmi / denom


def bootstrap_npmi_ci(pair_verse_ids, name_a_verse_ids, name_b_verse_ids, total_verses,
                       n_resamples=BOOTSTRAP_RESAMPLES, seed=RANDOM_SEED):
    """
    Resamples verses WITH REPLACEMENT n_resamples times, recomputing NPMI
    each time, and returns (lower, upper) at the 2.5/97.5 percentiles.

    NOTE on method: this resamples at the VERSE level (not the dyad-instance
    level), which is the correct unit here — verses are the independent
    sampling unit in the corpus, dyad co-occurrences within a verse are not
    independent of each other.
    """
    rng = random.Random(seed)
    all_verse_ids = list(range(total_verses))
    pair_set = set(pair_verse_ids)
    a_set = set(name_a_verse_ids)
    b_set = set(name_b_verse_ids)

    estimates = []
    for _ in range(n_resamples):
        sample = [rng.choice(all_verse_ids) for _ in range(total_verses)]
        pair_c = sum(1 for v in sample if v in pair_set)
        a_c = sum(1 for v in sample if v in a_set)
        b_c = sum(1 for v in sample if v in b_set)
        val = compute_npmi(pair_c, a_c, b_c, total_verses)
        if not math.isnan(val):
            estimates.append(val)

    if len(estimates) < 30:
        # Too few valid resamples (e.g. extremely rare pair) to trust a
        # percentile CI — flag rather than report a misleadingly tight range.
        return (float("nan"), float("nan"), "INSUFFICIENT_RESAMPLES")

    estimates.sort()
    lo = estimates[int(0.025 * len(estimates))]
    hi = estimates[int(0.975 * len(estimates))]
    return (lo, hi, "OK")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--include-unreviewed", action="store_true",
                         help="Use ALL dyads including homonym-flagged/unreviewed ones. "
                              "Default (off) uses only the confident subset — see filters.py.")
    args = parser.parse_args()
    confident_only = not args.include_unreviewed

    print("Loading dyad dataset and verse-level name occurrences...")
    dyads = load_dyads(confident_only=confident_only)
    verse_names = load_verse_names(confident_only=confident_only)

    # Build verse-id space: (surah, ayah) -> integer id, needed for the
    # resampling arithmetic above.
    verse_ids = {}
    for row in verse_names:
        key = (row["surah_number"], row["ayah_number"])
        if key not in verse_ids:
            verse_ids[key] = len(verse_ids)
    total_verses = len(verse_ids)
    print(f"  {total_verses} distinct verses contain at least one divine name.")

    # name_serial -> set of verse ids it occurs in
    name_verses = defaultdict(set)
    for row in verse_names:
        key = (row["surah_number"], row["ayah_number"])
        name_verses[row["name_serial"]].add(verse_ids[key])

    # (name_a, name_b) -> set of verse ids where BOTH occur as a dyad
    # (order-independent for this purpose; NPMI doesn't care about direction)
    pair_verses = defaultdict(set)
    pair_meta = {}
    for row in dyads:
        a, b = sorted([row["name_1_serial"], row["name_2_serial"]])
        key = (a, b)
        vkey = (row["surah_number"], row["ayah_number"])
        pair_verses[key].add(verse_ids[vkey])
        pair_meta[key] = (row["name_1_translit"] if row["name_1_serial"] == a else row["name_2_translit"],
                           row["name_2_translit"] if row["name_1_serial"] == a else row["name_1_translit"])

    print(f"  {len(pair_verses)} unique unordered name-pairs found.")
    print(f"Computing NPMI + bootstrap CI ({BOOTSTRAP_RESAMPLES} resamples per pair — this is the slow part)...")

    results = []
    for i, (key, pverses) in enumerate(pair_verses.items()):
        a, b = key
        translit_a, translit_b = pair_meta[key]
        pair_count = len(pverses)
        a_count = len(name_verses[a])
        b_count = len(name_verses[b])

        npmi = compute_npmi(pair_count, a_count, b_count, total_verses)
        lo, hi, status = bootstrap_npmi_ci(pverses, name_verses[a], name_verses[b], total_verses)

        results.append({
            "name_1_serial": a, "name_1_translit": translit_a,
            "name_2_serial": b, "name_2_translit": translit_b,
            "raw_frequency": pair_count,
            "npmi": round(npmi, 4) if not math.isnan(npmi) else "NaN",
            "npmi_ci_lower": round(lo, 4) if not math.isnan(lo) else "NaN",
            "npmi_ci_upper": round(hi, 4) if not math.isnan(hi) else "NaN",
            "ci_status": status,
            "hapax_flag": (pair_count == 1),
        })
        if (i + 1) % 20 == 0:
            print(f"  ...{i+1}/{len(pair_verses)} pairs done")

    NPMI_OUTPUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    out_path = NPMI_OUTPUT_CSV if confident_only else NPMI_OUTPUT_CSV.with_name(
        NPMI_OUTPUT_CSV.stem + "_UNREVIEWED_INCLUDED" + NPMI_OUTPUT_CSV.suffix)
    with open(out_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(results[0].keys()))
        writer.writeheader()
        writer.writerows(results)

    n_hapax = sum(1 for r in results if r["hapax_flag"])
    print(f"\nWrote {len(results)} pairs -> {out_path}")
    if confident_only:
        print("  (Filename unchanged from before — this IS the confident-subset file now,")
        print("   by default. Use --include-unreviewed for the old unfiltered behavior,")
        print("   which will write to a separate *_UNREVIEWED_INCLUDED file instead.)")
    print(f"  {n_hapax}/{len(results)} pairs are hapax (n=1) — expect very wide CIs on these.")
    print("\nREMINDER (Appendix A.2.11): comparative NPMI claims ('X binds stronger than Y')")
    print("are only valid where the 95% CIs do NOT overlap. Check ci_status != 'OK' rows")
    print("before using them in any ranking claim.")


if __name__ == "__main__":
    main()
