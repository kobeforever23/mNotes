# Stress Scenario Propagation & Formatting Prompts

A collection of prompts to propagate driver-level shocks to granular risk factors, validate cohesiveness, and generate narratives.

---

## PROMPT 1: Master Propagation Prompt (Full Scenario)

```
You are a senior Market Risk Quantitative Analyst tasked with propagating a stress scenario from high-level driver shocks down to granular risk factor shocks suitable for Schedule F / FR Y-14Q submission.

## SCENARIO CONTEXT

**Scenario Name:** AI Bubble Correction Stress Scenario
**Horizons:** Moderate (10 trading days) | Severe (60 trading days)

**Fixed Binding Constraints:**
- AI Single Names (NVDA, AMD, AVGO): -40% (Mod) / -50% (Sev)
- AI Utilities (VST, CEG): -15% (Mod) / -30% (Sev)

**Derived Index Shocks:**
- S&P 500: -22% (Mod) / -33% (Sev)
- QQQ (NDX): -30% (Mod) / -43% (Sev)
- VIX: 38 (Mod) / 58 (Sev)
- IG OAS: +100bp (Mod) / +200bp (Sev)
- HY OAS: +180bp (Mod) / +420bp (Sev)
- UST 10Y: -40bp (Mod) / -80bp (Sev)
- DXY: +3.5% (Mod) / +7% (Sev)

## YOUR TASK

Take the above driver-level shocks and propagate them to ALL granular risk factors needed for a complete stress test. You must:

### 1. PROPAGATION REQUIREMENTS

**Equity Factors:**
- All S&P 500 sector indices (GICS Level 1)
- All S&P 500 industry groups (GICS Level 2)
- Individual single names for top 50 by market cap
- Small-cap / mid-cap index shocks (Russell 2000, S&P 400)
- International equity indices (STOXX 600, Nikkei, MSCI EM)

**Rates Factors:**
- Full UST curve (1M, 3M, 6M, 1Y, 2Y, 3Y, 5Y, 7Y, 10Y, 20Y, 30Y)
- USD Swap curve (same tenors)
- SOFR curve (1M, 3M, 6M, 1Y)
- Inflation breakevens (5Y, 10Y, 30Y TIPS spreads)
- Mortgage spreads (30Y FNCL, GNMA)

**Credit Factors:**
- OAS by rating (AAA, AA, A, BBB, BB, B, CCC)
- OAS by sector (Financials, Tech, Healthcare, Energy, Consumer, Industrials, Utilities)
- OAS by tenor (1Y, 3Y, 5Y, 7Y, 10Y, 30Y)
- CDX/iTraxx indices (IG, HY, Main, Xover) with term structure
- Single-name CDS for top 20 AI-exposed issuers

**Volatility Factors:**
- VIX term structure (1W, 1M, 2M, 3M, 6M, 1Y)
- SPX vol surface (10d, 25d, ATM, 75d, 90d puts/calls by expiry)
- Single-name IV for Mag-7 and top 20 AI names
- MOVE index and swaption vol grid
- FX vol (major pairs 1M, 3M, 1Y)

**FX Factors:**
- All G10 pairs vs USD
- Major EM pairs (CNY, MXN, BRL, INR, KRW, TWD)
- FX forward points (1M, 3M, 6M, 1Y)

**Commodity Factors:**
- Energy (WTI, Brent, Nat Gas, RBOB)
- Metals (Gold, Silver, Copper, Aluminum)
- Agriculture (Corn, Wheat, Soybeans) if relevant

### 2. OUTPUT FORMAT

For EACH risk factor, provide in this exact format:

| DRIVER_ID | DRIVER_NAME | ASSET_CLASS | SECTOR | TENOR | CURRENT | MOD_SHOCK | MOD_LEVEL | SEV_SHOCK | SEV_LEVEL | PROPAGATION_SOURCE | BETA | RATIONALE |
|-----------|-------------|-------------|--------|-------|---------|-----------|-----------|-----------|-----------|-------------------|------|-----------|

Where:
- DRIVER_ID: Unique identifier (e.g., EQ.SPX.TECH, CR.IG.5Y.TECH, VOL.NVDA.1M.25D)
- PROPAGATION_SOURCE: Which parent driver this derives from
- BETA: Sensitivity to parent driver
- RATIONALE: 1-sentence explanation

### 3. COHESIVENESS VALIDATION

After producing the shock grid, validate:

**A. Cross-Asset Consistency:**
- If SPX -22%, then sector sum weighted = -22%
- If VIX 38, then single-name vols must be internally consistent
- Credit widening must match equity decline via credit-equity beta

**B. Sign Convention:**
- Risk-off: Equities ↓, Credit spreads ↑, VIX ↑, UST yields ↓, USD ↑, Gold ↑
- Flag ANY violations

**C. Monotonicity:**
- |Severe| ≥ |Moderate| for all factors
- Flag ANY violations

**D. Historical Plausibility:**
- Compare to COVID Mar 2020, GFC 2008, Q4 2018
- Flag ANY shocks outside 0.5x - 2.0x historical range

### 4. NARRATIVE SUMMARY

Provide:
1. **Executive Summary** (1 paragraph) - What is this scenario and why
2. **Transmission Mechanism** - How shocks propagate across asset classes
3. **By Asset Class Summary** - 2-3 sentences each for Equity, Rates, Credit, Vol, FX, Commodities
4. **Key Risks & Sensitivities** - What assumptions matter most
5. **Limitations** - What this scenario does NOT capture

### 5. DELIVERABLES

1. Complete shock grid in table format (Excel-ready)
2. Validation report with pass/fail for each check
3. Narrative document
4. Driver hierarchy diagram showing propagation flow
```

