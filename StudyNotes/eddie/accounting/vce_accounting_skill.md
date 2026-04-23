# Skill: VCE Accounting Cheat Sheet Generator

## Purpose
Generate interactive HTML cheat sheets for VCE Accounting Units 1 & 2 (Neville Box 7th ed.).
Each chapter becomes a standalone `.html` file that students can open in any browser.

---

## Output Rules

### File format
- Always output `text/html` artifact type — NEVER React/TSX
- Single self-contained file: all CSS and JS inline, no external dependencies
- Must download as `.html` from Claude artifact panel

### JavaScript rules (critical — past errors)
- Always use `var` — never `const` or `let`
- Never use template literals (backticks) — use string concatenation only
- Never use arrow functions — use `function` keyword or IIFE
- Use HTML entities for special characters: `&#9660;` (▼), `&#9650;` (▲), `&#9658;` (▶), `&#9733;` (★), `&#9888;` (⚠), `&#128161;` (💡), `&#10003;` (✓)
- Avoid apostrophes inside JS strings — rephrase or use `&apos;`

### CSS rules
- No CSS variables — use hardcoded hex values only
- No `position: absolute` tooltips inside `overflow: hidden` containers (causes clipping)
- Hover annotations on balance sheet lines: use adjacent sibling CSS (`.bs-line.indent:hover + .bs-line.anno`) not absolute positioning
- Hot badge tooltips: use `position: absolute; top: calc(100% + 6px)` (drops DOWN) — never upward

---

## Visual Design System

### Page structure
```html
<h1>VCE Accounting — Chapter X</h1>
<p class="subtitle">Chapter Title · tap any term to expand</p>
<input id="search" ...>
<p class="section-label">&#128202; Visual Reference Panels</p>
<!-- Visual panels (optional, collapsible) -->
<p class="section-label">&#128218; Key Terms by Section</p>
<div id="list"></div>
<p class="footer">...</p>
```

When a chapter has enough visual panels to warrant it, use `.section-label` dividers to split visual panels from the terms accordion. CSS:
```css
.section-label { margin: 16px 12px 4px; font-size: 11px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.8px; color: #888; }
```

### Colour palette for accordion sections
| Class | Border | Head bg | Example bg | Use for |
|-------|--------|---------|------------|---------|
| purple | #AFA9EC | rgba(206,203,246,0.3) / #3C3489 | #EEEDFE/#3C3489 | Intro/overview sections |
| teal | #5DCAA5 | rgba(159,225,203,0.25) / #085041 | #E1F5EE/#085041 | Assets, receipts, positive concepts |
| coral | #D85A30 | rgba(240,153,123,0.22) / #4A1B0C | #FAECE7/#4A1B0C | Liabilities, payments, risk |
| amber | #BA7517 | rgba(239,159,39,0.18) / #412402 | #FAEEDA/#412402 | Equity, formulas, calculations |
| blue | #378ADD | rgba(133,183,235,0.22) / #042C53 | #E6F1FB/#042C53 | Equations, share market, general |
| pink | #D4537E | rgba(237,147,177,0.2) / #4B1528 | #FBEAF0/#4B1528 | Ethics, evaluation sections |
| gray | #888780 | rgba(180,178,169,0.18) / #2C2C2A | #F1EFE8/#2C2C2A | Principles, definitions |

### Collapsible panel colours
| Class | Use for |
|-------|---------|
| .box-wrap.green | Inflow/receivables journals (Cash Receipts, Sales), positive visuals |
| .box-wrap.red | Outflow/payables journals (Cash Payments, Purchases) |
| .box-wrap.purple | Comparison tables |
| .box-wrap.amber | Formula cards |
| .box-wrap.teal | Statements, accounting equation effects, general worked examples |
| .box-wrap.blue | Income statements |

---

## Component Patterns

### 1. Terms accordion section
```javascript
// In the data array:
{ cat: "X.1 Section Title", color: "purple", hot: false, items: [
  { term: "Term name", def: "Plain English definition.", eg: "Concrete real-world example." },
  { term: "Another term", def: "Definition.", eg: "Example.", note: "Optional exam tip." }
]}
```
- `hot: true` adds a red ★ HOT TOPIC badge to the section header
- `note` appears as italic ⚠ Exam tip text inside the expanded term
- Colors rotate: purple → teal → coral → amber → blue → pink → gray

### 2. Hot topic badge
```html
<span class="hot-badge">&#9733; HOT TOPIC
  <span class="tip">High-frequency exam topic — appears in almost every exam</span>
</span>
```
CSS (tooltip drops DOWN to avoid clipping):
```css
.hot-badge { position: relative; display: inline-flex; background: #E24B4A; color: #fff; font-size: 10px; font-weight: 700; border-radius: 5px; padding: 2px 7px; cursor: help; white-space: nowrap; }
.hot-badge .tip { display: none; position: absolute; top: calc(100% + 6px); left: 50%; transform: translateX(-50%); background: #501313; color: #fff; font-size: 11px; border-radius: 6px; padding: 5px 9px; width: 190px; text-align: center; line-height: 1.4; z-index: 50; pointer-events: none; }
.hot-badge .tip::after { content: ""; position: absolute; bottom: 100%; left: 50%; transform: translateX(-50%); border: 5px solid transparent; border-bottom-color: #501313; }
.hot-badge:hover .tip { display: block; }
```

