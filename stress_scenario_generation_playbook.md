# Stress Scenario Generation and Development Playbook (Industry Best Practice)

**Purpose:** A practical, defensible, end-to-end framework for **stress risk** and **stress scenario generation** (solvency, liquidity, market shocks, counterparty default, and climate) used by industry leaders and supervisors.

**How to use this document**
- Copy/paste **any formula** from the `code blocks` (they are plain text, not rendered LaTeX).
- Treat the worked examples as templates; swap in your firm’s variables, risk factors, and calibration choices.

**Scope note (important):** No single “best model” exists. The most defensible programs use a **hybrid stack**: narrative deterministic macro scenarios + risk-factor market shocks + credit loss translation (PD×LGD×EAD) + reverse stress optimization + rigorous governance and model risk controls.

---

## 1) What “best” means in practice

A stress scenario framework is “best-in-practice” when it is:

1. **Coherent** across macro, markets, and balance-sheet mechanics.
2. **Severe but plausible** (common supervisory standard language) and **traceable** to evidence and judgement.
3. **Portfolio-relevant** (targets material concentrations, optionality, wrong-way risk).
4. **Explainable and auditable** (reproducible, documented, independently challenged).
5. **Actionable** (links to risk appetite, limits, hedging, capital, liquidity, recovery options).
6. **Model-risk controlled** (validation, uncertainty, overlays, governance).

**Authoritative standards that shape “what good looks like”**
- BCBS/FSB stress testing principles (2009; updated principles also exist).[^bcbs155][^fsb2018]
- PRA SS3/18 model risk management expectations for stress testing models.[^ss318]
- Federal Reserve supervisory stress test scenarios and documentation (macro + Global Market Shock).[^^fed2025pdf][^gmsdoc2025]
- Basel market risk standard (Expected Shortfall, stress calibration concepts in FRTB context).[^bcbs_mr]
- PFMI standards and CCP resilience guidance (stress testing expectations for FMIs/CCPs).[^pfmi][^ccp_resilience]
- NGFS climate scenarios technical documentation.[^ngfs_v5]
- EBA guidelines on environmental scenario analysis (application date 1 Jan 2027).[^eba_env]

---

## 2) Big picture architecture: 3 layers (this is how leaders structure it)

### Layer A — Scenario design / generation (“state of the world”)
Outputs:
- Macro paths (9+ quarters, yearly, or longer)
- Market shocks (instantaneous or path-based)
- Credit event overlays (counterparty default)
- Climate pathways (transition and physical)

### Layer B — Transmission / translation (“how the world hits your P&L and balance sheet”)
Outputs:
- PD, LGD, EAD, pre-provision net revenue (PPNR) projections
- Trading and CVA losses under revaluation
- Margin calls, liquidity outflows, funding costs

### Layer C — Aggregation / decisioning (“what it means”)
Outputs:
- Capital ratios, leverage, RWAs, liquidity survival horizon
- Breach analysis vs risk appetite / regulatory minima
- Management actions and remediation plan

**Key principle:** The “best” scenario generators are those that generate **coherent inputs** into Layer B, and can be **defended** at Layer C.

---

## 3) A “perfect” stress scenario development lifecycle (with tangible artifacts)

This lifecycle is structured into **phases** and **governance gates**. The best firms run it quarterly (or more frequently for market risk), with annual deep refresh.

### Phase 0 — Objectives, scope, and governance
**Decisions**
- Use-cases: capital planning, liquidity survival, limit setting, recovery, ICAAP/ILAAP, client risk, etc.
- Horizons: intraday/10-day, 1-year, 9-quarter, multi-year.
- Perimeter: entities, consolidation, portfolios.

**Artifacts**
- Stress Testing Policy (objectives, frequency, responsibilities)
- Governance map and RACI (owners, approvers, independent challenge)

**Gate 0:** Senior committee approves objectives, scope, and scenario families.

---

### Phase 1 — Risk identification and materiality (what can kill us?)
**How to do it systematically**
1) Build a risk taxonomy (macro/credit, market, liquidity, counterparty, concentration, op risk, climate, model risk).
2) Map exposures to primary drivers: sector, geography, product, optionality, funding profile.
3) Score materiality (size × sensitivity × convexity × interconnectedness).

