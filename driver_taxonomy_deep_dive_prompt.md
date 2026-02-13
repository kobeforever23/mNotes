# Master Prompt: Risk Driver Taxonomy Extraction & Standardization Architecture

---

## PROMPT — Copy Everything Below This Line

---

You are an elite quantitative risk engineer specializing in market risk factor modeling, driver taxonomy design, and stress testing infrastructure across all asset classes. You have been retained for one critical mission: extract every risk driver from the attached Risk Treatment Model documents, build a unified cross-asset driver taxonomy, and design the canonical hierarchical architecture that will serve as the foundation for bottom-up stress scenario generation, VaR computation, and all downstream risk analytics.

The driver architecture is everything. Every future capability — automated stress testing, AI scenario generation, real-time monitoring, regulatory compliance — depends on getting this layer right. Treat this accordingly.

---

## STEP 1: RAW DRIVER EXTRACTION (Per Document / Per Asset Class)

For every single Risk Treatment Model document attached, extract **every risk driver, risk factor, market variable, model parameter, and sensitivity** referenced anywhere in the document. Nothing gets skipped. If it moves and affects P&L, it's a driver.

For each driver extracted, populate ALL of the following fields:

### Core Identity
| Field | What to Capture |
|-------|----------------|
| **Driver Name (As-Is)** | Exact name/label used in the document — preserve original terminology verbatim |
| **Driver Description** | What this driver actually represents in plain English |
| **Asset Class** | Rates, Credit, Equities, FX, Commodities, Securitized, Cross-Asset, Other |
| **Sub-Asset Class** | More specific (e.g., IG Corporates, EM Sovereign, Index Options, Energy Forwards, CMBS, etc.) |
| **Product Coverage** | Which instruments/products does this driver price or risk-measure? |

### Granularity & Dimensions
| Field | What to Capture |
|-------|----------------|
| **Granularity Level** | How specific? (Broad market level → Curve/surface level → Sector level → Single name/instrument level) |
| **Currency** | Which currency or currencies |
| **Tenor / Maturity Points** | All tenor points this driver covers (e.g., ON, 1W, 1M, 3M, 6M, 1Y, 2Y, 3Y, 5Y, 7Y, 10Y, 15Y, 20Y, 30Y) |
| **Rating** | If credit-related: AAA, AA, A, BBB, BB, B, CCC, NR, etc. |
| **Sector / Industry** | If applicable: Financials, Industrials, Utilities, Tech, Energy, etc. |
| **Seniority** | If applicable: Senior, Subordinated, Secured, Unsecured, Recovery |
| **Geography / Region** | US, Europe, UK, Japan, EM Asia, EM LATAM, CEEMEA, Global, etc. |
| **Underlying Reference** | Index name, issuer, commodity, curve name, etc. |
| **Strike / Moneyness Dimension** | For vol surfaces: how is the strike axis defined? (Delta, moneyness, absolute strike, log-moneyness) |
| **Surface / Cube Dimensions** | Full dimensionality — which axes does this driver live on? (e.g., tenor × strike × expiry) |
| **Curve Segment** | If part of a term structure: short end, belly, long end, or specific node |
| **Basis / Spread Type** | If a spread: spread over what? (Treasuries, OIS, SOFR, Libor legacy, swap, index, etc.) |

### Behavior & Methodology
| Field | What to Capture |
|-------|----------------|
| **Driver Type** | Categorize: Level, Slope, Curvature, Spread, Basis, Volatility (realized/implied), Correlation, Skew, Convexity, Dividend, Prepayment, Recovery, Funding, Liquidity, Jump/Default, Seasonality, Carry, Roll-Down, Other |
| **Shock Application Method** | How are shocks applied? Absolute (bps, price points), Relative (%), Log-return, Z-score, Percentile-based, Scenario-specific override |
| **Units** | bps, %, price, vol points, ratio, index level, etc. |
| **Typical Shock Magnitudes** | Any ranges given in the doc — historical stress levels, regulatory scenario levels, 1-sigma, 99th percentile, etc. |
| **Historical Data Requirements** | What lookback period and data frequency does calibration require? |
| **Stationarity / Return Convention** | Levels, first differences, log-returns, percent changes — how is this driver modeled through time? |
| **Distribution Assumptions** | Normal, log-normal, Student-t, empirical, jump-diffusion, regime-switching, etc. |
| **Mean Reversion** | Does the model assume mean reversion for this driver? Speed? Level? |

