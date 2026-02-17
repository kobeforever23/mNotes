# BUILD PROMPT: CIB Model Risk Oversight & Health Monitoring Dashboard

## Context & Role

You are building a **state-of-the-art, standalone Model Risk Management (MRM) dashboard** for the **Head of Model Risk in Corporate & Investment Banking (CIB)**. This person owns and oversees every model across CIB Risk — hundreds of models spanning market risk, credit risk, counterparty risk, liquidity risk, and operational risk — across 19+ trading desks, 300,000+ risk drivers, and multiple regulatory frameworks (CCAR/DFAST, Basel III/IV, SR 11-7, OCC 2011-12).

The dashboard must function as the **single pane of glass** for model governance, health, performance, lifecycle, and regulatory compliance. It should be the kind of tool that a Fed examiner would see and immediately understand that this institution has best-in-class model risk management.

---

## Phase 1: Model Universe Discovery & Taxonomy

Before building any UI, you must first construct the **model inventory schema and classification framework**. This is the foundation everything else sits on.

### 1.1 Model Inventory Architecture

Build a comprehensive data model that captures every model in the CIB Risk ecosystem. Each model record should include:

**Identity & Ownership**
- Model ID (unique identifier, e.g., MR-VaR-001)
- Model Name & Version (with full version history)
- Model Owner (individual + team)
- Model Developer (individual + team)
- Model Validator (independent validation unit)
- Business Line / Desk Assignment (map to all 19+ desks)
- Upstream/Downstream Model Dependencies (directed graph)

**Classification**
- Risk Type: Market Risk | Credit Risk | Counterparty Credit Risk | Liquidity Risk | Operational Risk | Valuation/Pricing | Capital/Regulatory
- Model Category: VaR | Stress Testing | Pricing/Valuation | PD/LGD/EAD | CVA/DVA/FVA | Liquidity Coverage | CCAR/DFAST | Sensitivity/Greeks | Reserves/FVA | Other
- Materiality Tier: Tier 1 (Critical/Regulatory) | Tier 2 (Significant) | Tier 3 (Standard) | Tier 4 (Low Impact)
- Regulatory Touchpoints: Which regulations/submissions does this model feed into?

**Lifecycle Metadata**
- Initial Approval Date
- Last Validation Date
- Next Scheduled Validation Date
- Last Material Change Date
- Current Lifecycle Stage: Development | Validation | Approved | Monitoring | Remediation | Sunset/Decommission
- MRA/MRIA Status (Matter Requiring Attention / Immediate Attention)
- Open Findings Count & Severity
- Compensating Controls (if any)

### 1.2 Model Taxonomy Tree

Build a hierarchical, interactive taxonomy that lets the user navigate:

```
CIB Risk Models
├── Market Risk
│   ├── VaR Models
│   │   ├── Historical Simulation VaR
│   │   ├── Parametric VaR
│   │   ├── Monte Carlo VaR
│   │   ├── Stressed VaR (SVaR)
│   │   └── Incremental/Component VaR
│   ├── Sensitivity Models
│   │   ├── Greeks (Delta, Gamma, Vega, Theta, Rho)
│   │   └── Basis Risk Models
│   ├── Stress Testing / Scenario Models
│   │   ├── CCAR/DFAST Scenario Models
│   │   ├── Reverse Stress Tests
│   │   ├── Ad-Hoc Scenario Engines
│   │   └── Macroeconomic Variable Translation Models
│   └── Pricing/Valuation Models
│       ├── Derivatives Pricing (by product: IRS, CDS, FX Options, Exotics, etc.)
│       ├── Structured Products
│       └── IPV / Independent Price Verification Models
├── Credit Risk
│   ├── PD Models (by segment)
│   ├── LGD Models
│   ├── EAD Models
│   ├── Rating/Scorecard Models
│   └── Concentration Risk Models
├── Counterparty Credit Risk
│   ├── PFE / EPE Models
│   ├── CVA/DVA/FVA Models
│   ├── Wrong-Way Risk Models
│   └── Margin/Collateral Models
├── Liquidity Risk
│   ├── LCR Models
│   ├── NSFR Models
│   ├── Intraday Liquidity Models
│   └── Contingent Liquidity Models
└── Operational / Other
    ├── Op Risk Capital Models
    ├── Revenue Forecasting Models
    └── Data Quality / Transformation Models
```

**Deliverable:** An interactive, expandable/collapsible tree with click-through to any model's detail page. Each node shows aggregate health metrics (green/yellow/red) that roll up from children.

---

## Phase 2: Model Health Scoring Engine

This is the core analytical engine. Build a **composite health score** for every model, updated continuously, that synthesizes multiple dimensions into a single 0–100 score with intuitive color coding.