**Artifacts**
- Material Risk Inventory
- Concentration heatmaps and top vulnerabilities
- “Risk driver dictionary” (variables and risk factors used in modeling)

**Gate 1:** CRO-level approval of materiality conclusions and “what must be stressed.”

---

### Phase 2 — Scenario library design (avoid “one scenario” thinking)
**Best practice:** maintain a *library* of scenario families, then choose a set per cycle.

Minimum scenario families (recommended):
1) Systemic macro recession (baseline / adverse / severely adverse)
2) Inflation shock / stagflation
3) Market dislocation (Global Market Shock style)
4) Funding / liquidity freeze
5) Counterparty default + wrong-way overlay
6) Idiosyncratic concentration stress (e.g., CRE region, sector crash)
7) Operational risk tail (outage/fraud/legal)
8) Climate transition + physical (NGFS anchored)

**Artifacts**
- Scenario inventory, tagging, and reuse rules
- Scenario triggers and early warning indicators

**Gate 2:** Risk committee approves the library structure and selection criteria.

---

### Phase 3 — Scenario ideation (narrative first, then math)
**Process**
- Start with a one-page scenario narrative (what happens, why, and transmission channels).
- Name the “failure mechanism” you are targeting (e.g., CRE → bank losses → funding stress).
- Identify *required* variable movements (signs and magnitudes).

**Artifacts**
- 1-page narrative concept note (story, affected businesses, key drivers)
- Transmission mechanism diagram (“cause → effect → financial impact”)

---

### Phase 4 — Quantification: build the macro paths and/or risk-factor shocks
This is where your “scenario generation algorithms” enter.

**Outputs**
- Macro time paths: (GDP, unemployment, inflation, policy rates, house prices, CRE prices, equity index, credit spreads, FX blocks, etc.)
- Market shock set: risk-factor shocks for trading/counterparty (rates curve, spreads, equity, FX, vol, commodities)

**Artifacts**
- Scenario data pack (time series + shock tables)
- Calibration memo (“severity, plausibility, evidence, expert judgement”)

**Gate 3:** Scenario design committee approves the quantified scenario.

---

### Phase 5 — Calibration, severity scoring, plausibility, and coherence checks
**Best practice** uses both:
- Quantitative severity metrics (percentiles, z-scores, historical analogs)
- Qualitative plausibility justification (narrative consistency, expert judgement)

**Artifacts**
- Severity dashboard and benchmarking pack
- Coherence check results (passed/failed + fixes)

**Gate 4:** Independent challenge signs off (or logs issues + overlays).

---

### Phase 6 — Scenario expansion and mapping (macro → desk → instrument)
**Core task:** convert your macro scenario variables into the risk factors used by pricing/credit models.

Examples:
- macro rates → full yield curve
- unemployment + GDP → sector default rates / PD drivers
- equity index + vol regime → implied vol surface
- credit conditions → rating spreads by sector/rating

**Artifacts**
- Mapping model documentation (“macro-to-risk-factor transformer”)
- Override policy and override log

---

### Phase 7 — Portfolio impact modeling (Layer B)
Run:
- credit losses (PD×LGD×EAD)
- trading losses (revaluation under market shocks)
- counterparty/CVA losses + defaults
- liquidity outflows / margin calls / funding costs
- PPNR (fees, trading revenue, NII sensitivity, etc.)

**Artifacts**
- Model run pack, controls, and reconciliation
- Driver decomposition (“what caused the loss?”)

---

### Phase 8 — Management actions and dynamic balance sheet (don’t assume paralysis)
Run at least two views:
- **Static balance sheet** (pure vulnerability)
- **Dynamic with credible actions** (realistic response)

**Artifacts**
- Management actions playbook
- Constraints and feasibility analysis

---

### Phase 9 — Aggregation, second-round effects, and constraints (Layer C)
Aggregate:
- capital ratios, leverage, RWAs
- liquidity ratios/survival horizon
- constraints: regulatory minima, internal risk appetite, recovery triggers

**Artifacts**
- Enterprise result pack
- Breach analysis and remediation plan

---

### Phase 10 — Independent challenge, validation, and model risk governance
Supervisors expect rigorous model risk controls for stress testing models.[^ss318]