---

## PROMPT 2: Equity-Specific Propagation

```
You are an Equity Risk Specialist. Given the following high-level equity shocks, propagate to granular equity risk factors.

## INPUT SHOCKS

| Index | Moderate | Severe |
|-------|----------|--------|
| S&P 500 | -22% | -33% |
| QQQ (NDX) | -30% | -43% |
| AI Single Names | -40% | -50% |
| AI Utilities | -15% | -30% |

## PROPAGATION REQUIREMENTS

### 1. SECTOR INDICES (GICS Level 1)
Propagate to all 11 S&P 500 sectors. Use sector betas and AI-exposure weights:

| Sector | SPX Weight | AI Exposure | Expected Beta |
|--------|------------|-------------|---------------|
| Info Tech | 32% | High | 1.3-1.5x |
| Comm Services | 9% | High | 1.2-1.4x |
| Consumer Disc | 10% | Medium | 1.1-1.3x |
| Financials | 13% | Low | 0.9-1.1x |
| Healthcare | 12% | Low | 0.7-0.9x |
| Industrials | 8% | Medium | 1.0-1.2x |
| Consumer Staples | 6% | Low | 0.5-0.7x |
| Energy | 4% | Low | 0.8-1.0x |
| Utilities | 2% | Medium (AI power) | 0.6-0.8x |
| Materials | 2% | Low | 0.9-1.1x |
| Real Estate | 2% | Low | 0.8-1.0x |

### 2. SINGLE NAME SHOCKS
Provide shocks for:
- All Magnificent 7
- Top 20 semiconductor names
- Top 10 AI software names
- Top 5 AI utility/power names
- Top 20 by SPX weight (remaining)

Include: Ticker, Name, Sector, SPX Weight, Beta, Current Price, Mod Shock, Sev Shock

### 3. OTHER INDICES
Derive shocks for:
- Russell 2000 (small cap)
- S&P 400 (mid cap)
- STOXX 600 (Europe)
- Nikkei 225 (Japan)
- MSCI EM
- Hang Seng
- KOSPI

### 4. OUTPUT FORMAT

```
DRIVER_ID,NAME,SECTOR,WEIGHT,BETA_SPX,CURRENT,MOD_SHOCK,MOD_LEVEL,SEV_SHOCK,SEV_LEVEL,RATIONALE
EQ.NVDA,NVIDIA,Info Tech,8.0%,1.65,184.50,-40%,110.70,-50%,92.25,AI infrastructure leader - direct exposure
EQ.XLK,Tech Select Sector,Info Tech,32%,1.35,225.80,-30%,158.06,-43%,128.71,Weighted avg of tech constituents
...
```

### 5. VALIDATION

Prove that:
1. Σ(sector_weight × sector_shock) = SPX shock (±1%)
2. Tech sector shock > SPX shock (AI-led)
3. Defensive sectors (Staples, Healthcare, Utilities) shock < SPX shock
4. Single name shocks respect beta relationships

Provide validation table showing expected vs actual.
```

