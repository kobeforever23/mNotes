# CIB Trading Strategies: Complete Technical Specification

**The definitive practitioner's guide to trading strategies across a global investment bank—covering the exact math, signal construction, Greeks management, P&L drivers, and realistic performance expectations that differentiate successful desks from textbook theory.**

Every major trading desk operates on a foundation of quantifiable edge sources, precise risk management, and disciplined execution. This specification provides the full technical architecture: formulas that matter, trade constructions that work, and honest assessments of what generates actual P&L versus what merely backtests well. The content assumes familiarity with derivatives pricing and market microstructure—the focus is implementation detail and practitioner insight.

---

## Part 1: Rates trading strategies

### Curve trading: Steepeners and flatteners

**DV01-weighted construction** forms the foundation of all curve trades. For a 2s10s steepener (short 2Y, long 10Y), the hedge ratio is:

```
Notional_2Y / Notional_10Y = DV01_10Y / DV01_2Y
```

With current DV01s of approximately **$37/bp** for 2Y and **$79/bp** for 10Y, this yields a ratio of **2.13:1**. A $100M DV01-neutral position requires ~$213M in 2Y versus $100M in 10Y.

**Implementation varies significantly across instruments:**

| Instrument | Advantages | Considerations |
|------------|-----------|----------------|
| Cash bonds | Direct exposure, repo income | Financing costs, settlement, specials risk |
| Futures | Standardized, liquid | CTD optionality, basis risk, roll costs |
| Swaps | Precise tenor targeting, no financing | Collateral requirements (IM/VM), basis spread |

**Carry and roll-down decomposition:**

```
Carry_swap(3Y) = 3m forward 2Y9M rate − spot 3Y rate
Carry_bond = (Coupon − Repo rate) × Days/360
Roll-down = Duration × (Current yield − Yield at shorter maturity)
```

Numerical example: A 5Y bond at 4.00% yield, 3% repo, 4.5 duration with 4Y yield at 3.80%:
- Carry (6mo): (4.00% − 3.00%) × 0.5 = **50bp**
- Roll-down (6mo): 4.5 × (4.00% − 3.80%) = **90bp**
- Total carry and roll: **140bp annualized**

**P&L attribution follows a Taylor expansion:**

```
ΔP&L = -Duration × Δy_parallel + Σ KRD_i × Δy_slope + ½ × Convexity × (Δy)² + Carry + Roll
```

**Steepening signals** include early Fed easing cycles (front-end rallies faster), recession expectations, flight-to-quality flows, and fiscal deficit expansion. **Flattening signals** emerge in late hiking cycles, inflation repricing, and liability-driven pension demand at the long end.

### Butterflies: Three construction methods

**Method 1: Duration-neutral 1:2:1**
```
Notional_wing1 × DV01_wing1 = Notional_body × DV01_body × 0.5
Notional_wing2 × DV01_wing2 = Notional_body × DV01_body × 0.5
```

**Method 2: Regression-weighted**
Solve for weights where β equals the regression coefficient between (Y_body − Y_wing1) and (Y_wing2 − Y_body). Typical 2s5s10s β ranges **0.25–0.36**.

**Method 3: PCA-weighted** (institutional standard)
Use PC3 loadings (curvature factor) as weights. Example loadings: [3Y: 0.63, 5Y: -0.70, 10Y: 0.32]. This produces trades uncorrelated with level (PC1) and slope (PC2).

**Butterfly value** = Y_wing1 + Y_wing2 − 2 × Y_body (expresses pure curvature view)

**Breakeven** = Net Carry&Roll / Duration of body position

Long butterfly positions exhibit positive convexity; short butterflies exhibit negative convexity.

### Swap spreads and box trades

**Swap spread** = IRS Fixed Rate − Treasury Yield (same maturity)

**Key drivers:** Bank funding costs (LIBOR-OIS), balance sheet constraints (SLR, RWA), Treasury supply/demand (QT effects), repo market dynamics, and mortgage hedging flows.