### 3. Collapsible panel wrapper
```html
<div class="box-wrap green">
  <div class="box-toggle" onclick="toggleB(this)">
    <span>&#128229; Panel Title</span>
    <span class="cat-arrow">&#9660;</span>
  </div>
  <div class="box-body">
    <!-- content here -->
    <p class="box-note">&#128161; Tip note here.</p>
  </div>
</div>
```
JS toggle function:
```javascript
function toggleB(el) {
  var body = el.nextElementSibling;
  var arr = el.querySelector(".cat-arrow");
  var open = body.classList.toggle("open");
  arr.innerHTML = open ? "&#9650;" : "&#9660;";
}
```

### 4. Journal table (receipts or payments)
```html
<div class="box-wrap green"> <!-- green=receipts, red=payments -->
  <div class="box-toggle" onclick="toggleB(this)">
    <span>&#128229; Cash Receipts Journal — worked example</span>
    <span class="cat-arrow">&#9660;</span>
  </div>
  <div class="box-body">
    <div style="overflow-x:auto;">
      <table class="jt">
        <thead><tr>
          <th>Date</th><th>Details</th><th>Rec No.</th>
          <th class="num">Bank <span class="col-tag tag-g">asset up</span></th>
          <th class="num">Sales</th>
          <th class="num">Sundries</th>
        </tr></thead>
        <tbody>
          <tr><td>1 Jun</td><td>Cash sales</td><td>001</td>
            <td class="num">850</td><td class="num">850</td><td class="num">-</td></tr>
          <tr><td colspan="6" class="label">Customers paid cash — Bank up, Sales revenue recorded</td></tr>
        </tbody>
        <tfoot>
          <tr><td colspan="3">Totals</td>
            <td class="num">$ 850</td><td class="num">$ 850</td><td class="num">$ 0</td></tr>
          <tr><td colspan="6" class="label">Bank total must equal sum of all other columns &#10003;</td></tr>
        </tfoot>
      </table>
    </div>
    <p class="box-note">&#128161; The Bank column total must always equal the sum of all other column totals.</p>
  </div>
</div>
```

### 5. Comparison table
```html
<div class="box-wrap purple">
  <div class="box-toggle" onclick="toggleB(this)">
    <span>&#128202; Comparison Title</span>
    <span class="cat-arrow">&#9660;</span>
  </div>
  <div class="box-body">
    <div style="overflow-x:auto;">
      <table class="ct">
        <thead><tr><th>Feature</th><th>Option A</th><th>Option B</th></tr></thead>
        <tbody>
          <tr>
            <td><strong>Liability</strong></td>
            <td><span class="tag tag-r">risk</span>Unlimited</td>
            <td><span class="tag tag-g">safer</span>Limited</td>
          </tr>
        </tbody>
      </table>
    </div>
    <p class="box-note">&#128161; Tip here.</p>
  </div>
</div>
```

### 6. Formula cards
Uniform white cards with a soft cream formula bar (no dark backgrounds — they read busy). The amber panel wrapper provides the only colour cue.
```html
<div class="box-wrap amber">
  <div class="box-toggle" onclick="toggleB(this)">
    <span>&#129518; Key Formulas</span>
    <span class="cat-arrow">&#9660;</span>
  </div>
  <div class="box-body">
    <div class="formula-grid">
      <div class="fcard">
        <h3>Rate of Return</h3>
        <div class="formula">Net return / Cost x 100</div>
        <p>Plain English explanation of what this calculates.</p>
        <div class="worked">Invested $5,000, net return $400<br>
          <strong>= 400 / 5,000 x 100 = 8% p.a.</strong></div>
      </div>
    </div>
    <p class="box-note">&#128161; Always use NET return after costs — common exam mistake.</p>
  </div>
</div>
```
CSS (uniform white card style):
```css
.formula-grid { display: grid; grid-template-columns: 1fr; gap: 12px; }
.fcard { background: #fff; border: 1px solid #E8E4D5; border-radius: 8px; padding: 13px; box-shadow: 0 1px 3px rgba(0,0,0,0.04); }
.fcard h3 { font-size: 13.5px; color: #2C2C2A; margin-bottom: 8px; font-weight: 700; }
.fcard .formula { background: #F7F5EF; color: #2C2C2A; border: 1px solid #E8E4D5; padding: 9px 12px; border-radius: 6px; font-family: "SF Mono", Consolas, monospace; font-size: 13px; font-weight: 600; text-align: center; margin-bottom: 9px; }
.fcard p { font-size: 12px; color: #555; margin-bottom: 9px; }
.fcard .worked { background: #F7F5EF; border-left: 3px solid #BA7517; padding: 8px 10px; font-size: 12px; color: #412402; border-radius: 0 6px 6px 0; }
@media (min-width: 640px) { .formula-grid { grid-template-columns: 1fr 1fr; } }
```
**Design note:** earlier iterations used a dark-brown background for the formula bar and per-card colour accents. Both were rejected as too busy — keep formula cards uniform and let the amber panel wrapper carry the colour cue.