**Artifacts**
- Independent challenge log + management responses
- Validation report(s)
- Limitations register + overlays

---

### Phase 11 — Board/exec approval and decisioning
**Artifacts**
- Board deck: narrative → quantification → results → decisions
- Action plan: limits, hedges, portfolio changes, capital/liquidity actions

---

### Phase 12 — Post-mortem and continuous improvement
**Artifacts**
- Lessons learned report
- Updated scenario library, mappings, and models

---

## 4) The “best of the best” scenario generation models and where they fit

Below is a catalog of leading approaches. Each includes:
- **When to use**
- **Math**
- **Intuition**
- **Validation / challenge points**
- **Lifecycle fit**

---

### 4.1 Narrative-anchored deterministic macro scenarios (regulatory workhorse)

**What it is**
A scenario is a **story** (e.g., “severe global recession with CRE stress”) turned into **time paths** for macro/financial variables (typically 9 quarters in US supervisory stress tests).

**Where it’s used**
- Supervisory stress tests: Federal Reserve scenarios are a primary public example.[^fed2025pdf]
- Industry: banks run internal stress tests aligned to supervisory expectations.

**Lifecycle fit**
- Phase 3–5 (design, quantification, calibration)
- Phase 11 (defense to executives/supervisors)

**Math (structure)**
Represent the scenario as a vector time series:
```text
y_t = [GDP_t, Unemp_t, CPI_t, PolicyRate_t, HPI_t, CRE_t, Equity_t, Spreads_t, FX_t, ...]
t = 0..T
```

**Practical way to generate deterministic paths (constraint-based macro builder)**
Use simple macro relationships as *guides* (not “truth”):
1) Okun-like relationship (GDP ↔ unemployment)
2) Phillips curve-like relationship (slack ↔ inflation)
3) Policy rule (inflation/unemployment ↔ policy rate)

Example guide equations:
```text
(1) Unemployment change (Okun-like):
    dU_t = a0 + a1 * (g*_t - GDPgrowth_t)

(2) Inflation (Phillips-like):
    Inflation_t = b0 + b1 * Inflation_{t-1} + b2 * (U_t - U*_t) + supply_shock_t

(3) Policy rate (Taylor-like):
    i_t = c0 + c1*(Inflation_t - InflationTarget) + c2*(U_t - U*_t)
```

**Intuition**
- Deterministic macro scenarios are best when you need:
  - a coherent enterprise-wide story,
  - stable inputs for credit/PPNR models,
  - governance-friendly explainability.

**Validation / challenge checklist**
- Coherence: signs and magnitudes align with narrative.
- Feasibility: no impossible combos (e.g., collapsing GDP but booming credit spreads tightening).
- Benchmarking: severity vs history, vs supervisory scenarios, vs internal risk appetite.

---

### 4.2 Global Market Shock (GMS) / risk-factor shock libraries (trading & counterparty)

**What it is**
A set of instantaneous shocks to a large set of risk factors applied to trading/counterparty portfolios. The Fed applies the GMS losses in the first quarter to reflect rapid market dislocation.[^fed2025pdf][^gmsdoc2025]

**Lifecycle fit**
- Phase 4 (shock design) → Phase 7 (revaluation)

**Math**
Let X be a vector of risk factors; V(X) is portfolio value.

```text
Shock:   X' = X + ΔX
Loss:    L = V(X) - V(X')
```

For small changes you may approximate with Greeks, but for stress you should prefer revaluation:
```text
ΔV ≈ (∂V/∂X)' ΔX + 0.5 * ΔX' (∂²V/∂X²) ΔX
```

**Intuition**
- Trading portfolios have convexity/volatility effects.
- A deterministic macro path alone often misses “gap” moves and vol spikes.

**Validation / challenge checklist**
- Nonlinearity: compare delta-only vs full revaluation losses.
- Correlation regime: ensure shocks imply crisis-like co-movements.
- Liquidity: include widening bid-ask or haircut overlays where relevant.

---

### 4.3 Counterparty default add-on (wrong-way risk)

**What it is**
Overlay the default of one (or several) large counterparties on top of market stress; supervisory frameworks often require or include this concept.[^fed2025pdf]

