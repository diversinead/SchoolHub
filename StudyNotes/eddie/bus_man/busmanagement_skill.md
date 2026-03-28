# Skill: VCE Business Management Cheat Sheet Generator

## Purpose
Generate interactive HTML cheat sheets for VCE Business Management Units 3 & 4
using the Jacaranda Key Concepts 7th edition (Chapman, Phelan, Richardson, Rabenda, Smithies).
Each topic becomes a standalone `.html` file students can open in any browser.

---

## Key Difference from Accounting Skill

Business Management is NOT primarily a definitions subject.
The VCE exam tests students on:
- **Applying** concepts to unseen business case studies
- **Comparing** strategies, styles and approaches
- **Evaluating** effectiveness with justified recommendations
- **Discussing** advantages and disadvantages
- **Constructing** structured written responses using command terms

Therefore cheat sheets must include MORE than just term definitions. Every topic needs:
1. Key terms with plain English definitions (accordion — same as Accounting)
2. Advantages / disadvantages panels for every strategy or approach
3. Comparison tables where concepts are commonly compared in exams
4. Model answer structures for common exam question types
5. Command term guidance (define vs explain vs discuss vs evaluate vs justify)

---

## Book Structure

**Unit 3 — Managing a Business**
| Topic | Title | Area of Study |
|-------|-------|---------------|
| Topic 1 | Business Foundations | AOS 1 |
| Topic 2 | Human Resource Management | AOS 2 |
| Topic 3 | Operations Management | AOS 3 |

**Unit 4 — Transforming a Business**
| Topic | Title | Area of Study |
|-------|-------|---------------|
| Topic 4 | Reviewing Performance — the Need for Change | AOS 1 |
| Topic 5 | Implementing Change | AOS 2 |

Each topic has numbered subtopics (e.g. 1.2, 1.3) rather than chapters.

---

## HTML Output Rules

### File format
- Always output `text/html` artifact type — NEVER React/TSX
- Single self-contained file: all CSS and JS inline, no external dependencies
- Must download as `.html` from Claude artifact panel

### JavaScript rules (critical)
- Always use `var` — never `const` or `let`
- Never use template literals (backticks) — use string concatenation only
- Never use arrow functions — use `function` keyword or IIFE
- Use HTML entities for special characters:
  - `&#9660;` (▼), `&#9650;` (▲), `&#9658;` (▶)
  - `&#9733;` (★), `&#9888;` (⚠), `&#128161;` (💡), `&#10003;` (✓)
  - `&#43;` (+), `&#8722;` (−)
- Avoid apostrophes inside JS strings — rephrase or use HTML entity

### CSS rules
- No CSS variables — hardcoded hex values only
- No `position: absolute` tooltips inside `overflow: hidden` containers
- Hot badge tooltips: `position: absolute; top: calc(100% + 6px)` — always drops DOWN

---

## Visual Design System

### Colour palette for accordion sections
Same system as Accounting skill:
| Class | Use for |
|-------|---------|
| purple | Intro/overview/foundations sections |
| teal | People management, positive strategies |
| coral | Risk, termination, negative concepts |
| amber | Operations, calculations, processes |
| blue | Change management, KPIs, performance |
| pink | Ethics, CSR, evaluation sections |
| gray | Definitions, principles, key terms |

### Collapsible panel colours
| Class | Use for |
|-------|---------|
| .box-wrap.green | Advantages lists, positive outcomes |
| .box-wrap.red | Disadvantages lists, risks |
| .box-wrap.purple | Comparison tables |
| .box-wrap.amber | Model answer structures, formulas |
| .box-wrap.blue | KPI tables, performance data |
| .box-wrap.teal | General worked examples, case study panels |

---

## Component Patterns

### 1. Terms accordion (same as Accounting skill)
```javascript
var data = [
  { cat: "1.2 Types of Businesses", color: "purple", hot: false, items: [
    { term: "Sole trader", def: "A business owned and operated by one person.", eg: "A local plumber who runs their own ABN." },
    { term: "Partnership", def: "A business owned by 2 or more people sharing profits and losses.", eg: "Two lawyers who open a firm together.", note: "Optional exam tip here." }
  ]}
];
```

