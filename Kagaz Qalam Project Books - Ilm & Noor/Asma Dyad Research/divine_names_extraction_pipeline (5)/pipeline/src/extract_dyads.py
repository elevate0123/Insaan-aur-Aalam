# -*- coding: utf-8 -*-
"""
extract_dyads.py — Main extraction pipeline.

Implements Dossier v2.1 §5.3 (Morphologically-Normalized Extraction):
  1. Parse Tanzil XML -> verses
  2. CAMeL Tools morphological analysis -> normalized lemma per token
  3. Match normalized lemmas against the divine-names list
  4. Compute word-distance between matches within the same verse
  5. Classify grammatical position (verse-opening / mid-verse / verse-final)
  6. Flag homonym-risk names for mandatory HITL review
  7. Emit the primary dataset + a separate HITL review queue

USAGE:
    python extract_dyads.py                      # primary threshold (config.py)
    python extract_dyads.py --threshold 7         # override threshold
    python extract_dyads.py --limit-surah 12      # debug: one surah only

OUTPUT SCHEMA (output/dyad_dataset_raw.csv):
    Matches Dossier §5.3 Column Groups A-C, I, L (D/E/F/G/H/J/K need the
    downstream JJK/theme/statistical/HITL scripts this pipeline hands off
    to — see README.md "What this pipeline does NOT do").
"""

import argparse
import csv
import logging
import sys
from collections import defaultdict
from itertools import combinations
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from config import (
    PRIMARY_DISTANCE_THRESHOLD, DYAD_OUTPUT_CSV, HITL_QUEUE_CSV,
    REFRAIN_OUTPUT_CSV, REFRAIN_MIN_OCCURRENCES, EXTRACTION_LOG_PATH,
    FORCE_HOMONYM_REVIEW, HOMONYM_CONTEXT_WINDOW, OUTPUT_DIR, LOG_DIR,
    VERSE_NAMES_CSV, SUSPICIOUS_POS_TAGS,
)
from quran_source import load_verses, load_meccan_medinan
from morphology import MorphAnalyzer
from names_loader import load_divine_names, build_lemma_index, DivineName

# Names whose Tier is "Tier 3" (documented exclusions) match but are routed
# here instead of the primary dataset, unless you deliberately reactivate
# them. See names_loader.py docstring.
TIER3_POLICY = "exclude_from_primary"  # or "include_flagged"


def setup_logging():
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s  %(levelname)-8s  %(message)s",
        handlers=[
            logging.FileHandler(EXTRACTION_LOG_PATH, encoding="utf-8"),
            logging.StreamHandler(sys.stdout),
        ],
    )
    return logging.getLogger("extract_dyads")


def classify_position(idx: int, verse_token_count: int) -> str:
    """
    verse-opening: token is among the first 2 tokens of the verse
    verse-final:   token is among the last 2 tokens of the verse
    mid-verse:     everything else
    (2-token windows account for a trailing/leading particle or connective
    commonly attached before/after a name; adjust WINDOW below if your
    HITL review shows this over- or under-catches in practice.)
    """
    WINDOW = 2
    if idx < WINDOW:
        return "verse-opening"
    if idx >= verse_token_count - WINDOW:
        return "verse-final"
    return "mid-verse"


def find_name_matches(tokens, lemma_index):
    """
    Returns a list of (token_index, [DivineName,...]) for every token that
    matched one or more divine names. Multiple matches at one position means
    genuine ambiguity (e.g. shared-root collisions) — NOT resolved here;
    flagged downstream for HITL.
    """
    matches = []
    for tok in tokens:
        hits = lemma_index.get(tok.normalized)
        if hits:
            matches.append((tok, hits))
    return matches


