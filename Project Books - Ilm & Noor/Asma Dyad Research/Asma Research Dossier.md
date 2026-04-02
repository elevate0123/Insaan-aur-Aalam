

# بِسْمِ اللَّهِ الرَّحْمَٰنِ الرَّحِيمِ

---

# COMPUTATIONAL SEMANTIC NETWORK OF PAIRED DIVINE NAMES IN THE QUR'AN

## _Asmā' al-Ḥusnā Dyad Analysis — Project Dossier v2.0_

> **Version:** 2.0 | **Status:** Active — Single Source of Truth  
> **Replaces:** Dossier v1.0 (all prior documents superseded)  
> **Audience:** Academic Collaborators · Funding Bodies · Islamic Studies Scholars · Computational Researchers · Network Scientists · Philosophers of Religion · Digital Humanities Community  
> **Maintained by:** Principal Researcher

---

## HOW TO USE THIS DOCUMENT

This dossier is the single source of truth for the entire research programme. It is structured in two parts:

**Part I — The Programme** contains everything needed to understand, execute, and publish this research. It is organized by audience: each major section is self-contained enough for a collaborator joining at any stage to orient themselves without reading everything.

**Part II — Appendix** contains the complete v1.0 → v2.0 critique, a change log with rationale for every decision revision, and the full IRR and HITL protocols.

**Quick navigation by role:**

- _Islamic Studies scholar / tafsīr consultant_ → Sections 4, 6.3, 7, 10
- _Data engineer / Python developer_ → Sections 5, 6.1, 6.2, 9
- _Network scientist_ → Sections 5.4–5.6, 6.4, 8 (Paper 4 revised)
- _Philosopher of religion_ → Sections 4.5, 8 (Paper 5)
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

## 1.4 What v2.0 Changes

Version 2.0 incorporates ten structural changes to the research design — driven by a systematic critique of the v1.0 programme. The core dataset remains valid. What changes is: the taxonomic framework (Kamāl split into two sub-classes), the statistical reporting standard (NPMI CIs, stratified null model), the network model (directed/undirected decision, Louvain consensus), the paper pipeline (Papers 2+5 merged; Paper 4 replaced), and the HITL protocol (stratified sampling). Full rationale is in Appendix A.

## 1.5 Programme Outputs

|Output|Timeline|Status|
|---|---|---|
|Master dataset (Zenodo, CC-BY 4.0)|Month 4|In preparation|
|Paper 0: Methodology + HITL pipeline|Month 10|Drafting|
|Paper 1: Corpus frequency + network structure|Month 12|In preparation|
|Paper 2: Jalāl–Jamāl axis + semantic polarity|Month 16|Planned|
|Paper 3: Dyad–theme contextual correlation|Month 20|Planned|
|Paper 4 (revised): Cross-corpus religious network comparison|Month 24|Planned|
|Paper 5 (merged with former P2/P5): Structured pattern + contextual deployment|Month 26|Planned|
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

## 4.5 Philosophy of Religion — Divine Attribute Theory

**Core principle:** The intertextual analysis (Paper 5, merged) directly engages the philosophical question of whether divine attributes are essential and immutable or contextually modulated.

**The positions:**

- **Essentialism** (Alston, Swinburne, Plantinga): each divine name names an intrinsic, unchanging property of the divine nature. Context cannot modulate the attribute itself.
- **Contextual theology** (Murata, Chittick): the same name, used in different contexts, expresses different facets or intensities of the underlying reality.
- **The Muʿtazilī position** (Ibn al-Jabbār, Zamakhsharī): divine names are different linguistic expressions of the same undivided reality — ontological distinctions between attributes are denied. This is functionally closer to contextualism than to Ashʿarī essentialism.

**The v2.0 theoretical contribution:** The programme's unified finding — dyad system is structurally patterned _and_ contextually deployed — maps onto a position that is neither pure essentialism nor pure contextualism. The structural patterning (stable JJK combinations, stable network topology across Meccan and Medinan periods) supports the essentialist claim that names carry stable semantic properties. The contextual deployment (same dyad appears across different verse themes; high-surprise dyads mark rhetorical exceptions) supports the contextualist claim that selection among available names is contextually sensitive. The Qur'an's dyad system is, on this reading, _essentialist at the attribute level and contextualist at the deployment level_ — a position not articulated in the existing philosophical literature and publishable as an original contribution to _Sophia_ or _Journal of Religion_.