### 2. Advantages / Disadvantages panel
This is unique to Business Management — used for every strategy, style or approach.
```html
<div style="display:grid;grid-template-columns:1fr 1fr;gap:12px;padding:12px;background:#fff;">
  <div style="background:#E1F5EE;border:1px solid #5DCAA5;border-radius:8px;padding:12px;">
    <h3 style="font-size:13px;font-weight:600;color:#085041;margin-bottom:8px;">&#43; Advantages</h3>
    <ul style="font-size:12px;color:#085041;line-height:1.8;padding-left:16px;">
      <li>Advantage one — brief explanation</li>
      <li>Advantage two — brief explanation</li>
      <li>Advantage three — brief explanation</li>
    </ul>
  </div>
  <div style="background:#FAECE7;border:1px solid #D85A30;border-radius:8px;padding:12px;">
    <h3 style="font-size:13px;font-weight:600;color:#4A1B0C;margin-bottom:8px;">&#8722; Disadvantages</h3>
    <ul style="font-size:12px;color:#4A1B0C;line-height:1.8;padding-left:16px;">
      <li>Disadvantage one — brief explanation</li>
      <li>Disadvantage two — brief explanation</li>
      <li>Disadvantage three — brief explanation</li>
    </ul>
  </div>
</div>
```
Wrap this in a collapsible `.box-wrap.purple` panel with a title like "Autocratic style — advantages vs disadvantages".

### 3. Comparison table
Used when two or more concepts are commonly compared in exams.
```html
<div class="box-wrap purple">
  <div class="box-toggle" onclick="toggleB(this)">
    <span>&#128202; Management Styles — comparison</span>
    <span class="cat-arrow">&#9660;</span>
  </div>
  <div class="box-body">
    <div style="overflow-x:auto;">
      <table class="ct">
        <thead><tr>
          <th>Feature</th><th>Autocratic</th><th>Persuasive</th><th>Consultative</th><th>Participative</th><th>Laissez-faire</th>
        </tr></thead>
        <tbody>
          <tr><td><strong>Decision making</strong></td><td>Manager only</td><td>Manager decides, explains why</td><td>Seeks input, manager decides</td><td>Group decides together</td><td>Staff decide independently</td></tr>
          <tr><td><strong>Best used when</strong></td><td>Crisis, unskilled staff</td><td>Staff need motivation</td><td>Experienced team</td><td>Highly skilled staff</td><td>Expert professionals</td></tr>
        </tbody>
      </table>
    </div>
    <p class="box-note">&#128161; Exams ask you to justify which style suits a given situation — always link to the scenario.</p>
  </div>
</div>
```

### 4. Model answer structure panel
Unique to Business Management — shows students how to structure exam responses.
```html
<div class="box-wrap amber">
  <div class="box-toggle" onclick="toggleB(this)">
    <span>&#128221; Model answer structure — discuss/evaluate questions</span>
    <span class="cat-arrow">&#9660;</span>
  </div>
  <div class="box-body">
    <div style="padding:12px;background:#fff;">
      <div style="background:#FAEEDA;border-left:4px solid #BA7517;border-radius:0 8px 8px 0;padding:10px 12px;margin-bottom:10px;">
        <p style="font-size:12px;font-weight:600;color:#412402;margin-bottom:4px;">Question: Discuss the use of on-the-job training at Acme Co. (4 marks)</p>
      </div>
      <div style="font-size:12px;line-height:1.8;color:#333;">
        <p><strong>Step 1 — Define:</strong> On-the-job training involves employees learning skills while performing their actual work duties, guided by an experienced colleague.</p>
        <p style="margin-top:6px;"><strong>Step 2 — Advantage + link to scenario:</strong> This approach allows Acme Co. employees to develop practical, job-specific skills immediately relevant to their role, reducing the time before they become productive.</p>
        <p style="margin-top:6px;"><strong>Step 3 — Disadvantage + link to scenario:</strong> However, the quality of training depends on the trainer's skills and availability, which may limit consistency across Acme Co.'s workforce.</p>
        <p style="margin-top:6px;"><strong>Step 4 — Conclusion (for evaluate/justify):</strong> Overall, on-the-job training is suitable for Acme Co. because... [link to case study detail].</p>
      </div>
    </div>
    <p class="box-note">&#128161; Always link back to the business in the case study — generic answers lose marks.</p>
  </div>
</div>
```

### 5. Command terms reference panel
Include in every cheat sheet — critical for exam technique.
```html
<div class="box-wrap blue">
  <div class="box-toggle" onclick="toggleB(this)">
    <span>&#128270; Command terms — what each word requires</span>
    <span class="cat-arrow">&#9660;</span>
  </div>
  <div class="box-body">
    <div style="overflow-x:auto;">
      <table class="ct">
        <thead><tr><th>Command term</th><th>What it means</th><th>Marks typically</th></tr></thead>
        <tbody>
          <tr><td><strong>Define</strong></td><td>State the precise meaning of a term</td><td>1-2</td></tr>
          <tr><td><strong>Describe</strong></td><td>Give a detailed account of characteristics or features</td><td>2-3</td></tr>
          <tr><td><strong>Explain</strong></td><td>Make clear how or why — give reasons</td><td>2-4</td></tr>
          <tr><td><strong>Discuss</strong></td><td>Give both sides — advantages AND disadvantages</td><td>4-6</td></tr>
          <tr><td><strong>Evaluate</strong></td><td>Discuss both sides AND make a judgement with justification</td><td>6-10</td></tr>
          <tr><td><strong>Justify</strong></td><td>Give reasons that support a decision or recommendation</td><td>3-6</td></tr>
          <tr><td><strong>Compare</strong></td><td>Show similarities AND differences between two things</td><td>3-6</td></tr>
          <tr><td><strong>Propose</strong></td><td>Put forward a strategy or solution with reasons</td><td>3-5</td></tr>
        </tbody>
      </table>
    </div>
    <p class="box-note">&#128161; Discuss = both sides. Evaluate = both sides + judgement. These are the most common exam mistakes.</p>
  </div>
</div>
```

