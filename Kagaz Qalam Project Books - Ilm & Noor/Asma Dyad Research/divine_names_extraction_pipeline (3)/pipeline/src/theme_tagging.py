# -*- coding: utf-8 -*-
"""
theme_tagging.py — LLM-assisted macro/micro theme tagging, Dossier §5.9.

Two modes, and the script REFUSES to run --mode full until --mode calibrate
has passed the accuracy threshold. This is a hard gate in code, not a
process you have to remember to follow:

  --mode calibrate   Runs the prompt against data/theme_calibration_GOLD.csv
                      (which YOU must have hand-labeled first — see
                      make_calibration_sets.py). Reports accuracy. Writes a
                      pass/fail marker file that --mode full checks for.

  --mode full         Runs against the full dyad dataset. REFUSES to start
                      if the calibration marker doesn't show a passing run,
                      or if it's stale (calibration file changed since).

Requires ANTHROPIC_API_KEY in your environment. Never put a key in this
repo.

USAGE:
    export ANTHROPIC_API_KEY=sk-...
    python theme_tagging.py --mode calibrate
    # ... review the accuracy report, hand-fix the prompt/examples if <80% ...
    python theme_tagging.py --mode full
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
    THEME_CALIBRATION_CSV, THEME_CALIBRATION_ACCURACY_THRESHOLD,
    THEME_PROMPT_PATH, DYAD_OUTPUT_CSV, THEME_OUTPUT_CSV,
    THEME_DISAGREEMENT_LOG_CSV, OUTPUT_DIR,
)

CALIBRATION_MARKER_PATH = OUTPUT_DIR / ".theme_calibration_passed.json"


def get_client():
    try:
        import anthropic
    except ImportError:
        print("ERROR: pip install anthropic")
        sys.exit(1)
    key = os.environ.get("ANTHROPIC_API_KEY")
    if not key:
        print("ERROR: ANTHROPIC_API_KEY not set in environment. Never hardcode it in this repo.")
        sys.exit(1)
    return anthropic.Anthropic(api_key=key)


def load_prompt():
    if not THEME_PROMPT_PATH.exists():
        print(f"ERROR: {THEME_PROMPT_PATH} not found.")
        sys.exit(1)
    text = THEME_PROMPT_PATH.read_text(encoding="utf-8")
    if "[ADD MORE" in text:
        print(f"WARNING: {THEME_PROMPT_PATH} still contains placeholder few-shot examples.")
        print("  Dossier §5.9 requires 3 real worked examples per macro category (21 total)")
        print("  before scale use. Fill these in from your calibration gold labels first.")
        print("  Proceeding anyway since this is a warning, not a hard block — but the")
        print("  accuracy check below is your real signal, not this warning.")
    return text


def call_claude(client, system_prompt, verse_text, translation, name_1, name_2):
    user_msg = (
        f"Verse: {verse_text}\n"
        f"Translation: {translation}\n"
        f"Divine Name pair in this verse: {name_1} — {name_2}\n\n"
        f"Classify per the instructions."
    )
    resp = client.messages.create(
        model=CLAUDE_MODEL,
        max_tokens=CLAUDE_MAX_TOKENS,
        temperature=CLAUDE_TEMPERATURE,
        system=system_prompt,
        messages=[{"role": "user", "content": user_msg}],
    )
    return resp.content[0].text


def parse_response(text):
    macro, micro, confidence = None, None, None
    for line in text.strip().splitlines():
        line = line.strip()
        if line.upper().startswith("MACRO:"):
            macro = line.split(":", 1)[1].strip()
        elif line.upper().startswith("MICRO:"):
            micro = line.split(":", 1)[1].strip()
        elif line.upper().startswith("CONFIDENCE:"):
            confidence = line.split(":", 1)[1].strip().lower()
    return macro, micro, confidence


def run_calibration(client, system_prompt):
    if not THEME_CALIBRATION_CSV.exists():
        print(f"ERROR: {THEME_CALIBRATION_CSV} not found.")
        print("  Run make_calibration_sets.py first, then hand-label the GOLD columns.")
        sys.exit(1)

    with open(THEME_CALIBRATION_CSV, encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    unlabeled = [r for r in rows if not r.get("GOLD_macro_theme", "").strip()]
    if unlabeled:
        print(f"ERROR: {len(unlabeled)}/{len(rows)} rows in {THEME_CALIBRATION_CSV} have no")
        print("  GOLD_macro_theme filled in. Hand-label ALL rows before running calibration —")
        print("  a partial calibration set doesn't tell you anything reliable about accuracy.")
        sys.exit(1)

    print(f"Running {len(rows)} calibration verses through the LLM (NOTE: this script does not")
    print("re-fetch verse text/translation for you — see the 'context needed' note in README.md")
    print("Step 11; you'll need to join calibration rows to your Tanzil text before this works")
    print("end-to-end, or paste verse text into the calibration CSV yourself.)\n")

    correct_macro, correct_both = 0, 0
    disagreements = []
    for row in rows:
        # NOTE: verse_text/translation are placeholders here — wire up your
        # own Tanzil lookup (quran_source.load_verses) keyed on
        # (surah_number, ayah_number) before running for real.
        verse_text = row.get("verse_text", "[VERSE TEXT NOT WIRED UP — see README Step 11]")
        translation = row.get("translation", "")
        response = call_claude(client, system_prompt, verse_text, translation,
                                row["name_1_translit"], row["name_2_translit"])
        macro, micro, conf = parse_response(response)

        macro_match = (macro == row["GOLD_macro_theme"])
        both_match = macro_match and (micro == row["GOLD_micro_theme"])
        correct_macro += macro_match
        correct_both += both_match
        if not both_match:
            disagreements.append({
                **row, "llm_macro": macro, "llm_micro": micro, "llm_confidence": conf,
            })
        time.sleep(0.5)  # gentle rate limiting

    macro_accuracy = correct_macro / len(rows)
    both_accuracy = correct_both / len(rows)
    print(f"Macro-only accuracy: {macro_accuracy:.1%}")
    print(f"Macro+micro accuracy: {both_accuracy:.1%}")
    print(f"Threshold required: {THEME_CALIBRATION_ACCURACY_THRESHOLD:.0%}\n")

    passed = both_accuracy >= THEME_CALIBRATION_ACCURACY_THRESHOLD

    if disagreements:
        with open(THEME_DISAGREEMENT_LOG_CSV, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=list(disagreements[0].keys()))
            writer.writeheader()
            writer.writerows(disagreements)
        print(f"Wrote {len(disagreements)} disagreements -> {THEME_DISAGREEMENT_LOG_CSV}")

    # Marker file records a hash of the calibration CSV + prompt file, so
    # --mode full can detect staleness (calibration file edited after the
    # passing run) rather than trusting an old pass forever.
    calib_hash = hashlib.sha256(
        THEME_CALIBRATION_CSV.read_bytes() + THEME_PROMPT_PATH.read_bytes()
    ).hexdigest()
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    with open(CALIBRATION_MARKER_PATH, "w") as f:
        json.dump({
            "passed": passed, "macro_accuracy": macro_accuracy, "both_accuracy": both_accuracy,
            "threshold": THEME_CALIBRATION_ACCURACY_THRESHOLD, "input_hash": calib_hash,
        }, f)

    if passed:
        print("PASSED. You may now run --mode full.")
    else:
        print("FAILED threshold. Review theme_disagreement_log.csv, revise the prompt")
        print(f"(edit {THEME_PROMPT_PATH} or bump to v2 and update config.py), and re-run")
        print("calibration. --mode full will refuse to run until this passes.")
    return passed


def run_full(client, system_prompt):
    if not CALIBRATION_MARKER_PATH.exists():
        print("ERROR: no calibration run found. Run --mode calibrate first (this is a hard")
        print("gate, not a suggestion — Dossier §5.9 requires it).")
        sys.exit(1)
    with open(CALIBRATION_MARKER_PATH) as f:
        marker = json.load(f)
    if not marker["passed"]:
        print(f"ERROR: last calibration run FAILED ({marker['both_accuracy']:.1%} < "
              f"{marker['threshold']:.0%}). Fix the prompt and pass calibration before "
              f"running the full corpus.")
        sys.exit(1)
    calib_hash_now = hashlib.sha256(
        THEME_CALIBRATION_CSV.read_bytes() + THEME_PROMPT_PATH.read_bytes()
    ).hexdigest()
    if calib_hash_now != marker["input_hash"]:
        print("ERROR: calibration file or prompt changed since the last passing run.")
        print("Re-run --mode calibrate to confirm the change didn't break accuracy.")
        sys.exit(1)

    print(f"Calibration passed at {marker['both_accuracy']:.1%} (fresh, hash-verified).")
    print("Proceeding to full-corpus tagging. This calls the API once per dyad — check")
    print("your Anthropic usage/cost dashboard; Dossier §12.2 estimates $10-30 for ~177")
    print("verses, but your actual corpus size may differ from that estimate.\n")

    with open(DYAD_OUTPUT_CSV, encoding="utf-8") as f:
        dyads = list(csv.DictReader(f))

    results = []
    for i, row in enumerate(dyads):
        verse_text = row.get("verse_text", "[WIRE UP quran_source lookup — see README Step 11]")
        translation = row.get("translation", "")
        response = call_claude(client, system_prompt, verse_text, translation,
                                row["name_1_translit"], row["name_2_translit"])
        macro, micro, conf = parse_response(response)
        results.append({
            **row, "llm_macro_theme": macro, "llm_micro_theme": micro,
            "llm_confidence": conf, "hitl_reviewed": False, "hitl_final_macro": "",
            "hitl_final_micro": "", "hitl_reviewer_notes": "",
        })
        if (i + 1) % 20 == 0:
            print(f"  ...{i+1}/{len(dyads)}")
        time.sleep(0.5)

    THEME_OUTPUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    with open(THEME_OUTPUT_CSV, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(results[0].keys()))
        writer.writeheader()
        writer.writerows(results)
    print(f"\nWrote {len(results)} LLM first-pass tags -> {THEME_OUTPUT_CSV}")
    print("MANDATORY NEXT STEP (§5.9): 100% researcher HITL review of every row against")
    print("tafsir sources. Fill in hitl_final_macro/hitl_final_micro/hitl_reviewer_notes")
    print("and set hitl_reviewed=True. The llm_* columns are NEVER primary evidence on")
    print("their own — this is a first-pass suggestion only, per project policy.")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=["calibrate", "full"], required=True)
    args = parser.parse_args()

    client = get_client()
    system_prompt = load_prompt()

    if args.mode == "calibrate":
        run_calibration(client, system_prompt)
    else:
        run_full(client, system_prompt)


if __name__ == "__main__":
    main()
