This is the **Single Source of Truth (SSOT)**.

This document is not a tutorial; it is a **specification** for upgrading your mental model from "Markdown Writer" to "Typst Architect." It is structured to prevent the specific failures common to developers moving to document compilation.

---

# THE TYPST MANIFESTO
**Version:** 1.0 (Targeting Typst 0.12+)
**Objective:** High-End RTL/Islamic Publishing
**Prerequisites:** VS Code, Tinymist Extension, Git.

---

## PHASE 0: THE INFRASTRUCTURE
**The Principle:** *If the feedback loop is slow, you will fail.*

### 0.1 The Toolchain
Do not use the web app for serious publishing.
1.  **Editor:** VS Code.
2.  **Engine:** **Tinymist** (Extension).
    *   *Config:* Enable "Pin Preview" (keep the PDF visible while editing sub-files).
    *   *Config:* Set `typst.root` to your project folder (allows absolute paths `/images/logo.png`).
3.  **Fonts:**
    *   Install **Amiri** (Naskh/Body) and **Scheherazade New** (Alternative).
    *   *Verify:* Run `typst fonts` in terminal to confirm Typst sees them.

### 0.2 The Package Manager (Universe)
Do not download files manually. Import them.
*   **Syntax:** `#import "@preview/package-name:version": *`
*   **Essential Packages for you:**
    *   `hydra`: For complex headers/footers (retrieving current chapter title).
    *   `codly`: If you ever need to display code blocks nicely.

---

## PHASE 1: THE SYNTAX SHIFT
**The Principle:** *Unlearn Markdown. Respect the Modes.*

### 1.1 The Three Modes
Typst is not a single language. It is three languages in a trench coat.
1.  **Markup Mode:** The default. Text is text. (Like Markdown).
2.  **Script Mode:** Logic and variables. Triggered by `#`. (Like Python).
3.  **Math Mode:** Equations. Triggered by `$`. (Like LaTeX).

### 1.2 The Translation Dictionary (Memorize This)
| Feature | Markdown | Typst | The "Gotcha" |
| :--- | :--- | :--- | :--- |
| **Heading** | `# Title` | `= Title` | **# is reserved for code.** |
| **Bold** | `**Text**` | `*Text*` | Single asterisk only. |
| **Italic** | `*Text*` | `_Text_` | Underscore is strictly italic. |
| **Link** | `[Txt](url)` | `#link("url")[Txt]` | It's a function. |
| **Image** | `![Alt](src)` | `#image("src")` | It's a function. |
| **List** | `- Item` | `- Item` | Same. |
| **Enum** | `1. Item` | `+ Item` | Use `+` for auto-numbering. |
| **Comments** | `<!-- -->` | `//` or `/* */` | Standard C-style comments. |

### 1.3 The Container Concept (`[...]`)
In Markdown, text is just characters. In Typst, `[Text]` is a **Content Block**.
*   You can pass text into functions: `#rect[This is text inside a box]`
*   You can save text to variables: `#let disclaimer = [*Warning:* Haram content.]`

---

## PHASE 2: THE STYLING ENGINE
**The Principle:** *`set` is for defaults. `show` is for exceptions.*

### 2.1 The `set` Rule (Global Inheritance)
Equivalent to CSS `body { ... }`. Put this at the top of your `main.typ`.

```typst
// RTL ISLAMIC BOOK DEFAULTS
#set text(
  font: "Amiri",
  size: 12pt,
  lang: "ar",
  region: "SA",
  dir: rtl  // CRITICAL: Flips the layout logic
)
#set par(
  leading: 0.8em,       // Line height
  justify: true,        // Essential for Arabic
  first-line-indent: 0pt
)
#set page(
  paper: "a5",
  numbering: "١",       // Eastern Arabic Numerals for page numbers
)
```

### 2.2 The `show` Rule (Transformation)
Equivalent to CSS Selectors `h1 { ... }`.
*   **Basic:** Change the look.
    ```typst
    #show heading: set text(fill: maroon, font: "Scheherazade New")
    ```
*   **Advanced:** Change the structure (The "Hook").
    ```typst
    // Add a decorative ornament after every Level 1 heading
    #show heading.where(level: 1): it => [
      #align(center)[#it]
      #align(center)[*** ۞ ***]
    ]
    ```