**Lifecycle fit**
- Phase 4 (design overlay) → Phase 7 (CVA/default loss + liquidity effects)

**Math (simplified)**
```text
Exposure under stress: EAD = max(MtM_stress - collateral + add_ons, 0)
Loss ≈ EAD * LGD
```

**Challenge checklist**
- Margin period of risk assumptions
- Collateral haircuts under stress
- Wrong-way coupling: counterparty credit worsens as your exposure increases

---

### 4.4 Credit loss “satellite” modeling: PD × LGD × EAD

**What it is**
The dominant modular framework for solvency stress testing of banking books.

**Lifecycle fit**
- Phase 6–7 (transmission and execution)

**Math**
For exposure i in period t:
```text
EL_{i,t} = PD_{i,t} * LGD_{i,t} * EAD_{i,t}
Total loss_t = Σ_i EL_{i,t}
```

**Typical PD model form (logit)**
```text
PD_{i,t} = 1 / (1 + exp(-(β0 + β' z_t + γ' w_i)))
```
- z_t: macro variables (unemployment, GDP growth, rates, HPI, spreads)
- w_i: obligor/loan features (LTV, FICO, DSCR, sector, vintage)

**Intuition**
- Separates frequency (PD), severity (LGD), and exposure (EAD).
- Highly defensible because it’s transparent and decomposable.

**Challenge checklist**
- Stability under stress: monotonicity (PD increases when macro worsens).
- Data representativeness: include downturn periods; avoid optimistic bias.
- Model overlays: where data is thin, use conservative overlays and document.

---

### 4.5 VAR/BVAR macro-financial generators (scenario libraries)

**What it is**
Statistical models for joint dynamics of variables; can generate many coherent scenarios and conditional paths.

**Lifecycle fit**
- Phase 2–5 (scenario library generation, benchmarking)

**Math (VAR(p))**
```text
y_t = c + A1 y_{t-1} + ... + Ap y_{t-p} + ε_t
ε_t ~ (0, Σ)
```

**Bayesian VAR (BVAR)**
Same structure, but with priors on A’s to stabilize estimation.

**Stress generation tactics**
- Shock the system: choose ε sequences to drive downturn outcomes.
- Condition on an event: "U peaks at 10%" and generate implied paths (simulation/conditioning).

**Challenge checklist**
- Tail risk: plain Gaussian errors understate crises; consider t-distributed errors or regime switching.
- Structural breaks: macro regimes change; validate across subsamples.

---

### 4.6 Regime-switching and fat-tail models (crisis realism)

**What it is**
Models that allow transitions between “normal” and “crisis” regimes (vol/correlation jumps).

**Math (Markov regime switching, stylized)**
```text
y_t = μ_{s_t} + A_{s_t} y_{t-1} + ε_t
s_t ∈ {Normal, Crisis}
P(s_t=j | s_{t-1}=i) = p_ij
```

**Intuition**
- Many stress events are regime changes.
- This method is excellent for market stress realism and correlation spikes.

---

### 4.7 Filtered Historical Simulation (FHS) + GARCH scaling (market stress engine)

**What it is**
Resample standardized shocks from history and rescale them to today’s volatility.

**Math (GARCH(1,1) skeleton)**
```text
r_t = μ + σ_t z_t
σ_t^2 = ω + α (r_{t-1}-μ)^2 + β σ_{t-1}^2
Standardize: z_t = (r_t - μ)/σ_t
Resample z_t and reconstruct with current σ
```

**Use case**
- Daily market risk stress, margin-like engines, risk-factor scenario generation.

---

### 4.8 EVT tail calibration (severity beyond limited history)

**What it is**
Model tails beyond a threshold using Generalized Pareto (POT method).

**Math (POT, GPD)**
```text
For losses L above threshold u:
Excess Y = L - u
P(Y ≤ y | L > u) ≈ 1 - (1 + ξ y/β)^(-1/ξ)
```

**Use case**
- “Beyond history” plausibility checks and severity calibration.

---

### 4.9 Copulas / tail dependence models (when correlation is the risk)

**Math**
```text
Joint CDF: F(x1..xd) = C(F1(x1), ..., Fd(xd))
```
Use a t-copula (often) when you need tail dependence.

