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
<!-- Visual panels (optional, collapsible) -->
<!-- Terms accordion -->
<div id="list"></div>
<p class="footer">...</p>
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
| .box-wrap.green | Cash receipts journals, positive visuals |
| .box-wrap.red | Cash payments journals |
| .box-wrap.purple | Comparison tables |
| .box-wrap.amber | Formula cards |
| .box-wrap.teal | Statements, general worked examples |
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

### 7. Balance sheet visual
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

---

## Workflow for New Chapters

When given a new chapter, follow this process:

1. **Ask** (if not already provided): chapter number, title, section headings (x.1, x.2 etc.)
2. **Identify** which sections are hot topics based on VCE exam history
3. **Decide** which visual panels would help (journals, comparison tables, formula cards, balance sheet)
4. **Confirm** with the user before building if unsure about visuals
5. **Build** the complete HTML file using this skill
6. **Remind** the user to download as `.html` (not `.tsx`)

---

## Prompt to activate this skill in a new conversation

Paste the following at the start of a new chat, followed by this skill document:

> "I am creating interactive HTML cheat sheets for VCE Accounting Units 1 & 2 using the Neville Box 7th edition textbook. Please use the attached skill document to generate each chapter. I will give you the chapter number, title and section headings. You should identify hot topics, suggest appropriate visual panels, and produce a complete downloadable HTML file following all the rules and patterns in the skill."