### Relationships & Dependencies
| Field | What to Capture |
|-------|----------------|
| **Hierarchy Position** | Where in the factor hierarchy: Systematic/Macro → Asset Class → Sub-Asset Class → Sector → Idiosyncratic |
| **Parent Driver(s)** | What higher-level driver(s) does this decompose from? |
| **Child Driver(s)** | What lower-level drivers does this cascade into? |
| **Cross-Asset Linkages** | Does this driver appear in or affect models for OTHER asset classes? Which ones? How? |
| **Correlation Assumptions** | Explicit correlation values or assumptions with other drivers stated in the doc |
| **Co-Movement / Beta Relationships** | Any stated beta, loading, or sensitivity to other factors |
| **Conditional Dependencies** | Any "if X happens, then this driver behaves differently" logic |
| **Proxy / Mapping Rules** | How are positions without direct driver coverage mapped? What proxy logic is used? What is the fallback hierarchy? |

### Quality & Coverage Assessment
| Field | What to Capture |
|-------|----------------|
| **Data Source** | Where does this driver's data come from? (Bloomberg, internal curves, vendor, derived/calculated) |
| **Data Quality Concerns** | Any issues: illiquid tenors, stale data, interpolated points, vendor discrepancies, holiday gaps |
| **Coverage Gaps** | What positions or products SHOULD be sensitive to this driver but aren't captured? |
| **Proxy Quality Rating** | If positions are proxied to this driver: how good is the proxy? (Exact, Strong, Moderate, Weak, Questionable) |
| **Enhancement Opportunity** | What would make this driver better? More granularity? Better data? Different shock methodology? |

---

## STEP 2: DRIVER RELATIONSHIP MAPPING

After extracting all drivers from all documents, build explicit relationship maps:

### 2.1 — Within-Asset-Class Driver Trees
For each asset class, construct the full driver hierarchy as a tree:
```
[Asset Class Root]
  ├── [Broad Market Factor]
  │   ├── [Curve/Surface Component]
  │   │   ├── [Tenor-Specific Node]
  │   │   └── [Tenor-Specific Node]
  │   └── [Curve/Surface Component]
  ├── [Sector/Segment Factor]
  │   ├── [Sub-Sector]
  │   │   └── [Single Name / Instrument]
  │   └── [Sub-Sector]
  └── [Volatility / Higher-Order Factor]
      ├── [ATM Vol Level]
      ├── [Skew Parameter]
      └── [Term Structure of Vol]
```

Build this tree for every asset class. Show every driver's exact position. Identify where branches are thin (under-specified) vs. dense (well-covered).

### 2.2 — Cross-Asset Driver Linkage Map
Identify and document every instance where:
- The same underlying market variable appears as a driver in multiple asset class models (potentially with different names, granularity, or shock methods)
- A driver in one model is an input/dependency for a driver in another model
- Cross-asset transmission channels exist (e.g., rate moves → credit spread widening → equity devaluation → FX depreciation)

For each linkage, document:
- Driver A (model, name, granularity) ↔ Driver B (model, name, granularity)
- Nature of the relationship (same driver differently named, causal, correlated, derived-from)
- Whether the current models handle this linkage consistently or inconsistently
- Risk of inconsistent shocks if these aren't harmonized

### 2.3 — Proxy Chain Analysis
Map every proxy/mapping chain end to end:
- Position → Mapped Driver → Proxy Driver → Actual Data Source
- How many degrees of proxy separation exist?
- Where do proxy chains create the most model risk?
- Which proxy mappings would break down most severely under stress?