def process_verse(verse, tokens, lemma_index, threshold, logger):
    """
    Returns (dyad_rows, hitl_rows) for a single verse.
    Dyads are formed from every pair of distinct name-matches within the
    verse whose word-distance <= threshold, per Dossier §5.7 sensitivity
    analysis design — this function is called once per threshold value by
    run_sensitivity.py, and once at PRIMARY_DISTANCE_THRESHOLD by main().
    """
    dyad_rows, hitl_rows = [], []
    matches = find_name_matches(tokens, lemma_index)

    if len(matches) < 2:
        return dyad_rows, hitl_rows

    for (tok_a, names_a), (tok_b, names_b) in combinations(matches, 2):
        distance = abs(tok_b.position_in_verse - tok_a.position_in_verse)
        if distance > threshold:
            continue  # SKIP_DISTANCE, per extraction_log.txt convention

        for name_a in names_a:
            for name_b in names_b:
                if name_a.serial == name_b.serial:
                    continue  # same name repeated is not a dyad

                needs_review = (
                    (FORCE_HOMONYM_REVIEW and (name_a.homonym_flag or name_b.homonym_flag))
                    or (tok_a.confidence == 0.0 or tok_b.confidence == 0.0)
                    or (len(names_a) > 1 or len(names_b) > 1)
                    or (tok_a.pos_guess in SUSPICIOUS_POS_TAGS or tok_b.pos_guess in SUSPICIOUS_POS_TAGS)
                )

                row = {
                    "surah_number": verse.surah_number,
                    "surah_name": verse.surah_name,
                    "ayah_number": verse.ayah_number,
                    "verse_text": verse.text,  # ADDED after real-run review showed HITL rows
                                                # were unreviewable without the actual verse —
                                                # reviewers should not have to look this up separately
                    "name_1_serial": name_a.serial,
                    "name_1_arabic": name_a.arabic,
                    "name_1_translit": name_a.transliteration,
                    "name_1_tier": name_a.tier,
                    "name_2_serial": name_b.serial,
                    "name_2_arabic": name_b.arabic,
                    "name_2_translit": name_b.transliteration,
                    "name_2_tier": name_b.tier,
                    "word_distance": distance,
                    "position_name1": classify_position(tok_a.position_in_verse, len(tokens)),
                    "position_name2": classify_position(tok_b.position_in_verse, len(tokens)),
                    "meccan_medinan": verse.meccan_medinan,
                    "needs_hitl_review": needs_review,
                    "tier3_involved": (name_a.tier == "Tier 3" or name_b.tier == "Tier 3"),
                }

                if row["tier3_involved"] and TIER3_POLICY == "exclude_from_primary":
                    hitl_rows.append({**row, "review_reason": "Tier 3 name matched — policy-excluded from primary dataset, verify"})
                    continue

                if needs_review:
                    ctx_lo = max(0, min(tok_a.position_in_verse, tok_b.position_in_verse) - HOMONYM_CONTEXT_WINDOW)
                    ctx_hi = min(len(tokens), max(tok_a.position_in_verse, tok_b.position_in_verse) + HOMONYM_CONTEXT_WINDOW + 1)
                    context = " ".join(t.surface_form for t in tokens[ctx_lo:ctx_hi])
                    reason = []
                    if name_a.homonym_flag or name_b.homonym_flag:
                        reason.append("homonym-flagged name")
                    if tok_a.confidence == 0.0 or tok_b.confidence == 0.0:
                        reason.append("no morphological analysis found (low confidence)")
                    if len(names_a) > 1 or len(names_b) > 1:
                        reason.append("ambiguous lemma match (multiple candidate names)")
                    if tok_a.pos_guess in SUSPICIOUS_POS_TAGS or tok_b.pos_guess in SUSPICIOUS_POS_TAGS:
                        reason.append(f"suspicious POS tag (pos1={tok_a.pos_guess}, pos2={tok_b.pos_guess}) — likely non-nominal usage")
                    hitl_rows.append({**row, "review_reason": "; ".join(reason), "context": context})

                dyad_rows.append(row)

    return dyad_rows, hitl_rows