### 7. Accounting equation effects table
Maps a single transaction to the multiple balance-sheet lines it affects. Use `.ct` with `rowspan` on the transaction cell. Good for credit transaction chapters where one invoice hits assets, liabilities, and equity simultaneously.
```html
<div class="box-wrap teal">
  <div class="box-toggle" onclick="toggleB(this)">
    <span>&#9874; Accounting Equation Effects — credit transactions</span>
    <span class="cat-arrow">&#9660;</span>
  </div>
  <div class="box-body">
    <div style="overflow-x:auto;">
      <table class="ct">
        <thead><tr><th>Transaction</th><th>Item in Balance Sheet</th><th>Classification</th><th>Change</th><th>$</th></tr></thead>
        <tbody>
          <tr>
            <td rowspan="3"><strong>Credit sale $900 + GST</strong><br><small>Invoice issued</small></td>
            <td>Accounts Receivable</td><td>Current Asset</td><td>Increase</td><td>990</td>
          </tr>
          <tr><td>Sales Revenue</td><td>Revenue (Equity up)</td><td>Increase</td><td>900</td></tr>
          <tr><td>GST Payable</td><td>Current Liability</td><td>Increase</td><td>90</td></tr>
        </tbody>
      </table>
    </div>
    <p class="box-note">&#128161; Assets up, Liabilities up, Equity up — the equation stays balanced.</p>
  </div>
</div>
```

### 8. Year-by-Year Interest Comparison Table
Shows how different interest types (flat rate vs reducing balance) diverge over the life of a loan. Use when a chapter needs to make the difference between nominal and effective rates concrete. Good for finance chapters.
```html
<div class="box-wrap amber">
  <div class="box-toggle" onclick="toggleB(this)">
    <span>&#128200; Flat Rate vs Reducing Balance &mdash; Year-by-Year</span>
    <span class="cat-arrow">&#9660;</span>
  </div>
  <div class="box-body">
    <p style="font-size:12.5px; margin-bottom:10px; color:#412402;"><strong>Scenario:</strong> Debbie borrows $6,000 at 10% over 4 years. She repays $1,500 of principal each year.</p>
    <div style="overflow-x:auto;">
      <table class="inttbl">
        <thead><tr>
          <th>Year</th>
          <th>Opening<span class="sub">balance owed</span></th>
          <th>Flat rate<span class="sub">10% of $6,000</span></th>
          <th>Reducing<span class="sub">10% of balance</span></th>
          <th>Closing<span class="sub">balance owed</span></th>
        </tr></thead>
        <tbody>
          <tr><td>1</td><td>$6,000</td><td class="red-flat">$600</td><td class="green-rb">$600</td><td>$4,500</td></tr>
          <tr><td>2</td><td>$4,500</td><td class="red-flat">$600</td><td class="green-rb">$450</td><td>$3,000</td></tr>
          <tr><td>3</td><td>$3,000</td><td class="red-flat">$600</td><td class="green-rb">$300</td><td>$1,500</td></tr>
          <tr><td>4</td><td>$1,500</td><td class="red-flat">$600</td><td class="green-rb">$150</td><td>$0</td></tr>
          <tr class="total-row">
            <td colspan="2">Total interest</td>
            <td class="red-flat">$2,400</td>
            <td class="green-rb">$1,500</td>
            <td></td>
          </tr>
        </tbody>
      </table>
    </div>
    <div style="background:#fff; border:1px solid #EED09A; border-radius:6px; padding:10px 12px; margin-top:10px;">
      <div style="font-size:11px; font-weight:700; color:#412402; text-transform:uppercase; letter-spacing:0.4px; margin-bottom:6px;">The effective rate of the flat loan</div>
      <div style="font-size:12.5px; color:#412402; line-height:1.7;">
        Avg interest per year = $2,400 &divide; 4 = <strong>$600</strong><br>
        Avg balance owing = ($6,000 + $0) &divide; 2 = <strong>$3,000</strong><br>
        Effective rate = $600 &divide; $3,000 &times; 100 = <strong>20% p.a.</strong>
      </div>
    </div>
    <p class="box-note">&#128161; Tip goes here.</p>
  </div>
</div>
```
CSS:
```css
.inttbl { width: 100%; border-collapse: collapse; font-size: 12px; }
.inttbl th, .inttbl td { padding: 7px 6px; text-align: right; border-bottom: 1px solid #EEEAE0; }
.inttbl th:first-child, .inttbl td:first-child { text-align: center; font-weight: 700; width: 40px; }
.inttbl th { background: #FAEEDA; color: #412402; font-weight: 700; font-size: 10.5px; text-transform: uppercase; letter-spacing: 0.3px; line-height: 1.3; }
.inttbl .red-flat { background: #FAECE7; }
.inttbl .red-flat td { color: #4A1B0C; }
.inttbl .green-rb { background: #E1F5EE; }
.inttbl .green-rb td { color: #085041; }
.inttbl .total-row { background: #FFF4E3; font-weight: 700; }
.inttbl .total-row td { border-top: 2px solid #BA7517; border-bottom: none; padding-top: 9px; color: #412402; }
.inttbl .sub { font-size: 10px; font-weight: 400; display: block; opacity: 0.75; margin-top: 1px; }
```
**When to use:** loan comparison chapters (flat rate vs reducing balance, or simple vs compound interest). Column colouring is critical — coral/red for the expensive option, green for the cheaper one — so the visual comparison is immediate. Always include a mini effective-rate calculation box below the table for VCE questions that require `effective rate = avg interest / avg balance x 100`.

