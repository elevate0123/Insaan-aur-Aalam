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
- Theme tagging (macro/micro) — this is the one major piece NOT yet built.
  It needs an LLM-assisted first-pass (Claude Sonnet, per Dossier §5.9) with
  100% HITL review — a fundamentally different kind of script (API calls,
  prompt versioning, disagreement logging) from everything else here. Ask
  for it as a separate deliverable when you're ready for it; bolting it
  onto this batch would make the "no execution on your servers" boundary
  harder to keep clean, since it needs your Anthropic API key.
- Cramér's V for JJK×Theme specifically (blocked on theme tagging above —
  everything else needed for it, bias-corrected V calculation included, is
  a small addition once theme data exists)
- Anything requiring a live LLM call — kept out of this batch entirely

## What this pipeline DOES do (updated — network/stats now included)

- Steps 1-6: corpus parsing, morphological extraction, dyad matching, HITL
  routing, sensitivity analysis (as before)
- **Step 7:** NPMI with bootstrap confidence intervals (§5.6/A.2.11)
- **Step 8:** Null Model A (corpus-wide) and Null Model B (period-
  stratified) permutation significance (§5.8/A.2.4)
- **Step 9:** Undirected weighted graph construction, centrality with
  bootstrap-CI stability labels, 100-run Louvain consensus with γ
  sensitivity (§5.6/A.2.5/A.2.6)
- **Step 10:** Network motif analysis — anonymous, post-hoc-nameable
  structural pattern detection (§5.7, v2.1 addition)

---

## ⚠️ Known bug found in the first real corpus run — read before re-running

The first full run you sent back showed only **3 of 108 names matched
anywhere in the entire Qur'an** (Allāh: 2681 occurrences, Al-Ḥaqq: 115,
Al-Ḥayy: 12 — everything else: zero), and an **empty HITL review queue**.
This is a genuine bug, not a quirk of the text. Two issues, found by
diagnosing your actual output:

**Bug 1 (critical, likely root cause): definite-article mismatch.**
The master names list stores names in their conventional citation form,
WITH the definite article attached (e.g. `الْمَلِك` = "Al-Malik"). Standard
Arabic morphological analysis treats `ال` as a bound clitic and strips it
from the lemma — so CAMeL Tools' analysis of a real Qur'anic occurrence of
"Al-Malik" would very likely return the lemma `ملك` (no article), which
never equals our master entry's `الملك`. Allāh matches because `الله` is an
atomic proper noun CAMeL doesn't decompose; Al-Ḥaqq/Al-Ḥayy matching at all
is consistent with occasional analyzer fallback (see `morphology.py`
`_analyze_token`'s no-analysis path, which preserves the raw surface form
including its article).