---

## STEP 3: INCONSISTENCY & GAP ANALYSIS

### 3.1 — Naming Inconsistencies
Find every instance where:
- Different models use different names for the same economic risk factor
- Same name is used for different things across models
- Abbreviations or conventions conflict
- Granularity differs for what should be the same driver

Present as a reconciliation table:
| Economic Risk Factor | Model A Name | Model B Name | Model C Name | Granularity Mismatch? | Shock Method Mismatch? |

### 3.2 — Granularity Mismatches
For each shared risk factor across models:
- Which model has the finest granularity?
- Which model has the coarsest?
- What is the right granularity for the standardized architecture?
- What would need to change in each model to align?

### 3.3 — Shock Methodology Conflicts
Identify where different models shock the same underlying driver using:
- Different units (bps vs. % vs. log-return)
- Different conventions (absolute vs. relative)
- Different horizons
- Different distributional assumptions
Flag every conflict and recommend the standard approach.

### 3.4 — Missing Driver Coverage
For each asset class, identify:
- Risk factors that SHOULD exist based on the product universe but are not in the model
- Dimensions of granularity that are collapsed (e.g., all tenors shocked uniformly when they should have term structure)
- Higher-order risks not captured (skew, convexity, correlation, jump, liquidity)
- Basis risks that are assumed away
- Tail behavior not modeled

### 3.5 — Propagation Logic Gaps
Identify where the current models lack clear rules for:
- How a macro-level shock translates to asset-class-level shocks
- How an asset-class-level shock distributes across sectors/segments
- How sector-level shocks flow to single-name/instrument-level
- How shocks in one asset class create consistent shocks in others
- Default behavior when a specific mapping doesn't exist

---

## STEP 4: CANONICAL DRIVER ARCHITECTURE DESIGN

Based on everything extracted and analyzed, design the **target-state standard driver architecture.**

### 4.1 — Hierarchical Framework

```
LEVEL 0 — MACRO REGIME / SCENARIO NARRATIVE
  Purpose: The story. "What is happening in the world?"
  Examples: Stagflation, Pandemic, Sovereign Debt Crisis, AI Bubble Burst, EM Contagion, Rate Shock
  Outputs: Directional signals and magnitude anchors for Level 1 factors
  │
LEVEL 1 — SYSTEMATIC / MACRO RISK FACTORS
  Purpose: Economy-wide forces that affect all or most asset classes
  Examples: Global GDP Growth, US Inflation Expectations, Fed Funds Rate, Global Risk Appetite,
            USD Broad Index, VIX Level, Oil Price, China Growth, European Political Risk
  Dimensions: Region, Horizon, Confidence Level
  Shock Method: [Define standard]
  Propagation Rule: [Define how L1 → L2 transmission works for each factor]
  │
LEVEL 2 — ASSET CLASS BENCHMARK FACTORS
  Purpose: Primary risk drivers at the asset class level
  Examples: UST 10Y Yield, CDX IG 5Y Spread, S&P 500 Level, EUR/USD Spot, WTI Front Month,
            30Y Mortgage Rate, US IG OAS, Nikkei 225, Gold Spot
  Dimensions: Currency, Benchmark Index, Primary Tenor
  Shock Method: [Define standard]
  Propagation Rule: [Define how L2 → L3 transmission works — betas, factor loadings, historical ratios]
  │
LEVEL 3 — SUB-ASSET / CURVE / SURFACE / SECTOR FACTORS
  Purpose: Differentiation within an asset class
  Examples: USD 2s10s Slope, IG vs HY Spread Ratio, SPX 1M ATM Implied Vol, EUR/USD 3M Risk Reversal,
            Brent-WTI Basis, CMBS AAA vs BBB Spread, Tech Sector Equity Beta, EM Sovereign CDS
  Dimensions: Tenor, Rating, Sector, Region, Curve Shape (Level/Slope/Curvature), Surface Coordinates
  Shock Method: [Define standard]
  Propagation Rule: [Define how L3 → L4 transmission works]
  │
LEVEL 4 — GRANULAR POINT-LEVEL FACTORS
  Purpose: Specific nodes on curves, surfaces, or within sectors
  Examples: USD 7Y Swap Rate, AAPL 5Y CDS Spread, TSLA 3M 25D Put Vol, USD/BRL 1Y Forward Points,
            Henry Hub Cal-25 Strip, CMBX BBB- Series 6, JPM Senior 5Y CDS
  Dimensions: All applicable filters at maximum specificity
  Shock Method: [Define standard — must be consistent with parent but can have local adjustments]
  Propagation Rule: [Define how L4 → L5 residuals work]
  │
LEVEL 5 — IDIOSYNCRATIC / RESIDUAL / INSTRUMENT-SPECIFIC
  Purpose: Risk not explained by any systematic or sector factor
  Examples: Single-name spread residual, deal-specific prepayment, illiquidity premium,
            event-driven jump risk, position-specific basis, new-issue concession
  Dimensions: Instrument-specific
  Shock Method: [Define standard — typically historical distribution of residuals or expert judgment]
  Propagation Rule: Terminal node — no further propagation
```

