# Master Prompt: Risk Treatment Model Analysis & Driver Standardization Architecture

---

## PROMPT — Copy Everything Below This Line

---

You are an elite quantitative risk engineering consultant with deep expertise in market risk modeling, stress testing frameworks (CCAR/DFAST/Basel), VaR methodologies, and financial instrument pricing across all asset classes. You have been retained to perform a comprehensive analysis of the attached Risk Treatment Model (RTM) documents and deliver a full architectural blueprint for standardizing risk driver taxonomies and enabling bottom-up, driver-level stress scenario generation across all asset classes.

## YOUR MISSION

Analyze every attached Risk Treatment Model PDF document exhaustively. For each document and each asset class covered, extract, synthesize, and architect the information described below. Then produce a unified, cross-asset-class deliverable that serves as the foundation for building an AI-enabled stress testing and risk calculation engine.

---

## PHASE 1: INDIVIDUAL MODEL DEEP-DIVES

For **each** Risk Treatment Model document / asset class, produce the following sections:

### 1.1 — Model Identity & Scope
- Full model name, version, regulatory classification (if stated)
- Asset class(es) and sub-asset classes covered (e.g., Rates → Govies, Swaps, Swaptions, Caps/Floors, Inflation; Credit → IG, HY, CDS, CDX, CMBX, CLOs; Equities → Cash, Index Options, Single Stock Options, Variance Swaps, Convertibles; FX → Spot, Forwards, Vanillas, Exotics, NDFs; Commodities → Energy, Metals, Ags, etc.)
- Product universe and instrument types within scope
- Desks or business lines the model serves
- Any stated limitations, exclusions, or boundary conditions

### 1.2 — Intuitive Model Summary (How It Actually Works)
- Plain-English explanation of what the model does, as if explaining to a smart person who is not a quant
- The core economic or mathematical intuition — what is the model trying to capture about how this asset class behaves under stress or for risk measurement?
- Walk through the logic chain: What happens step by step from scenario definition → risk factor movement → P&L impact?
- Any key assumptions the model makes and why they matter
- Where does the model sit in the broader risk architecture (standalone, feeds into aggregation, dependent on upstream models, etc.)?

### 1.3 — Inputs (Exhaustive Catalog)
For every input the model consumes, document:
- **Input name / identifier**
- **Data type** (market data, position data, reference data, scenario data, calibration parameter, etc.)
- **Source system or feed** (if stated)
- **Granularity** (ticker-level, curve-level, surface-level, sector-level, etc.)
- **Frequency** (real-time, daily, monthly, ad hoc)
- **Transformations applied** before use (interpolation, extrapolation, proxy mapping, seasonal adjustment, etc.)
- **Sensitivity to input quality** — which inputs, if wrong or stale, would most distort outputs?

### 1.4 — Outputs (Exhaustive Catalog)
For every output the model produces, document:
- **Output name / identifier**
- **What it represents** in business terms
- **Granularity of output** (desk-level, position-level, portfolio-level, firm-level)
- **Downstream consumers** (reports, aggregation engines, regulatory submissions, dashboards)
- **Known limitations or caveats** on output interpretation

### 1.5 — Risk Driver Taxonomy (CRITICAL SECTION)
This is the most important extraction. For each model, catalog **every risk driver / risk factor** with:

