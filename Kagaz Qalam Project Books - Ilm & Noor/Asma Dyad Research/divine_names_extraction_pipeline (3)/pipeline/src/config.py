# -*- coding: utf-8 -*-
"""
config.py — Central configuration for the Divine Name Dyad Extraction Pipeline.

Edit the paths in this file to match your local environment before running
anything else. Nothing here talks to the network; all inputs are local files.
"""

from pathlib import Path

# ── Paths ────────────────────────────────────────────────────────────────
# Project root = the folder that contains data/, src/, output/, logs/
ROOT = Path(__file__).resolve().parent.parent

DATA_DIR = ROOT / "data"
OUTPUT_DIR = ROOT / "output"
LOG_DIR = ROOT / "logs"

# You must download this yourself (see README.md, Step 2). Tanzil's
# quran-uthmani.xml or quran-simple.xml both work; uthmani is closer to the
# riwāyat Ḥafṣ ʿan ʿĀṣim orthography the dossier commits to using.
TANZIL_XML_PATH = DATA_DIR / "quran-uthmani.xml"

# Exported from Master_Divine_Names_Dataset_v2_1.xlsx -> "Master Name List"
# sheet. Already generated for you as divine_names_master.csv — re-export
# it from the workbook any time the master list changes.
DIVINE_NAMES_CSV = DATA_DIR / "divine_names_master.csv"

# Where results land.
DYAD_OUTPUT_CSV = OUTPUT_DIR / "dyad_dataset_raw.csv"
SENSITIVITY_OUTPUT_CSV = OUTPUT_DIR / "sensitivity_analysis.csv"
HITL_QUEUE_CSV = OUTPUT_DIR / "hitl_review_queue.csv"
REFRAIN_OUTPUT_CSV = OUTPUT_DIR / "structural_refrains.csv"
EXTRACTION_LOG_PATH = LOG_DIR / "extraction_run.log"

# ── Dyad definition parameters (Dossier v2.1 §5.7, Appendix A.2.17) ───────
# Primary threshold used for the main dataset. The dossier's own sensitivity
# analysis requirement means you should ALSO run extract_dyads.py once per
# value in SENSITIVITY_THRESHOLDS and diff the results — run_sensitivity.py
# does this for you automatically.
PRIMARY_DISTANCE_THRESHOLD = 10
SENSITIVITY_THRESHOLDS = [5, 7, 10, 15]

# A dyad may not cross a verse boundary — this is fixed, not configurable,
# per the dossier's own operational definition (Appendix A.3, "What did NOT
# change"). Do not add a cross-verse mode without updating the dossier's
# methodology section first — every paper's methodology text asserts this.
ALLOW_CROSS_VERSE_DYADS = False

# Refrain detection: same surah, same ordered name-pair, occurring at least
# this many times, is flagged as a structural refrain candidate (Dossier
# §5.7/Appendix A.2.20) rather than an independent contextual deployment.
REFRAIN_MIN_OCCURRENCES = 3

# ── CAMeL Tools model ───────────────────────────────────────────────────
# CAMeL Tools ships MSA (Modern Standard Arabic) analyzers by default; there
# is no first-party Classical/Quranic-Arabic-specific morphological database.
# calima-msa-r13 is the closest available and handles the shared root/pattern
# system reasonably, but WILL mis-analyze some Classical-Arabic-only forms
# (certain energetic moods, archaic case endings, some construct-state edge
# cases). See README.md "Known limitation" section before trusting edge
# cases blindly — cross-validate flagged low-confidence tokens against the
# Qur'anic Arabic Corpus (corpus.quran.com), which IS purpose-built for
# Quranic morphology and is already a listed project resource.
CAMEL_DB_NAME = "calima-msa-r13"

# Minimum CAMeL Tools analysis confidence/score before a match is trusted
# without a manual-review flag. Below this, the token is still matched (if
# it matches a name) but routed to the HITL review queue with a low-
# confidence flag rather than silently accepted.
MIN_ANALYSIS_CONFIDENCE = 0.15  # camel-tools MLE scores are often small; see README

# ── Homonym handling ────────────────────────────────────────────────────
# Names flagged C4_Homonym_Flag=Yes in the master CSV are NEVER auto-accepted
# even at high analyzer confidence — they always route to HITL review with
# the surrounding context (±5 tokens) attached, per Dossier §5.2.3.
FORCE_HOMONYM_REVIEW = True
HOMONYM_CONTEXT_WINDOW = 5  # tokens on each side, for the reviewer to read

# Real-run finding: Al-'Alī (#37) collided catastrophically with the
# preposition 'ʿalā' (على, "upon/on") after alef-maksūra normalization —
# 1241 raw matches, dominating as a false "refrain" in nearly every surah.
# The dossier's own design (§5.3 step 4) calls for using CAMeL's syntactic-
# role tag to distinguish nominal/proper-noun usage from other parts of
# speech — this was captured in TokenAnalysis.pos_guess but NEVER actually
# used to filter or flag anything until this fix. Run
# diagnose_pos_tags.py to find the EXACT tag string CAMeL returns for the
# 'ʿalā' case on your installed DB version, then add it here. Left empty
# by default rather than guessing a tag string that might be wrong for
# your camel-tools version — an empty set here means this safeguard is
# INACTIVE until you populate it; the homonym-flag fixes above already
# cover the specific names found problematic in the real run regardless.
SUSPICIOUS_POS_TAGS = set()  # e.g. {"prep", "part", "conj"} — CONFIRM, don't guess