---

## PROMPT 3: Rates & Credit Propagation

```
You are a Fixed Income Risk Specialist. Propagate the following rates and credit shocks to full curve granularity.

## INPUT SHOCKS

**Rates:**
| Driver | Current | Moderate | Severe |
|--------|---------|----------|--------|
| UST 10Y | 4.18% | -40bp | -80bp |
| UST 2Y | 3.54% | -50bp | -100bp |
| 2s10s | 64bp | +10bp | +20bp |

**Credit:**
| Driver | Current | Moderate | Severe |
|--------|---------|----------|--------|
| IG OAS | 82bp | +100bp | +200bp |
| HY OAS | 276bp | +180bp | +420bp |

**Context:** Flight-to-quality driven by AI equity correction. Fed cut expectations rise.

## PROPAGATION REQUIREMENTS

### 1. RATES CURVE GRANULARITY

**UST Curve:**
Provide shocks for: 1M, 3M, 6M, 1Y, 2Y, 3Y, 5Y, 7Y, 10Y, 20Y, 30Y

Use curve shape assumptions:
- Front end rallies most (Fed cut expectations)
- Long end rallies less (inflation concerns persist)
- Curve steepens

**Swap Curve:**
Same tenors, with swap spread assumptions (typically widen 5-15bp in stress)

**SOFR/OIS:**
1M, 3M, 6M, 1Y SOFR + Fed Funds implied path

### 2. CREDIT GRANULARITY

**By Rating:**
| Rating | Current OAS | Beta to IG | Beta to HY |
|--------|-------------|------------|------------|
| AAA | 45bp | 0.7x | — |
| AA | 55bp | 0.8x | — |
| A | 70bp | 0.9x | — |
| BBB | 115bp | 1.2x | — |
| BB | 185bp | — | 0.8x |
| B | 320bp | — | 1.0x |
| CCC | 850bp | — | 1.5x |

**By Sector:**
Provide OAS shocks for: Financials, Tech, Healthcare, Energy, Consumer, Industrials, Utilities, Communications

Tech/Semi sector should have 1.3-1.5x beta to broad IG/HY

**By Tenor:**
1Y, 3Y, 5Y, 7Y, 10Y, 30Y for both IG and HY

**CDX/iTraxx:**
- CDX IG 5Y, 10Y
- CDX HY 5Y
- iTraxx Main 5Y, 10Y
- iTraxx Xover 5Y

### 3. OUTPUT FORMAT

```
DRIVER_ID,CURVE,TENOR,RATING,SECTOR,CURRENT,MOD_SHOCK,MOD_LEVEL,SEV_SHOCK,SEV_LEVEL,RATIONALE
RT.UST.1M,UST,1M,,,4.32%,-15bp,4.17%,-30bp,4.02%,Fed cut pricing
RT.UST.30Y,UST,30Y,,,4.82%,-35bp,4.47%,-70bp,4.12%,Flight to quality dampened by supply
CR.IG.5Y.TECH,Corporate,5Y,A,Tech,68bp,+120bp,188bp,+280bp,348bp,AI correction hits tech credit
...
```

### 4. VALIDATION

1. Verify curve shape is monotonic (no inversions beyond 2s10s)
2. Verify credit-equity relationship: CR_shock ≈ EQ_shock × credit_equity_beta
3. Verify rating hierarchy: CCC shock > B > BB > BBB > A > AA > AAA
4. Verify sector hierarchy: Tech > Financials > Industrials > Utilities
```

---

## PROMPT 4: Volatility Surface Propagation

