# Industry-Leading Stress Testing Models & Scenario Development Framework
## A Complete Technical Guide for Market Risk Professionals

---

# Table of Contents

1. [Executive Summary](#1-executive-summary)
2. [Regulatory Framework Overview](#2-regulatory-framework-overview)
3. [Best-in-Class Models - Complete Technical Analysis](#3-best-in-class-models---complete-technical-analysis)
   - 3.1 [Monte Carlo Simulation](#31-monte-carlo-simulation-framework)
   - 3.2 [Vector Autoregression (VAR/BVAR)](#32-vector-autoregression-varbvar-models)
   - 3.3 [GARCH Family Models](#33-garch-family-models)
   - 3.4 [Copula-Based Dependence Modeling](#34-copula-based-dependence-modeling)
   - 3.5 [Extreme Value Theory (EVT)](#35-extreme-value-theory-evt)
   - 3.6 [DSGE Models](#36-dynamic-stochastic-general-equilibrium-dsge-models)
   - 3.7 [Reverse Stress Testing](#37-reverse-stress-testing)
   - 3.8 [Machine Learning Approaches](#38-machine-learning-approaches)
4. [Scenario Design - Worked Examples](#4-scenario-design---worked-examples)
5. [Complete Stress Scenario Development Lifecycle](#5-complete-stress-scenario-development-lifecycle)
6. [Challenge & Defense Framework](#6-challenge--defense-framework)
7. [Systematic Implementation Framework](#7-systematic-implementation-framework)
8. [Model Selection Decision Tree](#8-model-selection-decision-tree)
9. [References](#9-references)

---

# 1. Executive Summary

Stress testing has evolved from a simple regulatory compliance exercise into a sophisticated, multi-dimensional risk management framework. This guide provides:

- **Complete mathematical foundations** for each industry-leading model
- **Worked examples** of scenario design and calibration
- **Challenge questions and defense strategies** for model validation
- **Systematic framework** for implementation

**Key Models Covered:**
| Model | Primary Use | Industry Leaders |
|-------|-------------|------------------|
| Monte Carlo | Full loss distribution | All G-SIBs |
| BVAR | Macro scenario coherence | Fed, ECB, BoI |
| GARCH | Volatility dynamics | Trading desks |
| Copulas | Tail dependence | GS, MS, insurers |
| EVT | Extreme quantiles | Reinsurers |
| DSGE | Structural scenarios | Central banks |
| Reverse ST | Breaking point identification | UK/EU banks |

---

# 2. Regulatory Framework Overview

## 2.1 U.S. Federal Reserve (CCAR/DFAST)

**Applicability:** Banks with ≥$100B in assets

**Key Requirements:**
- Annual supervisory stress test
- 9-quarter projection horizon
- Severely adverse scenario: unemployment to 10%, equity decline 45-55%, HPI decline 25-30%
- Global Market Shock (GMS) for trading book
- Counterparty default component for G-SIBs

**Capital Impact:** Results feed directly into Stress Capital Buffer (SCB)

```
SCB = max(2.5%, Starting CET1 - Minimum Stressed CET1 + 4 quarters planned dividends)
```

## 2.2 EBA/ECB Framework

**Applicability:** EU significant institutions

**Key Requirements:**
- Biennial EU-wide stress test
- 3-year projection horizon
- Static balance sheet assumption
- Bottom-up approach (bank models, supervisory constraints)
- SREP integration for Pillar 2 guidance

## 2.3 Framework Comparison

| Dimension | Federal Reserve | EBA/ECB |
|-----------|----------------|---------|
| Approach | Top-down (Fed models) | Bottom-up (bank models) |
| Frequency | Annual | Biennial |
| Horizon | 9 quarters | 3 years |
| Balance Sheet | Dynamic | Static |
| Capital Impact | Direct (SCB) | SREP/Pillar 2 |
| Disclosure | Bank-level results | Bank-level results |

---

# 3. Best-in-Class Models - Complete Technical Analysis

## 3.1 Monte Carlo Simulation Framework

### Industry Status
**Gold Standard** for enterprise-wide capital adequacy assessment

### Who Uses It
JPMorgan Chase, Goldman Sachs, Morgan Stanley, Citigroup, Bank of America, Wells Fargo

### Mathematical Foundation

**Core Equation - Geometric Brownian Motion:**

```
S(t + Δt) = S(t) × exp[(μ - σ²/2)Δt + σ × √Δt × Z]
```

Where:
- `S(t)` = Asset price at time t
- `μ` = Drift rate (expected return)
- `σ` = Volatility
- `Δt` = Time step
- `Z` = Standard normal random variable ~ N(0,1)

**For Correlated Assets - Cholesky Decomposition:**

Given correlation matrix R, find lower triangular L such that:
```
R = L × L'
```

Then for n correlated assets with independent standard normals Z₁, Z₂, ..., Zₙ:
```
[ε₁]   [L₁₁  0    0  ] [Z₁]
[ε₂] = [L₂₁  L₂₂  0  ] [Z₂]
[ε₃]   [L₃₁  L₃₂  L₃₃] [Z₃]
```

**Example - 3 Asset Correlation:**

Given correlation matrix:
```
R = [1.0   0.6   0.3]
    [0.6   1.0   0.5]
    [0.3   0.5   1.0]
```

Cholesky decomposition yields:
```
L = [1.000  0.000  0.000]
    [0.600  0.800  0.000]
    [0.300  0.400  0.866]
```

### Worked Example - Portfolio VaR Under Stress

**Setup:**
- Portfolio: $100M equity, $50M corporate bonds, $30M commodities
- Horizon: 1 quarter
- Simulations: 100,000

**Step 1: Define Parameters**
```
Equity:  μ = 0.08/4, σ = 0.20/√4 = 0.10
Bonds:   μ = 0.04/4, σ = 0.06/√4 = 0.03
Commod:  μ = 0.05/4, σ = 0.25/√4 = 0.125
```

**Step 2: Stress Correlations (Crisis Regime)**
```
Normal:  ρ_equity_bonds = 0.2,  ρ_equity_commod = 0.3
Stress:  ρ_equity_bonds = 0.6,  ρ_equity_commod = 0.7
```

**Step 3: Simulate 100,000 Paths**

For each simulation i = 1 to 100,000:
```
Z = [Z₁, Z₂, Z₃] ~ N(0, I₃)
ε = L × Z  (correlated shocks)

R_equity(i) = exp[(0.02 - 0.01²/2) + 0.10 × ε₁] - 1
R_bonds(i)  = exp[(0.01 - 0.03²/2) + 0.03 × ε₂] - 1
R_commod(i) = exp[(0.0125 - 0.125²/2) + 0.125 × ε₃] - 1

Portfolio_Loss(i) = -[100M × R_equity(i) + 50M × R_bonds(i) + 30M × R_commod(i)]
```

**Step 4: Calculate Risk Metrics**
```
VaR_99 = Percentile(Portfolio_Loss, 99) = $28.5M
ES_99  = Mean(Portfolio_Loss | Loss > VaR_99) = $35.2M
```

### Intuitive Rationale

Monte Carlo explores the **entire distribution** of possible outcomes rather than a single point estimate. Instead of asking "what happens if unemployment hits 10%?", it asks "what's the probability that losses exceed $X billion across all possible futures?"

**Key Insight:** Running history forward millions of times with different random seeds reveals tail risks that deterministic scenarios miss.

### Lifecycle Placement

| Phase | Monte Carlo Role |
|-------|------------------|
| Scenario Generation | Generate thousands of internally consistent scenarios |
| Loss Estimation | Compute full loss distribution |
| Model Validation | Verify deterministic results fall within probability bounds |
| Capital Calculation | Economic capital at 99.9% confidence |

### Challenge Questions & Defense

**Q1: "Why 100,000 simulations? Isn't that arbitrary?"**

**Defense:** Convergence analysis shows that key percentiles (99th, 99.9th) stabilize within ±2% at 100,000 simulations. We run convergence diagnostics:
```
VaR_99 at 10K sims:   $27.8M ± $1.2M
VaR_99 at 50K sims:   $28.3M ± $0.6M
VaR_99 at 100K sims:  $28.5M ± $0.3M
```

**Q2: "How do you validate that your correlation assumptions are appropriate?"**

**Defense:** 
1. Historical calibration using rolling 252-day windows
2. Crisis-period recalibration (2008-09, 2020) for stress correlations
3. DCC-GARCH model to capture time-varying correlations
4. Sensitivity analysis: Results presented across correlation range [ρ_base - 0.2, ρ_base + 0.2]

**Q3: "Monte Carlo assumes known distributions. What about model risk?"**

**Defense:**
1. Multiple distribution specifications tested (Normal, Student-t, Skewed-t)
2. EVT applied to tails beyond 95th percentile
3. Model uncertainty quantified via parameter bootstrap
4. Results presented with confidence intervals, not point estimates

---

## 3.2 Vector Autoregression (VAR/BVAR) Models

### Industry Status
**Standard** for macroeconomic scenario calibration and coherence testing

### Who Uses It
Federal Reserve (scenario design), ECB (NAWM support), Bank of Italy, all G-SIBs for internal scenarios

### Mathematical Foundation

**VAR(p) Model:**

For a vector of n macroeconomic variables Y_t:

```
Y_t = c + Φ₁Y_{t-1} + Φ₂Y_{t-2} + ... + Φ_pY_{t-p} + ε_t
```

Where:
- `Y_t` = n×1 vector of endogenous variables at time t
- `c` = n×1 vector of constants
- `Φᵢ` = n×n coefficient matrices
- `ε_t` = n×1 vector of error terms with E[ε_t] = 0, Var[ε_t] = Σ

**Expanded Form (3-variable example):**

```
[GDP_t    ]   [c₁]   [φ₁₁ φ₁₂ φ₁₃] [GDP_{t-1}    ]   [ε₁_t]
[Unemp_t  ] = [c₂] + [φ₂₁ φ₂₂ φ₂₃] [Unemp_{t-1}  ] + [ε₂_t]
[Spread_t ]   [c₃]   [φ₃₁ φ₃₂ φ₃₃] [Spread_{t-1} ]   [ε₃_t]
```

**Bayesian VAR (BVAR) - Minnesota Prior:**

To address overparameterization, impose shrinkage prior:

```
E[Φᵢⱼₖ] = δᵢⱼ if k=1 else 0  (own first lag = 1, others = 0)

Var[Φᵢⱼₖ] = λ² × (σᵢ/σⱼ)² × (1/k²)
```

Where:
- `λ` = overall tightness (typically 0.1-0.2)
- `σᵢ/σⱼ` = scale adjustment for different variable units
- `1/k²` = decay for longer lags

### Worked Example - Scenario Calibration

**Objective:** Calibrate severely adverse scenario with unemployment rising to 10%

**Step 1: Estimate BVAR on Historical Data**

Variables: GDP growth, Unemployment, 10Y Treasury, BBB Spread, HPI, S&P 500
Sample: 1980Q1 - 2024Q4 (quarterly)
Lags: 4

**Step 2: Identify Structural Shock**

Using Cholesky identification (unemployment ordered last for demand shock):
```
Structural shock to unemployment: ε_unemp = +3.5 standard deviations
```

**Step 3: Compute Impulse Response Functions**

```
Quarter | Unemployment | GDP Growth | BBB Spread | HPI      | S&P 500
--------|--------------|------------|------------|----------|--------
Q1      | +1.5%        | -2.1%      | +180bp     | -3.2%    | -15%
Q2      | +2.8%        | -3.5%      | +320bp     | -7.1%    | -28%
Q3      | +3.9%        | -2.8%      | +380bp     | -11.5%   | -35%
Q4      | +4.5%        | -1.9%      | +350bp     | -15.2%   | -38%
Q5      | +4.8%        | -0.8%      | +300bp     | -18.1%   | -40%
Q6      | +5.2%        | +0.2%      | +260bp     | -20.5%   | -42%
Q7      | +5.5%        | +0.9%      | +220bp     | -22.3%   | -41%
Q8      | +5.8%        | +1.5%      | +180bp     | -23.8%   | -38%
Q9      | +5.9%        | +2.0%      | +150bp     | -24.8%   | -35%
```

**Step 4: Scenario Severity Assessment**

Calculate percentile of scenario path in simulated distribution:
```
Joint probability of scenario path ≈ 2.3% (1-in-43 year event)
```

### Intuitive Rationale

VAR models capture the **interconnectedness** of macroeconomic variables. A shock to GDP doesn't happen in isolation—it affects unemployment, which affects consumption, which feeds back to GDP. By modeling these dynamics explicitly, scenarios maintain **internal consistency**.

**Key Insight:** When unemployment rises 6 percentage points, the model ensures GDP, house prices, and credit spreads respond in historically consistent ways—not arbitrary combinations.

### Lifecycle Placement

| Phase | VAR/BVAR Role |
|-------|---------------|
| Scenario Design | Calibrate variable paths for internal consistency |
| Severity Assessment | Compute joint probability of scenario |
| Conditional Forecasting | Project paths for unspecified variables |
| Narrative Support | Validate economic story with historical precedent |

### Challenge Questions & Defense

**Q1: "VAR is linear. Don't crises exhibit non-linear dynamics?"**

**Defense:**
1. Threshold VAR (TVAR) estimated for crisis vs. normal regimes
2. Regime-switching VAR captures state-dependent dynamics
3. Asymmetric GARCH errors allow non-linear volatility
4. Results compared across linear and non-linear specifications

**Q2: "How do you handle structural breaks (e.g., post-COVID)?"**

**Defense:**
1. Rolling estimation windows (20-year) to capture evolution
2. Explicit dummy variables for structural breaks
3. Time-varying parameter BVAR for gradual changes
4. Post-2020 period down-weighted in estimation

**Q3: "Minnesota prior is arbitrary. Why not a different prior?"**

**Defense:**
1. Minnesota prior has strong theoretical foundation (random walk benchmark)
2. Sensitivity analysis conducted with alternative priors (SSVS, normal-Wishart)
3. Out-of-sample forecast comparison validates prior choice
4. Prior tightness (λ) optimized via marginal likelihood

---

## 3.3 GARCH Family Models

### Industry Status
**Essential** for market risk stress testing and VaR/ES computation

### Who Uses It
All major trading banks, required for FRTB internal models

### Mathematical Foundation

**GARCH(1,1) - The Workhorse:**

```
Return:    r_t = μ + ε_t,  where ε_t = σ_t × z_t,  z_t ~ N(0,1)

Variance:  σ²_t = ω + α × ε²_{t-1} + β × σ²_{t-1}
```

Where:
- `ω` = long-run variance weight (ω > 0)
- `α` = shock impact coefficient (α ≥ 0)
- `β` = persistence coefficient (β ≥ 0)
- Stationarity requires: α + β < 1

**Long-Run Variance:**
```
σ²_LR = ω / (1 - α - β)
```

**GJR-GARCH (Asymmetric/Leverage Effect):**

```
σ²_t = ω + (α + γ × I_{t-1}) × ε²_{t-1} + β × σ²_{t-1}
```

Where `I_{t-1} = 1 if ε_{t-1} < 0` (negative shock), else 0

**Key Insight:** γ > 0 means negative returns increase volatility more than positive returns of equal magnitude—the "leverage effect"

**DCC-GARCH (Dynamic Conditional Correlation):**

For multivariate returns, correlation evolves as:

```
Q_t = (1 - a - b) × Q̄ + a × (u_{t-1} × u'_{t-1}) + b × Q_{t-1}

R_t = diag(Q_t)^{-1/2} × Q_t × diag(Q_t)^{-1/2}
```

Where:
- `Q̄` = unconditional correlation matrix
- `u_t` = standardized residuals
- `a, b` = correlation dynamics parameters

### Worked Example - Stress VaR Calculation

**Setup:** Equity trading book, $500M notional

**Step 1: Estimate GJR-GARCH(1,1) on S&P 500**

Using daily returns 2019-2024:
```
ω = 0.000002
α = 0.05
γ = 0.08  (leverage effect)
β = 0.90

Long-run volatility: σ_LR = √(0.000002 / (1 - 0.05 - 0.08/2 - 0.90)) = 16.3% annualized
```

**Step 2: Compute Current Conditional Volatility**

Given yesterday's return r_{t-1} = -2.5% and σ_{t-1} = 22%:
```
ε_{t-1} = -0.025
ε²_{t-1} = 0.000625
I_{t-1} = 1 (negative return)

σ²_t = 0.000002 + (0.05 + 0.08×1) × 0.000625 + 0.90 × 0.0484
     = 0.000002 + 0.000081 + 0.0436
     = 0.0437

σ_t = 20.9% (daily: 20.9% / √252 = 1.32%)
```

**Step 3: Calculate Stress VaR**

10-day 99% VaR:
```
VaR_99_10d = $500M × 1.32% × √10 × 2.33 = $48.7M
```

Under stress (volatility doubles to 42%):
```
VaR_99_10d_stress = $500M × 2.64% × √10 × 2.33 = $97.4M
```

### Intuitive Rationale

Financial markets exhibit **volatility clustering**—periods of high volatility persist, as do calm periods. GARCH captures this reality: after a large move, expect continued turbulence; after quiet markets, expect continued calm.

**Key Insight:** A 10% market decline isn't just a 10% shock—it's typically accompanied by volatility doubling or tripling, which compounds risk through feedback effects.

### Lifecycle Placement

| Phase | GARCH Role |
|-------|------------|
| Marginal Distribution | Filter returns for copula estimation |
| Volatility Forecasting | Project stressed volatility paths |
| VaR/ES Computation | Conditional risk estimates |
| Trading Book Stress | FRTB internal model compliance |

### Challenge Questions & Defense

**Q1: "GARCH assumes normal innovations. Financial returns have fat tails."**

**Defense:**
1. Student-t innovations estimated with degrees of freedom ν ≈ 5-8
2. Skewed-t distribution captures asymmetry
3. EVT applied to standardized residuals beyond 95th percentile
4. QQ-plots and Kolmogorov-Smirnov tests validate distribution choice

**Q2: "How do you forecast volatility beyond a few days?"**

**Defense:**
1. Multi-step forecasts use law of iterated expectations:
   ```
   E[σ²_{t+h}] = σ²_LR + (α + β)^h × (σ²_t - σ²_LR)
   ```
2. Term structure of volatility validated against options-implied volatility
3. For longer horizons (quarterly), HAR-RV models complement GARCH

**Q3: "DCC-GARCH is computationally intensive for large portfolios."**

**Defense:**
1. Two-step estimation: univariate GARCH first, then DCC parameters
2. Composite likelihood methods for 100+ assets
3. Block structure exploited for computational efficiency
4. Factor-DCC reduces dimensionality while preserving dynamics

---

## 3.4 Copula-Based Dependence Modeling

### Industry Status
**State-of-the-Art** for tail dependence and systemic risk modeling

### Who Uses It
Goldman Sachs, Morgan Stanley, major European banks, insurance companies, Basel III CVA

### Mathematical Foundation

**Sklar's Theorem:**

Any multivariate distribution F(x₁, x₂, ..., xₙ) can be written as:

```
F(x₁, x₂, ..., xₙ) = C(F₁(x₁), F₂(x₂), ..., Fₙ(xₙ))
```

Where:
- `C` = copula function (dependence structure)
- `Fᵢ` = marginal CDF of variable i

**Key Copula Types:**

**1. Gaussian Copula:**
```
C_Gaussian(u₁, u₂; ρ) = Φ₂(Φ⁻¹(u₁), Φ⁻¹(u₂); ρ)
```
- No tail dependence: λ_L = λ_U = 0
- Suitable for normal market conditions

**2. Student-t Copula:**
```
C_t(u₁, u₂; ρ, ν) = t₂,ν(t⁻¹_ν(u₁), t⁻¹_ν(u₂); ρ)
```
- Symmetric tail dependence:
  ```
  λ = 2 × t_{ν+1}(-√((ν+1)(1-ρ)/(1+ρ)))
  ```
- Lower ν = fatter tails = higher tail dependence

**3. Clayton Copula:**
```
C_Clayton(u₁, u₂; θ) = (u₁^{-θ} + u₂^{-θ} - 1)^{-1/θ}
```
- Lower tail dependence only: λ_L = 2^{-1/θ}, λ_U = 0
- Captures joint crash risk

**4. Gumbel Copula:**
```
C_Gumbel(u₁, u₂; θ) = exp(-[(-ln u₁)^θ + (-ln u₂)^θ]^{1/θ})
```
- Upper tail dependence only: λ_L = 0, λ_U = 2 - 2^{1/θ}
- Captures joint boom risk

**5. Vine Copulas (Pair-Copula Constructions):**

For n variables, decompose joint density using conditional bivariate copulas:

```
f(x₁, x₂, x₃) = f₁(x₁) × f₂(x₂) × f₃(x₃) 
              × c₁₂(F₁(x₁), F₂(x₂))
              × c₁₃(F₁(x₁), F₃(x₃))
              × c₂₃|₁(F_{2|1}(x₂|x₁), F_{3|1}(x₃|x₁))
```

### Worked Example - Systemic Risk Assessment

**Objective:** Model joint tail risk between 4 major banks

**Step 1: Fit Marginal GARCH Models**

For each bank's equity returns, estimate GJR-GARCH(1,1) with Student-t innovations.

**Step 2: Transform to Uniform Marginals**

Using probability integral transform (PIT):
```
u_i,t = F_i(r_i,t | information_{t-1})
```

**Step 3: Fit Student-t Copula**

Estimate correlation matrix R and degrees of freedom ν:
```
R = [1.00  0.72  0.65  0.58]
    [0.72  1.00  0.68  0.61]
    [0.65  0.68  1.00  0.55]
    [0.58  0.61  0.55  1.00]

ν = 4.2 (estimated via MLE)
```

**Step 4: Calculate Tail Dependence**

For ν = 4.2 and average ρ = 0.64:
```
λ = 2 × t_{5.2}(-√((5.2)(1-0.64)/(1+0.64)))
  = 2 × t_{5.2}(-1.10)
  = 2 × 0.16
  = 0.32
```

**Interpretation:** 32% probability that if one bank is in its worst 1% of outcomes, the other is also in its worst 1%

**Step 5: CoVaR Calculation**

CoVaR measures risk of bank j conditional on bank i being in distress:
```
CoVaR^j_{99|i in distress} = VaR^j_{99} × (1 + Δ)

Where Δ depends on copula parameters and conditional distribution
```

### Intuitive Rationale

The 2008 financial crisis demonstrated that **correlations spike during stress**—diversification benefits disappear precisely when needed most. Copulas model "tail dependence": the tendency for extreme events to occur simultaneously.

**Key Insight:** A correlation of 0.3 in normal times might translate to 0.8+ during a crisis. Gaussian copula (used infamously in CDO pricing) has ZERO tail dependence—a critical flaw exposed in 2008.

### Lifecycle Placement

| Phase | Copula Role |
|-------|-------------|
| Scenario Generation | Create joint scenarios with appropriate tail dependence |
| Systemic Risk | Model contagion and interconnectedness |
| CoVaR/MES | Measure systemic risk contribution |
| CVA | Counterparty credit risk under Basel III |

### Challenge Questions & Defense

**Q1: "How do you choose between copula families?"**

**Defense:**
1. Statistical tests: Cramér-von Mises, Kolmogorov-Smirnov on copula
2. Information criteria: AIC, BIC across copula families
3. Economic rationale: Clayton for crash risk, Gumbel for bubble risk
4. Empirical tail dependence coefficient estimation

**Q2: "Copulas are static. Don't dependencies change over time?"**

**Defense:**
1. Time-varying copulas with DCC-style dynamics
2. Regime-switching copulas (calm vs. crisis)
3. Rolling window estimation (252-day)
4. Results presented for multiple time periods

**Q3: "Vine copulas have explosion of parameters for high dimensions."**

**Defense:**
1. Truncated vines (set distant pair-copulas to independence)
2. Regularized estimation with sparsity penalties
3. Factor copula structures reduce dimensionality
4. Compare simplified vine to full specification for materiality

---

## 3.5 Extreme Value Theory (EVT)

### Industry Status
**Essential** for tail risk quantification and regulatory capital

### Who Uses It
Swiss Re, Munich Re, all G-SIBs for trading book, FRTB Expected Shortfall

### Mathematical Foundation

**Generalized Pareto Distribution (GPD) - Peaks Over Threshold:**

For exceedances Y = X - u above threshold u:

```
F_u(y) = P(X - u ≤ y | X > u) = 1 - (1 + ξy/σ)^{-1/ξ}
```

Where:
- `ξ` = shape parameter (tail index)
  - ξ > 0: Heavy tails (Fréchet domain)
  - ξ = 0: Exponential tails (Gumbel domain)
  - ξ < 0: Bounded tails (Weibull domain)
- `σ` = scale parameter (σ > 0)

**Financial returns typically have ξ ∈ [0.1, 0.4]**

**VaR and ES from GPD:**

```
VaR_p = u + (σ/ξ) × [(n/N_u × (1-p))^{-ξ} - 1]

ES_p = VaR_p / (1-ξ) + (σ - ξu) / (1-ξ)
```

Where:
- `n` = total observations
- `N_u` = observations exceeding threshold u

### Worked Example - Trading Book Tail Risk

**Objective:** Calculate 99.9% ES for equity derivatives desk

**Step 1: Extract Daily P&L and Identify Threshold**

P&L history: 1,000 observations
Threshold selection using Mean Excess Plot:
```
u = -$5M (approximately 90th percentile of losses)
N_u = 103 exceedances
```

**Step 2: Estimate GPD Parameters (MLE)**

```
ξ̂ = 0.28  (heavy tails confirmed)
σ̂ = $2.1M
```

**Step 3: Calculate Risk Measures**

99% VaR:
```
VaR_99 = -5 + (2.1/0.28) × [(1000/103 × 0.01)^{-0.28} - 1]
       = -5 + 7.5 × [0.97^{-0.28} - 1]
       = -5 + 7.5 × 0.69
       = -5 + 5.2
       = $10.2M
```

99.9% VaR:
```
VaR_999 = -5 + 7.5 × [(1000/103 × 0.001)^{-0.28} - 1]
        = -5 + 7.5 × [0.097^{-0.28} - 1]
        = -5 + 7.5 × 1.42
        = $15.7M
```

99.9% ES:
```
ES_999 = 15.7 / (1 - 0.28) + (2.1 - 0.28 × 5) / (1 - 0.28)
       = 21.8 + 1.0
       = $22.8M
```

**Comparison with Normal Distribution:**

Under normality (same mean and variance):
```
VaR_999_normal = μ + 3.09 × σ = $12.3M  (22% UNDER-ESTIMATE)
ES_999_normal = μ + 3.37 × σ = $13.4M   (41% UNDER-ESTIMATE)
```

### Intuitive Rationale

Normal distributions dramatically **underestimate tail risk**—a "six sigma" event under normality should occur once every 1.4 million years, yet we observe them regularly. EVT recognizes that extreme events follow **different statistical laws** than typical fluctuations.

**Key Insight:** By focusing specifically on the tail behavior (the GPD), EVT provides reliable estimates for events beyond historical experience. It allows extrapolation to 99.9th percentile even with limited tail data.

### Lifecycle Placement

| Phase | EVT Role |
|-------|----------|
| Tail Risk | Quantify extreme loss probabilities |
| Expected Shortfall | FRTB-compliant ES calculation |
| Marginal Modeling | Semi-parametric distributions for copulas |
| Scenario Calibration | Assess severity of proposed scenarios |

### Challenge Questions & Defense

**Q1: "How do you select the threshold u?"**

**Defense:**
1. Mean Excess Plot: linear region indicates GPD appropriate
2. Parameter stability: ξ̂ stable across threshold choices
3. Trade-off: lower u = more data but increased bias; higher u = less bias but more variance
4. Rule of thumb: top 5-10% of data (adjusted for sample size)

**Q2: "GPD assumes independence. Financial returns are autocorrelated."**

**Defense:**
1. Pre-filter with GARCH to remove volatility clustering
2. Apply EVT to standardized residuals (approximately iid)
3. Decluster extremes using runs method
4. POT applied to independent blocks

**Q3: "The shape parameter ξ has high estimation uncertainty."**

**Defense:**
1. Profile likelihood confidence intervals reported
2. Bayesian estimation with informative prior (ξ ∈ [0, 0.5] for financial data)
3. Bootstrap confidence intervals
4. Sensitivity analysis across ξ range

---

## 3.6 Dynamic Stochastic General Equilibrium (DSGE) Models

### Industry Status
**Central Bank Standard** for structural macroeconomic scenario generation

### Who Uses It
Federal Reserve (EDO Model), ECB (NAWM, BEAST), Bank of England, Sveriges Riksbank, IMF

### Mathematical Foundation

**Core New Keynesian Structure:**

**1. IS Curve (Aggregate Demand):**
```
y_t = E_t[y_{t+1}] - (1/σ)(i_t - E_t[π_{t+1}] - r*) + g_t
```
Where:
- `y_t` = output gap
- `i_t` = nominal interest rate
- `π_t` = inflation
- `r*` = natural rate of interest
- `g_t` = demand shock
- `σ` = intertemporal elasticity of substitution

**2. New Keynesian Phillips Curve (Aggregate Supply):**
```
π_t = β × E_t[π_{t+1}] + κ × y_t + u_t
```
Where:
- `β` = discount factor (~0.99)
- `κ` = slope (function of price stickiness)
- `u_t` = cost-push shock

**3. Taylor Rule (Monetary Policy):**
```
i_t = ρ × i_{t-1} + (1-ρ)[r* + π* + φ_π(π_t - π*) + φ_y × y_t] + ε^m_t
```
Where:
- `ρ` = interest rate smoothing (~0.8)
- `φ_π` = inflation response (~1.5)
- `φ_y` = output response (~0.5)
- `ε^m_t` = monetary policy shock

**Smets-Wouters Extensions:**
- Habit formation in consumption
- Investment adjustment costs
- Variable capital utilization
- Wage stickiness (Calvo pricing)
- Indexation to past inflation

### Worked Example - Financial Crisis Scenario

**Objective:** Generate internally consistent scenario with GDP decline of 4%

**Step 1: Calibrate to U.S. Economy**

```
β = 0.99 (discount factor)
σ = 1.0 (log utility)
κ = 0.05 (moderate price stickiness)
φ_π = 1.5 (Taylor rule inflation response)
φ_y = 0.5 (Taylor rule output response)
ρ = 0.8 (interest rate smoothing)
```

**Step 2: Identify Shock Required**

To generate y_t = -4%, solve for required demand shock:
```
From IS curve (assuming no expected recovery):
-0.04 = 0 - (1/1.0)(i_t - E_t[π_{t+1}] - r*) + g_t

With ZLB binding (i_t = 0) and deflation expectation E_t[π_{t+1}] = -1%:
-0.04 = -(0 - (-0.01) - 0.02) + g_t
-0.04 = -(-0.01) + g_t
g_t = -0.05  (5% demand shock)
```

**Step 3: Trace Through Model Dynamics**

```
Quarter | Output Gap | Inflation | Interest Rate | Unemployment*
--------|------------|-----------|---------------|---------------
Q1      | -4.0%      | -0.5%     | 0.0% (ZLB)    | +2.5%
Q2      | -3.8%      | -0.8%     | 0.0% (ZLB)    | +3.8%
Q3      | -3.5%      | -0.6%     | 0.0% (ZLB)    | +4.5%
Q4      | -3.0%      | -0.3%     | 0.0% (ZLB)    | +4.8%
Q5      | -2.5%      | 0.0%      | 0.0% (ZLB)    | +4.6%
Q6      | -2.0%      | +0.2%     | 0.25%         | +4.2%
Q7      | -1.5%      | +0.5%     | 0.50%         | +3.7%
Q8      | -1.0%      | +0.8%     | 0.75%         | +3.1%
Q9      | -0.5%      | +1.0%     | 1.00%         | +2.5%

*Unemployment linked via Okun's Law: Δu = -0.5 × Δy
```

### Intuitive Rationale

Unlike purely statistical models, DSGE models are **structural**—they tell a coherent economic story. A productivity shock has different implications than a demand shock, even if both produce the same GDP decline.

**Key Insight:** The economic narrative affects which portfolios are most vulnerable and how recovery unfolds. A demand-driven recession hits consumer credit differently than a supply shock.

### Lifecycle Placement

| Phase | DSGE Role |
|-------|-----------|
| Scenario Design | Generate structurally consistent macro paths |
| Narrative Development | Provide economic story behind scenario |
| Policy Analysis | Model central bank and fiscal response |
| Counterfactual Analysis | "What if Fed had responded differently?" |

### Challenge Questions & Defense

**Q1: "DSGE models failed to predict the 2008 crisis."**

**Defense:**
1. Post-crisis DSGE models incorporate financial frictions (Bernanke-Gertler-Gilchrist)
2. Shadow banking sector now modeled (Gertler-Kiyotaki)
3. Liquidity risk and fire sales included
4. DSGE used for scenario consistency, not forecasting

**Q2: "Rational expectations assumption is unrealistic."**

**Defense:**
1. Bounded rationality extensions (learning models)
2. Heterogeneous expectations across agents
3. For stress testing, rational expectations provides discipline
4. Alternative behavioral models run as challengers

**Q3: "DSGE models are too complex for practical use."**

**Defense:**
1. Smets-Wouters is tractable (7 variables, well-documented)
2. Estimation via Bayesian methods is standard
3. Central banks use daily—proven practical utility
4. Results validated against reduced-form VAR

---

## 3.7 Reverse Stress Testing

### Industry Status
**Mandatory** in UK/EU, growing adoption in US

### Who Uses It
All PRA-regulated UK banks, EBA-supervised institutions, increasingly Fed-supervised G-SIBs

### Mathematical Foundation

**Optimization Problem:**

Find minimum shock vector S* that causes firm to breach capital threshold:

```
S* = argmin ||S|| 
     subject to: Capital(S) ≤ K_min
                 S ∈ Plausibility_Set
```

Where:
- `||S||` = norm measuring shock severity (e.g., Mahalanobis distance)
- `K_min` = minimum regulatory capital (e.g., 4.5% CET1)
- `Plausibility_Set` = constraints ensuring economic coherence

**Mahalanobis Distance (for severity measurement):**

```
D_M(S) = √[(S - μ)' × Σ⁻¹ × (S - μ)]
```

Where:
- `μ` = expected values of risk factors
- `Σ` = covariance matrix of risk factors

**Simulated Annealing Algorithm:**

For complex, non-convex optimization:

```
1. Initialize: S₀ = random starting point, T₀ = initial temperature
2. For iteration k = 1, 2, ...
   a. Generate neighbor: S_new = S_k + random perturbation
   b. Compute ΔE = f(S_new) - f(S_k)
   c. If ΔE < 0: accept S_{k+1} = S_new
      Else: accept with probability exp(-ΔE / T_k)
   d. Cool: T_{k+1} = α × T_k (where α ≈ 0.95)
3. Stop when Capital(S_k) ≤ K_min
```

### Worked Example - Identifying Breaking Point

**Objective:** Find minimum stress that depletes CET1 below 4.5%

**Bank Profile:**
- Starting CET1: 12.5%
- RWA: $500B
- CET1 Capital: $62.5B
- Minimum CET1 Capital: $22.5B (4.5%)
- Buffer to breach: $40B

**Step 1: Define Risk Factors**

```
S = [Unemployment_shock, HPI_shock, Spread_shock, Equity_shock]
```

**Step 2: Map Shocks to Losses**

Loss function (simplified):
```
Credit_Loss = β₁ × Unemp_shock + β₂ × HPI_shock
Market_Loss = β₃ × Spread_shock + β₄ × Equity_shock

Where (estimated from historical data):
β₁ = $8B per 1% unemployment increase
β₂ = $6B per 10% HPI decline
β₃ = $4B per 100bp spread widening
β₄ = $3B per 10% equity decline
```

**Step 3: Run Optimization**

```
Minimize: √(Unemp² + (HPI/10)² + (Spread/100)² + (Equity/10)²)

Subject to: 8×Unemp + 0.6×HPI + 0.04×Spread + 0.3×Equity ≥ 40
           (Total losses ≥ $40B)
```

**Solution (via Simulated Annealing):**
```
Breaking Point Scenario:
- Unemployment: +3.2%
- HPI: -18%
- Spreads: +250bp
- Equity: -35%

Total Losses: $40.4B
Severity (Mahalanobis): 3.8 (approximately 1-in-100 event)
```

**Step 4: Validate Economic Coherence**

Check against VAR: Given Unemp +3.2%, model predicts HPI -20% to -25%
→ Scenario of HPI -18% is slightly optimistic but plausible

### Intuitive Rationale

As Nassim Taleb observed: "It is far easier to figure out if something is fragile than to predict the occurrence of an event that may harm it."

**Key Insight:** Reverse stress testing identifies **specific vulnerabilities** regardless of whether a corresponding scenario appears in historical data. The 2023 SVB failure revealed that interest rate + deposit run scenarios weren't adequately captured in traditional forward stress tests.

### Lifecycle Placement

| Phase | Reverse ST Role |
|-------|-----------------|
| Risk Identification | Discover unknown vulnerabilities |
| Scenario Design | Inform forward scenario selection |
| Recovery Planning | Define triggers for contingency actions |
| Board Communication | Explain "what could cause us to fail" |

### Challenge Questions & Defense

**Q1: "The optimization might find implausible scenarios."**

**Defense:**
1. Plausibility constraints from VAR/DSGE ensure coherence
2. Multiple solutions explored—report range of breaking points
3. Economic narrative required for each breaking point
4. Subject matter expert review of scenario plausibility

**Q2: "The loss function is too simplified."**

**Defense:**
1. Full satellite models used for loss calculation
2. Non-linear effects captured via iterative optimization
3. Second-round effects (RWA migration) included
4. Results validated against full Monte Carlo

**Q3: "There are infinitely many breaking points."**

**Defense:**
1. Focus on MINIMUM severity (most likely path to failure)
2. Report distribution of breaking points across dimensions
3. Identify common themes across solutions
4. Prioritize scenarios aligned with current risk environment

---

## 3.8 Machine Learning Approaches

### Industry Status
**Emerging** - Used for challenger models and exploratory analysis

### Who Uses It
Goldman Sachs, JPMorgan (internal research), Two Sigma, select central banks (Bank of Canada, Norges Bank)

### Key Approaches

**1. Variational Autoencoders (VAEs) for Scenario Generation:**

```
Encoder:  q(z|x) = N(μ(x), σ(x))  (maps data to latent space)
Decoder:  p(x|z) = N(f(z), I)     (generates data from latent)

Loss:  L = E[log p(x|z)] - KL(q(z|x) || p(z))
         = Reconstruction + Regularization
```

**Application:** Generate synthetic crisis scenarios by sampling from learned latent distribution, then decoding to macro variables

**2. LSTM for Time Series Stress:**

```
h_t = LSTM(h_{t-1}, x_t)
ŷ_{t+1} = W × h_t + b

Where LSTM cell:
f_t = σ(W_f × [h_{t-1}, x_t] + b_f)    (forget gate)
i_t = σ(W_i × [h_{t-1}, x_t] + b_i)    (input gate)
c_t = f_t × c_{t-1} + i_t × tanh(W_c × [h_{t-1}, x_t] + b_c)
o_t = σ(W_o × [h_{t-1}, x_t] + b_o)    (output gate)
h_t = o_t × tanh(c_t)
```

**Application:** Capture long-range dependencies in credit migration patterns

**3. Random Forests for PD Estimation:**

```
PD = (1/B) × Σ_{b=1}^{B} Tree_b(X)

Where each tree:
- Bootstrap sample of observations
- Random subset of features at each split
- Grown to maximum depth
```

**Application:** Non-linear PD models that capture interactions missed by logistic regression

### Worked Example - VAE Scenario Generation

**Objective:** Generate synthetic stress scenarios that preserve historical statistical properties

**Step 1: Train VAE on Historical Macro Data**

Input: 160 quarters (1984-2024) of [GDP, Unemp, HPI, Spread, Equity, Rates]
Architecture: 6 → 32 → 8 → 2 (latent) → 8 → 32 → 6

**Step 2: Sample Stress Scenarios from Latent Space**

```
z_stress = μ_latent - 2.5 × σ_latent  (tail of latent distribution)
x_stress = Decoder(z_stress)
```

**Step 3: Generate 1,000 Stress Paths**

Sample from p(x|z_stress) to get distribution of stressed macro paths

**Step 4: Validate Generated Scenarios**

```
Check         | Historical Crisis | VAE Generated | Pass?
--------------|-------------------|---------------|-------
GDP decline   | -4.0% to -8.0%    | -4.5% to -7.2%| ✓
Unemp increase| +4% to +6%        | +3.8% to +5.5%| ✓
Correlation   | Unemp-GDP: -0.85  | -0.82         | ✓
Tail behavior | ξ = 0.25          | 0.23          | ✓
```

### Challenge Questions & Defense

**Q1: "ML models are black boxes. How do you explain to regulators?"**

**Defense:**
1. SHAP values for feature importance
2. Partial dependence plots for relationships
3. ML used for scenario generation, not capital calculation
4. Traditional models remain primary—ML is challenger

**Q2: "Neural networks can overfit small financial datasets."**

**Defense:**
1. Cross-validation with rolling windows
2. Early stopping and dropout regularization
3. Bayesian neural networks for uncertainty
4. Ensemble across architectures

**Q3: "How do you ensure generated scenarios are plausible?"**

**Defense:**
1. Constrained VAE with economic priors
2. Discriminator network (GAN-style) trained on real data
3. Post-generation filtering via VAR plausibility checks
4. Human review of generated scenarios

---

# 4. Scenario Design - Worked Examples

## 4.1 Severely Adverse Scenario (Fed-Style)

### Step 1: Establish Narrative

**Narrative:** Global recession triggered by trade war escalation and emerging market debt crisis. Risk-off sentiment drives flight to quality, crushing EM assets and commodities while US Treasuries rally.

### Step 2: Set Anchor Variables

Per Fed Scenario Design Framework:
```
Unemployment Peak:     10.0% (from 4.0% baseline)
Real GDP Trough:       -6.5% cumulative
10Y Treasury Low:      0.5%
S&P 500 Decline:       -55%
HPI Decline:           -30%
CRE Decline:           -40%
BBB Spread Peak:       +550bp
```

### Step 3: Calibrate Using BVAR

Run scenario through BVAR to ensure consistency:

```
Variable        | Q1    | Q2    | Q3    | Q4    | Q5    | Q6    | Q7    | Q8    | Q9
----------------|-------|-------|-------|-------|-------|-------|-------|-------|-------
Unemployment    | 5.2%  | 6.8%  | 8.2%  | 9.3%  | 9.8%  | 10.0% | 9.8%  | 9.4%  | 9.0%
Real GDP (Q/Q)  | -3.5% | -5.0% | -3.0% | -1.0% | +0.5% | +1.5% | +2.0% | +2.5% | +3.0%
10Y Treasury    | 2.8%  | 2.0%  | 1.2%  | 0.8%  | 0.5%  | 0.5%  | 0.6%  | 0.8%  | 1.0%
BBB Spread      | +150  | +350  | +500  | +550  | +500  | +420  | +350  | +280  | +220
S&P 500 (cum)   | -20%  | -40%  | -52%  | -55%  | -50%  | -45%  | -38%  | -30%  | -22%
HPI (cum)       | -5%   | -12%  | -18%  | -24%  | -28%  | -30%  | -29%  | -27%  | -25%
```

### Step 4: Assess Severity

Compare to historical distribution from Monte Carlo:
```
GDP path:         3rd percentile
Unemployment:     2nd percentile  
Equity decline:   1st percentile
Credit spreads:   4th percentile

Joint probability: ~1.5% (1-in-67 year event)
```

### Step 5: Document Rationale

**Why this severity?**
- Unemployment to 10%: Mandated by Fed scenario framework
- GDP decline 6.5%: Consistent with historical Okun's Law relationship (Δu = -0.5 × Δy)
- Equity -55%: Comparable to 2008-09 (-57%) and 2000-02 (-49%)
- Spreads +550bp: Exceeds 2008 peak (+540bp) given EM focus

---

## 4.2 Interest Rate Shock Scenario (2023-Style)

### Step 1: Establish Narrative

**Narrative:** Persistent inflation forces aggressive Fed tightening. Long-end rates rise faster than expected, causing HTM/AFS losses. Combined with deposit competition from high-rate alternatives, banks face funding pressure.

### Step 2: Set Anchor Variables

```
Fed Funds Terminal:    6.5%
10Y Treasury Peak:     5.5%
3M-10Y Curve:          -150bp (inverted)
Deposit Beta:          0.75 (elevated)
Uninsured Deposit Run: -15% (for vulnerable profiles)
```

### Step 3: Model Mechanics

**AFS/HTM Portfolio Impact:**

Using duration approximation:
```
ΔP/P ≈ -D × Δy + (1/2) × C × (Δy)²

For portfolio with D = 6, C = 50, Δy = +200bp:
ΔP/P = -6 × 0.02 + 0.5 × 50 × 0.0004
     = -0.12 + 0.01
     = -11%
```

**NII Impact:**

```
ΔNII = Assets × Asset_Beta × Δr - Deposits × Deposit_Beta × Δr

For $500B assets (beta 0.4), $400B deposits (beta 0.75), Δr = +200bp:
ΔNII = 500 × 0.4 × 0.02 - 400 × 0.75 × 0.02
     = $4B - $6B
     = -$2B annualized
```

### Step 4: Differentiate by Business Model

| Bank Type | AFS/HTM Loss | NII Impact | Deposit Run | Net Impact |
|-----------|--------------|------------|-------------|------------|
| Money Center | -3% capital | +$2B | -5% | Manageable |
| Regional | -8% capital | -$1B | -15% | Severe |
| Community | -5% capital | -$0.5B | -20% | Critical |

---

## 4.3 Operational Risk Scenario (Cyber Attack)

### Step 1: Establish Narrative

**Narrative:** State-sponsored cyber attack compromises core banking systems. 72-hour service disruption, customer data breach affecting 10M accounts, regulatory fines and litigation.

### Step 2: Quantify Components

```
Direct Costs:
- Remediation/forensics:      $500M
- Customer notification:       $50M
- Credit monitoring:          $200M
- System rebuild:             $800M
Subtotal Direct:              $1,550M

Indirect Costs:
- Business interruption:      $300M (72hr × $4M/hr revenue)
- Customer attrition:         $400M (2% × $20B deposits × 100bp margin × 5yr)
- Reputational damage:        $250M (reduced new customer acquisition)
Subtotal Indirect:            $950M

Regulatory/Legal:
- Regulatory fines:           $750M (GDPR, OCC, state AGs)
- Litigation settlement:      $1,200M (class action)
- Legal fees:                 $150M
Subtotal Regulatory:          $2,100M

TOTAL:                        $4,600M
```

### Step 3: Scenario Variants

| Severity | Description | Loss Estimate | Probability |
|----------|-------------|---------------|-------------|
| Moderate | Contained breach, quick recovery | $1.5B | 5% annual |
| Severe | Extended outage, data exfiltration | $4.6B | 1% annual |
| Extreme | Critical infrastructure failure | $12B | 0.1% annual |

---

# 5. Complete Stress Scenario Development Lifecycle

## Phase 1: Strategic Planning & Governance (Weeks 1-4)

### 1.1 Objective Definition

| Question | Response Required |
|----------|-------------------|
| Purpose | Regulatory (CCAR/EBA) vs. Internal Capital Planning vs. ICAAP |
| Scope | Enterprise-wide vs. Portfolio-specific |
| Horizon | 9 quarters (CCAR) vs. 3 years (EBA) vs. Custom |
| Metrics | CET1, Tier 1 Leverage, LCR, NSFR, PPNR |

### 1.2 Governance Structure

```
Board Risk Committee
        ↓
    CRO (Sponsor)
        ↓
Steering Committee (CRO, CFO, Treasurer, Business Heads)
        ↓
    ┌────────────┬────────────┬────────────┐
    ↓            ↓            ↓            ↓
Scenario    Model        Data         Reporting
Design      Development  Management   Working Group
```

### 1.3 Key Deliverables

- [ ] Approved project charter
- [ ] Resource allocation and timeline
- [ ] RACI matrix for all workstreams
- [ ] Escalation protocols

---

## Phase 2: Risk Identification & Assessment (Weeks 3-8)

### 2.1 Risk Inventory

| Risk Type | Sub-Categories | Key Drivers |
|-----------|----------------|-------------|
| Credit | C&I, CRE, Consumer, Cards | PD, LGD, EAD by segment |
| Market | Rates, Equity, FX, Commodity | Position sensitivities |
| Operational | Cyber, Legal, Conduct | Scenario-based |
| Liquidity | Funding, Market, Contingent | LCR, NSFR, survival days |
| Interest Rate | Repricing, Basis, Optionality | NII at risk, EVE |
| Strategic | Business model, Competitive | Revenue growth |

### 2.2 Concentration Analysis

```
Top 10 Exposures:     $X B (Y% of capital)
Top Industry:         [Industry] at $X B
Top Geography:        [Region] at $X B
Single Name Limit:    Breaches identified: [count]
```

### 2.3 Historical Crisis Analysis

| Crisis | Peak Unemployment | GDP Decline | Credit Losses | Recovery Time |
|--------|-------------------|-------------|---------------|---------------|
| 2008 GFC | 10.0% | -4.3% | 8.5% | 4 years |
| 2020 COVID | 14.7% | -9.0% | 2.8% | 2 years |
| 2001 Dot-com | 6.3% | -0.3% | 2.1% | 3 years |
| 1990 S&L | 7.8% | -1.4% | 3.2% | 3 years |

---

## Phase 3: Scenario Design (Weeks 6-12)

### 3.1 Scenario Types Required

| Scenario | Description | Source |
|----------|-------------|--------|
| Supervisory Severely Adverse | Severe global recession | Fed-prescribed |
| Supervisory Baseline | Consensus forecast | Fed-prescribed |
| BHC Severely Adverse | Firm-specific vulnerabilities | Internal |
| BHC Baseline | Management forecast | Internal |
| Exploratory | Emerging risks | Internal/Regulatory |

### 3.2 Narrative Template

```
SCENARIO: [Name]
TRIGGER: [Initial shock event]
TRANSMISSION: [How shock propagates through economy]
AMPLIFICATION: [Feedback mechanisms and second-round effects]
POLICY RESPONSE: [Monetary, fiscal, regulatory actions]
RECOVERY: [Path back to baseline]
```

### 3.3 Variable Specification Checklist

- [ ] 28 domestic macro variables (Fed requirement)
- [ ] 16 international variables (4 countries × 4 variables)
- [ ] Market factors (equity indices, spreads, rates)
- [ ] All paths internally consistent (VAR/DSGE verified)

---

## Phase 4: Model Development & Implementation (Weeks 8-20)

### 4.1 Satellite Model Inventory

| Risk Type | Model Type | Inputs | Outputs |
|-----------|------------|--------|---------|
| Wholesale Credit | Migration matrix | Macro, industry, ratings | PD by grade |
| Retail Credit | Logistic regression | Unemployment, HPI | Segment PD |
| LGD | Beta regression | Collateral values, cycle | Loss severity |
| PPNR - NII | Gap analysis + prepay | Rates, curve, volumes | NII projection |
| PPNR - Fee | Elasticity models | GDP, equity markets | Non-II projection |
| Market Risk | Full reval | GMS shocks | Trading P&L |
| Operational | Scenario-based | Macro indicators | Op risk loss |

### 4.2 Model Integration Points

```
                        ┌─────────────────┐
                        │ Macro Scenario  │
                        └────────┬────────┘
                                 │
        ┌────────────────────────┼────────────────────────┐
        ↓                        ↓                        ↓
┌───────────────┐      ┌─────────────────┐      ┌─────────────────┐
│ Credit Models │      │ Market Models   │      │ PPNR Models     │
│ (PD, LGD)     │      │ (Reval, CVA)    │      │ (NII, Fees)     │
└───────┬───────┘      └────────┬────────┘      └────────┬────────┘
        │                       │                        │
        └───────────────────────┼────────────────────────┘
                                ↓
                    ┌───────────────────────┐
                    │ Balance Sheet Engine  │
                    │ (RWA, Capital)        │
                    └───────────┬───────────┘
                                ↓
                    ┌───────────────────────┐
                    │ Capital Ratio Output  │
                    └───────────────────────┘
```

### 4.3 Key Modeling Decisions

| Decision | Options | Chosen | Rationale |
|----------|---------|--------|-----------|
| PD calibration | PIT vs TTC | PIT | Scenario-conditional required |
| LGD cycle | Downturn vs Current | Downturn | Conservative for stress |
| Prepayment | Static vs Dynamic | Dynamic | Rate-sensitive |
| Balance sheet | Static vs Dynamic | Per regulatory | Fed = dynamic |

---

## Phase 5: Execution & Computation (Weeks 18-26)

### 5.1 Data Requirements

| Data Type | Source System | Frequency | Quality Checks |
|-----------|---------------|-----------|----------------|
| Loan tape | LOS/Core | As-of date | Reconcile to GL |
| Trading positions | Risk systems | As-of date | Reconcile to P&L |
| Deposits | Core banking | As-of date | Segment verification |
| Off-balance sheet | Commitment systems | As-of date | Line utilization |

### 5.2 Execution Sequence

```
Week 18-19: Data extraction and quality assurance
Week 20-21: Credit loss model runs
Week 22-23: PPNR and trading model runs
Week 24:    Balance sheet projection
Week 25:    Capital ratio calculation
Week 26:    Results validation and reconciliation
```

### 5.3 Quality Control Checkpoints

- [ ] Data completeness: <1% missing critical fields
- [ ] GL reconciliation: Within $X tolerance
- [ ] Model execution logs: No errors
- [ ] Output reasonability: Within historical bounds

---

## Phase 6: Validation & Challenge (Weeks 22-30)

### 6.1 Model Risk Management

| Validation Element | Description | Documentation |
|--------------------|-------------|---------------|
| Conceptual Soundness | Theory, assumptions | Model documentation |
| Developmental Evidence | Estimation, testing | Technical report |
| Outcomes Analysis | Backtesting, benchmarking | Validation memo |
| Ongoing Monitoring | Performance tracking | Dashboard |

### 6.2 Effective Challenge

| Level | Participants | Focus |
|-------|--------------|-------|
| Working | Model developers, validators | Technical accuracy |
| Management | Business heads, risk officers | Business reasonability |
| Executive | CRO, CFO, ALCO | Strategic implications |
| Board | Risk committee | Governance, risk appetite |

### 6.3 Challenger Model Requirements

For each primary model, maintain challenger:
```
Primary: Logistic regression PD
Challenger: Machine learning (XGBoost)
Comparison: Results within ±15%, investigate if exceeded
```

---

## Phase 7: Reporting & Action (Weeks 28-34)

### 7.1 Internal Reporting Package

| Report | Audience | Content |
|--------|----------|---------|
| Executive Summary | Board, C-suite | Key metrics, narrative |
| Detailed Results | Risk Committee | By portfolio, quarter |
| Loss Attribution | Business Heads | Drivers, sensitivities |
| Action Items | Management | Remediation, limits |

### 7.2 Regulatory Submissions

| Submission | Deadline | Content |
|------------|----------|---------|
| FR Y-14A | April 5 | Summary, projections |
| FR Y-14Q | 45 days post-quarter | Detailed schedules |
| FR Y-14M | 30 days post-month | Trading positions |
| Company-run results | June 30 | Public disclosure |

### 7.3 Management Actions

Based on stress test results:

| Finding | Action | Owner | Deadline |
|---------|--------|-------|----------|
| CRE concentration | Reduce exposure $XB | Commercial Head | Q2 |
| Duration mismatch | Extend funding | Treasurer | Q3 |
| Model gap | Develop new model | CRO | Q4 |

---

# 6. Challenge & Defense Framework

## 6.1 Scenario Design Challenges

### Challenge: "The scenario is too severe/not severe enough"

**Defense Framework:**
```
1. Quantitative Evidence:
   - Percentile rank from BVAR simulation: [X]th percentile
   - Historical comparison: [Event] had similar/greater severity
   - Fed scenario guidance compliance: ✓ (unemployment to 10%)

2. Qualitative Evidence:
   - Expert panel judgment: [Economist names, dates]
   - Regulatory precedent: Fed's 2024 scenario used [Y]% GDP decline
   - Peer comparison: [Bank X] used similar assumptions

3. Sensitivity Analysis:
   - Results under +/- 20% severity: [Range]
   - Key driver: [Variable] has greatest impact
```

### Challenge: "Variables are not internally consistent"

**Defense Framework:**
```
1. Model-Based Validation:
   - BVAR residuals within 2 standard deviations: ✓
   - DSGE steady-state deviation: <X%
   - No arbitrage violations: ✓

2. Historical Precedent:
   - Similar combination observed in [Crisis]: [Statistics]
   - Correlation during stress periods: [Comparison]

3. Economic Narrative:
   - Causal mechanism: [Explanation]
   - Policy response assumed: [Details]
```

---

## 6.2 Model Challenges

### Challenge: "Model has poor out-of-sample performance"

**Defense Framework:**
```
1. Performance Metrics:
   - In-sample R²: [X]%
   - Out-of-sample RMSE: [Y]
   - Bias: [Z] (direction and magnitude)

2. Contextualization:
   - Comparison to benchmark: [Outperforms/underperforms by X%]
   - Industry standard: [Peer performance]
   - COVID impact: [Pre/post comparison]

3. Model Uncertainty:
   - Confidence intervals on key outputs: [Range]
   - Parameter stability: [Analysis]
   - Challenger model comparison: [Results within X%]
```

### Challenge: "Model assumptions are too conservative/aggressive"

**Defense Framework:**
```
1. Assumption Inventory:
   | Assumption | Value Used | Historical Range | Rationale |
   |------------|------------|------------------|-----------|
   | PD uplift  | 2.5x       | 2.0x - 3.5x      | Median historical |
   | LGD stress | +15%       | +10% - +25%      | Segment specific |

2. Sensitivity Analysis:
   - Capital impact of +/- 1 SD on key assumptions: [Table]
   - Rank ordering of assumption importance: [List]

3. Regulatory Guidance:
   - Fed SR 11-7 compliance: ✓
   - EBA guidelines adherence: ✓
```

---

## 6.3 Results Challenges

### Challenge: "Results differ significantly from prior year"

**Defense Framework:**
```
1. Variance Decomposition:
   | Driver | Impact on CET1 | Explanation |
   |--------|----------------|-------------|
   | Scenario severity | -50bp | More severe unemployment path |
   | Portfolio changes | +30bp | Reduced CRE concentration |
   | Model updates | -20bp | New PD model |
   | Methodology | -10bp | Changed prepayment approach |
   | Net change | -50bp | |

2. Reasonability Checks:
   - Loss rates vs historical crisis: [Comparison]
   - Peer comparison (disclosed): [Analysis]
   - Internal consistency: [Verification]

3. Supporting Analysis:
   - Attribution by portfolio: [Breakdown]
   - Quarter-by-quarter evolution: [Path analysis]
```

---

# 7. Systematic Implementation Framework

## 7.1 Capability Maturity Model

| Dimension | Level 1: Initial | Level 2: Developing | Level 3: Defined | Level 4: Advanced | Level 5: Leading |
|-----------|------------------|---------------------|------------------|-------------------|------------------|
| Governance | Ad hoc | Annual process | Formal framework | Integrated planning | Continuous |
| Scenario Design | Regulatory only | Internal scenarios | Model-based | Reverse ST | Real-time |
| Models | Spreadsheets | Basic regression | Validated models | Challenger framework | ML/AI |
| Data | Manual | Semi-automated | Automated, reconciled | Real-time feeds | Predictive |
| Technology | Standalone | Integrated platform | Enterprise solution | Cloud-based | AI-enabled |
| Reporting | Static reports | Interactive | Self-service | Automated narrative | Predictive |

## 7.2 Implementation Roadmap

### Year 1: Foundation

**Q1-Q2:**
- Establish governance structure
- Document current state assessment
- Identify capability gaps

**Q3-Q4:**
- Implement core scenario design process
- Develop/validate primary satellite models
- Build integrated data feeds

### Year 2: Enhancement

**Q1-Q2:**
- Deploy challenger model framework
- Implement reverse stress testing
- Automate reporting

**Q3-Q4:**
- Integrate ML capabilities
- Real-time scenario updating
- Advanced analytics dashboard

### Year 3: Optimization

**Q1-Q2:**
- Full enterprise risk integration
- Climate scenario capabilities
- AI-assisted narrative generation

**Q3-Q4:**
- Continuous stress testing
- Predictive early warning
- Industry benchmarking

## 7.3 Technology Stack Recommendations

| Layer | Tool/Technology | Purpose |
|-------|----------------|---------|
| Data | Snowflake / Databricks | Scalable data lake |
| Compute | AWS/Azure HPC | Monte Carlo simulation |
| Modeling | Python (scikit, PyTorch) | ML and statistical models |
| Orchestration | Airflow / Prefect | Workflow automation |
| Visualization | Tableau / Power BI | Interactive reporting |
| Documentation | Confluence | Model documentation |
| Version Control | Git | Code and model versioning |

---

# 8. Model Selection Decision Tree

```
START: What is your primary objective?
│
├─► Capital Adequacy Assessment
│   │
│   ├─► Enterprise-wide?
│   │   │
│   │   └─► YES → Monte Carlo Simulation
│   │       (Full distribution, all risk types)
│   │
│   └─► Portfolio-specific?
│       │
│       └─► Credit Portfolio → Satellite Models (PD/LGD/EAD)
│           Market Portfolio → GARCH + EVT + Copulas
│
├─► Scenario Design
│   │
│   ├─► Need internal consistency?
│   │   │
│   │   └─► YES → VAR/BVAR
│   │       (Macro variable coherence)
│   │
│   └─► Need economic structure?
│       │
│       └─► YES → DSGE
│           (Policy analysis, counterfactuals)
│
├─► Tail Risk Quantification
│   │
│   ├─► Single asset/factor?
│   │   │
│   │   └─► YES → EVT (GPD)
│   │
│   └─► Multiple assets with dependence?
│       │
│       └─► YES → Copulas + EVT
│           (Vine copulas for high dimensions)
│
├─► Volatility Forecasting
│   │
│   └─► GARCH Family
│       (GJR for asymmetry, DCC for multivariate)
│
├─► Vulnerability Discovery
│   │
│   └─► Reverse Stress Testing
│       (Simulated annealing, optimization)
│
└─► Exploratory / Challenger
    │
    └─► Machine Learning
        (VAE for scenarios, LSTM for dynamics, RF for PD)
```

---

# 9. References

## Regulatory Sources

1. Federal Reserve Board (2025). "Supervisory Stress Test Methodology"
2. Federal Reserve Board (2020). "Policy Statement on the Scenario Design Framework for Stress Testing" (12 CFR 252, Appendix A)
3. European Banking Authority (2018). "Guidelines on Stress Testing" (EBA/GL/2018/04)
4. Basel Committee on Banking Supervision (2018). "Supervisory and Bank Stress Testing: Range of Practices"
5. Bank of England PRA (2023). "Supervisory Statement SS31/15: Internal Capital Adequacy Assessment Process"

## Academic Sources

### Monte Carlo & Simulation
- Glasserman, P. (2003). *Monte Carlo Methods in Financial Engineering*. Springer.
- McNeil, A.J., Frey, R., & Embrechts, P. (2015). *Quantitative Risk Management*. Princeton.

### VAR/BVAR
- Sims, C.A. (1980). "Macroeconomics and Reality." *Econometrica*, 48(1), 1-48.
- Litterman, R.B. (1986). "Forecasting with Bayesian Vector Autoregressions." *Journal of Business & Economic Statistics*.

### GARCH
- Bollerslev, T. (1986). "Generalized Autoregressive Conditional Heteroskedasticity." *Journal of Econometrics*, 31(3), 307-327.
- Engle, R. (2002). "Dynamic Conditional Correlation." *Journal of Business & Economic Statistics*, 20(3), 339-350.

### Copulas
- Sklar, A. (1959). "Fonctions de répartition à n dimensions et leurs marges." *Publications de l'Institut Statistique de l'Université de Paris*, 8, 229-231.
- Joe, H. (2014). *Dependence Modeling with Copulas*. CRC Press.
- Koliai, L. (2016). "Extreme Risk Modeling: An EVT-Pair-Copulas Approach." *Journal of Banking & Finance*, 70, 1-22.

### EVT
- Embrechts, P., Klüppelberg, C., & Mikosch, T. (1997). *Modelling Extremal Events*. Springer.
- McNeil, A.J. & Frey, R. (2000). "Estimation of Tail-Related Risk Measures." *Journal of Empirical Finance*, 7(3), 271-300.

### DSGE
- Smets, F. & Wouters, R. (2007). "Shocks and Frictions in US Business Cycles: A Bayesian DSGE Approach." *American Economic Review*, 97(3), 586-606.
- Christiano, L.J., Eichenbaum, M., & Trabandt, M. (2018). "On DSGE Models." *Journal of Economic Perspectives*, 32(3), 113-140.

### Reverse Stress Testing
- Breuer, T. & Csiszár, I. (2013). "Systematic Stress Tests with Entropic Plausibility Constraints." *Journal of Banking & Finance*, 37(5), 1552-1559.
- Glasserman, P., Kang, C., & Kang, W. (2015). "Stress Scenario Selection by Empirical Likelihood." *Quantitative Finance*, 15(1), 25-41.

### Machine Learning in Finance
- Gu, S., Kelly, B., & Xiu, D. (2020). "Empirical Asset Pricing via Machine Learning." *Review of Financial Studies*, 33(5), 2223-2273.
- Dixon, M., Halperin, I., & Bilokon, P. (2020). *Machine Learning in Finance*. Springer.

## Industry Publications

- Farmer, J.D., Kleinnijenhuis, A.M., Schuermann, T., & Wetzer, T. (Eds.). (2022). *Handbook of Financial Stress Testing*. Cambridge University Press.
- Bank Policy Institute (2024). "Deep Dive: DFAST 2024 Stress Test Scenarios"
- Moody's Analytics (2023). "Process Workflow for Stress Testing"

---

*Document prepared for Market Risk professionals seeking comprehensive understanding of stress testing methodologies. For questions or updates, consult latest regulatory guidance.*