### 6. Hot topic badge (identical to Accounting skill)
```html
<span class="hot-badge">&#9733; HOT TOPIC
  <span class="tip">High-frequency exam topic — appears in almost every exam</span>
</span>
```

---

## Core JS Functions (always include verbatim)

Identical to Accounting skill — use the same `build()`, `toggle()`, `filterTerms()` and `toggleB()` functions. See Accounting skill for full code.

---

## Content Guidelines

### Definitions
- Plain English — one or two sentences
- Always include what it IS, not just what it does
- Avoid apostrophes in JS strings

### Examples
- Always use real or realistic Australian business scenarios
- Reference well-known Australian businesses where appropriate:
  - Manufacturing: Toyota, Qantas, Bega Cheese
  - Service: Commonwealth Bank, Medibank, Linfox
  - Retail: Woolworths, JB Hi-Fi, Bunnings
  - Small business: local cafe, boutique retailer, trades business

### Advantages / Disadvantages
- Always 3 advantages and 3 disadvantages minimum
- Each point must be one sentence that includes a brief explanation of WHY it is an advantage/disadvantage
- Never just a single word (e.g. "Costly" is wrong — "High implementation costs can reduce profitability" is correct)

### Model answer structures
- Include for any concept that is commonly asked as a "discuss" or "evaluate" question
- Always show the Define → Advantage → Disadvantage → Conclusion structure
- Use a fictional but realistic business (e.g. "Acme Manufacturing", "Metro Cafe")

### Exam tips (note field)
- Focus on common exam mistakes for this subject:
  - "Always link your answer back to the business in the case study"
  - "Discuss requires BOTH advantages and disadvantages — not just one side"
  - "Evaluate requires a conclusion/judgement — not just discussion"
  - "Define the term before discussing it, even if not explicitly asked"

---

## Hot Topics by Topic (confirmed high-frequency exam areas)

| Topic | Hot subtopics |
|-------|--------------|
| Topic 1 | Management styles, Management skills, Corporate culture, Stakeholders |
| Topic 2 | Motivation theories (Maslow, Locke, Lawrence & Nohria), Training types, Performance management, Termination |
| Topic 3 | Operations strategies, Quality management, Technology & automation, CSR in operations |
| Topic 4 | Key Performance Indicators (KPIs), Forces for change, SWOT analysis |
| Topic 5 | Leadership styles (Lewin), Strategies to overcome resistance, Kotter 8-step model, Learning organisation |

---

## Recommended Panel Structure per Topic

When building each topic, always include these panels in this order:
1. **Command terms panel** (blue) — include in every topic
2. **Key terms accordion** — all subtopic definitions
3. **Advantages/Disadvantages panels** — for every strategy, style or approach in the topic
4. **Comparison table** — where multiple similar concepts exist (e.g. management styles)
5. **Model answer structure** — for the most likely "discuss/evaluate" exam question in the topic

---

## Workflow for New Topics

When given a new topic, follow this process:

1. **Ask** (if not provided): topic number, title, subtopic list (e.g. 1.2, 1.3...)
2. **Identify** hot subtopics based on exam history above
3. **Plan** which panels are needed:
   - Are there multiple styles/strategies to compare? → comparison table
   - Are there strategies with pros/cons? → adv/disadv panels
   - Is there a likely discuss/evaluate question? → model answer panel
4. **Confirm** panel plan with user before building
5. **Build** complete HTML using this skill and the Accounting skill's core JS/CSS
6. **Remind** user to download as `.html`

---

## Prompt to activate this skill in a new conversation

Paste the following at the start of a new chat, followed by this skill document AND the Accounting skill document (for shared CSS/JS patterns):

> "I am creating interactive HTML cheat sheets for VCE Business Management Units 3 & 4 using the Jacaranda Key Concepts 7th edition textbook. Please use the attached skill document to generate each topic. I will give you the topic number, title and subtopic headings. You should identify hot topics, suggest appropriate visual panels (comparison tables, advantages/disadvantages, model answer structures), and produce a complete downloadable HTML file following all the rules and patterns in the skill. Always use the core JS/CSS from the Accounting skill for consistency."