```
You are a Volatility Derivatives Specialist. Propagate VIX and vol shocks to full surface granularity.

## INPUT SHOCKS

| Driver | Current | Moderate | Severe |
|--------|---------|----------|--------|
| VIX (SPX 1M ATM) | 16.5 | 38 | 58 |
| VVIX | 95 | 130 | 160 |
| MOVE | 98 | 133 | 160 |
| SPX | — | -22% | -33% |

## PROPAGATION REQUIREMENTS

### 1. VIX TERM STRUCTURE

Propagate to: 1W, 2W, 1M, 2M, 3M, 6M, 9M, 1Y

In stress:
- Front month spikes most (panic)
- Term structure inverts (M1 > M2 > M3)
- Back months rise but less

### 2. SPX VOL SURFACE

**By Delta:**
- 10-delta put
- 25-delta put
- ATM (50-delta)
- 25-delta call
- 10-delta call

**By Expiry:**
- 1 week
- 2 weeks
- 1 month
- 2 months
- 3 months
- 6 months
- 1 year

**Skew Behavior:**
- Put skew steepens in stress (downside protection demand)
- 25d put skew: +4 pts (Mod), +7 pts (Sev)
- 10d put skew: +6 pts (Mod), +12 pts (Sev)

### 3. SINGLE NAME VOL

Provide IV shocks for:
- All Magnificent 7
- Top 10 semiconductor names
- Top 5 AI software names

Use vol-spot beta:
- AI names: 2.8-3.5x
- Mega-cap diversified: 2.0-2.5x
- Defensive: 1.5-2.0x

### 4. RATES VOLATILITY

**MOVE Index:** As given
**Swaption Vol Grid:**
- Expiries: 1M, 3M, 6M, 1Y
- Tails: 2Y, 5Y, 10Y, 30Y

### 5. OUTPUT FORMAT

```
DRIVER_ID,UNDERLYING,EXPIRY,DELTA,CURRENT_IV,MOD_IV,MOD_CHANGE,SEV_IV,SEV_CHANGE,RATIONALE
VOL.SPX.1M.ATM,SPX,1M,50d,16.5%,38%,+21.5pts,58%,+41.5pts,VIX proxy
VOL.SPX.1M.25DP,SPX,1M,25d put,21.0%,46.5%,+25.5pts,69%,+48pts,Skew steepens +4pts
VOL.SPX.3M.ATM,SPX,3M,50d,17.8%,32%,+14.2pts,48%,+30.2pts,Term structure inversion
VOL.NVDA.1M.ATM,NVDA,1M,50d,48%,80%,+32pts,100%,+52pts,AI leader vol spike
...
```

### 6. VALIDATION

1. Term structure: VIX_1M > VIX_3M > VIX_6M in stress (inversion)
2. Skew: Put vol > ATM vol > Call vol
3. Vol-spot beta: Δvol / Δspot ≈ stated beta
4. Single-name vol > Index vol (idiosyncratic risk)
```

---

## PROMPT 5: Cohesiveness & Validation Prompt

```
You are a Model Validation Specialist. Given a complete stress scenario shock grid, validate internal consistency and cohesiveness.

## VALIDATION FRAMEWORK

### 1. CROSS-ASSET CONSISTENCY CHECKS

**Check A: Equity Index Decomposition**
```
Σ(sector_weight × sector_shock) = index_shock (±1%)
```
Run for: SPX, QQQ, Russell 2000

**Check B: Credit-Equity Relationship**
```
Credit_shock ≈ Equity_shock × credit_equity_beta × multiplier

Expected betas:
- IG: 0.4-0.5x
- HY: 0.6-0.7x
- Tech credit: 1.3-1.5x index beta
```

**Check C: Vol-Spot Relationship**
```
VIX_change ≈ SPX_decline × vol_spot_beta

