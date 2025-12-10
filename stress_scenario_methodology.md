# Comprehensive Stress Scenario Design Methodology

## Executive Framework

This document establishes a systematic, reproducible methodology for designing, calibrating, and maintaining stress scenarios across all asset classes. The framework ensures consistency, granularity, and auditability while enabling both strategic (top-down) and tactical (bottom-up) scenario construction.

---

## 1. Core Design Philosophy

### 1.1 The Three Pillars

**Coherence**: Every scenario must tell a consistent economic narrative. Shocks cannot be arbitrary—they must reflect plausible causal relationships across markets.

**Completeness**: Every material risk driver in the portfolio must receive a shock. No gaps. This requires a complete risk driver taxonomy before scenario design begins.

**Calibration Integrity**: Severity levels must be anchored to empirical distributions or defensible hypothetical reasoning, never arbitrary.

### 1.2 The Dual-Direction Principle

Every well-designed scenario operates on two axes simultaneously:

```
TOP-DOWN (Strategic)          BOTTOM-UP (Tactical)
         ↓                           ↑
Macro Narrative            →    Risk Driver Shocks
(e.g., "Fed Pivot")              (e.g., 2Y TSY -85bp)
         ↓                           ↑
Asset Class Themes         →    Position-Level P&L
(e.g., "Risk-On")                Attribution
         ↓                           ↑
Factor Movements           →    Desk/Book Aggregation
(e.g., "Duration +, Credit -)
```

The two directions must reconcile. Top-down narrative implies bottom-up shocks; bottom-up shocks must aggregate to a coherent top-down story.

---

## 2. Hierarchical Scenario Architecture

### 2.1 The Four-Tier Structure

```
┌─────────────────────────────────────────────────────────────┐
│  TIER 1: MACRO SCENARIO (1 per scenario)                    │
│  "Global Risk-Off / Flight to Quality"                      │
│  - Economic narrative in plain language                     │
│  - Key macro assumptions (GDP, inflation, policy)           │
│  - Geographic scope (US, Global, EM-focused, etc.)          │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│  TIER 2: ASSET CLASS THEMES (5-10 per scenario)             │
│  Rates: Bull flattener, front-end rally                     │
│  Credit: Spread widening, IG outperforms HY                 │
│  Equities: -15% broad selloff, defensive rotation           │
│  FX: USD strength, EM weakness                              │
│  Commodities: Oil down (demand), Gold up (safe haven)       │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│  TIER 3: FACTOR/CURVE SHOCKS (50-200 per scenario)          │
│  USD Swap Curve: 2Y -85bp, 5Y -60bp, 10Y -45bp, 30Y -35bp   │
│  CDX.IG: +45bp, CDX.HY: +180bp                              │
│  SPX: -15%, VIX: +25 pts                                    │
│  EUR/USD: -5%, USD/JPY: -8%                                 │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│  TIER 4: GRANULAR RISK DRIVERS (1,000s-100,000s)            │
│  Individual issuer spreads, specific tenor points,          │
│  basis relationships, vol surface nodes, etc.               │
│  DERIVED from Tier 3 using propagation rules                │
└─────────────────────────────────────────────────────────────┘
```

### 2.2 Propagation Rules (Tier 3 → Tier 4)

This is where consistency is enforced. Granular shocks are **derived**, not independently specified.

**Method A: Beta-Based Propagation**
```
Shock(Driver_i) = Beta(Driver_i, Factor_j) × Shock(Factor_j)

Example:
- Factor: CDX.HY spread +180bp
- Driver: Ford 5Y CDS
- Beta(Ford, CDX.HY) = 1.15 (estimated from regression)
- Shock(Ford 5Y) = 1.15 × 180bp = 207bp
```

**Method B: Ratio-Based Propagation**
```
Shock(Driver_i) = (Current_Spread_i / Index_Spread) × Shock(Index)

Example:
- CDX.HY current spread: 400bp
- Ford 5Y current spread: 520bp
- Ratio: 520/400 = 1.30
- Shock(Ford 5Y) = 1.30 × 180bp = 234bp
```

