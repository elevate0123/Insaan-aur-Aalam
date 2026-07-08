# -*- coding: utf-8 -*-
"""
null_models.py — Statistical Validation, Dossier §5.8.

Null Model A (corpus-wide): permutes name assignments across ALL verses,
    preserving the number of names per verse. Tests overall dyad
    significance (Paper 1).

Null Model B (period-stratified): permutes WITHIN Meccan verses and WITHIN
    Medinan verses separately, preserving period structure. Tests the
    Meccan/Medinan differential claim (Paper 3) — Model A CANNOT support
    this claim; this is exactly the Appendix A.2.4 fix for that gap.

Both models are permutation tests over verses, not over the already-paired
dyad list — this is why they consume verse_name_occurrences.csv (the full
per-verse name inventory), not dyad_dataset_raw.csv.

USAGE:
    python null_models.py                  # runs both A and B
    python null_models.py --model A        # A only
    python null_models.py --model B        # B only
"""

import argparse
import csv
import random
import sys
from collections import defaultdict, Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from config import (
    VERSE_NAMES_CSV, NULL_MODEL_A_OUTPUT_CSV, NULL_MODEL_B_OUTPUT_CSV,
    NULL_MODEL_A_PERMUTATIONS, NULL_MODEL_B_PERMUTATIONS, RANDOM_SEED,
)
from filters import load_verse_names as filtered_load_verse_names, print_filter_report


def load_verse_name_lists(path=VERSE_NAMES_CSV, confident_only=True):
    """
    Returns: dict verse_key -> {'names': [serial,...], 'period': 'Meccan'/'Medinan'/'UNKNOWN'}
    verse_key = (surah_number, ayah_number)
    """
    rows, n_excl, n_total = filtered_load_verse_names(path, confident_only)
    print_filter_report("null_models", n_excl, n_total, confident_only)
    verses = defaultdict(lambda: {"names": [], "period": "UNKNOWN"})
    for row in rows:
        key = (row["surah_number"], row["ayah_number"])
        verses[key]["names"].append(row["name_serial"])
        verses[key]["period"] = row["meccan_medinan"]
    return verses


def observed_pair_counts(verse_lists):
    counts = Counter()
    for v in verse_lists.values():
        names = sorted(set(v["names"]))
        for i in range(len(names)):
            for j in range(i + 1, len(names)):
                counts[(names[i], names[j])] += 1
    return counts


def permute_names_preserving_count(verse_lists, rng):
    """
    Shuffles ALL name tokens across ALL verses in verse_lists, then
    redistributes them back preserving each verse's original name COUNT
    (not identity). This is the corpus-wide null model's core operation.
    """
    all_tokens = []
    counts_per_verse = []
    keys = list(verse_lists.keys())
    for k in keys:
        names = verse_lists[k]["names"]
        counts_per_verse.append(len(names))
        all_tokens.extend(names)

    rng.shuffle(all_tokens)

    new_lists = {}
    cursor = 0
    for k, n in zip(keys, counts_per_verse):
        new_lists[k] = {"names": all_tokens[cursor:cursor + n], "period": verse_lists[k]["period"]}
        cursor += n
    return new_lists