**Use case**
- Multi-asset joint stress; correlation breakdown in crises.

---

### 4.10 Reverse stress via empirical likelihood / exponential tilting (best-in-class vulnerability discovery)

**What it is**
Find the **most plausible** distributional shift from history that forces a breach (capital, liquidity, loss threshold).

Public reference: OFR working paper on empirical likelihood stress scenario selection.[^ofr_el]

**Lifecycle fit**
- Phase 2–5 (scenario discovery, challenge)
- Phase 11 (board-level “what kills us?”)

**Math (conceptual, discrete historical draws)**
Given historical/simulated scenarios x_i (i=1..N) with baseline weights 1/N.
Choose new weights p_i closest to baseline but satisfying constraints:

```text
Minimize:   Σ_i p_i * log(p_i / (1/N))          (KL divergence)
Subject to: Σ_i p_i = 1,  p_i ≥ 0
            Σ_i p_i * g(x_i) = m                (constraint(s))
```

Solution has exponential tilt form:
```text
p_i ∝ exp(λ' g(x_i))
```

**Intuition**
- You stop arguing “plausible vs severe” qualitatively.
- You compute the *least distorted* change from history that still breaks you.

**Challenge checklist**
- Ensure g(x) constraints reflect real failure mechanisms.
- Stress is only as good as the scenario set x_i (garbage in, garbage out).

---

### 4.11 Basel market risk: Expected Shortfall and stress calibration (FRTB context)

**Why it matters**
Even if you are not calculating Basel capital, the concepts provide strong benchmarking:
- ES captures tail average loss, not just a quantile.
- Stress calibration anchors you to crisis-like conditions.[^bcbs_mr]

**Math (Expected Shortfall at level α)**
```text
ES_α = E[L | L ≥ VaR_α]
```

---

### 4.12 CCP/clearing stress: SPAN and PFMI-aligned stress testing

**SPAN methodology (widely used margin engine)**
SPAN is a market simulation-based margin framework using risk arrays; CME notes SPAN is used globally by exchanges/clearing orgs.[^cme_span_pdf][^cme_span_overview]

**Math (stress across discrete scenarios)**
```text
For scenario s=1..S:
    L_s = Σ_k ΔV_{k,s}
Margin ≈ max_s(L_s) + add-ons/adjustments
```

**PFMI guidance**
PFMI and CCP resilience guidance emphasize governance and financial risk management stress testing expectations for CCPs.[^pfmi][^ccp_resilience]

---

## 5) A systematic scenario design algorithm (repeatable, defensible)

This section is “how to do it systematically” so you can defend every decision.

### Step 1 — Define the failure threshold(s)
Examples:
- CET1 ratio breaches internal threshold
- liquidity survival horizon < X days
- margin calls exceed funding capacity
- loss exceeds capital buffer
- recovery triggers activated

Write them precisely as inequalities, e.g.:
```text
Breach if: CET1_min_over_horizon < 8.0%
Breach if: LCR < 100% for 2 consecutive weeks
Breach if: Peak_margin_call > Unencumbered_HQLA
```

### Step 2 — Define the driver set and mapping
Create a **driver dictionary**:
- macro variables: U, GDP, CPI, policy rate, HPI, CRE, etc.
- market factors: yield curve nodes, spreads, FX, equity, vol surfaces, commodity shocks
- liquidity factors: haircuts, run-off rates, rollover ratios, margin period of risk

### Step 3 — Choose scenario families and generation methods
Use a hybrid:
- deterministic macro scenario (for solvency/credit)
- market shock (for trading/counterparty)
- reverse stress (to discover vulnerabilities)
- climate scenario family (strategic horizon)

### Step 4 — Quantify a first-pass scenario (draft)
Quantify with:
- sign constraints (what must go up/down)
- magnitude targets (benchmarking)
- consistency constraints (rates/inflation logic, spreads widen in stress)

### Step 5 — Coherence checks (must pass)
Common coherence checks:
- If unemployment rises sharply, GDP growth should be negative for multiple quarters.
- If risk aversion spikes, credit spreads widen, equity falls, vol rises.
- If policy rate cuts, yield curve should reflect realistic term premia.

