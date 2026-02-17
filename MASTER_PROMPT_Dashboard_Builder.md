# MASTER PROMPT TEMPLATE: Build a Standalone Interactive Web Dashboard

> **HOW TO USE THIS TEMPLATE:** Copy everything below the line. Replace all `[BRACKETED PLACEHOLDERS]` with your specific topic, domain, data, and requirements. Delete any sections that don't apply. The design system, technical specs, and quality standards are pre-set to our established style — just fill in the **what** and the prompt handles the **how**.

---

# BUILD PROMPT: [YOUR DASHBOARD TITLE]

---

## WHO YOU ARE

You are the world's foremost expert in **[PRIMARY DOMAIN — e.g., quantitative risk modeling, real estate analytics, workforce transformation strategy, financial engineering, etc.]** combined with elite-tier frontend engineering and interactive data visualization. You have the strategic depth of a senior partner at a top-tier consulting firm, the quantitative rigor of a Goldman Sachs analyst, and the design sensibility of a Bloomberg Terminal architect.

You understand how **[TARGET USER — e.g., senior executives, portfolio managers, risk analysts, investors, traders]** actually make decisions: they need clarity over complexity, actionable levers over abstract charts, and real numbers attached to every insight.

---

## WHAT YOU'RE BUILDING

A **standalone, single-file web application** (`HTML + CSS + JS` — no backend, no server, no external APIs required) that serves as a **comprehensive, interactive [DASHBOARD TYPE — e.g., analytics platform, planning tool, intelligence dashboard, command center, decision engine]** for **[PURPOSE — 1-2 sentences describing what this tool does and why it exists]**.

This tool allows the user to:

1. **[CORE CAPABILITY 1 — e.g., "Map their entire organizational workforce against AI displacement risk"]**
2. **[CORE CAPABILITY 2 — e.g., "Model cost savings, productivity gains, and implementation timelines"]**
3. **[CORE CAPABILITY 3 — e.g., "Run stress-test scenarios with adjustable parameters"]**
4. **[CORE CAPABILITY 4 — e.g., "Generate exportable reports and board-ready outputs"]**
5. **[CORE CAPABILITY 5 — add/remove as needed]**

**This is NOT a toy.** This is not a dashboard with three charts and placeholder text. This is a **comprehensive, production-grade, interactive platform** that a **[TARGET USER DESCRIPTION — e.g., "senior market risk analyst managing 300,000+ risk drivers across 19 trading desks at a major bank"]** would actually open and use to make real decisions.

---

## TECHNICAL REQUIREMENTS