**Method C: Rating/Sector Matrix**
```
Pre-defined shock multipliers by rating and sector:

              | IG-AAA | IG-A | IG-BBB | HY-BB | HY-B | HY-CCC |
--------------+--------+------+--------+-------+------+--------|
Financials    |  0.8   | 1.0  |  1.2   |  1.5  | 2.0  |  3.0   |
Industrials   |  0.7   | 0.9  |  1.1   |  1.4  | 1.8  |  2.8   |
Energy        |  0.9   | 1.1  |  1.4   |  1.8  | 2.5  |  4.0   |
Tech          |  0.6   | 0.8  |  1.0   |  1.3  | 1.7  |  2.5   |
```

### 2.3 Handling Idiosyncratic Drivers

Some risk drivers don't map cleanly to systematic factors. Handle via:

1. **Basis Preservation**: Maintain current basis relationships unless scenario specifically targets basis
2. **Worst-Case Override**: For tail scenarios, apply additional idiosyncratic shock (e.g., +20% on top of systematic)
3. **Liquidity Multiplier**: Less liquid names get amplified shocks (liquidity score × systematic shock)

---

## 3. Scenario Generation Methods

### 3.1 Method Taxonomy

| Method | Best For | Advantages | Limitations |
|--------|----------|------------|-------------|
| **Historical Replay** | Regulatory, Backtesting | Empirically grounded, internally consistent | Past ≠ future, missing novel risks |
| **Historical Analog** | Emerging situations | Leverages relevant precedent | Requires judgment on applicability |
| **Hypothetical Narrative** | Forward-looking, strategic | Captures novel risks | Requires expert calibration |
| **Algorithmic/Statistical** | Systematic coverage | Objective, reproducible | May miss narrative coherence |
| **Hybrid** | Production use | Combines strengths | More complex to implement |

### 3.2 Historical Replay Method

**Process:**
1. Select historical window (start date, end date)
2. Calculate actual changes in all risk factors over window
3. Apply those exact changes as scenario shocks

**Date Selection Framework:**

| Crisis Type | Recommended Window | Key Characteristics |
|-------------|-------------------|---------------------|
| Liquidity Crisis | 2008-09-15 to 2008-10-15 | Credit freeze, correlation spike |
| Rate Shock | 2022-09-22 to 2022-10-22 | Front-end selloff, curve inversion |
| EM Contagion | 1998-08-01 to 1998-09-30 | EM spreads, flight to quality |
| Flash Crash | 2010-05-06 (intraday) | Equity dislocation, vol spike |
| COVID Shock | 2020-02-20 to 2020-03-23 | All-asset correlation, liquidity |
| SVB/Regional Bank | 2023-03-08 to 2023-03-15 | Bank spreads, rate vol |

**Dynamic Lookback Calibration:**
```
For rolling historical scenarios:
- Lookback window: 250 days (1Y), 500 days (2Y), or 1250 days (5Y)
- Percentile selection: 99th, 99.5th, or 99.9th
- Apply: Use factor changes at selected percentile from lookback
```

### 3.3 Hypothetical Narrative Method

**Process:**
1. Define macro narrative (what happens and why)
2. Identify primary transmission channels
3. Set anchor shocks for key factors (based on historical analogs or expert judgment)
4. Derive secondary shocks using propagation rules
5. Validate internal consistency

**Narrative Construction Template:**

```
SCENARIO: [Name]
TRIGGER: [What initiates the stress]
TRANSMISSION: [How stress propagates through markets]
DURATION: [Instantaneous / 1-week / 1-month / 3-month]
GEOGRAPHIC SCOPE: [US / Global / Regional]

PRIMARY SHOCKS (Tier 3):
- [Factor 1]: [Shock] | Rationale: [Why this magnitude]
- [Factor 2]: [Shock] | Rationale: [Why this magnitude]

ASSET CLASS IMPACTS (Tier 2):
- Rates: [Theme]
- Credit: [Theme]
- Equities: [Theme]
- FX: [Theme]
- Commodities: [Theme]

CROSS-ASSET CONSISTENCY CHECK:
- [ ] Rate-equity relationship sensible?
- [ ] Credit-equity relationship sensible?
- [ ] FX-rate differentials sensible?
- [ ] Commodity-equity demand story sensible?
```