### 9. Balance sheet visual
Use inline annotation rows (not absolute tooltips) that appear on hover:
```html
<div class="bs-line indent">Cash at Bank<span>18,000</span></div>
<div class="bs-line anno">Most liquid asset — listed first</div>
```
CSS (annotation hidden by default, shown on hover of preceding row):
```css
.bs-line.anno { display: none; font-style: italic; font-size: 11px; color: #3C3489; background: #EEEDFE; padding: 3px 12px 3px 22px; }
.bs-line.indent:hover + .bs-line.anno,
.bs-line.subtotal:hover + .bs-line.anno { display: block; }
```

---

## Core JS Functions (always include verbatim)

```javascript
function build(source) {
  var list = document.getElementById("list");
  list.innerHTML = "";
  for (var i = 0; i < source.length; i++) {
    var cat = source[i];
    if (!cat.items.length) continue;
    var div = document.createElement("div");
    div.className = "cat " + cat.color;
    var badge = cat.hot ? '<span class="hot-badge">&#9733; HOT TOPIC<span class="tip">High-frequency exam topic — appears in almost every exam</span></span>' : "";
    var head = document.createElement("div");
    head.className = "cat-head";
    head.innerHTML = '<span class="cat-head-text">' + cat.cat + '</span><div class="cat-head-right">' + badge + '<small>' + cat.items.length + ' terms</small><span class="cat-arrow">&#9660;</span></div>';
    (function(d, h) {
      h.onclick = function() {
        var b = d.querySelector(".cat-body");
        var a = h.querySelector(".cat-arrow");
        var c = b.classList.toggle("collapsed");
        a.innerHTML = c ? "&#9658;" : "&#9660;";
      };
    })(div, head);
    div.appendChild(head);
    var body = document.createElement("div");
    body.className = "cat-body";
    for (var j = 0; j < cat.items.length; j++) {
      var item = cat.items[j];
      var t = document.createElement("div");
      t.className = "term";
      var note = item.note ? '<span class="term-note">&#9888; Exam tip: ' + item.note + '</span>' : "";
      t.innerHTML = '<div class="term-title" onclick="toggle(this)"><span>' + item.term + '</span><span class="arrow">&#9660;</span></div><div class="term-body"><p class="term-def">' + item.def + '</p><span class="term-eg">Eg: ' + item.eg + '</span>' + note + '</div>';
      body.appendChild(t);
    }
    div.appendChild(body);
    list.appendChild(div);
  }
}

function toggle(el) {
  var body = el.nextElementSibling;
  var arr = el.querySelector(".arrow");
  var open = body.classList.toggle("open");
  arr.innerHTML = open ? "&#9650;" : "&#9660;";
}

function filterTerms(q) {
  q = q.toLowerCase();
  var filtered = [];
  for (var i = 0; i < data.length; i++) {
    var cat = data[i];
    var items = [];
    for (var j = 0; j < cat.items.length; j++) {
      var item = cat.items[j];
      if (!q || item.term.toLowerCase().indexOf(q) > -1 || item.def.toLowerCase().indexOf(q) > -1) {
        items.push(item);
      }
    }
    filtered.push({ cat: cat.cat, color: cat.color, hot: cat.hot, items: items });
  }
  build(filtered);
}

build(data);
```

---

## Content Guidelines

### Definitions
- Plain English — no jargon unless the jargon IS the term being defined
- One or two sentences maximum
- Avoid apostrophes in JS strings (rephrase: "does not" not "doesn't")