### Stack & Architecture
- **Single HTML file** with all CSS and JavaScript embedded inline — zero external dependencies beyond CDN-loaded libraries
- **CDN libraries allowed:** Chart.js, D3.js, Plotly.js, html2canvas, jsPDF (for export), Papa Parse (for CSV), SheetJS (for Excel), math.js, Three.js (only if 3D visualizations are justified)
- Must work **completely offline** after initial CDN load — users will access this in confidential settings, boardrooms, flights, and air-gapped environments
- **All computation runs client-side** — no API calls, no fetch requests, no external data
- All data is **realistic, hardcoded mock data** that demonstrates every feature as if the real product existed today
- **Responsive** but optimized for large screens (13"+ laptops, external monitors, projection screens)
- **Print/export ready** — every view should be cleanly exportable as PDF or PNG
- **Performance:** Smooth 60fps interactions, lazy-render off-screen sections, handle large datasets without jank

### Code Quality
- Clean, well-commented, modular JavaScript
- CSS variables for the entire design system (colors, spacing, typography, shadows, borders)
- Semantic HTML structure
- Accessible: proper ARIA labels, keyboard navigation, focus states
- No inline styles — everything via CSS classes and variables

---

## DESIGN SYSTEM — THE VISUAL DNA (NON-NEGOTIABLE)

This is the aesthetic standard. Every dashboard built from this prompt must adhere to this system precisely. The vibe is: **Bloomberg Terminal meets institutional-grade analytics meets dark luxury.**

### Color Palette (CSS Variables)

```css
:root {
  /* === BACKGROUNDS === */
  --bg-primary: #0B0F19;           /* Deep navy-black — main page background */
  --bg-secondary: #111827;         /* Slightly lighter — card/panel backgrounds */
  --bg-tertiary: #1A2236;          /* Tertiary surface — hover states, secondary panels */
  --bg-input: #0D1321;             /* Input fields, text areas */
  --bg-overlay: rgba(0, 0, 0, 0.6); /* Modal/overlay backdrop */

  /* === BORDERS & DIVIDERS === */
  --border-primary: #1E293B;       /* Subtle card borders */
  --border-hover: #334155;         /* Border on hover */
  --border-active: var(--accent);  /* Active/focused element borders */

  /* === TEXT === */
  --text-primary: #E2E8F0;        /* Main body text — crisp off-white */
  --text-secondary: #94A3B8;      /* Muted/secondary text */
  --text-dim: #64748B;            /* Tertiary/disabled text */
  --text-inverse: #0B0F19;        /* Text on light/accent backgrounds */

  /* === ACCENT COLORS === */
  --accent: #3B82F6;              /* Primary accent — electric blue (links, active tabs, key highlights) */
  --accent-glow: rgba(59, 130, 246, 0.15); /* Subtle glow behind accent elements */
  --accent-secondary: #8B5CF6;    /* Secondary accent — violet (optional differentiation) */

  /* === DATA / SEMANTIC COLORS === */
  --green: #10B981;               /* Positive values, success, growth, low risk */
  --green-dim: rgba(16, 185, 129, 0.15);
  --red: #EF4444;                 /* Negative values, danger, loss, high risk */
  --red-dim: rgba(239, 68, 68, 0.15);
  --amber: #F59E0B;               /* Warning, medium risk, caution, neutral change */
  --amber-dim: rgba(245, 158, 11, 0.15);
  --cyan: #06B6D4;                /* Informational, secondary data points */
  --rose: #F43F5E;                /* Emphasis, tags, breaking/critical labels */

  /* === SHADOWS & DEPTH === */
  --shadow-sm: 0 1px 2px rgba(0, 0, 0, 0.3);
  --shadow-md: 0 4px 12px rgba(0, 0, 0, 0.4);
  --shadow-lg: 0 8px 32px rgba(0, 0, 0, 0.5);
  --shadow-glow: 0 0 20px var(--accent-glow);

  /* === SPACING SCALE === */
  --space-xs: 4px;
  --space-sm: 8px;
  --space-md: 16px;
  --space-lg: 24px;
  --space-xl: 32px;
  --space-2xl: 48px;

  /* === BORDER RADIUS === */
  --radius-sm: 6px;
  --radius-md: 10px;
  --radius-lg: 16px;
  --radius-pill: 999px;

  /* === TRANSITIONS === */
  --transition-fast: 150ms ease;
  --transition-base: 250ms ease;
  --transition-slow: 400ms ease;
}
```

### Typography

```css
/* IMPORT THESE — no exceptions */
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@300;400;500;600;700&family=IBM+Plex+Mono:wght@400;500;600&family=DM+Serif+Display&display=swap');

/* NEVER use Inter, Arial, Roboto, Helvetica, or system-ui as primary fonts */

--font-heading: 'DM Serif Display', serif;          /* Hero headlines, page titles */
--font-body: 'IBM Plex Sans', sans-serif;            /* Body text, labels, UI elements */
--font-mono: 'IBM Plex Mono', monospace;             /* Data values, code, metric numbers, tables */
```

**Typography Scale:**
- Hero title: 36-48px, `DM Serif Display`, gradient or off-white
- Page/section titles: 24-28px, `IBM Plex Sans` 600-700 weight
- Card titles: 16-18px, `IBM Plex Sans` 600 weight
- Body text: 14-15px, `IBM Plex Sans` 400 weight, `--text-secondary`
- Data values/metrics: 20-32px, `IBM Plex Mono` 600 weight
- Labels/captions: 10-12px, `IBM Plex Mono` 500 weight, uppercase, letter-spacing: 0.05-0.1em, `--text-dim`
- Table data: 13px, `IBM Plex Mono` 400 weight

### Component Library

Build these reusable component patterns into the CSS:

**1. Cards**
```
Background: var(--bg-secondary)
Border: 1px solid var(--border-primary)
Border-radius: var(--radius-md)
Padding: var(--space-lg)
Hover: border-color transitions to var(--border-hover), subtle translateY(-1px)
Variants:
  .card-highlight → left border 3px solid var(--accent), bg slightly tinted
  .card-success → left border 3px solid var(--green)
  .card-danger → left border 3px solid var(--red)
  .card-warning → left border 3px solid var(--amber)
```

**2. Metric Cards**
```
Small card with:
  - Label: uppercase monospace caption at top (--text-dim)
  - Value: large monospace number (--text-primary)
  - Delta/change indicator: small text below, color-coded green/red/amber with ▲/▼ arrows
  - Optional sparkline or mini bar
```

**3. Tables**
```
Font: IBM Plex Mono throughout
Header row: uppercase, 11px, letter-spacing, --text-dim, border-bottom 1px
Data rows: 13px, alternating row backgrounds (--bg-secondary / transparent)
Hover: row background shifts to --bg-tertiary
Alignment: text-left for labels, text-right for numbers
Color-code positive/negative values inline
```

**4. Tabs/Navigation**
```
Tab bar: flex row, gap 0, border-bottom 1px solid var(--border-primary)
Tab button: padding 12px 20px, IBM Plex Sans 500, --text-dim
Active tab: --text-primary or --accent color, border-bottom 2px solid var(--accent)
Transition: color and border 250ms ease
```

**5. Sidebar (if applicable)**
```
Width: 240-280px fixed
Background: --bg-primary or slightly darker
Border-right: 1px solid var(--border-primary)
Nav items: padding 10px 16px, hover background --bg-tertiary, active left-border accent
Collapsible on smaller screens
```

**6. Section Labels**
```
IBM Plex Mono, 10-11px, uppercase, letter-spacing 0.1em
Color: var(--accent) or var(--rose)
Optional: ::after pseudo-element with gradient line extending to the right
Margin-bottom: var(--space-sm)
```

**7. Buttons**
```
Primary: bg var(--accent), text white, radius-sm, 14px IBM Plex Sans 500
Hover: slightly brighter, subtle box-shadow glow
Secondary: bg transparent, border 1px var(--border-primary), text --text-secondary
Hover: border-color --accent, text --accent
Sizes: sm (28px height), md (36px), lg (44px)
```

**8. Input Fields**
```
Background: var(--bg-input)
Border: 1px solid var(--border-primary)
Border-radius: var(--radius-sm)
Font: IBM Plex Sans for text inputs, IBM Plex Mono for number inputs
Focus: border-color var(--accent), box-shadow var(--shadow-glow)
```

**9. Charts & Visualizations**
```
Background: transparent or var(--bg-secondary) for chart container cards
Grid lines: rgba(255,255,255,0.05) — barely visible
Axis labels: IBM Plex Mono, 11px, --text-dim
Data colors: cycle through --accent, --cyan, --green, --amber, --rose, --accent-secondary
Tooltips: --bg-tertiary background, white text, radius-sm, shadow-md
```

**10. Status Indicators / Badges**
```
Small pills: padding 4px 10px, radius-pill, font 11px IBM Plex Mono 500 uppercase
Variants by color: each has tinted background + matching text
  Success: bg var(--green-dim), text var(--green)
  Danger: bg var(--red-dim), text var(--red)
  Warning: bg var(--amber-dim), text var(--amber)
  Info: bg var(--accent-glow), text var(--accent)
```

### Atmospheric Effects

Apply these to give the dashboard depth and polish:

- **Noise texture overlay:** Subtle SVG noise pattern, fixed position, full viewport, pointer-events: none, opacity 0.02-0.04
- **Staggered fade-in animations:** Sections/cards animate in on load — opacity 0→1, translateY(8-12px)→0, with increasing `animation-delay` per element (0.05-0.1s stagger)
- **Gradient accents:** Use linear-gradient on hero titles (text), key stat backgrounds, and section dividers
- **Subtle glassmorphism (sparingly):** backdrop-filter: blur(10px) on header/sidebar if layered over content
- **Scrollbar styling:** Thin (6px), dark track, slightly lighter thumb, rounded

---

## DASHBOARD STRUCTURE

> **INSTRUCTIONS:** Define every tab/page/section of your dashboard below. Be as specific as possible about what data, charts, tables, calculators, and interactions belong in each section. The more detail you give, the better the output.

### LAYOUT

- **[Choose one: Sidebar + Content | Top Tabs + Content | Multi-page with Header Nav]**
- **Header:** App title on left, status indicators or metadata on right (date, version, user context)
- **Navigation:** [Describe nav structure — list every tab/page name]
- **Footer (optional):** Disclaimer, version, attribution

---

### TAB 1: [TAB NAME — e.g., "Executive Overview"]

**Purpose:** [What does this tab show? What decision does it support?]

**Components:**

#### 1A. [Component Name — e.g., "KPI Summary Bar"]
- [Describe: what metrics, how displayed, what data]
- [Layout: grid of N metric cards across top]
- [Interactivity: click to drill down? filter? hover tooltips?]

#### 1B. [Component Name — e.g., "Risk Heatmap"]
- [Describe: rows, columns, color coding logic, data source]
- [Interactivity: click cells for detail, sort columns, filter rows]

#### 1C. [Component Name — e.g., "Trend Chart"]
- [Chart type: line, bar, area, scatter, candlestick, etc.]
- [Data: what series, what time range, what axes]
- [Interactivity: hover tooltips, toggle series, zoom, time range selector]

*[Add as many sub-components as needed per tab]*

---

### TAB 2: [TAB NAME]

**Purpose:** [...]

**Components:**

#### 2A. [Component Name]
- [...]

#### 2B. [Component Name]
- [...]

*[Repeat for all tabs...]*

---

### TAB N: [FINAL TAB — e.g., "Reference / Methodology / Help"]

**Purpose:** Embedded documentation, methodology explanations, formulas, glossary, and user guide.

**Components:**
- Navigable knowledge base with expandable sections
- Formula displays (use styled code blocks or KaTeX-style rendering)
- Glossary with search/filter
- "How to use this tool" walkthrough

---

## MOCK DATA REQUIREMENTS

**All data must be realistic and internally consistent.** This is a prototype — the mock data IS the demo. Bad data breaks the illusion.

- **[Describe your data domain — e.g., "Financial data: generate realistic stock prices, interest rates, VaR figures, P&L numbers that move together logically"]**
- **[Scale — e.g., "At least 50 rows in main tables, 12+ months of time series, 5-10 categories/segments"]**
- **[Consistency — e.g., "Portfolio allocations must sum to 100%, P&L must reconcile with position sizes × price moves"]**
- **[Variety — e.g., "Include both positive and negative scenarios, outliers, different magnitudes"]**
- Use realistic entity names, dates, and values — no "Lorem ipsum" or "Company A/B/C" unless explicitly a template
- Time series data should show realistic patterns (trends, seasonality, mean-reversion, occasional spikes)

---

## INTERACTIVITY REQUIREMENTS

Every dashboard must include these interaction patterns where applicable:

1. **All navigation is functional** — every tab, sidebar link, and button does something
2. **Hover tooltips** on all charts and data-dense elements
3. **Click to drill down** — tables/cards that expand to show detail views
4. **Interactive calculators** — sliders, inputs, dropdowns that recompute results in real-time
5. **Sorting and filtering** — tables must be sortable by any column, filterable by key dimensions
6. **Search** — if there are 20+ items in any list, include a search/filter box
7. **Toggle/switch** — show/hide data series, switch between views (e.g., table vs. chart, absolute vs. percentage)
8. **State persistence** — active tab, filter selections, and input values should persist during the session
9. **Smooth transitions** — all state changes (tab switches, panel opens, data updates) should animate smoothly
10. **Export buttons** — "Export PDF" and/or "Copy to Clipboard" where appropriate

---

## QUALITY STANDARDS — THE ACID TEST

Before delivering, verify the dashboard passes ALL of these:

- [ ] **Opens in any modern browser** with zero errors in console
- [ ] **Every tab/page is navigable** and displays content (no empty states, no "coming soon")
- [ ] **Every chart renders** with proper data, axes, labels, and tooltips
- [ ] **Every table has data** that is realistic and properly formatted (commas in numbers, 2 decimal places for currency, %, bps)
- [ ] **Every interactive element works** — sliders slide, buttons click, dropdowns open, inputs calculate
- [ ] **Color coding is consistent** — green/red/amber mean the same thing everywhere
- [ ] **Typography hierarchy is clear** — you can scan the page and understand the information architecture in 5 seconds
- [ ] **No visual bugs** — no overflows, no text truncation, no misaligned grids, no janky animations
- [ ] **Looks stunning on a 15" laptop screen** — this is the primary viewport
- [ ] **The mock data tells a coherent story** — a domain expert would look at this and say "this data makes sense"
- [ ] **A non-technical executive** could open this, navigate it, and extract insights without any training
- [ ] **A domain expert** would find the depth, methodology, and analytical rigor credible and useful

---

## PRIORITY ORDER FOR BUILDING

If the full scope is too large for a single generation, build in this priority order:

1. **Design system + layout + navigation** — get the shell perfect first
2. **Tab 1 (Overview/Summary)** — this is the first impression, make it flawless
3. **The most complex analytical tab** — this is the differentiated value
4. **Interactive calculators/simulators** — these are what make the tool sticky
5. **Remaining content tabs** — fill out the depth
6. **Reference/methodology tab** — the credibility layer
7. **Export/sharing features** — the actionability layer

**Build everything.** But if you must prioritize, follow this order.

---

## EXAMPLES OF WHAT EXCELLENCE LOOKS LIKE

The dashboard should make the user feel like they have:
- **A private McKinsey team** in their browser
- **A Bloomberg Terminal** tailored to their exact domain
- **An institutional-grade analytics desk** they can open anywhere

When someone opens this file, they should think: *"Wait, this is a single HTML file? This looks like a $500K enterprise platform."*

**Build accordingly.**

---

## CUSTOMIZATION NOTES

> **[ADD ANY DOMAIN-SPECIFIC INSTRUCTIONS HERE]**
>
> Examples:
> - "Use financial services terminology — bps, notional, DV01, VaR, CCAR, not generic business language"
> - "Include pre-loaded templates for different industries: banking, tech, healthcare, manufacturing"
> - "The primary user is a CFO — every view should tie back to dollar impact"
> - "Include a glossary of all technical terms used in the dashboard"
> - "Add a 'Methodology' expandable panel in every section explaining the math"
> - "Time series should cover 2020-2025 to capture COVID + rate hiking cycle"
> - "Include both a 'simple mode' and 'advanced mode' toggle for different user sophistication levels"

---

*This dashboard should make its user feel like they have a private command center built specifically for them. Build accordingly.*