**Full P&L with financing for a long swap spread position (pay fixed IRS + long Treasury):**

```
P&L = (Swap Rate Δ × Swap DV01) − (Treasury Yield Δ × Bond DV01) 
      − Repo Financing Cost − Initial Margin Cost − Balance Sheet Charges (SLR ~5-6%)
```

**Critical insight:** Negative swap spreads persist due to regulatory constraints—this is not free arbitrage. Post-Basel III ROE on swap spread trades has collapsed; per NY Fed research, SLR charges on Treasury holdings dramatically reduce attractiveness.

### Rates volatility: Swaptions and gamma

**Swaption breakeven calculation:**
```
Breakeven Move = Premium / (Duration × Notional) = Premium / DV01
```

**SABR model parameters** (α, β, ρ, ν):
- α: ATM vol level
- β: Backbone parameter (typically 0.5 for rates)
- ρ: Correlation controlling skew
- ν: Vol-of-vol controlling smile curvature

**Hagan approximation:**
```
σ_impl ≈ α × [log(F/K)/D(ζ)] × {1 + [adjustment terms] × T}
```

**Gamma scalping P&L:**
```
Delta-hedged P&L = ½ × Γ × S² × (σ²_realized − σ²_implied) × Δt
Breakeven daily move = √(2 × |Θ| / Γ)
```

**Vega/gamma tradeoff:** Short-dated options have high gamma, low vega; long-dated options exhibit the inverse. Calendar spreads express this relative value.

**Convexity adjustments (critical for CMS and in-arrears):**
```
Futures vs Forward: Adjustment ≈ ½ × σ² × T₁ × (T₂ − T₁)
CMS Replication: CMS Rate = Forward Swap Rate + ∫ Swaption_smile dK
```

### Repo and funding trades

**Specials P&L:**
```
P&L = (GC Rate − Special Rate) × Notional × Days/360
```
Example: GC at 5.00%, special at 4.50%, $100M for 7 days yields **$9,722**.

**Cross-currency basis** = FX Forward Implied Rate − SOFR. A negative basis (typical for USD vs EUR, JPY) means USD funding is cheaper direct than synthetic.

---

## Part 2: Credit trading strategies

### Cash-CDS basis trading

**Basis definition:** CDS Spread − Bond Z-spread (or ASW spread)

**Z-spread calculation:** Solve iteratively for Z in:
```
Price = Σ CF_t / (1 + r_t + Z)^t
```

**Basis drivers:**
- **Positive basis:** High funding costs, scarce repo, CTD optionality priced in
- **Negative basis:** Synthetic demand, liquidity premium on bonds, restructuring clause differences

**Negative basis trade construction (buy bond, buy CDS protection):**
```
P&L = (ASW − CDS spread) × Notional × Duration + Carry − Funding Cost − Transaction Costs
```

Numerical example:
- 5Y bond at price 95, Z-spread 180bp
- 5Y CDS at 150bp
- Basis = 150 − 180 = **−30bp negative**
- If basis converges: 30bp × $10M × 4.2 duration = **$126,000**

**Critical risks:** Funding squeeze (2008 showed basis widening to −200bp), CDS-bond divergence, restructuring event mismatch, and mark-to-market duration mismatch.

### Capital structure arbitrage: Merton model implementation

**Core equations:**
```
Equity = V × N(d₁) − D × e^(−rT) × N(d₂)
d₁ = [ln(V/D) + (r + σ²_V/2)T] / (σ_V × √T)
d₂ = d₁ − σ_V × √T
```

**Implementation process:**
1. Observe equity price S and equity vol σ_E
2. Calculate asset vol: σ_V = σ_E × (E/V) × (1/N(d₁))
3. Solve iteratively for V using equity equation
4. Calculate model-implied CDS spread
5. Compare to market: If model spread > market → credit cheap → sell CDS protection + short equity

**Delta hedge ratio:**
```
Hedge Ratio = (∂CDS/∂V) × (1/N(d₁))
```