**Critical addition (v2.0):** Paper 5 must now include a 300-word kalām contextualization section situating the essentialism/contextualism debate within the Ashʿarī vs. Muʿtazilī Sifāt dispute. This is not optional — reviewers at _Sophia_ and _Journal of Religion_ will expect it, and the Muʿtazilī position is theoretically important because it predicts a different network structure than the Ashʿarī position (if names are merely different expressions of one undivided reality, the co-occurrence network should show high clustering and low modularity; if names are genuinely distinct properties, the network should show identifiable community structure).

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

## 5.7 Step 7 — Statistical Validation (Stratified Null Model)

**v2.0 critical change from v1.0:** The v1.0 null model used corpus-wide permutation — shuffling name assignments across all verses, preserving only the number of names per verse. This proves overall co-occurrence is non-random but does not prove that the Meccan/Medinan differential is non-random, which is where the more interesting theological argument lives.

**v2.0 approach:** Two null models:

**Null Model A (corpus-wide):** Permute name assignments across all verses 10,000 times, preserving number of names per verse. Produces p-values for overall dyad significance (Paper 1).

**Null Model B (period-stratified):** Permute name assignments within Meccan verses only, then within Medinan verses only — preserving period structure. Produces p-values for Meccan-specific and Medinan-specific pair frequencies, and for the period-differential finding (Jalāl+Jalāl doubling). This is the null model for the Meccan/Medinan evolution claim (Paper 3).

**Effect size reporting:** All chi-square tests report bias-corrected Cramér's V (V_corr, Bergsma & Wicher 2013) alongside χ² and p-value. Effect size conventions: Strong > 0.35, Moderate 0.20–0.35, Small < 0.20. Claims about "strong" association require V_corr > 0.35.

**Sensitivity analysis on dyad definition:** Run full extraction at word-distance thresholds of 5, 7, 10, and 15 words. Report which key findings (top dyad pairs, JJK distribution, Meccan/Medinan shift) are stable across thresholds. Publish sensitivity table in Paper 0 supplementary materials.

## 5.8 Step 8 — LLM-Assisted Tagging (HITL Pipeline v2.0)

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

## 5.9 Step 9 — Tafsīr-Grounded Interpretation

Computational findings are interpreted through classical exegetical tradition. For each significant pattern, the relevant tafsīr passages are consulted: did classical scholars notice this pattern? How did they explain it? Does the computational finding confirm, extend, or challenge the classical interpretation?

Al-Rāzī's _Mafātīḥ al-Ghayb_ is the primary classical interlocutor at the pair level — he is uniquely systematic in justifying specific name pairs at specific verse closings. Al-Ṭabarī provides early linguistic grounding. Ibn Kathīr provides standard Sunni exegetical validation. Al-Qurṭubī provides legal and contextual thematic tagging validation.

This step is not decorative. It is the scholarly warrant for the theological claims. Without it, the paper is a computer science paper about a text it does not understand. With it, it is a contribution to Islamic scholarship that happens to use computational tools.

---

# 6. Tools, Software, and Resources

## 6.1 Primary Data Sources

|Resource|Description|Access|
|---|---|---|
|Tanzil.net XML Corpus (v2.1.0)|Complete Qur'an, Unicode Arabic XML, Meccan/Medinan tags, verse numbering|Free download — tanzil.net|
|Al-Maktaba al-Shāmila|Complete classical tafsīr in Arabic — Al-Ṭabarī, Ibn Kathīr, Al-Qurṭubī, Al-Rāzī|Free — shamela.ws|
|OpenITI Corpus|Machine-readable classical Arabic texts including tafsīr|Free — openiti.org|
|Qur'anic Arabic Corpus (Leeds)|Morphologically annotated Qur'an — supplementary morphological reference|Free — corpus.quran.com|
|Al-Qushayrī _Sharḥ Asmā'_|Primary JJK classification source|Print edition (Dār al-Kutub) / Shamela|

## 6.2 Computational Tools

