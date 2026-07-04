# Divine Name Dyad Extraction Pipeline
### Computational Semantic Network of Paired Divine Names in the Qur'an — v2.1

This implements Dossier v2.1 §5.3 (Morphologically-Normalized Extraction) end
to end: Tanzil XML → CAMeL Tools morphology → name matching → dyad dataset +
HITL review queue. Everything runs **locally on your machine**, nothing
phones home except the one-time model download in Step 1.

---

## What this pipeline DOES do

- Parses the Qur'an corpus (Tanzil XML)
- Morphologically normalizes every token (CAMeL Tools) so definite-article
  variation, construct-state forms, and pronoun clitics don't cause missed
  matches
- Matches normalized tokens against the master 108-name list
- Computes word-distance and flags dyads within your chosen threshold
- Classifies grammatical position (verse-opening / mid-verse / verse-final)
- Force-routes homonym-flagged names and low-confidence matches to a
  separate HITL review queue — **never silently auto-accepts these**
- Detects structural refrains (same pair, same surah, ≥3 occurrences)
- Runs the full 4-threshold sensitivity analysis (5/7/10/15 words) required
  by §5.7 / Appendix A.2.17

## What this pipeline does NOT do (by design — separate scripts/phase)

- JJK classification (already done by hand against Al-Qushayrī/Al-Ghazālī —
  see Master_Divine_Names_Dataset_v2_1.xlsx)
- Theme tagging (macro/micro) — separate LLM-assisted HITL script, not built yet
- NPMI, bootstrap CIs, null-model permutation tests, Cramér's V — separate
  statistics script, consumes this pipeline's output as input
- Network graph construction / Louvain — separate script, same reason
- Anything requiring a live LLM call — kept out of this pipeline entirely so
  it's a pure, deterministic, reproducible corpus-extraction step

---

## Step 1 — Environment setup

```bash
# From the pipeline/ root folder
python3 -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\activate

pip install -r requirements.txt
```

