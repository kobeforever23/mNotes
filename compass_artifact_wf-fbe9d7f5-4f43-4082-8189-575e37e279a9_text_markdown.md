# AI Market Correction Stress Testing: Comprehensive Calibration Framework

**Bottom line:** Current market conditions present elevated risk for AI-related equity correction, with the S&P 500 trading at **6,847** (Shiller CAPE 40.33—highest since December 1999), VIX at a complacent **16.75** in contango, and credit spreads near record tights (IG OAS 82bp, HY OAS 280bp). Historical analogs suggest a moderate correction scenario mirrors Q4 2018 (-20% SPX, VIX to 36, HY +170bp), while severe scenarios calibrate to 2022 (-25% SPX, VIX to 37, HY +300bp) or dot-com bust dynamics (-30-50% for AI names). All stress parameters below are historically grounded and internally consistent across asset classes.

---

## Section 1: Current market baseline establishes starting conditions

The baseline data below represents current market levels from which stress shocks should be applied. These tight valuations and low volatility conditions amplify potential drawdown severity.

**Equity Indices and Valuations**

| Metric | Current Value | Historical Context |
|--------|---------------|-------------------|
| S&P 500 | **6,846.51** | All-time highs |
| NASDAQ Composite | **~20,167** | At/near ATH (crossed 20,000 Dec 2024) |
| S&P 500 Trailing P/E | **27.5–31.0** | 75th percentile historically |
| Shiller CAPE Ratio | **40.33** | Only exceeded in Dec 1999 (44.19) |

**Volatility Surface Baseline**

| Metric | Current Value | Stress Implications |
|--------|---------------|---------------------|
| VIX Spot | **16.75** | Low—significant upside in stress |
| VIX3M | **19.41** | Term structure in contango |
| VIX/VIX3M Ratio | **0.86** | Normal; backwardation indicates stress |
| VVIX (Vol of Vol) | **83–86** | Subdued; can spike to 150+ in stress |
| SPX 30-day Realized Vol | **12–15%** | Below long-term average of ~18% |

**Individual AI Stock Implied Volatility (30-Day)**

| Ticker | Current IV30 | Historical Range | IV Percentile Est. |
|--------|-------------|-----------------|-------------------|
| **NVDA** | 40.5% | 32–89% | ~25th percentile |
| **AMD** | 40–50% | 35–85% | ~30th percentile |
| **AVGO** | 30–35% | 25–60% | ~30th percentile |
| **MSFT** | 20–24% | 16–35% | ~25th percentile |
| **GOOGL** | 23% | 19–39% | ~25th percentile |
| **AMZN** | 26% | 22–49% | ~20th percentile |
| **META** | 28% | 24–53% | ~25th percentile |
| **CRM** | 30–35%* | 25–55% | ~30th percentile |
| **PLTR** | 55–65%* | 50–100% | ~25th percentile |
| **NOW** | 30–35%* | 28–50% | ~30th percentile |
| **SNOW** | 50–55%* | 45–80% | ~30th percentile |

*Estimated based on historical relationships and comparable names

**Credit Spreads Baseline**

| Metric | Current Level | 20-Year Average | Stress Upside |
|--------|--------------|-----------------|---------------|
| ICE BofA IG OAS | **82bp** | ~130bp | Significant tightening = room to widen |
| ICE BofA HY OAS | **280bp** | ~490bp | Near record tights |
| CDX IG | **55–65bp** | ~80bp | Historically tight |
| CDX HY | **280–320bp** | ~400bp | Compression limits downside protection |

**Treasury Yields and Curve**

| Metric | Current Level | Stress Direction |
|--------|--------------|------------------|
| 2-Year Treasury | **4.40–4.45%** | Likely down (Fed cuts) |
| 10-Year Treasury | **4.18–4.20%** | Down in flight-to-quality |
| 30-Year Treasury | **4.61%** | Down, but fiscal premium limits rally |
| 2s10s Spread | **+10 to +20bp** | Curve un-inverted Oct 2024 |
| 5s30s Spread | **~21bp** | May steepen |
| MOVE Index | **95–110** | Below 200-day MA of 110 |
| 10Y Breakeven | **2.26%** | Key indicator for rates behavior |
| Fed Funds Rate | **4.25–4.50%** | 2 cuts priced for 2025 |

---

## Section 2: Custom AI portfolio construction with weighted exposure