### 3.4 Algorithmic/Statistical Method

**Approach A: Principal Component Stress**
```
1. Perform PCA on historical factor returns
2. Shock PC1 (market direction) by X standard deviations
3. Optionally shock PC2 (curve shape), PC3 (sector rotation)
4. Transform back to original factor space
```

**Approach B: Conditional Stress**
```
1. Condition on anchor shock (e.g., SPX -20%)
2. Calculate conditional expectations: E[Factor_i | SPX = -20%]
3. Use conditional covariance for secondary shocks
4. Optionally add tail dependency adjustments
```

**Approach C: Reverse Stress Testing**
```
1. Define P&L threshold (e.g., -$500M)
2. Use optimization to find minimum-norm shock vector achieving threshold
3. Analyze: Is resulting scenario plausible? What are key drivers?
```

### 3.5 Hybrid Method (Recommended for Production)

```
STEP 1: Narrative Anchor
- Define macro story
- Set 3-5 anchor shocks for major indices/factors

STEP 2: Historical Calibration
- Find closest historical analog
- Use historical correlations for secondary shocks
- Scale to desired severity

STEP 3: Algorithmic Fill
- Propagate to granular drivers via beta/ratio methods
- Apply basis and liquidity adjustments

STEP 4: Expert Override
- SME review of key positions
- Override specific drivers if justified (document rationale)

STEP 5: Consistency Validation
- Check cross-asset relationships
- Verify aggregated P&L makes sense vs. narrative
```

---

## 4. Top-Down ↔ Bottom-Up Integration

### 4.1 Top-Down Flow (Strategy → Shocks)

```
┌─────────────────────────────────────────────────────────────┐
│  INPUT: Macro View / Risk Committee Direction               │
│  "We're concerned about a China hard landing"               │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│  TRANSLATION: Asset Class Implications                      │
│  - EM FX weakness (CNY -10%, EM basket -15%)                │
│  - Commodity demand shock (Oil -25%, Copper -30%)           │
│  - Risk-off in equities (SPX -12%, HSI -25%)                │
│  - Mild US rates rally (safe haven, 10Y -30bp)              │
│  - Credit: EM spreads +200bp, DM +50bp                      │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│  CALIBRATION: Anchor to Severity Level                      │
│  Moderate: 1-in-10 year event (Scale × 0.6)                 │
│  Severe: 1-in-25 year event (Scale × 1.0)                   │
│  Extreme: 1-in-100 year event (Scale × 1.5)                 │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│  PROPAGATION: Generate Granular Shocks                      │
│  Apply beta/ratio methods to derive 10,000+ driver shocks   │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│  OUTPUT: Complete Shock Vector for Pricing Engine           │
└─────────────────────────────────────────────────────────────┘
```

### 4.2 Bottom-Up Flow (Positions → Scenarios)

```
┌─────────────────────────────────────────────────────────────┐
│  INPUT: Current Position Inventory                          │
│  All trades, sensitivities, Greeks by risk driver           │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│  ANALYSIS: Identify Key Exposures                           │
│  - Largest DV01 concentrations                              │
│  - Biggest single-name exposures                            │
│  - Correlation/basis risks                                  │
│  - Convexity/gamma concentrations                           │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│  SCENARIO TARGETING: Design Position-Specific Stresses      │
│  "What scenario would stress our BBB energy concentration?" │
│  → Energy-specific credit stress with oil correlation       │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│  REVERSE VALIDATION: Does Scenario Have Macro Coherence?    │
│  Map bottom-up scenario back to plausible macro story       │
└─────────────────────────────────────────────────────────────┘
```

### 4.3 Reconciliation Process

When top-down and bottom-up don't align:

| Symptom | Diagnosis | Resolution |
|---------|-----------|------------|
| P&L doesn't match narrative severity | Propagation rules miscalibrated | Recalibrate betas, check basis assumptions |
| Scenario misses key position risk | Top-down too coarse | Add targeted factor to Tier 3 |
| Bottom-up scenario has no macro story | Idiosyncratic risk | Accept as separate scenario or find analog |
| Cross-asset P&L inconsistent | Correlation assumptions wrong | Review and adjust conditional relationships |