### Examples
- Always real-world and specific (dollar amounts, business names, scenarios)
- Prefer Australian context (ATO, GST, ASX, Pty Ltd, EFTPOS)
- Match the Sarah's Cafe / small business scenario used throughout existing chapters for consistency

### Exam tips (note field)
- Only add when there is a genuinely common exam mistake or trap
- Keep to one sentence
- Examples of good exam tips:
  - "Use 'for the period ended' not 'as at' — this report covers a period, not a single date."
  - "Always use NET return (after costs) when calculating rate of return in VCE."
  - "Placing $ on every line is a common exam formatting mistake."

### Hot topic identification
Apply `hot: true` to sections that are high-frequency exam topics. Confirmed hot topics by chapter:
| Chapter | Hot sections |
|---------|-------------|
| Ch.1 | 1.3 Key Principles |
| Ch.2 | 2.4 Qualitative Characteristics, 2.5 Accounting Assumptions, 2.6 Ethics |
| Ch.3 | 3.3 Classified Balance Sheets, 3.4 Financial Transactions |
| Ch.4 | 4.2 Source Documents |
| Ch.5 | 5.3 Forms of Business Ownership, 5.5 Success and Failure |
| Ch.6 | 6.3 Rates of Return, 6.4 Simple vs Compound Interest |
| Ch.7 | 7.5 GST, 7.6 Evaluating Single Entry |
| Ch.8 | 8.2 Cash vs Profit, 8.3 Preparing an Income Statement |
| Ch.9 | 9.2 Accounts Receivable, 9.3 Accounts Payable, 9.4 GST in Credit Transactions, 9.5 Source Documents for Credit Transactions |
| Ch.10 | 10.2 The Cost of Interest, 10.4 Gearing, 10.5 Return on Owner's Investment |

---

## Workflow for New Chapters

When given a new chapter, follow this process:

1. **Ask** (if not already provided): chapter number, title, section headings (x.1, x.2 etc.)
2. **Identify** which sections are hot topics based on VCE exam history
3. **Decide** which visual panels would help (journals, comparison tables, formula cards, balance sheet)
4. **Confirm** with the user before building if unsure about visuals
5. **Build** the complete HTML file using this skill
6. **Remind** the user to download as `.html` (not `.tsx`)
7. **Offer** to build the matching chapter quiz as a second deliverable (see Quiz Generation section below)

---

## Quiz Generation

Each chapter gets a matching quiz HTML file with two tabs: **Multiple Choice** and **Exam Practice**. Filename convention: `vce_accounting_ch{N}_quiz.html`.

### Quiz Structure

**Multiple Choice tab — 15 questions** grouped into 3–5 sections matching the chapter's section headings. Questions mix:
- Definition recall ("Which is an example of X?")
- Calculation ("Given these numbers, what is the debt ratio?")
- Conceptual distinction ("Why would a borrower prefer reducing balance over flat rate?")
- Scenario application ("A cafe owner needs short-term cash — which source?")

**Exam Practice tab — 6–8 questions** split into Short Answer and Extended Response subsections. Use the exact scenarios from the textbook's end-of-chapter exercises wherever possible so the quiz directly prepares students for the workbook tasks.

### Coverage Check (before building)

Before generating the quiz, cross-reference against the textbook's end-of-chapter exercises. Build a coverage table:

| # | Topic | Section | Covered? |
|---|-------|---------|----------|

Every textbook exercise should be supported by at least one MC or exam question.

### Theme Colour

The quiz uses the chapter's dominant colour from the cheat sheet — i.e. the colour of the biggest/most relevant accordion section (usually a hot topic). For Ch.10, purple (#3C3489) matches the textbook chapter heading colour as well. Replace these values consistently throughout the template:
- Primary: `#3C3489` (headers, tab underline, progress bar stroke)
- Light accent: `#EEEDFE` (stimulus backgrounds, marks badges)
- Progress bar fill: medium version (e.g. `#7F77DD` for purple)

### Quiz Page Structure

```html
<h1>VCE Accounting &mdash; Chapter X Quiz</h1>
<p class="subtitle">Chapter Title &middot; Multiple choice + exam practice &middot; Hot topics focus</p>

<div class="tab-bar">
  <button class="tab-btn active" onclick="switchTab('mc')">&#127919; Multiple Choice</button>
  <button class="tab-btn" onclick="switchTab('exam')">&#128221; Exam Practice</button>
</div>

<div id="tab-mc" class="tab-pane active">
  <div class="score-bar">...</div>
  <div class="q-section-head">Section emoji + Title</div>
  <!-- MC cards -->
</div>

<div id="tab-exam" class="tab-pane">
  <div class="q-section-head">&#128203; Short Answer Questions</div>
  <!-- eq-cards -->
  <div class="q-section-head">&#128218; Extended Response Questions</div>
  <!-- eq-cards -->
</div>
```