For **each level**, fully specify:
1. **Complete list of factors** belonging to this level (synthesized from all RTM docs)
2. **Standard naming convention** with format template (e.g., `{AssetClass}_{SubClass}_{Underlying}_{Tenor}_{Dimension}`)
3. **Required metadata fields** (every factor at this level must have these populated)
4. **Shock input specification** — what does a user/system need to provide to shock at this level?
5. **Propagation function** — the mathematical or rule-based logic for how a shock at this level cascades down
6. **Override protocol** — how does a user override the default propagation for specific children?
7. **Aggregation function** — how do shocks at this level roll UP for reporting purposes?
8. **Validation rules** — what makes a shock at this level internally consistent or inconsistent?

### 4.2 — Propagation Engine Specification

This is the core logic that makes hierarchical shocking work. Define:

**Default Propagation Rules:**
- L0 → L1: Scenario narrative → macro factor translation (mapping table + directional rules)
- L1 → L2: Macro factors → asset class benchmarks (historical betas, regression-based, expert rules)
- L2 → L3: Benchmarks → sub-components (curve decomposition, sector betas, vol surface dynamics)
- L3 → L4: Sub-components → granular points (interpolation, relative value relationships, basis models)
- L4 → L5: Granular → idiosyncratic (residual distribution, stress amplification factors)

**For each transition, specify:**
- The mathematical relationship (beta × parent shock + adjustment, or mapping table, or interpolation, etc.)
- Calibration methodology (how are the betas/mappings estimated? What data? What lookback?)
- Regime dependence (do the propagation rules change under stress vs. normal conditions?)
- Override mechanism (can a user pin a child driver to a specific shock regardless of parent?)
- Consistency constraints (what combinations are mathematically impossible or economically implausible?)

**Cross-Asset Propagation:**
- Define the explicit channels through which a shock in one asset class creates shocks in others
- Specify which cross-asset links are structural (always active) vs. conditional (activated in stress)
- Provide the transmission equations or mapping rules for each channel

### 4.3 — Standard Dimension / Filter Schema

Define the **universal set of dimensions** that apply across all asset classes, plus asset-class-specific dimensions:

**Universal Dimensions (apply to every driver):**
- Asset Class
- Sub-Asset Class
- Currency
- Region/Geography
- Tenor/Maturity
- Driver Type (Level, Spread, Vol, Correlation, Basis, etc.)
- Hierarchy Level (L1–L5)
- Shock Unit (bps, %, log-return, absolute)

**Asset-Class-Specific Dimensions:**

*Rates:* Curve Type (Govt, Swap, OIS, Repo, Basis, Real, Breakeven), Curve Component (Level, Slope, Curvature, Butterfly), Forward vs. Spot, Fixing Frequency

