# بِسْمِ اللَّهِ الرَّحْمَٰنِ الرَّحِيمِ

---

# COMPUTATIONAL SEMANTIC NETWORK OF PAIRED DIVINE NAMES IN THE QUR'AN

## _Asmā' al-Ḥusnā Dyad Analysis — Project Dossier v2.1_

> **Version:** 2.1 | **Status:** Active — Single Source of Truth  
> **Replaces:** Dossier v2.0 (v1.0 and all prior documents superseded)  
> **v2.1 additions:** Network Motif Analysis (Section 5.7); Dynamic Essentialism / Relational Ontology (Sections 4.5, 8 Paper 5); Reproducible Research Pipeline & Tech Stack (Section 6)  
> **Audience:** Academic Collaborators · Funding Bodies · Islamic Studies Scholars · Computational Researchers · Network Scientists · Philosophers of Religion · Digital Humanities Community  
> **Maintained by:** Principal Researcher

---

## HOW TO USE THIS DOCUMENT

This dossier is the single source of truth for the entire research programme. It is structured in two parts:

**Part I — The Programme** contains everything needed to understand, execute, and publish this research. It is organized by audience: each major section is self-contained enough for a collaborator joining at any stage to orient themselves without reading everything.

**Part II — Appendix** contains the complete v1.0 → v2.0 critique, a change log with rationale for every decision revision, and the full IRR and HITL protocols.

**Quick navigation by role:**

- _Islamic Studies scholar / tafsīr consultant_ → Sections 4, 6.3, 7, 10
- _Data engineer / Python developer_ → Sections 5, 6.1, 6.2, 6.5 (Tech Stack), 9
- _Network scientist_ → Sections 5.4–5.7, 6.4, 8 (Papers 1, 4)
- _Philosopher of religion_ → Sections 4.5, 8 (Paper 5 — Dynamic Essentialism)
- _Funding body / institutional partner_ → Sections 1, 2, 11, 12
- _Digital humanities collaborator_ → Sections 3, 5, 6, 8 (Paper 0)
- _Potential co-author_ → Section 13

---

## PART I — THE PROGRAMME

---

# 1. Executive Summary

## 1.1 The Research in One Paragraph

The Qur'an contains 6,236 verses. A structurally dominant pattern across that corpus has never been studied computationally: two Divine Names (Asmā' al-Ḥusnā) placed together — nearly always at the close of a verse — forming what this programme calls a **dyad**. _Al-Ghafūr_ with _Al-Raḥīm_. _Al-ʿAzīz_ with _Al-Ḥakīm_. _Al-Samīʿ_ with _Al-ʿAlīm_. Classical scholars from Al-Ṭabarī to Fakhr al-Dīn al-Rāzī consistently commented on why a specific pair closes a specific verse, and why a different pair would be theologically wrong in that position. Yet no study has ever mapped this pattern systematically, computationally, or statistically across the entire Qur'anic corpus. This programme fills that gap.

## 1.2 Core Research Question

> _When Allah's names appear together in pairs at the close of Qur'anic verses — Al-Ghafūr with Al-Raḥīm, Al-ʿAzīz with Al-Ḥakīm, Al-Samīʿ with Al-ʿAlīm — is this a systematic, semantically deliberate structure, or coincidence? This programme answers that question with data, network science, and classical scholarship._

## 1.3 What Has Been Established (v1.0 Dataset Results)

The foundational dataset — 177 validated dyads extracted from the Tanzil corpus, representing 71 unique name pairs across 50 active nodes — has already produced the following empirical results:

|Finding|Metric|Status|
|---|---|---|
|Dyad pairings are non-random|Z-scores up to 70.11; p < 0.001 for 27/71 pairs|Established|
|Al-ʿAzīz — Al-Ḥakīm is the dominant dyad|n=29, present in 22 surahs, both Meccan and Medinan|Established|
|NPMI bond strength diverges from raw frequency|Al-Wāḥid–Al-Qahhār NPMI=1.32 > Al-ʿAzīz–Al-Ḥakīm NPMI=1.11|Established|
|JJK×Theme association is moderate, not strong|χ²=93.49, V_corr=0.21|Established|
|Jalāl+Jalāl dyads double in Medinan period|5.9% → 23.7%, Δ+17.8pp|Established|
|64/71 unique pairs are hapax|Single-occurrence pairs dominate|Established|
|Three structural refrains identified|Surah 26 (n=9), Surah 2 (n=4), Surah 3 (n=4)|Established|

## 1.4 What v2.0 and v2.1 Change

Version 2.0 incorporated ten structural changes to the research design — driven by a systematic critique of the v1.0 programme. The core dataset remains valid. Changes in v2.0: the taxonomic framework (Kamāl split into two sub-classes), the statistical reporting standard (NPMI CIs, stratified null model), the network model (directed/undirected decision, Louvain consensus), the paper pipeline (Papers 2+5 merged; Paper 4 replaced), and the HITL protocol (stratified sampling).

**v2.1 adds three targeted theoretical and infrastructural upgrades:**

1. **Network Motif Analysis** — moving from global topology (centrality, communities) to local topology (recurring triadic sub-graphs), added to Paper 1 and Paper 3. This shifts the analytical frame from "which names appear together" to "what compositional structures the Qur'an uses to build theological arguments."
2. **Dynamic Essentialism** — a new positive theoretical claim for Paper 5, replacing the binary essentialism-vs.-contextualism debate framing with a relational ontology in which the dyadic Edge (the pairing relation) is the primary locus of meaning.
3. **Reproducible Research Pipeline** — a full, layer-by-layer tech stack specification replacing tool lists with a complete, version-controlled, auditable infrastructure.

Full rationale for all v2.0 changes is in Appendix A.

## 1.5 Programme Outputs

|Output|Timeline|Status|
|---|---|---|
|Master dataset (Zenodo, CC-BY 4.0)|Month 4|In preparation|
|Paper 0: Methodology + HITL pipeline + reproducibility checklist|Month 10|Drafting|
|Paper 1: Corpus frequency + network structure + **motif architecture**|Month 12|In preparation|
|Paper 2: Jalāl–Jamāl axis + semantic polarity|Month 16|Planned|
|Paper 3: Dyad–theme correlation + **motif–theme structural tendencies**|Month 20|Planned|
|Paper 4 (revised): Cross-corpus religious network comparison|Month 24|Planned|
|Paper 5 (merged): **Dynamic Essentialism** — structural regularity + contextual deployment|Month 26|Planned|
|Scholarly monograph|Month 36|Planned|

---

# 2. The Research Problem

## 2.1 What Are Paired Divine Names?

The Qur'an does not present Divine Names as a list. Names appear embedded in verses, and a structurally dominant pattern emerges: two names placed together, almost always at the close of a verse, forming a dyad. Consider:

|Arabic Dyad|Transliteration|Verse-context pattern|
|---|---|---|
|الغَفُورُ الرَّحِيمُ|Al-Ghafūr — Al-Raḥīm|Follows verses on sin, transgression, and repentance|
|الْعَزِيزُ الْحَكِيمُ|Al-ʿAzīz — Al-Ḥakīm|Follows verses on divine decree, law, and prophethood|
|السَّمِيعُ الْعَلِيمُ|Al-Samīʿ — Al-ʿAlīm|Follows verses on prayer, supplication, and hidden intention|
|التَّوَّابُ الرَّحِيمُ|Al-Tawwāb — Al-Raḥīm|Follows verses on accepted repentance and divine turning|
|الْعَلِيمُ الْخَبِيرُ|Al-ʿAlīm — Al-Khabīr|Follows verses on hidden states and inner reality|

These are not ornamental closings. Al-Rāzī in _Mafātīḥ al-Ghayb_ makes this argument explicitly and repeatedly — commenting on _why_ a specific pair closes a specific verse, and why a semantically related but different pair would be theologically wrong in that position. Yet no scholar has ever mapped this pattern computationally across the entire Qur'an.

## 2.2 The Precise Gap in Existing Scholarship

Existing scholarship on the Asmā' al-Ḥusnā falls into three categories, each with significant limitations:

**Theological treatises** (Al-Ghazālī, Ibn al-Qayyim): enumerate and explain individual names but do not systematically study pairings. Al-Ghazālī's _Al-Maqṣad al-Asnā_ provides exhaustive individual-name taxonomy — it has no chapter on co-occurrence.

**Modern Islamic devotional literature**: treats names as a memorization list for supplication. No structural analysis.

**Computational Qur'anic studies** (Dukes 2011, Sharaf & Alias 2014, Alaiyed et al. 2020): focuses on word frequency, verse structure, and stylistics — not divine name co-occurrence as a semantic network.

> **The gap, stated precisely:** No existing study has (a) extracted all divine name dyads from the complete Qur'anic corpus with principled operational definitions, (b) modelled them as a weighted co-occurrence network with statistical validation, (c) demonstrated non-randomness with a permutation-based null model, (d) correlated pairs with verse thematic context at both macro and micro granularity, (e) classified pairs according to a rigorously operationalized JJK polarity framework with inter-rater reliability, or (f) tested the theological tension between dyad-system structural regularity and contextual modulation against the essentialism/contextualism debate in philosophy of religion. This programme does all six.

## 2.3 Why This Question Matters — By Disciplinary Audience

**For Qur'anic Studies:** If the data shows that specific pairs reliably co-occur with specific verse themes, this constitutes evidence that divine name dyads function as an embedded interpretive system — a theological grammar written into the texture of the text itself. This is a structural argument that extends and empirically tests what classical tafsīr scholars argued propositionally.

**For Corpus Linguistics:** The dyad phenomenon is a novel case of sacred-text collocation — where the co-occurring units are theological attributes rather than lexical items. The methodology is transferable to other scriptural corpora (Hebrew Bible divine epithets, Sanskrit divine name pairs in Vedic hymns, Syriac Christian doxologies).

**For Islamic Theology:** The empirical pattern of pairings can confirm, nuance, or challenge classical Sifāt theory — particularly whether the Ashʿarī framework of divine attribute classification corresponds to the Qur'an's own co-occurrence structure, or whether the co-occurrence network reveals a different grouping.

**For Network Science:** Sacred text as a network object is methodologically novel. The specific challenge here — small N (177 dyads, 50 nodes), high hapax rate (90%), and theologically structured edge weights — raises interesting questions about network topology inference under data sparsity.

**For Philosophy of Religion:** Recurring dyads used across varying verse contexts test whether divine attributes are essential and immutable (essentialism: Alston, Swinburne) or contextually weighted (attributive contextualism: Murata, Chittick). This is the first dataset capable of addressing this question empirically rather than purely analytically.

---

# 3. Novelty and Scholarly Contribution

## 3.1 Methodological Contributions (Novel to the Field)

- The first open, machine-readable dataset of Qur'anic divine name dyads, annotated with thematic, grammatical, semantic, and theological metadata — built using a fully documented, reproducible pipeline.
- A HITL protocol combining LLM-assisted first-pass tagging with morphologically-normalized Arabic extraction (CAMeL Tools) and stratified inter-rater validation — a methodological model for computational Islamic studies.
- A stratified permutation-based null model (period-preserving) that converts 'pairings are non-random' from claim to finding with formal p-values.
- A principled five-class JJK taxonomy (Jalāl / Jamāl / Kamāl-epistemic / Kamāl-ontological / Disputed) with an operationalized decision procedure and published inter-rater reliability.
- A sensitivity analysis of dyad definition across word-distance thresholds (5, 7, 10, 15 words), demonstrating robustness of core findings to operational specification.

## 3.2 Empirical Contributions (New Facts About the Qur'an)

- Complete frequency and NPMI distribution of all divine name dyads across the Qur'an, including bootstrap confidence intervals on all co-occurrence metrics.
- A weighted co-occurrence network with consensus Louvain community detection (100-run ensemble) identifying which names cluster into stable theological communities.
- Correlation analysis between dyad types and verse thematic context at two granularity levels (7 macro-categories, 20 micro-categories).
- Meccan vs. Medinan distribution analysis: Jalāl+Jalāl dyads double in the Medinan period (+17.8pp), Jalāl+Kamāl-epistemic drops; interpreted as a structural shift in divine self-presentation across revelation contexts.
- Identification of three structural refrains (Surah 26, Surah 2, Surah 3) as literary devices requiring separate treatment from independent contextual dyad deployment.
- Semantic surprise index (Shannon information content) identifying 32 CRITICAL and 20 HIGH-priority dyads whose JJK type is unexpected given their verse theme — prime candidates for tafsīr case-study analysis.

## 3.3 Theoretical Contributions (New Claims for Scholars)

- A revised five-type dyad relationship taxonomy (complementary / balancing / reinforcing / sequential / intensifying) with a published inter-rater decision tree and κ ≥ 0.65 reliability standard.
- A revised five-class JJK attribute taxonomy (Jalāl / Jamāl / Kamāl-epistemic / Kamāl-ontological / Disputed) that resolves the conceptual overloading of the classical three-class system.
- A unified theoretical argument: the Qur'anic dyad system is **structurally patterned** (dominant JJK combinations are non-random, Meccan/Medinan evolution is statistically significant) **and contextually deployed** (same dyad appears across different verse themes; high-surprise dyads mark theologically significant rhetorical moments). This dual structure does not contradict divine immutability — it reflects the difference between essential divine attributes and their contextual rhetorical surface.
- A cross-corpus network comparison framework (Paper 4 revised) establishing a graph-theoretic protocol for comparing religious name networks across traditions.

---

# 4. Theoretical Frameworks

This programme draws on five theoretical traditions. Each provides a distinct analytical lens and maps to a specific disciplinary audience and publication venue.

## 4.1 Corpus Linguistics — Collocation Theory

**Core principle:** Co-occurrence is semantically significant. J.R. Firth (1957): _"You shall know a word by the company it keeps."_ Sinclair's (1991) collocation theory demonstrates that systematic co-occurrence patterns in corpora carry semantic weight that isolated word-frequency analysis cannot reveal.

**Application:** If Al-Ghafūr and Al-Raḥīm systematically co-occur (they do — n=11, the second-highest frequency dyad after the refrain-corrected Al-ʿAzīz–Al-Ḥakīm), this co-occurrence is itself a semantic fact about how the text constructs divine forgiveness. The NPMI score quantifies the strength of that association independent of marginal frequency.

**Key theorists:** J.R. Firth (1957), John Sinclair (1991), Douglas Biber (register analysis), Stefan Th. Gries (collostructional analysis), Michael Stubbs (corpus semantics).

**Journal homes:** _Journal of Quantitative Linguistics_, _Corpus Linguistics and Linguistic Theory_, _Digital Scholarship in the Humanities_.

## 4.2 Cognitive Linguistics — Conceptual Blending

**Core principle:** Fauconnier and Turner's (2002) conceptual blending theory: when two concepts are placed together in a structured discourse frame, they create a blended conceptual space with emergent meaning not present in either concept alone.

**Application:** When Al-ʿAzīz (the Almighty — a Jalāl name of power) is paired with Al-Raḥīm (the Merciful — a Jamāl name of intimacy), the blend is not merely "powerful and merciful." The pairing creates a third meaning: power that is constitutively constrained by mercy — a theological claim about the nature of divine sovereignty that neither name alone can make. This is the theoretical grounding for the _balancing_ relationship type in the dyad taxonomy.

**Key theorists:** Gilles Fauconnier & Mark Turner (2002), Zoltán Kövecses (metaphor theory), Leonard Talmy (force dynamics — relevant for Jalāl/Jamāl structural tension).