### Step 6 — Severity scoring (must be documented)
Quantitative severity metrics to compute:
- Historical percentile of each move
- Z-score relative to long history
- “Distance” metric: Mahalanobis distance of vector shocks (with caution)

Example:
```text
z = (Δx - mean(Δx_hist)) / std(Δx_hist)
Mahalanobis = sqrt( (Δx - μ)' Σ^{-1} (Δx - μ) )
```

### Step 7 — Independent challenge and refinement loop
Require a structured challenge:
- “What is the weakest assumption?”
- “Where is the scenario under-stressing our concentrations?”
- “What breaks coherence?”
- “What happens if vol/correlation regime is worse?”

Log all changes and rationale.

---

## 6) Worked Example A: Build a coherent “Severe Recession + CRE Crash” macro scenario

### A.1 Narrative (one page)
**Story**
- A sharp decline in risk appetite triggers a drop in investment and consumption.
- CRE refinancing wall meets widening spreads and declining property values.
- Banks tighten credit; defaults rise; unemployment peaks high.

**Transmission channels**
- Unemployment ↑ → consumer credit PD ↑
- CRE prices ↓ and cap rates ↑ → CRE LGD ↑
- Spreads ↑ → funding cost ↑; NII pressure
- Equity ↓ and vol ↑ → trading losses; margin calls

### A.2 Select variables (minimum viable set)
```text
Macro: GDP growth, unemployment (U), inflation (CPI), policy rate (i)
Asset prices: equity index, HPI, CRE price index
Credit: BBB spread, HY spread (or broad credit spread index)
```

### A.3 Draft macro path (illustrative numbers; replace with your calibration)
9-quarter horizon (t=0..8). Values are illustrative and should be calibrated to your governance bar.

```text
Quarter t:       0      1      2      3      4      5      6      7      8
GDP yoy %:     +2.0   +0.5   -2.0   -3.5   -2.5   -1.0   +0.0   +0.8   +1.5
Unemp %:        4.0    5.2    7.0    8.8   10.0    9.6    8.7    7.8    7.0
CPI yoy %:      2.5    2.2    1.6    1.0    0.8    1.0    1.3    1.6    1.9
Policy rate %:  4.0    3.5    2.5    1.5    1.0    1.0    1.2    1.5    2.0
Equity (idx):  100     92     78     72     70     75     80     86     92
HPI (idx):     100     98     94     90     88     88     89     90     92
CRE (idx):     100     96     88     80     76     76     77     78     80
BBB spr (bp):  180    220    320    420    480    450    380    320    260
```

### A.4 Coherence check examples (how to defend)
- GDP contraction aligns with unemployment rise.
- Inflation drops with demand shock (unless you explicitly include a supply shock).
- Policy rate cuts in response to recession.
- Equity and CRE fall; spreads widen.

**If you want stagflation instead:** inflation rises while GDP falls, and policy rate may rise.

---

## 7) Worked Example B: Trading book “Global Market Shock” style scenario

### B.1 Shock table (illustrative)
```text
Risk factor shock set:
- Equity index: -35%
- Equity implied vol: +25 vol points (or +X% relative)
- Credit spreads: +250 bp HY, +150 bp IG (sector/rating granular if possible)
- Rates: bull flattening: -150 bp front-end, -75 bp long-end (example)
- FX: USD +10% vs EM basket (example)
- Commodities: oil -25% (example)
```

### B.2 Portfolio revaluation example (simple bond and option)
**Bond**
```text
Price change approx: ΔP ≈ -Duration * Δy
Example: Duration=5, Δy=+1.50% => ΔP ≈ -5 * 0.015 = -7.5%
```

**Option (delta-gamma approximation)**
```text
ΔV ≈ Delta * ΔS + 0.5 * Gamma * (ΔS)^2 + Vega * ΔVol
```
In stress, prefer **full repricing** if you can.

**Defense points**
- Show that shocks reflect crisis behavior: equity down, vol up, spreads up.
- Compare delta-only vs full repricing to prove you captured convexity.

---

## 8) Worked Example C: Credit loss calculation with PD×LGD×EAD (concrete numbers)

### C.1 Define a simple PD model
```text
PD_t = 1 / (1 + exp(-(β0 + β1*Unemp_t + β2*GDPgrowth_t + β3*Spread_t + β4*LTV)))
```