---

## 5. Cross-Asset Consistency Framework

### 5.1 The Consistency Matrix

Every scenario must pass this cross-asset logic check:

```
                    RISK-OFF              RISK-ON
                    ────────              ───────
Equities            Down                  Up
Credit Spreads      Wider                 Tighter
Rates (DM)          Down (safe haven)     Up (growth)
Vol (Equity)        Up                    Down
Vol (Rates)         Up initially          Down
FX (USD)            Up (flight)           Down
FX (EM)             Down                  Up
Commodities (Oil)   Down (demand)         Up
Commodities (Gold)  Up (safe haven)       Down
Correlations        Spike to 1            Normalize
```

### 5.2 Asset Class Specific Shock Design

#### Rates
```
CURVE DYNAMICS:
- Parallel: All tenors move same direction/magnitude
- Steepener: Long end sells off more (or short end rallies more)
- Flattener: Short end sells off more (or long end rallies more)
- Twist: Short and long move opposite directions

CALIBRATION ANCHORS:
- Fed Funds implied: Policy expectation
- 2Y: Near-term policy path
- 10Y: Growth/inflation expectations
- 30Y: Term premium, supply/demand

VOLATILITY SURFACE:
- ATM vol: Overall rate uncertainty
- Skew: Directional bias (payer vs receiver)
- Term structure: Near-term vs long-term uncertainty
```

#### Credit
```
SPREAD DYNAMICS:
- Systematic (beta to index)
- Sector rotation (financials vs industrials vs energy)
- Quality rotation (IG vs HY, rating migration)
- Curve shape (short spread vs long spread)

CALIBRATION ANCHORS:
- CDX.IG: Investment grade benchmark
- CDX.HY: High yield benchmark
- ITRAXX: European credit
- EM sovereign: Emerging markets

CONSISTENCY RULES:
- HY/IG ratio typically expands in stress (HY underperforms)
- Subordinated widens more than senior
- Short-dated can gap more (jump-to-default)
- Basis (cash vs CDS) can blow out in liquidity stress
```

#### Equities
```
DYNAMICS:
- Index level (beta 1)
- Sector rotation (cyclicals vs defensives)
- Factor rotation (value vs growth, small vs large)
- Single-stock idiosyncratic

VOLATILITY SURFACE:
- ATM implied vol
- Skew (put premium)
- Term structure (near vs far expiry)
- Vol-of-vol (correlation with spot)

CONSISTENCY RULES:
- Vol typically rises 4-6 points per 1% spot decline
- Skew steepens in selloffs
- Correlation increases in stress
- Dividend expectations may need adjustment
```

#### FX
```
DYNAMICS:
- Spot rate
- Forward points (interest rate differential)
- Volatility surface

CONSISTENCY RULES:
- Rate differential changes → forward point adjustment
- Risk-off → USD, JPY, CHF strength
- Risk-on → EM, commodity currency strength
- Carry trade unwind → high-yield currency weakness
```

#### Commodities
```
DYNAMICS:
- Spot price
- Curve shape (contango/backwardation)
- Volatility

CONSISTENCY RULES:
- Demand shock → oil, copper down together
- Supply shock → specific commodity spikes, others stable
- Risk-off → gold up, industrial metals down
- Inflation shock → broad commodity strength
```

### 5.3 Cross-Asset Correlation Matrix (Stress Regime)

Default correlations to apply when designing scenarios:

```
              | SPX   | UST10Y | CDX.HY | EURUSD | WTI   | VIX   |
--------------+-------+--------+--------+--------+-------+-------|
SPX           | 1.00  |        |        |        |       |       |
UST10Y (px)   | -0.40 | 1.00   |        |        |       |       |
CDX.HY (sprd) | -0.75 | 0.30   | 1.00   |        |       |       |
EURUSD        | 0.50  | -0.20  | -0.40  | 1.00   |       |       |
WTI           | 0.55  | -0.15  | -0.45  | 0.35   | 1.00  |       |
VIX           | -0.80 | 0.35   | 0.70   | -0.40  | -0.45 | 1.00  |
```