|Tool|Purpose|Notes|
|---|---|---|
|Python 3.10+|Core pipeline language|Libraries: pandas, numpy, scipy, lxml, matplotlib, seaborn|
|CAMeL Tools (NYUAD)|Arabic morphological analysis and lemmatization|v2.0 addition; pip install camel-tools|
|NetworkX|Graph construction, centrality, null model permutation|Standard|
|Gephi 0.10|Network visualization and Louvain community detection|Free, cross-platform|
|SciPy stats|Chi-square, Cramér's V, bootstrap resampling|Standard|
|Protégé + OWL|Divine attribute ontology (background resource, not Paper 4)|Free|
|Voyant Tools / AntConc|Concordance and collocation analysis for Paper 5|Free|
|Git + GitHub (private)|Version control for dataset — mandatory in v2.0|Free|
|Zenodo|Open dataset publication with versioned DOIs|Free|
|Zotero|Reference management across 100+ sources|Free|
|Overleaf / LaTeX|Paper typesetting|Preferred by most target journals|

## 6.3 AI and LLM Tools (HITL Pipeline)

|Tool|Role|Constraint|
|---|---|---|
|Claude Sonnet (Anthropic)|First-pass theme tagging; relationship type heuristic|First-pass only; all output HITL-validated|
|GPT-4 (optional)|Cross-validation of theme tags on 10% sample|Not primary; shared bias risk acknowledged|
|Python prompt templates|Versioned, stored in repository, published with Paper 0|Mandatory for reproducibility|

**What LLM does NOT do in v2.0:** JJK classification (done by researcher against Al-Qushayrī directly), homonym resolution (done by researcher against tafsīr), HITL reviewer decisions (done by researcher and Islamic Studies consultant).

## 6.4 Key Scholarly Sources

### Classical Islamic Sources

|Source|Author|Direct relevance|
|---|---|---|
|_Sharḥ Asmā' Allāh al-Ḥusnā_|Al-Qushayrī (d. 1072)|**Primary JJK classification source** (v2.0)|
|_Al-Maqṣad al-Asnā_|Al-Ghazālī (d. 1111)|Secondary name inclusion validator; individual name theology|
|_Mafātīḥ al-Ghayb_|Fakhr al-Dīn Al-Rāzī (d. 1210)|**Primary tafsīr interlocutor** — systematic pairing justifications|
|_Jāmiʿ al-Bayān_|Al-Ṭabarī (d. 923)|Early tafsīr; linguistic analysis|
|_Tafsīr al-Qur'ān al-ʿAẓīm_|Ibn Kathīr (d. 1373)|Standard Sunni validation source|
|_Al-Jāmiʿ li-Aḥkām al-Qur'ān_|Al-Qurṭubī (d. 1273)|Legal/contextual tagging validation|
|_Al-Futūḥāt al-Makkiyya_|Ibn ʿArabī (d. 1240)|Kamāl-ontological category; relational attribute ontology|
|_Badāʾiʿ al-Fawāʾid_|Ibn al-Qayyim (d. 1350)|Classical pairing logic|

### Modern and Bridge Scholarship

|Source|Author|Relevance|
|---|---|---|
|_The Tao of Islam_|Sachiko Murata (1992)|Best Western-academic Jalāl/Jamāl framework|
|_The Self-Disclosure of God_|William C. Chittick (1998)|Ibn ʿArabī's Names doctrine in English|
|_The Qur'an and Its Exegesis_|Helmut Gätje (1976)|Western framework for tafsīr methodology|
|_The Verbal Idioms of the Qur'an_|Mustansir Mir (1989)|Linguistic patterning in Qur'anic language|
|_Scripture, Poetry and the Making..._|Angelika Neuwirth (2019)|Verse-final rhetorical weight; discourse structure|
|_The Rhetoric of the Quran_|Michel Cuypers (2015)|Compositional and directional analysis|
|_Corpus, Method and Case Study_|Dukes (2011)|Computational Qur'anic studies baseline|

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

## Paper 1 — Corpus Frequency and Network Structure

|Element|Detail|
|---|---|
|**Working title**|Divine Name Dyads in the Qur'an: Frequency, NPMI Bonding Strength, and Semantic Network Architecture|
|**Core contribution**|Full frequency and NPMI analysis (with bootstrap CIs); weighted undirected co-occurrence network; betweenness and degree centrality for Stable/Moderate nodes only; consensus Louvain communities (100-run ensemble); stratified null model significance; Meccan vs. Medinan network comparison (Spearman ρ on degree hierarchy)|
|**Key finding**|Divine name pairings are statistically non-random and form an identifiable semantic topology; the degree hierarchy is stable across revelation periods (Spearman ρ=0.84) even as JJK composition shifts|
|**Target journal**|_Journal of Quranic Studies_ (Edinburgh/SOAS, Scopus Q1–Q2)|
|**Critical warning for reviewers**|All centrality claims are restricted to Stable and Moderate nodes (9/50 in v1.0); Unstable nodes explicitly flagged. All chi-square results report V_corr. NPMI comparisons restricted to pairs where 95% bootstrap CIs do not overlap|

