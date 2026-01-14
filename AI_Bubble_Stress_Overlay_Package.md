# AI Bubble Stress Scenario Overlay Package (Markdown Spec)

**Base scenario:** *Severe Rates Rally* (Rates + FX unchanged)  
**Objective:** Starting from the **Severe Rates Rally** base scenario, apply **equity, credit, commodity, and equity-volatility overlays** so the combined scenario lands **exactly** on the **AI Bubble Moderate (10 trading days)** and **AI Bubble Severe (60 trading days)** targets, with **binding single-name shocks** and an **Apr 3–7, 2025 vol-surface template**.

---

## Table of contents

1. [Scope and design principles](#1-scope-and-design-principles)  
2. [Required inputs and outputs](#2-required-inputs-and-outputs)  
3. [Overlay mathematics](#3-overlay-mathematics)  
4. [Scenario narrative and macro context](#4-scenario-narrative-and-macro-context)  
5. [Historical regime anchors (dates + why)](#5-historical-regime-anchors-dates--why)  
6. [Equity overlay (granular, with binding constraints)](#6-equity-overlay-granular-with-binding-constraints)  
7. [Credit overlay (sector-aware)](#7-credit-overlay-sector-aware)  
8. [Commodity overlay (metals + energy + battery materials)](#8-commodity-overlay-metals--energy--battery-materials)  
9. [Equity volatility overlay (Apr 3–7, 2025 surface)](#9-equity-volatility-overlay-apr-37-2025-surface)  
10. [Time-series calibration method (max/min vs percentile + scaling)](#10-time-series-calibration-method-maxmin-vs-percentile--scaling)  
11. [Implementation runbook (A→Z)](#11-implementation-runbook-az)  
12. [Validation checklist](#12-validation-checklist)  
13. [Appendix: canonical target tables](#13-appendix-canonical-target-tables)  

---

## 1) Scope and design principles

### What this document is
A complete, auditable specification for generating an **AI Bubble stress scenario** by **overlaying** shocks on top of a pre-existing **Severe Rates Rally** base scenario.

### What this document is not
- It does **not** change the base scenario’s **Rates** or **FX** shocks.
- It does **not** require a black-box macro model; it is explicitly designed for regulator-friendly auditability.

### Design principles
1. **Binding constraints dominate**: the AI names and AI-power utilities must hit the mandated endpoints exactly.  
2. **Historical shape, scaled to target**: use history for *shape* and calibrate *level* to land exactly on targets.  
3. **No double-counting**: base scenario shocks remain; overlays are computed so final results match desired endpoints.  
4. **Cross-asset coherence**: equities, credit, vol, and commodities must tell one consistent story.

---

## 2) Required inputs and outputs

### Inputs from the base scenario (Severe Rates Rally)
You must obtain base scenario outputs for both horizons (10d and 60d), ideally by driver:

**Equities**
- SPX return, QQQ return
- Sector-level returns (recommended)
- Single-name returns for: NVDA, AMD, AVGO, VST, CEG, plus other key names you include

**Credit**
- IG OAS change (bp), HY OAS change (bp)
- Sector OAS changes (bp): Tech/Semis IG & HY, Software IG, Utilities IG (recommended)

**Volatility**
- VIX (spot) level
- Term structure points: 1W, 1M, 3M, 6M, 1Y (ATM)
- Skew metrics: 1M 25Δ put – ATM; 1M 10Δ put – ATM
- Optional: VVIX (spot)

**Commodities**
- Gold, silver
- WTI (or Brent), Henry Hub natural gas
- Copper
- Cobalt, lithium
- Steel, aluminum

**Rates + FX**
- Keep **exactly as base** (no overlay).

---

### Outputs (final scenario endpoints)
Two complete scenarios:
- **AI Bubble Moderate**: 10 trading days  
- **AI Bubble Severe**: 60 trading days  

Each includes final shocks for:
- Equity indices (SPX, QQQ), sectors, and single names
- Credit spreads (broad + sector)
- Commodities (metals + energy + battery materials)
- Equity volatility (surface; VIX/VVIX; skew and term structure)

---

## 3) Overlay mathematics

### 3.1 Returns (equities, commodities, indices): multiplicative overlay
To avoid arithmetic errors on large moves, combine returns multiplicatively:

\[
(1+R_{final}) = (1+R_{base}) \times (1+R_{overlay})
\]

So the overlay needed to hit a desired target is:

\[
R_{overlay} = \frac{1 + R_{target}}{1 + R_{base}} - 1
\]

**Use this for**
- all equity returns (single names, sectors, indices, baskets)
- all commodity returns

---

### 3.2 Spreads / yields (bp): additive overlay
Spreads and yields combine additively in basis points:

\[
\Delta_{overlay} = \Delta_{target} - \Delta_{base}
\]

**Use this for**
- OAS changes
- CDX / iTraxx levels (if modeled as bp)

---

### 3.3 Volatility levels (VIX, VVIX, tenor IV): set-to-target or Δ-points
Preferred for governance: **set-to-target**.  
If your engine requires overlays:

\[
V_{overlay} = V_{target} - V_{base}
\]

**Use for**
- VIX, VVIX (levels)
- ATM implied vol by tenor (levels)

---

## 4) Scenario narrative and macro context

### Starting point (inherited from base)
The base “Severe Rates Rally” implies:
- recession probability repricing / flight to quality
- lower yields, defensive positioning, risk-off in growth assets (to some extent)

### What the AI overlay adds (theme-specific shock)
This overlay creates an **AI bubble unwind** (valuation compression) on top of the rates rally:

1. **AI earnings + guidance disappointment**
   - AI revenue and ROI scrutiny, slowing incremental returns on CapEx
2. **Rapid multiple compression**
   - high-duration tech repriced sharply even as rates rally
3. **Credit contagion concentrated in tech-heavy sectors**
   - tech/semis and software spreads widen disproportionately
4. **Commodity cross-check**
   - safe-haven bid supports gold
   - industrial and battery materials fall as CapEx expectations reset

---

## 5) Historical regime anchors (dates + why)

This scenario uses different historical anchors by driver:

### 5.1 Equity volatility surface (shape template)
**Anchor window:** **Apr 3–7, 2025**  
**Purpose:** provide a *real* panic surface with:
- steepened skew,
- inverted term structure,
- correlation spike behavior.

**Implementation rule:** use this window for *shape*; scale to VIX targets (Section 9).

---

### 5.2 AI infrastructure / semiconductors (multiple compression template)
**Anchor window:** **Late 2021 peak → Oct 2022 trough**  
**Purpose:** modern precedent for violent semi drawdowns under multiple compression.

Used to justify that -40% / -50% single-name shocks are within observed regimes.

---

### 5.3 AI software / SaaS (valuation compression template)
**Anchor window:** **2022 software bear market**  
**Purpose:** modern analog for duration-driven SaaS multiple reset.

---

### 5.4 Severe continuation / bubble unwind persistence (optional)
**Anchor window:** **early dot-com unwind (Mar–Apr 2000 initiation), continued drawdown regime**  
**Purpose:** justify that the 60d severe scenario includes a second phase beyond the initial panic.

---

## 6) Equity overlay (granular, with binding constraints)

### 6.1 Binding constraints (must hit exactly)

| Asset bucket | Examples | Moderate (10d) | Severe (60d) |
|---|---|---:|---:|
| **AI single names (Infrastructure)** | NVDA, AMD, AVGO, etc. | **−40%** | **−50%** |
| **AI-exposed power utilities (Enablers)** | VST, CEG, etc. | **−15%** | **−30%** |

These are *hard constraints*; everything else is calibrated around them.

---

### 6.2 Equity bucket endpoints (final targets)

#### 6.2.1 Moderate (10d) targets
| Bucket | Description | Examples / proxy | Target return |
|---|---|---|---:|
| AI Infrastructure (binding) | semis/compute | NVDA/AMD/AVGO | −40% |
| AI Software / Applications | SaaS/apps | CRM/NOW/PLTR | −35% |
| AI Power utilities (binding) | data-center power unwind | VST/CEG | −15% |
| Mega-cap spillover | concentration + contagion | AAPL/MSFT/GOOGL/AMZN/META | −30% |
| Rest of QQQ | sympathetic selling | QQQ ex above | −20% |
| Non-tech SPX | correlation + risk-off | SPX ex tech | −10% |

#### 6.2.2 Severe (60d) targets
| Bucket | Description | Examples / proxy | Target return |
|---|---|---|---:|
| AI Infrastructure (binding) | semis/compute | NVDA/AMD/AVGO | −50% |
| AI Software / Applications | SaaS/apps | CRM/NOW/PLTR | −45% |
| AI Power utilities (binding) | data-center power unwind | VST/CEG | −30% |
| Mega-cap spillover | concentration unwind | AAPL/MSFT/GOOGL/AMZN/META | −40% |
| Rest of QQQ | broad tech drawdown | QQQ ex above | −35% |
| Non-tech SPX | recession + corr spike | SPX ex tech | −25% |

---

### 6.3 Sector propagation targets (non-tech SPX granularity)

These are recommended sector endpoints used to allocate the “non-tech SPX” bucket.

#### Moderate (10d) sector targets (excluding AI-power special names)
| Sector | Target return | Notes |
|---|---:|---|
| Industrials | −12% | cyclical + capex |
| Financials | −12% | credit stress |
| Consumer Discretionary | −15% | recession repricing |
| Communication Services | −22% | overlaps mega-cap growth |
| Materials | −10% | industrial metals down |
| Energy | −15% | oil down |
| Staples | −6% | defensive |
| Health Care | −7% | defensive |
| Real Estate | −10% | credit sensitivity |
| Utilities (non-AI-power) | −5% | defensive bucket |

#### Severe (60d) sector targets
| Sector | Target return | Notes |
|---|---:|---|
| Industrials | −30% | capex retrenchment |
| Financials | −30% | credit cycle stress |
| Consumer Discretionary | −35% | earnings hit |
| Communication Services | −40% | mega-cap dominated |
| Materials | −25% | metals down |
| Energy | −35% | oil/NG down |
| Staples | −15% | correlation regime |
| Health Care | −18% | correlation regime |
| Real Estate | −25% | refi stress |
| Utilities (non-AI-power) | −15% | not immune in severe |

---

### 6.4 Index reconciliation (how to make SPX/QQQ “perfect” without touching bindings)

If you build index returns from buckets:

\[
R_{Index} = \sum_i w_i \cdot R_i
\]

Use one scaling factor **λ** on non-binding buckets:

\[
R_i^{adj} =
\begin{cases}
R_i & \text{if } i \in \text{binding}\\
\lambda \cdot R_i & \text{otherwise}
\end{cases}
\]

Solve λ so SPX and QQQ land exactly on desired final endpoints (moderate and severe). This preserves:
- binding exact hits,
- cross-sector shape,
- full auditability.

---

### 6.5 Converting base → final (overlay computation)

For each equity item (index/sector/name):

1) Decide the **target final return** (tables above).
2) Read the **base return** from the Severe Rates Rally.
3) Compute overlay:

\[
R_{overlay}=\frac{1+R_{target}}{1+R_{base}} - 1
\]

4) Apply base + overlay in your scenario engine.

---

## 7) Credit overlay (sector-aware)

### 7.1 Final credit endpoints (OAS widening)

| Credit series | Moderate (10d) | Severe (60d) | Rationale |
|---|---:|---:|---|
| IG OAS (broad) | +100 bp | +200 bp | risk-off repricing |
| HY OAS (broad) | +250 bp | +500 bp | downgrade + liquidity premium |
| Tech/Semis IG | +140 bp | +260 bp | higher beta in AI stress |
| Tech/Semis HY | +320 bp | +600 bp | funding-risk repricing |
| Software IG | +130 bp | +240 bp | duration + earnings risk |
| Utilities IG | +70 bp | +150 bp | defensive but widens |

### 7.2 Overlay vs base
For each spread:

\[
\Delta_{overlay} = \Delta_{target} - \Delta_{base}
\]

### 7.3 Consistency rule
If AI semis equities are down −50% (severe), it is inconsistent for Tech/Semis spreads to widen *less* than broad IG. Enforce sector widening > index widening.

---

## 8) Commodity overlay (metals + energy + battery materials)

### 8.1 Final commodity endpoints (as requested)

| Commodity | Moderate (10d) | Severe (60d) | Narrative fit |
|---|---:|---:|---|
| Gold | +10% | +18% | safe-haven bid |
| Silver | −10% | −15% | industrial exposure under growth fear |
| Natural gas | −20% | −35% | cyclical demand repricing |
| Crude oil | −15% | −30% | demand shock / recession risk |
| Copper | −20% | −30% | growth barometer, capex reset |
| Cobalt | −20% | −30% | battery chain cyclicality |
| Lithium | −20% | −30% | battery chain cyclicality |
| Steel | −10% | −15% | industrial cycle downshift |
| Aluminum | −10% | −15% | industrial cycle downshift |

### 8.2 Overlay vs base (returns)
Compute for each commodity:

\[
R_{overlay}=\frac{1+R_{target}}{1+R_{base}}-1
\]

---

## 9) Equity volatility overlay (Apr 3–7, 2025 surface)

### 9.1 Final vol endpoints
| Vol metric | Moderate (10d) | Severe (60d) |
|---|---:|---:|
| VIX (spot) | 40 | 58 |
| VVIX (spot) | 130 | 170 |
| Skew (1M) | steeper vs base | materially steeper vs base |
| Term structure | flat→inverted | deep inversion |

### 9.2 Apply Apr 3–7, 2025 as a *shape template*
You should not hardcode every strike/tenor number. Instead:

1) Pull the Apr 3–7, 2025 surface snapshot from your vendor/internal store:
   - ATM vols: 1W, 1M, 3M, 6M, 1Y
   - skew: (25Δ put − ATM) at 1M; (10Δ put − ATM) at 1M
   - term ratios: (1M/6M), (1W/3M)

2) Scale the template level to land at VIX targets:
   - Let ATM(1M) of the template be \(IV^{temp}_{1M}\)
   - Choose scaling \(k = \frac{VIX_{target}}{IV^{temp}_{1M}}\)
   - Apply to each tenor/strike:
     \[
     IV^{scenario}(T,\Delta)=k\cdot IV^{temp}(T,\Delta)
     \]

3) Correlation consistency:
   - Moderate implied corr: 0.65
   - Severe implied corr: 0.85

This avoids the common inconsistency of “single names crash but index vol doesn’t move.”

---

## 10) Time-series calibration method (max/min vs percentile + scaling)

This is the recommended “perfect + auditable” method for shaping shocks from history without losing exact endpoints.

### 10.1 Define proxy time series per driver
- AI infrastructure: SOX/SMH and/or AI basket
- AI software: IGV/WCLD or internal SaaS basket
- Credit: CDX IG/HY, sector OAS indices
- Commodities: front-month futures total returns
- Vol: SPX surface + VIX/VVIX + term structure

### 10.2 Compute rolling shocks within the chosen windows
For a horizon \(H\) in trading days:

**Returns**
\[
R_{t,H}=\prod_{j=1}^{H}(1+r_{t+j})-1
\]

**Spreads**
\[
\Delta S_{t,H}=S_{t+H}-S_t
\]

### 10.3 Choose statistic by severity
- Moderate (10d): use 95th percentile worst move in-window
- Severe (60d): use 99th percentile worst move in-window (with governance caps if needed)

### 10.4 Scale to binding constraints
Let \(F^{hist}\) be the historical shock vector (across assets). Scale it by \(k\) so binding constraints are satisfied:

- Enforce equality on binding names (NVDA/AMD/AVGO/VST/CEG),
- Minimize deviation for all other assets (least squares).

This produces a historically shaped scenario that lands exactly on required endpoints.

---

## 11) Implementation runbook (A→Z)

1) Clone the **Severe Rates Rally** scenario.  
2) Freeze **Rates + FX** exactly as base (no changes).  
3) Create overlay container: **“AI Bubble Unwind”**.  
4) Set binding shocks:
   - NVDA/AMD/AVGO: −40% (Mod), −50% (Sev)
   - VST/CEG: −15% (Mod), −30% (Sev)
5) Map all equities into buckets (AI infra / AI software / AI utilities / mega-cap spillover / rest QQQ / non-tech SPX).  
6) Assign bucket targets for Moderate and Severe.  
7) Convert base → overlay returns using:
   \[
   R_{overlay}=\frac{1+R_{target}}{1+R_{base}}-1
   \]