*Note: These are STRESS correlations. Normal correlations are lower in absolute value.*

---

## 6. Severity & Horizon Calibration

### 6.1 Severity Framework

| Level | Probability | Approx. Return Period | Historical Analog |
|-------|-------------|----------------------|-------------------|
| Mild | 10-20% | 5-10 years | 2011 Euro crisis |
| Moderate | 5-10% | 10-20 years | 2015-16 China deval |
| Severe | 1-5% | 20-100 years | 2008 GFC |
| Extreme | <1% | >100 years | 1929, theoretical |

### 6.2 Calibrating to Severity

**Statistical Approach:**
```
1. Calculate historical distribution of factor returns
2. Select percentile corresponding to desired severity:
   - Moderate: 95th-99th percentile
   - Severe: 99th-99.9th percentile
   - Extreme: 99.9th+ percentile
3. Use percentile shock as anchor, propagate to other factors
```

**Analog Scaling Approach:**
```
1. Select historical event as baseline (e.g., 2008 GFC)
2. Define scaling factors:
   - Moderate: 0.5-0.7× GFC
   - Severe: 1.0× GFC
   - Extreme: 1.3-1.5× GFC
3. Apply scaling to all shocks in analog
```

**Expert Calibration Approach:**
```
1. Gather SME estimates for key anchors
2. Use Delphi method or structured elicitation
3. Document rationale and confidence intervals
4. Cross-check against historical and statistical bounds
```

### 6.3 Time Horizon Framework

| Horizon | Duration | Use Case | Characteristics |
|---------|----------|----------|-----------------|
| Instantaneous | 1 day | Trading limits, VaR | Assumes no management action |
| Short-term | 1-2 weeks | Liquidity stress | Limited management action |
| Medium-term | 1-3 months | Capital planning | Partial de-risking possible |
| Long-term | 1 year+ | Strategic planning | Full management response |

**Horizon-Specific Adjustments:**

```
INSTANTANEOUS (1-day):
- Full shock magnitude
- No mean reversion
- No management action
- Liquidity impact at maximum

SHORT-TERM (1-2 weeks):
- Shock may intensify initially then stabilize
- Partial bid-offer widening
- Limited hedging possible
- Margin calls crystallize

MEDIUM-TERM (1-3 months):
- Shock may mean-revert partially
- Credit events may realize
- Significant position adjustment possible
- Funding costs elevated

LONG-TERM (1 year):
- Consider second-order effects
- Business mix may change
- Regulatory response possible
- Economic recovery path
```

### 6.4 Dynamic Horizon Shocks

For multi-period scenarios, define shock path:

```
Example: "Slow Burn Credit Crisis"

Month 1: CDX.HY +50bp, SPX -5%
Month 2: CDX.HY +100bp (cumulative), SPX -8%
Month 3: CDX.HY +180bp (cumulative), SPX -15%
Month 4: Peak stress, CDX.HY +200bp, SPX -18%
Month 5: Partial recovery, CDX.HY +150bp, SPX -12%
Month 6: New equilibrium, CDX.HY +100bp, SPX -8%
```

---

## 7. Recalibration & Maintenance

### 7.1 Recalibration Triggers

| Trigger | Action Required |
|---------|-----------------|
| Quarterly cycle | Review all severity calibrations |
| Vol regime change | Update shock magnitudes (high vol → larger shocks) |
| Correlation breakdown | Review propagation betas |
| New risk factor | Add to taxonomy, define propagation rules |
| Major market event | Add as new historical analog, recalibrate bounds |
| Position change >20% | Review scenario coverage |

### 7.2 Recalibration Process

**Statistical Recalibration (Quarterly):**
```
1. Update lookback windows with latest data
2. Recalculate percentile shocks
3. Recalculate factor betas for propagation
4. Compare new vs old shocks
5. Document and approve material changes (>10% difference)
```

**Correlation Recalibration:**
```
1. Estimate rolling correlations (60-day, 250-day windows)
2. Compare current regime to stress regime assumptions
3. If normal correlations approaching stress levels → caution flag
4. Update stress correlation matrix if structural change evident
```