Expected: 2.5-4.0 points VIX per 1% SPX decline
```

**Check D: Rates-Equity Relationship**
```
In risk-off: Rates ↓ (flight to quality)
UST_10Y_change should be negative when SPX negative
```

**Check E: FX-Risk Relationship**
```
USD should strengthen (DXY ↑) in risk-off
Risk currencies (AUD, EM) should weaken
Safe havens (JPY, CHF) behavior depends on carry unwind
```

### 2. SIGN CONVENTION VALIDATION

| Asset Class | Expected Sign in Risk-Off |
|-------------|---------------------------|
| Equity indices | Negative (↓) |
| Credit spreads | Positive (widen ↑) |
| VIX/Vol | Positive (↑) |
| UST yields | Negative (↓) |
| DXY | Positive (↑) |
| Gold | Positive (↑) |
| Oil | Negative (demand fears ↓) |
| Risk FX (AUD, EM) | Negative vs USD |

Flag ANY violations with explanation.

### 3. MONOTONICITY VALIDATION

For EVERY driver:
```
|Severe_shock| ≥ |Moderate_shock|
```

Exception: Rates can have non-monotonic curve shape changes.

### 4. HISTORICAL PLAUSIBILITY

Compare each shock to historical episodes:
- COVID March 2020
- GFC October 2008
- Q4 2018
- 2022 Tech Selloff
- Dot-Com 2000-2002

Flag if shock is:
- < 0.5x smallest historical analog (possibly too mild)
- > 2.0x largest historical analog (possibly too severe)

### 5. OUTPUT FORMAT

```
CHECK_ID,CHECK_NAME,ASSET_CLASS,EXPECTED,ACTUAL,STATUS,NOTES
CHK001,SPX Sector Decomposition,Equity,-22%,-21.8%,PASS,Within 1% tolerance
CHK002,Credit-Equity Beta IG,Credit,+88bp,+100bp,PASS,Slightly elevated but justified
CHK003,VIX Vol-Spot Beta,Volatility,+55 pts,+58 pts,PASS,Consistent with 3.2x beta
CHK004,UST Sign Convention,Rates,Negative,-40bp,PASS,Flight to quality
CHK005,Tech Credit Beta,Credit,1.5x index,1.4x index,PASS,AI-specific premium
...
```

### 6. SUMMARY REPORT

Provide:
1. Total checks run
2. Pass/Fail count
3. List of all failures with recommended fixes
4. Cohesiveness score (% of checks passed)
5. Recommendation: Approve / Revise / Reject
```

---

## PROMPT 6: Narrative Generation Prompt

```
You are a Risk Communication Specialist. Given a complete stress scenario with driver-level shocks, generate professional narrative documentation.

## INPUT

[Insert shock grid or summary table]

## NARRATIVE REQUIREMENTS

### 1. EXECUTIVE SUMMARY (1 page max)

Structure:
- **Scenario Name & Classification** (Moderate/Severe/Reverse)
- **Trigger Event** (1-2 sentences on what causes this scenario)
- **Key Thesis** (Why this scenario is plausible now)
- **Headline Shocks** (Table: SPX, VIX, IG OAS, HY OAS, UST 10Y)
- **Time Horizon** (Trading days, calendar days)
- **Historical Analog** (Which past event this resembles)

### 2. TRANSMISSION MECHANISM (1-2 pages)

Explain the causal chain:
1. **Initial Shock** - What triggers the scenario
2. **First-Order Effects** - Immediate market reaction
3. **Contagion Channels** - How it spreads across asset classes
4. **Feedback Loops** - Self-reinforcing dynamics
5. **Stabilization Factors** - What eventually stops the decline

Use a flow diagram or numbered sequence.

### 3. ASSET CLASS NARRATIVES

For EACH asset class, provide (2-3 paragraphs each):

**Equity:**
- Which sectors hit hardest and why
- Concentration risk (Mag-7 impact)
- International spillover

**Rates:**
- Flight-to-quality dynamics
- Fed reaction function
- Curve shape implications

**Credit:**
- Spread widening by rating tier
- Sector differentiation
- Default/downgrade expectations

**Volatility:**
- VIX spike and term structure
- Skew behavior
- Correlation regime

**FX:**
- USD strength dynamics
- EM vulnerability
- Carry trade unwind

**Commodities:**
- Safe haven flows (gold)
- Demand destruction (oil, copper)

### 4. SECTOR DEEP DIVES

For the 3 most impacted sectors, provide:
- Specific shock magnitude
- Key names affected
- Credit implications
- Recovery expectations

### 5. KEY ASSUMPTIONS & LIMITATIONS

List:
- 5 critical assumptions this scenario relies on
- 3 things this scenario does NOT capture
- Sensitivity: What if X is wrong?

### 6. FORMATTING REQUIREMENTS

- Professional tone (board/regulator ready)
- No jargon without definition
- Tables for quantitative content
- Bullets for lists
- Headers for navigation
- Page numbers
- Date and version
```