# BUGFIX (found from second real run): rows routed to the HITL queue were
# ALSO being added to the primary dataset unconditionally — a missing
# `continue` after the hitl_rows.append() in extract_dyads.py meant "needs
# review" and "in the primary dataset" were treated as compatible, which
# contradicts this file's own stated policy ("never silently auto-accepts").
# This flag makes the exclusion explicit and toggleable rather than
# hardcoding it back in silently. Default True = flagged rows are EXCLUDED
# from dyad_dataset_raw.csv until a human clears them in the HITL queue and
# manually re-adds them (see README.md "After running").
EXCLUDE_HITL_FLAGGED_FROM_PRIMARY = True

# ── Statistics & Network parameters (Dossier §5.6-5.8) ─────────────────
BOOTSTRAP_RESAMPLES = 5000          # NPMI CIs and centrality CIs
NULL_MODEL_A_PERMUTATIONS = 10000   # corpus-wide (Paper 1)
NULL_MODEL_B_PERMUTATIONS = 10000   # period-stratified (Paper 3)
LOUVAIN_RUNS = 100                  # consensus partition ensemble
LOUVAIN_GAMMA_PRIMARY = 1.0
LOUVAIN_GAMMA_SENSITIVITY = [0.5, 2.0]
LOUVAIN_CONSENSUS_THRESHOLD = 0.80  # node must share a community in >80% of runs to count "stable"
MOTIF_NULL_PERMUTATIONS = 10000     # degree-sequence-preserving, §5.7
MOTIF_SIGNIFICANCE_ALPHA = 0.05
CENTRALITY_STABLE_COV = 0.15        # CoV < this => "Stable" per §5.6
CENTRALITY_MODERATE_COV = 0.30      # CoV < this (and >= STABLE) => "Moderate"; else "Unstable"
RANDOM_SEED = 42                    # fixed and reported everywhere, per §9.3

VERSE_NAMES_CSV = OUTPUT_DIR / "verse_name_occurrences.csv"
NPMI_OUTPUT_CSV = OUTPUT_DIR / "npmi_with_ci.csv"
NULL_MODEL_A_OUTPUT_CSV = OUTPUT_DIR / "null_model_a_results.csv"
NULL_MODEL_B_OUTPUT_CSV = OUTPUT_DIR / "null_model_b_results.csv"
CENTRALITY_OUTPUT_CSV = OUTPUT_DIR / "network_centrality.csv"
COMMUNITY_OUTPUT_CSV = OUTPUT_DIR / "louvain_communities.csv"
MOTIF_OUTPUT_CSV = OUTPUT_DIR / "network_motifs.csv"
GRAPH_GRAPHML_PATH = OUTPUT_DIR / "dyad_network.graphml"
GRAPH_GEXF_PATH = OUTPUT_DIR / "dyad_network.gexf"

# ── LLM-assisted tagging (Dossier §5.9) ─────────────────────────────────
# Requires ANTHROPIC_API_KEY set as an environment variable — NEVER hardcode
# a key in this file or any file in this repo. See README.md Step 11.
CLAUDE_MODEL = "claude-sonnet-4-5"   # update if a newer Sonnet is current when you run this
CLAUDE_MAX_TOKENS = 1024
CLAUDE_TEMPERATURE = 0.0             # deterministic classification, not creative generation

# Calibration requirement (§5.9, §5.8.1): prompts MUST be pilot-tested
# against a human-labeled gold set BEFORE scale use. This is a hard gate,
# not a suggestion — theme_tagging.py and relationship_type.py both refuse
# to run in full-corpus mode until the calibration file exists AND passes
# threshold. There is no way around a human doing the gold-labeling once —
# nobody has classified these dyads before, so there is no pre-existing
# ground truth to bootstrap from. See README.md Step 11 "chicken-and-egg."
THEME_CALIBRATION_SIZE = 20
THEME_CALIBRATION_ACCURACY_THRESHOLD = 0.80
RELATIONSHIP_CALIBRATION_SIZE = 30
RELATIONSHIP_IRR_KAPPA_THRESHOLD = 0.65

PROMPTS_DIR = ROOT / "prompts"
THEME_PROMPT_PATH = PROMPTS_DIR / "theme_tagging_prompt_v1.txt"
RELATIONSHIP_PROMPT_PATH = PROMPTS_DIR / "relationship_type_prompt_v1.txt"

THEME_CALIBRATION_CSV = DATA_DIR / "theme_calibration_GOLD.csv"
RELATIONSHIP_CALIBRATION_CSV = DATA_DIR / "relationship_calibration_GOLD.csv"
MICRO_TAXONOMY_CSV = DATA_DIR / "micro_taxonomy_20.csv"

THEME_OUTPUT_CSV = OUTPUT_DIR / "theme_tags.csv"
THEME_DISAGREEMENT_LOG_CSV = OUTPUT_DIR / "theme_disagreement_log.csv"
RELATIONSHIP_OUTPUT_CSV = OUTPUT_DIR / "relationship_types.csv"
RELATIONSHIP_CALIBRATION_RESULTS_CSV = OUTPUT_DIR / "relationship_irr_results.csv"

# ── Network flag respect ────────────────────────────────────────────────
# Names with F1_Include_in_Network=No in the master CSV are still extracted
# (we don't want to lose data) but are tagged so downstream network-building
# scripts can filter them out without re-deriving the decision. As of this
# writing ALL rows say "Yes" including the 4 Disputed/Supra-polarity nodes
# (Allāh, Al-Wājid, Dhū al-Jalāl wa'l-Ikrām, Al-Nūr) — that flag has NOT yet
# been reviewed by the Islamic Studies consultant. Re-export the CSV after
# that review updates the flags; this pipeline will pick the change up
# automatically, no code change needed.
RESPECT_NETWORK_FLAG_AT_EXTRACTION = False  # extract everything; filter downstream