### 2.1 Health Score Dimensions

Each dimension should be independently scored (0–100) and weighted based on model materiality tier:

| Dimension | Description | Weight (Tier 1) | Weight (Tier 3) |
|---|---|---|---|
| **Backtesting Performance** | P&L explain, VaR exceedances, coverage ratios, Kupiec/Christoffersen tests | 25% | 15% |
| **Validation Recency** | Time since last independent validation vs. policy requirement | 15% | 20% |
| **Finding Severity** | Open MRAs/MRIAs, aging of findings, remediation progress | 20% | 15% |
| **Data Quality** | Input data completeness, staleness, anomaly rates | 10% | 15% |
| **Implementation Integrity** | Code vs. documentation alignment, change control adherence | 10% | 10% |
| **Stability & Drift** | Parameter stability, output distribution shifts, concept drift detection | 10% | 15% |
| **Operational Resilience** | Runtime failures, fallback activations, SLA adherence | 10% | 10% |

### 2.2 Scoring Logic

```
Health Score = Σ (Dimension Score × Dimension Weight)

Thresholds:
  85–100  → Green  (Healthy)
  70–84   → Yellow (Watch)
  50–69   → Orange (Elevated Concern)
  0–49    → Red    (Critical / Action Required)
```

### 2.3 Automated Degradation Triggers

The system should automatically downgrade a model's health score (override to Red/Orange) if ANY of the following are true, regardless of composite score:

- Validation is overdue by > 90 days
- Any open MRIA older than 60 days without remediation plan
- Backtesting failures exceed regulatory threshold (e.g., Basel traffic light: >10 VaR exceptions in 250 days)
- Model has been running on compensating controls for > 180 days
- Critical data feed has been stale for > 2 business days
- Any P1 production incident in last 30 days unresolved

---

## Phase 3: Dashboard Design & Interactive Views

### 3.1 Executive Command Center (Landing Page)

The first thing the Head of Model Risk sees. Must convey the **entire portfolio's health in 5 seconds**.

**Layout:**

```
┌─────────────────────────────────────────────────────────────┐
│  CIB MODEL RISK COMMAND CENTER          [Date] [Refresh ↻] │
├──────────┬──────────┬──────────┬──────────┬─────────────────┤
│  TOTAL   │  GREEN   │  YELLOW  │  ORANGE  │      RED        │
│  347     │  281     │   42     │   18     │       6         │
│  Models  │  (81%)   │  (12%)   │  (5%)    │     (2%)        │
├──────────┴──────────┴──────────┴──────────┴─────────────────┤
│                                                             │
│  [INTERACTIVE TREEMAP / HEATMAP]                            │
│  Rectangles sized by materiality, colored by health score.  │
│  Grouped by Risk Type > Category > Individual Model.        │
│  Click any rectangle to drill into model detail.            │
│                                                             │
├─────────────────────────┬───────────────────────────────────┤
│  CRITICAL ALERTS (6)    │  UPCOMING DEADLINES (Next 30d)    │
│  ▸ MR-VaR-003: 14 VaR  │  ▸ 8 validations due              │
│    exceptions (Red)     │  ▸ 3 MRA remediation deadlines     │
│  ▸ CR-PD-012: MRIA      │  ▸ 1 CCAR submission milestone     │
│    open 94 days         │  ▸ 2 model sunsets pending          │
│  ▸ CCR-CVA-001: Data    │                                    │
│    feed stale 3 days    │                                    │
├─────────────────────────┴───────────────────────────────────┤
│  TREND: Portfolio Health Score (12-month rolling)            │
│  [Sparkline/Area chart showing aggregate health over time]  │
│                                                             │
│  REGULATORY PULSE                                           │
│  CCAR: ██████████░░ 83%    Basel: █████████░░░ 75%          │
│  SR 11-7: ████████████ 97%  Internal Audit: ████████░░ 80%  │
└─────────────────────────────────────────────────────────────┘
```

### 3.2 Model Deep-Dive Page (Click-Through from Any Model)

When you click any model, you get a **comprehensive single-model view**:

**Section A: Model Identity Card**
- All metadata from Phase 1 displayed cleanly
- Model dependency graph (what feeds this model, what this model feeds)
- Visual lifecycle timeline (development → validation → approval → current state)

**Section B: Performance Analytics (Interactive Charts)**
- **Backtesting Panel**: Rolling VaR exceedance chart (actual P&L vs. VaR bands), Basel traffic light indicator, Kupiec test p-values over time, Christoffersen independence test results
- **P&L Attribution / Explain**: Hypothetical vs. Actual P&L decomposition, risk-theoretical P&L vs. actual
- **Sensitivity Analysis**: How model outputs change with input perturbations (interactive sliders)
- **Benchmark Comparison**: If challenger models exist, show side-by-side performance
- **Distribution Analysis**: QQ plots of model residuals, tail behavior analysis, Kolmogorov-Smirnov tests over rolling windows