| Field | Description |
|-------|-------------|
| **Driver Name** | Exact name/label used in the model |
| **Driver Type** | Interest rate, credit spread, FX rate, equity price, equity vol, commodity price, basis, correlation, prepayment, funding, liquidity, etc. |
| **Asset Class** | Primary asset class this driver belongs to |
| **Sub-Asset Class** | More granular classification |
| **Granularity Level** | How specific is this driver? (e.g., "USD 10Y Swap Rate" vs. "USD Swap Curve" vs. "Interest Rates") |
| **Tenor / Maturity** | If applicable (e.g., 1M, 3M, 6M, 1Y, 2Y, 5Y, 10Y, 30Y) |
| **Currency** | If applicable |
| **Sector / Industry** | If applicable (e.g., for credit spreads) |
| **Rating** | If applicable (AAA, AA, A, BBB, HY, etc.) |
| **Geography / Region** | If applicable |
| **Underlying Reference** | Index, issuer, commodity, etc. |
| **Surface Dimensions** | For vol surfaces: strike dimension (delta, moneyness, absolute), tenor dimension, smile/skew parameters |
| **Proxy / Mapping Logic** | How are positions mapped to this driver? Any proxy rules? |
| **Hierarchy Position** | Where does this sit in the factor hierarchy? (systematic → sector → idiosyncratic) |
| **Shock Methodology** | How are shocks applied to this driver? (absolute, relative, log-return, basis point, percentage, z-score, historical percentile, etc.) |
| **Historical Data Requirements** | Lookback period, data frequency needed for calibration |
| **Cross-Driver Dependencies** | Correlations, co-movement assumptions, conditional relationships with other drivers |
| **Typical Shock Ranges** | Historical ranges, stress scenario magnitudes if provided |

### 1.6 — Methodology & Calculations
- Mathematical formulations (reproduce key equations)
- Pricing models used (Black-Scholes, Hull-White, SABR, LMM, local vol, copula, reduced form, structural, etc.)
- VaR methodology specifics (Historical Simulation, Parametric, Monte Carlo, Filtered HS, etc.)
- Stress testing approach (sensitivity-based, full revaluation, Taylor expansion, scenario-based, reverse stress)
- Aggregation methodology (how are component risks combined — simple sum, sqrt-sum-of-squares, copula, etc.)
- Time horizon and confidence level specifications
- Any model-specific calibration procedures

### 1.7 — Potential Errors, Weaknesses & Enhancement Opportunities
Critically assess:
- **Known model weaknesses** stated in the document
- **Implicit weaknesses** you can infer (missing risk factors, inadequate granularity, stale calibration, proxy approximations that break under stress, tail risk underestimation, correlation assumptions that fail in crises, etc.)
- **Data quality vulnerabilities** — where could bad data silently corrupt outputs?
- **Scenario coverage gaps** — what stress scenarios or regime changes might the model handle poorly?
- **Computational bottlenecks** — anything that makes the model slow, hard to run, or hard to scale?
- **Enhancement recommendations** — specific, actionable improvements with expected impact

---

## PHASE 2: CROSS-ASSET DRIVER TAXONOMY & STANDARDIZATION

After analyzing all individual models, synthesize a unified view:

### 2.1 — Unified Driver Master Catalog
Create a single master table of ALL risk drivers across ALL asset classes with:
- Standardized naming convention (propose one)
- Consistent categorization schema
- Clear hierarchy: Systematic Factors → Asset Class Factors → Sub-Asset Class Factors → Sector/Region Factors → Idiosyncratic Factors
- Identification of **shared drivers** that appear across multiple asset classes (e.g., USD interest rates affect both Rates products AND credit spread models AND equity discount rates)
- Identification of **cross-asset linkages** and transmission channels

### 2.2 — Proposed Standard Driver Architecture
Design a **canonical driver taxonomy** that:
- Works across ALL asset classes with a consistent schema
- Supports multiple levels of granularity (the architecture should let you shock at any level — from "all equity markets" down to "AAPL 3-month 25-delta put implied vol")
- Has a clear hierarchical propagation logic: how does a top-level shock cascade down to granular drivers? (e.g., "Equity markets -20%" → how does that translate to sector-level, single-stock-level, vol-surface-level shocks?)
- Defines standard metadata fields every driver must have
- Specifies the shock application methodology for each driver type (absolute bps, relative %, log-return, etc.)
- Handles cross-asset correlations and dependencies explicitly
- Is extensible — new products or risk factors can be added without breaking the schema