def detect_refrains(dyad_rows, confident_only=True):
    """
    Flags (surah, name_pair) combinations occurring >= REFRAIN_MIN_OCCURRENCES
    times as structural refrains, per Dossier §5.7 / Appendix A.2.20. These
    stay IN the primary dataset (refrain_type column is set, nothing is
    dropped) — exclusion from theme chi-square happens in the downstream
    statistics script, not here, per the dossier's explicit instruction that
    refrains are case-studies, not noise.

    BUGFIX (found via first real corpus run): the grouping key MUST use an
    unordered (canonical/sorted) name pair, not (name_1_serial, name_2_serial)
    as stored per-row. Per-row name_1/name_2 reflects POSITION IN VERSE
    (whichever name appears first) and legitimately varies verse-to-verse for
    the same semantic pair — grouping on the raw ordered tuple would silently
    split a single real refrain (e.g. Al-'Azīz-Al-Ḥakīm repeating 9x in Surah
    26) into two undercounted buckets if even one occurrence had the names in
    the opposite order. Direction is still preserved per-row (untouched) —
    only the GROUPING key is canonicalized here.

    SECOND BUGFIX (found via THIRD real run — this function was missed when
    filters.py was wired into npmi_stats.py/null_models.py/build_network.py/
    motif_analysis.py): confident_only=True by default now excludes rows
    flagged needs_hitl_review, same policy as everywhere else. Before this
    fix, the false "Allāh+Al-'Alī" pairing (a preposition collision, see
    README "Second incident") was showing up as a 77-occurrence "refrain" in
    Surah 2 alone — impossible for a genuine literary refrain (the one
    confirmed real case, Al-'Azīz-Al-Raḥīm in Surah 26, is n=9) but nothing
    was filtering it out of this specific function even after the other four
    scripts were fixed. Pass confident_only=False to restore old (unfiltered,
    currently-misleading) behavior.
    """
    if confident_only:
        n_before = len(dyad_rows)
        dyad_rows = [r for r in dyad_rows if str(r.get("needs_hitl_review", "")).strip().lower() != "true"]
        print(f"[detect_refrains] Confident-subset mode: excluded {n_before - len(dyad_rows)}/{n_before} "
              f"flagged rows before refrain detection.")

    counts = defaultdict(list)
    for row in dyad_rows:
        pair_key = tuple(sorted((row["name_1_serial"], row["name_2_serial"])))
        key = (row["surah_number"], pair_key[0], pair_key[1])
        counts[key].append(row)

    refrains = []
    for key, rows in counts.items():
        if len(rows) >= REFRAIN_MIN_OCCURRENCES:
            for row in rows:
                row["refrain_type"] = f"refrain_surah{key[0]}_n{len(rows)}"
            refrains.append({
                "surah_number": key[0], "name_1_serial": key[1], "name_2_serial": key[2],
                "occurrence_count": len(rows),
                "ayahs": ",".join(str(r["ayah_number"]) for r in rows),
            })
    for row in dyad_rows:
        row.setdefault("refrain_type", "")
    return refrains