## Paper 2 — Jalāl–Jamāl Axis and Semantic Polarity

|Element|Detail|
|---|---|
|**Working title**|The Jalāl–Jamāl–Kamāl Axis: Semantic Polarity in Qur'anic Divine Name Pairings|
|**Core contribution**|Tests revised five-class JJK taxonomy against full corpus; applies conceptual blending theory (Fauconnier & Turner) to balancing dyads; documents classical disagreements on individual name classification; shows Jalāl+Kamāl-epistemic as dominant pairing type and its theological interpretation|
|**Key finding**|The Qur'an structurally performs, at the textual level, the Jalāl–Jamāl balance that classical scholars argued for propositionally — with refinements visible only at the Kamāl-epistemic vs. Kamāl-ontological level of the taxonomy|
|**Target journal**|_Journal of Quranic Studies_; _Islam and Christian–Muslim Relations_; _Religions_ (MDPI, Scopus Q1)|
|**Classical interlocutors**|Al-Qushayrī (primary), Al-Ghazālī (secondary), Ibn ʿArabī (Kamāl category)|

## Paper 3 — Contextual Correlation

|Element|Detail|
|---|---|
|**Working title**|Divine Name Dyads as Contextual Signals: Dyad–Theme Correlation in the Qur'anic Corpus|
|**Core contribution**|Statistical correlation (χ², V_corr) between dyad types and verse themes at both macro (7) and micro (20) granularity levels; semantic surprise index identifying 32 theologically marked dyads; period-stratified null model for Meccan/Medinan differential; three structural refrain case studies|
|**Key finding**|Dyad–theme correlation is moderate at macro granularity (V_corr ≈ 0.21) and significantly stronger at micro granularity — the granularity-sensitivity differential is a finding about the interpretive grain of the dyad system. High-surprise dyads mark exceptional rhetorical moments documented in Al-Rāzī's commentary|
|**Target journal**|_Arabica_ (Brill, Scopus Q1); _Journal of Arabic and Islamic Studies_; _Al-Qantara_ (CSIC)|

## Paper 4 (Revised) — Cross-Corpus Religious Network Comparison

|Element|Detail|
|---|---|
|**Working title**|Comparing Divine Name Networks Across Scriptural Traditions: A Graph-Theoretic Framework|
|**Core contribution**|Graph-theoretic comparison of the Qur'anic divine name co-occurrence network against: (a) the divine name network derived from the Hebrew Bible (Elohim, YHWH, El Shaddai, Adonai, and their co-occurrence contexts); (b) divine epithet co-occurrence in the Rigveda (where available through digital corpus). Comparison metrics: network density, modularity, average path length, hub concentration, inter-community edge ratio|
|**Rationale for replacement of v1.0 Paper 4**|The v1.0 OWL ontology paper is not publishable in _Applied Network Science_ or _Semantic Web Journal_ without alignment to an upper ontology and formal consistency checks. A cross-corpus comparison paper uses the same analytical framework, targets the same journals, and produces a substantially more impactful contribution — it establishes the Qur'anic divine name network as a data point in a comparative religion network science|
|**Target journal**|_Applied Network Science_ (Springer, Scopus Q1); _Religions_ (MDPI); _Journal of the American Oriental Society_|
|**Feasibility note**|Hebrew Bible divine name co-occurrence can be derived from the SEFARIA digital corpus. Rigveda availability depends on digital humanities partnerships — if unavailable, paper proceeds as Qur'an–Hebrew Bible comparison only|

## Paper 5 (Merged) — Structural Pattern and Contextual Deployment