**Empirical performance** (Yu 2005): 33 obligors studied, mean return **2.78%** at 180-day horizon for speculative grade—but only ~10% of trades converge. Individual trades are very risky; portfolio approach required.

### Index versus single-name arbitrage

**Intrinsic spread calculation:**
```
Intrinsic = Σ (w_i × CS01_i × S_i) / Σ (w_i × CS01_i)
Index Basis = Market Index Spread − Intrinsic Spread
```

**Skew trading:** When basis is negative (index tighter than intrinsic), buy index protection and sell single-name protection on constituents. Need basis of **4–5bp+** to cover transaction costs on 125-name portfolios.

### Tranche trading and correlation exposure

**Correlation exposure by tranche:**
- **Equity (0–3%):** Short correlation—benefits from dispersed defaults, high spread, positive carry
- **Senior (10%+):** Long correlation—benefits from clustered defaults (all or none)

**Gaussian copula conditional default probability:**
```
p(M) = N[(N⁻¹(PD) − √ρ × M) / √(1−ρ)]
```

**Base correlation** (industry standard since JPMorgan 2004): Define ρ_base(K) as correlation pricing equity tranche [0, K]. To price [K_A, K_U]: subtract [0, K_A] priced at ρ_base(K_A) from [0, K_U] at ρ_base(K_U).

**Delta-hedging tranches** removes spread risk, leaving pure correlation exposure:
```
Hedge Ratio = CS01_tranche / CS01_index
```

### Distressed and LME plays

**Fulcrum security identification:**
1. Estimate Enterprise Value via comps/DCF
2. Map EV to capital structure waterfall
3. Fulcrum = most senior class receiving partial recovery

Example waterfall with $500M EV:
- Senior Secured TL ($200M): **100% recovery**
- Senior Notes ($400M): ($500−$200)/$400 = **75% recovery** ← FULCRUM
- Subordinated Notes ($150M): **0% recovery**

**LME transaction types:**
- **Uptier/priming:** Majority lenders approve amendment, new super-senior debt issued
- **Drop-down:** Transfer assets to unrestricted subsidiary, subordinating existing creditors
- **Double-dip:** Structure allowing dual claims in bankruptcy via intercompany loans

---

## Part 3: Securitized products strategies

### Agency MBS prepayment modeling

**Core formulas:**
```
SMM = 1 − (1 − CPR)^(1/12)
CPR (100% PSA) = min(0.2% × min(Month, 30), 6%)
```

**S-curve prepayment model:**
```
Refi_CPR = 0.2406 − 0.1389 × arctan(5.952 × (1.089 − Coupon/Mortgage_rate))
```

**Combined CPR:** Refi_Incentive × Seasoning × Seasonality × Burnout

**Specified pool pay-ups:**

| Pool Type | Typical Pay-up | Rationale |
|-----------|---------------|-----------|
| Low Loan Balance (<$85k) | 40–60/32nds | High friction costs slow prepayment |
| High LTV (>80%) | 5–15/32nds | Difficult to refinance |
| NY/TX Geography | 8–25/32nds | State laws slow refinancing |

**Pay-up valuation:**
```
Pay-up = PV(TBA_Prepay − Specified_Prepay) × Principal × Discount_Factor
```

### Dollar roll mechanics

**Key calculations:**
```
Drop = Front_Month_Price − Back_Month_Price
Implied_Repo = [(Drop + Accrued_front − Accrued_back) × 360] / [Front_Price × Days]
```

**Decision rule:** If Implied_Repo < Funding_Cost → roll position (sell/buy). If Implied_Repo > Funding_Cost → take delivery and finance via repo.

Roll is "special" when implied financing rate approaches zero or negative—signals supply/demand imbalances.

### OAS calculation via Monte Carlo

**Step-by-step process:**
1. Calibrate interest rate model (Hull-White, BDT)
2. Generate 500–2000 interest rate paths
3. For each path: project prepayment rates, calculate cash flows
4. Discount using path-specific short rates + OAS
5. Solve for OAS equating average simulated price to market price

