# Dalail al-Khayrat — Master Tagging Schema (v1.0, locked)

Companion doc to `DK_Tagging_Template.xlsx`. This schema governs Book A/B print,
the digital/app format, and Urdu/English/Hindi translation — one schema, reused,
never rebuilt.

## The one decision that matters most

**Language is a row, not a column.** Every prior temptation to add `text_ur`,
`text_en`, `text_hi` columns to a single flat sheet is the rework trap: it caps
you at the languages you thought of on day one, and every commentary/transliteration
variant needs its own column too. Instead:

- `01_DK_UNITS` — the structural spine. One row per addressable unit. No text, no language. Ever.
- `02_DK_CONTENT` — one row per unit **per language per content_role**. Adding Hindi,
  adding a second English commentary layer, adding transliteration — all of it is
  new rows here. The schema shape never changes.

Everything else in this document exists to defend that one decision.

---

## 1. `DK_UNITS` — structural spine (language-independent)

| Column | Type | Required | Controlled values | Notes |
|---|---|---|---|---|
| `unit_id` | string | ✅ | — | `DK-{SECTION}-{NNNN}`. Permanent once assigned. Never renumbered, never reused. |
| `parent_unit_id` | string | | — | FK to another `unit_id`. Blank = root-level unit. Used for nested blocks (e.g. a name-unit's parent is the Asma block header). |
| `sequence_global` | integer | ✅ | — | Monotonic reading order across the *entire* book, front matter to colophon. Powers "next/previous" in the app without touching hizb logic. |
| `section` | enum | ✅ | `front_matter` \| `hizb` \| `closing_dua` | Matches the pipeline already in production — Asma-un-Nabi (201 names) stays under `front_matter`, consistent with the existing `DK-FM-0039` records. |
| `hizb_no` | int 1–8 | | 1–8, blank outside hizb | |
| `day_of_week` | enum | | `mon`…`sun`, blank outside hizb | The daily-recitation assignment (Hizb 1 = Monday, etc., per the manuscript's own ترتیب). |
| `rub_no` | int 1–4 | | blank if n/a | Quarter-division cross-reference (4-day reading plan). |
| `thuluth_no` | int 1–3 | | blank if n/a | Third-division cross-reference (3-day reading plan). Rub and thuluth are **independent overlapping views onto the same spine** — a unit can carry both, since the manuscript itself offers 2-day/3-day/4-day/7-day reading schedules over identical content. |
| `block_kind` | enum | ✅ | `title_matter` \| `heading` \| `dua_formula` \| `salawat_formula` \| `name_of_prophet` \| `rubric` \| `instructional` \| `hikayat` \| `quran_ayah` \| `hadith_citation` \| `invocation_closing` \| `colophon` | Document-role classification. This is what InDesign paragraph styles key off — one enum value maps to exactly one style, so a print-layout decision never requires touching content. |
| `semantic_type` | enum | ✅ | `matn` \| `hikayat` \| `rubric` \| `instructional` \| `citation-ref` \| `quran-ayah` | Retained from the existing pipeline for continuity. Coarser than `block_kind`; used for translation-memory grouping and normalization keying. |
| `is_boilerplate` | bool | ✅ | TRUE/FALSE | See §4 below — the single highest-leverage field in this schema for translation cost. |
| `template_id` | string | | blank if not templated | Groups units sharing a formula skeleton (e.g. `TPL-IBRAHIMI-01`, `TPL-ADAD-QUANTIFIER-01`). |
| `repeat_count` | int | ✅ (default 1) | — | Captures inline recitation instructions like "(تین بار)" = recite 3×. |
| `quran_ref` | string | | e.g. `33:56` | Surah:ayah for `block_kind = quran_ayah`. |
| `hadith_narrator` | string | | e.g. "Abu Hurairah" | For `block_kind = hadith_citation`. |
| `footnote_ref` | string | | — | Any manuscript footnote/marginal reference. |
| `source_anchor` | string | ✅ | — | Human-readable pointer back to the Google Doc source (tab + approximate location), so a scholar or editor can always find the original. |
| `scholar_flag` | bool | ✅ | TRUE/FALSE | Set TRUE for anything needing a ruling (the 189-vs-201 pattern). |
| `scholar_flag_reason` | text | | — | Concrete, enumerated description — never a vague "check this." |
| `status` | enum | ✅ | `draft` → `normalized` → `tagged` → `scholar_review` → `scholar_approved` → `locked` | Moves rightward only. A correction after `locked` spawns a child `unit_id`, it does not reopen the row. |
| `notes_internal` | text | | — | Pipeline notes. Never shown to scholars (see `05_SCHOLAR_REVIEW`). |

## 2. `DK_CONTENT` — per-language content

| Column | Type | Required | Controlled values | Notes |
|---|---|---|---|---|
| `content_id` | string | ✅ | `{unit_id}-{LANG}` (append `-TL` for transliteration, `-C1`/`-C2` for multiple commentary layers) | |
| `unit_id` | string | ✅ | FK → `DK_UNITS.unit_id` | |
| `language_code` | enum | ✅ | `ar` \| `ur` \| `en` \| `hi` | Appending a 5th language = appending a value here, nothing upstream changes. |
| `content_role` | enum | ✅ | `source_original` \| `translation` \| `transliteration` \| `commentary` | |
| `text` | text | ✅ for `locked`/`published` rows | — | The actual string. RTL scripts (Arabic/Urdu) and LTR (English) coexist fine — Sheets/Docs auto-detect direction per cell. |
| `script` | enum | ✅ | `Arabic` \| `Nastaliq` \| `Devanagari` \| `Latin` | Needed because Urdu can be written Nastaliq or (rarely) Latin, and transliteration is always Latin regardless of `language_code`. |
| `translator` | string | | — | |
| `translation_date` | date | | — | |
| `review_status` | enum | ✅ | `untranslated` → `draft` → `scholar_review` → `scholar_approved` → `published` | Independent per language — English can be `published` while Hindi is still `untranslated`, which is exactly the phased Urdu→English→Hindi rollout already planned. |
| `reviewer` | string | | — | |
| `review_notes` | text | | — | |
| `char_length` | int | ✅ (auto) | — | |
| `word_count` | int | ✅ (auto) | — | |
| `version` | int | ✅ | — | Bump on any post-approval text change. |

## 3. `DK_NAMES_ASMA` — special case: the 201/189 names block

One row per **discrete name-unit** as currently isolated (`DK-FM-0039-*`). This
table is where the scholar's ruling on the shortfall gets recorded permanently,
without ever touching `DK_UNITS` or `DK_CONTENT` structurally.

| Column | Type | Controlled values | Notes |
|---|---|---|---|
| `name_id` | string | `{unit_id}-{NNN}` | e.g. `DK-FM-0039-014` |
| `unit_id` | string | FK → parent Asma block | |
| `seq_no_manuscript` | int | 1–201 | The manuscript's own claimed numbering, kept even where later found to be non-discrete. |
| `arabic_name` | text | — | |
| `separator_formula_present` | bool | TRUE/FALSE | Whether the expected separator formula appears before this name — the mechanical marker that produced the 189-count. |
| `discrete_unit_confirmed` | enum | `pending` \| `confirmed_discrete` \| `merge_with_next` \| `merge_with_previous` | The scholar's actual ruling. |
| `scholar_decision` / `scholar_notes` | text | — | |

## 4. `DK_PRODUCTION` — print + digital metadata

| Column | Type | Controlled values | Notes |
|---|---|---|---|
| `unit_id` | string | FK | |
| `book_target` | enum | `A` \| `B` \| `both` | Since Book A is Arabic-only daily-carry and Book B is the full language-specific companion, most `matn` units are `both`; commentary/translation units are `B` only. |
| `indesign_style` | string | — | Keyed off `block_kind`, not typed per-unit by a designer — one style per `block_kind` value, period. |
| `print_color` | enum | `black` \| `red` | Matches the locked two-color interior spec (black + red ink). |
| `page_break_hint` | enum | `none` \| `before` \| `after` | |
| `audio_file_ref` / `audio_start_ms` / `audio_end_ms` | string/int | — | For the app's synced recitation audio. |
| `app_screen_ref` | string | — | Deep-link target inside the app. |
| `search_keywords` | text | — | App/site search index terms. |

## 5. `SCHOLAR_REVIEW` — the only sheet scholars need to open

Pulled by formula from `01_DK_UNITS` + `02_DK_CONTENT`, filtered to what a scholar
actually needs: `unit_id`, `hizb_no`, `day_of_week`, `section`, `block_kind`,
`arabic_text`, `flag_reason`, plus three input columns — `scholar_decision`
(`approved` / `needs_correction` / `needs_discussion`), `scholar_notes`,
`reviewed_by`, `review_date`. No production or translation-workflow columns are
visible here — scholars review classical-text fidelity, not typesetting.

## 6. `CONTROLLED_VOCAB`

Single source of truth for every enum above. All dropdowns validate against this
sheet. **When a new value is genuinely needed, add it here first, then to the
column's dropdown range — never type a one-off value directly into a data row.**

---

## Governance rules (this is what actually prevents rework — not exhaustive fields)

1. **Append-only.** New need → new column at the right end of a sheet, existing
   rows blank. Never repurpose a column's meaning, never reorder, never rename.
2. **`unit_id` is permanent.** A structural correction (like the 189-vs-201 case)
   creates a **child** `unit_id` (`DK-FM-0039-A`, `-B`, …), never mutates or
   deletes the parent. Full audit trail back to the ruling that caused it.
3. **Status only moves forward**: `draft → normalized → tagged → scholar_review
   → scholar_approved → locked`. A `locked` row that needs to change gets a new
   version or a child unit — not a silent edit.
4. **Structure lives once.** Hizb/day/rub/thuluth/block_kind exist only in
   `DK_UNITS`. Every other table points back by `unit_id` — never duplicated.
5. **Section codes match production already in use**: `FM` (front matter incl.
   Asma-un-Nabi), `H1`–`H8`, `CD` (closing dua/colophon). Nothing here
   contradicts the existing `DK_AR1_tagged_final` pipeline; this is a superset.

## Key architectural insight: boilerplate deduplication

Hizb 4–7 in particular are dominated by one salawat skeleton repeated with only
the closing quantifier clause varying — "…عدد قطر الامطار" / "…عدد النجوم" /
"…ملء السموات", and so on, often dozens of times per hizb. Tag every instance
`is_boilerplate = TRUE` with a shared `template_id`. A translator then translates
the **template once per language** and the **quantifier clauses as a short table**,
rather than every instance as a discrete unit. This is a scope/cost decision for
the translation commission, not just a tagging nicety — confirm the approach
with the scholar and the translators *before* Urdu translation begins, since it
changes what "translate the whole book" actually means in terms of billable units.

---

## JSON mirror (for the app/API — same fields, nested per unit)

```json
{
  "unit_id": "DK-H1-0012",
  "parent_unit_id": null,
  "sequence_global": 340,
  "section": "hizb",
  "hizb_no": 1,
  "day_of_week": "mon",
  "rub_no": null,
  "thuluth_no": null,
  "block_kind": "salawat_formula",
  "semantic_type": "matn",
  "is_boilerplate": true,
  "template_id": "TPL-IBRAHIMI-01",
  "repeat_count": 1,
  "quran_ref": null,
  "hadith_narrator": null,
  "footnote_ref": null,
  "source_anchor": "Hizb 1, Ibrahimi salawat variant",
  "scholar_flag": false,
  "scholar_flag_reason": null,
  "status": "tagged",
  "content": [
    {
      "content_id": "DK-H1-0012-AR",
      "language_code": "ar",
      "content_role": "source_original",
      "text": "اَللّٰہُمَّ صَلِّ عَلٰی سَیِّدِنَا وَ مَوْلَانَا مُحَمَّدٍ...",
      "script": "Arabic",
      "review_status": "scholar_approved",
      "version": 3
    },
    {
      "content_id": "DK-H1-0012-UR",
      "language_code": "ur",
      "content_role": "translation",
      "text": null,
      "script": "Nastaliq",
      "review_status": "untranslated",
      "version": 1
    }
  ],
  "production": {
    "book_target": "both",
    "indesign_style": "Salawat_Body_AR",
    "print_color": "black",
    "page_break_hint": "none",
    "audio_file_ref": "H1_track03.mp3",
    "audio_start_ms": 12400,
    "audio_end_ms": 18900,
    "app_screen_ref": "hizb1/day-monday/unit-0012",
    "search_keywords": ["salawat", "ibrahimi", "hizb1", "monday"]
  }
}
```

This nests cleanly for the app/API layer while the relational tables stay flat
and simple for Google Sheets / scholar review. Same fields, two shapes — no
duplication of meaning.