**Journal homes:** _Cognitive Linguistics_, _Language and Cognition_, _Metaphor and Symbol_.

## 4.3 Islamic Theology — Sifāt Doctrine and the Revised JJK Framework

**Core principle:** Classical Islamic theology (kalām) distinguishes between attributes of divine essence (Sifāt al-dhāt) and attributes of divine action (Sifāt al-fiʿl). The Sufi and philosophical tradition — developed most rigorously by Al-Ghazālī, Ibn ʿArabī, and Al-Qushayrī — introduces a further polarity between Jalāl (divine majesty) and Jamāl (divine beauty).

**The revised JJK taxonomy (v2.0):** The v1.0 three-class system (Jalāl / Jamāl / Kamāl) placed too many semantically heterogeneous names into Kamāl, weakening discriminating power. The v2.0 taxonomy uses five classes:

|Class|Definition|Examples|
|---|---|---|
|**Jalāl**|Names of divine majesty, transcendence, awe, power|Al-Jabbār, Al-Qahhār, Al-ʿAzīz, Al-Mutakabbir, Al-Muntaqim|
|**Jamāl**|Names of divine beauty, mercy, intimacy, generosity|Al-Raḥmān, Al-Raḥīm, Al-Ghafūr, Al-Wadūd, Al-Laṭīf|
|**Kamāl-epistemic**|Names of divine knowledge and perception|Al-ʿAlīm, Al-Ḥakīm, Al-Khabīr, Al-Samīʿ, Al-Baṣīr|
|**Kamāl-ontological**|Names of divine existence, completeness, self-sufficiency|Al-Ḥayy, Al-Qayyūm, Al-Wāḥid, Al-Ḥaqq, Al-Ghanī, Al-Ḥamīd|
|**Disputed**|Names where classical sources disagree on classification|See Disputed Names register|