**Formula:**
```
Market_Price = (1/N) × Σᵢ Σₜ [CF(i,t) × exp(−∫₀ᵗ (r(i,s) + OAS) ds)]
```

**Z-spread versus OAS:** Z-spread = OAS + Option_Cost. For negative convexity MBS, option cost > 0.

### CLO trading

**Equity NAV calculation:**
```
NAV = Portfolio_MV − Liabilities_Par + Accrued_Interest − Fees
IO_Return = (Portfolio_Spread − Weighted_Avg_Debt_Cost − Mgmt_Fee) × Leverage
```

Example: Portfolio at SOFR+350bp, debt at SOFR+173bp blended, spread differential 177bp × 9x leverage = **~16% gross IO return** before defaults.

**Tranche attachment points:**
| Tranche | Attachment | Credit Enhancement |
|---------|-----------|-------------------|
| AAA | 36% | 36% |
| AA | 24% | 24% |
| BBB | 12.5% | 12.5% |
| Equity | 0% | First loss |

---

## Part 4: FX trading strategies

### Carry trade construction

**True carry calculation:**
```
Carry = (F − S) / S × (360/days) ≈ r_domestic − r_foreign
Vol-Adjusted Carry = Annualized_Carry / σ_expected
```

**Historical Sharpe ratios:**
- Simple nominal carry: **0.4–0.5**
- Real carry (inflation-adjusted): **0.48**
- Hedged real carry: **0.67**
- EM carry with hedging: **0.71–1.29**

**Key characteristics:** High seasonality, **~40% correlation** with S&P 500, negative skewness (crash risk). Standard practice: 10% annualized vol target with maximum 5× leverage.

### Momentum and trend signals

**Time-series momentum (TSMOM):**
```
Signal = sign(r_{t-12,t-1})
Position = Signal × (σ_target / σ_realized)
```

**Moving average crossover:**
```
Signal = MA_fast(P, n_short) − MA_slow(P, n_long)
Position = sign(Signal) × σ_adjustment
```

**Optimal lookback periods:** 1–3 months for autocorrelation capture, 12 months for drift capture, 50–300 days robust across regimes. TSMOM achieves **Sharpe 0.45–0.55** net of costs.

### FX volatility surface

**SABR model for FX:**
```
dF = σF^β dW₁, dσ = ν×σ×dW₂, Corr = ρ
```

Calibration: Fix β (typically 0.5), fit α to ATM, optimize ρ and ν to match RR and BF quotes.

**25-Delta conventions:**
```
σ_25D_Call = ATM + 0.5×RR + BF
σ_25D_Put = ATM − 0.5×RR + BF
```

**Variance swap fair value:**
```
K²_var = (2/T) × [∫₀^F P(K)/K² dK + ∫_F^∞ C(K)/K² dK]
```

Payoff = (σ²_realized − K²_var) × Vega_notional. **Variance risk premium** averages 2–4 vol points positive.

---

## Part 5: Equity trading strategies

### Statistical arbitrage: Pairs trading

**Cointegration testing:**
```
Z_t = Y_t − β×X_t ~ I(0) (stationary)
ADF critical value: −3.38 (95% for pairs)
```

**Half-life calculation:**
```
Half-life = −ln(2) / ln(φ) where φ = AR(1) coefficient
```
Example: φ = 0.95 → Half-life = 13.5 days. **Reject pairs with half-life >50 days or <1 day.**

**Entry/exit rules:**
| Signal | Action |
|--------|--------|
| z > +2σ | Short spread |
| z < −2σ | Long spread |
| z crosses 0 | Exit (profit) |
| \|z\| > 4σ | Stop-loss |

**Performance metrics:** Sharpe 0.5–1.5, annual returns 10–20%, max drawdown 10–20%, holding period 10–30 days, win rate 55–65%.

### Dispersion trading

**Construction:**
1. Sell index variance swap (or ATM straddle)
2. Buy single-stock variance swaps on N constituents
3. Net position: **SHORT CORRELATION**