---

## PROMPT 7: Format Conversion Prompt

```
You are a Data Engineer. Convert stress scenario shocks into the required regulatory/system format.

## INPUT FORMAT

The shock data is provided as:
[Insert table or CSV]

## OUTPUT FORMAT REQUIREMENTS

### FORMAT A: Schedule F Style (FR Y-14Q)

```csv
as_of_date,scenario_id,scenario_name,severity,driver_id,driver_name,asset_class,sub_class,currency,tenor,current_value,current_unit,shock_value,shock_unit,shocked_level,shocked_unit,source,rationale
2026-01-13,AI_CORRECTION_2026Q1,AI Bubble Correction,MODERATE,EQ.SPX,S&P 500 Index,EQUITY,INDEX,USD,,6966,INDEX,-22,%,5434,INDEX,Derived,Weight-avg sector shocks
2026-01-13,AI_CORRECTION_2026Q1,AI Bubble Correction,MODERATE,RT.UST.10Y,US Treasury 10Y,RATES,GOVT,USD,10Y,4.18,%,-40,BP,3.78,%,Direct,Flight to quality
...
```

### FORMAT B: Risk System Import (JSON)

```json
{
  "scenario": {
    "id": "AI_CORRECTION_2026Q1",
    "name": "AI Bubble Correction",
    "as_of_date": "2026-01-13",
    "horizons": {
      "moderate": {"days": 10, "description": "10 trading days"},
      "severe": {"days": 60, "description": "60 trading days"}
    }
  },
  "shocks": [
    {
      "driver_id": "EQ.SPX",
      "asset_class": "EQUITY",
      "current": {"value": 6966, "unit": "INDEX"},
      "moderate": {"shock": -0.22, "level": 5434},
      "severe": {"shock": -0.33, "level": 4667},
      "metadata": {"source": "derived", "parent": null}
    }
  ]
}
```

### FORMAT C: Bloomberg-Style (BVAL)

```
SCENARIO: AI_CORRECTION_MOD
DATE: 2026-01-13
HORIZON: 10D

SPX Index    | -22.0% | 5434
NDX Index    | -30.0% | 14280
VIX Index    | +130%  | 38.0
USGG10YR     | -40BP  | 3.78%
CDX IG CDSI  | +80BP  | 128BP
...
```

### FORMAT D: Internal Grid (Excel-Ready)

| Driver_ID | Name | Class | Sector | Tenor | Current | Mod_Shock | Mod_Level | Sev_Shock | Sev_Level |
|-----------|------|-------|--------|-------|---------|-----------|-----------|-----------|-----------|

### CONVERSION RULES

1. **Shock Units:**
   - Equity: % (e.g., -22%)
   - Rates: BP (e.g., -40bp)
   - Credit: BP (e.g., +100bp)
   - Vol: Points or % (e.g., +21.5 pts)
   - FX: % (e.g., +3.5%)

2. **Driver ID Convention:**
   ```
   {ASSET_CLASS}.{INDEX/ISSUER}.{TENOR}.{ATTRIBUTE}
   
   Examples:
   EQ.SPX           - S&P 500 spot
   EQ.NVDA          - NVIDIA equity
   RT.UST.10Y       - UST 10Y yield
   CR.IG.5Y         - IG 5Y OAS
   CR.IG.5Y.TECH    - Tech sector IG 5Y OAS
   VOL.SPX.1M.ATM   - SPX 1M ATM vol
   FX.EURUSD        - EUR/USD spot
   ```

3. **Required Fields:**
   - driver_id (unique)
   - asset_class
   - current_value
   - moderate_shock
   - severe_shock
   - unit
   - source/rationale

### DELIVERABLES

Provide the shock grid in ALL requested formats, ensuring:
1. No data loss in conversion
2. Consistent driver IDs across formats
3. Proper unit handling
4. Metadata preserved
```

---

## PROMPT 8: Granular Sector Drill-Down