**Why this matters:** The v1.0 Kamāl category contained both Al-ʿAlīm (knowledge) and Al-Ḥayy (life) — two names Al-Ghazālī places in fundamentally different attribute clusters. Separating them allows the network analysis to test whether epistemic names cluster with each other (expected if the Qur'an uses them as a coherent knowledge-discourse pair) independently of ontological names. This is a new empirical question the v1.0 design cannot ask.

**Primary classical sources:** Al-Qushayrī, _Sharḥ Asmā' Allāh al-Ḥusnā_ (primary operational source for JJK classification — most systematic treatment); Al-Ghazālī, _Al-Maqṣad al-Asnā_ (secondary validator — individual name theology); Ibn ʿArabī, _Al-Futūḥāt al-Makkiyya_ (theoretical framework for Kamāl); Ibn al-Qayyim, _Badāʾiʿ al-Fawāʾid_ (pairing logic).

**Critical methodological note:** Al-Qushayrī is the primary operational source for JJK classification in v2.0. Al-Ghazālī is a secondary validator. The v1.0 used Al-Ghazālī as primary source — a mismatch, since Al-Ghazālī does not apply the JJK framework uniformly across _Al-Maqṣad al-Asnā_. Where Al-Qushayrī and Al-Ghazālī disagree on a name's classification, the name is flagged Disputed.

**Bridge text for Western academic audience:** Sachiko Murata, _The Tao of Islam_ (1992) — the most rigorous Western-academic treatment of the Jalāl/Jamāl polarity.

## 4.4 Network Science and Graph Theory

**Core principle:** Network analysis provides the formal mathematical framework for modelling the divine name system as a whole — something that close reading of individual verses cannot achieve.

**Key metrics and their theological interpretation in this programme:**

|Metric|Mathematical meaning|Theological interpretation|
|---|---|---|
|Weighted degree centrality|Total co-occurrence frequency|Overall "pairing centrality" — which names appear most often in dyads|
|Betweenness centrality|Fraction of shortest paths passing through a node|Names that "bridge" otherwise disconnected name-clusters — theological mediators|
|Dyadic entropy|Shannon entropy of a name's partner distribution|High entropy = semantically versatile; low entropy = captured by one dominant relationship|
|NPMI bond strength|Normalized co-occurrence above chance|Strength of theological association independent of frequency|
|Louvain community|Consensus cluster across 100 runs|Stable theological groupings in the co-occurrence structure|

**Note on directed vs. undirected (v2.0 decision):** The network is modelled as **undirected** for all centrality and community detection analyses. Directionality (Name1 → Name2 in canonical verse order) is retained as a dataset attribute and analysed descriptively in Paper 1 (which name tends to appear first in Jalāl+Jamāl balancing pairs?) but does not drive the network topology, because there is no established precedent in Arabic rhetorical scholarship for canonical verse order within a closing formula encoding theological priority. This decision is documented and falsifiable — if a future study demonstrates that ordering carries consistent semantic weight, the directed analysis can be re-run on the published dataset.

**Key theorists:** Albert-László Barabási (scale-free networks and hubs), Mark Newman (community detection and modularity), Santo Fortunato (resolution parameter sensitivity in Louvain).

**Journal homes:** _Applied Network Science_, _Journal of Complex Networks_, _Social Networks_.

## 4.5 Philosophy of Religion — Dynamic Essentialism and Relational Ontology

**Core principle:** This programme does not referee the essentialism/contextualism debate in philosophy of religion — it proposes a resolution by reframing the unit of analysis. The debate has proceeded by treating individual Names as the primary objects (are they essentially fixed or contextually variable?). The Qur'anic dyad data points to a third option: **the dyadic relation — the Edge — is the primary locus of meaning, not the Node**.

**The three positions:**

- **Essentialism** (Alston, Swinburne, Plantinga): each divine name names an intrinsic, unchanging property of the divine nature. Context cannot modulate the attribute itself.
- **Contextual theology** (Murata, Chittick): the same name, used in different contexts, expresses different facets or intensities of the underlying reality.
- **The Muʿtazilī position** (Ibn al-Jabbār, Zamakhsharī): divine names are different linguistic expressions of the same undivided reality — ontological distinctions between attributes are denied.

**Dynamic Essentialism — the v2.1 theoretical contribution:**

The programme proposes a synthesis that is neither binary:

- **The Nodes are Essential.** Divine Names carry stable, immutable semantic properties. This is demonstrated by the stable network topology across Meccan and Medinan periods (Spearman ρ=0.84 on degree hierarchy) and the high NPMI of canonical pairs. The Name Al-ʿAzīz is always a Jalāl name; Al-Raḥīm is always a Jamāl name. Their properties do not change.
- **The Edges are Dynamic.** The _pairing_ of these names is where the text's active theological work occurs. The meaning of a verse's closing dyad is not located in Al-Ghafūr _or_ Al-Raḥīm — it is located in the relational vector created _between_ them in that specific verse context.
- **The Synthesis.** The Qur'an operates a system of **Relational Attributes**: the divine essence is immutable (essentialism at the attribute level), but the _presentation_ of that essence to the human recipient is dynamically calibrated through the specific pairing chosen for each verse context (contextualism at the deployment level). The dyad system is the mechanism of that calibration.

**The evidence base for this claim:**

- **High-surprise dyads** are the key proof. A dyad with semantic surprise > 3.5 bits (e.g., Q42:28 Al-Walī–Al-Ḥamīd) is a "relational exception" — a moment where the text intentionally breaks the dominant motif to produce a specific, high-intensity theological signal. The surprise is not in either name alone; it is in the _relation between them in that context_. Al-Rāzī comments on exactly these moments.
- **Structural motifs** (see Section 5.7) show that recurring triadic structures (Jalāl → Kamāl-epistemic → Jamāl) are the "molecular" units of theological argument, not individual names. The composition operates at the relational level.
- **The Louvain community structure** provides preliminary network evidence: if names were genuinely distinct properties (Ashʿarī), we expect high modularity; if names were undifferentiated expressions of one reality (Muʿtazilī), we expect low modularity. The observed structure (subject to resolution-parameter sensitivity) can be read as evidence for the Ashʿarī position at the node level and the contextual position at the edge level — precisely what Dynamic Essentialism predicts.

**The kalām mapping (required for Paper 5):**

- **Ashʿarī position** (divine attributes are real, distinct, subsistent) → maps onto Node-level essentialism. Confirmed by stable topology.
- **Muʿtazilī position** (names are linguistic expressions of one undivided reality) → predicts no community structure. Disconfirmed by observed modularity.
- **Ibn ʿArabī's tajallī** (names as relational properties of divine self-disclosure, not intrinsic essences) → maps most closely onto Dynamic Essentialism. The Edge is the tajallī — the specific mode of divine self-presentation in a given verse context.

Paper 5 will present Dynamic Essentialism as its positive theoretical claim, not as a compromise between existing positions. It will engage Alston (1989), Swinburne (1993), Murata (1992), and Chittick (1998) in the literature review, and the Ashʿarī/Muʿtazilī/Ibn ʿArabī debate in the kalām section — and then argue that the data supports a position none of these articulate.

**Journal homes:** _Sophia_ (Springer, Scopus Q1); _Journal of Religion_ (Chicago); _Philosophy East and West_; _International Journal for Philosophy of Religion_.

---

# 5. Methodology

The methodology integrates computational corpus analysis, morphologically-normalized Arabic NLP, network graph modelling, classical Islamic exegesis, and a stratified HITL validation protocol into a single reproducible pipeline. Every step is documented for transparency and reproducibility.

## 5.1 Step 1 — Primary Source Acquisition

**Qur'anic corpus:** Tanzil.net XML corpus (riwāyat Ḥafṣ ʿan ʿĀṣim, version 2.1.0). Standard in computational Qur'anic studies (Dukes 2011, Sharaf & Alias 2014). Provides complete Qur'an in Unicode Arabic XML with verse numbering, surah names, and pre-tagged Meccan/Medinan classification.

**Scope note on recitation variants:** This programme uses the Ḥafṣ ʿan ʿĀṣim riwāya exclusively. The three most theologically consequential name-boundary cases in other riwāyāt (Al-Raḥmān reading in Basri transmission, Al-Quddūs morphology in Warsh, Al-Ḥayy vocalization in Qālūn) have been cross-checked and do not affect any dyad in the current dataset. This is documented in the dataset metadata.

**Classical tafsīr sources:** Al-Qurṭubī's _Al-Jāmiʿ li-Aḥkām al-Qur'ān_, Al-Ṭabarī's _Jāmiʿ al-Bayān_, Ibn Kathīr's _Tafsīr al-Qur'ān al-ʿAẓīm_, and Al-Rāzī's _Mafātīḥ al-Ghayb_. Digital versions via Al-Maktaba al-Shāmila and OpenITI Corpus. Al-Rāzī is the primary classical interlocutor — uniquely systematic in justifying why specific name pairs close specific verses.

## 5.2 Step 2 — Name Identification and the Definitive Name List

### 5.2.1 The Core Methodological Decision

The most critical decision — and the one most existing work sidesteps — is establishing a principled, documented list of what counts as a "Divine Name" for extraction purposes. Three sources give partially different lists:

- The Tirmidhī hadith tradition: 99 names, various transmission chains.
- Al-Ghazālī's _Al-Maqṣad al-Asnā_: 99 names with theological justification.
- Direct Qur'anic occurrence: names functioning as divine attributes in context, verified by tafsīr — includes some names not in the 99 (e.g., Dhū al-Jalāl, Al-Walī in specific senses) and excludes some in the lists that occur as common adjectives.

**v2.0 approach:** Primary classification source is **Al-Qushayrī's _Sharḥ Asmā' Allāh al-Ḥusnā_** (most systematic JJK taxonomy). Al-Ghazālī's _Al-Maqṣad al-Asnā_ is a secondary validator for individual name inclusion decisions. The Tirmidhī list and Hamza Ashraf / Dalā'il al-Khayrāt are source-provenance tracking (Group B columns in the dataset schema). A name is included if it functions as a divine attribute in its Qur'anic context, verified by Al-Qushayrī or Al-Ghazālī.

### 5.2.2 The Tier System

|Tier|Definition|
|---|---|
|**Tier 1**|Present in Al-Ghazālī's _Al-Maqṣad al-Asnā_ core 99|
|**Tier 2**|Additional names with Qur'anic divine-attribute evidence verified in tafsīr but not in the core 99|
|**Tier 3**|Documented exclusions: hadith-only, devotional-only, or homonym-resolved as non-divine in Qur'anic context|

All three tiers are published in the dataset. Tier 3 is specifically valuable: documenting _what was excluded and why_ is a methodological contribution in itself.

### 5.2.3 The Homonym Problem

Several Arabic roots appearing as divine names also appear as common adjectives in the Qur'an. Al-ʿAzīz in Q12:30 refers to the Egyptian official, not to Allah. Al-Jalīl's root appears in various non-divine contexts. The extraction pipeline must flag and resolve these cases. HITL validation is non-negotiable here.

**v2.0 addition:** CAMeL Tools morphological analysis (see Section 5.3) provides a morphological context signal to the extraction algorithm, reducing false positives before HITL review. Manual HITL review remains the final gate.

## 5.3 Step 3 — Morphologically-Normalized Extraction

**v2.0 critical change from v1.0:** The v1.0 extraction pipeline matched on surface-form Unicode strings. This approach produces false positives (root-overlapping forms), misses morphological variants (definite article variation, construct state forms, pronoun attachment), and cannot distinguish divine-name occurrences from homonyms at the morphological level.

**v2.0 approach:** Python extraction pipeline integrates **CAMeL Tools** (Arabic NLP library, open source, NYUAD) for morphological normalization:

1. Parse Tanzil XML and extract all tokens per verse using CAMeL Tools morphological analyzer.
2. Normalize each token to its base lemma form.
3. Match normalized lemmas against the divine name list (also stored in base lemma form).
4. Flag matches for: definite article status, syntactic position (nominal predicate vs. adjective vs. proper noun usage), and proximity to other divine name matches.
5. Distance calculation on word position (not character position) after morphological tokenization.
6. All matched instances passed to HITL review queue.

**Dataset fields extracted per dyad:**

|Column group|Fields|Used in|
|---|---|---|
|**A — Location**|surah_number, surah_name, ayah_number|All papers|
|**B — Name identity**|name_1_arabic, name_2_arabic, name_1_transliteration, name_2_transliteration, name_1_english, name_2_english|All papers|
|**C — Structural**|direction (N1→N2), word_distance, grammatical_position (verse-opening/mid-verse/verse-final), triple_flag|Papers 0, 1, 3|
|**D — Period**|meccan_medinan, revelation_order_approx|Papers 1, 3|
|**E — JJK**|name_1_jjk (5-class v2.0), name_2_jjk, jjk_pair_type|Papers 1, 2, 5|
|**F — Semantic**|name_1_semantic_domain, name_2_semantic_domain, polarity_tension_index, signed_tension|Papers 2, 3, 5|
|**G — Thematic**|verse_theme_macro (7 categories), verse_theme_micro (20 categories), theme_entropy|Papers 3, 5|
|**H — Relationship**|relationship_type (5 types, operationalized), relationship_decision_path|Papers 2, 3|
|**I — Statistical**|npmi, npmi_ci_lower, npmi_ci_upper, z_score, p_value, semantic_surprise_bits, hapax_flag, refrain_type|Papers 0, 1|
|**J — HITL**|hitl_priority, al_razi_consulted, al_tabari_consulted, ibn_kathir_consulted, classical_explanation_found, confirms_signal, reviewer_notes, date_reviewed|Paper 0|
|**K — Network**|include_in_network, node_label, node_color_group|Papers 1, 4|
|**L — Morphological**|word_form_type, grammatical_gender, intensification_pattern, shared_root_flag|Papers 0, 1|

## 5.4 Step 4 — Two-Level Thematic Tagging

**v2.0 critical change from v1.0:** The v1.0 seven-category taxonomy (Tawḥīd, Prophethood, Worship, Narrative, Creation, Eschatology, Law/Community) was too coarse. Tawḥīd verses range from ontological declarations to polemic refutations of shirk to Asmaul Husna catalogues — these are not the same thematic context for dyad-theme correlation. The v1.0 V_corr=0.21 moderate effect size is partly a consequence of this blurring.

**v2.0 approach:** Two-level taxonomy:

**Macro-level (7 categories — retained from v1.0):** Tawḥīd, Prophethood, Worship, Narrative, Creation, Eschatology, Law/Community. Used in Paper 3 for the overview correlation result.

**Micro-level (20 categories — new in v2.0):** Sub-divisions of each macro-category. Examples:

|Macro|Micro sub-categories|
|---|---|
|Tawḥīd|Divine ontology declaration, Anti-shirk polemic, Asmaul Husna catalogue, Divine transcendence statement|
|Prophethood|Prophetic mission commissioning, Prophetic consolation, Inter-prophet narrative, Rejection narrative|
|Worship|Du'a / supplication context, Ritual instruction, Devotional exhortation|
|Narrative|Prophetic story, Community history, Parable|
|Creation|Cosmological, Natural phenomena, Human creation|
|Eschatology|Judgement day, Paradise, Hellfire, Resurrection|
|Law/Community|Legislation, Community ethics, War/treaty rulings, Family law|

The micro-level drives the case-study analysis in Paper 3 and the semantic surprise recalculation in Paper 5. Micro-level chi-square is expected to produce stronger V_corr than macro-level — this differential is itself a publishable finding about granularity-sensitivity.

**Tagging procedure:** First-pass by LLM (Claude Sonnet) for both macro and micro levels. 100% HITL researcher review against tafsīr sources. All disagreements logged. See Section 6.3 (HITL Protocol) for full procedure.

## 5.5 Step 5 — Operationalized Relationship Type Classification

**v2.0 critical change from v1.0:** The v1.0 five relationship types (complementary / balancing / reinforcing / sequential / intensifying) were not operationally defined. They were applied by LLM heuristic without a published decision procedure and without inter-rater reliability testing. This is not publishable in corpus linguistics journals.

**v2.0 approach:** A formal decision tree published in Paper 0 and applied before LLM first-pass:

```
Q1: Do the two names belong to the same JJK class (same primary domain)?
  → YES → Q2: Are they near-synonymous (share root or near-identical semantic scope)?
              → YES → INTENSIFYING
              → NO  → REINFORCING
  → NO  → Q3: Do the names come from opposing JJK poles (Jalāl + Jamāl)?
              → YES → BALANCING
              → NO  → Q4: Does the combination of the two names produce a theological
                         meaning not present in either alone (complementary coverage)?
                          → YES → COMPLEMENTARY
                          → NO  → Q5: Does the first name's divine action logically
                                       precede or enable the second name's action?
                                        → YES → SEQUENTIAL
                                        → NO  → COMPLEMENTARY (default)
```

**IRR standard:** κ ≥ 0.65 (substantial agreement) required before applying to full corpus. IRR test on 30-dyad calibration set (two independent annotators: researcher + Islamic Studies consultant). If κ < 0.65, the decision tree is revised and re-tested before scale application.

## 5.6 Step 6 — Graph Construction

The validated dataset is imported into Python (NetworkX) to construct a **weighted, undirected graph:**

- **Nodes:** Divine Names. Node weight = total frequency of appearance in any dyad.
- **Edges:** Co-occurrence (pairing). Edge weight = raw co-occurrence frequency. NPMI is stored as an edge attribute (not the primary weight) due to CI instability at low frequencies.
- Self-loops excluded. Directed edge attribute (N1→N2 order) retained as metadata.

**Network metrics computed:**

- Weighted degree centrality, betweenness centrality, closeness centrality
- Dyadic entropy (Shannon) of partner distribution
- Bootstrap confidence intervals on weighted degree (B=5000 resamples) — only Stable (CoV < 0.15) and Moderate (CoV 0.15–0.30) nodes reported as primary centrality findings; Unstable nodes (CoV > 0.30) explicitly flagged as provisional
- Louvain community detection — 100-run ensemble with consensus partition; nodes stable across > 80% of runs reported as community members; unstable nodes reported as "boundary nodes"
- Resolution parameter γ reported explicitly for all Louvain runs (default γ=1.0 for primary analysis; sensitivity test at γ=0.5 and γ=2.0)

**Export formats:** NetworkX GraphML (archival), Gephi GEXF (visualization), CSV edge list (interoperability).

## 5.7 Step 7 — Network Motif Analysis (v2.1 addition)

**What motifs are and why they matter:**  
Global network metrics (centrality, communities) reveal the _who_ and the _where_ of the divine name system — which names are hubs, which cluster together. Motif analysis reveals the _how_: the recurring local sub-graph structures that function as the "molecular" compositional units of the Qur'an's theological argument. A motif is a recurring pattern of three or four names connected by dyadic edges across different verses. If a "Balancing Triad" (Jalāl — Kamāl-epistemic — Jamāl) appears significantly more often than chance, this is evidence that the Qur'an operates not with isolated pairs but with triadic relational structures as its basic compositional grammar.

**Critical procedural constraint:** Motif analysis runs _on top of_ a stable, fully validated network — it is not a standalone step. The logical sequence is: lock graph definition (Section 5.6) → confirm consensus Louvain communities → run motif enumeration. Theological naming of motifs happens _after_ the computational finding, not before. Pre-specifying which motifs to look for introduces confirmation bias.

**Implementation procedure:**

1. **Enumerate all 3-node and 4-node sub-graphs** in the undirected weighted network using `NetworkX`'s `enumerate_all_cliques` and `subgraph_isomorphisms_iter`. For a 50-node network, this is computationally trivial (seconds).
    
2. **Compute observed motif frequencies** — how many times each distinct connected sub-graph pattern appears across the network.
    
3. **Construct a degree-sequence-preserving null model** — randomize edge assignments 10,000 times while preserving each node's degree (number of pairing partners). This is not the same null model as Null Models A and B (Section 5.8): those permute name assignments across verses; this one permutes edges within the network graph itself. The two null models test different hypotheses.
    
4. **Compute motif significance** (Z-score and p-value) for each observed motif pattern against the null distribution. Only motifs with p < 0.05 are reported as significant.
    
5. **Classify significant motifs by JJK polarity** — once computational significance is established, examine the JJK composition of each significant motif. Example motif types that may emerge:
    
    |Motif type|Composition|Theological interpretation if significant|
    |---|---|---|
    |Balancing Triad|Jalāl — Kamāl-epistemic — Jamāl|Power mediated through wisdom producing mercy — the Qur'an's most common triadic theological complex|
    |Epistemic Cluster|Kamāl-epistemic — Kamāl-epistemic — Jalāl|Knowledge reinforced by awareness, grounded in might — typical of legislative and judgement contexts|
    |Ontological Bridge|Kamāl-ontological — Jalāl — Jamāl|Divine life/existence as the ground of both majesty and mercy — relatively rare, theologically dense|
    |Refrain Chain|Same-JJK — Same-JJK — Same-JJK|Intensification without polarity modulation — typical of narrative refrains|
    
    These are _illustrative labels_. Actual motif types and their labels emerge from the data.
    
6. **Motif–Theme correlation** (feeds Paper 3): For each significant motif, compute its distribution across the 20 micro-level thematic categories. Report which motifs are statistically over-represented in which themes. This is the upgrade to Paper 3 — instead of correlating a single dyad to a theme, we correlate a triadic compositional structure to a theme. The claim becomes: "When the Qur'an addresses the theme of 'Divine Decree,' a [Jalāl+Kamāl-epistemic] structural tendency is statistically over-represented" — framed as a recurring structural tendency, not as an "algorithm."
    

**Implementation note — framing for publication:**  
The word "algorithm" must not appear in Papers 1 or 3 in relation to motif findings. The correct framing is "statistically over-represented structural tendency" or "recurring compositional pattern." The theological claim is interpretive and follows from the statistical finding; it is not generated by the statistical finding. Reviewers at _Arabica_ and _Journal of Quranic Studies_ will correctly reject algorithmic determinism. Reviewers at _Applied Network Science_ will accept over-represented motifs as a standard finding if properly significance-tested.

**Tools:** `NetworkX` (motif enumeration, degree-preserving randomization), `SciPy` (Z-scores), `Seaborn`/`Plotly` (motif frequency histograms vs. null distribution).

## 5.8 Step 8 — Statistical Validation (Stratified Null Model)

**v2.0 critical change from v1.0:** The v1.0 null model used corpus-wide permutation — shuffling name assignments across all verses, preserving only the number of names per verse. This proves overall co-occurrence is non-random but does not prove that the Meccan/Medinan differential is non-random, which is where the more interesting theological argument lives.

**v2.0 approach:** Two null models (distinct from the motif null model in Section 5.7, which operates at the graph level):

**Null Model A (corpus-wide):** Permute name assignments across all verses 10,000 times, preserving number of names per verse. Produces p-values for overall dyad significance (Paper 1).

**Null Model B (period-stratified):** Permute name assignments within Meccan verses only, then within Medinan verses only — preserving period structure. Produces p-values for Meccan-specific and Medinan-specific pair frequencies, and for the period-differential finding (Jalāl+Jalāl doubling). This is the null model for the Meccan/Medinan evolution claim (Paper 3).

**Effect size reporting:** All chi-square tests report bias-corrected Cramér's V (V_corr, Bergsma & Wicher 2013) alongside χ² and p-value. Effect size conventions: Strong > 0.35, Moderate 0.20–0.35, Small < 0.20. Claims about "strong" association require V_corr > 0.35.

**Sensitivity analysis on dyad definition:** Run full extraction at word-distance thresholds of 5, 7, 10, and 15 words. Report which key findings (top dyad pairs, JJK distribution, Meccan/Medinan shift) are stable across thresholds. Publish sensitivity table in Paper 0 supplementary materials.

## 5.9 Step 9 — LLM-Assisted Tagging (HITL Pipeline v2.0)

### For Computational/Data Science Audience

The HITL pipeline uses Claude Sonnet as a first-pass tagger for two tasks: (1) macro and micro verse theme classification, and (2) relationship type heuristic (pre-decision-tree suggestion). JJK classification is **not** done by LLM — it is done by the researcher directly against Al-Qushayrī's classifications.

**Prompt design requirements (v2.0):**

- Prompts are written and pilot-tested on a 20-dyad calibration set _before_ scale application.
- Calibration set = 20 dyads with highest-confidence HITL-validated labels (known-correct answers).
- Prompt accuracy threshold: ≥ 80% agreement with known-correct answers before accepting for scale use.
- If prompt accuracy < 80%, the prompt is revised and retested.
- All prompts published verbatim in Paper 0 supplementary materials.
- System prompt includes: task definition, taxonomy definitions with examples, explicit instructions for ambiguous cases, and few-shot examples (3 per category for theme tagging).

**LLM output handling:**

- LLM output = first-pass suggestion only. Never primary evidence.
- 100% researcher HITL review of all LLM suggestions against tafsīr sources.
- Disagreements between LLM suggestion and researcher decision logged with rationale.
- Disagreement rate reported in Paper 0 as a calibration metric.

### 5.8.1 Stratified IRR Sampling (v2.0 critical change from v1.0)

The v1.0 IRR sample was random 10% of corpus. This is methodologically insufficient because the high-priority rows (CRITICAL and HIGH semantic surprise) are exactly where error is most consequential and where random sampling will under-represent them.

**v2.0 IRR sampling design:**

- **Stratum 1 (mandatory):** All 32 CRITICAL rows (semantic surprise > 3.5 bits) — 100% validation by Islamic Studies consultant.
- **Stratum 2 (mandatory):** All 20 HIGH rows (semantic surprise 2.5–3.5 bits) — 100% validation by Islamic Studies consultant.
- **Stratum 3 (standard):** Random 20% of remaining 125 STANDARD rows.
- **Total IRR sample:** 52 + 25 = 77 dyads (~44% of corpus).

This stratified design provides maximum coverage where it matters most while remaining feasible for a consultant with limited time.

## 5.10 Step 10 — Tafsīr-Grounded Interpretation

Computational findings are interpreted through classical exegetical tradition. For each significant pattern, the relevant tafsīr passages are consulted: did classical scholars notice this pattern? How did they explain it? Does the computational finding confirm, extend, or challenge the classical interpretation?

Al-Rāzī's _Mafātīḥ al-Ghayb_ is the primary classical interlocutor at the pair level — he is uniquely systematic in justifying specific name pairs at specific verse closings. Al-Ṭabarī provides early linguistic grounding. Ibn Kathīr provides standard Sunni exegetical validation. Al-Qurṭubī provides legal and contextual thematic tagging validation.

This step is not decorative. It is the scholarly warrant for the theological claims. Without it, the paper is a computer science paper about a text it does not understand. With it, it is a contribution to Islamic scholarship that happens to use computational tools.

---

# 6. Reproducible Research Pipeline and Tech Stack

The biggest failure mode in Digital Humanities is the "black box" effect: a researcher produces a graph, but no one can trace exactly how the data moved from the raw XML to the published image. This programme is designed to be fully transparent, versioned, and auditable at every layer. The stack below is organised by function — not by tool — so collaborators can understand _why_ each component exists before they learn _how_ to use it.

---

## 6.1 Layer 1 — Primary Data Sources

|Resource|Description|Access|
|---|---|---|
|Tanzil.net XML Corpus (v2.1.0)|Complete Qur'an, Unicode Arabic XML, Meccan/Medinan tags, verse numbering|Free — tanzil.net|
|Al-Maktaba al-Shāmila|Complete classical tafsīr in Arabic — Al-Ṭabarī, Ibn Kathīr, Al-Qurṭubī, Al-Rāzī|Free — shamela.ws|
|OpenITI Corpus|Machine-readable classical Arabic texts including tafsīr|Free — openiti.org|
|Qur'anic Arabic Corpus (Leeds)|Morphologically annotated Qur'an — supplementary morphological reference|Free — corpus.quran.com|
|Al-Qushayrī _Sharḥ Asmā'_|Primary JJK classification source|Print edition (Dār al-Kutub) / Shamela|

---

## 6.2 Layer 2 — HITL Interface (Data Entry and Validation)

**Tool: Airtable**

The Islamic Studies consultant is not a developer. They need a UI that feels like a spreadsheet but behaves like a database. Airtable solves this cleanly.

**Why Airtable and not Excel:**

- Excel has no version control, no linked records, and no audit trail. It is where data goes to die across a multi-year, multi-collaborator programme.
- Airtable allows _Views_: a "Consultant View" can hide the statistical columns (NPMI, Z-scores, bootstrap CIs) and display only the Arabic text, the verse, and the JJK classification dropdowns. This prevents the consultant from accidentally overwriting quantitative fields while entering theological notes.
- Airtable has a Snapshot/Revision History feature. If a collaborator changes 40 labels in a session, yesterday's state can be restored.
- Airtable supports dropdown fields, linked records, and mandatory field completion — enforcing data integrity without requiring the consultant to know what data integrity means.

**The workflow:** Airtable is the interface; it is never the source of truth. The source of truth is always the Git-versioned CSV (Layer 3). Export from Airtable → commit to GitHub is the canonical data flow, not the reverse.

**Shared annotation interface:** The Airtable base is shared with the Islamic Studies consultant for stratified HITL annotation (Section 5.9). The principal researcher retains admin rights. All consultant edits are logged in Airtable's revision history before being merged into the canonical CSV.

---

## 6.3 Layer 3 — Version Control (The Source of Truth)

**Tool: GitHub (private repository) + Git-versioned CSVs + Zenodo (public archive)**

The truth of this project is not in Airtable. It is in a CSV file committed to a private GitHub repository. Every change to the 177-dyad dataset must be traceable to a commit with a descriptive message.

**The non-negotiable requirement:** When Paper 1 is submitted, the methodology section must be able to state: _"This paper was based on Dataset v1.2 (GitHub commit: a1b2c3d, Zenodo DOI: 10.5281/zenodo.XXXXXXX)."_ If a homonym correction is made six months into Paper 3, that correction must be traceable — and every paper based on a prior dataset version must be re-evaluated against the change.

**Repository structure:**

```
/data
  /raw           ← Tanzil XML, unchanged
  /processed     ← dyad_dataset_v*.csv, master_names_v*.csv
  /outputs       ← network exports (GraphML, GEXF, CSV edge lists)
/code
  /extraction    ← CAMeL Tools pipeline, name matching
  /analysis      ← null models, bootstrap CIs, motif analysis
  /visualization ← Gephi exports, Plotly/Seaborn scripts
/prompts         ← versioned LLM prompts (published with Paper 0)
/docs            ← this dossier, IRR protocols, decision trees
requirements.txt ← pinned Python dependency versions
```

**Zenodo releases:** Each major dataset version that underpins a paper submission gets a Zenodo release with its own DOI. A paper with a Zenodo DOI for the dataset is treated as reproducible science. A paper that says "data available upon request" is treated as a soft humanities document.

---

## 6.4 Layer 4 — Computational Engine (Arabic NLP and Analysis)

**Language: Python 3.11+**

Python is the only language with the specific ecosystem needed for this project's combination of Arabic NLP, graph theory, and statistical analysis. R is not used (no Arabic NLP ecosystem comparable to CAMeL Tools). MATLAB is not used (proprietary, not reproducible). Julia is not used (immature NLP tooling for Arabic).

**Environment management: Conda or Poetry (mandatory)**

All dependency versions must be pinned. If CAMeL Tools updates and changes its lemmatization logic, the entire dataset could shift without anyone noticing. Pin everything. The `requirements.txt` (or `pyproject.toml` if using Poetry) is committed to GitHub and never modified without a version bump and a note in the commit message explaining why.

### Core Libraries

|Library|Role|Critical notes|
|---|---|---|
|**CAMeL Tools** (NYUAD)|Arabic morphological analysis and lemmatization|Non-negotiable. The only library capable of handling the morphological complexity of Classical Qur'anic Arabic — definite article variation, construct state forms, pronoun clitics, homonym disambiguation — with the precision required for publication-grade extraction. `pip install camel-tools`|
|**Pandas**|Tabular data manipulation|Industry standard. All dataset transformations, merges, and exports.|
|**NetworkX**|Graph construction, centrality, motif enumeration, degree-preserving null model|Fast enough for 50 nodes in-memory — no graph database needed. Use for all graph math: `enumerate_all_cliques`, `subgraph_isomorphisms_iter`, betweenness, weighted degree, Louvain (via `python-louvain`). Do not use Neo4j — 50 nodes does not justify a graph database.|
|**python-louvain**|Louvain community detection|Run 100 times with different seeds; report consensus partition.|
|**SciPy**|Chi-square, bootstrap resampling, Z-scores|All inferential statistics.|
|**Statsmodels**|Cramér's V (bias-corrected), confidence intervals|Required for V_corr reporting in all chi-square results.|
|**NumPy**|Numerical operations, random seeds|Pin the random seed in all permutation and bootstrap procedures. Report the seed value in Paper 0.|

**What is explicitly not used:**

- **Neo4j or any graph database:** You have 50 nodes. Neo4j is a Boeing 747 for crossing the street. NetworkX is correct at this scale.
- **AI-only extraction pipelines:** If you use an LLM to perform name extraction without CAMeL Tools morphological normalization and HITL review, the results will contain hallucinated dyads and missed homonyms. This will be identified in peer review.
- **Excel for any computation:** No formulas, no pivot tables, no analysis in Excel. Excel is for nothing in this pipeline.

---

## 6.5 Layer 5 — Visualization

**Tools: Gephi (network topology) + Plotly / Seaborn (statistics)**

### Network Visualization — Gephi 0.10

Gephi is used exclusively for the final publication-quality network visualizations. NetworkX produces "hairballs" at 50 nodes with default layouts; Gephi produces publication figures.

**Required settings:**

- Layout: **ForceAtlas2** — reveals community cluster structure naturally. Do not use Fruchterman-Reingold; it does not separate communities as cleanly at this scale.
- Node size: weighted by degree centrality (Stable and Moderate nodes only — Section 5.8).
- Node color: JJK class (Jalāl = red/coral, Jamāl = green/teal, Kamāl-epistemic = blue, Kamāl-ontological = purple, Disputed = grey).
- Edge weight: raw co-occurrence frequency (NPMI as edge label for canonical pairs only).
- Export: SVG for print, PNG at 300dpi for journals that require raster figures.

**Gephi workflow:** NetworkX produces the validated, analyzed network → export to GEXF → import into Gephi → apply ForceAtlas2 → run Louvain in Gephi as visual confirmation of NetworkX consensus communities → export.

### Statistical Visualization — Plotly and Seaborn

|Plot type|Tool|Papers|
|---|---|---|
|NPMI distribution with bootstrap CI bands|Seaborn|Papers 0, 1|
|Semantic surprise histogram (by HITL priority tier)|Plotly (interactive)|Papers 0, 3|
|Motif frequency vs. null distribution|Seaborn|Paper 1|
|Meccan/Medinan JJK composition shift|Seaborn stacked bar|Papers 1, 3|
|Dyad–theme chi-square heatmap|Seaborn|Paper 3|
|Dynamic Essentialism — Edge vs. Node locus (conceptual)|Plotly|Paper 5|

**Plotly for digital humanities outputs:** Plotly generates interactive HTML figures that can be embedded in a programme website, supplementary materials, or a Jupyter notebook. For Digital Humanities venues, interactive figures are a feature, not a distraction.

---

## 6.6 Layer 6 — AI and LLM Tools (HITL Pipeline)

|Tool|Role|Hard constraint|
|---|---|---|
|Claude Sonnet (Anthropic)|First-pass macro and micro verse theme tagging; relationship type heuristic suggestion|First-pass only. All output HITL-validated by researcher against tafsīr.|
|Python prompt templates|Versioned in GitHub `/prompts/` directory|Published verbatim with Paper 0 supplementary materials.|
|GPT-4 (optional)|Cross-validation of theme tags on 10% sample|Not primary evidence. Shared-bias risk acknowledged.|

**What LLM does not do:**

- JJK classification (researcher directly against Al-Qushayrī).
- Homonym resolution (researcher against tafsīr).
- Motif classification (computational, post-hoc, and theological — researcher only).
- HITL reviewer decisions (researcher and Islamic Studies consultant).

---

## 6.7 Layer 7 — Scholarly Sources

### Classical Islamic Sources

|Source|Author|Direct relevance|
|---|---|---|
|_Sharḥ Asmā' Allāh al-Ḥusnā_|Al-Qushayrī (d. 1072)|**Primary JJK classification source**|
|_Al-Maqṣad al-Asnā_|Al-Ghazālī (d. 1111)|Secondary name inclusion validator|
|_Mafātīḥ al-Ghayb_|Fakhr al-Dīn Al-Rāzī (d. 1210)|**Primary tafsīr interlocutor** — systematic pairing justifications|
|_Jāmiʿ al-Bayān_|Al-Ṭabarī (d. 923)|Early tafsīr; linguistic analysis|
|_Tafsīr al-Qur'ān al-ʿAẓīm_|Ibn Kathīr (d. 1373)|Standard Sunni validation source|
|_Al-Jāmiʿ li-Aḥkām al-Qur'ān_|Al-Qurṭubī (d. 1273)|Legal/contextual tagging validation|
|_Al-Futūḥāt al-Makkiyya_|Ibn ʿArabī (d. 1240)|Kamāl-ontological; tajallī framework for Dynamic Essentialism|
|_Badāʾiʿ al-Fawāʾid_|Ibn al-Qayyim (d. 1350)|Classical pairing logic|

### Modern and Bridge Scholarship

|Source|Author|Relevance|
|---|---|---|
|_The Tao of Islam_|Sachiko Murata (1992)|Best Western-academic Jalāl/Jamāl framework|
|_The Self-Disclosure of God_|William C. Chittick (1998)|Ibn ʿArabī's Names doctrine — tajallī framework|
|_The Qur'an and Its Exegesis_|Helmut Gätje (1976)|Western framework for tafsīr methodology|
|_The Verbal Idioms of the Qur'an_|Mustansir Mir (1989)|Linguistic patterning in Qur'anic language|
|_Scripture, Poetry and the Making..._|Angelika Neuwirth (2019)|Verse-final rhetorical weight; discourse structure|
|_The Rhetoric of the Quran_|Michel Cuypers (2015)|Compositional and directional analysis|
|_Corpus, Method and Case Study_|Dukes (2011)|Computational Qur'anic studies baseline|

---

## 6.8 Full Pipeline Summary — The Reproducible Data Flow

```
[Tanzil XML]
     ↓
[CAMeL Tools — morphological normalization]
     ↓
[Python extraction pipeline — name matching, distance calc, homonym flagging]
     ↓
[Airtable — HITL interface for Islamic Studies consultant annotation]
     ↓
[CSV export → GitHub commit (versioned, auditable)]
     ↓
[Python analysis — NPMI + bootstrap CIs, null models A & B, chi-square + V_corr]
     ↓
[NetworkX — graph construction, centrality, motif enumeration, degree-preserving null]
     ↓
[python-louvain — 100-run consensus communities]
     ↓
[Gephi — ForceAtlas2 layout, publication figures]
     ↓
[Plotly / Seaborn — statistical visualizations]
     ↓
[Zenodo — versioned dataset release with DOI]
     ↓
[LaTeX / Overleaf — paper typesetting]
     ↓
[Journal submission — Paper 0 first to Data in Brief; subsequent papers cite published DOI]
```

Every arrow in this flow is a documented, version-controlled step. No black boxes. No "data available upon request."

---

# 7. Section for Islamic Studies Scholars

_This section is written specifically for tafsīr scholars, kalām specialists, and Islamic Studies academics evaluating this programme or considering collaboration._

## 7.1 What This Research Is and Is Not

**This is not:**

- A theological reform project or reinterpretation of Islamic doctrine.
- A claim that AI or computers can understand or interpret the Qur'an.
- An iʿjāz (miraculous inimitability) claim — we make no revelatory assertions.
- An adjudication between kalām schools or madhāhib.
- An extension to Hadith corpus in its primary phase.

**This is:**

- A computational mapping of a structural pattern that classical scholars — especially Al-Rāzī — consistently observed and commented upon, but never mapped systematically across the full corpus.
- An empirical test of the Jalāl/Jamāl polarity framework that Al-Ghazālī, Al-Qushayrī, and Ibn ʿArabī articulated propositionally.
- A dataset and methodology that will enable future scholarship — in tafsīr, linguistics, and theological education — that we have not predicted.

The relationship between this research and classical tafsīr is one of extension, not replacement. Al-Rāzī spent his scholarly life on exactly these questions. We seek to map, with modern tools, the structure that scholars like Al-Rāzī illuminated through sustained exegetical attention — and to make that map available as open knowledge.

## 7.2 The Role of the Islamic Studies Consultant

The programme requires one Islamic Studies consultant with the following specific qualifications:

- Fluency in classical Arabic (reading Al-Rāzī, Al-Qushayrī, and Al-Ṭabarī in Arabic, not in translation).
- Familiarity with the Sifāt doctrine in the Ashʿarī tradition and awareness of the Muʿtazilī position.
- Ability to classify pairs as Jalāl/Jamāl/Kamāl using the operationalized decision procedure and explain the reasoning.
- Availability for approximately 15–20 hours of structured annotation work (52 CRITICAL/HIGH priority dyads, plus 25 STANDARD sample).

**Compensation:** Co-authorship on Papers 2, 3, and 5 (those papers use the HITL-validated JJK and relationship-type classifications most directly), in accordance with CRediT (Contributor Roles Taxonomy) standards. The specific CRediT roles would include: Validation, Formal Analysis (theological), Writing – Review & Editing.

## 7.3 The JJK Framework — A Note on Classical Sources

The Jalāl/Jamāl/Kamāl framework is not monolithic in the classical tradition:

- **Al-Qushayrī** applies it most systematically and is the primary operational source for this programme.
- **Al-Ghazālī** uses a related but not identical taxonomy in _Al-Maqṣad al-Asnā_ — his categories are not consistently labelled Jalāl/Jamāl, but the polarity is implicit.
- **Ibn ʿArabī** develops the framework most philosophically in _Al-Futūḥāt_ — his treatment of Kamāl names as preconditions for both Jalāl and Jamāl is the theoretical basis for the v2.0 Kamāl-ontological sub-category.
- **Disagreements** between these sources on individual name classification are a finding, not a problem. They are flagged in the Disputed Names register and will be reported in Paper 2 as a section on "classical disagreements and what the co-occurrence data adds."

## 7.4 On Meccan and Medinan Classification

The programme uses the Nöldeke-Schwally chronological ordering as cross-referenced with Tanzil metadata. This is a Western scholarly construction and Islamic scholars may have reservations about it as a primary classification. Our response:

- We use it as a structural variable (revealed in Meccan context vs. Medinan context), not as a historical claim about the precise sequence of revelation.
- Disputed surahs and disputed verses within surahs are flagged in the dataset and excluded from the period-differential analysis.
- The Meccan/Medinan distinction is also recognized in classical Islamic scholarship (Al-Suyūṭī's _Al-Itqān fī ʿUlūm al-Qur'ān_ is the classical source); the Western Nöldeke ordering is used only because it provides a more granular sequential estimate for surah-level analysis.

---

# 8. Paper Pipeline — v2.0

The programme generates six publications from a single unified dataset. Papers are sequenced so each builds on the last. Two v1.0 papers are merged (former Papers 2 and 5 → new Paper 5), and one is replaced (former Paper 4: OWL ontology → new Paper 4: cross-corpus network comparison).

## Paper 0 — Methodology, Dataset, and HITL Pipeline

|Element|Detail|
|---|---|
|**Working title**|Mapping the Divine Name Dyads of the Qur'an: A Morphologically-Normalized, HITL-Validated Corpus Analysis|
|**Core contribution**|Documents dataset construction; CAMeL Tools integration; two-level thematic taxonomy; operationalized JJK and relationship-type decision trees; stratified IRR protocol; sensitivity analysis on dyad definition; open dataset release|
|**Target journal**|_Data in Brief_ (Elsevier, fast review 4–6 weeks) for dataset paper — published first to anchor the programme. _Digital Scholarship in the Humanities_ (Oxford) for full methodology paper.|
|**Companion output**|Dataset published on Zenodo under CC-BY 4.0 with versioned DOI; all code published on GitHub|
|**Publication rationale**|_Data in Brief_ gets the dataset into the public domain immediately, allows subsequent papers to cite a published dataset, and establishes credibility before the slow DSH review cycle|

## Paper 1 — Corpus Frequency, Network Structure, and Motif Architecture

|Element|Detail|
|---|---|
|**Working title**|Divine Name Dyads in the Qur'an: Frequency, NPMI Bonding Strength, Semantic Network Architecture, and Theological Motif Structures|
|**Core contribution**|Full frequency and NPMI analysis (with bootstrap CIs); weighted undirected co-occurrence network; betweenness and degree centrality for Stable/Moderate nodes only; consensus Louvain communities (100-run ensemble); stratified null model significance; Meccan vs. Medinan network comparison (Spearman ρ); **motif enumeration — all statistically over-represented 3-node and 4-node sub-graphs identified against a degree-sequence-preserving null model**|
|**Key findings**|Divine name pairings are non-random; the degree hierarchy is stable across revelation periods (Spearman ρ=0.84); **specific triadic motif patterns are significantly over-represented, suggesting the Qur'an operates with compositional structures beyond isolated pairs**|
|**Target journal**|_Journal of Quranic Studies_ (Edinburgh/SOAS, Scopus Q1–Q2)|
|**Critical constraints**|All centrality claims restricted to Stable and Moderate nodes. All chi-square results report V_corr. NPMI comparisons restricted to pairs where 95% CIs do not overlap. Motif findings reported as "statistically over-represented structural tendencies" — not as generative rules or algorithms. Theological naming of motifs is post-hoc and interpretive.|

## Paper 2 — Jalāl–Jamāl Axis and Semantic Polarity

|Element|Detail|
|---|---|
|**Working title**|The Jalāl–Jamāl–Kamāl Axis: Semantic Polarity in Qur'anic Divine Name Pairings|
|**Core contribution**|Tests revised five-class JJK taxonomy against full corpus; applies conceptual blending theory (Fauconnier & Turner) to balancing dyads; documents classical disagreements on individual name classification; shows Jalāl+Kamāl-epistemic as dominant pairing type and its theological interpretation|
|**Key finding**|The Qur'an structurally performs, at the textual level, the Jalāl–Jamāl balance that classical scholars argued for propositionally — with refinements visible only at the Kamāl-epistemic vs. Kamāl-ontological level of the taxonomy|
|**Target journal**|_Journal of Quranic Studies_; _Islam and Christian–Muslim Relations_; _Religions_ (MDPI, Scopus Q1)|
|**Classical interlocutors**|Al-Qushayrī (primary), Al-Ghazālī (secondary), Ibn ʿArabī (Kamāl category)|

## Paper 3 — Contextual Correlation and Motif–Theme Structural Tendencies

|Element|Detail|
|---|---|
|**Working title**|Divine Name Dyads as Contextual Signals: Dyad–Theme and Motif–Theme Structural Tendencies in the Qur'anic Corpus|
|**Core contribution**|Statistical correlation (χ², V_corr) between dyad types and verse themes at both macro (7) and micro (20) granularity levels; **second analytical layer: motif–theme correlation — which statistically over-represented triadic structures are associated with which micro-level thematic categories**; semantic surprise index (32 CRITICAL dyads); period-stratified null model for Meccan/Medinan differential; three structural refrain case studies|
|**Key findings**|Dyad–theme correlation is moderate at macro granularity (V_corr ≈ 0.21) and stronger at micro granularity — granularity-sensitivity differential is itself a publishable finding. **Specific motif structures show differential distribution across thematic categories: e.g., a [Jalāl+Kamāl-epistemic] triadic pattern is statistically over-represented in 'Divine Decree' micro-categories.** High-surprise dyads mark rhetorical exceptions documented in Al-Rāzī.|
|**Framing constraint**|Motif–theme findings are framed as "statistically over-represented structural tendencies," not as compositional rules or algorithms. The claim is descriptive and probabilistic, not deterministic.|
|**Target journal**|_Arabica_ (Brill, Scopus Q1); _Journal of Arabic and Islamic Studies_; _Al-Qantara_ (CSIC)|

## Paper 4 (Revised) — Cross-Corpus Religious Network Comparison

|Element|Detail|
|---|---|
|**Working title**|Comparing Divine Name Networks Across Scriptural Traditions: A Graph-Theoretic Framework|
|**Core contribution**|Graph-theoretic comparison of the Qur'anic divine name co-occurrence network against: (a) the divine name network derived from the Hebrew Bible (Elohim, YHWH, El Shaddai, Adonai, and their co-occurrence contexts); (b) divine epithet co-occurrence in the Rigveda (where available through digital corpus). Comparison metrics: network density, modularity, average path length, hub concentration, inter-community edge ratio|
|**Rationale for replacement of v1.0 Paper 4**|The v1.0 OWL ontology paper is not publishable in _Applied Network Science_ or _Semantic Web Journal_ without alignment to an upper ontology and formal consistency checks. A cross-corpus comparison paper uses the same analytical framework, targets the same journals, and produces a substantially more impactful contribution — it establishes the Qur'anic divine name network as a data point in a comparative religion network science|
|**Target journal**|_Applied Network Science_ (Springer, Scopus Q1); _Religions_ (MDPI); _Journal of the American Oriental Society_|
|**Feasibility note**|Hebrew Bible divine name co-occurrence can be derived from the SEFARIA digital corpus. Rigveda availability depends on digital humanities partnerships — if unavailable, paper proceeds as Qur'an–Hebrew Bible comparison only|

## Paper 5 (Merged) — Dynamic Essentialism: Structural Regularity and Relational Meaning in Qur'anic Divine Name Pairings

|Element|Detail|
|---|---|
|**Working title**|The Edge as Meaning: Dynamic Essentialism and Relational Ontology in the Qur'anic Divine Name System|
|**Core contribution**|Proposes Dynamic Essentialism as a new theoretical position: Divine Names are essentially fixed at the node level (stable semantic properties, stable topology across periods) while the dyadic pairing relation — the Edge — is the primary locus of meaning and contextual calibration. Engages the essentialism/contextualism debate as the literature review, not the conclusion. Introduces relational ontology (grounded in the network's edge structure) as the positive claim. Deploys high-surprise dyads as the key evidence: a surprising pairing is a "relational exception" — a moment where the text intentionally breaks dominant motif patterns to produce a high-intensity theological signal located in the Edge, not in either Node alone. Includes 300-word kalām contextualization (Ashʿarī / Muʿtazilī / Ibn ʿArabī — mapping onto Node-level essentialism, low-modularity prediction disconfirmed, and tajallī as the closest classical analogue to the Edge-locus claim).|
|**Rationale for merger**|Former Paper 2 (structural pattern) and Paper 5 (contextual modulation) addressed claims in tension. Merging them into a single paper unified by Dynamic Essentialism produces a stronger philosophical contribution. The tension between structural regularity and contextual deployment is the argument — resolved by locating regularity at the Node and deployment at the Edge.|
|**Evidence hierarchy**|(1) Stable network topology across periods → Node-level essentialism confirmed. (2) High-surprise dyads → Edge-level contextual calibration confirmed. (3) Significant motif structures → Relational grammar confirmed at triadic level. (4) Hapax dyads as sub-analysis: which JJK combinations appear only once, and what does their singularity reveal about the outer limits of the dyad system?|
|**Target journal**|_Sophia_ (Springer, Scopus Q1); _Journal of Religion_ (Chicago); _Philosophy East and West_; _International Journal for Philosophy of Religion_|
|**Kalām section requirement**|The Ashʿarī/Muʿtazilī mapping must appear. The Muʿtazilī position predicts low modularity; observed community structure disconfirms it. Ibn ʿArabī's tajallī is the closest classical analogue to Dynamic Essentialism — divine self-disclosure through specific relational modes, not intrinsic static essence. This is not presented as Islamic theology but as a classical framework through which the data can be read.|

---

# 9. Section for Network Scientists and Computational Researchers

_This section addresses the specific methodological and technical questions that network science and computational linguistics reviewers will raise._

## 9.1 Why This Network Is Interesting to Network Scientists

The divine name co-occurrence network has four properties that make it atypical and analytically interesting:

1. **Extreme hub dominance with small N:** Al-ʿAzīz has weighted degree 71 in a network of 50 nodes. This is an unusually concentrated hub structure for a 50-node network and raises the question of whether it reflects a scale-free (Barabási-Albert) growth mechanism or a designed theological hierarchy.
    
2. **Very high hapax rate (90%):** 64/71 unique pairs occur exactly once. This is not noise — it reflects the finite Qur'anic corpus and the theological diversity of contextual divine-name deployment. Network metrics on hapax edges are unreliable; the programme explicitly separates canonical (n≥5) from hapax edge analysis, and treats hapax dyads as a primary sub-analysis in Paper 5.
    
3. **Period-structured temporal evolution:** The corpus has a known approximate temporal ordering (Meccan before Medinan revelation). This allows the network to be split into two "time periods" and compared — a form of temporal network analysis rarely applied to religious texts. Spearman ρ=0.84 on degree hierarchy across periods is the stability finding; Jalāl+Jalāl doubling (+17.8pp) is the evolution finding.
    
4. **Motif over-representation as a local topology signal (v2.1):** Beyond global metrics, the network's local structure — which 3-node and 4-node sub-graphs are statistically over-represented against a degree-sequence-preserving null — reveals the "molecular" compositional grammar of the text. This is a novel application of motif analysis to a sacred-text network. The combination of small N, high hapax rate, and theologically interpretable node labels makes the motif findings interpretable in ways that purely sociological or biological networks are not.
    

## 9.2 Known Limitations Acknowledged for Reviewers

|Limitation|Consequence|Mitigation|
|---|---|---|
|N=177 dyads, 50 nodes|Many centrality estimates are statistically unstable|Bootstrap CIs reported; only Stable/Moderate nodes cited as primary findings|
|Louvain resolution-parameter dependence|11 communities may be artefact of γ=1.0 choice|100-run consensus + sensitivity at γ=0.5 and γ=2.0|
|Single corpus (one recitation)|Findings apply to Ḥafṣ riwāya specifically|Documented; other riwāyāt checked for dyad-affecting variants|
|NPMI on low-frequency pairs|CIs are very wide for n=1,2,3 pairs|NPMI comparisons restricted to pairs with non-overlapping 95% CIs|
|Undirected model loses directionality information|Cannot test whether N1→N2 ordering carries meaning|Directionality retained as dataset attribute; descriptive analysis in Paper 1; note as limitation|

## 9.3 Code and Reproducibility Standards

- All extraction, cleaning, network construction, and statistical analysis code published on GitHub (MIT license) alongside Paper 0.
- Dependency versions pinned in `requirements.txt`.
- Random seeds fixed and reported for all permutation tests and bootstrap analyses.
- Full dataset with all columns published on Zenodo (CC-BY 4.0) with versioned DOI.
- Paper 0 contains a reproducibility checklist modelled on the ACM artifact evaluation standard.

---

# 10. Section for Philosophers of Religion and Theologians

_This section addresses the philosophical and theological arguments of the programme for readers in philosophy of religion, Islamic philosophy, and systematic theology._

## 10.1 The Central Philosophical Claim — Dynamic Essentialism

This programme does not merely produce data relevant to the essentialism/contextualism debate in philosophy of religion — it proposes a resolution. The debate has stalled because both sides treat individual Names (the Node) as the primary object of inquiry: is Al-Raḥīm essentially merciful in a fixed, context-independent way, or is its mercy contextually modulated? The Qur'anic dyad data reveals that this is the wrong unit of analysis.

**The positive claim of this programme:** The dyadic Edge — the pairing relation between two names — is the primary locus of theological meaning in the Qur'anic closing formula system. This is _Dynamic Essentialism_:

- **Essential at the Node level.** Divine Names carry stable, immutable semantic properties. Al-ʿAzīz is always a Jalāl name (power, transcendence). Al-Raḥīm is always a Jamāl name (mercy, intimacy). These properties do not vary with context. The network topology confirms this: Spearman ρ=0.84 on the degree hierarchy across Meccan and Medinan periods means the same names are the same hubs in both revelation contexts. The Nodes are stable.
    
- **Dynamic at the Edge level.** The _pairing_ of names — which two Nodes are connected in any given verse — is where the text does its active theological work. The meaning produced by Al-ʿAzīz–Al-Raḥīm is not a sum of their individual properties; it is a third meaning generated by the relational tension between power and mercy in a specific verse context. When the same dyad closes nine different verses in Surah 26, each closing activates the same relational vector in a different narrative situation. The Edge is dynamic.
    
- **The synthesis.** The Qur'an operates a system of Relational Attributes: the divine essence is immutable (essential Nodes), but the presentation of that essence to the human recipient is dynamically calibrated through the specific pairing selected for each verse (dynamic Edges). This is neither pure essentialism (which cannot account for the contextual variation in high-surprise dyads) nor pure contextualism (which cannot account for the stable topology and dominant canonical pairs). It is a position not articulated in the existing literature on divine attribute theory.
    

**What the data cannot claim.** Dynamic Essentialism is a claim about the Qur'anic _text's_ compositional structure, not about the nature of the divine essence itself. The data resolves the _textual_ question, not the _metaphysical_ one. Whether divine attributes are _really_ immutable remains a theological and metaphysical question beyond the reach of corpus analysis.

## 10.2 The Three Evidence Layers

Paper 5 argues Dynamic Essentialism through three independent evidence layers, each necessary and none sufficient alone:

**Layer 1 — Network stability (Node-level essentialism confirmed).** The Spearman ρ=0.84 finding means that the degree hierarchy of names — which names are most central to the pairing system — is stable across the two revelation contexts. If contextual factors drove the choice of names completely, we would expect a different hub structure in Meccan versus Medinan revelation. We do not find this. The Nodes are stable.

**Layer 2 — High-surprise dyads (Edge-level dynamics confirmed).** The 32 CRITICAL-priority dyads (semantic surprise > 3.5 bits) are the programme's most important theological evidence. A "surprising" dyad is one where the JJK combination is unexpected given the verse theme — the text is deploying a relational vector that breaks the dominant pattern. The surprise is not located in either name alone (both are familiar, essential, well-attested). The surprise is entirely in their _relation_ in that context. Al-Rāzī comments on exactly these moments, though without the statistical language to quantify them. This is where Dynamic Essentialism shows its interpretive power: it explains why a "wrong" pair would be theologically wrong — not because either name is wrong in isolation, but because the Edge it would create is contextually inappropriate.

**Layer 3 — Motif over-representation (relational grammar confirmed at triadic level).** If the Edge is the primary unit of meaning, we would expect the Qur'an to operate not just with isolated pairings but with recurring triadic relational structures — compositional patterns that deploy multiple Edges together. The motif analysis (Section 5.7) tests exactly this. Statistically over-represented 3-node sub-graphs are evidence that the relational grammar operates above the dyadic level, confirming that the Edge-as-meaning claim scales up from pairs to higher-order compositional units.

## 10.3 The Kalām Mapping — Ashʿarī, Muʿtazilī, and Ibn ʿArabī

Dynamic Essentialism engages three classical Islamic positions on divine attributes. This mapping is required in Paper 5 — reviewers at _Sophia_ and _Journal of Religion_ will expect it, and the Muʿtazilī position makes an empirically testable prediction.

**Ashʿarī position** (Al-Bāqillānī, Al-Juwaynī, Al-Ghazālī): Divine attributes are real, ontologically distinct, and subsistent in the divine essence. Each name names a genuinely distinct property. This maps onto Node-level essentialism — names are distinct because they carry distinct essential properties. The observed modularity of the network (stable community clusters separating, e.g., epistemic names from Jalāl names) is consistent with the Ashʿarī prediction of genuine categorical distinctness.

**Muʿtazilī position** (Al-Naẓẓām, Abū ʿAlī al-Jubbāʾī): Divine attributes are not ontologically distinct from the divine essence. Names are different linguistic expressions of the same undivided reality. This predicts a network with _low modularity_ — if all names express the same undivided reality, co-occurrence patterns should show high integration and no stable community structure. The observed community structure (subject to Louvain resolution-parameter sensitivity, documented in Section 5.6) is preliminary evidence _against_ the Muʿtazilī prediction. This is reported with appropriate epistemic hedging — the community structure is sensitive to the resolution parameter γ, and the programme does not claim to settle the kalām debate. It claims only that the data is more consistent with Ashʿarī categorical distinctness at the Node level than with Muʿtazilī undifferentiation.

**Ibn ʿArabī's tajallī framework** (_Al-Futūḥāt al-Makkiyya_): Divine names are real and distinct, but they are relational properties of divine self-disclosure (tajallī) rather than intrinsic properties of the divine essence. The name is not a description of God-in-Himself but of God-as-disclosed-to-creation in a specific relational mode. This is the classical framework closest to Dynamic Essentialism — and the one the programme engages most directly in Paper 5. The Kamāl-ontological sub-category in the v2.1 JJK taxonomy (Al-Ḥayy, Al-Qayyūm, Al-Wāḥid, Al-Ḥaqq) names precisely those attributes that are preconditions for divine relational action — God's life, self-subsistence, unity, and reality as the ground from which tajallī proceeds. The co-occurrence of Kamāl-ontological names with both Jalāl and Jamāl names in the dyad data is therefore not merely a statistical pattern; it is structurally congruent with Ibn ʿArabī's schema in which ontological names ground and make possible the relational disclosure of majesty and mercy.

## 10.4 The Comparison with Western Analytic Philosophy of Religion

For readers working primarily in Anglophone philosophy of religion:

**Alston (1989), Swinburne (1993):** Both argue that divine attributes are essential, intrinsic, and context-independent. Dynamic Essentialism agrees at the Node level but diverges at the Edge level — the programme's contribution is to show that the _deployment_ of essentially stable names is contextually sensitive in statistically demonstrable ways that neither Alston nor Swinburne's frameworks predict or explain.

**Murata (1992), Chittick (1998):** Both argue for contextual modulation of divine attributes drawing on Ibn ʿArabī. Dynamic Essentialism is closer to their position at the Edge level but provides what they lack: a formal, testable, data-grounded account of _how_ contextual modulation operates — through the specific pairing of essentially stable names, quantifiable by NPMI, semantic surprise, and motif significance.

The contribution of this programme to Western analytic philosophy of religion is to move the essentialism/contextualism debate from purely analytical argument to empirically grounded structural analysis — while remaining epistemically honest about what corpus data can and cannot establish.

---

# 11. Timeline and Phases

The programme has no artificial deadline. Quality of the dataset determines quality of every paper. Phase 2 (dataset construction and validation) is the longest and most critical phase.

## 11.1 Phase Overview

|Phase|Duration|Key deliverables|Dependencies|
|---|---|---|---|
|**Phase 1 — Setup**|Months 1–2|Tanzil XML downloaded and verified; Python 3.11+ environment with CAMeL Tools configured and pinned (`requirements.txt`); Al-Qushayrī classification table complete; **private GitHub repository initialized with folder structure**; Airtable base created with Consultant View; tafsīr PDFs acquired|None|
|**Phase 2 — Dataset Construction**|Months 2–7|CAMeL Tools extraction pipeline validated; JJK classifications complete (researcher vs. Al-Qushayrī directly); two-level thematic tagging (LLM first-pass → HITL); stratified IRR with Islamic Studies consultant (52 CRITICAL/HIGH + 25 STANDARD); IRR κ ≥ 0.65 confirmed; sensitivity analysis at 4 distance thresholds; **first Zenodo release (dataset v1.0 with DOI)**|Phase 1 complete|
|**Phase 3 — Network Analysis**|Months 6–8 (parallel with late Phase 2)|Undirected weighted graph constructed in NetworkX; bootstrap CIs on centrality (B=5000); 100-run Louvain consensus with γ sensitivity; Null Models A and B run; dyadic entropy computed; **motif enumeration (3-node and 4-node sub-graphs, degree-preserving null, 10,000 permutations)**; Gephi ForceAtlas2 visualization; Plotly/Seaborn statistical figures|Dataset v1.0 locked on Zenodo|
|**Phase 4 — Paper 0 and Data Paper**|Months 8–11|_Data in Brief_ dataset paper submitted (fast track); _DSH_ methodology paper drafted; **all code + versioned prompts published on GitHub (MIT license)**; reproducibility checklist completed|Phase 2 complete|
|**Phase 5 — Papers 1 and 2**|Months 11–16|Paper 1 (network structure + motif architecture) submitted; Paper 2 (JJK axis) submitted; responding to reviewer comments|Phase 3 complete|
|**Phase 6 — Papers 3 and 4**|Months 16–22|Paper 3 (dyad–theme + motif–theme structural tendencies) submitted; Paper 4 (cross-corpus comparison) submitted|Papers 1–2 accepted or in revision|
|**Phase 7 — Paper 5**|Months 22–26|Paper 5 (Dynamic Essentialism — structural regularity + relational ontology) submitted|Papers 2–3 accepted or in revision|
|**Phase 8 — Monograph**|Months 26–36|Scholarly monograph synthesizing programme for educated Muslim and non-Muslim readership|Papers 1–5 accepted|

## 11.2 Parallel Track: Consultant Annotation

The Islamic Studies consultant's stratified annotation (52 CRITICAL/HIGH rows) runs concurrently with Phase 3 network analysis — not sequentially after Phase 2. A shared annotation interface (Airtable or Notion database) allows the consultant to enter tafsīr notes and classification decisions while the principal researcher handles network construction. Serializing these phases adds 2–3 months unnecessarily.

---

# 12. Resources and Funding

## 12.1 Personnel

|Role|Responsibilities|Time commitment|
|---|---|---|
|Principal Researcher|Overall direction; dataset design; JJK classification (against Al-Qushayrī); tafsīr validation; paper writing; all final decisions|Full-time equivalent across programme|
|Data Engineer (self or contracted)|CAMeL Tools integration; Python extraction pipeline; network construction; statistical analysis|~3 months intensive (Phases 2–3); lighter ongoing support|
|Islamic Studies Consultant|Stratified IRR annotation (52 CRITICAL/HIGH + 25 STANDARD rows); review of tafsīr-based claims; co-authorship on Papers 2, 3, 5|~20 hours intensive + reading time|
|Language Editor|Arabic transliteration consistency; academic English proofread|One-time per paper (~5 hours)|
|Network Science Collaborator (optional)|Graph theory and community detection expertise; co-authorship on Paper 4 (cross-corpus)|~2 months for Paper 4 preparation|

## 12.2 Budget Estimate

|Item|Estimated cost|
|---|---|
|Software (all open-source)|USD 0|
|Data sources|USD 0|
|LLM API costs (Claude Sonnet, theme tagging ~177 verses)|USD 10–30|
|Islamic Studies consultant (annotation + co-authorship)|USD 500–2,000 or co-authorship-only arrangement|
|Journal submission fees (OA journals)|USD 500–2,500 per paper (varies by journal; _Data in Brief_ ~USD 500; _Religions_ MDPI ~USD 1,800)|
|Language editing|USD 100–300 per paper|
|Conference presentations (2–3 targeted)|USD 500–2,000 per conference|
|**Total estimated programme cost**|**USD 3,000–12,000** depending on OA choices and conferences|

## 12.3 Potential Funding Sources

|Funder|Programme|Notes|
|---|---|---|
|Islamic Development Bank (IsDB)|Research & Innovation Fund|Strongest fit — Islamic studies + computational methods|
|British Academy / Leverhulme Trust|Small Research Grants|Humanities projects ≤ GBP 10,000 — good fit for Phase 2–3|
|Qatar National Research Fund (QNRF)|National Priorities Research Programme|Digital humanities and Islamic studies intersection|
|Andrew W. Mellon Foundation|Digital Humanities grants|Requires institutional affiliation|
|IIUM Research Grants|Open to external collaborators|Islamic studies focus|
|University internal funds|Depends on affiliation|Data engineer contract most fundable here|

---

# 13. Collaboration Opportunities

This programme welcomes collaboration in specific, well-defined roles. Co-authorship follows CRediT (Contributor Roles Taxonomy) standards — formal, documented, role-specific.

|Role|Papers|What is needed|What is offered|
|---|---|---|---|
|**Islamic Studies Scholar** (tafsīr, kalām)|Papers 2, 3, 5|Classical Arabic fluency; familiarity with Sifāt doctrine; 20 hours structured annotation|Co-authorship on Papers 2, 3, 5; full CRediT attribution|
|**Corpus Linguist**|Papers 0, 1|Expertise in collocation analysis and corpus methods; ability to review methodology paper|Co-authorship on Papers 0, 1|
|**Network Scientist**|Paper 4|Graph theory and community detection expertise; interest in religious text networks|Co-authorship on Paper 4 (cross-corpus comparison)|
|**Arabic Computational Linguist**|Papers 0, 1|NLP expertise with classical Arabic; CAMeL Tools experience; morphological disambiguation|Co-authorship on Paper 0|
|**Philosopher of Religion**|Paper 5|Expertise in divine attribute theory; familiarity with Alston, Swinburne, Islamic kalām|Co-authorship on Paper 5|
|**Institutional Partner**|All|University or research centre affiliation for grant applications and journal access|Acknowledgement; potential grant co-applicant status|

To discuss collaboration, contact the Principal Researcher with: (a) your relevant expertise, (b) which paper(s) you are interested in, and (c) your available time in the next 12 months.

---

# 14. Scope Boundaries (Hard — Included in Every Paper's Methodology Section)

These boundaries are not optional — they are stated explicitly in the methodology section of every paper submitted.

> _This programme is not a theological reform project. It does not reinterpret Islamic doctrine. It does not claim AI understands or interprets the Qur'an. It makes no claims about divine miracle (iʿjāz). It does not extend to Hadith corpora in its primary phase. It does not adjudicate between madhāhib or kalām schools. Computational findings are evidence about the structure of the Qur'anic text — not revelatory claims about the divine. The Islamic Studies consultant's role is validation and co-authorship — the programme does not use LLM output as primary theological evidence under any circumstances._

---

# 15. Expected Impact

## 15.1 Short-Term (Year 1)

- Dataset published on Zenodo — immediately usable by other researchers in Qur'anic studies, Arabic NLP, and digital humanities.
- _Data in Brief_ dataset paper published — gives subsequent papers a citable data source.
- Co-occurrence network visualization — likely to be widely reproduced in Islamic studies and digital humanities contexts.
- Methodology documented for replication in other scriptural corpora.

## 15.2 Medium-Term (Years 1–3)

- 5–6 peer-reviewed papers in Scopus Q1/Q2 journals.
- A cross-corpus religious network comparison framework — reusable by researchers studying Hebrew Bible, Vedic, or Christian doxological name patterns.
- Foundation for a new sub-field: Computational Theology of the Qur'an.

## 15.3 Long-Term

- Scholarly monograph synthesizing the programme for educated Muslim and non-Muslim readership.
- Potential collaboration with institutions building Qur'anic AI systems (semantic search, tafsīr assistants) — the dataset and network are directly applicable.
- Curriculum contribution: the dataset and methodology can be used in Islamic studies and digital humanities graduate courses.

> _The dataset and network graph, once published, will outlast any individual paper. Researchers for decades will be able to ask new questions of this data that we have not yet imagined. This is the hallmark of a foundational research contribution — it enables future work it did not predict._

---

# 16. Contribution Statement (Adaptable by Audience)

## For Academic Papers (use verbatim or adapt)

> This study presents the first computationally rigorous, morphologically normalized, and HITL-validated analysis of paired Divine Names (Asmā' al-Ḥusnā) in the Qur'an. Using the Tanzil XML corpus (riwāyat Ḥafṣ ʿan ʿĀṣim), we extract 177 divine name dyads representing 71 unique pairs across 50 active names, construct a weighted co-occurrence network, and demonstrate statistically — using both corpus-wide and period-stratified permutation null models — that pairing patterns are non-random. Employing a revised five-class JJK taxonomy validated against Al-Qushayrī's _Sharḥ Asmā' Allāh al-Ḥusnā_ and a stratified HITL protocol with Islamic Studies consultant inter-rater reliability (κ ≥ 0.65), we show that dyads cluster according to a revised Jalāl/Jamāl/Kamāl polarity, correlate with verse thematic context at both macro and micro granularity, and function as an embedded interpretive system within the Qur'anic text. The programme contributes an open dataset (Zenodo, CC-BY 4.0), reproducible code (GitHub, MIT), and a multi-paper series spanning corpus linguistics, Islamic theology, network science, and philosophy of religion.

## For Funding Applications

> The Qur'an contains hundreds of verses that close with two of God's names placed together — "the Forgiving, the Merciful"; "the Almighty, the All-Wise." Muslim scholars across centuries have considered these pairings deliberate and theologically meaningful. This project is the first to test that belief scientifically — using computational network analysis, Arabic morphological processing, and rigorous statistical methods across all 6,236 verses. We publish the results as open data and peer-reviewed papers, making this foundational resource freely available to Islamic studies scholars, digital humanists, and AI researchers worldwide.

## For Islamic Scholars

> This research applies contemporary computational methods to validate and extend the insights of classical scholars — particularly Al-Rāzī's systematic attention to why specific divine names close specific verses, and Al-Qushayrī's taxonomy of names according to Jalāl and Jamāl. We do not seek to interpret the Qur'an through AI. We seek to map, with modern tools, the structure that scholars like Al-Rāzī illuminated through sustained exegetical labour — and to make that map available as open knowledge for the entire scholarly community. Every computational finding is checked against classical tafsīr before any claim is made.

---

_وَهُوَ الْغَفُورُ الرَّحِيمُ_

_And He is the Forgiving, the Merciful._

_— Qur'an 2:173 — the most frequently occurring independent divine name dyad_

---

---

# PART II — APPENDICES

---

# Appendix A — Full Critique and Version Change Log (v1.0 → v2.0)

_This appendix documents every change made between v1.0 and v2.0, the precise critique that motivated each change, and the decision rationale. It is retained permanently in this dossier — future collaborators should understand not just what the current design is, but why v1.0 decisions were revised._

---

## A.1 Change Log Summary Table

|ID|Domain|v1.0 design|v2.0 change|Severity of v1.0 flaw|Section reference|
|---|---|---|---|---|---|
|C-01|Statistics|Logistic regression (97.5% accuracy) presented as evidence for essentialism|Removed from paper pipeline / reframed|**Critical — circular argument**|A.2.1|
|C-02|Taxonomy|Kamāl as single class (all non-Jalāl, non-Jamāl names)|Split into Kamāl-epistemic + Kamāl-ontological|**Critical — conceptual overloading**|A.2.2|
|C-03|Taxonomy|5 relationship types without decision procedure or IRR|Formal decision tree + κ ≥ 0.65 IRR standard|**Critical — not publishable**|A.2.3|
|C-04|Statistics|Corpus-wide permutation null model only|Added period-stratified null model (Null Model B)|**Serious — Meccan/Medinan claim unsupported**|A.2.4|
|C-05|Network|Edge table labelled "Undirected" despite directed methodology|Committed to undirected; directed retained as metadata|**Serious — internal contradiction**|A.2.5|
|C-06|Network|Single Louvain run ("11 communities")|100-run consensus partition; resolution parameter reported|**Serious — single run not reproducible**|A.2.6|
|C-07|Corpus|Surface-form Unicode string matching|CAMeL Tools morphological normalization|**Serious — fragile pipeline**|A.2.7|
|C-08|Papers|Papers 4 (OWL ontology) and original Paper structure|Paper 4 replaced with cross-corpus comparison; Papers 2+5 merged|**Serious — Paper 4 not publishable; Papers 2+5 redundant**|A.2.8|
|C-09|HITL|Random 10% IRR sample|Stratified IRR: 100% of CRITICAL/HIGH rows + 20% STANDARD|**Serious — under-represents high-priority rows**|A.2.9|
|C-10|Theology|Al-Ghazālī as primary JJK classification source|Al-Qushayrī as primary; Al-Ghazālī secondary|**Serious — source mismatch with theory**|A.2.10|
|C-11|Statistics|NPMI reported without confidence intervals|Bootstrap CIs on NPMI; comparisons restricted to non-overlapping CIs|**Serious — small-n NPMI unreliable**|A.2.11|
|C-12|Taxonomy|7-category macro thematic taxonomy|Two-level taxonomy: 7 macro + 20 micro|**Serious — too coarse for dyad-theme correlation**|A.2.12|
|C-13|Infrastructure|No version control on dataset|Git repository from day one; versioned Zenodo releases|**Serious — multi-year programme without version control**|A.2.13|
|C-14|Publication|Paper 0 targets DSH only (8–12 month review)|Data paper to _Data in Brief_ first (4–6 week review)|**Moderate — delays entire pipeline**|A.2.14|
|C-15|Philosophy|No engagement with Muʿtazilī position|300-word kalām contextualization added to Paper 5|**Moderate — philosophical vacuum**|A.2.15|
|C-16|Statistics|Eigenvector centrality reported without theoretical grounding|Removed from primary analysis or justified|**Moderate — no theological interpretation**|A.2.16|
|C-17|Corpus|Arbitrary 10-word distance threshold, unjustified|Sensitivity analysis at 5, 7, 10, 15 words|**Moderate — reviewer will ask**|A.2.17|
|C-18|LLM|Prompts not specified before pipeline run|Prompts written and pilot-tested on calibration set first|**Moderate — standard practice not followed**|A.2.18|
|C-19|LLM|JJK classification done by LLM|JJK classification done by researcher against Al-Qushayrī directly|**Moderate — LLM adds no value here**|A.2.19|
|C-20|Corpus|Refrain analysis treated as methodological exclusion|Refrain instances treated as case studies|**Moderate — underexplored finding**|A.2.20|
|C-21|Network|Hapax dyads treated as residual category|Hapax dyads as primary sub-analysis in Paper 5|**Moderate — 90% of pairs underanalyzed**|A.2.21|
|C-22|Network|Entropy computed but not mapped to a paper finding|Dyadic entropy as primary variable in Paper 4|**Moderate — insight buried**|A.2.22|
|C-23|Corpus|Riwāya scope not documented with dyad-impact check|Cross-checked; documented in dataset metadata|**Minor — reviewer objection prevented**|A.2.23|
|C-24|HITL|Annotation serialized (Phase 2 then Phase 3)|Annotation parallel with Phase 3; shared interface|**Minor — 2–3 month unnecessary delay**|A.2.24|
|C-25|Statistics|Bootstrap CIs computed for centrality; not for NPMI|Bootstrap CIs applied consistently to all metrics|**Addressed in C-11**|A.2.11|
|C-26|Papers|Logistic regression "theme-only model has no predictive power"|Removed (artifact of circular design)|**Addressed in C-01**|A.2.1|
|C-27|Network (v2.1)|No local topology analysis — only global centrality and communities|Network motif enumeration added (3-node and 4-node sub-graphs, degree-preserving null, motif–theme correlation in Paper 3)|**Serious — analytical depth capped at global metrics**|A.2.27|
|C-28|Philosophy (v2.1)|Paper 5 framed as refereeing essentialism vs. contextualism debate|Dynamic Essentialism proposed as new positive theoretical claim; Edge as locus of meaning; Section 10 fully rewritten|**Serious — "defense" framing produces a weaker paper than "proposal" framing**|A.2.28|
|C-29|Infrastructure (v2.1)|Tool list without pipeline architecture or reproducibility workflow|Full layer-by-layer reproducible research pipeline specified (Section 6); Airtable HITL interface; pinned dependencies; Zenodo release workflow; Gephi settings; full data flow diagram|**Serious — black-box pipeline not publishable at Q1 standard**|A.2.29|

---

## A.2 Detailed Critique and Rationale for Each Change

### A.2.1 — C-01: Logistic Regression Circular Argument (Critical)

**v1.0 design:** A logistic regression model predicting JJK pair-type label from verse features achieved 97.5% accuracy (vs. 51.5% majority-class baseline). This was presented as supporting essentialism: "JJK type is predictable primarily from the names chosen, not from the verse topic."

**The critique:** The model's features included "Name 1 is Jalāl" and "Name 2 is Jamāl" — but the JJK pair-type label is _definitionally_ constructed from these individual name classifications. The model is learning to reconstruct its own labels from their components. This is not a finding; it is algebraic identity. The 97.5% accuracy says nothing about whether divine attributes are essential — it says that Jalāl + Jamāl always produces the label "Jalāl+Jamāl," which is trivially true.

**What essentialism would actually require:** Showing that the _same dyad_ (same pair of names) produces the _same thematic signal_ regardless of verse context — i.e., that dyad identity predicts verse theme with above-chance accuracy. This is the reverse regression (theme ~ dyad identity) and is a genuinely non-circular test. It is also a much harder test to pass, and the v1.0 data (V_corr=0.21) suggests the answer would be "somewhat but not strongly."

**v2.0 decision:** Remove the logistic regression from the paper pipeline. If a predictive model is included in a future revision, it must predict verse theme from dyad identity (non-circular) — not JJK label from individual name classifications (circular). The unified theoretical argument in Paper 5 makes the essentialism/contextualism claim without the circular model.

---

### A.2.2 — C-02: Kamāl Split (Critical)

**v1.0 design:** The Kamāl category contained all names that are neither Jalāl nor Jamāl: Al-ʿAlīm, Al-Ḥakīm, Al-Khabīr, Al-Samīʿ, Al-Baṣīr, Al-Ḥayy, Al-Qayyūm, Al-Wāḥid, Al-Ḥaqq, Al-Ghanī, Al-Ḥamīd, and others — a heterogeneous category of 20+ names.

**The critique:** Al-Ghazālī in _Al-Maqṣad al-Asnā_ places Al-ʿAlīm (knowledge) and Al-Ḥayy (life) in fundamentally different attribute clusters. Al-ʿAlīm belongs to the epistemic attributes (ʿilm domain); Al-Ḥayy belongs to the ontological attributes (wujūd/ḥayāt domain). Collapsing both into Kamāl loses the discriminating power to test whether epistemic names cluster with each other independently of ontological names — which is a genuinely interesting theological and network question.

**v2.0 decision:** Split Kamāl into Kamāl-epistemic (Al-ʿAlīm, Al-Ḥakīm, Al-Khabīr, Al-Samīʿ, Al-Baṣīr) and Kamāl-ontological (Al-Ḥayy, Al-Qayyūm, Al-Wāḥid, Al-Ḥaqq, Al-Ghanī, Al-Ḥamīd). This creates a five-class taxonomy, increases categorical precision, and generates a new empirical question: do epistemic and ontological Kamāl names pair with each other, or do they pair preferentially with Jalāl and Jamāl names respectively? This is a publishable contribution to Sifāt classification literature.

---

### A.2.3 — C-03: Relationship Type Operationalization (Critical)

**v1.0 design:** Five relationship types (complementary / balancing / reinforcing / sequential / intensifying) applied by LLM heuristic. No published decision procedure. No inter-rater reliability test.

**The critique:** A corpus linguistics reviewer will require a published decision procedure and an IRR coefficient before accepting this taxonomy as an analytical variable. Without both, the relationship type labels are not reproducible and cannot be used as evidence in any paper.

**v2.0 decision:** Formal decision tree (see Section 5.5) written before LLM first-pass application. IRR test on 30-dyad calibration set; κ ≥ 0.65 required before scale application. Published in Paper 0 supplementary materials.

---

### A.2.4 — C-04: Stratified Null Model (Serious)

**v1.0 design:** Single corpus-wide permutation null model. Proves overall co-occurrence is non-random.

**The critique:** The Meccan/Medinan evolution finding (Jalāl+Jalāl doubles from 5.9% to 23.7%) is one of the programme's most theologically significant findings. The corpus-wide null model cannot test whether this differential is non-random — it only tests whether overall pairing frequency exceeds chance. To claim the period differential is significant, a period-stratified null model is required.

**v2.0 decision:** Two null models — Null Model A (corpus-wide, Paper 1) and Null Model B (period-stratified, Paper 3). The Meccan/Medinan evolution claim is backed only by Null Model B in Paper 3.

---

### A.2.5 — C-05: Directed vs. Undirected Network (Serious)

**v1.0 design:** Methodology claimed directed graph; Gephi edge table specified "Undirected." Contradiction. Centrality metrics therefore computed on the wrong graph type.

**The critique:** Directed and undirected betweenness centrality are computed differently. Using undirected centrality on what was claimed to be a directed network produces metrics that are not what the methodology says they are.

**v2.0 decision:** Network is undirected (co-occurrence, not causal/sequential). Canonical verse order (N1→N2) retained as edge attribute and analysed descriptively (which names tend to appear first in different JJK pair types) but does not drive topology. Decision documented and falsifiable. All centrality metrics recomputed on correctly specified undirected graph.

---

### A.2.6 — C-06: Louvain Consensus (Serious)

**v1.0 design:** Single Louvain run produced "11 communities." Resolution parameter not reported.

**The critique:** Louvain community detection at small N (50 nodes, 86 edges) is highly sensitive to random seed initialization and to the resolution parameter γ. A single run's output is not reproducible and may reflect initialization noise rather than true community structure. Resolution parameter γ determines whether you find 5 communities or 15 — reporting results without it makes the finding unreproducible.

**v2.0 decision:** 100-run Louvain ensemble. Consensus partition reported: nodes stable (same community in > 80% of runs) vs. boundary nodes (unstable). Resolution parameter γ=1.0 for primary analysis; sensitivity tests at γ=0.5 and γ=2.0 in supplementary materials. If consensus communities correspond to classical Sifāt attribute groupings, this is a strong finding. If they do not, this is also a finding.

---

### A.2.7 — C-07: CAMeL Tools Morphological Normalization (Serious)

**v1.0 design:** Python extraction pipeline matched divine names on surface-form Unicode strings.

**The critique:** Surface-form matching misses morphological variants (definite article variation, construct state, pronoun clitics) and cannot distinguish divine-name occurrences from homonyms at the morphological level. It produces false positives (the Egyptian official Al-ʿAzīz in Q12:30 was caught, but only by HITL review — not by the pipeline).

**v2.0 decision:** CAMeL Tools Arabic morphological analyzer integrated into the pipeline. Tokens normalized to base lemma form before matching. Syntactic position signal (nominal predicate vs. adjective) provided to HITL review queue. Reduces false positives before HITL and catches morphological variants that surface-form matching misses.

---

### A.2.8 — C-08: Paper Pipeline Restructuring (Serious)

**v1.0 design:** Paper 4 = OWL ontology. Papers 2 and 5 as separate papers making partially contradictory claims.

**The critique on Paper 4:** _Applied Network Science_ and _Semantic Web Journal_ require ontologies to be aligned to upper ontologies (DOLCE, BFO) and evaluated by formal consistency metrics. An OWL ontology of divine attributes without this alignment is not publishable in those venues as a primary paper. The ontology is useful as a background resource but not as Paper 4.

**The critique on Papers 2 and 5:** Paper 2 argued the dyad system is structurally patterned (supports essentialism); Paper 5 argued the same dyads show contextual modulation (supports contextualism). A reviewer at _Journal of Religion_ will ask why this is not one paper. The tension between the findings _is_ the argument — it should be made explicitly in a single paper, not split across two papers that appear to contradict each other.

**v2.0 decisions:** Paper 4 replaced with cross-corpus religious network comparison — same analytical framework, same journals, more impactful finding. Papers 2 and 5 merged into one paper that makes the unified claim: structurally patterned AND contextually deployed.

---

### A.2.9 — C-09: Stratified IRR Sampling (Serious)

**v1.0 design:** Random 10% of corpus (approximately 17–18 dyads) for IRR validation.

**The critique:** Random sampling under-represents the 52 CRITICAL and HIGH-priority rows, which are exactly where error is most consequential (they are the high-surprise, high-tension dyads that drive the case-study analysis in Papers 3 and 5). An IRR sample that misses most of the important rows gives false confidence in the validation.

**v2.0 decision:** Stratified sampling — 100% of CRITICAL and HIGH rows (52 dyads) + 20% random sample of STANDARD rows (25 dyads) = 77-dyad IRR set. This concentrates validation where it matters while remaining feasible.

---

### A.2.10 — C-10: Primary Classical Source Shift (Serious)

**v1.0 design:** Al-Ghazālī's _Al-Maqṣad al-Asnā_ used as primary JJK classification source.

**The critique:** Al-Ghazālī does not apply the Jalāl/Jamāl framework uniformly in _Al-Maqṣad al-Asnā_ — the framework is implicit and requires inference. Al-Qushayrī's _Sharḥ Asmā' Allāh al-Ḥusnā_ applies it most systematically. Using Al-Ghazālī as the primary operational source while citing Ibn ʿArabī and Al-Qushayrī for theoretical justification creates a source mismatch that Islamic Studies reviewers will identify.

**v2.0 decision:** Al-Qushayrī as primary operational source for JJK classification. Al-Ghazālī as secondary validator for name inclusion decisions. Disagreements between sources flagged as Disputed — a finding in their own right.

---

### A.2.11 — C-11: NPMI Confidence Intervals (Serious)

**v1.0 design:** NPMI reported for all 71 pairs without confidence intervals. Pairs compared on NPMI ranking without testing whether differences are statistically meaningful.

**The critique:** At n=1, 2, or 3, NPMI estimates have very wide confidence intervals that overlap substantially. Comparing NPMI rankings for low-frequency pairs produces false precision. The statement "Al-Wāḥid–Al-Qahhār has stronger bond strength than Al-ʿAzīz–Al-Ḥakīm" (NPMI 1.32 vs. 1.11) needs CI overlap testing before it can be claimed.

**v2.0 decision:** Bootstrap CIs on NPMI for all pairs (B=5000 resamples). NPMI comparisons in papers restricted to pairs where 95% CIs do not overlap. Pairs where CIs overlap reported as "comparable bond strength" without ranking claim.

---

### A.2.12 — C-12: Two-Level Thematic Taxonomy (Serious)

**v1.0 design:** Seven-category macro taxonomy applied to all dyads. Chi-square produced V_corr=0.21 (moderate effect).

**The critique:** The seven categories are internally heterogeneous — Tawḥīd ranges from ontological declarations to polemic to Asmaul Husna catalogues. This heterogeneity inflates variance within categories, reducing the measured association between JJK type and theme. The V_corr=0.21 is partly an artefact of category blurring, not entirely a reflection of the underlying dyad-theme relationship.

**v2.0 decision:** Two-level taxonomy (7 macro + 20 micro). Macro level used for overview (Paper 3, expected V_corr ≈ 0.21). Micro level used for case-study analysis (Papers 3 and 5, expected stronger V_corr). The differential between macro and micro effect sizes is itself a publishable finding.

---

### A.2.13 — C-13: Version Control (Serious)

**v1.0 design:** Dataset files named v1_0, v2_0 etc. manually. No Git repository.

**The critique:** A multi-year, multi-paper programme that shares one dataset across 6 papers and publishes it on Zenodo cannot be version-controlled by manual filename suffixes. When corrections are made (and they will be — homonym flags change, HITL decisions are revised, N changes from 177), there is no audit trail showing which version of the dataset each paper used.

**v2.0 decision:** Private GitHub repository from day one. Every dataset change is a commit with a descriptive message. Zenodo release uses Git tag. Each paper's supplementary materials record the Zenodo version DOI for the dataset version used.

---

### A.2.14 — C-14: Publication Sequence (Moderate)

**v1.0 design:** Paper 0 submitted to _Digital Scholarship in the Humanities_ (DSH) first. Review time 8–12 months.

**The critique:** If the dataset paper is in DSH review for a year, subsequent papers cannot cite a published dataset. They must cite "in preparation," which weakens their credibility and may delay acceptance.

**v2.0 decision:** Dataset paper submitted to _Data in Brief_ (Elsevier, 4–6 week review) first. DSH methodology paper submitted in parallel but is not the blocking first publication. _Data in Brief_ + Zenodo release together establish the dataset in the public domain quickly.

---

### A.2.15 — C-15: Kalām Contextualization (Moderate)

**v1.0 design:** Paper 5 engaged the essentialism/contextualism debate (Alston, Swinburne, Murata, Chittick) without addressing the parallel Ashʿarī/Muʿtazilī dispute in Islamic kalām.

**The critique:** Reviewers at _Sophia_ and _Journal of Religion_ cover both Western analytic philosophy of religion and Islamic theology. A paper that ignores the internal Islamic debate while engaging the Western one will be flagged as incomplete. The Muʿtazilī position is also theoretically important — it predicts a different network structure than the Ashʿarī position.

**v2.0 decision:** 300-word kalām contextualization section in Paper 5 situating the essentialism/contextualism debate within the Ashʿarī/Muʿtazilī Sifāt dispute, noting the structural homology, and applying the network structure finding as preliminary evidence.

---

### A.2.16 — C-16: Eigenvector Centrality (Moderate)

**v1.0 design:** Eigenvector centrality reported for all 50 nodes in the centrality metrics table.

**The critique:** Eigenvector centrality measures connection to well-connected nodes. In this network, there is no articulated theological interpretation of what it means for a divine name to be "connected to well-connected names." Degree centrality (how many partners → pairing versatility) and betweenness centrality (bridging role → theological mediation) have natural interpretations. Eigenvector centrality does not, and its inclusion without theoretical grounding invites the reviewer question "why this measure?"

**v2.0 decision:** Eigenvector centrality removed from primary analysis. Retained in supplementary data table for completeness. Not cited in any paper as primary evidence.

---

### A.2.17 — C-17: Distance Threshold Sensitivity (Moderate)

**v1.0 design:** Dyad defined as "two names within ten words of each other." Threshold not justified.

**The critique:** The choice of 10 words is arbitrary. A reviewer will ask why 10 rather than 5 or 15. If the core findings change substantially at different thresholds, the findings are not robust. If they are stable, that stability is itself evidence for the robustness of the dyad phenomenon.

**v2.0 decision:** Sensitivity analysis at 5, 7, 10, and 15 words. Core findings (top dyad pairs, JJK distribution, Meccan/Medinan shift) reported at each threshold. Stability across thresholds reported in Paper 0 supplementary materials. This turns an arbitrary methodological choice into a feature.

---

### A.2.18 — C-18: LLM Prompt Design Protocol (Moderate)

**v1.0 design:** LLM prompts described as "structured" but not specified before pipeline run. To be published with Paper 0.

**The critique:** LLM classification accuracy for theological concepts is highly sensitive to prompt phrasing. Running the pipeline without first testing prompts on a calibration set risks systematic prompt-induced errors propagating through the entire dataset.

**v2.0 decision:** Prompts written and pilot-tested on 20-dyad calibration set (known-correct labels) before scale application. Accuracy threshold ≥ 80% required. If < 80%, prompt revised and retested. All prompts published in Paper 0 supplementary materials verbatim.

---

### A.2.19 — C-19: JJK Classification by LLM (Moderate)

**v1.0 design:** JJK classification done by LLM (first pass) with HITL validation.

**The critique:** The JJK classification task covers 106 names × 1 label each = 106 decisions. This is a 3–5 hour task for a researcher working directly from Al-Qushayrī's classifications. LLM first-pass adds no value here because the ground truth is in a specific classical text that can be read directly. Any LLM errors require HITL correction anyway — skipping the LLM step for JJK classification saves time and eliminates a source of systematic bias.

**v2.0 decision:** JJK classification done by researcher directly against Al-Qushayrī. No LLM involvement in this task. LLM reserved for thematic tagging (where the ground truth is distributed across many tafsīr passages and LLM first-pass genuinely reduces researcher workload).

---

### A.2.20 — C-20: Structural Refrains as Case Studies (Moderate)

**v1.0 design:** Three structural refrains (Surah 26 Al-ʿAzīz–Al-Raḥīm n=9, Surah 2 Al-Tawwāb–Al-Raḥīm n=4, Surah 3 Al-ʿAzīz–Al-Ḥakīm n=4) identified and excluded from predictive model.

**The critique:** The Surah 26 refrain — nine repetitions of Al-ʿAzīz–Al-Raḥīm across seven prophet narratives — is itself a theologically significant finding. Why does the longest narrative surah use this specific balancing pair as its structural refrain? Al-Rāzī comments on this. Treating it as methodological noise misses a ready-made case study for Papers 3 and 5.

**v2.0 decision:** Each refrain is treated as a mini-case-study in Paper 3 — why this pair, why this surah, what the refrain structure adds to the theological argument of the surah. Refrain instances remain excluded from the dyad-theme chi-square (to avoid inflating frequencies) but are analysed separately as literary-theological evidence.

---

### A.2.21 — C-21: Hapax Dyad Sub-Analysis (Moderate)

**v1.0 design:** 64/71 pairs (90%) are hapax. Treated as residual category in frequency tables.

**The critique:** Hapax dyads — pairs occurring exactly once in the entire Qur'an — are potentially the most theologically interesting set. They are the pairs where the theological work is maximally context-specific, where no formulaic repetition is possible. Their verse types, JJK combinations, and positions deserve dedicated analysis.

**v2.0 decision:** Hapax dyads treated as a primary sub-analysis in Paper 5. Research questions: Do hapax dyads concentrate in specific verse types? Do they show higher semantic surprise scores than canonical dyads? What JJK combinations are only found in hapax pairs? This analysis can produce novel findings about the boundaries of the dyad system — which combinations are systematically avoided (appear in neither canonical nor hapax form) and which are used only once.

---

### A.2.22 — C-22: Dyadic Entropy as Primary Variable (Moderate)

**v1.0 design:** Dyadic entropy computed in Statistical_Analysis_Upgrade Sheet 5 but never clearly mapped to a paper finding or used as primary evidence.

**The critique:** Al-Ḥaqq (the Truth) is the most "promiscuous" name in the dataset — 9 unique partners, entropy 2.97 bits — suggesting it functions as a semantic bridge across multiple name-clusters. This is theologically significant: Al-Ḥaqq's versatility as a pairing partner may reflect its classical role as a name that grounds and validates other divine attributes. Burying this insight in a supplementary sheet loses it.

**v2.0 decision:** Dyadic entropy is a primary variable in Paper 4 (cross-corpus comparison) — used to identify "semantic bridge" names (high entropy) vs. "captured" names (low entropy, dominated by one pairing) in both the Qur'anic network and the comparison corpus. This gives entropy a clear analytical role and theoretical interpretation.

---

### A.2.23 — C-23: Riwāya Scope Documentation (Minor)

**v1.0 design:** Tanzil corpus used; riwāya variants outside scope, mentioned in passing.

**The critique:** An Islamic Studies reviewer may ask whether the findings are specific to the Ḥafṣ riwāya. Without documentation that other riwāyāt do not produce different dyads, this is an open vulnerability.

**v2.0 decision:** Cross-check documented in dataset metadata: the three most theologically consequential name-boundary cases in other riwāyāt have been verified to not affect any dyad in the current dataset. Statement included in Paper 0 methodology section.

---

### A.2.24 — C-24: Parallel Annotation and Network Construction (Minor)

**v1.0 design:** Phase 2 (dataset construction) completed before Phase 3 (network analysis) begins.

**The critique:** The Islamic Studies consultant's stratified annotation (52 CRITICAL/HIGH rows) runs concurrently with network construction. Serializing adds 2–3 months unnecessarily.

**v2.0 decision:** Shared annotation interface (Airtable or Notion) allows consultant to annotate while principal researcher handles network construction. Phases 2 and 3 overlap from month 5 onwards.

---

### A.2.27 — C-27: Network Motif Analysis Absent (Serious — v2.1 addition)

**v1.0 and v2.0 design:** Network analysis limited to global topology — centrality, communities. No local topology analysis.

**The critique:** Global metrics answer "who" and "where" (which names are hubs, which cluster together). They do not answer "how" — the recurring compositional structures that constitute the Qur'an's theological grammar above the dyadic level. With N=50 nodes and 86 edges, motif enumeration is computationally trivial (seconds in NetworkX) but analytically massive: it is the highest ROI modification available to the programme at the network analysis stage. Absence of motif analysis leaves the programme's network contribution at the level of descriptive topology rather than structural theory.

**v2.1 decision:** Full motif analysis added as Section 5.7 and as a primary analytical layer in Paper 1. Procedure: enumerate all 3-node and 4-node sub-graphs using NetworkX; compute significance against a degree-sequence-preserving null model (10,000 permutations); classify significant motifs by JJK polarity post-hoc; extend to motif–theme correlation in Paper 3. Critical procedural constraint: motif analysis runs after the stable graph is constructed and consensus communities are established — not before. Theological naming of motifs is interpretive and post-hoc, not pre-specified. Framing in publications: "statistically over-represented structural tendencies," not "compositional algorithms."

---

### A.2.28 — C-28: Paper 5 Framing as Debate Referee (Serious — v2.1 addition)

**v2.0 design:** Paper 5 framed as an engagement with the essentialism vs. contextualism debate in philosophy of religion — presenting both sides and arguing for a position "between" them.

**The critique:** A mature scholarly paper does not referee an existing debate — it proposes a new position. The "between" framing (essentialist at the attribute level, contextualist at the deployment level) is a compromise rather than a theory. It tells the reader that both sides are partially right, which is less interesting and less publishable than proposing a framework that resolves the debate by reframing the unit of analysis. Furthermore, the "between" framing does not make use of the programme's most distinctive contribution — the network's Edge structure — as a theoretical resource. The Edge is the dyadic relation; locating meaning in the Edge rather than in the Node is a structural claim that goes beyond the existing debate's terms.

**v2.1 decision:** Paper 5 reframed around Dynamic Essentialism as a positive theoretical claim. The existing debate (Alston, Swinburne, Murata, Chittick) becomes the literature review. The Ashʿarī/Muʿtazilī/Ibn ʿArabī kalām mapping becomes the contextual section. Dynamic Essentialism — Nodes are essential and stable; Edges are dynamic and contextually calibrated; the Edge is the primary locus of meaning — is the paper's contribution. High-surprise dyads are the evidence base: they are "relational exceptions" whose surprise is located entirely in the pairing relation, not in either name alone. Section 4.5 and Section 10 rewritten accordingly.

---

### A.2.29 — C-29: Tool List Without Pipeline Architecture (Serious — v2.1 addition)

**v2.0 design:** Section 6 listed tools in tables without specifying the pipeline architecture — how data moves between tools, who has access to what, how versions are managed, and what the audit trail looks like.

**The critique:** The biggest failure mode in Digital Humanities is the "black box" effect: a researcher produces a network graph, but the path from raw XML to published image is undocumented and irreproducible. A tool list is not a pipeline. Without specifying: (a) which tool is the source of truth (not Airtable — GitHub), (b) how the HITL consultant interface is isolated from the statistical columns, (c) how dependency versions are pinned, (d) what the Zenodo release workflow is, and (e) exactly which Gephi settings produce the publication figure — the programme cannot claim reproducibility. A paper with a Zenodo DOI for the dataset and a GitHub link for the code is treated as hard science. A paper that says "data available upon request" is treated as soft humanities.

**v2.1 decision:** Section 6 fully replaced with a layer-by-layer reproducible research pipeline specification. Eight layers: (1) Primary Data Sources; (2) HITL Interface (Airtable with Consultant View and snapshot capability); (3) Version Control (GitHub private repository with specified folder structure, CSV as source of truth, Zenodo releases per paper); (4) Computational Engine (Python 3.11+, CAMeL Tools, Pandas, NetworkX, SciPy, Statsmodels — with pinned dependencies and the anti-stack explicitly named); (5) Visualization (Gephi with ForceAtlas2 and specified node/edge settings; Plotly/Seaborn for statistical figures); (6) LLM Tools (Claude Sonnet first-pass only, prompts versioned in /prompts/); (7) Scholarly Sources; (8) Full pipeline data-flow diagram. Anti-stack: no Neo4j (overkill for 50 nodes), no Excel (no version control), no AI-only extraction (no HITL = hallucinated dyads, rejected in peer review).

---

## A.3 What Did NOT Change from v1.0 (Retained in v2.0 and v2.1)

For completeness — these decisions are retained without modification across all versions:

- **Core dataset:** 177 dyads, 71 unique pairs, 50 active nodes — validated and correct.
- **Primary Qur'anic corpus:** Tanzil XML (Ḥafṣ ʿan ʿĀṣim) — standard and defensible.
- **Dyad definition:** Two divine names within the same verse, within ten words — retained with added sensitivity analysis.
- **Meccan/Medinan key finding:** Jalāl+Jalāl doubles (+17.8pp) in Medinan period — finding retained; statistical support strengthened with Null Model B.
- **Structural refrain identification:** Surahs 2, 3, and 26 — retained and promoted to case studies.
- **NPMI as co-occurrence metric** — retained with added bootstrap CIs.
- **Semantic surprise index** — retained as primary HITL prioritization tool and as key evidence base for Dynamic Essentialism (Paper 5).
- **Polarity Tension Index** — retained as continuous measure of Jalāl–Jamāl tension.
- **Al-Rāzī as primary tafsīr interlocutor at the pair level** — retained.
- **Five-type relationship taxonomy** — retained with added decision tree and IRR standard.
- **Scope boundaries** — retained unchanged. This programme does not make theological reform claims, iʿjāz claims, or extend to Hadith.
- **v2.1 adds to, but does not change, the above.** Motif analysis is additive (extends global to local topology). Dynamic Essentialism is additive (gives Paper 5 a positive claim rather than a weaker compromise). The reproducible pipeline specification is additive (turns tool lists into an auditable architecture). No existing data, finding, or paper target is removed by v2.1.

---

_End of Dossier v2.1_

_Document maintained by the Principal Researcher. All changes to be committed to the project Git repository with descriptive commit messages. Next scheduled review: upon submission of Paper 1._

_وَهُوَ بِكُلِّ شَيْءٍ عَلِيمٌ_

_And He is, of all things, Knowing._

_— Qur'an 2:29_