Example coefficients (illustrative):
```text
β0 = -8.0
β1 = +0.35     (higher unemployment increases PD)
β2 = -0.20     (higher growth reduces PD)
β3 = +0.002    (spread in bp increases PD slightly)
β4 = +1.5      (higher LTV increases PD)
```

Loan attributes:
```text
LTV = 0.80
EAD = 100,000,000
LGD = 45%   (0.45)
```

Macro inputs at t=4 from Example A:
```text
Unemp_t = 10.0
GDPgrowth_t = -2.5
Spread_t = 480
```

Compute:
```text
Score = β0 + β1*10 + β2*(-2.5) + β3*480 + β4*0.80
      = -8.0 + 3.5 + 0.5 + 0.96 + 1.2
      = -1.84
PD = 1 / (1 + exp(1.84)) ≈ 0.137  (13.7%)
EL = PD * LGD * EAD
   = 0.137 * 0.45 * 100,000,000
   ≈ 6,165,000
```

**Defense points**
- Monotonicity: PD rises when unemployment rises; test this explicitly.
- Downturn LGD: ensure LGD increases when collateral values (HPI/CRE) fall.
- EAD dynamics: stress drawdowns for commitments/credit lines.

---

## 9) Reverse stress template (defensible and systematic)

### 9.1 Define breach constraint
Example:
```text
Constraint: Expected loss E_p[L] ≥ 500,000,000
```

### 9.2 Exponential tilting method (discrete scenario set)
Given scenarios x_i (i=1..N) and loss L(x_i). Choose weights p_i:

```text
p_i ∝ exp(λ * L(x_i))
Choose λ such that Σ_i p_i L(x_i) = 500,000,000
```

Outputs:
- The tilted distribution p_i
- A “representative” reverse-stress scenario: weighted average of risk factors,
  or the top-k scenarios with largest p_i weights.

**Defense points**
- Shows the *most plausible breach* relative to history/simulation base.
- Explain what “plausible” means: minimal KL divergence from baseline.
- Ensure your base scenarios cover relevant risk regimes.

---

## 10) Review, challenge, and defense pack (what you need to defend “in all aspects”)

### 10.1 What a reviewer will challenge (and how to pre-answer)

**A) Severity vs plausibility**
- Provide severity metrics (percentiles/z-scores), and historical analogs.
- Document expert judgement and why it is reasonable.

**B) Coherence**
- Provide explicit cross-variable checks (sign constraints and economic logic).

**C) Relevance**
- Map to your material risks and concentrations; show how scenario targets them.

**D) Transmission**
- Explain why macro moves cause PD/LGD/PPNR/trading losses in your models.
- Provide sensitivity: change one variable and show effect.

**E) Model risk**
- Provide limitations and overlays.
- Validation and benchmarking plan (see PRA SS3/18 as an expectations reference).[^^ss318]

---

### 10.2 Independent challenge log template (copy/paste)

```text
Challenge ID:
Date:
Challenger (function):
Scenario / model component:
Issue type: [Severity | Plausibility | Coherence | Data | Model | Governance | Controls]
Description:
Evidence:
Impact assessment:
Proposed change / overlay:
Owner response:
Decision: [Accept | Accept with overlay | Reject with rationale]
Approver:
```

---

### 10.3 “Scenario Design Memo” template (board/supervisor defensible)

**1) Objective and use-case**
- capital planning / liquidity / limits / recovery

**2) Narrative**
- 1–2 pages, including transmission channels

**3) Variable set and horizon**
- list variables; why they matter; data sources

**4) Quantification method**
- deterministic macro builder / VAR / historical analog / expert judgement
- for market shocks: GMS-style shock construction

**5) Severity and plausibility evidence**
- benchmark tables, z-scores, historical comparisons

**6) Coherence checks**
- list checks; show pass/fail and fixes

**7) Mapping/transformation to risk factors**
- how macro becomes curves/spreads/vol/PD/LGD inputs

**8) Limitations and overlays**
- where data/model is weak and how you compensate

**9) Governance**
- approvals, challenge, versioning, audit trail

---

## 11) Implementation blueprint (to run this industrially)