```
You are a Sector Risk Analyst. Take the high-level sector shocks and propagate to industry/sub-industry granularity.

## INPUT: SECTOR-LEVEL SHOCKS

| Sector | SPX Weight | Moderate | Severe | AI Exposure |
|--------|------------|----------|--------|-------------|
| Info Tech | 32% | -30% | -43% | High |
| Comm Services | 9% | -28% | -40% | High |
| Consumer Disc | 10% | -25% | -38% | Medium |
| Financials | 13% | -18% | -28% | Low |
| Healthcare | 12% | -15% | -25% | Low |
| Industrials | 8% | -20% | -32% | Medium |
| Consumer Staples | 6% | -10% | -18% | Low |
| Energy | 4% | -18% | -30% | Low |
| Utilities | 2% | -12% | -22% | Medium |
| Materials | 2% | -20% | -32% | Low |
| Real Estate | 2% | -18% | -28% | Low |

## PROPAGATION REQUIREMENTS

### 1. INDUSTRY GROUP LEVEL (GICS Level 2)

For EACH sector, break down to industry groups.

Example for Info Tech:
| Industry Group | Sector Weight | AI Exposure | Beta to Sector | Mod | Sev |
|----------------|---------------|-------------|----------------|-----|-----|
| Semiconductors | 40% | Very High | 1.3x | -39% | -56% |
| Software | 35% | High | 1.1x | -33% | -47% |
| Tech Hardware | 15% | Medium | 0.9x | -27% | -39% |
| IT Services | 10% | Medium | 0.8x | -24% | -34% |

### 2. INDUSTRY LEVEL (GICS Level 3)

Go one level deeper for high-impact industries.

Example for Semiconductors:
| Industry | AI Exposure | Names | Mod | Sev |
|----------|-------------|-------|-----|-----|
| Semiconductor Equipment | Very High | ASML, LRCX, AMAT, KLAC | -42% | -55% |
| Semiconductors | Very High | NVDA, AMD, AVGO, QCOM | -40% | -50% |

### 3. SINGLE NAME ATTRIBUTION

For top 5 names in each high-impact industry, provide:
- Ticker
- Name
- Industry
- Market Cap
- SPX Weight
- Beta
- Moderate Shock
- Severe Shock
- P&L Impact Estimate

### 4. CREDIT OVERLAY

For each sector, provide credit spread shocks:
| Sector | IG Current | IG Mod | IG Sev | HY Current | HY Mod | HY Sev |
|--------|------------|--------|--------|------------|--------|--------|

### 5. OUTPUT FORMAT

Hierarchical structure:
```
SECTOR: Information Technology (-30% Mod / -43% Sev)
├── INDUSTRY GROUP: Semiconductors (-39% / -56%)
│   ├── INDUSTRY: Semiconductor Equipment (-42% / -55%)
│   │   ├── ASML: -45% / -55%
│   │   ├── LRCX: -40% / -52%
│   │   └── AMAT: -38% / -50%
│   └── INDUSTRY: Semiconductors (-40% / -50%)
│       ├── NVDA: -40% / -50%
│       ├── AMD: -40% / -50%
│       └── AVGO: -40% / -50%
├── INDUSTRY GROUP: Software (-33% / -47%)
...
```

Plus tabular format for system import.
```

---

## PROMPT 9: Quick Scenario Extension Prompt

```
You are a Stress Testing Analyst. Given an existing stress scenario, extend it to additional risk factors or time horizons.

## EXISTING SCENARIO

[Paste existing shock grid]

## EXTENSION REQUIREMENTS

Choose ONE of the following extensions:

### OPTION A: Additional Time Horizons
Add shocks for:
- Instantaneous (T+0)
- 1-week (5 trading days)
- 1-month (22 trading days)
- 3-month (66 trading days)
- 6-month (132 trading days)

Interpolation rules:
- Equity: sqrt(t) scaling
- Vol: front-loaded (70% of shock in first 30%)
- Credit: linear with acceleration in severe
- Rates: front-loaded

### OPTION B: Regional Extension
Extend to non-US markets:
- Europe (STOXX 600, DAX, FTSE 100)
- Asia (Nikkei, Hang Seng, KOSPI, ASX 200)
- EM (MSCI EM, specific countries)
- FX implications for each region

Use regional betas to US:
- Europe: 0.8-0.9x SPX
- Japan: 0.7-0.85x SPX
- EM: 1.1-1.3x SPX

### OPTION C: Counterparty/Issuer Extension
Extend from index-level to issuer-level for:
- Top 50 counterparties by exposure
- All counterparties with >$100M exposure
- Specific sector (e.g., all Tech issuers)

Use issuer-specific betas and credit ratings.

### OUTPUT FORMAT

Same as original scenario, with clear labeling of extended drivers.
```