### 2.3 Micro-Typography (The "InDesign" Layer)
*   **Tracking:** `#set text(tracking: 0.5pt)` (Rarely used in Arabic, useful for English headers).
*   **Kashida:** Typst's justification engine handles Arabic stretching automatically if the font supports it, but you can force "Justify" or "Ragged" via `#set par(justify: true)`.

---

## PHASE 3: THE LAYOUT ARCHITECTURE
**The Principle:** *Everything is a box. Grids are the skeleton.*

### 3.1 Block vs. Box
*   **`#block[...]`**: Takes full width (like `<div>`). Breaks the paragraph.
*   **`#box[...]`**: Inline (like `<span>`). Flows with text.
    *   *Use case:* Drawing a border around a specific word in a sentence.

### 3.2 The Tafsir Layout (The Grid)
For side-by-side translation (Arabic Right, English Left).

```typst
#grid(
  columns: (1fr, 1fr), // Equal width columns
  gutter: 1cm,         // Space between
  // COLUMN 1 (Right, because dir is RTL)
  [
    = سورة الفاتحة
    بسم الله الرحمن الرحيم
  ],
  // COLUMN 2 (Left)
  text(dir: ltr, lang: "en")[
    = The Opening
    In the name of Allah...
  ]
)
```

### 3.3 Reference Management
*   **Footnotes:** `#footnote[This is a note.]`.
*   **Bibliography:** `#bibliography("works.bib")`.
*   **Reference:** `@key` creates a link to the bibliography or a figure.

---

## PHASE 4: THE LOGIC CORE
**The Principle:** *Don't repeat yourself. Automate.*

### 4.1 Variables & Functions (`#let`)
Create a "Hadith Box" component.

```typst
#let hadith(source, body) = {
  block(
    fill: luma(240), // Light gray
    stroke: (right: 2pt + maroon), // Right border only
    inset: 1em,
    width: 100%,
    radius: 4pt,
    [
      *#source:* \   // The Source (e.g., Bukhari)
      #body          // The Hadith text
    ]
  )
}

// Usage:
#hadith("Sahih Bukhari")[Actions are by intentions...]
```

### 4.2 The `context` System (The "State" Manager)
**Replacing `locate`.** You need this to know "Where am I?" (e.g., for headers that change based on the chapter).

```typst
#context {
  if counter(page).get().first() > 1 [
    // Content to show only after page 1
    #line(length: 100%)
  ]
}
```

---

## PHASE 5: THE PROJECT STRUCTURE
**The Principle:** *Separate Content from Presentation.*

### 5.1 The File Tree
```text
/my-book
  /fonts
  /images
  main.typ       (The Entry Point)
  template.typ   (The Design System)
  /chapters
    01-intro.typ
    02-tawhid.typ
```

### 5.2 The Template Pattern (`template.typ`)
Wrap your entire document in a function.

```typst
// template.typ
#let book-template(title: "", body) = {
  set document(title: title)
  set page(paper: "a5")
  set text(font: "Amiri", dir: rtl)
  
  // Title Page
  align(center + horizon)[
    #text(2em, weight: "bold")[#title]
  ]
  pagebreak()
  
  // The Content
  body
}
```

### 5.3 The Main File (`main.typ`)
```typst
#import "template.typ": book-template

#show: book-template.with(title: "My Islamic Book")

#include "chapters/01-intro.typ"
#include "chapters/02-tawhid.typ"
```

---

## THE DRILL (Your First Assignment)

**Objective:** Create a single PDF page that looks like a classical page of Tafsir.

1.  **Setup:** Create `main.typ` and `template.typ`.
2.  **Config:** Set margins to 2.5cm, font to Amiri.
3.  **Header:** Create a header that says "Chapter 1" on the right and page number on the left.
4.  **Layout:**
    *   Top: A centered block containing a Quranic verse (large font).
    *   Middle: A 2-column grid. Right column: Arabic commentary. Left column: English translation.
    *   Bottom: A footnote explaining a word.
5.  **Logic:** Create a function `#ayah[text]` that automatically wraps the text in a decorative frame.