8) Reconcile SPX and QQQ endpoints using the λ scaling on non-binding buckets.  
9) Apply credit spread widenings additively:
   \[
   \Delta_{overlay}=\Delta_{target}-\Delta_{base}
   \]
10) Apply commodity endpoints (gold up; industrial/battery metals down; energy down), computing overlays via the return formula.  
11) Apply equity vol surface:
   - shape from Apr 3–7, 2025 template,
   - scale to VIX=40 (Mod), VIX=58 (Sev),
   - set implied correlation 0.65 / 0.85.
12) Validate consistency (Section 12).

---

## 12) Validation checklist

### Equity consistency
- [ ] Binding single names hit exactly (−40/−50; −15/−30)
- [ ] Bucket logic preserves ranking: AI infra worse than broad tech; broad tech worse than non-tech
- [ ] SPX/QQQ land exactly on target endpoints after reconciliation

### Credit consistency
- [ ] Tech/Semis spreads widen more than IG overall
- [ ] HY widens more than IG in both scenarios
- [ ] Utilities widen less than tech (but not zero)

### Commodity consistency
- [ ] Gold up while industrial/battery materials down
- [ ] Energy down in line with growth scare narrative

### Volatility consistency
- [ ] VIX hits 40/58 and surface shows inversion/skew consistent with a panic regime
- [ ] Correlation set appropriately so index vol is coherent with cross-sector drawdown