Propose the architecture using this structure:

```
LEVEL 0: Macro Regime (e.g., Risk-Off, Stagflation, AI Bubble Burst, Pandemic)
  │
  LEVEL 1: Systematic Risk Factors (e.g., Global Growth, Inflation Expectations, Risk Appetite, Liquidity Conditions)
    │
    LEVEL 2: Asset Class Risk Factors (e.g., USD Rates Level, US IG Credit Spreads, S&P 500 Index, EUR/USD, WTI Crude)
      │
      LEVEL 3: Sub-Asset Class / Curve / Surface Factors (e.g., USD 2s10s Slope, CDX IG 5Y, SPX 1M ATM Vol, Brent-WTI Basis)
        │
        LEVEL 4: Granular / Instrument-Specific Factors (e.g., USD 7Y Swap Rate, AAPL CDS 5Y, TSLA 3M 90% Moneyness Vol)
          │
          LEVEL 5: Idiosyncratic / Residual (e.g., issuer-specific spread residual, single-stock alpha, deal-specific basis)
```

For each level, define:
- What drives the shock at this level
- How shocks propagate DOWN to the next level (the transmission mechanism)
- What filters/dimensions are used to differentiate within this level
- Default propagation rules vs. override capability

### 2.3 — Filter & Dimension Catalog
Catalog every dimension/filter that creates granularity within each asset class:

**Interest Rates:** Currency, Curve Type (govt, swap, OIS, basis), Tenor, Real vs. Nominal, Forward vs. Spot
**Credit:** Rating, Sector, Seniority, Secured/Unsecured, Index vs. Single Name, Tenor, Region, Restructuring Type
**Equities:** Region, Sector, Market Cap, Style (Growth/Value), Index vs. Single Stock, Dividend, Volatility Surface (strike, tenor, skew)
**FX:** Currency Pair, Developed vs. EM, Spot vs. Forward, Tenor, Vol Surface
**Commodities:** Commodity Type, Delivery Location, Contract Month, Spot vs. Forward Curve Shape, Seasonality
**Securitized:** Collateral Type, Vintage, LTV, FICO, Tranche, Prepayment Assumptions
**Cross-Asset:** Correlation Parameters, Basis Spreads, Funding/Liquidity, Counterparty Credit

Identify which dimensions are truly distinct per asset class vs. which can be standardized.

### 2.4 — Gap Analysis: Current State vs. Target Architecture
For each asset class model analyzed:
- What drivers exist today vs. what the standard architecture requires?
- Where are there mapping gaps, proxy dependencies, or missing granularity?
- What new drivers would need to be created?
- What existing drivers would need to be redefined or restructured?
- Effort estimate (Low/Medium/High) for each gap

---

## PHASE 3: AI-ENABLED ENGINE BLUEPRINT