### MC Card Pattern

```html
<div class="q-card" id="mc1">
  <div class="q-meta">
    <span class="q-num">Q1</span>
    <span class="q-hot">&#9733; HOT</span>  <!-- only on hot-topic questions -->
    <span class="q-marks">1 mark</span>
  </div>
  <div class="q-text">Question text here.</div>
  <div class="mc-options">
    <div class="mc-opt" onclick="checkMC(this,'mc1','A')"><span class="opt-letter">A</span>Option A</div>
    <div class="mc-opt" onclick="checkMC(this,'mc1','B')"><span class="opt-letter">B</span>Option B</div>
    <div class="mc-opt" onclick="checkMC(this,'mc1','C')"><span class="opt-letter">C</span>Option C</div>
    <div class="mc-opt" onclick="checkMC(this,'mc1','D')"><span class="opt-letter">D</span>Option D</div>
  </div>
  <div class="q-feedback" id="fb-mc1"></div>
</div>
```

Answers and feedback live in a `mcData` object in the script:
```javascript
var mcData = {
  mc1: { correct: 'C', fb: 'Correct: C &mdash; Explanation of why C is right and why the distractors fail.' },
  ...
};
```

### Exam Card Pattern

```html
<div class="eq-card">
  <div class="eq-head">
    <span class="eq-type">Short Answer</span>  <!-- or "Extended Response" -->
    <span class="eq-hot">&#9733; HOT</span>    <!-- optional -->
    <span class="eq-marks">3 marks</span>
  </div>
  <div class="eq-stimulus">Scenario text here (optional but preferred for exam realism).</div>
  <div class="eq-q">Question text. (3 marks)</div>
  <div class="eq-body">
    <textarea class="eq-answer-area" placeholder="Write your answer here..."></textarea>
    <button class="eq-reveal-btn" onclick="toggleModel(this)">&#128065; Show Model Answer</button>
    <div class="eq-model">
      <div class="eq-model-head">&#9989; Model Answer</div>
      <div class="eq-model-body">
        <p><strong>Point 1 (1 mark):</strong> ...</p>
        <p><strong>Point 2 (1 mark):</strong> ...</p>
        <p><strong>Point 3 (1 mark):</strong> ...</p>
        <div class="mark-scheme">&#9888; What a student needs to include for full marks / common mistake.</div>
        <!-- OR -->
        <div class="examiner-tip">&#128161; Positive advice on how to maximise marks.</div>
      </div>
    </div>
  </div>
</div>
```

### Quiz Content Guidelines

**MC distractors must be plausible.** Each wrong option should represent a genuine misconception a student might hold — not a silly answer. Good distractors for a debt ratio question:
- Correct: `$20k / $100k = 20%`
- Distractor 1: `$80k / $100k = 80%` (confused equity with debt)
- Distractor 2: `$20k / $80k = 25%` (divided by equity not assets)
- Distractor 3: `$100k / $20k = 500%` (inverted the ratio)

**Mark allocation in model answers must be explicit.** Break every answer into `(1 mark)`, `(2 marks)` etc. blocks so students learn how examiners divide marks. A 3-mark answer should have three clearly labelled points.

**Always include either a `mark-scheme` or `examiner-tip` callout at the end of each exam model answer.** Use:
- `mark-scheme` (amber, warning tone) for common errors that lose marks
- `examiner-tip` (purple, positive tone) for how to maximise marks

**Reuse textbook scenarios verbatim.** If the textbook's exercise 7 is "St Kilda Boat Hire vs Williamstown Boat Hire" with specific numbers, use the same business names and numbers in the quiz. This directly prepares students for the workbook task.

**Every extended response must require evaluation or comparison**, not just recall. A 4+ mark question should require weighing trade-offs, justifying a recommendation, or explaining both sides of a concept (e.g. "gearing is a double-edged sword — explain both").

### Core JS Functions (quiz — always include verbatim)

