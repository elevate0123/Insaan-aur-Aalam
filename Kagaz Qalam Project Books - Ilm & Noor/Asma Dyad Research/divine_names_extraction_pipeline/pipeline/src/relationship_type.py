# -*- coding: utf-8 -*-
"""
relationship_type.py — Dyad Relationship Type Classification, Dossier §5.5.

IMPORTANT DESIGN NOTE: the decision tree's Q1-Q3 are MECHANICALLY
DERIVABLE from data we already have (JJK 5-class + Arabic root), so this
script applies them deterministically — no LLM call, no ambiguity, no
HITL needed for these branches. Only when Q1-Q3 fall through to the
Q4/Q5 branch (different JJK classes, not an opposing Jalal+Jamal pair) does
this script call Claude for a first-pass suggestion, per relationship_
type_prompt_v1.txt — and even then, every answer is still HITL-reviewed.

This split matters: the dossier's IRR requirement (kappa >= 0.65) is about
testing whether TWO HUMANS agree on the genuinely judgment-based part of
the tree, not about re-litigating Q1-Q3, which are not judgment calls at
all once the JJK classification is settled.

DECISION TREE (Dossier §5.5):
    Q1: Same JJK class?
        YES -> Q2: near-synonymous (shared root)?
            YES -> INTENSIFYING
            NO  -> REINFORCING
        NO  -> Q3: opposing poles (Jalal + Jamal)?
            YES -> BALANCING
            NO  -> [Q4/Q5 branch -> LLM-assisted, see relationship_type_prompt_v1.txt]

MODES:
    --mode calibrate   Runs against relationship_calibration_GOLD.csv,
                        computes Cohen's kappa between the GOLD column and
                        this script's own output (mechanical + LLM-assisted).
                        NOTE: true IRR per §5.5 needs a SECOND independent
                        human annotator's labels compared against the FIRST
                        human's — this script can only check "does the
                        pipeline agree with one human," which is a
                        different (necessary but not sufficient) check.
                        See README.md Step 12 for the real IRR procedure.
    --mode full         Runs against the full dyad dataset. Same calibration
                        gate pattern as theme_tagging.py.

USAGE:
    python relationship_type.py --mode calibrate
    python relationship_type.py --mode full
"""

import argparse
import csv
import hashlib
import json
import os
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from config import (
    CLAUDE_MODEL, CLAUDE_MAX_TOKENS, CLAUDE_TEMPERATURE,
    RELATIONSHIP_CALIBRATION_CSV, RELATIONSHIP_IRR_KAPPA_THRESHOLD,
    RELATIONSHIP_PROMPT_PATH, DYAD_OUTPUT_CSV, RELATIONSHIP_OUTPUT_CSV,
    RELATIONSHIP_CALIBRATION_RESULTS_CSV, DIVINE_NAMES_CSV, OUTPUT_DIR,
)

CALIBRATION_MARKER_PATH = OUTPUT_DIR / ".relationship_calibration_passed.json"

JALAL, JAMAL = "Jalāl", "Jamāl"


def load_names_lookup():
    lookup = {}
    with open(DIVINE_NAMES_CSV, encoding="utf-8") as f:
        for row in csv.DictReader(f):
            lookup[int(row["A1_Serial_Number"])] = {
                "jjk": row["H1_JJK_5Class_v2_1"], "root": row["A5_Arabic_Root"].strip(),
            }
    return lookup


def deterministic_classify(name_1_info, name_2_info):
    """
    Applies Q1-Q3 mechanically. Returns a relationship type string if
    resolved, or None if it falls through to the Q4/Q5 (LLM-assisted) branch.
    Also returns which question resolved it, for audit purposes.
    """
    jjk1, jjk2 = name_1_info["jjk"], name_2_info["jjk"]

    if jjk1 in ("Disputed",) or jjk2 in ("Disputed",):
        return None, "Q1_UNRESOLVABLE_DISPUTED_NODE"

    # Q1: same JJK class? (treat Kamal-epistemic and Kamal-ontological as
    # DIFFERENT classes for this purpose — they are meaningfully distinct
    # sub-categories per the v2.1 split, Appendix A.2.2; do not silently
    # collapse them back to one "Kamal" bucket here.)
    if jjk1 == jjk2:
        # Q2: near-synonymous (shared root)?
        if name_1_info["root"] and name_1_info["root"] == name_2_info["root"]:
            return "INTENSIFYING", "Q2_SHARED_ROOT"
        return "REINFORCING", "Q1_SAME_CLASS_DIFFERENT_ROOT"

    # Q3: opposing poles (Jalal + Jamal)?
    if {jjk1, jjk2} == {JALAL, JAMAL}:
        return "BALANCING", "Q3_OPPOSING_POLES"

    # Falls through to Q4/Q5 — needs semantic judgment, not mechanical.
    return None, "FALLTHROUGH_TO_Q4Q5"