**Vega-neutral sizing:**
```
Notional_i = w_i × Notional_index × (σ_index / σ_i)
```

**P&L mathematics:**
```
σ²_index ≈ Σ w_i² σ_i² + 2×Σ w_i w_j σ_i σ_j ρ_ij
Dispersion P&L = (σ²_index_implied − σ²_index_realized) × Notional_index − Σ(σ²_i_implied − σ²_i_realized) × Notional_i
```

**Correlation risk premium:** Implied correlation exceeds realized by **6–18 points** (Driessen et al.). Typical Sharpe 0.3–0.6. **Tail risk:** Correlation spikes to >0.8 in crises.

### Variance swaps

**Fair strike (replication):**
```
K²_var = (2/T) × Σᵢ [w_i × Option_i / K_i²]
```

**Convexity adjustment:** Var swap ≈ σ_ATM × (1 + 3T × skew²)

**Variance risk premium:** VRP = Implied Variance − Realized Variance ≈ **2–4 vol points**. Systematic variance selling achieves Sharpe 0.3–0.5.

### Event-driven: Merger arbitrage

**Spread calculation:**
```
Cash deal: Spread = (Offer_Price − Current_Price) / Current_Price
Stock deal: Spread = (Exchange_Ratio × Acquirer_Price − Target_Price) / Target_Price
```

**Expected return decomposition:**
```
E[Return] = P(close) × Upside − P(break) × Downside
Implied P(close) = Downside / (Upside + Downside)
```

**Deal risk factors add to spread:** Regulatory (DOJ, FTC, CFIUS) +5–15%, financing condition +2–5%, shareholder vote +1–3%. **Historical completion rate: ~94%** for announced deals.

---

## Part 6: Commodities strategies

### Crude oil term structure

**Cost of carry model:**
```
F(T) = S × e^{(r+u−y)T}
```
Where r = interest rate, u = storage cost rate, y = convenience yield.

**Storage arbitrage condition:** If Spread > Storage + Financing + Insurance, buy spot and sell forward.

Example (2020 contango): Spot $50, 6-month futures $57.50, storage $5 → **Net profit $2.50/barrel**.

**Crack spread (3:2:1):**
```
Crack = [(2 × RBOB_$/gal × 42) + (1 × ULSD_$/gal × 42)] / 3 − WTI_$/bbl
```

Example: WTI $75, RBOB $2.20/gal ($92.40/bbl), ULSD $2.00/gal ($84.00/bbl):
Crack = [2×$92.40 + $84.00]/3 − $75 = **$14.60/bbl**

**Historical ranges:** Normal $10–25/bbl; pre-2008 $5–20/bbl; post-Russia/Ukraine (2022) spiked to **$50+/bbl**.

### Natural gas strategies

**Spark spread:**
```
Spark_Spread = Power_Price − (Gas_Price × Heat_Rate)
```

Heat rate = BTUs required per kWh. Efficient CCGT: 7,000 BTU/kWh (~49% efficiency). When Implied Heat Rate > Physical Heat Rate → profitable to run plant.

**Locational basis spreads:**

| Hub | Typical Basis vs Henry Hub |
|-----|---------------------------|
| Waha (TX) | −$0.50 to −$4.00 |
| SoCal Citygate | +$1.00 to +$11.00 |
| Algonquin (Boston) | +$5.00 to +$30.00 |

**Extreme example (March 2024):** Waha traded at $0.08/MMBtu while Henry Hub was $4.12—basis spread of **$4.04**.

### Precious metals

**Gold-silver ratio:** Historical range 50–80:1; extreme high 125:1 (March 2020); trading rule: long silver/short gold when ratio >80, reverse when <60.

**Gold versus real rates:**
```
ln(Gold) = α + β × (−Real_Yield) + ε
```
β typically 0.15–0.25, R² around 0.6–0.7.

---

## Part 7: Macro and cross-asset strategies

### Cross-market rate spreads with FX hedge

