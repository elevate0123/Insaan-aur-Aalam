# -*- coding: utf-8 -*-
"""
filters.py — Shared "confident subset" filtering for all downstream scripts.

FOUND THIS SESSION: npmi_stats.py, null_models.py, build_network.py, and
motif_analysis.py all consumed dyad_dataset_raw.csv / verse_name_occurrences.csv
directly, with no regard for the needs_hitl_review flag that extract_dyads.py
already computes per row. Result: 58% of dyads were flagged for review (Al-'Alī,
Al-Mu'min, etc.) but EVERY downstream statistic — NPMI, null models, network
centrality, motifs — was still computed on the full, contaminated 100%. Al-'Alī
still showed up as the #2 network hub (982 weighted degree) even after being
correctly flagged, because nothing was actually gated on the flag.

This module fixes that by providing one shared, consistent "confident subset"
across every downstream script, so they can't drift out of sync with each
other the way the ungated versions did.

DEFAULT BEHAVIOR CHANGED (deliberately) from "include everything" to
"exclude flagged rows by default" — given the current state (58% flagged),
defaulting to "include everything" produces obviously misleading results
(all-Unstable centrality, a preposition ranking as a top hub) with no
warning. An explicit --include-unreviewed flag is required to get the old
(unfiltered) behavior back, so nobody gets the misleading numbers silently.

WHAT THIS DOES NOT DO: it does not replace actual HITL review. Excluding a
homonym-flagged name's dyads is conservative (drops real signal along with
the noise — e.g. all of Al-'Azīz's genuine occurrences get excluded too,
not just the Q12:30/51 homonym cases) but not misleading. It buys you
meaningful PROVISIONAL numbers while real review is pending — it is not a
substitute for that review, and every provisional output this produces
should say so explicitly (which the scripts using this module now do).
"""

import csv
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from config import DYAD_OUTPUT_CSV, VERSE_NAMES_CSV, DIVINE_NAMES_CSV


def load_homonym_flagged_serials():
    flagged = set()
    with open(DIVINE_NAMES_CSV, encoding="utf-8") as f:
        for row in csv.DictReader(f):
            if row["C4_Homonym_Flag"].strip().lower() == "yes":
                flagged.add(int(row["A1_Serial_Number"]))
    return flagged


def load_dyads(path=DYAD_OUTPUT_CSV, confident_only=True):
    """
    Loads dyad_dataset_raw.csv. If confident_only=True (default), excludes
    every row where needs_hitl_review == 'True' — this is the SAME flag
    extract_dyads.py already computes (homonym-flagged name, ambiguous
    match, zero-confidence analysis, or suspicious POS tag). Returns
    (rows, n_excluded, n_total) so callers can report what was dropped.
    """
    with open(path, encoding="utf-8") as f:
        all_rows = list(csv.DictReader(f))
    if not confident_only:
        return all_rows, 0, len(all_rows)
    kept = [r for r in all_rows if r.get("needs_hitl_review", "").strip().lower() != "true"]
    return kept, len(all_rows) - len(kept), len(all_rows)


def load_verse_names(path=VERSE_NAMES_CSV, confident_only=True):
    """
    Loads verse_name_occurrences.csv. If confident_only=True (default),
    excludes every occurrence of a name currently flagged C4_Homonym_Flag=Yes
    in the master CSV. This is COARSER than the dyad-level filter above
    (it drops a name's occurrences everywhere, not just in risky pairings)
    — necessary because this file is per-name-occurrence, not per-dyad, so
    there is no needs_hitl_review flag available at this granularity.
    Returns (rows, n_excluded, n_total).
    """
    with open(path, encoding="utf-8") as f:
        all_rows = list(csv.DictReader(f))
    if not confident_only:
        return all_rows, 0, len(all_rows)
    flagged_serials = load_homonym_flagged_serials()
    kept = [r for r in all_rows if int(r["name_serial"]) not in flagged_serials]
    return kept, len(all_rows) - len(kept), len(all_rows)


def print_filter_report(script_name, n_excluded, n_total, confident_only):
    if not confident_only:
        print(f"[{script_name}] --include-unreviewed set: using ALL {n_total} rows, "
              f"INCLUDING homonym-flagged/unreviewed matches. Treat these results as "
              f"provisional-at-best and do not cite them as final — see filters.py docstring.")
    else:
        pct = (n_excluded / n_total * 100) if n_total else 0
        print(f"[{script_name}] Confident-subset mode (default): excluded {n_excluded}/{n_total} "
              f"({pct:.1f}%) rows pending HITL review. This is PROVISIONAL, not final — it is "
              f"conservative (drops some real signal along with the noise) but not misleading. "
              f"Re-run with --include-unreviewed only if you specifically want the unfiltered "
              f"(currently known-contaminated) view, e.g. for debugging.")