|Element|Detail|
|---|---|
|**Working title**|Same Dyad, Different World: Structural Regularity and Contextual Deployment in Qur'anic Divine Name Pairings|
|**Core contribution**|Tracks high-frequency canonical dyads (n≥5, surahs≥3, themes≥2) across all occurrences; tests whether verse context modulates semantic weight; engages divine attribute essentialism vs. contextualism debate; includes 300-word kalām contextualization (Ashʿarī vs. Muʿtazilī Sifāt dispute); presents the unified theoretical claim: dyad system is essentialist at the attribute level and contextualist at the deployment level|
|**Rationale for merger of v1.0 Papers 2 and 5**|Former Paper 2 (structural pattern) and Paper 5 (contextual modulation) addressed claims in tension with each other. Merging them into a single paper that holds both findings in explicit relation produces a stronger philosophical contribution than either paper alone — the tension _is_ the argument|
|**Target journal**|_Sophia_ (Springer, Scopus Q1); _Journal of Religion_ (Chicago); _Philosophy East and West_|
|**Critical addition**|Kalām contextualization section: the Muʿtazilī position predicts a different network structure than the Ashʿarī position (low modularity vs. high modularity) — the observed community structure (11 communities in v1.0, subject to resolution-parameter sensitivity) can be read as evidence in this debate|

---

# 9. Section for Network Scientists and Computational Researchers

_This section addresses the specific methodological and technical questions that network science and computational linguistics reviewers will raise._

## 9.1 Why This Network Is Interesting to Network Scientists

The divine name co-occurrence network has three properties that make it atypical and analytically interesting:

1. **Extreme hub dominance with small N:** Al-ʿAzīz has weighted degree 71 in a network of 50 nodes. This is an unusually concentrated hub structure for a 50-node network and raises the question of whether it is scale-free (Barabási-Albert growth model) or reflects a designed theological hierarchy.
    
2. **Very high hapax rate (90%):** 64/71 unique pairs occur exactly once. This is not noise — it reflects the finite Qur'anic corpus and the theological diversity of contextual divine-name deployment. Network metrics on hapax edges are unreliable; the programme explicitly separates canonical (n≥5) from hapax edge analysis.
    
3. **Period-structured temporal evolution:** The corpus has a known approximate temporal ordering (Meccan before Medinan revelation). This allows the network to be split into two "time periods" and compared — a form of temporal network analysis rarely applied to religious texts.
    

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

## 10.1 The Central Philosophical Claim

This programme produces empirical data relevant to a debate that has proceeded entirely in the mode of analytical argument: whether divine attributes are essential and immutable (essentialism) or contextually modulated (contextualism). The data cannot resolve the metaphysical question — whether divine attributes are _really_ immutable — but it can address the textual and theological question of how the Qur'an _deploys_ divine names and whether that deployment pattern is consistent with one position more than the other.

The v2.0 unified theoretical claim is: **the Qur'an's dyad system exhibits both structural regularity and contextual variation, which maps onto a position that is essentialist at the attribute level (names carry stable properties that govern their co-occurrence patterns) and contextualist at the deployment level (which specific names are selected for any given verse context is sensitive to that context).** This is not a contradiction — it is a distinction between the ontology of divine attributes and the epistemology of their textual presentation.

## 10.2 The Kalām Dimension (Required for Paper 5)

The essentialism/contextualism debate in Western analytic philosophy of religion (Alston 1989, Swinburne 1993) runs parallel to the Ashʿarī/Muʿtazilī dispute in Islamic kalām:

- **Ashʿarī position:** Divine attributes are real, distinct, and ontologically subsistent in the divine essence. Al-Bāqillānī, Al-Juwaynī, Al-Ghazālī. This is structurally analogous to essentialism.
- **Muʿtazilī position:** Divine attributes are not ontologically distinct from the divine essence — names are different linguistic expressions of one undivided reality. Al-Naẓẓām, Abū ʿAlī al-Jubbāʾī. This is structurally closer to contextualism.

**The empirical relevance:** If the Ashʿarī position is correct — that Al-Raḥīm and Al-ʿAzīz are genuinely distinct attributes — then we would expect the co-occurrence network to show high modularity (distinct attribute clusters with relatively few inter-cluster edges). If the Muʿtazilī position is correct — that all names express the same undivided reality — then we would expect low modularity, high integration, and no stable community structure. The observed community structure (subject to Louvain resolution-parameter sensitivity, addressed in Paper 4) can be read as preliminary evidence in this debate. Paper 5 will present this argument carefully, with appropriate epistemic hedging.

## 10.3 Ibn ʿArabī's Position and the Kamāl-Ontological Sub-Category