**Construction (Long 10Y UST vs Short 10Y Bund):**
```
DV01 Hedge Ratio = DV01_UST / DV01_Bund × FX_Spot
```

With UST DV01 ~$875/bp, Bund DV01 ~$950/bp, and EUR/USD at 1.08: ratio ≈ 0.995. For $100M UST → short ~€92.5M Bunds.

**P&L attribution (12-month horizon):**

| Component | Calculation | Return |
|-----------|------------|--------|
| UST Carry | 4.50% − 4.25% funding | +25bp |
| Bund Carry | −(2.50% − 2.15%) | −35bp |
| XCCY Basis Pickup | −20bp adds to USD carry | +20bp |
| Rate Spread P&L | 200bp → 210bp × 8.5 DV01 | +85bp |
| **Net Return** | | **+78bp** |

### Risk-on/risk-off indicator construction

**Multi-component RORO index:**
```
RORO_Index = PCA_1 of: VIX, MOVE, FX_Vol, Credit_Spreads, EM_Spreads, Equity_Returns, Gold
```

**Regime classification:**

| Regime | VIX | Credit OAS | Allocation |
|--------|-----|-----------|------------|
| Bull/Complacent | <15 | <100bp | Max risk-on |
| Normal | 15–20 | 100–150bp | Balanced |
| Elevated Stress | 20–30 | 150–250bp | Reduce risk |
| Crisis | >30 | >250bp | Max risk-off |

### Unified carry framework

**Asset class carry definitions:**

| Asset Class | Carry Formula |
|-------------|--------------|
| FX | Interest rate differential |
| Commodities | (Spot − Future) / Future |
| Bonds | Term premium + Roll-down |
| Credit | Spread − Expected default |

**Historical performance (Koijen et al.):** Global Carry Factor Sharpe **1.1**, correlation to equities 0.25, max drawdown −15%.

---

## Part 8: Market making and flow strategies

### Adverse selection models

**Glosten-Milgrom:** Spread = 2 × σ × P(informed). Transaction prices form martingale as quotes are revised expectations.

**Kyle model:** Price impact ΔP = λ × OrderFlow, where **λ = σ_V / (2×σ_u)**. Empirical median λ ~6.3.

**VPIN (Flow Toxicity):**
```
VPIN = Σ|V_buy − V_sell| / (n × Volume_Bucket_Size)
```
Normal values 0.15–0.30; >0.4 indicates high toxicity. Pre-Flash Crash VPIN reached historically high levels ~1 hour before crash.

### Avellaneda-Stoikov model

**Reservation price:**
```
r(s,q,t) = s − q×γ×σ²×(T−t)
```

**Optimal spread:**
```
δ = γσ²(T−t) + (2/γ)×ln(1 + γ/κ)
```

Where s = mid-price, q = inventory, γ = risk aversion, σ = volatility, κ = order arrival intensity.

**Key insight:** Spread has two components: (1) inventory risk term γσ²(T−t), (2) order arrival term. Simulation shows inventory strategy achieves **std(P&L) = 5.89** versus symmetric strategy std = 13.43.

---

## Part 9: Quantitative and systematic strategies

### Signal construction

**Time-series momentum:**
```
Signal = sign(r_{t-12,t-1})
Position = Signal × (σ_target / σ_asset)
```
Achieves Sharpe ~0.96 annualized for diversified futures TSMOM (Moskowitz et al. 2012).

**Mean reversion:**
```
Bollinger z-score: z = (P − MA_n) / σ_n
RSI = 100 − 100/(1 + avg_gain/avg_loss)
```

### Portfolio construction

**Mean-variance optimization:**
```
w* = Σ⁻¹(μ − r_f×1) / (1'×Σ⁻¹×(μ − r_f×1))
```

**Risk parity (Equal Risk Contribution):** Solve for w such that w_i × (Σw)_i = w_j × (Σw)_j for all i,j.

**Black-Litterman posterior:**
```
E(R) = [(τΣ)⁻¹ + P'Ω⁻¹P]⁻¹ × [(τΣ)⁻¹π + P'Ω⁻¹Q]
```