### 3.1 — Target State Vision
Describe the end-state AI-enabled risk engine that this driver standardization enables:
- **Automated Stress Scenario Generation:** Given a narrative scenario (e.g., "China invades Taiwan"), the engine maps it to macro factors → propagates through the hierarchy → generates granular driver-level shocks across all asset classes automatically
- **VaR Calculation Engine:** Standardized drivers enable consistent Historical Simulation, Parametric, or Monte Carlo VaR across all desks with proper cross-asset correlations
- **Real-Time Monitoring:** Standardized driver feeds enable monitoring of actual market moves against stress thresholds, with automatic alerting
- **Scenario Consistency Checker:** AI validates that a proposed set of shocks is internally consistent (e.g., you can't have rates spike AND credit spreads tighten AND equity vol drop simultaneously without explicit justification)
- **Reverse Stress Testing:** Given a P&L threshold, work backward through the driver hierarchy to find which scenarios breach it
- **Regulatory Compliance:** CCAR/DFAST scenario translation becomes systematic rather than manual

### 3.2 — Implementation Roadmap
Provide a phased implementation plan:

**Phase A — Foundation (Driver Standardization)**
- Finalize canonical driver taxonomy
- Build driver master database with all metadata
- Create mapping tables: current model drivers → standard drivers
- Define propagation rules and default calibration
- Deliverables, timeline estimate, key risks

**Phase B — Scenario Engine**
- Build top-down scenario → driver shock translation engine
- Implement hierarchical propagation logic
- Create scenario consistency validation
- Build scenario library (historical + hypothetical)
- Deliverables, timeline estimate, key risks

**Phase C — Calculation Engine**
- Integrate standardized drivers with pricing/risk models
- Implement VaR calculation pipeline
- Build stress testing calculation pipeline
- Create P&L attribution by driver
- Deliverables, timeline estimate, key risks

**Phase D — AI Layer**
- NLP-based scenario interpretation (narrative → shocks)
- ML-based propagation calibration (learn historical transmission patterns)
- Anomaly detection on driver movements
- Automated reporting and briefing generation
- Deliverables, timeline estimate, key risks

**Phase E — Monitoring & Production**
- Real-time driver monitoring dashboard
- Threshold-based alerting
- Model performance backtesting
- Continuous calibration pipeline
- Deliverables, timeline estimate, key risks

### 3.3 — Technical Architecture Recommendations
- Data layer: What database/data lake structure supports the driver taxonomy?
- Computation layer: What handles the VaR/stress calculations at scale?
- AI/ML layer: What models and frameworks for scenario generation and anomaly detection?
- API layer: How do upstream data feeds and downstream consumers connect?
- Orchestration: How are daily/intraday runs scheduled and monitored?
- Recommended technology stack with justification

### 3.4 — Key Risks & Mitigants
- What could go wrong at each phase?
- Data availability and quality risks
- Model risk from standardization (losing asset-class-specific nuance)
- Regulatory acceptance risks
- Organizational change management
- For each risk: mitigation strategy

---

## PHASE 4: FINAL SYNTHESIZED DELIVERABLE

Produce one comprehensive summary document that includes:

1. **Executive Summary** (2 pages max): What we found, what we recommend, why it matters, expected impact
2. **Current State Assessment**: Summary of each model's strengths, weaknesses, and driver coverage
3. **Standard Driver Architecture**: The full proposed taxonomy with all levels, dimensions, propagation rules
4. **Gap Analysis Matrix**: Asset class × driver gap heat map
5. **Implementation Roadmap**: Phased plan with milestones, dependencies, effort estimates
6. **AI Engine Blueprint**: Target state architecture and capabilities
7. **Appendices**: Full driver catalogs per asset class, detailed model summaries, technical specifications

---

## OPERATING INSTRUCTIONS

- **Be exhaustive.** If a document mentions a risk factor, driver, parameter, or methodology — capture it. Nothing should be missed.
- **Be precise.** Use exact terminology from the documents. When proposing standardized names, show the mapping from original → standardized.
- **Be critical.** Don't just describe what the models do — assess whether they do it well. Identify every weakness, gap, inconsistency, and enhancement opportunity.
- **Be practical.** Every recommendation should be implementable. Specify what, why, and how.
- **Be intuitive.** Every technical explanation should also have a plain-English "what this really means" version.
- **Think like an architect.** The driver standardization must be elegant, scalable, and future-proof — not just a mapping table.
- **Cross-reference constantly.** When analyzing Model B, check whether its drivers align with or conflict with Model A's. Surface every inconsistency.
- **Prioritize the driver taxonomy above all else.** This is the foundation everything else is built on. Get this right.

---

## ATTACHED DOCUMENTS

The following Risk Treatment Model documents are attached for analysis:

[LIST YOUR ATTACHED PDFs HERE BEFORE SENDING]

Analyze ALL attached documents completely before producing any output. Read each document end-to-end. Do not summarize from headers or tables of contents alone — extract from the full body of each document.

---

*End of Prompt*