The stress framework requires constructing a representative AI-exposed portfolio. Below are the key constituents with index weights, betas, and AI revenue exposure for calibrating idiosyncratic vs. systematic risk.

**AI Infrastructure—Semiconductors**

| Ticker | Market Cap | S&P 500 Weight | QQQ Weight | Beta (SPX) | AI Revenue Exposure |
|--------|-----------|---------------|------------|------------|---------------------|
| **NVDA** | $3.5T | ~7.0% | ~8.7% | 1.65–1.70 | **80–90%** |
| **AMD** | $200B | ~0.6% | ~1.8% | 1.55–1.60 | 35–40% |
| **AVGO** | $1.1T | ~2.0% | ~5.0% | 1.35–1.40 | 35–40% |
| **MRVL** | $95B | ~0.3% | ~0.8% | 1.45–1.50 | 25–30% |
| **QCOM** | $185B | ~0.5% | ~1.5% | 1.25–1.30 | 15–20% |
| **INTC** | $100B | ~0.3% | ~0.7% | 1.10–1.15 | 10–15% |
| **MU** | $115B | ~0.3% | ~0.9% | 1.50–1.55 | 30–35% |

**AI Infrastructure—Cloud Hyperscalers**

| Ticker | Market Cap | S&P 500 Weight | Cloud Revenue Q3 2024 | YoY Growth | Beta (SPX) |
|--------|-----------|---------------|----------------------|------------|------------|
| **AMZN** (AWS) | $2.35T | ~4.0% | $33B | +20% | 1.20–1.25 |
| **MSFT** (Azure) | $3.19T | ~6.5% | 40% segment growth | +40% | 1.10–1.15 |
| **GOOGL** (Cloud) | $2.3T | ~4.0% | $15.15B | +34% | 1.15–1.20 |

**AI Software/Applications**

| Ticker | Market Cap | Beta (SPX) | AI Revenue Exposure | 3Y Max Drawdown |
|--------|-----------|------------|---------------------|-----------------|
| **PLTR** | $433B | 2.10–2.20 | **Core business** | 80%+ (2022) |
| **CRM** | $315B | 1.15–1.20 | Medium-High | 52% |
| **NOW** | $220B | 1.20–1.25 | Medium-High | 45% |
| **SNOW** | $77B | 1.35–1.40 | Medium | 75%+ |
| **ADBE** | $185B | 1.25–1.30 | Medium | 55% |
| **ORCL** | $510B | 0.95–1.00 | Medium | 35% |

**AI Enablers—Data Center Power**

| Ticker | Market Cap | Beta (SPX) | DC Power Exposure |
|--------|-----------|------------|-------------------|
| **VST** | $60B | 0.85–0.95 | High |
| **CEG** | $85B | 0.70–0.80 | Very High |
| **NRG** | $22B | 1.00–1.10 | High |

**Key ETF Compositions for Benchmarking**

| ETF | AUM | Top Holdings | Expense Ratio | Beta (5Y) |
|-----|-----|--------------|---------------|-----------|
| **SMH** | $35.8B | NVDA 17%, TSM 9.3%, AVGO 8.6% | 0.35% | **1.70** |
| **SOXX** | $16.7B | AVGO 8.8%, AMD 8.7%, NVDA 6.6% | 0.35% | **1.77** |
| **XLK** | $72B | NVDA 14.8%, MSFT 12.6%, AAPL 12.3% | 0.09% | 1.15 |
| **IGV** | $9.5B | PLTR 9.0%, MSFT 8.5%, ORCL 7.1% | 0.40% | 1.25 |
| **AIQ** | $7.0B | GOOGL 4.4%, Samsung 3.9%, TSLA 3.6% | 0.68% | **1.42** |

**Index Concentration Risk:** NVIDIA alone contributed **22.4%** of S&P 500's 2024 return. Top 10 holdings comprise **53.3%** of QQQ and **~35%** of S&P 500.

---

## Section 3: Historical analog calibration establishes shock magnitudes

Four historical periods provide empirically-grounded calibration for stress scenarios. The dot-com crash represents severe AI bubble burst, 2022 provides the recent tech correction template, Q4 2018 calibrates moderate corrections, and August 2024 calibrates extreme volatility spikes.

### Dot-Com Crash (March 2000–October 2002): Severe scenario ceiling