### Operating cadence (example)
- Monthly: market shock and liquidity stress refresh
- Quarterly: enterprise scenario set + full run + committee sign-off
- Annually: scenario library refresh + deep model validation + governance review

### Minimum technical components
- Scenario data store (versioned time series and shock sets)
- Mapping engine (macro → risk factors → model inputs)
- Loss engines (credit PD/LGD/EAD; trading reval; liquidity cashflows)
- Controls: run reproducibility, data lineage, override logging

### Roles (RACI idea)
- Scenario Owner (Risk)
- Quant Team (Risk Analytics)
- Finance (capital, PPNR)
- Treasury (liquidity/funding)
- Model Risk/Validation (independent)
- Front Office (trading/counterparty specifics)
- Governance secretariat (committees, documentation)

---

## 12) References (public, authoritative)

[^fed2025pdf]: Federal Reserve — “2025 Stress Test Scenarios” (PDF, Feb 5, 2025): https://www.federalreserve.gov/publications/files/2025-stress-test-scenarios-20250205.pdf
[^gmsdoc2025]: Federal Reserve — “Supervisory Stress Test Documentation: Global Market Shock Component” (PDF, Oct 2025): https://www.federalreserve.gov/supervisionreg/files/gms-model.pdf
[^bcbs155]: BCBS — “Principles for sound stress testing practices and supervision” (May 2009, PDF): https://www.bis.org/publ/bcbs155.pdf
[^fsb2018]: FSB — “Stress testing principles” page (Oct 2018): https://www.fsb.org/2018/10/stress-testing-principles/
[^ss318]: Bank of England / PRA — SS3/18 “Model risk management principles for stress testing” (PDF): https://www.bankofengland.co.uk/-/media/boe/files/prudential-regulation/supervisory-statement/2018/ss318.pdf
[^bcbs_mr]: BCBS — “Minimum capital requirements for market risk” (PDF): https://www.bis.org/bcbs/publ/d457.pdf
[^pfmi]: CPMI-IOSCO — Principles for Financial Market Infrastructures (PFMI) portal: https://www.iosco.org/v2/about/?subSection=cpmi_iosco&subSection1=pfmi
[^ccp_resilience]: CPMI-IOSCO — “Resilience of central counterparties (CCPs): Further guidance on the PFMI” (Jul 2017): https://www.bis.org/cpmi/publ/d163.htm
[^cme_span_overview]: CME — SPAN methodology overview (web): https://www.cmegroup.com/solutions/risk-management/performance-bonds-margins/span-methodology-overview.html
[^cme_span_pdf]: CME — “SPAN Methodology” (PDF): https://www.cmegroup.com/clearing/files/span-methodology.pdf
[^ngfs_v5]: NGFS — Climate Scenarios Technical Documentation (vintage 5 / v5, PDF): https://www.ngfs.net/system/files/2025-01/NGFS%20Climate%20Scenarios%20Technical%20Documentation.pdf
[^eba_env]: EBA — Final Guidelines on environmental scenario analysis (Nov 2025; applies 1 Jan 2027): https://www.eba.europa.eu/sites/default/files/2025-11/170da4c8-9b56-4fb0-ad60-94d433b7e866/Guidelines%20on%20environmental%20scenario%20analysis.pdf
[^ofr_el]: Office of Financial Research (OFR) working paper — “Stress Scenario Selection by Empirical Likelihood” (Glasserman et al.): https://www.financialresearch.gov/working-papers/files/OFRwp-2015-09_Stress_Scenario_Selection_by_Empirical_Likelihood.pdf

---

## 13) What to do next (quick-start plan)
If you want to implement this in a real program, do this in order:

1) Build your **material risk inventory** + driver dictionary.
2) Stand up a **scenario library** with 8 families (minimum).
3) Build a deterministic macro scenario (Example A template) and pass coherence checks.
4) Build a GMS-style shock set (Example B template) and revalue trading/counterparty.
5) Implement PD×LGD×EAD translation with monotonicity tests (Example C template).
6) Run reverse stress (tilting) against your breach thresholds and add the top vulnerabilities to the library.
7) Create the defense pack: design memo, severity dashboard, challenge log, validation plan.

---

*Version:* 1.0 (generated 2025-12-12)