---

## PROMPT 10: Reverse Stress Test Prompt

```
You are a Reverse Stress Testing Specialist. Given a loss threshold, work backwards to determine what market shocks would cause that loss.

## LOSS THRESHOLD

Target P&L Impact: -$[X] million
Confidence: 99th percentile
Time Horizon: [Y] trading days

## PORTFOLIO CONTEXT

[Insert portfolio sensitivities or risk profile]

Example:
- Equity Delta: $50M per 1% SPX move
- Credit CS01: $2M per 1bp IG widening
- Rates DV01: $1.5M per 1bp parallel shift
- Vega: $0.5M per 1 vol point

## REVERSE ENGINEERING REQUIREMENTS

### 1. IDENTIFY BINDING CONSTRAINTS
Which risk factors, if shocked, would cause the target loss?

### 2. SOLVE FOR SHOCK MAGNITUDES
Given sensitivities, what shock sizes produce the target P&L?

```
SPX_shock = Target_Loss / Equity_Delta
           = -$500M / ($50M per 1%)
           = -10% SPX
```

### 3. VALIDATE PLAUSIBILITY
- Compare to historical worst days/weeks
- Check if shock combination is internally consistent
- Identify if scenario is "possible but extreme" vs "implausible"

### 4. IDENTIFY VULNERABILITIES
What combinations of shocks would be most damaging?
- Single factor concentration?
- Correlation breakdown?
- Liquidity events?

### 5. OUTPUT FORMAT

```
REVERSE STRESS TEST RESULTS

Target Loss: -$500M
Horizon: 10 trading days

SCENARIO THAT ACHIEVES TARGET:
| Driver | Shock Required | Historical Precedent | Plausibility |
|--------|----------------|----------------------|--------------|
| SPX | -15% | COVID: -34% | Plausible |
| VIX | +45 pts | COVID: +65 pts | Plausible |
| IG OAS | +150bp | COVID: +140bp | Plausible |

PORTFOLIO BREAKDOWN:
| Risk Factor | Sensitivity | Shock | P&L Impact |
|-------------|-------------|-------|------------|
| Equity Delta | $50M/1% | -15% | -$375M |
| Credit CS01 | $2M/1bp | +150bp | -$150M |
| Rates DV01 | $1.5M/1bp | -50bp | +$25M |
| **TOTAL** | | | **-$500M** |

CONCLUSION: Scenario is plausible based on COVID March 2020 analog.
```
```

---

## Usage Guide

| Prompt | Use Case | Output |
|--------|----------|--------|
| **1. Master** | Full scenario propagation | Complete shock grid + validation |
| **2. Equity** | Deep equity analysis | Sector/single-name shocks |
| **3. Rates/Credit** | Fixed income detail | Curve + spread granularity |
| **4. Volatility** | Vol surface analysis | Full vol surface + skew |
| **5. Validation** | QA/QC existing scenario | Pass/fail report |
| **6. Narrative** | Documentation | Board-ready narrative |
| **7. Format** | System integration | Multi-format export |
| **8. Sector** | Industry deep dive | GICS hierarchy |
| **9. Extension** | Add time/region | Extended shock grid |
| **10. Reverse** | Loss-based analysis | Vulnerability assessment |

**Recommended Workflow:**
1. Start with **Prompt 1** for initial propagation
2. Use **Prompts 2-4** for asset-class deep dives
3. Run **Prompt 5** for validation
4. Generate **Prompt 6** narrative for stakeholders
5. Export via **Prompt 7** for system integration