| Asset | Peak Date | Trough Date | Drawdown | Duration |
|-------|-----------|-------------|----------|----------|
| S&P 500 | Mar 24, 2000 | Oct 9, 2002 | **-49.1%** | 31 months |
| NASDAQ Composite | Mar 10, 2000 | Oct 9, 2002 | **-78%** | 31 months |
| Philadelphia Semiconductor (SOX) | Mar 2000 | Oct 2002 | **~85%** | 31 months |
| Software Sector | 2000 | 2002 | **70–90%** | 31 months |

**Volatility Profile:**
- VIX peak: **~45** (July/August 2002)
- Average VIX during drawdown: **25–27** (sustained elevation)
- Term structure: **Persistent backwardation** lasting weeks to months
- NVIDIA historical max drawdown: **-89.72%** during this period

**Credit Spreads:**
- IG OAS peak: **~300–350bp** (significant widening from ~100bp)
- HY OAS peak: **>1,000bp** (doubled from ~500bp starting level)
- Duration of stress: 2–3 years of elevated spreads

**Sector Rotation:** Utilities delivered **+132%** (Southern Company) while tech fell 78%. Defensive sectors outperformed by **80–100+ percentage points**.

### 2022 Tech Correction (January–October 2022): Recent analog

| Asset | Peak-to-Trough | Peak Date | Trough Date |
|-------|---------------|-----------|-------------|
| S&P 500 | **-25.4%** | Jan 3, 2022 | Oct 12, 2022 |
| QQQ | **-33%** | Nov 2021 | Oct 2022 |
| SMH | **-42%** | Jan 2022 | Oct 2022 |
| ARKK | **-81%** | Feb 2021 | Dec 2022 |
| **NVDA** | **-66%** | Nov 2021 | Oct 2022 |
| **AMD** | **-65%** | Nov 2021 | Oct 2022 |
| **CRM** | **-52%** | Nov 2021 | Dec 2022 |
| **PLTR** | **-78%** | Feb 2021 | Dec 2022 |
| **SNOW** | **-67%** | Nov 2021 | Dec 2022 |

**Volatility Profile:**
- VIX peak: **36–37** (March and October 2022)
- Average VIX: **25–26** throughout drawdown
- SPX realized volatility: **22–28%** (vs. ~15% normal)
- Term structure: Backwardation periods shorter (days–weeks vs. months)

**Credit Spreads:**
- IG OAS: **95bp → 170–180bp** (+75–85bp widening)
- HY OAS: **310bp → 600–620bp** (+290–310bp widening)
- **Key difference from 2000:** Credit stress significantly milder

**Recovery:** 15 months to new S&P 500 all-time highs (January 2024)

### Q4 2018 Selloff: Moderate correction template

| Metric | Value | Notes |
|--------|-------|-------|
| S&P 500 Drawdown | **-19.8%** | Near bear market threshold |
| Duration | **~3 months** | Sept 20–Dec 24, 2018 |
| VIX Peak | **~36** | Elevated but not extreme |
| IG OAS Widening | **+60bp** (to ~157bp) | Moderate stress |
| HY OAS Widening | **+170bp** (to ~533bp) | Not crisis levels |
| Recovery | **V-shaped** | S&P +28.9% in 2019 |

**Trigger factors:** Fed hiking cycle, China trade war, global growth fears
**Calibration value:** Good template for "significant but not severe" stress scenario

### August 2024 Volatility Event: Extreme vol spike calibration

| Metric | Value | Context |
|--------|-------|---------|
| VIX Intraday Peak | **65.73** | 7th largest daily VIX spike ever |
| VIX Closing Level | **38.57** | Opened at 23.39 |
| VIX–Futures Gap | **30+ points** | Extreme dislocation |
| S&P 500 Drawdown | **~8–10%** | Modest vs. VIX spike |
| Normalization | **Days to weeks** | VIX below 20 by late August |

**Trigger:** Bank of Japan rate hike → yen carry trade unwind (~$250B, 65–75% liquidated)
**Critical insight:** VIX spike was largely **technical/microstructural**, not fundamental. Demonstrates vol can overshoot dramatically in illiquid conditions before rapid mean reversion.

---

## Section 4: Volatility dynamics research enables consistent calibration

The empirical relationships below ensure stress scenario volatility shocks are internally consistent with equity drawdown assumptions.

**Vol-Spot Beta (VIX Response to SPX Declines)**