def write_csv(path, rows, logger):
    if not rows:
        logger.warning(f"No rows to write for {path} — writing header-only file.")
    path.parent.mkdir(parents=True, exist_ok=True)
    all_keys = []
    seen = set()
    for r in rows:
        for k in r:
            if k not in seen:
                seen.add(k)
                all_keys.append(k)
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=all_keys)
        writer.writeheader()
        writer.writerows(rows)
    logger.info(f"Wrote {len(rows)} rows -> {path}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--threshold", type=int, default=PRIMARY_DISTANCE_THRESHOLD)
    parser.add_argument("--limit-surah", type=int, default=None, help="Debug: process one surah only")
    parser.add_argument("--out", type=Path, default=DYAD_OUTPUT_CSV)
    parser.add_argument("--hitl-out", type=Path, default=HITL_QUEUE_CSV)
    parser.add_argument("--refrain-out", type=Path, default=REFRAIN_OUTPUT_CSV)
    parser.add_argument("--include-unreviewed-in-refrains", action="store_true",
                         help="Don't exclude flagged/homonym-risk rows from refrain detection. "
                              "Default (off) excludes them — see detect_refrains() docstring, "
                              "'Second bugfix', re: the false Allāh+Al-'Alī 77x 'refrain'.")
    args = parser.parse_args()

    logger = setup_logging()
    logger.info(f"=== Extraction run starting: threshold={args.threshold} ===")

    logger.info("Loading divine names master list...")
    names = load_divine_names()
    lemma_index = build_lemma_index(names)
    logger.info(f"Loaded {len(names)} names, {len(lemma_index)} unique normalized lemma keys.")
    collisions = {k: v for k, v in lemma_index.items() if len(v) > 1}
    if collisions:
        logger.warning(f"{len(collisions)} normalized-lemma collisions across distinct names (expected — these route to HITL on match):")
        for k, v in collisions.items():
            logger.warning(f"    {k!r} -> {[n.transliteration for n in v]}")

    logger.info("Loading Qur'an corpus...")
    verses = load_verses()
    verses = load_meccan_medinan(verses)
    if args.limit_surah:
        verses = [v for v in verses if v.surah_number == args.limit_surah]
    logger.info(f"Loaded {len(verses)} verses.")

    logger.info(f"Loading CAMeL Tools morphology DB ({args.threshold=})... this can take ~10-30s.")
    analyzer = MorphAnalyzer()

    all_dyads, all_hitl, verse_name_rows = [], [], []
    for i, verse in enumerate(verses):
        tokens = analyzer.analyze_verse(verse.text)
        dyads, hitl = process_verse(verse, tokens, lemma_index, args.threshold, logger)
        all_dyads.extend(dyads)
        all_hitl.extend(hitl)

        # Record every name occurrence in this verse (not just paired ones) —
        # Null Models A and B (§5.7/5.8) need the FULL per-verse name
        # inventory to permute correctly, not just the dyads that survived
        # the distance threshold. A name that occurs alone in a verse (no
        # partner within threshold) still counts toward that verse's name
        # inventory for permutation purposes.
        matches = find_name_matches(tokens, lemma_index)
        for tok, names in matches:
            for name in names:
                verse_name_rows.append({
                    "surah_number": verse.surah_number,
                    "ayah_number": verse.ayah_number,
                    "meccan_medinan": verse.meccan_medinan,
                    "name_serial": name.serial,
                    "name_translit": name.transliteration,
                    "position_in_verse": tok.position_in_verse,
                })

        if (i + 1) % 500 == 0:
            logger.info(f"  ...processed {i+1}/{len(verses)} verses, {len(all_dyads)} dyads so far")

    refrain_confident_only = not args.include_unreviewed_in_refrains
    refrains = detect_refrains(all_dyads, confident_only=refrain_confident_only)
    logger.info(f"Detected {len(refrains)} structural refrain patterns (>= {REFRAIN_MIN_OCCURRENCES} occurrences).")

    write_csv(args.out, all_dyads, logger)
    write_csv(args.hitl_out, all_hitl, logger)
    refrain_out_path = args.refrain_out if refrain_confident_only else args.refrain_out.with_name(
        args.refrain_out.stem + "_UNREVIEWED_INCLUDED" + args.refrain_out.suffix)
    write_csv(refrain_out_path, refrains, logger)
    write_csv(VERSE_NAMES_CSV, verse_name_rows, logger)

    logger.info("=== Done. Summary ===")
    logger.info(f"  Total dyads extracted:        {len(all_dyads)}")
    logger.info(f"  Routed to HITL review queue:  {len(all_hitl)}")
    logger.info(f"  Structural refrains detected: {len(refrains)}")
    logger.info(f"  NEXT STEP: open {args.hitl_out} and manually review every row before")
    logger.info(f"  treating {args.out} as final — see README.md 'After running' section.")


if __name__ == "__main__":
    main()