def run_null_model_a(verse_lists, n_permutations, seed, logger=print):
    """
    Corpus-wide permutation. Returns dict (name_a, name_b) -> {observed, p_value, z_score}
    """
    observed = observed_pair_counts(verse_lists)
    logger(f"Observed {len(observed)} unique pairs across {len(verse_lists)} verses.")
    rng = random.Random(seed)

    null_counts = defaultdict(list)  # pair -> list of counts across permutations
    for p in range(n_permutations):
        permuted = permute_names_preserving_count(verse_lists, rng)
        pc = observed_pair_counts(permuted)
        for pair in observed:
            null_counts[pair].append(pc.get(pair, 0))
        if (p + 1) % max(1, n_permutations // 10) == 0:
            logger(f"  ...permutation {p+1}/{n_permutations}")

    results = []
    for pair, obs_count in observed.items():
        dist = null_counts[pair]
        mean = sum(dist) / len(dist)
        var = sum((x - mean) ** 2 for x in dist) / len(dist)
        std = var ** 0.5
        z = (obs_count - mean) / std if std > 0 else float("inf")
        p_value = sum(1 for x in dist if x >= obs_count) / len(dist)
        results.append({
            "name_1_serial": pair[0], "name_2_serial": pair[1],
            "observed_count": obs_count, "null_mean": round(mean, 4),
            "null_std": round(std, 4), "z_score": round(z, 4) if z != float("inf") else "inf",
            "p_value": round(p_value, 6),
            "significant_p05": p_value < 0.05,
        })
    return results


def run_null_model_b(verse_lists, n_permutations, seed, logger=print):
    """
    Period-stratified permutation: split verses by period, run the SAME
    procedure as Model A independently within each period, then also report
    the DIFFERENTIAL (Medinan rate - Meccan rate) with its own null
    distribution — this differential null is what actually tests the
    Jalāl+Jalāl-doubling-style claims, not the within-period p-values alone.
    """
    meccan = {k: v for k, v in verse_lists.items() if v["period"] == "Meccan"}
    medinan = {k: v for k, v in verse_lists.items() if v["period"] == "Medinan"}
    unknown_n = len(verse_lists) - len(meccan) - len(medinan)
    if unknown_n:
        logger(f"WARNING: {unknown_n} verses have UNKNOWN period (quran-data.xml not loaded?) "
               f"— these are EXCLUDED from Null Model B entirely, not guessed into a period.")

    logger(f"Meccan verses: {len(meccan)}, Medinan verses: {len(medinan)}")
    rng = random.Random(seed)

    obs_meccan = observed_pair_counts(meccan)
    obs_medinan = observed_pair_counts(medinan)
    all_pairs = set(obs_meccan) | set(obs_medinan)

    null_meccan = defaultdict(list)
    null_medinan = defaultdict(list)
    for p in range(n_permutations):
        perm_meccan = permute_names_preserving_count(meccan, rng)
        perm_medinan = permute_names_preserving_count(medinan, rng)
        pc_m = observed_pair_counts(perm_meccan)
        pc_d = observed_pair_counts(perm_medinan)
        for pair in all_pairs:
            null_meccan[pair].append(pc_m.get(pair, 0))
            null_medinan[pair].append(pc_d.get(pair, 0))
        if (p + 1) % max(1, n_permutations // 10) == 0:
            logger(f"  ...permutation {p+1}/{n_permutations}")

    results = []
    for pair in all_pairs:
        om = obs_meccan.get(pair, 0)
        od = obs_medinan.get(pair, 0)
        # rates per 1000 verses, so Meccan/Medinan corpora of different sizes are comparable
        rate_m = om / max(1, len(meccan)) * 1000
        rate_d = od / max(1, len(medinan)) * 1000
        observed_diff = rate_d - rate_m

        null_diffs = []
        for nm, nd in zip(null_meccan[pair], null_medinan[pair]):
            nrm = nm / max(1, len(meccan)) * 1000
            nrd = nd / max(1, len(medinan)) * 1000
            null_diffs.append(nrd - nrm)
        null_diffs.sort()
        p_value = sum(1 for x in null_diffs if abs(x) >= abs(observed_diff)) / len(null_diffs)

        results.append({
            "name_1_serial": pair[0], "name_2_serial": pair[1],
            "meccan_count": om, "medinan_count": od,
            "meccan_rate_per_1000v": round(rate_m, 4), "medinan_rate_per_1000v": round(rate_d, 4),
            "observed_differential": round(observed_diff, 4),
            "differential_p_value": round(p_value, 6),
            "significant_p05": p_value < 0.05,
        })
    return results


def write_csv(path, rows):
    if not rows:
        print(f"No rows for {path}, skipping write.")
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)
    print(f"Wrote {len(rows)} rows -> {path}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", choices=["A", "B", "both"], default="both")
    parser.add_argument("--permutations-a", type=int, default=NULL_MODEL_A_PERMUTATIONS)
    parser.add_argument("--permutations-b", type=int, default=NULL_MODEL_B_PERMUTATIONS)
    parser.add_argument("--include-unreviewed", action="store_true",
                         help="Include homonym-flagged/unreviewed names. Default (off) excludes them.")
    args = parser.parse_args()
    confident_only = not args.include_unreviewed

    print("Loading per-verse name occurrences...")
    verse_lists = load_verse_name_lists(confident_only=confident_only)
    print(f"  {len(verse_lists)} verses with >=1 divine name.\n")

    if args.model in ("A", "both"):
        print(f"=== Null Model A: corpus-wide, {args.permutations_a} permutations ===")
        print("(This is slow in pure Python at 10,000 permutations on ~90 pairs —")
        print(" budget several minutes to an hour depending on your machine. If you")
        print(" need it faster, vectorize with numpy; left as pure Python here for")
        print(" auditability over speed, per the project's transparency-first ethos.)")
        results_a = run_null_model_a(verse_lists, args.permutations_a, RANDOM_SEED)
        write_csv(NULL_MODEL_A_OUTPUT_CSV, results_a)
        n_sig = sum(1 for r in results_a if r["significant_p05"])
        print(f"  {n_sig}/{len(results_a)} pairs significant at p<0.05\n")

    if args.model in ("B", "both"):
        print(f"=== Null Model B: period-stratified, {args.permutations_b} permutations ===")
        results_b = run_null_model_b(verse_lists, args.permutations_b, RANDOM_SEED)
        write_csv(NULL_MODEL_B_OUTPUT_CSV, results_b)
        n_sig = sum(1 for r in results_b if r["significant_p05"])
        print(f"  {n_sig}/{len(results_b)} pairs show significant Meccan/Medinan differential at p<0.05")
        print("  ONLY this table supports Meccan/Medinan claims (Appendix A.2.4) — Model A does not.")


if __name__ == "__main__":
    main()