| Regime | SPX Move | VIX Beta | Calibration Use |
|--------|----------|----------|-----------------|
| Normal (VIX <18) | ±0.5–1% | **-6 to -8** | Small drawdowns |
| Elevated (VIX 18–25) | ±1–2% | **-5 to -6** | Moderate stress |
| Stress (VIX >25) | ±2–3% | **-4 to -5** | Sustained selloff |
| First shock from calm | Initial -3%+ | **-12 to -14** | Acute surprise |
| Extreme | >3% | **-3 to -4** | Beta compresses at extremes |

**Application:** For a -25% SPX drawdown from current VIX 16.75:
- First -10%: VIX rises ~12–14 points → VIX at ~29–31
- Next -10%: VIX rises ~8–10 points → VIX at ~38–40
- Final -5%: VIX rises ~3–4 points → VIX at ~42–44
- **Calibrated VIX peak for -25% SPX: 38–44**

**Volatility Surface Stress Parameters**

| Parameter | Normal Level | Stress Level | Extreme |
|-----------|-------------|--------------|---------|
| 25-delta put skew | 4–6 vol pts above ATM | 8–12 vol pts | 15+ vol pts |
| 10-delta put skew | 8–12 vol pts | 15–20 vol pts | 25+ vol pts |
| Term structure | Contango (back 3–6 pts above front) | Flat to inverted | Front 5–10+ pts above back |
| VRP (IV–RV) | +3 to +5 vol pts | Can go negative briefly | +5 to +10 vol pts after spike |
| Speed of inversion | N/A | **1–2 days** | Hours |

**Implied Correlation Dynamics**

| Regime | SPX Implied Correlation | Behavior |
|--------|------------------------|----------|
| Normal | **25–40%** | Dispersion opportunities exist |
| Elevated | **40–60%** | Diversification eroding |
| Crisis | **70–90%+** | "Correlation goes to 1" |
| Peak (Nov 2008) | **105.93** | Mathematical ceiling exceeded |

**Correlation spike speed:** Can surge from 0.3–0.5 to 0.8+ in **a few days**. March 2020 saw 12-month rolling correlations reach **~0.9**.

---

## Section 5: Credit spread calibration with Merton model grounding

Credit shocks must be consistent with equity drawdowns through the Merton model relationship between equity volatility and credit spreads.

**Historical Credit Spread Peaks (Ceiling Calibration)**

| Event | IG OAS Peak | HY OAS Peak | Context |
|-------|-------------|-------------|---------|
| **2008 GFC** (ceiling) | **656bp** | **2,182bp** | Systemic financial crisis |
| 2020 COVID | ~400bp | 1,087bp | Demand shock, Fed intervened |
| 2022 Rate Shock | 170–180bp | 600–620bp | Inflation-driven, not liquidity |
| 2015–16 Energy | 188bp | 887bp | Sector-specific stress |
| **Current (baseline)** | **82bp** | **280bp** | Record tights |

**Spread Widening per 10% Equity Decline (Empirical)**

| Credit Tier | Moderate Stress | Severe Stress |
|-------------|-----------------|---------------|
| IG OAS | +30–40bp | +45–60bp |
| HY OAS | +100–150bp | +200–250bp |

**Technology Sector Credit Context:**
- No dedicated tech credit indices exist
- Tech issuers primarily investment grade (GOOGL AA+, MSFT AAA, ORCL BBB)
- Recent CoreWeave (AI infrastructure, HY): CDS widened from 360bp to **630bp**
- Oracle: 5Y CDS at 80–105bp, 30Y bonds at 65 cents (down 8% from peak)

**Calibrated Stress Spreads (NOT to exceed 2008 peaks)**

| Scenario | IG OAS | HY OAS | CDX IG | CDX HY |
|----------|--------|--------|--------|--------|
| **Current Baseline** | 82bp | 280bp | 60bp | 300bp |
| **Moderate (-15–20% SPX)** | 140–160bp | 450–520bp | 100–120bp | 450–480bp |
| **Severe (-25–30% SPX)** | 200–250bp | 600–700bp | 150–180bp | 550–600bp |
| **Extreme (-35%+ SPX)** | 300–400bp | 900–1,100bp | 200–250bp | 700–850bp |
| **Ceiling (2008)** | 656bp | 2,182bp | N/A | N/A |

---