Ibn ʿArabī's _Al-Futūḥāt al-Makkiyya_ presents a third position that is neither Ashʿarī nor Muʿtazilī: divine names are real and distinct, but they are relational properties of divine self-disclosure (tajallī) rather than intrinsic properties of the divine essence. On this reading, names like Al-Ḥayy (the Living) and Al-Qayyūm (the Self-Subsisting) are not attributes of God-in-Himself but of God-as-related-to-creation. This is what the v2.0 taxonomy captures in the Kamāl-ontological sub-category — names that name the preconditions for divine action in relation to the created order, rather than God's internal epistemic operations.

The co-occurrence of Kamāl-ontological names with Kamāl-epistemic names (e.g., Al-Ḥayy–Al-Qayyūm, Al-ʿAlīm–Al-Ḥakīm) or the relative rarity of such cross-sub-category pairings would be evidence about which of these frameworks the Qur'anic text itself supports structurally.

---

# 11. Timeline and Phases

The programme has no artificial deadline. Quality of the dataset determines quality of every paper. Phase 2 (dataset construction and validation) is the longest and most critical phase.

## 11.1 Phase Overview

|Phase|Duration|Key deliverables|Dependencies|
|---|---|---|---|
|**Phase 1 — Setup**|Months 1–2|Tanzil XML downloaded and verified; Python environment with CAMeL Tools configured; Al-Qushayrī classification table complete; GitHub repository initialized; tafsīr PDFs acquired|None|
|**Phase 2 — Dataset Construction**|Months 2–7|CAMeL Tools extraction pipeline validated; JJK classifications complete (researcher vs. Al-Qushayrī directly); two-level thematic tagging with HITL; stratified IRR with Islamic Studies consultant (52 CRITICAL/HIGH + 25 STANDARD); IRR κ ≥ 0.65 confirmed; sensitivity analysis at 4 distance thresholds; dataset published on Zenodo|Phase 1 complete|
|**Phase 3 — Network Analysis**|Months 6–8 (parallel with late Phase 2)|Undirected weighted graph constructed; bootstrap CIs on centrality; 100-run Louvain consensus; two null model runs; dyadic entropy computed; Gephi visualization|Dataset v1.0 locked on Zenodo|
|**Phase 4 — Paper 0 and Data Paper**|Months 8–11|_Data in Brief_ dataset paper submitted (fast track); _DSH_ methodology paper drafted; all code published on GitHub|Phase 2 complete|
|**Phase 5 — Papers 1 and 2**|Months 11–16|Paper 1 (network structure) submitted; Paper 2 (JJK axis) submitted; responding to reviewer comments|Phase 3 complete|
|**Phase 6 — Papers 3 and 4**|Months 16–22|Paper 3 (contextual correlation) submitted; Paper 4 (cross-corpus comparison, requires Hebrew Bible network preparation) submitted|Papers 1–2 accepted or in revision|
|**Phase 7 — Paper 5**|Months 22–26|Merged Paper 5 (structural + contextual, philosophy) submitted|Papers 2–3 accepted or in revision|
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

## A.3 What Did NOT Change from v1.0

For completeness — these v1.0 decisions are retained in v2.0 without modification:

- **Core dataset:** 177 dyads, 71 unique pairs, 50 active nodes — validated and correct.
- **Primary Qur'anic corpus:** Tanzil XML (Ḥafṣ ʿan ʿĀṣim) — standard and defensible.
- **Dyad definition:** Two divine names within the same verse, within ten words — retained with added sensitivity analysis.
- **Meccan/Medinan key finding:** Jalāl+Jalāl doubles (+17.8pp) in Medinan period — finding retained; statistical support strengthened with Null Model B.
- **Structural refrain identification:** Surahs 2, 3, and 26 — retained and promoted to case studies.
- **NPMI as co-occurrence metric** — retained with added CIs.
- **Semantic surprise index** — retained as primary HITL prioritization tool.
- **Polarity Tension Index** — retained as continuous measure of Jalāl–Jamāl tension.
- **Al-Rāzī as primary tafsīr interlocutor at the pair level** — retained.
- **Five-type relationship taxonomy** — retained with added decision tree and IRR standard.
- **Scope boundaries** — retained unchanged. This programme does not make theological reform claims, iʿjāz claims, or extend to Hadith.

---

_End of Dossier v2.0_

_Document maintained by the Principal Researcher. All changes to be committed to the project Git repository with descriptive commit messages. Next scheduled review: upon submission of Paper 1._

_وَهُوَ بِكُلِّ شَيْءٍ عَلِيمٌ_

_And He is, of all things, Knowing._

_— Qur'an 2:29_