**Beta Recalibration:**
```
For each granular driver i and factor j:
1. Run regression: Return_i = α + β × Return_j + ε
2. Use recent window (1Y) weighted toward stressed periods
3. Update propagation beta if |Δβ| > 0.1
4. Document stability of beta estimate (R², SE)
```

### 7.3 Governance & Documentation

**Scenario Approval Workflow:**
```
1. Designer creates scenario (Analyst)
2. Technical review (Quant/Model team)
3. Business review (Desk heads, SMEs)
4. Risk sign-off (Senior Risk Manager)
5. Documentation in scenario library
6. Version control with change log
```

**Required Documentation:**
```
For each scenario:
- [ ] Narrative description (plain language)
- [ ] Tier 1-4 shock specifications
- [ ] Calibration methodology and sources
- [ ] Historical analog reference (if applicable)
- [ ] Propagation rules applied
- [ ] Override log (any manual adjustments)
- [ ] Validation results (P&L attribution, consistency checks)
- [ ] Approval chain
- [ ] Last recalibration date
- [ ] Next review date
```

---

## 8. Implementation Tool Architecture

### 8.1 System Components

```
┌─────────────────────────────────────────────────────────────────┐
│                    SCENARIO DESIGN PLATFORM                      │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │  SCENARIO    │  │  CALIBRATION │  │  PROPAGATION │          │
│  │  BUILDER     │  │  ENGINE      │  │  ENGINE      │          │
│  │              │  │              │  │              │          │
│  │ - Narrative  │  │ - Historical │  │ - Beta maps  │          │
│  │ - Tier 1-3   │  │ - Statistical│  │ - Ratio maps │          │
│  │ - Templates  │  │ - Analog     │  │ - Matrix     │          │
│  │ - Validation │  │ - Expert     │  │ - Override   │          │
│  └──────────────┘  └──────────────┘  └──────────────┘          │
│         │                 │                 │                   │
│         └────────────────┼────────────────┘                    │
│                          │                                      │
│                          ▼                                      │
│              ┌──────────────────────┐                          │
│              │   RISK DRIVER        │                          │
│              │   TAXONOMY           │                          │
│              │   (Master List)      │                          │
│              └──────────────────────┘                          │
│                          │                                      │
│                          ▼                                      │
│              ┌──────────────────────┐                          │
│              │   SHOCK VECTOR       │                          │
│              │   GENERATOR          │                          │
│              │   (Output File)      │                          │
│              └──────────────────────┘                          │
│                          │                                      │
│         ┌────────────────┼────────────────┐                    │
│         ▼                ▼                ▼                    │
│  ┌──────────────┐ ┌──────────────┐ ┌──────────────┐           │
│  │  PRICING     │ │  P&L         │ │  REPORTING   │           │
│  │  ENGINE      │ │  AGGREGATION │ │  & ANALYTICS │           │
│  │  INTERFACE   │ │              │ │              │           │
│  └──────────────┘ └──────────────┘ └──────────────┘           │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 8.2 Key Data Structures

**Scenario Definition Object:**
```json
{
  "scenario_id": "SCN-2024-0042",
  "name": "China Hard Landing",
  "version": "2.1",
  "status": "approved",
  "effective_date": "2024-01-15",
  "narrative": {
    "description": "Severe economic contraction in China...",
    "trigger": "Property sector collapse spreads to broader economy",
    "transmission": "EM contagion, commodity demand shock, risk-off",
    "duration": "3-month stress horizon"
  },
  "severity": {
    "level": "severe",
    "probability": "1-in-25 year",
    "historical_analog": "2015 China devaluation scaled 2.5x"
  },
  "tier_2_themes": {
    "rates": "DM bull flattener, EM rates selloff",
    "credit": "EM +200bp, DM HY +100bp, IG +30bp",
    "equities": "SPX -12%, HSI -25%, EM -20%",
    "fx": "USD +5%, CNY -10%, EM basket -15%",
    "commodities": "Oil -25%, Copper -30%, Gold +8%"
  },
  "tier_3_shocks": [
    {"factor": "SPX", "shock": -0.12, "unit": "pct"},
    {"factor": "UST_2Y", "shock": -0.0035, "unit": "bp"},
    {"factor": "CDX_HY", "shock": 100, "unit": "bp"},
    // ... 100+ factor shocks
  ],
  "propagation_config": {
    "credit_method": "beta",
    "rates_method": "curve_model",
    "equity_method": "beta_to_sector"
  },
  "overrides": [
    {
      "driver": "CHINA_SOV_5Y",
      "override_shock": 150,
      "rationale": "Direct sovereign exposure to scenario trigger"
    }
  ],
  "validation": {
    "consistency_check": "pass",
    "p&l_attribution": "validated",
    "last_validated": "2024-01-10"
  },
  "governance": {
    "created_by": "jsmith",
    "approved_by": "mwilliams",
    "approval_date": "2024-01-12"
  }
}
```

**Risk Driver Taxonomy:**
```json
{
  "driver_id": "USD_SWAP_5Y",
  "asset_class": "rates",
  "sub_class": "usd_swaps",
  "tenor": "5Y",
  "factor_mappings": [
    {"factor": "UST_5Y", "beta": 1.02, "method": "regression"},
    {"factor": "SWAP_SPREAD_5Y", "beta": 1.00, "method": "direct"}
  ],
  "data_source": "Bloomberg",
  "last_calibration": "2024-01-01",
  "calibration_window": "2Y"
}
```

### 8.3 Workflow Automation

**Scenario Generation Pipeline:**
```
INPUT: Scenario template + parameters
  │
  ├─► [1] Load narrative and Tier 2 themes
  │
  ├─► [2] Fetch calibration data
  │       - Historical distributions
  │       - Current market levels
  │       - Beta estimates
  │
  ├─► [3] Generate Tier 3 factor shocks
  │       - Apply severity scaling
  │       - Apply horizon adjustments
  │
  ├─► [4] Propagate to Tier 4 drivers
  │       - Apply propagation rules
  │       - Apply overrides
  │
  ├─► [5] Validate consistency
  │       - Cross-asset checks
  │       - Sign and magnitude checks
  │
  ├─► [6] Generate shock vector file
  │
  └─► OUTPUT: Scenario package ready for pricing