---

## 13) Appendix: canonical target tables

### 13.1 Canonical index endpoints (recommended)
These are recommended endpoints consistent with your AI bubble narrative and the binding constraints.

| Metric | Moderate (10d) | Severe (60d) |
|---|---:|---:|
| SPX | −27% (target range −25% to −30%) | −47% (target range −45% to −50%) |
| QQQ | −34% (target range −30% to −35%) | −50% (target range −48% to −52%) |
| VIX (spot) | 40 | 58 |
| IG OAS widening | +100 bp | +200 bp |
| HY OAS widening | +250 bp | +500 bp |

### 13.2 Canonical single-name constraints (must hit)
| Category | Moderate | Severe |
|---|---:|---:|
| AI infrastructure (NVDA/AMD/AVGO etc.) | −40% | −50% |
| AI power utilities (VST/CEG etc.) | −15% | −30% |

### 13.3 Canonical commodity endpoints
| Commodity | Moderate | Severe |
|---|---:|---:|
| Gold | +10% | +18% |
| Silver | −10% | −15% |
| Natural gas | −20% | −35% |
| Crude | −15% | −30% |
| Copper | −20% | −30% |
| Cobalt | −20% | −30% |
| Lithium | −20% | −30% |
| Steel | −10% | −15% |
| Aluminum | −10% | −15% |

---

## References (titles only; add your internal links/IDs)
- Volatility surface template: Apr 3–7, 2025 “tariff panic” (SPX/VIX spike episode)  
- Semi multiple compression: late 2021 to Oct 2022 drawdown regime  
- SaaS/software multiple compression: 2022 valuation reset regime  
- Bubble unwind persistence: dot-com initiation (Mar–Apr 2000), used as plausibility bound  