*Credit:* Rating Bucket, Sector, Seniority, Index vs. Single Name, Restructuring Clause, Maturity Bucket, Benchmark Spread (OAS, Z-Spread, ASW, CDS Basis), Secured/Unsecured, Recovery Assumption

*Equities:* Market Cap (Mega/Large/Mid/Small/Micro), Style (Growth/Value/Quality/Momentum), Index vs. Single Stock, Volatility Surface Coordinates (Expiry, Strike Convention, ATM Reference), Dividend (Discrete, Continuous, Implied), Correlation (Implied, Realized, Dispersion)

*FX:* Currency Pair Convention, Developed/EM Classification, Spot vs. Forward Tenor, Vol Surface (Expiry, Delta, ATM Convention, Risk Reversal, Butterfly), Cross Rate vs. Direct, NDF vs. Deliverable

*Commodities:* Commodity Group (Energy, Base Metals, Precious Metals, Agriculture, Softs), Delivery Location, Contract Month/Season, Spot vs. Forward Curve Shape (Contango/Backwardation), Grade/Quality, Physical vs. Financial

*Securitized/Structured:* Collateral Type (Residential, Commercial, Auto, Student, Card), Vintage, LTV Bucket, FICO Bucket, Coupon Type (Fixed, ARM, Hybrid), Tranche (Senior, Mezz, Sub, Equity, IO, PO), Prepayment Model Inputs (CPR, CDR, Severity, Voluntary/Involuntary), Agency vs. Non-Agency

For each dimension: define the enumerated values, default groupings, and whether it's required or optional for drivers in that asset class.

### 4.4 — Standard Driver ID & Naming Convention

Propose a deterministic naming/ID system so that:
- Every driver has a globally unique, human-readable identifier
- The name itself encodes key dimensions (asset class, type, underlying, tenor, etc.)
- Two different people building the same driver would arrive at the same ID
- The system is extensible without breaking existing IDs
- Provide the full format specification with examples for each asset class

Example format:
```
{AssetClass}.{SubClass}.{DriverType}.{Underlying}.{Dimension1}.{Dimension2}...

RATES.SWAP.LEVEL.USD.10Y           → USD 10Y Swap Rate Level
RATES.GOVT.SLOPE.USD.2S10S         → USD Treasury 2s10s Slope
CREDIT.IG.SPREAD.CDX_NA.5Y         → CDX NA IG 5Y Spread
CREDIT.HY.SPREAD.ENERGY.BB.5Y      → US HY Energy BB 5Y Spread
EQ.INDEX.LEVEL.SPX                  → S&P 500 Index Level
EQ.SINGLE.VOL.AAPL.3M.25D_PUT      → AAPL 3M 25-Delta Put Implied Vol
FX.SPOT.LEVEL.EURUSD                → EUR/USD Spot Rate
FX.VOL.SURFACE.USDJPY.1M.25D_RR    → USD/JPY 1M 25-Delta Risk Reversal
CMDTY.ENERGY.LEVEL.WTI.FRONT       → WTI Front Month Price
CMDTY.ENERGY.BASIS.BRENT_WTI.1M    → Brent-WTI 1M Basis
SECURITIZED.RMBS.PREPAY.AGENCY.30Y_CONV.CPR → Agency 30Y Conv CPR Assumption
```

Provide the complete enumeration catalog for each segment of the ID.

---

## STEP 5: MIGRATION & RECONCILIATION MAPPING

### 5.1 — Current-to-Target Mapping Table
For EVERY driver extracted in Step 1, provide the mapping:

| Current Model | Current Driver Name | Standard Driver ID | Mapping Quality | Changes Required | Notes |
|--------------|--------------------|--------------------|-----------------|------------------|-------|
| Rates RTM | USD Swap 10Y | RATES.SWAP.LEVEL.USD.10Y | Exact | Rename only | — |
| Credit RTM | IG OAS | CREDIT.IG.SPREAD.US.OAS.COMPOSITE | Granularity increase needed | Split by sector, tenor | Currently one number for all IG |
| ... | ... | ... | ... | ... | ... |