```javascript
function switchTab(name) {
  var panes = document.querySelectorAll('.tab-pane');
  var btns = document.querySelectorAll('.tab-btn');
  for (var i = 0; i < panes.length; i++) panes[i].className = 'tab-pane';
  for (var i = 0; i < btns.length; i++) btns[i].className = 'tab-btn';
  document.getElementById('tab-' + name).className = 'tab-pane active';
  btns[name === 'mc' ? 0 : 1].className = 'tab-btn active';
}

var totalMC = 15;  // adjust to match actual MC count
var mcAnswered = 0;
var mcCorrect = 0;

function updateScore(gotIt) {
  mcAnswered++;
  if (gotIt) mcCorrect++;
  document.getElementById('score-correct').textContent = mcCorrect;
  document.getElementById('score-total').textContent = mcAnswered;
  document.getElementById('progress-bar').style.width = Math.round((mcAnswered / totalMC) * 100) + '%';
}

function checkMC(el, qid, chosen) {
  var card = document.getElementById(qid);
  if (card.classList.contains('correct') || card.classList.contains('wrong')) return;
  var ans = mcData[qid];
  var correct = (chosen === ans.correct);
  var opts = card.querySelectorAll('.mc-opt');
  var letters = ['A','B','C','D'];
  for (var i = 0; i < opts.length; i++) {
    opts[i].classList.add('disabled');
    if (letters[i] === ans.correct) opts[i].classList.add('reveal-correct');
  }
  el.classList.add(correct ? 'selected-correct' : 'selected-wrong');
  card.classList.add(correct ? 'correct' : 'wrong');
  var fb = document.getElementById('fb-' + qid);
  fb.innerHTML = ans.fb;  // use innerHTML so HTML entities render
  fb.className = 'q-feedback show ' + (correct ? 'correct-fb' : 'wrong-fb');
  updateScore(correct);
}

function toggleModel(btn) {
  var model = btn.nextElementSibling;
  var open = model.classList.toggle('open');
  btn.innerHTML = open ? '&#128065; Hide Model Answer' : '&#128065; Show Model Answer';
}

function resetMC() {
  mcAnswered = 0; mcCorrect = 0;
  document.getElementById('score-correct').textContent = '0';
  document.getElementById('score-total').textContent = '0';
  document.getElementById('progress-bar').style.width = '0%';
  var cards = document.querySelectorAll('.q-card');
  for (var i = 0; i < cards.length; i++) {
    cards[i].classList.remove('correct','wrong');
    var opts = cards[i].querySelectorAll('.mc-opt');
    for (var j = 0; j < opts.length; j++) {
      opts[j].className = 'mc-opt';
      opts[j].onclick = (function(o,id,l){return function(){checkMC(o,id,l);};})(opts[j],cards[i].id,['A','B','C','D'][j]);
    }
    var fbs = cards[i].querySelectorAll('.q-feedback');
    for (var j = 0; j < fbs.length; j++) { fbs[j].className = 'q-feedback'; fbs[j].innerHTML = ''; }
  }
}
```

### Quiz CSS Reference (complete)

