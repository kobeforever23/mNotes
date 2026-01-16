# The Ultimate Guide to Interpreting Market Shocks by Asset Class

## A Complete Framework for Building Expert-Level Market Intuition

---

# Table of Contents

1. [Foundation: How to Think About Shocks](#foundation-how-to-think-about-shocks)
2. [Equities](#equities)
3. [Interest Rates](#interest-rates)
4. [Credit Spreads](#credit-spreads)
5. [Foreign Exchange](#foreign-exchange)
6. [Commodities](#commodities)
7. [Volatility](#volatility)
8. [Cross-Asset Relationships](#cross-asset-relationships)
9. [Regime Classification](#regime-classification)
10. [Trading Position Impact Examples](#trading-position-impact-examples)
11. [Historical Calibration](#historical-calibration)
12. [Quick Reference](#quick-reference)

---

# Foundation: How to Think About Shocks

## The Mental Model

Every market shock tells a story. Your job is to reverse-engineer that story instantly. When you see a set of shocks, you should immediately be able to answer:

1. **What type of crisis is this?** (Demand shock, supply shock, financial crisis, geopolitical event)
2. **Who is getting hurt?** (Which sectors, which geographies, which types of investors)
3. **Where is capital flowing?** (Risk-off to safe havens? Sector rotation? Geographic reallocation?)
4. **What are the second-order effects?** (Margin calls, forced selling, liquidity spirals)
5. **What's the policy response?** (Fed cuts? Fiscal stimulus? Currency intervention?)

## The Three Questions Framework

For every shock, ask:

| Question | Why It Matters |
|----------|----------------|
| **Direction** | Is this risk-on or risk-off? Inflationary or deflationary? |
| **Magnitude** | Is this a garden-variety correction or a tail event? |
| **Speed** | Gradual repricing or violent dislocation? (affects liquidity, margin calls) |

## Units Cheat Sheet

| Asset Class | Unit | Example |
|-------------|------|---------|
| Equities | % change | -25% means index drops by one quarter |
| Rates | Basis points (bps) | +100 bps = +1.00% yield change |
| Credit Spreads | Basis points (bps) | +200 bps = 2% extra yield over Treasuries |
| FX | % change | +10% USD = dollar strengthens 10% |
| Commodities | % change | -30% oil = price drops by ~1/3 |
| Volatility (VIX) | Points (absolute) | +20 pts = VIX moves from 15 to 35 |

---

# Equities

## The Basics

Equity shocks represent percentage changes to index levels or individual stock prices.

**The Math:**
```
Shocked Price = Current Price × (1 + Shock%)

Example: S&P 500 at 5,000 with -30% shock
Shocked Price = 5,000 × (1 - 0.30) = 3,500
```

## Severity Scale

| Shock Magnitude | Classification | Historical Parallel | Implied Scenario |
|-----------------|----------------|---------------------|------------------|
| -5% to -10% | Correction | Regular pullbacks | Profit-taking, minor concerns |
| -10% to -20% | Sharp correction | 2018 Q4, 2011 | Growth scare, policy uncertainty |
| -20% to -30% | Bear market | 2020 COVID, 2022 | Recession, major policy error |
| -30% to -40% | Severe bear | 2008-2009 | Financial crisis, systemic risk |
| -40% to -50% | Crash | 1929, 2008 trough | Depression-level event |
| > -50% | Catastrophic | 1929-1932, Nikkei 1990s | Structural collapse |

## What Drives Equity Shocks

### Earnings Channel (Fundamental)
```
Stock Price = Earnings × Multiple (P/E)

A -30% shock could be:
- Earnings drop 20% AND multiple contracts from 20x to 17.5x
- Earnings flat BUT multiple crashes from 20x to 14x (valuation reset)
- Earnings drop 30% AND multiple stays flat (pure earnings recession)
```

**Intuition:** In recessions, you get hit TWICE—earnings fall AND investors pay less per dollar of earnings because future is uncertain.

### Discount Rate Channel
```
Higher rates → Higher discount rate → Lower present value of future cash flows

Tech/Growth stocks hit hardest (more value in distant future earnings)
Value/Dividend stocks more resilient (near-term cash flows)
```

### Risk Premium Channel
```
Uncertainty rises → Investors demand higher risk premium → Stocks reprice lower

This explains why stocks can crash even when earnings haven't fallen yet
Markets are forward-looking and price in EXPECTED damage
```

## Sector Sensitivity Matrix

Not all stocks react equally. Understand beta and sector dynamics:

| Sector | Typical Beta | Recession Shock | Rate Shock (+) | Rate Shock (-) |
|--------|--------------|-----------------|----------------|----------------|
| Technology | 1.2–1.5 | -35% to -45% | Very negative | Very positive |
| Financials | 1.1–1.4 | -40% to -50% | Mixed (NIM vs credit) | Negative |
| Consumer Discretionary | 1.1–1.3 | -35% to -40% | Negative | Positive |
| Industrials | 1.0–1.2 | -30% to -35% | Slightly negative | Positive |
| Energy | 0.9–1.3 | Depends on oil | Neutral | Neutral |
| Healthcare | 0.7–0.9 | -15% to -20% | Slightly negative | Neutral |
| Utilities | 0.4–0.6 | -10% to -15% | Very negative | Very positive |
| Consumer Staples | 0.5–0.7 | -10% to -15% | Slightly negative | Neutral |

**Trading Intuition:**
- In a -30% broad market shock, expect high-beta tech to be down -40% or more
- Defensive sectors (utilities, staples, healthcare) might only be down -15%
- This is why sector allocation matters enormously in drawdowns

## Trading Examples: Equity Shocks

### Example 1: Long S&P 500 Futures Position

**Position:** Long 10 E-mini S&P 500 futures (ES)
**Current Level:** S&P at 5,000
**Contract Multiplier:** $50 per point
**Notional Exposure:** 10 × 5,000 × $50 = $2,500,000

**Shock:** -20% equity shock

```
New Index Level: 5,000 × 0.80 = 4,000
Point Change: -1,000 points
P&L = 10 contracts × (-1,000 points) × $50 = -$500,000

You just lost $500,000 on a $2.5M notional position (20% of notional)
```

**Risk Insight:** Futures P&L moves 1:1 with the underlying (delta = 1). No optionality protection.

### Example 2: Long Call Option Position

**Position:** Long 100 SPY 500 strike calls, 3 months to expiry
**SPY Price:** $500 (tracking S&P at 5,000)
**Option Premium Paid:** $15 per contract
**Delta:** 0.50 initially
**Vega:** 0.20
**Total Investment:** 100 × $15 × 100 shares = $150,000

**Shock:** -20% equity shock, VIX +25 points

```
New SPY Price: $500 × 0.80 = $400
Your 500-strike calls are now deep out-of-the-money

Delta P&L (rough): 100 × 100 × 0.50 × (-$100) = -$500,000
But wait—you only paid $150,000 for the options!

Actual outcome: Options likely worth ~$0.50 (mostly time value + vol)
Actual Loss: ~$145,000 (you can't lose more than premium paid)

BUT the VIX spike means if you had PUTS, they'd be worth even more than 
delta alone suggests (vega gains on top of delta gains)
```

**Risk Insight:** Long options have defined risk (max loss = premium) but can still lose 95%+ of value.

### Example 3: Short Put Position (The Dangerous One)

**Position:** Short 50 SPY 450 strike puts, 1 month to expiry
**SPY Price:** $500
**Premium Collected:** $3 per contract
**Total Premium:** 50 × $3 × 100 = $15,000

**Shock:** -20% equity shock, VIX +30 points

```
New SPY Price: $400
Your 450-strike puts are now $50 in-the-money

Intrinsic Value Alone: $50 per share
New Put Value: ~$55 (intrinsic + remaining time value + vol expansion)

P&L = 50 × 100 × ($3 - $55) = -$260,000

You collected $15,000 in premium and lost $260,000
This is why short vol strategies blow up in crashes
```

**Risk Insight:** Short options have unlimited (puts) or substantial (calls) risk. Premium collected is NOT your max loss.

---

# Interest Rates

## The Basics

Rate shocks are expressed in **basis points (bps)**. 100 bps = 1.00%.

**The Math:**
```
Shocked Yield = Current Yield + Shock (in decimal)

Example: 10Y Treasury at 4.00%, shock of +150 bps
Shocked Yield = 4.00% + 1.50% = 5.50%
```

## The Inverse Relationship: Yields and Prices

This is **critical** and trips up many people:

```
YIELDS UP = BOND PRICES DOWN
YIELDS DOWN = BOND PRICES UP

Why? A bond pays fixed coupons. If new bonds offer higher yields,
your old bond with lower coupons is worth less.
```

## Duration: The Sensitivity Measure

**Duration** tells you how much a bond's price changes for a 1% (100 bps) yield change.

```
Price Change ≈ -Duration × Yield Change

Example: 10-year Treasury, Duration = 8
If yields rise 100 bps (+1%), price falls approximately 8%
If yields fall 100 bps (-1%), price rises approximately 8%
```

### Duration by Instrument

| Instrument | Typical Duration | 100 bps Impact |
|------------|------------------|----------------|
| 2-Year Treasury | ~2 | ~2% price change |
| 5-Year Treasury | ~4.5 | ~4.5% price change |
| 10-Year Treasury | ~8 | ~8% price change |
| 30-Year Treasury | ~17 | ~17% price change |
| IG Corporate (10Y) | ~7 | ~7% price change |
| HY Corporate | ~4 | ~4% price change |
| Mortgage-Backed | ~5 (but negative convexity) | Complicated |

**Trading Intuition:** Long-duration bonds are leveraged bets on rates. A 30-year bond moves 4x as much as a 2-year for the same rate shock.

## Convexity: The Second-Order Effect

Duration is a linear approximation. **Convexity** captures the curvature:

```
For large rate moves, convexity helps you:
- Rates up a lot: You lose LESS than duration suggests
- Rates down a lot: You gain MORE than duration suggests

Price Change ≈ -Duration × ΔY + 0.5 × Convexity × (ΔY)²
```

**Why it matters:** In a +300 bps shock, a bond with high convexity loses less than simple duration math implies.

## Yield Curve Shocks

The yield curve can move in different ways:

### Parallel Shift
All maturities move by the same amount.
```
+100 bps parallel: 2Y, 5Y, 10Y, 30Y all rise 100 bps
This is the simplest shock to model
```

### Steepening
Long rates rise more than short rates (or short rates fall more than long rates).
```
Bull Steepener: Fed cuts → 2Y falls 100 bps, 10Y falls 50 bps
Bear Steepener: Inflation fears → 2Y rises 50 bps, 10Y rises 150 bps
```

### Flattening
Short rates rise more than long rates (or long rates fall more than short rates).
```
Bear Flattener: Fed hikes → 2Y rises 150 bps, 10Y rises 50 bps
Bull Flattener: Recession fears → 2Y falls 50 bps, 10Y falls 100 bps
```

### Twist
Short and long rates move in opposite directions.
```
2Y rises 50 bps while 10Y falls 50 bps (curve inverts further)
```

## Macro Narratives for Rate Moves

| Shock | Narrative | Historical Example |
|-------|-----------|-------------------|
| +200 bps (10Y) | Inflation spike, Fed behind the curve | 2022 |
| +100 bps (10Y) | Growth acceleration, term premium rise | 2023 |
| -100 bps (10Y) | Recession fears, flight to quality | 2020, 2008 |
| -200 bps (10Y) | Severe crisis, deflation fears | 2008 |
| +150 bps (2Y), flat 10Y | Fed hiking aggressively, curve flattens | 2022 |
| -150 bps (2Y), -50 bps 10Y | Fed cutting, curve steepens | 2020, 2008 |

## Trading Examples: Rate Shocks

### Example 1: Long 10-Year Treasury Position

**Position:** $10 million face value 10-Year Treasury
**Yield:** 4.00%
**Duration:** 8.0
**Price:** ~100 (par)

**Shock:** +150 bps rate rise

```
New Yield: 5.50%
Price Change ≈ -8.0 × 1.50% = -12%
New Price: ~88

Dollar P&L: $10,000,000 × (-12%) = -$1,200,000

You lost $1.2 million on a $10 million bond position
```

### Example 2: 2s10s Steepener Trade

**Position:** Long $5M 10Y Treasury, Short $12.5M 2Y Treasury (duration-weighted)
**Rationale:** Betting the curve steepens (10Y yields rise less than 2Y, or 2Y falls more)

**Initial Curve:** 2Y at 4.50%, 10Y at 4.00% (curve inverted by 50 bps)

**Shock:** Bull steepener—2Y falls 100 bps, 10Y falls 50 bps

```
2Y Position (short, duration ~2):
Price rises ~2% → You lose 2% × $12.5M = -$250,000

10Y Position (long, duration ~8):
Price rises ~4% (50 bps × 8) → You gain 4% × $5M = +$200,000

Net P&L: -$250,000 + $200,000 = -$50,000

Wait, curve steepened but you lost money?
Yes! Because BOTH yields fell. The curve steepened in a BULL move.
Your short 2Y position lost more than your long 10Y gained.

Lesson: Steepener trades can lose even when the curve steepens if the 
direction is wrong. You needed a BEAR steepener (2Y rises less than 10Y).
```

### Example 3: Receive Fixed Interest Rate Swap

**Position:** Receive fixed 4.00%, pay floating (SOFR) on $50M notional, 5Y swap
**Duration:** ~4.5 (like a 5Y bond)
**Current SOFR:** 4.50%

**Shock:** Rates fall 100 bps across the curve

```
You're receiving fixed 4.00%—this is now valuable because new swaps
would only pay ~3.00% fixed.

Mark-to-Market Gain ≈ Duration × Rate Change × Notional
≈ 4.5 × 1.00% × $50,000,000 = +$2,250,000

Plus, your ongoing carry improves:
Before: Receive 4.00%, Pay 4.50% = -50 bps negative carry
After: Receive 4.00%, Pay 3.50% = +50 bps positive carry
```

---

# Credit Spreads

## The Basics

Credit spreads represent the **extra yield** investors demand over risk-free Treasuries to compensate for default risk.

```
Corporate Bond Yield = Treasury Yield + Credit Spread

Example: 10Y Treasury at 4.00%, IG spread at 100 bps
Corporate Bond Yield = 4.00% + 1.00% = 5.00%
```

## What Spread Widening Means

```
SPREADS WIDEN = Credit risk increasing = Bond prices FALL
SPREADS TIGHTEN = Credit risk decreasing = Bond prices RISE

Widening is the credit market's way of saying "we're worried about defaults"
```

## The Credit Hierarchy

Different credit instruments have different spread levels and sensitivities:

| Credit Tier | Typical Spread (Normal) | Stressed Spread | Default Probability |
|-------------|-------------------------|-----------------|---------------------|
| AAA | 20-40 bps | 80-150 bps | ~0.01% |
| AA | 40-60 bps | 100-200 bps | ~0.02% |
| A | 60-90 bps | 150-300 bps | ~0.05% |
| BBB | 100-150 bps | 300-500 bps | ~0.15% |
| BB | 200-300 bps | 500-800 bps | ~1% |
| B | 350-500 bps | 800-1200 bps | ~3% |
| CCC | 600-1000 bps | 1500-3000 bps | ~15% |
| Distressed | 1000+ bps | 3000+ bps | >25% |

## Spread Duration

Just like rates, credit spreads have duration:

```
Price Change from Spread Move ≈ -Spread Duration × Spread Change

Example: IG corporate bond, spread duration = 7
Spreads widen 100 bps
Price Change ≈ -7 × 1.00% = -7%
```

**Important:** Credit bonds have BOTH rate duration AND spread duration. They can lose money from:
1. Rates rising (rate duration effect)
2. Spreads widening (spread duration effect)
3. BOTH at the same time (double whammy)

## Credit vs. Rates: The Correlation Question

| Scenario | Rates | Spreads | Corporate Bond |
|----------|-------|---------|----------------|
| Risk-off recession | ↓ (flight to quality) | ↑ (default fears) | Mixed—rates help, spreads hurt |
| Inflation shock | ↑ (Fed hikes) | ↑ (growth concerns) | Double whammy—both hurt |
| Goldilocks | Stable | ↓ (confidence) | Positive—spreads help |
| Financial crisis | ↓↓ (extreme flight) | ↑↑↑ (panic) | Spreads dominate—very negative |

**Key Insight:** In 2008 and 2020, Treasury yields plunged (helping bonds) but credit spreads blew out so much that corporate bonds still got crushed.

## Severity Scale for Credit Spreads

### Investment Grade (IG)

| Spread Level | Environment | Historical Parallel |
|--------------|-------------|---------------------|
| 80-100 bps | Tight/complacent | 2021, 2006 |
| 100-150 bps | Normal | Average historical |
| 150-200 bps | Mild stress | Growth concerns |
| 200-300 bps | Significant stress | 2015-2016, 2018 |
| 300-400 bps | Severe stress | COVID March 2020 |
| 400-600 bps | Crisis | 2008-2009 |
| 600+ bps | Panic | Peak 2008 |

### High Yield (HY)

| Spread Level | Environment | Historical Parallel |
|--------------|-------------|---------------------|
| 300-400 bps | Tight/complacent | 2021, 2007 |
| 400-500 bps | Normal | Long-term average |
| 500-700 bps | Mild stress | Typical correction |
| 700-900 bps | Significant stress | 2015-2016 |
| 900-1200 bps | Severe stress | COVID March 2020 |
| 1200-1500 bps | Crisis | Early 2009 |
| 1500+ bps | Panic | Peak 2008 (~2000 bps) |

## Trading Examples: Credit Spread Shocks

### Example 1: Long IG Corporate Bond

**Position:** $5 million face value BBB-rated 10Y corporate bond
**Treasury Yield:** 4.00%
**Credit Spread:** 150 bps
**All-in Yield:** 5.50%
**Rate Duration:** 7.5
**Spread Duration:** 7.0

**Shock:** Rates +50 bps, Spreads +200 bps (stagflationary stress)

```
Rate Effect: -7.5 × 0.50% = -3.75%
Spread Effect: -7.0 × 2.00% = -14.00%
Total Price Change: -17.75%

Dollar P&L: $5,000,000 × (-17.75%) = -$887,500

The spread widening did 4x more damage than the rate move
```

### Example 2: Long Credit, Short Duration (Hedged)

**Position:** Long $10M BBB corporate, Short $10M Treasury futures (duration-matched)
**Goal:** Isolate credit spread exposure, hedge out rate risk

**Shock:** Rates -100 bps (flight to quality), Spreads +150 bps (credit stress)

```
Corporate Bond:
- Rate effect: +7.5% (gains from rate drop)
- Spread effect: -10.5% (loss from spread widening)
- Net: -3.0%

Treasury Hedge:
- Duration ~7: +7% gain on short (you're short, rates fell, treasuries rose)
- Wait—you're SHORT treasuries. If prices rose, you LOSE.
- Loss: -7%

Total:
- Corporate: $10M × (-3%) = -$300,000
- Treasury short: $10M × (-7%) = -$700,000
- Net: -$1,000,000

What went wrong? In a flight-to-quality, Treasuries rally MORE than
your hedge assumed. Plus spreads widened. You got hit on both sides.
```

**Lesson:** "Hedged" credit positions can still lose significantly in stress because correlations change.

### Example 3: CDS Protection (Long Protection)

**Position:** Buy $20M notional 5Y CDS protection on a BBB company
**Spread at Entry:** 150 bps (you pay 150 bps/year for protection)
**Annual Premium:** $20M × 0.015 = $300,000/year

**Shock:** Company faces stress, CDS spreads widen to 500 bps

```
Mark-to-Market Gain:
Spread widened by 350 bps on $20M notional, ~4Y remaining duration
MTM ≈ Spread Change × Duration × Notional
≈ 3.50% × 4 × $20,000,000 = +$2,800,000

You paid $300K/year for protection that's now worth $2.8M more
This is how you profit from credit deterioration
```

---

# Foreign Exchange

## The Basics

FX shocks are percentage changes to exchange rates. **Convention is critical:**

```
USD/JPY = 150 means 1 USD buys 150 JPY
EUR/USD = 1.10 means 1 EUR buys 1.10 USD

"USD strengthens 10%" means:
- USD/JPY goes from 150 to 165 (more JPY per dollar)
- EUR/USD goes from 1.10 to 1.00 (fewer dollars per euro)
```

## The Dollar Smile Framework

The dollar tends to strengthen in two opposite scenarios:

```
        STRONG USD                    STRONG USD
            ↑                             ↑
            |                             |
      [US CRISIS]                   [GLOBAL CRISIS]
            |                             |
            ↓                             ↓
        WEAK USD ←——— GOLDILOCKS ———→ WEAK USD
                    (risk-on, stable)
```

| Scenario | USD Direction | Reasoning |
|----------|---------------|-----------|
| Global risk-off | USD ↑↑ | Flight to safety, dollar is reserve currency |
| US-specific crisis | USD ↓↓ | Capital flees US, dollar weakness |
| Synchronized growth | USD ↓ | Risk-on, capital flows to higher-yielding EM |
| US outperformance | USD ↑ | Capital flows to US for growth/yields |

## Currency Pairs and Their Stories

### Major Pairs

| Pair | What It Tells You | Shock Interpretation |
|------|-------------------|----------------------|
| EUR/USD | Risk appetite, relative growth | EUR up = risk-on or US weakness |
| USD/JPY | Risk appetite, carry trade | JPY up (USD/JPY down) = risk-off, carry unwind |
| GBP/USD | UK sentiment, Brexit effects | Highly idiosyncratic |
| USD/CHF | Safe haven flows | CHF up = European stress |
| AUD/USD | China/commodities proxy | AUD up = global growth optimism |
| USD/CAD | Oil prices, US/Canada relative | CAD up = oil up, risk-on |

### Emerging Market Currencies

EM currencies are **high-beta** risk assets:

| Scenario | EM FX Move | Reason |
|----------|------------|--------|
| Global risk-off | -10% to -30% | Capital flight, dollar funding stress |
| Commodity crash | -15% to -25% | Terms of trade shock (commodity exporters) |
| US rate hikes | -5% to -15% | Carry unwind, dollar strength |
| EM-specific crisis | -20% to -50% | Argentina, Turkey, etc. |

## FX P&L Calculation

```
FX P&L = Position Size × (End Rate - Start Rate) / End Rate [for foreign currency position]

Or more simply for USD-based investor with foreign asset:
Return in USD = Local Return + FX Return + (Local Return × FX Return)
```

### Example: Unhedged Foreign Equity Position

**Position:** $1,000,000 invested in Japanese equities
**USD/JPY at Entry:** 150
**JPY Position:** ¥150,000,000

**Shock:** Japanese stocks +10%, USD/JPY goes to 165 (USD strengthens 10%)

```
Local Return: +10%
JPY Value: ¥150,000,000 × 1.10 = ¥165,000,000

Converting back to USD:
USD Value: ¥165,000,000 / 165 = $1,000,000

Wait—you made 10% in local terms but $0 in USD terms!
The USD strengthening wiped out your equity gain.

FX Return: (150 - 165) / 165 = -9.1%
Total USD Return: +10% + (-9.1%) + (10% × -9.1%) ≈ 0%
```

**Lesson:** Unhedged international positions have massive FX exposure. A 10% currency move can erase (or double) your returns.

## Trading Examples: FX Shocks

### Example 1: Long EUR/USD Spot

**Position:** Long €10,000,000 at EUR/USD 1.1000
**USD Equivalent:** $11,000,000

**Shock:** EUR/USD falls to 1.0000 (EUR weakens 9.1%, USD strengthens)

```
New USD Value: €10,000,000 × 1.0000 = $10,000,000
P&L: $10,000,000 - $11,000,000 = -$1,000,000

Lost $1M on the EUR depreciation
```

### Example 2: USD/JPY Carry Trade Unwind

**Classic Carry Trade:** Borrow JPY (low rates), invest in USD (higher rates)
**Position:** Borrow ¥1,500,000,000 at 0.5%, invest in USD at 5.0%
**USD/JPY at Entry:** 150
**USD Position:** $10,000,000

**Shock:** Risk-off event, USD/JPY crashes to 130 (JPY strengthens 15%)

```
Annual Carry Earned: 5.0% - 0.5% = 4.5% = $450,000

FX Loss:
JPY Liability in USD terms:
- At entry: ¥1.5B / 150 = $10M
- After shock: ¥1.5B / 130 = $11.54M
- You now owe $1.54M more in USD terms

Net P&L: +$450,000 (carry) - $1,540,000 (FX loss) = -$1,090,000

One risk-off move wiped out 2+ years of carry
This is why carry trades are called "picking up pennies in front of a steamroller"
```

### Example 3: EM Currency Exposure

**Position:** $5,000,000 invested in Brazilian local currency bonds
**USD/BRL at Entry:** 5.00
**BRL Position:** R$25,000,000
**Bond Yield:** 12%

**Shock:** EM selloff—USD/BRL goes to 6.00 (BRL depreciates 17%)

```
Local Bond Return (assume flat): 0% (ignoring coupon for simplicity)
BRL Position: R$25,000,000

Converting to USD:
New USD Value: R$25,000,000 / 6.00 = $4,166,667

FX P&L: $4,166,667 - $5,000,000 = -$833,333 (-17%)

You earned 12% yield but lost 17% on FX
Net annualized return: approximately -5%
```

---

# Commodities

## The Basics

Commodity shocks are percentage changes to spot or futures prices.

```
Shocked Price = Current Price × (1 + Shock%)

Example: WTI Crude at $80/barrel with -40% shock
Shocked Price = $80 × 0.60 = $48/barrel
```

## Commodity Complex Overview

| Category | Key Commodities | Primary Drivers |
|----------|-----------------|-----------------|
| Energy | Crude Oil (WTI, Brent), Natural Gas, Gasoline | Supply/demand, geopolitics, OPEC |
| Precious Metals | Gold, Silver, Platinum | Inflation, real rates, safe haven |
| Industrial Metals | Copper, Aluminum, Iron Ore | Global growth, China, construction |
| Agriculture | Corn, Wheat, Soybeans | Weather, trade policy, ethanol |

## Oil: The Most Important Commodity

### Oil Shock Interpretation Framework

| Shock | Narrative | Macro Implication |
|-------|-----------|-------------------|
| -30% to -50% | Demand destruction | Recession, economic collapse |
| -20% to -30% | Oversupply or growth scare | OPEC+ dispute, mild recession |
| -10% to -20% | Moderate demand weakness | Growth slowdown |
| +10% to +20% | Supply tightness | OPEC cuts working, recovering demand |
| +20% to +40% | Supply disruption | Geopolitical event, major outage |
| +40% to +100%+ | Supply crisis | War, major producer offline |

### Oil's Second-Order Effects

```
Oil Down → 
  → Energy stocks crater (-40% to -60%)
  → Inflation falls → Fed can cut
  → Consumer discretionary income rises
  → EM oil exporters (Russia, Saudi, Brazil) suffer
  → Credit spreads widen in energy sector
  
Oil Up →
  → Energy stocks rally
  → Inflation rises → Fed may hike
  → Consumer squeezed
  → EM oil importers (India, Turkey) suffer
  → Airlines, transports crushed
  → Potential stagflation if demand also weak
```

### Historical Oil Shocks

| Event | Oil Move | Context |
|-------|----------|---------|
| 2020 COVID | -70% (negative prices briefly) | Demand collapsed, storage full |
| 2014-2016 | -75% | Shale supply surge, OPEC price war |
| 2008 GFC | -77% | Demand destruction |
| 2022 Russia | +60% | Supply fears, sanctions |
| 1973 Embargo | +300% | OPEC embargo |
| 1990 Gulf War | +100% | Iraq invades Kuwait |

## Gold: The Anti-Currency

### Gold Shock Interpretation

| Shock | Narrative |
|-------|-----------|
| +15% to +25% | Inflation fears, currency debasement |
| +10% to +15% | Mild risk-off, diversification |
| -5% to -15% | Risk-on, real rates rising |
| -15% to -25% | Strong dollar, rising real rates, confidence |

### Gold's Key Relationships

```
Gold vs. Real Rates (TIPS yields):
- STRONGLY INVERSELY CORRELATED
- Real rates up → Gold down
- Real rates down → Gold up
- 100 bps rise in real rates ≈ -10% to -15% gold move

Gold vs. USD:
- Generally inverse (weaker dollar = higher gold)
- But BOTH can rise in extreme panic (2020 March)

Gold vs. Inflation:
- Positive correlation but not 1:1
- Gold anticipates inflation, doesn't just track it
```

## Copper: Dr. Copper's Economic Diagnosis

Copper is called "Dr. Copper" because it has a PhD in economics—it predicts growth:

| Copper Move | Interpretation |
|-------------|----------------|
| +20% | Global growth accelerating, China stimulus |
| +10% | Construction/manufacturing pickup |
| -10% | Growth moderating |
| -20% | Recession fears, China slowdown |
| -30%+ | Severe global recession |

## Trading Examples: Commodity Shocks

### Example 1: Long Crude Oil Futures

**Position:** Long 100 WTI crude oil futures (CL)
**Contract Size:** 1,000 barrels
**Current Price:** $80/barrel
**Notional:** 100 × 1,000 × $80 = $8,000,000

**Shock:** -40% oil crash (demand destruction)

```
New Price: $80 × 0.60 = $48/barrel
Dollar Move: -$32/barrel

P&L = 100 contracts × 1,000 barrels × (-$32) = -$3,200,000

Lost $3.2M on a $8M notional position (40% loss)
```

### Example 2: Gold as Portfolio Hedge

**Portfolio:** $10,000,000 in equities
**Hedge:** $1,000,000 in gold (10% allocation)

**Shock:** Deflationary crisis—equities -30%, gold +25%

```
Equity P&L: $10,000,000 × (-30%) = -$3,000,000
Gold P&L: $1,000,000 × (+25%) = +$250,000

Net Portfolio P&L: -$2,750,000

Gold helped but only offset 8% of equity losses
Lesson: Gold allocation needs to be sized properly to meaningfully hedge
```

### Example 3: Energy Sector Correlation

**Position:** Long $5M Exxon (XOM) stock as "oil proxy"
**Beta to Oil:** ~0.6

**Shock:** Oil -30%

```
Expected XOM Move: -30% × 0.6 = -18%
But in reality, energy stocks often overshoot...

Actual XOM Move: -25% (beta expansion in stress)
P&L: $5,000,000 × (-25%) = -$1,250,000

Energy equities can move MORE than oil in severe stress
due to leverage, sentiment, and earnings impact
```

---

# Volatility

## The Basics

VIX measures expected 30-day volatility of the S&P 500, derived from options prices.

**Critical:** VIX shocks are in **points**, not percentages.

```
Shocked VIX = Current VIX + Shock

Example: VIX at 15, shock of +25 points
Shocked VIX = 15 + 25 = 40
```

## What VIX Actually Measures

```
VIX ≈ Expected Annualized Volatility of S&P 500

VIX of 20 implies:
- Expected annual move: ~20%
- Expected monthly move: 20% / √12 ≈ 5.8%
- Expected daily move: 20% / √252 ≈ 1.26%

VIX of 40 implies:
- Expected daily move: 40% / √252 ≈ 2.5%
- Markets expect 2.5% daily swings!
```

## VIX Regime Classification

| VIX Level | Regime | Market State | Daily Move Implied |
|-----------|--------|--------------|-------------------|
| 10-12 | Extreme complacency | "Buy everything" | 0.6-0.8% |
| 12-15 | Low vol | Normal bull market | 0.8-1.0% |
| 15-20 | Normal | Typical conditions | 1.0-1.25% |
| 20-25 | Elevated | Uncertainty rising | 1.25-1.6% |
| 25-30 | High | Significant stress | 1.6-1.9% |
| 30-40 | Very high | Crisis developing | 1.9-2.5% |
| 40-50 | Extreme | Full crisis mode | 2.5-3.2% |
| 50-70 | Panic | 2008/2020 territory | 3.2-4.4% |
| 70+ | Capitulation | Historic events | 4.4%+ |

## VIX Term Structure

The VIX has a term structure (VIX futures at different expirations):

### Contango (Normal)
```
Front Month VIX < Back Month VIX

Example: VIX spot = 15, 3-month VIX future = 18

Interpretation: Markets expect volatility to rise (mean reversion from low levels)
This is the NORMAL state ~80% of the time
```

### Backwardation (Stressed)
```
Front Month VIX > Back Month VIX

Example: VIX spot = 40, 3-month VIX future = 32

Interpretation: Markets expect current panic to subside
This signals FEAR and is often a contrarian buy signal
```

## The VIX-SPX Relationship

```
VIX and SPX are NEGATIVELY CORRELATED

SPX down → VIX up (fear increases)
SPX up → VIX down (fear decreases)

The relationship is ASYMMETRIC:
- VIX spikes MORE on down moves than it falls on up moves
- A -5% SPX day might send VIX +50%
- A +5% SPX day might only drop VIX -20%
```

## Historical VIX Spikes

| Event | VIX Peak | SPX Move | Date |
|-------|----------|----------|------|
| 2008 Financial Crisis | 80 | -57% (total) | October 2008 |
| 2020 COVID | 82 | -34% | March 2020 |
| 2011 US Downgrade | 48 | -19% | August 2011 |
| 2015 China Deval | 53 | -12% | August 2015 |
| 2018 Volmageddon | 37 | -10% | February 2018 |
| 2022 Rate Shock | 36 | -25% (total) | Throughout 2022 |

## Trading Examples: Volatility Shocks

### Example 1: Long VIX Futures as Hedge

**Position:** Long 100 VIX futures contracts
**Contract Multiplier:** $1,000 per point
**VIX at Entry:** 15
**Notional:** 100 × 15 × $1,000 = $1,500,000

**Shock:** Market crash, VIX spikes to 45

```
VIX Move: +30 points
P&L = 100 × 30 × $1,000 = +$3,000,000

Massive gain! VIX futures as tail hedge can pay off enormously.
```

**BUT—the catch:**
```
VIX futures in contango = negative roll yield
If nothing happens, you lose ~5-10% per month holding VIX futures
This is why VIX hedges are expensive to maintain
```

### Example 2: Short Volatility Blowup

**Position:** Short 50 VIX futures at VIX = 12 (collecting roll yield)
**Contract Multiplier:** $1,000 per point

**Shock:** VIX spikes from 12 to 50

```
VIX Move: +38 points
P&L = 50 × (-38) × $1,000 = -$1,900,000

You were collecting ~$50K/month in roll yield
One spike wiped out 3+ years of gains
```

This is exactly what happened in "Volmageddon" (February 2018) and why XIV (short VIX ETN) went to zero.

### Example 3: Option Portfolio VIX Sensitivity (Vega)

**Position:** Long portfolio of SPY options with total Vega = $50,000 per vol point
**Current IV:** 15%

**Shock:** VIX rises 20 points (IV rises from 15% to 35%)

```
Vega P&L = $50,000 × 20 = +$1,000,000

If you're long options, rising vol HELPS you (more time value)
If you're short options, rising vol HURTS you
```

**Combined with Delta:**
```
If SPX drops 20% AND VIX spikes 25 points:
- Long puts: Gain from delta + Gain from vega = HUGE profit
- Short puts: Loss from delta + Loss from vega = CATASTROPHIC
```

---

# Cross-Asset Relationships

## The Correlation Matrix (Normal Times)

| | Equities | Rates (Yields) | Credit | USD | Oil | Gold | VIX |
|---|---|---|---|---|---|---|---|
| **Equities** | 1.0 | +0.3 | -0.4 | -0.2 | +0.3 | -0.1 | -0.7 |
| **Rates** | +0.3 | 1.0 | +0.2 | +0.2 | +0.2 | -0.3 | -0.2 |
| **Credit (Spreads)** | -0.4 | +0.2 | 1.0 | +0.3 | -0.2 | +0.1 | +0.6 |
| **USD** | -0.2 | +0.2 | +0.3 | 1.0 | -0.3 | -0.4 | +0.2 |
| **Oil** | +0.3 | +0.2 | -0.2 | -0.3 | 1.0 | +0.1 | -0.2 |
| **Gold** | -0.1 | -0.3 | +0.1 | -0.4 | +0.1 | 1.0 | +0.2 |
| **VIX** | -0.7 | -0.2 | +0.6 | +0.2 | -0.2 | +0.2 | 1.0 |

## Correlation Breakdown in Crises

**Critical insight:** In crises, correlations move toward ±1. Diversification fails when you need it most.

```
Normal Times:
- Stocks and bonds: slightly positive or uncorrelated
- Different equity sectors: 0.5-0.7 correlation

Crisis Times:
- Everything risky correlates to 1.0 (falls together)
- Everything safe correlates to 1.0 (rises together)
- Risky vs. safe: correlation goes to -1.0
```

### The "Risk-On / Risk-Off" Regime

In RISK-OFF environments:

| Asset | Direction | Reasoning |
|-------|-----------|-----------|
| Equities | ↓↓ | Risk assets sold |
| Treasury Yields | ↓↓ | Flight to quality |
| Credit Spreads | ↑↑ | Default fears |
| USD | ↑↑ | Reserve currency demand |
| JPY | ↑↑ | Carry trade unwind |
| Gold | ↑ | Safe haven |
| Oil | ↓ | Demand destruction |
| VIX | ↑↑↑ | Fear spikes |
| EM Assets | ↓↓↓ | Capital flight |

## Second-Order Effects and Feedback Loops

### The Margin Call Cascade

```
Initial Shock: Equities -10%
    ↓
Leveraged funds face margin calls
    ↓
Forced selling of other assets (even winners)
    ↓
Correlations spike—everything falls
    ↓
More margin calls
    ↓
Liquidity disappears—bid/ask spreads widen
    ↓
Fire sale prices
    ↓
NAV drops trigger redemptions
    ↓
More forced selling...
```

### The Dollar Funding Crisis

```
Global stress event
    ↓
Everyone needs USD (it's the funding currency)
    ↓
Dollar strengthens (demand surge)
    ↓
EM currencies crash (dollar debt becomes heavier)
    ↓
EM corporates face debt crises
    ↓
EM credit spreads blow out
    ↓
Contagion to global credit markets
    ↓
More dollar demand...
```

### The Volatility Feedback Loop

```
Equities drop -5%
    ↓
VIX spikes from 15 to 25
    ↓
Options market makers are now short gamma
    ↓
To hedge, they must sell futures into falling market
    ↓
Selling pressure accelerates decline
    ↓
VIX spikes further
    ↓
More hedging needed
    ↓
Liquidity evaporates as dealers reduce inventory
    ↓
Bid/ask spreads widen
    ↓
Prices gap lower...
```

---

# Regime Classification

## The Four Macro Regimes

### 1. Inflationary Boom
```
Characteristics:
- Growth strong
- Inflation rising
- Central bank hawkish (hiking)

Asset Performance:
- Equities: Positive (but multiples compressing)
- Rates: Rising (hurts bonds)
- Credit: Spreads tight
- USD: Rising (rate differential)
- Commodities: Rising
- Gold: Mixed (inflation helps, rates hurt)
```

### 2. Deflationary Bust (Risk-Off Recession)
```
Characteristics:
- Growth collapsing
- Inflation falling (or deflation)
- Central bank dovish (cutting)

Asset Performance:
- Equities: Falling sharply
- Rates: Falling (flight to quality)
- Credit: Spreads widening sharply
- USD: Rising (safe haven)
- Commodities: Falling (demand destruction)
- Gold: Rising (but real rates matter)
```

### 3. Stagflation
```
Characteristics:
- Growth weak or negative
- Inflation high
- Central bank in impossible position

Asset Performance:
- Equities: Falling (earnings hit + multiples compress)
- Rates: Rising (inflation fighting)
- Credit: Spreads widening (growth concerns)
- USD: Mixed (depends on relative performance)
- Commodities: Rising (supply shock often the cause)
- Gold: Rising (inflation hedge + uncertainty)

This is the WORST regime—almost nothing works
```

### 4. Goldilocks (Risk-On)
```
Characteristics:
- Moderate growth
- Low/stable inflation
- Central bank accommodative

Asset Performance:
- Equities: Rising
- Rates: Stable or slowly rising
- Credit: Spreads tightening
- USD: Weakening (risk-on)
- Commodities: Rising (demand growth)
- Gold: Falling (no fear, rising real rates ok)
```

## Identifying Regimes from Shock Combinations

| Equities | Rates | Spreads | USD | Oil | Regime |
|----------|-------|---------|-----|-----|--------|
| -30% | -100 bps | +300 bps | +15% | -40% | **Deflationary Bust** |
| -20% | +200 bps | +200 bps | +5% | +50% | **Stagflation** |
| -15% | +150 bps | +100 bps | +10% | flat | **Rate Shock** |
| +15% | +50 bps | -30 bps | -5% | +20% | **Goldilocks** |
| -10% | -50 bps | +50 bps | flat | -10% | **Growth Scare** |
| -40% | -150 bps | +500 bps | +20% | -50% | **Financial Crisis** |

---

# Trading Position Impact Examples

## Multi-Asset Portfolio Stress Test

### Portfolio:
| Asset | Position | Exposure |
|-------|----------|----------|
| S&P 500 Futures | Long | $50,000,000 |
| 10Y Treasury | Long | $30,000,000 |
| IG Credit | Long | $20,000,000 |
| EUR/USD | Long EUR | $10,000,000 |
| Gold | Long | $5,000,000 |
| VIX Futures | Long (hedge) | $2,000,000 notional |

### Scenario: COVID-Style Crash

| Asset | Shock | Calculation | P&L |
|-------|-------|-------------|-----|
| S&P 500 | -30% | $50M × -30% | -$15,000,000 |
| 10Y Treasury | -75 bps | $30M × 8 duration × 0.75% | +$1,800,000 |
| IG Credit | Rates -75 bps, Spreads +200 bps | $20M × [(7 × 0.75%) - (6.5 × 2.0%)] | -$1,550,000 |
| EUR/USD | -8% | $10M × -8% | -$800,000 |
| Gold | +10% | $5M × 10% | +$500,000 |
| VIX Futures | +35 points | 20 contracts × 35 × $1,000 | +$700,000 |

**Total P&L: -$14,350,000**

Even with hedges, the equity exposure dominated.

### Scenario: Stagflation

| Asset | Shock | Calculation | P&L |
|-------|-------|-------------|-----|
| S&P 500 | -20% | $50M × -20% | -$10,000,000 |
| 10Y Treasury | +150 bps | $30M × 8 × -1.50% | -$3,600,000 |
| IG Credit | Rates +150 bps, Spreads +150 bps | $20M × [(-7 × 1.5%) + (-6.5 × 1.5%)] | -$4,050,000 |
| EUR/USD | -5% | $10M × -5% | -$500,000 |
| Gold | +20% | $5M × 20% | +$1,000,000 |
| VIX Futures | +20 points | 20 contracts × 20 × $1,000 | +$400,000 |

**Total P&L: -$16,750,000**

Stagflation is WORSE because even bonds lose money.

---

# Historical Calibration

## Major Crisis Comparison

| Metric | 2008 GFC | 2020 COVID | 2022 Rate Shock | 2011 Euro Crisis |
|--------|----------|------------|-----------------|------------------|
| **S&P 500** | -57% | -34% | -25% | -19% |
| **VIX Peak** | 80 | 82 | 36 | 48 |
| **10Y Yield Move** | -200 bps | -150 bps | +230 bps | -100 bps |
| **IG Spreads** | +550 bps | +300 bps | +60 bps | +150 bps |
| **HY Spreads** | +1600 bps | +800 bps | +200 bps | +400 bps |
| **Oil** | -77% | -70% | +40% | -20% |
| **Gold** | +5%* | +25% | -1% | +15% |
| **USD (DXY)** | +20% | +8% | +15% | +5% |

*Gold initially fell in 2008 due to margin call liquidation, then rallied.

## Speed of Moves

| Event | Time to Trough | Daily Moves |
|-------|----------------|-------------|
| 2008 GFC | 17 months | Multiple -5% to -9% days |
| 2020 COVID | 23 trading days | Fastest -30% ever |
| 2022 Rate Shock | 9 months | Grind lower, few big down days |
| 1987 Black Monday | 1 day | -22% in single day |

**Key Insight:** Fast crashes (2020) have V-shaped recoveries. Slow grinds (2008, 2022) take longer to bottom.

---

# Quick Reference

## Shock Interpretation At-a-Glance

| Asset | Shock Unit | ↑ Means | ↓ Means | Severity Threshold |
|-------|------------|---------|---------|-------------------|
| **Equities** | % | Risk-on | Risk-off | >20% = severe |
| **Rates (Yields)** | bps | Inflation/hawkish | Flight to quality | >150 bps = severe |
| **Credit Spreads** | bps | Default fears | Confidence | >200 bps IG = severe |
| **USD** | % | Global risk-off | US weakness | >10% = severe |
| **EUR** | % | Risk-on | Risk-off | >10% = severe |
| **JPY** | % (vs USD) | Risk-off (JPY↑) | Risk-on (JPY↓) | >10% = severe |
| **Oil** | % | Supply shock | Demand destruction | >30% = severe |
| **Gold** | % | Fear/inflation | Confidence | >15% = notable |
| **VIX** | points | Uncertainty | Complacency | >30 pts = severe |

## Regime Quick ID

| If you see... | It's probably... |
|---------------|------------------|
| Equities ↓, Rates ↓, USD ↑, Spreads ↑, Oil ↓ | Deflationary recession |
| Equities ↓, Rates ↑, USD ↑, Spreads ↑, Oil ↑ | Stagflation |
| Equities ↓, Rates ↑, USD ↑, Spreads flat, Oil flat | Rate shock |
| Equities ↑, Rates ↑, USD ↓, Spreads ↓, Oil ↑ | Goldilocks/reflationary |
| Everything down, correlations → 1 | Liquidity crisis |

## Position Sensitivity Cheat Sheet

| If You're... | Equities ↓ | Rates ↑ | Spreads ↑ | USD ↑ | VIX ↑ |
|--------------|------------|---------|-----------|-------|-------|
| Long stocks | ❌❌ | ❌ | ❌ | ✓ (if US) | ❌❌ |
| Long bonds | ✓ (flight) | ❌❌ | N/A | ✓ | ✓ |
| Long credit | ❌ | ❌ | ❌❌ | ✓ | ❌ |
| Long EM | ❌❌ | ❌ | ❌ | ❌❌ | ❌❌ |
| Long gold | ✓ | ❌ | ✓ | ❌ | ✓ |
| Long vol | ✓✓ | ✓ | ✓ | N/A | ✓✓✓ |
| Short vol | ❌❌❌ | ❌ | ❌ | N/A | ❌❌❌ |

## Mental Model Summary

```
1. DIRECTION: Risk-on or risk-off?
2. MAGNITUDE: Correction, bear market, or crisis?
3. REGIME: Inflationary, deflationary, stagflationary?
4. DURATION: What's moving and who's hurt?
5. SECOND-ORDER: What feedback loops are activated?
6. POLICY RESPONSE: What will central banks/governments do?
7. POSITIONING: How is my book affected across all assets?
```

---

# Final Thoughts

The best traders and risk managers don't just see numbers—they see **stories**. When you see:

```
Equities: -25%
Rates: -75 bps  
IG Spreads: +200 bps
HY Spreads: +500 bps
USD: +12%
Oil: -35%
VIX: +30 points
```

You should instantly think:

> "This is a classic deflationary shock—probably a growth scare or financial stress event. Investors are fleeing risk assets and piling into Treasuries. The dollar is screaming higher as the global safe haven. Credit markets are seizing up—investment grade is stressed and high yield is in crisis territory. Oil is collapsing on demand destruction, not supply. The Fed will likely cut rates aggressively. I need to check my credit exposure, my EM exposure, and whether my hedges are working."

That's the level of intuition you're building.

---

*Now go stress test your book.*