def get_client():
    try:
        import anthropic
    except ImportError:
        print("ERROR: pip install anthropic")
        sys.exit(1)
    key = os.environ.get("ANTHROPIC_API_KEY")
    if not key:
        print("ERROR: ANTHROPIC_API_KEY not set.")
        sys.exit(1)
    return anthropic.Anthropic(api_key=key)


def call_claude_q4q5(client, system_prompt, name_1, name_2, verse_text, translation):
    user_msg = (
        f"Names: {name_1} - {name_2}\nVerse: {verse_text}\nTranslation: {translation}\n\n"
        f"Apply the Q4/Q5 branch as instructed."
    )
    resp = client.messages.create(
        model=CLAUDE_MODEL, max_tokens=CLAUDE_MAX_TOKENS, temperature=CLAUDE_TEMPERATURE,
        system=system_prompt, messages=[{"role": "user", "content": user_msg}],
    )
    text = resp.content[0].text
    answer, reasoning, confidence = None, None, None
    for line in text.strip().splitlines():
        line = line.strip()
        if line.upper().startswith("ANSWER:"):
            answer = line.split(":", 1)[1].strip()
        elif line.upper().startswith("REASONING:"):
            reasoning = line.split(":", 1)[1].strip()
        elif line.upper().startswith("CONFIDENCE:"):
            confidence = line.split(":", 1)[1].strip().lower()
    return answer, reasoning, confidence


def cohens_kappa(labels_a, labels_b):
    """Simple unweighted Cohen's kappa for categorical agreement."""
    from collections import Counter
    n = len(labels_a)
    agree = sum(1 for a, b in zip(labels_a, labels_b) if a == b)
    p_o = agree / n

    cats = set(labels_a) | set(labels_b)
    count_a = Counter(labels_a)
    count_b = Counter(labels_b)
    p_e = sum((count_a.get(c, 0) / n) * (count_b.get(c, 0) / n) for c in cats)

    if p_e == 1.0:
        return 1.0
    return (p_o - p_e) / (1 - p_e)


def classify_one(row, names_lookup, client, prompt):
    n1 = names_lookup.get(int(row["name_1_serial"]))
    n2 = names_lookup.get(int(row["name_2_serial"]))
    result, path = deterministic_classify(n1, n2)
    llm_reasoning, llm_confidence = "", ""
    if result is None and path == "FALLTHROUGH_TO_Q4Q5":
        verse_text = row.get("verse_text", "[WIRE UP verse lookup — see README Step 11]")
        translation = row.get("translation", "")
        result, llm_reasoning, llm_confidence = call_claude_q4q5(
            client, prompt, row["name_1_translit"], row["name_2_translit"], verse_text, translation
        )
        time.sleep(0.5)
    elif result is None and path == "Q1_UNRESOLVABLE_DISPUTED_NODE":
        result = "UNRESOLVED_DISPUTED_NODE"
    return result, path, llm_reasoning, llm_confidence