**Section C: Stability & Drift Monitor**
- Time series of key model parameters with control limits (Shewhart-style)
- Population Stability Index (PSI) for input features and output distributions
- Concept drift detection using statistical tests (CUSUM, Page-Hinkley, ADWIN)
- Alert history: when drift was detected, what action was taken

**Section D: Finding & Issue Tracker**
- All open MRAs/MRIAs with severity, age, owner, remediation status
- Finding aging analysis (Gantt-style chart: opened → target → actual resolution)
- Historical finding trends: are we improving or accumulating debt?
- Compensating controls inventory with effectiveness assessment

**Section E: Operational Health**
- Model runtime performance (execution time trends, SLA adherence)
- Data input quality metrics (completeness, timeliness, accuracy checks)
- Failure/fallback activation log
- Change history (all model changes with approval chain)

### 3.3 Comparative & Cross-Sectional Views

**Desk-Level Risk View**: Aggregate model health by trading desk. Which desks have the most model risk exposure? Interactive bar chart with drill-down.

**Risk-Type Heatmap**: Matrix view — rows are risk types, columns are health dimensions. Each cell is color-coded. Instantly see "Credit Risk models have a data quality problem" or "Market Risk models are overdue for validation."

**Validation Pipeline**: Kanban-style board showing all models flowing through the validation lifecycle. Columns: Scheduled → In Progress → Findings Issued → Remediation → Closed. Drag-and-drop prioritization for the MRM team.

**Regulatory Readiness Tracker**: For each regulatory framework (CCAR, Basel, SR 11-7), show:
- Which models are in scope
- Current compliance status of each
- Gap analysis
- Timeline to next submission with readiness percentage

**Model Dependency Network Graph**: Force-directed graph visualization showing all model interdependencies. Node size = materiality. Node color = health. Edge thickness = strength of dependency. Click any node to see upstream/downstream impact analysis ("if this model breaks, what else breaks?").

### 3.4 Analytics & Intelligence Layer

**Predictive Model Risk Scoring**: Using historical patterns of model degradation, build a simple ML layer that predicts which models are likely to breach health thresholds in the next 30/60/90 days. Display as a "watch list" with confidence intervals.

**What-If Scenario Engine**: "If we delay validation of these 5 models by 60 days, what happens to our portfolio health score and regulatory compliance posture?" Interactive sliders.

**Peer Benchmarking** (if data available): How does our model risk posture compare to industry benchmarks? SR 11-7 compliance rates, average finding resolution times, validation coverage ratios.

**Natural Language Summary Generator**: For each model, each desk, and the overall portfolio, auto-generate a plain-English narrative summary of current health status, key risks, and recommended actions. This should read like a concise executive briefing paragraph that the Head of Model Risk could paste into a board report.

---

## Phase 4: Interaction & UX Requirements

### 4.1 Core Interactions
- **Global Search**: Type any model name, ID, desk, risk type, or finding ID to jump directly there
- **Filtering**: Multi-select filters for risk type, materiality tier, health status, desk, lifecycle stage, regulatory scope — all combinable
- **Time Travel**: Slider to view the portfolio's health at any historical point in time
- **Export**: Any view exportable to PDF (board-ready formatting), Excel (raw data), or PowerPoint (presentation slides)
- **Bookmarks**: Save custom filtered views for quick access
- **Annotations**: Add notes/comments to any model or finding for context (audit trail maintained)

### 4.2 Alerting & Notification System
- Configurable alert rules (e.g., "alert me when any Tier 1 model drops below 70")
- Alert channels: in-dashboard notification center, email digest (daily/weekly), Slack/Teams integration
- Escalation chains: if alert unacknowledged in 24 hours, escalate to next level
- Alert fatigue prevention: intelligent grouping, suppression of duplicate alerts, severity-based prioritization

### 4.3 Access Control & Audit
- Role-based access: Head of MRM (full access), Model Validators (read + validate workflow), Model Owners (their models only), Regulators (read-only curated view), Internal Audit (read-only full access)
- Every action logged with user, timestamp, and before/after state
- Regulatory examination mode: pre-built views and reports formatted for Fed/OCC examiner walkthroughs

---

## Phase 5: Data Architecture & Integration