CAMeL Tools needs its morphology database downloaded separately (not
bundled in the pip package — it's several hundred MB):

```bash
camel_data -i morphology-db-msa-r13
```

This downloads to `~/.camel_tools/`. One-time only, works offline after.

**Known limitation, read before trusting edge cases:** CAMeL Tools ships
Modern Standard Arabic (MSA) analyzers. There is no first-party
Classical/Quranic-Arabic-specific morphological database. The MSA analyzer
(`calima-msa-r13`) handles the shared root-and-pattern system reasonably
well for Quranic text, but **will** mis-analyze some Classical-Arabic-only
forms (certain energetic-mood verbs, archaic case endings, some
construct-state edge cases). This is exactly why the pipeline routes
zero-confidence and ambiguous matches to a mandatory HITL queue rather than
trusting the analyzer blindly — but it means the HITL queue will likely be
non-trivial in size on the first run. Cross-validate persistently-flagged
tokens against the **Qur'anic Arabic Corpus** (corpus.quran.com), which is
purpose-built for Quranic morphology and is already a listed resource in
the dossier (§6.1).

## Step 2 — Get the Qur'an corpus

This pipeline does not download anything from the internet automatically —
by design, so the whole thing stays auditable and offline-reproducible.

1. Go to **https://tanzil.net/download/** yourself.
2. Choose **Uthmani** script (matches riwāyat Ḥafṣ ʿan ʿĀṣim, per the
   dossier's stated scope), format **XML**, uncompressed.
3. Save as `data/quran-uthmani.xml` in this project.
4. (Optional but recommended) Also download **quran-data.xml** from the same
   page for Meccan/Medinan classification — save it alongside the main file
   in `data/`. Without it, `meccan_medinan` will be `UNKNOWN` for every verse,
   which silently breaks Papers 1 and 3's period-differential analysis. The
   pipeline warns you at runtime if this file is missing; it will not guess.

## Step 3 — Confirm the master names list is current

`data/divine_names_master.csv` is already generated from
`Master_Divine_Names_Dataset_v2_1.xlsx` as of this session (108 names, dual
JJK, Tier 1-3). **Re-export it any time the master workbook changes** —
this pipeline reads the CSV, not the xlsx, so a stale CSV will silently use
old classifications. A one-line re-export (run from wherever you have the
workbook open in Python/openpyxl) is in `data/README_reexport.md`.

⚠️ **Before your first full run**, note two things flagged in the current
export that affect this pipeline's behavior:
- `F1_Include_in_Network = Yes` for all 4 Disputed/Supra-polarity nodes
  (Allāh, Al-Wājid, Dhū al-Jalāl wa'l-Ikrām, Al-Nūr) — **not yet reviewed
  by the Islamic Studies consultant**. The pipeline extracts these regardless
  (`RESPECT_NETWORK_FLAG_AT_EXTRACTION = False` in `config.py`) so no data is
  lost, but any downstream network-building script should filter on this
  column, and the column's current values should be treated as provisional.
- Tier 3 names (Al-Sittīr, Al-Jamīl) are in the CSV and WILL be matched if
  they occur in the text, but are excluded from the primary dataset and
  routed to the HITL queue instead (`TIER3_POLICY` in `config.py`).

## Step 4 — Self-test (30 seconds, do this before the full run)

```bash
cd src
python selftest.py
```

Runs 3 hand-verified verses from `extraction_log.txt` (already cross-checked
against the v2.1 master dataset this session — zero mismatches). If this
fails, something in your environment is wrong — fix it here before debugging
a 6,236-verse run.

## Step 5 — Full extraction

```bash
python extract_dyads.py
```

Takes several minutes (CAMeL Tools analysis is the bottleneck, ~6,236
verses). Progress logs every 500 verses. Produces:

| File | Contents |
|---|---|
| `output/dyad_dataset_raw.csv` | Primary dataset — every dyad within threshold, confidently matched |
| `output/hitl_review_queue.csv` | Everything flagged for manual review, WITH context text, and WHY it was flagged |
| `output/structural_refrains.csv` | Same-surah repeated pairs (≥3 occurrences) |
| `logs/extraction_run.log` | Full run log, timestamped, for your audit trail |

## Step 6 — Sensitivity analysis (required before locking the final threshold)

```bash
python run_sensitivity.py
```

Runs distance thresholds 5/7/10/15 against a single cached tokenization
pass (doesn't re-run CAMeL Tools 4×). Produces
`output/sensitivity_analysis.csv` — report this table in Paper 0
supplementary materials regardless of which threshold you keep, per
Dossier §5.7.

## After running — mandatory, not optional

**Review every row in `hitl_review_queue.csv` by hand before treating
`dyad_dataset_raw.csv` as final.** This is not a suggestion — it's the same
zero-silent-errors principle the whole project has run on. The queue
includes the surrounding ±5-token context for each flagged match
specifically so this review is fast, not so it can be skipped.

---

## Project structure

```
pipeline/
├── README.md                    ← you are here
├── requirements.txt
├── data/
│   ├── divine_names_master.csv  ← already generated from the v2.1 workbook
│   ├── quran-uthmani.xml        ← YOU download this (Step 2)
│   └── quran-data.xml           ← YOU download this, optional (Step 2)
├── src/
│   ├── config.py                ← all tunable parameters, read this first
│   ├── quran_source.py          ← Tanzil XML parser
│   ├── morphology.py            ← CAMeL Tools wrapper
│   ├── names_loader.py          ← master names list loader
│   ├── extract_dyads.py         ← main pipeline (run this)
│   ├── run_sensitivity.py       ← 4-threshold sensitivity analysis
│   └── selftest.py              ← run this FIRST
├── output/                      ← generated CSVs land here
└── logs/                        ← timestamped run logs land here
```

## Troubleshooting

| Symptom | Likely cause |
|---|---|
| `FileNotFoundError: Tanzil XML not found` | You skipped Step 2 |
| `selftest.py` reports FAIL on Q2:255 (Ḥayy/Qayyūm) | CAMeL DB not installed — re-run `camel_data -i morphology-db-msa-r13` |
| HITL queue is huge (>30% of matches) | Expected on first run given the MSA/Classical-Arabic gap noted above — this is the analyzer being honest about its limits, not a bug. Review a sample; if error rate is high, consider `MLEDisambiguator` (noted in `morphology.py`) for a second pass |
| `meccan_medinan` column is all `UNKNOWN` | You skipped the optional `quran-data.xml` download in Step 2 |
| Import errors on `camel_tools.*` | Virtual environment not activated, or `pip install -r requirements.txt` didn't complete — check for the ~2-3GB torch/transformers download finishing fully |

## Versioning

Pin bumps to `requirements.txt` require a commit message explaining why
(Dossier §9.3 reproducibility standard). Record the exact dataset version
(Zenodo DOI once published) alongside the code commit hash used to produce
it, in every paper's supplementary materials.