**Run this first, before anything else:**
```bash
cd src
python diagnose_matching.py
```
This prints, for 3 verses with a certain known dyad, the exact CAMeL
analysis output token-by-token, so you can see precisely where the mismatch
happens rather than trust a guess. A candidate fix (strip the leading
article from both sides before comparing, with an explicit safety exception
for Allāh so it's never mis-stripped into "له") is **already applied** in
`morphology.py`'s `normalize_for_matching()` — but treat it as a hypothesis
until `diagnose_matching.py`'s output confirms it's the actual (or only)
cause. If the mismatch turns out to be something else (e.g. a lemma
sense-suffix format I didn't anticipate), that script's output is what a
precise second fix would be based on — share it back rather than guessing again.

**Bug 2 (confirmed, fixed): directional pair-double-counting.**
`run_sensitivity.py` and `detect_refrains()` in `extract_dyads.py` were
grouping/counting pairs on `(name_1_serial, name_2_serial)` as stored per
row — but that ordering reflects which name appears first IN THE VERSE, and
legitimately flips between occurrences of the same real-world pair. This
silently fragmented every pair's count across up to 2 buckets (confirmed in
your data: Allāh–Al-Ḥaqq was being counted as two separate "pairs," `(1,52)`
and `(52,1)`). **Fixed** — both now canonicalize to a sorted, unordered key
for counting/grouping while still preserving per-row directional metadata
untouched, since direction itself is a retained dossier attribute (§4.4),
just not a valid grouping key.

**After confirming/fixing Bug 1, re-run from Step 5 onward** (Steps 1-4
don't need repeating). Bug 2's fix is already active in the code you're
about to re-run.

## ⚠️ Second incident, found in the SECOND real run — read before re-running again

After fixing Bug 1/2 above, the corpus run went from 3 matched names to 75,
and total dyads from 69 to 2,630 — real progress. But 2,630 is still ~15x
the project's own reference figure (177 dyads, from `extraction_log.txt`),
and the diagnosis found why: **the article-stripping fix that solved the
under-matching problem also removed the one signal that was preventing
several names from colliding with extremely common Arabic words.**

**The smoking gun:** Al-'Alī (#37) showed **1,241 raw occurrences** — 13x
higher than the next-highest legitimate name — and appeared as a false
"structural refrain" up to 77 times in a single surah (the one confirmed
*real* refrain in the whole corpus, Al-'Azīz–Al-Raḥīm in Surah 26, is only
n=9). Root cause: after alef-maksūra normalization, the preposition **"ʿalā"
(على, "upon/on")** — one of the most common words in the Qur'an — becomes
orthographically identical to the divine name **"Al-'Alī"**. Same story,
smaller scale, for Al-Mu'min (collides with the common noun "believer"),
Al-Ḥaqq (collides with "truth/right" as an ordinary noun), Al-Wālī
(collides with generic human "guardian"), and Al-Awwal (collides with the
ordinal "first").

**The good news, confirmed precisely:** the known ground-truth reference —
Al-'Azīz–Al-Raḥīm, Surah 26, all 9 canonical āyahs (9, 68, 104, 122, 140,
159, 175, 191, 217), every single one at word-distance 1 — was recovered
**perfectly, completely, with zero errors**. The extraction mechanics
(matching, distance, position, refrain-detection) are sound. The problem is
specifically homonym contamination on a handful of names, not a structural
flaw in the pipeline.

**What was fixed:**
1. **5 names newly flagged as homonym-risk** in the master dataset, based on
   direct evidence from this run (not guessing): Al-'Alī, Al-Mu'min,
   Al-Ḥaqq, Al-Wālī, Al-Awwal. `divine_names_master.csv` is already
   re-exported with these flags — every match against these 5 names will
   now force HITL review with context, same as the pre-existing Al-'Azīz
   homonym case.
2. **A POS-tag-based safeguard wired in** (`config.SUSPICIOUS_POS_TAGS`) —
   this was *designed* into the pipeline from the start (`pos_guess` field)
   but never actually connected to the filtering logic until now. It's
   **empty by default** — run `diagnose_pos_tags.py` first to find the exact
   tag string your CAMeL Tools version returns for the ʿalā preposition
   case, rather than have me guess a tag name that might not match your
   installed DB version.
3. **`verse_text` added to the dyad output** — the HITL queue was
   previously unreviewable without manually looking up every verse
   separately; that's fixed now.
4. **GraphML/GEXF export bug fixed**: the empty `dyad_network.graphml` (0
   bytes) you got was a confirmed bug — an edge attribute was stored as a
   Python list, which both GraphML and GEXF writers reject outright
   (`TypeError: GraphML does not support type <class 'list'> as data
   values`), leaving a silently-empty file with no error surfaced. Fixed to
   store as a capped string; export now also fails LOUD with a clear
   message (and deletes the empty artifact) if anything else goes wrong,
   instead of leaving a 0-byte file for you to discover later.

**Also found, not a bug, needs your action:** `null_model_a_results.csv`
and `null_model_b_results.csv` in your second upload were **byte-identical
to the first run's output** — `null_models.py` wasn't re-run. Re-run it
explicitly after re-extraction; it's not automatic.

**Recommended next run order:**
```bash
python diagnose_pos_tags.py         # find your CAMeL version's tag for 'ʿalā', add to config.py
python extract_dyads.py             # re-extract with updated homonym flags + verse_text
python run_sensitivity.py
python npmi_stats.py
python null_models.py               # do not skip this again
python build_network.py
python motif_analysis.py
```
After this run, sanity-check total dyad count against the ~177 reference
figure before trusting anything downstream — if it's still off by an order
of magnitude, something is still wrong and is worth stopping to find, not
proceeding past.

## ⚠️ Third finding: the review flag existed but nothing was gated on it

The second run correctly flagged 58% of dyads for HITL review (Al-'Alī,
Al-Mu'min, etc.) — but `npmi_stats.py`, `null_models.py`, `build_network.py`,
and `motif_analysis.py` all still consumed the **full, unfiltered** dataset.
Al-'Alī still showed up as the #2 network hub (982 weighted degree) even
though it was correctly flagged — the flag and the analysis were running in
parallel, not gating each other.

**Fixed:** new `filters.py` module, wired into all four downstream scripts.
Default behavior is now to **exclude** flagged/unreviewed rows automatically
(pass `--include-unreviewed` to get the old, currently-misleading, full-data
behavior back — outputs from that mode are tagged `_UNREVIEWED_INCLUDED` in
the filename so the two modes can never be confused for each other).

**A structural finding this surfaced, with hard numbers:** even in the
confident subset, **78.3% of dyads involve Allāh** (864 of 1,103). This is
almost certainly not the phenomenon this whole project studies — the
research question is about pairs of *attributes* (Al-Ghafūr–Al-Raḥīm), not
Allāh co-occurring with an attribute name anywhere within a 10-word window,
which will happen constantly simply because "Allāh" is the most frequent
word in the text. Excluding Allāh-involving dyads brings the count to 239
— much closer to the project's own reference figure of 177.

This directly connects to something already flagged as pending consultant
review: Allāh's `F1_Include_in_Network` flag is still "Yes." **The code
already supports excluding it** — `build_network.py`'s `build_graph()`
function has always respected this flag when set to "No." No code change
needed: once the consultant decision is made, flip it in the workbook,
re-export `divine_names_master.csv`, and re-run. Worth testing both ways
(with and without Allāh as a node) and comparing, given how much of the
graph's current shape (all-Unstable centrality, the largest motifs)
traces back to Allāh's sheer frequency swamping everything else.

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
| `output/verse_name_occurrences.csv` | Every name occurrence per verse (not just paired) — feeds the null models |
| `output/npmi_with_ci.csv` | NPMI + bootstrap CI per pair (Step 7) |
| `output/null_model_a_results.csv` | Corpus-wide permutation significance (Step 8) |
| `output/null_model_b_results.csv` | Period-stratified differential significance (Step 8) |
| `output/network_centrality.csv` | Degree/betweenness/closeness/entropy + stability labels (Step 9) |
| `output/louvain_communities.csv` | 100-run consensus partition + sensitivity (Step 9) |
| `output/dyad_network.graphml` / `.gexf` | The graph itself, for Gephi/archival (Step 9) |
| `output/network_motifs.csv` | Significant 3/4-node structural patterns, anonymous (Step 10) |
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

## Step 7 — NPMI with bootstrap confidence intervals

```bash
python npmi_stats.py
```

Implements §5.6/Appendix A.2.11 — resamples at the **verse level** (not
dyad-instance level, since verses are the actual independent sampling unit).
Produces `output/npmi_with_ci.csv`. **Do not rank pairs by raw NPMI** — only
compare pairs whose 95% CIs don't overlap; the `ci_status` column flags
pairs with too few valid resamples (typically hapax pairs) to trust at all.

## Step 8 — Null models A and B

```bash
python null_models.py
```

Implements §5.8/Appendix A.2.4 — **Model A** (corpus-wide permutation) tests
overall dyad significance; **Model B** (period-stratified) is the *only*
one of the two that can support any Meccan/Medinan differential claim.
Requires `quran-data.xml` from Step 2 — verses with `UNKNOWN` period are
excluded from Model B entirely (not guessed into a period), and the script
tells you how many that was.

⚠️ **Performance note:** this is pure Python, by design, for auditability
over raw speed (Dossier §9.3 reproducibility ethos — every step should be
readable by a non-specialist reviewer, not just fast). At 10,000
permutations this can take from several minutes to over an hour depending
on your machine. Reduce `NULL_MODEL_A_PERMUTATIONS` / `_B_` in `config.py`
for a quick sanity-check run first; restore to 10,000 for the numbers you
actually publish.

## Step 9 — Network construction, centrality, Louvain consensus

```bash
python build_network.py
```

Implements §5.6/Appendix A.2.5/A.2.6. Builds the **undirected** weighted
graph (directionality is retained as edge metadata only — this is a
deliberate decision documented in the dossier, not an oversight). Produces:

- `output/network_centrality.csv` — weighted degree, betweenness, closeness,
  dyadic entropy, **and a bootstrap-CI stability label (Stable/Moderate/
  Unstable) per node.** Only cite Stable+Moderate nodes as primary findings.
- `output/louvain_communities.csv` — 100-run consensus partition at γ=1.0,
  plus sensitivity columns at γ=0.5 and γ=2.0. Nodes below 80% stability
  are labeled "Boundary node" — report as provisional.
- `output/dyad_network.graphml` and `.gexf` — import the GEXF into Gephi,
  apply ForceAtlas2 layout per Dossier §6.5 for publication figures.

The script will print a warning if any of the 4 Disputed/Supra-polarity
nodes (Allāh, Al-Wājid, Dhū al-Jalāl wa'l-Ikrām, Al-Nūr) end up included —
as of this writing their `F1_Include_in_Network` flag is still "Yes"
pending Islamic Studies consultant review. Re-export the names CSV after
that review updates the flag; no code change needed.

## Step 10 — Network motif analysis (v2.1 addition)

```bash
python motif_analysis.py
```

Implements §5.7 — **must run after Step 9**, not before (motif analysis
operates on the already-built, already-validated graph). Enumerates all
3-node and 4-node connected sub-graphs, tests significance against a
degree-sequence-preserving null model (10,000 edge-swap permutations —
note this is a *different* null model from Step 8's verse-level
permutation; they test different hypotheses).

Output is deliberately **anonymous** — JJK composition and shape only, no
theological motif name attached. Per the dossier's explicit anti-bias
instruction, theological naming/interpretation of any significant pattern
is a human step that happens *after* seeing this table, not something this
script does for you. Also: never describe these findings using the word
"algorithm" in Papers 1 or 3 — frame as "statistically over-represented
structural tendency," per §5.7's publication note.



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
│   ├── extract_dyads.py         ← main extraction pipeline (Steps 4-6)
│   ├── run_sensitivity.py       ← 4-threshold sensitivity analysis (Step 6)
│   ├── npmi_stats.py            ← NPMI + bootstrap CI (Step 7)
│   ├── null_models.py           ← Null Models A & B (Step 8)
│   ├── build_network.py         ← graph + centrality + Louvain (Step 9)
│   ├── motif_analysis.py        ← motif significance testing (Step 10)
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