### Execution: Almgren-Chriss framework

**Optimal trajectory:**
```
x_j = sinh(κ(T−t_j)) / sinh(κT) × X
```

**Market impact (square-root law):**
```
Impact = σ × (Q/V)^0.5
```

Example: Daily vol 2%, trade 5% of ADV → Impact ≈ **45 bps**.

**Total transaction costs:** TC = Spread + Market Impact + Timing Risk + Opportunity Cost. NYSE average ~8.8 bps; NASDAQ ~13.8 bps.

### Kelly criterion

**Continuous version:**
```
f* = μ/σ²
```

**Fractional Kelly (practitioner standard):**
- Full Kelly: ~33% chance of 50% drawdown
- Half Kelly: 75% of growth rate, ~22% drawdown
- Quarter Kelly: 50% of growth rate, much lower variance

**Professional recommendation:** 0.10×–0.15× Kelly.

---

## Part 10: The math

### Greeks formulas (exact)

**Black-Scholes Greeks:**
```
Delta: Δ = e^(−qT)×N(d₁) [call]
Gamma: Γ = e^(−qT)×n(d₁)/(S×σ√T)
Vega: ν = S×e^(−qT)×√T×n(d₁)
Theta: θ = −S×e^(−qT)×n(d₁)×σ/(2√T) − r×K×e^(−rT)×N(d₂) [call]
Vanna: ∂Δ/∂σ = −e^(−qT)×n(d₁)×d₂/σ
Volga: ∂ν/∂σ = ν×d₁×d₂/σ
```

### P&L attribution

**Options:**
```
ΔP = Δ×ΔS + ½Γ×(ΔS)² + θ×Δt + ν×Δσ + Vanna×ΔS×Δσ + ½Volga×(Δσ)²
```

**Delta-hedged continuous P&L:**
```
P&L_hedged = ½Γ×S²×(σ²_realized − σ²_implied)×dt
```

### Sharpe ratio estimation

**Standard error:**
```
SE(SR) ≈ √[(1 + SR²/2)/T]
```

**Sample size requirement:** T ≈ 2/SR² years for 2σ significance. Need ~400 monthly observations for SR = 0.5 to be significant at 95%.

### Information coefficient

**Fundamental Law:**
```
IR = IC × √BR
E[r] = IC × σ × Score
```

Sample size for IC significance: N ≈ (z_α)²/IC².

---

## Part 11: Real trade examples

### 2s10s steepener (2019–2020)

**Setup:** Yield curve inverted August 2019 (−7bp). Thesis: Fed cuts normalize curve via bull steepening.

**Entry:** Short 4 TU contracts at $107.50, Long 1 TY contract at $128.00

**Outcome:** March 2020 Fed cut to zero; 2s10s moved from −7bp to +70bp by June 2020, eventually +150bp by 2021. P&L: ~100bp curve move × DV01 notional.

**Lesson:** Steepeners carry negatively during inversion—requires patience and financing stability.

### Negative basis trade (2005–2008)

**Setup:** ThyssenKrupp 4.375% Mar 2015 bond, Z-spread 103.7bp, CDS at 97bp, negative basis −6.7bp.

**Crisis outcome:** Basis widened to **−200bp** during 2008. Forced selling by hedge funds hitting stop-loss limits. Merrill Lynch, Deutsche Bank, Citadel reported major losses.

**Lesson:** Basis trades require holding to maturity; leverage + liquidity mismatch = disaster.

### Swiss franc carry (2015)

**Setup:** Borrow CHF at 0%, invest in EUR at ~0.5%. Long EUR/CHF at 1.20 floor. Retail leverage often 50:1.

**January 15, 2015:** SNB removed floor; EUR/CHF crashed from 1.20 to 0.85 intraday (30%+ move). Stop-losses triggered but filled around 1.03—slippage of 1,500+ pips.

**Lesson:** Central bank policy risk is not hedgeable. Stop losses worthless in gap moves.