def run_calibration(names_lookup, client, prompt):
    if not RELATIONSHIP_CALIBRATION_CSV.exists():
        print(f"ERROR: {RELATIONSHIP_CALIBRATION_CSV} not found. Run make_calibration_sets.py first.")
        sys.exit(1)
    with open(RELATIONSHIP_CALIBRATION_CSV, encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    unlabeled = [r for r in rows if not r.get("GOLD_relationship_type", "").strip()]
    if unlabeled:
        print(f"ERROR: {len(unlabeled)}/{len(rows)} rows have no GOLD_relationship_type. Label all first.")
        sys.exit(1)

    pipeline_labels, gold_labels, results = [], [], []
    for row in rows:
        result, path, reasoning, conf = classify_one(row, names_lookup, client, prompt)
        pipeline_labels.append(result)
        gold_labels.append(row["GOLD_relationship_type"])
        results.append({**row, "pipeline_result": result, "decision_path": path,
                         "llm_reasoning": reasoning, "llm_confidence": conf})

    kappa = cohens_kappa(pipeline_labels, gold_labels)
    print(f"Cohen's kappa (pipeline vs. your GOLD labels): {kappa:.3f}")
    print(f"Threshold: {RELATIONSHIP_IRR_KAPPA_THRESHOLD}")
    print()
    print("⚠️  REMINDER: this is pipeline-vs-single-human agreement, NOT the true IRR")
    print("   the dossier specifies (two INDEPENDENT human annotators, principal")
    print("   researcher + Islamic Studies consultant, both blind to each other's")
    print("   labels). Once the consultant labels this same 30-dyad set independently,")
    print("   compute cohens_kappa() on THEIR TWO label columns directly — that's the")
    print("   number that actually satisfies §5.5's kappa>=0.65 requirement. This")
    print("   script's number is a useful sanity check, not a substitute.\n")

    passed = kappa >= RELATIONSHIP_IRR_KAPPA_THRESHOLD
    RELATIONSHIP_CALIBRATION_RESULTS_CSV.parent.mkdir(parents=True, exist_ok=True)
    with open(RELATIONSHIP_CALIBRATION_RESULTS_CSV, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(results[0].keys()))
        writer.writeheader()
        writer.writerows(results)
    print(f"Wrote details -> {RELATIONSHIP_CALIBRATION_RESULTS_CSV}")

    calib_hash = hashlib.sha256(
        RELATIONSHIP_CALIBRATION_CSV.read_bytes() + RELATIONSHIP_PROMPT_PATH.read_bytes()
    ).hexdigest()
    with open(CALIBRATION_MARKER_PATH, "w") as f:
        json.dump({"passed": passed, "kappa": kappa, "input_hash": calib_hash}, f)

    print("PASSED" if passed else "FAILED — revise decision tree / prompt before --mode full")
    return passed


def run_full(names_lookup, client, prompt):
    if not CALIBRATION_MARKER_PATH.exists():
        print("ERROR: run --mode calibrate first.")
        sys.exit(1)
    with open(CALIBRATION_MARKER_PATH) as f:
        marker = json.load(f)
    if not marker["passed"]:
        print(f"ERROR: last calibration FAILED (kappa={marker['kappa']:.3f}). Fix before full run.")
        sys.exit(1)

    with open(DYAD_OUTPUT_CSV, encoding="utf-8") as f:
        dyads = list(csv.DictReader(f))

    results = []
    n_mechanical, n_llm = 0, 0
    for i, row in enumerate(dyads):
        result, path, reasoning, conf = classify_one(row, names_lookup, client, prompt)
        if "FALLTHROUGH" in path:
            n_llm += 1
        else:
            n_mechanical += 1
        results.append({**row, "relationship_type": result, "decision_path": path,
                         "llm_reasoning": reasoning, "llm_confidence": conf,
                         "hitl_reviewed": False, "hitl_final_type": ""})
        if (i + 1) % 50 == 0:
            print(f"  ...{i+1}/{len(dyads)}")

    RELATIONSHIP_OUTPUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    with open(RELATIONSHIP_OUTPUT_CSV, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(results[0].keys()))
        writer.writeheader()
        writer.writerows(results)
    print(f"\nWrote {len(results)} classifications -> {RELATIONSHIP_OUTPUT_CSV}")
    print(f"  {n_mechanical} resolved mechanically (Q1-Q3, no LLM call, no ambiguity)")
    print(f"  {n_llm} required the Q4/Q5 LLM-assisted branch — these need HITL review")
    print(f"  first; the mechanical ones are lower-risk but still worth spot-checking.")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=["calibrate", "full"], required=True)
    args = parser.parse_args()

    names_lookup = load_names_lookup()
    client = get_client()
    prompt = RELATIONSHIP_PROMPT_PATH.read_text(encoding="utf-8")

    if args.mode == "calibrate":
        run_calibration(names_lookup, client, prompt)
    else:
        run_full(names_lookup, client, prompt)


if __name__ == "__main__":
    main()