## Section 6: Rates and flight-to-quality scenario modeling

Treasury behavior during an AI correction depends critically on whether the shock is deflationary (2020-style) or inflationary (2022-style). Current conditions favor flight-to-quality.

**Historical Treasury Responses to Equity Stress**

| Event | 10Y Yield Change | Flight-to-Quality? | Key Driver |
|-------|-----------------|-------------------|------------|
| 2008 GFC | **-200bp** | Yes | Credit crisis, demand shock |
| Q4 2018 | **-55bp** | Yes | Growth fears, Fed pause |
| March 2020 | **-100bp net*** | Yes, then No, then Yes | Demand shock → liquidity crisis → Fed |
| 2022 | **+275bp** | **No** | Inflation shock, Fed hiking |

*March 2020 note: 10Y hit 0.318% low on March 9, then **spiked 64bp** March 9–18 during liquidity crisis before Fed intervention restored flight-to-quality dynamic.

**Key Determinant: Breakeven Inflation**
- Current 10Y breakeven: **2.26%** (anchored, near Fed target)
- If breakevens stay anchored or fall → Flight-to-quality likely (2020/2018 analog)
- If breakevens spike above 2.5–3% → Limited Treasury rally (2022 analog)

**Base Case for AI Bubble Burst:** An AI correction would likely be a **deflationary demand/valuation shock**, not an inflation shock:
- Capital expenditure pullback = deflationary
- No concurrent supply-shock inflation driver
- Fed not currently fighting 9% CPI (vs. 2022)
- **Expect 10Y yields to fall 75–150bp in severe scenario**

**Calibrated Rates Shocks**

| Scenario | 10Y Yield Change | 2s10s Spread | MOVE Index |
|----------|-----------------|--------------|------------|
| Current Baseline | 4.20% | +15bp | 100–110 |
| Moderate Stress | -50 to -75bp (to 3.45–3.70%) | Flattening to +5–10bp | 120–140 |
| Severe Stress | -100 to -150bp (to 2.70–3.20%) | Bull flattening, 0 to -10bp | 150–170 |
| Liquidity Crisis Risk | Initial +25–50bp spike possible | Curve distortion | 180–200+ |

---

## Section 7: Integrated stress scenario calibration matrices

The matrices below integrate all research into three coherent stress scenarios calibrated for professional risk management applications.

### Scenario A: Moderate Correction (Q4 2018 Analog)

| Asset Class | Shock | Rationale |
|-------------|-------|-----------|
| **S&P 500** | -18 to -22% | Q4 2018 was -19.8% |
| **NASDAQ/QQQ** | -25 to -28% | ~1.3x SPX drawdown |
| **AI Portfolio (SMH-weighted)** | -30 to -35% | Beta 1.7x |
| **NVDA** | -40 to -45% | High beta, high AI exposure |
| **VIX Peak** | 34–38 | Q4 2018 hit ~36 |
| **VIX Average** | 24–28 | Elevated but not extreme |
| **VIX Term Structure** | Flat to mild backwardation | Days in backwardation |
| **25-delta skew** | 8–10 vol pts above ATM | Moderate steepening |
| **Implied Correlation** | 50–60% | Diversification erodes |
| **IG OAS** | 150–165bp (+70–85bp) | Q4 2018 hit 157bp |
| **HY OAS** | 480–540bp (+200–260bp) | Q4 2018 hit 533bp |
| **CDX IG** | 100–120bp | |
| **CDX HY** | 450–500bp | |
| **10Y Treasury** | -50 to -75bp (to 3.45–3.70%) | Flight-to-quality |
| **MOVE Index** | 125–145 | Elevated but not extreme |
| **Duration** | 2–4 months | Q4 2018 was 3 months |

### Scenario B: Severe Correction (2022 Analog)