**Execute this.** If you can do this, you have graduated from Markdown.


---
---


### The Ruthless Critique (Phase 0 Audit)

You asked for a stress test of the draft I just provided. Here is where it failed to meet the "Manifesto" standard:

**1. The "Package" Breach (Critical Failure)**
*   **The Flaw:** In the SSOT, I promised **0.2 The Package Manager**. In the drafted Phase 0, I skipped it entirely in the "Drill".
*   **The Consequence:** You don't know if your firewall or network is blocking Typst from downloading packages. If you can't download packages, you can't use `codly` or `hydra` later.
*   **The Fix:** The Drill *must* include a package import to prove the connection works.

**2. The CLI "Ghost"**
*   **The Flaw:** I made you install the CLI (`typst --version`), but then we went straight back to VS Code.
*   **The Reality:** If VS Code crashes or the extension hangs (it happens), you need to know how to compile from the terminal.
*   **The Fix:** We need a one-line terminal command test.

**3. The Font "OS" Trap**
*   **The Flaw:** I told you to "Install to OS".
*   **The Edge Case:** If you are using **WSL (Windows Subsystem for Linux)** or a Docker container later, Typst won't see Windows fonts.
*   **The Fix:** For now, OS install is fine, but we must add a note that *local font folders* are the professional standard we will adopt in Phase 5.

---

### **PHASE 0: THE REVISED & PATCHED DRAFT**

Here is the corrected Phase 0. **Execute this version.**

#### **Step 1: The Engine (VS Code + Tinymist)**
1.  **Install VS Code.**
2.  **Install Extension:** `Tinymist` (Myriad Dreamin).
3.  **Config:**
    *   `Cmd/Ctrl + ,` -> Search `tinymist.preview`.
    *   Set **Scroll Sync** to `onSelection`.

#### **Step 2: The CLI (The Backup Engine)**
*   **Windows:** `winget install Typst.Typst`
*   **Mac:** `brew install typst`
*   **Linux:** `cargo install --locked typst-cli`
*   **Verify:** Terminal -> `typst --version`

#### **Step 3: The Fonts (Amiri & Scheherazade)**
1.  Download [Amiri](https://fonts.google.com/specimen/Amiri) and [Scheherazade New](https://fonts.google.com/specimen/Scheherazade+New).
2.  **Install to OS** (Right-click -> Install).
3.  **Verify:** Terminal -> `typst fonts --variants | grep "Amiri"` (or `findstr` on Windows).

---

### **THE DRILL: PHASE 0 VERIFICATION (PATCHED)**
*Changes: Added Package download test and CLI compilation test.*

**1. Create `main.typ` and paste this:**

```typst
// 1. PACKAGE TEST (Checks Internet & Universe)
// We import 'blind' to generate dummy text.
#import "@preview/blind:0.1.0": blind

// 2. GLOBAL SETTINGS
#set page(paper: "a5", margin: 2cm)
#set text(font: "Amiri", size: 14pt, lang: "ar")
#set text(dir: rtl)

// 3. CONTENT
= اختبار النظام (System Check)

بسم الله الرحمن الرحيم

// Ligature Check
اللّٰه

// Numeral Check (Should be Eastern Arabic ١ if configured, but here we test default)
رقم: 123

// 4. PACKAGE EXECUTION
// If this generates Latin text inside an RTL doc, the package works.
#text(dir: ltr, lang: "en")[
  #blind(1)
]
```

**2. The VS Code Test:**
*   Click the **"Preview"** button (Top Right, usually a 'K' or Magnifying Glass).
*   **Success Criteria:** You see the PDF. The Latin dummy text (Lorem ipsum...) appears at the bottom.

**3. The CLI Test (The "Headless" Check):**
*   Close the Preview. Open the **Terminal** in VS Code (`Ctrl + ~`).
*   Run: `typst compile main.typ`
*   **Success Criteria:** A `main.pdf` file appears in your file explorer. Open it. If it looks like the preview, your toolchain is bulletproof.

**Execute. If the CLI command works and the PDF generates with the "Lorem Ipsum" text, we are Go for Phase 1.**

---
---





