```css
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;background:#F5F4F0;color:#1a1a18;font-size:14px;line-height:1.6}
h1{font-size:1.4em;font-weight:700;color:#3C3489;padding:16px 16px 4px}
.subtitle{font-size:0.86em;color:#5F5E5A;padding:0 16px 14px}

/* Tabs */
.tab-bar{display:flex;border-bottom:2px solid #D3D1C7;background:#fff;padding:0 16px;gap:4px}
.tab-btn{padding:10px 18px;border:none;background:none;font-family:inherit;font-size:0.9em;font-weight:600;color:#5F5E5A;cursor:pointer;border-bottom:3px solid transparent;margin-bottom:-2px}
.tab-btn.active{color:#3C3489;border-bottom-color:#3C3489}
.tab-pane{display:none;padding:16px}
.tab-pane.active{display:block}

/* Score bar */
.score-bar{background:#fff;border:1px solid #D3D1C7;border-radius:8px;padding:12px 16px;margin-bottom:16px;display:flex;align-items:center;gap:16px;flex-wrap:wrap}
.score-text{font-size:0.86em}
.score-text strong{color:#3C3489;font-size:1.1em}
.progress-track{flex:1;min-width:100px;height:8px;background:#E5E3DC;border-radius:4px;overflow:hidden}
.progress-bar{height:100%;background:#7F77DD;border-radius:4px;width:0%;transition:width .4s}
.reset-btn{background:#fff;border:1px solid #D3D1C7;padding:6px 14px;border-radius:6px;cursor:pointer;font-size:0.82em}

/* Question cards */
.q-section-head{background:#3C3489;color:#fff;padding:8px 14px;border-radius:6px;margin:18px 0 10px;font-size:0.88em;font-weight:700}
.q-card{background:#fff;border:1px solid #D3D1C7;border-radius:8px;padding:16px;margin-bottom:12px}
.q-card.correct{border-color:#1D9E75;background:#F0FBF6}
.q-card.wrong{border-color:#D85A30;background:#FDF3EF}
.q-meta{display:flex;align-items:center;gap:8px;margin-bottom:8px;flex-wrap:wrap}
.q-num{font-size:0.79em;font-weight:700;color:#5F5E5A;text-transform:uppercase;letter-spacing:.3px}
.q-hot{background:#E24B4A;color:#fff;font-size:0.71em;font-weight:700;border-radius:4px;padding:1px 6px}
.q-marks{background:#EEEDFE;color:#3C3489;font-size:0.71em;font-weight:700;border-radius:4px;padding:1px 6px}
.q-text{font-size:0.93em;font-weight:600;margin-bottom:12px}

/* MC options */
.mc-options{display:flex;flex-direction:column;gap:7px}
.mc-opt{display:flex;align-items:flex-start;gap:10px;padding:9px 12px;border:1px solid #D3D1C7;border-radius:6px;cursor:pointer;font-size:0.86em;transition:background .15s}
.mc-opt:hover{background:#F5F4F0}
.mc-opt.selected-correct{background:#E1F5EE;border-color:#1D9E75;font-weight:600;color:#085041}
.mc-opt.selected-wrong{background:#FAECE7;border-color:#D85A30;color:#4A1B0C}
.mc-opt.reveal-correct{background:#E1F5EE;border-color:#1D9E75}
.mc-opt.disabled{cursor:default;pointer-events:none}
.opt-letter{font-weight:700;color:#3C3489;min-width:16px;flex-shrink:0}

/* Feedback */
.q-feedback{display:none;margin-top:10px;padding:10px 12px;border-radius:6px;font-size:0.82em;line-height:1.6}
.q-feedback.show{display:block}
.q-feedback.correct-fb{background:#E1F5EE;border-left:3px solid #1D9E75;color:#085041}
.q-feedback.wrong-fb{background:#FAECE7;border-left:3px solid #D85A30;color:#4A1B0C}

/* Exam practice tab */
.eq-card{background:#fff;border:1px solid #D3D1C7;border-radius:8px;margin-bottom:16px;overflow:hidden}
.eq-head{background:#F5F4F0;padding:10px 14px;display:flex;align-items:center;gap:10px;flex-wrap:wrap;border-bottom:1px solid #D3D1C7}
.eq-type{background:#3C3489;color:#fff;font-size:0.75em;font-weight:700;border-radius:4px;padding:2px 9px}
.eq-marks{background:#EEEDFE;color:#3C3489;font-size:0.75em;font-weight:700;border-radius:4px;padding:2px 9px}
.eq-hot{background:#E24B4A;color:#fff;font-size:0.75em;font-weight:700;border-radius:4px;padding:2px 9px}
.eq-stimulus{background:#EEEDFE;border-left:3px solid #3C3489;padding:10px 14px;margin:12px 14px 0;font-size:0.86em;border-radius:0 6px 6px 0}
.eq-q{padding:12px 14px 4px;font-weight:600;font-size:0.93em}
.eq-body{padding:10px 14px 14px}
.eq-answer-area{width:100%;min-height:80px;border:1px solid #D3D1C7;border-radius:6px;padding:9px;font-family:inherit;font-size:0.86em;resize:vertical;background:#fff}
.eq-reveal-btn{margin-top:9px;background:#fff;border:1px solid #3C3489;color:#3C3489;padding:7px 14px;border-radius:6px;cursor:pointer;font-size:0.82em;font-weight:600}
.eq-reveal-btn:hover{background:#3C3489;color:#fff}
.eq-model{display:none;margin-top:10px;border:1px solid #D3D1C7;border-radius:6px;overflow:hidden}
.eq-model.open{display:block}
.eq-model-head{background:#EEEDFE;padding:8px 12px;font-weight:700;color:#3C3489;font-size:0.86em}
.eq-model-body{padding:10px 14px;font-size:0.86em;line-height:1.7}
.eq-model-body p{margin-bottom:6px}
.mark-scheme{background:#FAEEDA;border-left:3px solid #BA7517;padding:8px 12px;margin-top:8px;font-size:0.82em;border-radius:0 4px 4px 0;color:#412402;font-style:italic}
.examiner-tip{background:#EEEDFE;border-left:3px solid #7F77DD;padding:8px 12px;margin-top:8px;font-size:0.82em;border-radius:0 4px 4px 0;color:#26215C}

.footer{text-align:center;font-size:0.79em;color:#888780;margin-top:28px;padding:12px 16px 24px;border-top:1px solid #D3D1C7}
```

### Quiz Workflow

1. **Read** the chapter's end-of-chapter exercises (user will provide images or text)
2. **Build a coverage table** mapping each textbook exercise to a topic
3. **Propose** the MC section split (e.g. 3 sections matching section headings) and exam question scenarios to use — confirm with user
4. **Confirm** quiz colour theme (usually matches the cheat sheet's hot-topic colour or the chapter's textbook colour)
5. **Build** the complete quiz HTML file
6. **Present** with a summary of what's covered vs the textbook exercises

---

## Prompt to activate this skill in a new conversation

Paste the following at the start of a new chat, followed by this skill document:

> "I am creating interactive HTML cheat sheets for VCE Accounting Units 1 & 2 using the Neville Box 7th edition textbook. Please use the attached skill document to generate each chapter. I will give you the chapter number, title and section headings. You should identify hot topics, suggest appropriate visual panels, and produce a complete downloadable HTML file following all the rules and patterns in the skill. After each chapter cheat sheet is complete, you should also offer to build a matching chapter quiz (multiple choice + exam practice) cross-referenced against the textbook's end-of-chapter exercises."