### 5.1 Data Sources to Integrate
- **Model Inventory System** (e.g., internal model registry database)
- **Risk Engines** (VaR calculation systems, stress testing platforms)
- **P&L Systems** (for backtesting: hypothetical and actual P&L feeds)
- **Market Data** (for risk driver monitoring: Bloomberg, Reuters, internal feeds)
- **Validation Management System** (findings, MRAs, validation reports)
- **Change Management / SDLC** (model code deployments, version control)
- **Operational Monitoring** (runtime logs, SLA tracking, job schedulers)
- **Regulatory Reporting Systems** (CCAR/DFAST submission platforms, FR Y-14)

### 5.2 Data Refresh Cadence
- **Real-time** (streaming): Production incident alerts, critical data feed status
- **Intraday** (every 1–4 hours): VaR exceedance checks, P&L feeds
- **Daily** (EOD): Full backtesting metrics, health score recalculation, data quality scores
- **Weekly**: Stability/drift analysis, trend calculations, predictive scoring refresh
- **On-demand**: Validation status changes, finding updates, manual overrides

### 5.3 Technical Stack Recommendations
- **Frontend**: React with D3.js/Plotly for advanced visualizations, AG Grid for tabular data, Cytoscape.js for network graphs
- **Backend**: Python (FastAPI) or Node.js for API layer
- **Database**: PostgreSQL for structured data, TimescaleDB or InfluxDB for time-series metrics
- **Caching**: Redis for real-time dashboard performance
- **Search**: Elasticsearch for full-text search across models, findings, and reports
- **Auth**: LDAP/Active Directory integration with row-level security
- **Deployment**: Containerized (Docker/Kubernetes), deployable on-prem or private cloud per bank infrastructure requirements

---

## Phase 6: Build Sequence & Milestones

### Sprint 1–2: Foundation
- [ ] Model inventory data model and database schema
- [ ] API layer for CRUD operations on model records
- [ ] Authentication and role-based access framework
- [ ] Basic UI shell with navigation and global search

### Sprint 3–4: Health Engine
- [ ] Health scoring engine (all 7 dimensions)
- [ ] Automated degradation trigger logic
- [ ] Historical health score storage and trend calculation
- [ ] Alert rule engine and notification system

### Sprint 5–7: Core Dashboard Views
- [ ] Executive Command Center (treemap, alerts, trends)
- [ ] Model Deep-Dive page (all 5 sections)
- [ ] Desk-level and risk-type comparative views
- [ ] Validation pipeline Kanban

### Sprint 8–9: Advanced Analytics
- [ ] Model dependency network graph
- [ ] Predictive degradation scoring
- [ ] What-if scenario engine
- [ ] Natural language summary generator

### Sprint 10: Polish & Regulatory Readiness
- [ ] Regulatory examination mode
- [ ] Export engine (PDF, Excel, PowerPoint)
- [ ] Performance optimization and load testing
- [ ] UAT with model validators and MRM leadership

---

## Guiding Principles

1. **Examiner-Ready at All Times**: Every view should answer the question a Fed examiner would ask. "Show me your worst-performing models." "How quickly do you resolve findings?" "What's your validation coverage?" — one click, instant answer.

2. **Action-Oriented, Not Just Informational**: Every metric should link to an action. Red health score → "Here's what's wrong and here's the remediation workflow." Overdue validation → "Here's the scheduling interface to assign it."

3. **Hierarchy of Information**: The Head of MRM should get the full picture in 5 seconds on the landing page, drill into concern areas in 30 seconds, and reach root-cause detail in 2 minutes. Never more than 3 clicks to any piece of information.

4. **No Stale Data, No Surprises**: The dashboard should surface problems before the Head of MRM hears about them from someone else. Proactive alerting > reactive reporting.

5. **Audit Trail Everything**: In a regulated environment, every state change, every override, every annotation must be logged and retrievable. The dashboard itself should be a model of the governance it monitors.

---

## Appendix: Sample Model Health Profiles for Testing

Use these representative model archetypes to validate dashboard behavior:

**Model A — Healthy Tier 1**: Historical Simulation VaR, 2 years since last finding, backtesting clean, stable parameters. Health: 94.

**Model B — Watch Status**: Credit PD model with PSI drift detected in 2 input features, validation due in 45 days, one low-severity open finding. Health: 73.

**Model C — Elevated Concern**: CVA model with stale counterparty data feed (2 days), backtesting marginal (9 exceptions in 250 days approaching Basel yellow zone), one open MRA at 50 days. Health: 58.

**Model D — Critical**: Exotic derivatives pricing model, MRIA open 120 days with no remediation plan, running on compensating controls for 200 days, 3 P1 production incidents in last 30 days. Health: 22 (auto-override to Red).

---

*This prompt is designed to be handed to a senior full-stack engineer, a development team, or an advanced AI coding assistant. The output should be a fully functional, standalone web application that requires only data source connectivity to go live.*