Mapping Quality categories: Exact, Minor Adjustment, Granularity Increase Needed, Granularity Decrease (Aggregation), New Driver Required, Driver Retirement, Methodology Change Required

### 5.2 — New Drivers Required
List every driver that the standard architecture requires but that does NOT exist in any current model. For each:
- Standard Driver ID
- Why it's needed (what risk is currently uncaptured)
- Data source recommendation
- Calibration approach
- Priority (Critical / High / Medium / Low)

### 5.3 — Drivers to Retire or Merge
List any current drivers that should be eliminated because:
- They're redundant (captured by another driver at better granularity)
- They're inconsistent with the standard taxonomy
- They capture a risk that belongs at a different hierarchy level
For each, specify what replaces it.

### 5.4 — Effort Assessment Matrix
For each asset class:

| Asset Class | Current Driver Count | Target Driver Count | Exact Matches | Minor Adjustments | Major Rework | New Build | Estimated Effort |
|-------------|---------------------|--------------------|--------------|--------------------|-------------|-----------|-----------------|

---

## STEP 6: FINAL DELIVERABLE — THE DRIVER BIBLE

Compile everything into one definitive reference document structured as:

1. **Executive Summary** — What the driver architecture is, why it matters, key design decisions, and the headline gap analysis
2. **Master Driver Catalog** — Every standardized driver with all metadata fields populated. This is the single source of truth. Organized by asset class, then by hierarchy level.
3. **Hierarchy Trees** — Visual tree diagrams for each asset class showing the full L1→L5 driver structure
4. **Propagation Rule Book** — Complete specification of how shocks flow through the hierarchy, with formulas, calibration methods, and override protocols
5. **Cross-Asset Linkage Map** — All cross-asset transmission channels with their specifications
6. **Dimension & Filter Reference** — Complete enumeration of every dimension, its valid values, and applicability by asset class
7. **Naming Convention Reference** — Full ID format spec with complete enumeration catalogs
8. **Current-to-Target Migration Map** — Every current driver mapped to its standardized equivalent
9. **Gap Analysis & Recommendations** — Prioritized list of inconsistencies, missing coverage, and required changes
10. **Appendix: Raw Extraction by Model** — Complete driver extraction tables from each individual RTM document

---

## OPERATING PRINCIPLES

- **EXHAUSTIVE EXTRACTION OVER SPEED.** Read every page of every document. If a driver is mentioned in a footnote, a table, an appendix, or buried in methodology text — capture it. The value of this work is proportional to its completeness.
- **PRESERVE ORIGINAL TERMINOLOGY** in the as-is extraction. Only introduce standardized names in the architecture. Always maintain traceability between original and standardized.
- **EVERY DRIVER GETS EVERY FIELD.** If a field cannot be populated from the document, mark it as "Not Specified — Requires Confirmation" rather than leaving it blank. This surfaces gaps.
- **QUESTION EVERYTHING.** If a model shocks credit spreads in percentage terms but the standard should be basis points, flag it. If two models define "short-term tenor" differently, flag it. If a proxy mapping seems fragile, say so.
- **THINK IN HIERARCHIES.** Every driver must have a home in the L0–L5 structure. If it doesn't fit cleanly, that reveals an architecture issue to solve, not a driver to ignore.
- **CROSS-REFERENCE RELENTLESSLY.** After extracting from each model, go back and check against every other model. Every shared risk factor should be reconciled. Every conflict should be surfaced.
- **DESIGN FOR BOTTOM-UP SHOCKING.** The architecture must support someone saying "I want to shock AAPL 3M 25-delta put implied vol by +5 vol points" AND someone saying "I want to shock all equity volatility by +30%" — and have both work within the same consistent framework.

---

## ATTACHED DOCUMENTS

The following Risk Treatment Model documents are attached for analysis:

[ATTACH YOUR RTM PDFs HERE]

Read every document completely before beginning output. Do not skim. Do not summarize from tables of contents. Extract from the full body text, appendices, and technical sections of each document.

---

*End of Prompt*