```

### 8.4 Recalibration Automation

```
SCHEDULED: Quarterly / On-Trigger

[1] Pull latest market data
    - Factor returns (1Y, 2Y, 5Y windows)
    - Correlation matrices
    
[2] Recalculate statistical parameters
    - Percentile shocks
    - Regression betas
    - Correlation estimates
    
[3] Compare to current scenario library
    - Flag material changes (>10%)
    - Generate recalibration report
    
[4] Route for review
    - Automated changes below threshold
    - Human review above threshold
    
[5] Update scenario library
    - Version increment
    - Audit trail
```

---

## 9. Scenario Library Structure

### 9.1 Standard Scenario Categories

**Regulatory/Required:**
- Fed Supervisory Severely Adverse
- Fed Supervisory Adverse
- Fed Supervisory Baseline
- CCAR Company-Run Scenarios
- Internal Stress Testing (Dodd-Frank)

**Market Risk Core:**
- Rates Parallel Up/Down
- Rates Steepener/Flattener
- Rates Twist
- Credit Spread Widening (IG, HY)
- Equity Selloff
- Equity Crash (-20%+)
- FX Major Moves (USD strength, weakness)
- Commodity Shocks (Oil, Gold)
- Volatility Spike

**Macro Themes:**
- Stagflation
- Deflation/Recession
- Growth Surprise (positive shock)
- Fed Policy Error (too tight, too loose)
- Geopolitical Crisis
- EM Contagion

**Tail/Extreme:**
- Correlation Breakdown
- Liquidity Crisis
- Counterparty Failure
- Sovereign Default
- Black Swan (novel, severe)

### 9.2 Naming Convention

```
[CATEGORY]-[THEME]-[SEVERITY]-[HORIZON]-[VERSION]