| Asset Class | Shock | Rationale |
|-------------|-------|-----------|
| **S&P 500** | -25 to -30% | 2022 was -25.4% |
| **NASDAQ/QQQ** | -32 to -38% | 2022 QQQ was -33% |
| **AI Portfolio (SMH-weighted)** | -42 to -50% | 2022 SMH was -42% |
| **NVDA** | -55 to -65% | 2022 was -66% |
| **PLTR** | -70 to -78% | 2022 was -78%; high beta |
| **SNOW** | -60 to -70% | 2022 was -67% |
| **VIX Peak** | 38–45 | 2022 hit 36–37; could exceed |
| **VIX Average** | 26–32 | Sustained elevation |
| **VIX Term Structure** | Backwardation (front 3–8 pts above back) | Weeks in backwardation |
| **25-delta skew** | 10–14 vol pts above ATM | Significant steepening |
| **Implied Correlation** | 60–75% | High correlation regime |
| **IG OAS** | 200–250bp (+120–170bp) | Below 2020 peak |
| **HY OAS** | 580–680bp (+300–400bp) | 2022 hit ~600bp |
| **CDX IG** | 140–170bp | |
| **CDX HY** | 530–600bp | |
| **10Y Treasury** | -75 to -125bp (to 2.95–3.45%) | Strong flight-to-quality |
| **MOVE Index** | 150–175 | Elevated bond vol |
| **Duration** | 6–10 months | 2022 was 9 months |

### Scenario C: Extreme/Tail (Dot-Com Severity with Modern Speed)

| Asset Class | Shock | Rationale |
|-------------|-------|-----------|
| **S&P 500** | -35 to -45% | Between 2022 and 2000 |
| **NASDAQ/QQQ** | -50 to -60% | Dot-com was -78% |
| **AI Portfolio (SMH-weighted)** | -60 to -70% | High-beta amplification |
| **NVDA** | -70 to -80% | Historical max -89.72% |
| **Speculative AI (PLTR, SNOW)** | -80 to -90% | ARKK fell -81% in 2022 |
| **VIX Peak** | 55–70 | Aug 2024 intraday was 65.73 |
| **VIX Average** | 35–45 | Dot-com average was 27; modern amplification |
| **VIX Term Structure** | Deep backwardation (front 8–15 pts above back) | Persistent |
| **25-delta skew** | 14–20+ vol pts above ATM | Extreme steepening |
| **Implied Correlation** | 75–90%+ | Near "correlation = 1" |
| **IG OAS** | 350–450bp (+270–370bp) | **Below 2008 ceiling of 656bp** |
| **HY OAS** | 900–1,200bp (+620–920bp) | **Below 2008 ceiling of 2,182bp** |
| **CDX IG** | 220–280bp | |
| **CDX HY** | 700–900bp | |
| **10Y Treasury** | -125 to -175bp (to 2.45–2.95%) | Major flight-to-quality |
| **MOVE Index** | 175–220 | Approaching 2008/2020 levels |
| **Duration** | 12–24 months | Prolonged de-rating |

---

## Conclusion: Key calibration principles for implementation

This research establishes five critical calibration principles for constructing arbitrage-free, historically-grounded stress scenarios:

**Vol-spot consistency is paramount.** VIX shocks must align with vol-spot beta relationships: a -25% SPX drawdown implies VIX peaks of 38–44, not 60+. The August 2024 VIX spike to 65 was a technical dislocation—monthly realized vol settled at only ~20%, demonstrating that extreme VIX prints do not necessarily imply proportional equity damage.

**Credit spreads should never exceed 2008 peaks** for scenarios short of complete financial system failure. IG OAS of 656bp and HY OAS of 2,182bp represent absolute ceilings. The empirical relationship of ~45–50bp IG widening and ~200–250bp HY widening per 10% equity decline provides internal consistency.

**Individual AI names require beta-adjusted shocks.** NVDA with beta 1.65–1.70 and 80–90% AI revenue exposure should experience drawdowns of **1.8–2.5x** SPX in stress scenarios. PLTR with beta 2.1–2.2 can decline 70–80% even in scenarios where SPX falls only 25–30%.

**Treasury behavior depends on inflation regime.** Current breakevens at 2.26% and subdued inflation expectations favor the 2020/Q4 2018 flight-to-quality template, with 10Y yields falling 75–150bp in severe scenarios. Monitor breakevens as the key leading indicator—rising above 2.5–3% would shift dynamics toward the 2022 template where bonds fail as hedges.

**Correlation regime shifts require modeling.** Implied correlations can spike from 30% to 80%+ in days, eliminating diversification benefits precisely when needed. Stress scenarios should assume correlation convergence toward 1.0, particularly for AI names with high common factor exposure.

These parameters enable construction of a professional-grade stress testing package with historically-calibrated, internally-consistent shocks across equities, volatility surfaces, credit, and rates—suitable for presentation to senior risk management at major financial institutions.