---

## Part 12: What actually works

### Realistic Sharpe ratios (net of costs)

| Strategy | Gross Sharpe | Net Sharpe | Capacity |
|----------|-------------|------------|----------|
| Rates RV | 0.5–1.0 | 0.3–0.8 | $1–5B |
| Credit RV | 0.6–1.2 | 0.4–0.9 | $1–5B |
| Stat arb | 0.8–2.0 | 0.5–1.5 | $500M–2B |
| Macro | 0.4–0.9 | 0.3–0.7 | $10B+ |
| Vol selling | 0.5–0.8 | 0.3–0.6 | $500M–5B |
| Market making | 0.8–2.5 | 0.5–2.0 | $100M–1B |
| HFT | 3.0–15.0 | 2.0–10.0 | $10–100M |

**Practitioner reality check:**
- "Quant funds won't consider strategies with Sharpe <2 in research"
- "Multi-manager pods: why fund 1.5 Sharpe when they have 3–4?"
- "A Sharpe of 1.5–2 with 10–20% returns and controlled drawdowns is the sweet spot"

### Edge sources and decay

**Information edge:** Faster/better data. Decay: 6–24 months as data commoditizes.

**Analytical edge:** Superior models/ML. Decay: 2–5 years as techniques diffuse.

**Execution edge:** Lower costs, better timing. Decay: 12–36 months.

**Balance sheet edge:** Hold through drawdowns. Decay: Persistent but requires scale.

**Decay indicators:** Declining gross returns requiring more leverage, increased correlation with peers, shorter holding periods, rising transaction costs.

### What blows people up

**LTCM (1998):** Leverage 25:1 balance sheet, 250:1 effective. Fatal flaw: "Long illiquid, short liquid" = massive liquidity factor exposure. Lesson: "You can take liquidity bets, but you cannot leverage them much."

**Quant crisis (August 2007):** One large fund unwinding caused cascade. Peak losses August 7–9, some funds −30% in days. Key factors: massive L/S equity AUM growth, declining profitability requiring leverage, crowding in "liquid" US equity factors.

**Classic mistakes:**
- Confusing luck with skill (August 2007 funds were profitable for years—until they weren't)
- Overtrading (transaction costs transform positive gross to negative net)
- Position sizing errors ("The most important decisions are 'how much' variety")
- Model overfit ("Even sophisticated models are subject to model risk")

### Practitioner wisdom

**Liquidity matters most:** "In crisis, leverage is not welcome. LTCM was being forced to liquidate." Theoretically hedged positions become correlated during deleveraging.

**Correlation breakdown is the killer:** "Correlation had dropped to 75% as recently as 1992—including this stress scenario might have led LTCM to assume less leverage."

**Position sizing:** Kelly criterion modified for parameter uncertainty (fractional Kelly 25–50%), maximum 2–3% of capital at risk per trade.

**Final benchmark:** Berkshire Hathaway Sharpe **0.79** over 40+ years—higher than any other stock or fund with 30+ year history. S&P 500 Sharpe 0.49 over same period. Most hedge funds: Sharpe 0.5–1.0 after fees.

---

## Summary of key P&L drivers by desk

| Desk | Primary P&L Driver | Critical Risk |
|------|-------------------|---------------|
| Rates | Carry/roll + curve positioning | Duration mismatch, vol regime |
| Credit | Spread carry + basis convergence | Liquidity, correlation spike |
| MBS | OAS alpha + prepayment model | Convexity, model error |
| FX | Carry differential + momentum | Crash risk, correlation |
| Equity | Factor exposure + vol premium | Crowding, correlation |
| Commodities | Roll yield + basis | Storage, delivery |
| Macro | Policy divergence + regime | Correlation breakdown |
| Market making | Spread capture | Adverse selection |

The strategies that persist generate edge from structural sources—balance sheet capacity, information processing, execution efficiency, or willingness to bear risks others avoid. Backtested alpha without identifiable edge source is noise.