Examples:
REG-CCAR-ADVERSE-9M-v2024Q1
MKT-RATES-FLATNER-SEV-1M-v2.1
MACRO-STAGFLATION-MOD-3M-v1.0
TAIL-LIQCRISIS-EXT-1W-v1.2
```

---

## 10. Quick Reference: Scenario Design Checklist

### Pre-Design
- [ ] Define scenario objective (regulatory, risk management, strategic)
- [ ] Identify target portfolio/positions
- [ ] Select severity level and horizon
- [ ] Choose generation method (historical, hypothetical, hybrid)

### Design
- [ ] Write Tier 1 macro narrative
- [ ] Define Tier 2 asset class themes
- [ ] Calibrate Tier 3 factor shocks
- [ ] Select propagation method for Tier 4
- [ ] Document any overrides with rationale

### Validation
- [ ] Cross-asset consistency check (signs, magnitudes)
- [ ] P&L attribution makes sense vs. narrative
- [ ] Severity appropriate for stated probability
- [ ] No missing material risk drivers
- [ ] Correlation assumptions documented

### Approval
- [ ] Technical review complete
- [ ] Business review complete
- [ ] Documentation complete
- [ ] Version controlled in library
- [ ] Recalibration schedule set

---

## Appendix A: Historical Shock Reference Table

| Event | Date Range | SPX | UST 10Y | CDX.HY | VIX | EUR/USD | WTI |
|-------|------------|-----|---------|--------|-----|---------|-----|
| GFC Peak | Sep-Nov 2008 | -40% | -100bp | +800bp | +50 | -10% | -55% |
| Flash Crash | May 6, 2010 | -9% (intraday) | -15bp | +40bp | +20 | -2% | -3% |
| Euro Crisis | Jul-Sep 2011 | -17% | -80bp | +250bp | +25 | -8% | -15% |
| China Deval | Aug-Sep 2015 | -12% | -30bp | +100bp | +20 | +1% | -20% |
| COVID Crash | Feb-Mar 2020 | -34% | -100bp | +550bp | +65 | +2% | -65% |
| 2022 Rate Shock | Sep-Oct 2022 | -15% | +80bp | +120bp | +15 | -6% | -10% |
| SVB Crisis | Mar 2023 | -5% | -50bp | +60bp | +10 | +2% | -10% |

---

## Appendix B: Propagation Beta Reference

### Credit Betas to CDX Indices

| Rating | CDX.IG Beta | CDX.HY Beta |
|--------|-------------|-------------|
| AAA | 0.5 | 0.2 |
| AA | 0.7 | 0.3 |
| A | 0.9 | 0.4 |
| BBB | 1.1 | 0.6 |
| BB | 1.5 | 0.9 |
| B | 2.0 | 1.1 |
| CCC | 3.0 | 1.5 |

### Equity Sector Betas to SPX

| Sector | Normal Beta | Stress Beta |
|--------|-------------|-------------|
| Technology | 1.15 | 1.25 |
| Financials | 1.10 | 1.40 |
| Energy | 1.05 | 1.30 |
| Consumer Disc. | 1.10 | 1.20 |
| Industrials | 1.05 | 1.15 |
| Healthcare | 0.80 | 0.85 |
| Utilities | 0.50 | 0.55 |
| Consumer Staples | 0.65 | 0.70 |

---

## Appendix C: Severity Scaling Quick Reference

### Moderate (1-in-10 year)
- SPX: -8% to -12%
- UST 10Y: ±40-60bp
- CDX.HY: +80-120bp
- VIX: +12-18 pts
- Major FX: ±4-6%

### Severe (1-in-25 year)
- SPX: -15% to -22%
- UST 10Y: ±70-100bp
- CDX.HY: +150-250bp
- VIX: +25-35 pts
- Major FX: ±8-12%

### Extreme (1-in-100 year)
- SPX: -30% to -45%
- UST 10Y: ±100-150bp
- CDX.HY: +400-800bp
- VIX: +50-70 pts
- Major FX: ±15-25%

---

*Document Version: 1.0*
*Framework Owner: Market Risk*
*Last Updated: [Current Date]*
*Next Review: Quarterly*
