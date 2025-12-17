---
title: "AI-Driven Stress Scenario Generation (SSG)"
subtitle: "A detailed research-style white paper with math, validation, and implementation guidance"
version: "2025-12-17"
---

# AI-Driven Stress Scenario Generation (SSG)

**Version:** 2025-12-17 (Wednesday)  
**Scope:** Finance + safety-critical systems (a unified mathematical treatment)  
**Keywords:** stress testing, reverse stress testing, scenario synthesis, generative AI, diffusion models, normalizing flows, CVAE, distributionally robust optimization, Wasserstein ambiguity sets, LLM narrative-to-quant pipelines

---

## Abstract

Stress Scenario Generation (SSG) is the problem of producing **severe, plausible, internally consistent** scenarios that expose vulnerabilities in a system. In finance this means macro/market/credit scenarios that produce tail losses and capital stress; in safety-critical AI it means environment configurations and trajectories that induce failures (collisions, constraint violations, unsafe behavior).

Traditional approaches (historical replay, handcrafted “severely adverse” narratives, parametric econometrics) struggle with **high dimensionality, regime changes, data scarcity in tails, and the need for multiple scenarios**. Recent work and policy discussions emphasize that *multiple* exploratory scenarios can reveal risks a single scenario can miss (e.g., to avoid predictability and “gaming”) and can improve risk coverage and supervisory insight.

This white paper presents a unified, modern framework for SSG driven by:

- **Generative modeling** (conditional VAEs, GANs, normalizing flows, diffusion/score-based models, factor-structured diffusion),
- **Optimization & adversarial search** (reverse stress testing, constrained maximization of loss under plausibility constraints),
- **Distributionally robust worst-case generation** (e.g., Wasserstein minimax and transport-map characterizations),
- **Narrative-to-quant pipelines** (LLMs producing auditable structured scenario specs, then a quantitative engine enforcing coherence and plausibility).

We provide math, implementation detail, diagnostics, and a practical end-to-end blueprint, grounded in up-to-date sources through late 2025.

---

## Table of contents

1. [Problem statement and definitions](#1-problem-statement-and-definitions)  
2. [Formal mathematical formulation](#2-formal-mathematical-formulation)  
3. [Quality requirements and objective trade-offs](#3-quality-requirements-and-objective-trade-offs)  
4. [Classical baselines](#4-classical-baselines)  
5. [Modern AI techniques (2025 state of the art)](#5-modern-ai-techniques-2025-state-of-the-art)  
   - 5.1 [Conditional VAEs and macro-conditioning](#51-conditional-vaes-and-macro-conditioning)  
   - 5.2 [GAN-based generators](#52-gan-based-generators)  
   - 5.3 [Normalizing flows](#53-normalizing-flows)  
   - 5.4 [Diffusion / score-based generators](#54-diffusion--score-based-generators)  
   - 5.5 [Scenario selection and reduction](#55-scenario-selection-and-reduction)  
   - 5.6 [Reverse stress testing as constrained optimization](#56-reverse-stress-testing-as-constrained-optimization)  
   - 5.7 [Distributionally robust stress generation (Wasserstein, KL)](#57-distributionally-robust-stress-generation-wasserstein-kl)  
   - 5.8 [Bayesian scenario synthesis and entropic tilting](#58-bayesian-scenario-synthesis-and-entropic-tilting)  
   - 5.9 [LLM narrative → machine-readable scenarios with auditability](#59-llm-narrative--machine-readable-scenarios-with-auditability)  
6. [Validation and diagnostics](#6-validation-and-diagnostics)  
7. [Implementation blueprint](#7-implementation-blueprint)  
8. [Best practices and open problems](#8-best-practices-and-open-problems)  
9. [References](#9-references)

---

## 1. Problem statement and definitions

### 1.1 What is a “stress scenario”?

A **scenario** is a structured description of exogenous conditions over a horizon \(t=1,\dots,T\).

- **Finance:** macro paths (GDP, unemployment, inflation, policy rates), market shock paths (curves, spreads, FX, equities, vol), credit migration and default dynamics, liquidity/margin conditions.
- **Safety-critical AI / engineering:** environment configuration and time evolution: weather, sensor noise, agent behaviors, disturbances, and other factors that induce failures.

A scenario is **stressful** if it produces large loss (or failure) for the target system, and is **useful** if it reveals actionable vulnerabilities rather than unrealistic artifacts.

A widely cited principle in banking stress testing is that scenarios should be **“severe but plausible”** (BCBS stress testing principles) [^bcbs147].

### 1.2 What is “stress scenario generation” (SSG)?

SSG is the algorithmic process that produces scenarios:

- as samples from a scenario distribution,
- as conditional samples given a narrative or constraints,
- or as adversarial/worst-case scenarios that maximize loss subject to plausibility constraints.

Many modern frameworks emphasize *multiple* scenarios rather than a single canonical scenario to broaden coverage and reduce predictability [^barr2023] [^ecb2941].

---

## 2. Formal mathematical formulation

### 2.1 Core objects

Let:

- \(z_{1:T}\): scenario trajectory (vector time series; macro variables, market factors, or environment states).
- \(x_t\): system state (portfolio/balance sheet state, robot state, etc.).
- \(u_t\): decisions/controls (hedging, rebalancing, controller actions).
- \(\pi\): policy mapping from information to decisions.
- \(\mathcal{M}\): simulator/transition model:

\[
x_{t+1} = \mathcal{M}(x_t, u_t, z_{t+1}).
\]

- \(L(\pi; z_{1:T})\): loss functional induced by scenario \(z_{1:T}\) under policy \(\pi\).

Examples of \(L\):
- trading book P\&L loss,
- capital ratio drawdown,
- expected shortfall of P\&L distribution,
- constraint violation indicators.

### 2.2 Scenario generation tasks

You usually want one or more of the following:

1. **Unconditional simulation**
   \[
   z_{1:T}\sim p(z_{1:T})
   \]
   for coverage of typical and tail behavior.

2. **Conditional generation**
   \[
   z_{1:T}\sim p(z_{1:T}\mid c)
   \]
   where \(c\) encodes narrative constraints (e.g., stagflation, commodity shock).

3. **Reverse stress testing**
   \[
   \text{find } z_{1:T} \ \text{s.t.}\ L(\pi; z_{1:T})\ge \ell^\star
   \]
   (or maximize \(L\) over a plausibility region).

4. **Worst-case generation under model uncertainty**
   Choose a distribution \(q\) near baseline \(p\) that maximizes a risk measure:
   \[
   \sup_{q\in\mathcal{U}(p)} \rho_q(L).
   \]

5. **Scenario set design**
   Select a *small* set of scenarios \(\{z^{(1)},\dots,z^{(K)}\}\) that maximizes risk capture while maintaining diversity and internal consistency (a key design goal for market shock scenario sets) [^richmond2024].

---

## 3. Quality requirements and objective trade-offs

A stress scenario generator must satisfy **multiple** requirements simultaneously.

### 3.1 Severity

A scenario should meaningfully stress the system. In finance this often means:

- large losses in tail outcomes,
- capital depletion, liquidity gaps,
- wrong-way risk, concentration risk,
- correlated market + funding stress.

Common severity metrics:
- \( \mathrm{VaR}_\alpha \), \( \mathrm{ES}_\alpha \),
- peak-to-trough drawdown,
- probability of breach of constraints,
- minimum capital ratio across horizon.

### 3.2 Plausibility (“severe but plausible”)

Plausibility can be operationalized as:

- **Likelihood-based** plausibility under a reference model \(p_\text{ref}\):
  \[
  \mathrm{plaus}(z)=\log p_\text{ref}(z).
  \]
- **Distance-based** plausibility: scenario distribution is within an ambiguity set around baseline (e.g., Wasserstein or KL balls).

A classic approach is to define a plausibility region in terms of the risk-factor distribution and search for the worst portfolio loss over that region [^breuer2009].

### 3.3 Internal consistency / coherence

Scenarios must preserve cross-factor relationships:
- macro ↔ policy rates ↔ term structure ↔ credit spreads ↔ equity risk premia
- FX ↔ rates ↔ relative growth
- volatility clustering and correlation spikes in crises

Market shock scenario design explicitly highlights the need to model relationships among market risk factors for internally consistent scenario design [^richmond2024].

### 3.4 Diversity / coverage

A single scenario can miss important vulnerabilities. Multi-scenario frameworks allow identification of which macro-financial risks are most relevant and enable reverse-stress-like search for worst outcomes across plausible alternative futures [^ecb2941]. Public policy discussion also emphasizes benefits of multiple exploratory scenarios [^barr2023].

### 3.5 A practical multi-objective lens

A common operational objective:

\[
\max_{z\in\mathcal{C}} \ \underbrace{L(\pi;z)}_{\text{severity}}
\ -\ \lambda \underbrace{\Omega(z)}_{\text{implausibility penalty}}
\ -\ \eta \underbrace{\mathrm{Redundancy}(z)}_{\text{diversity penalty}}.
\]

Where:
- \(\mathcal{C}\) encodes hard constraints (bounds, identities, monotonicity),
- \(\Omega(z)\) can be \(-\log p_\text{ref}(z)\) or distance-to-data measures.

---

## 4. Classical baselines

### 4.1 Historical replay / bootstrap

- Pros: transparent and plausible by construction.
- Cons: limited coverage of unobserved regimes; tails under-sampled.

### 4.2 Parametric econometric models

- VAR/BVAR, regime-switching VAR.
- Dynamic factor models.
- GARCH / DCC-GARCH.
- Copulas for dependence.

Pros: interpretable, estimable with limited data.  
Cons: limited expressiveness for nonlinear, high-dimensional dependence, and nonstationarity.

### 4.3 Handcrafted narratives + expert judgment

Pros: communicable.  
Cons: inconsistent, hard to calibrate, hard to update, and not scalable.

Modern practice is typically **hybrid**: structural constraints + flexible generative models + explicit scenario selection.

---

## 5. Modern AI techniques (2025 state of the art)

### 5.1 Conditional VAEs and macro-conditioning

A conditional VAE introduces latent \(h\) and maximizes an ELBO:

\[
\log p_\theta(x\mid c)\ge 
\mathbb{E}_{q_\phi(h\mid x,c)}[\log p_\theta(x\mid h,c)]
- D_{KL}(q_\phi(h\mid x,c)\|p(h)).
\]

**Use case:** generate market returns or risk-factor shocks conditioned on macro indicators or narrative constraints.

#### MacroVAE (ACM ICAIF 2025)

MacroVAE is a conditional VAE for generating multivariate return sequences under observed or counterfactual macro states [^macrovae2025]. It uses macroeconomic conditioning and discusses rolling out-of-sample evaluation to avoid look-ahead leakage.

**Practical relevance:** macro-conditioning enables counterfactual stress scenarios (e.g., unusual inflation-growth combinations) while preserving realistic return dynamics.

**Common conditioning mechanism:** Feature-wise Linear Modulation (FiLM):

\[
\mathrm{FiLM}(h,e_c)=\gamma(e_c)\odot h + \beta(e_c),
\]

where \(\gamma,\beta\) are learned functions of conditioning inputs. FiLM is a general conditioning layer introduced in the context of visual reasoning [^film].

---

### 5.2 GAN-based generators

GANs learn a generator \(G_\theta(\epsilon,c)\) via a discriminator \(D_\psi\):

\[
\min_\theta \max_\psi \
\mathbb{E}_{x\sim p_\text{data}}[\log D_\psi(x)]
+ \mathbb{E}_{\epsilon}[\log(1-D_\psi(G_\theta(\epsilon,c)))].
\]

**Strengths**
- high sample fidelity,
- flexible conditioning,
- good at capturing complex distributions when training is stable.

**Risks for stress testing**
- mode collapse reduces scenario diversity (a serious failure mode),
- likelihood is not explicit, complicating plausibility constraints,
- adversarial training instability can distort tails.

**Mitigations**
- WGAN-GP, spectral norm, gradient penalties,
- explicit diversity penalties,
- evaluation on tail dependence metrics, not just marginal moments.

---

### 5.3 Normalizing flows

Flows provide exact likelihood via invertible maps:

- \(x=f_\theta(u)\), \(u\sim p_0(u)\),
- density:
  \[
  \log p_\theta(x)=\log p_0(f_\theta^{-1}(x))
  +\log\left|\det \frac{\partial f_\theta^{-1}}{\partial x}\right|.
  \]

**Why flows are strong for stress testing**
- Explicit \(\log p_\theta(z)\) lets you enforce plausibility thresholds.
- Supports gradient-based reverse-stress search while remaining within plausibility constraints.

**Constrained reverse stress template with flows**
\[
\max_{z} \ L(\pi;z) \quad\text{s.t.}\quad \log p_\theta(z)\ge \tau.
\]
This can be solved by projected gradient methods or Lagrangian penalties:
\[
\max_z\ L(\pi;z) + \lambda(\log p_\theta(z)-\tau).
\]

---

### 5.4 Diffusion / score-based generators

Diffusion models are widely used due to stable training and strong mode coverage.

#### 5.4.1 DDPM basics

Forward noising:
\[
q(x_t\mid x_{t-1})=\mathcal{N}(\sqrt{1-\beta_t}x_{t-1}, \beta_t I).
\]

Reverse generation:
\[
p_\theta(x_{t-1}\mid x_t)=\mathcal{N}(\mu_\theta(x_t,t),\Sigma_\theta(x_t,t)).
\]

Equivalent score-based view learns \(s_\theta(x,t)\approx \nabla_x\log p_t(x)\).

#### 5.4.2 Conditioning and guidance (practical)

Common methods:
- classifier-free guidance,
- conditional score networks,
- energy-based guidance:
  \[
  s_\theta^\text{guided}(x,t)=s_\theta(x,t)+\alpha \nabla_x \log p(c\mid x),
  \]
  or replace \(\log p(c\mid x)\) with a differentiable constraint energy.

#### 5.4.3 Factor-structured diffusion for high-dimensional returns (2025)

A key challenge in finance is generating **high-dimensional** returns with limited data.

**Diffusion Factor Models** propose integrating latent factor structure into diffusion processes and decomposing the score function using time-varying orthogonal projections, with **nonasymptotic error bounds** primarily driven by intrinsic factor dimension \(k\) rather than ambient dimension \(d\) [^dfm2025].

This is especially relevant for stress testing large cross-asset universes (thousands of risk factors) with small effective sample sizes.

---

### 5.5 Scenario selection and reduction

In practice you often generate a large pool \(N\gg K\), then select a small scenario set of size \(K\) due to computational constraints.

A market shock scenario design approach proposes generating many scenarios and selecting those most likely to produce tail losses and meaningful variation while maintaining internal consistency [^richmond2024].

#### 5.5.1 A submodular-style selection objective (template)

Let \(S\subseteq \{1,\dots,N\}\), \(|S|=K\). Define utility:

\[
F(S)= \sum_{j\in \mathcal{E}} w_j \max_{i\in S}\mathrm{Impact}(j,z_i)
\ -\ \eta \cdot \mathrm{Redundancy}(S).
\]

- \(\mathcal{E}\) = exposures or portfolios you care about,
- \(\mathrm{Impact}\) = cheap proxy for tail loss (sensitivities, factor-P\&L),
- redundancy penalizes near-duplicate scenarios (e.g., via cosine similarity or Wasserstein distance between scenario trajectories).

Greedy maximization gives a strong practical heuristic.

---

### 5.6 Reverse stress testing as constrained optimization

Reverse stress testing asks: “What scenario breaks the system?”

A clean formulation:

\[
\max_{z_{1:T}} \ L(\pi; z_{1:T})
\quad \text{s.t.}\quad z_{1:T}\in\mathcal{C},\ \mathrm{plaus}(z_{1:T})\ge \tau.
\]

Where \(\mathcal{C}\) includes:
- bounds on variables,
- monotonicity constraints,
- macro identities,
- market consistency constraints.

The ECB multi-scenario stress testing framework discusses searching for scenarios that push the banking system toward worst outcomes and highlights reverse-stress concepts in that context [^ecb2941].

The Breuer et al. framework provides an operational definition using a plausibility region and systematic search for worst loss over that region [^breuer2009].

---

### 5.7 Distributionally robust stress generation (Wasserstein, KL)

Rather than selecting a single worst scenario, define a *worst-case distribution* near a baseline.

#### 5.7.1 Wasserstein ambiguity sets

Let \(p\) be baseline distribution. Define:

\[
\mathcal{U}=\{q:\ W(q,p)\le \epsilon\}.
\]

Then solve:

\[
\sup_{q\in \mathcal{U}} \mathbb{E}_{q}[L].
\]

#### 5.7.2 Worst-case generation via minimax in Wasserstein space (Dec 2025)

A recent framework develops a worst-case generator via a min–max optimization over continuous distributions in Wasserstein space and uses Brenier’s theorem to characterize least favorable distributions as the pushforward of a transport map; it proposes a single-loop GDA-type scheme with global convergence guarantees under mild assumptions [^wasserstein2025].

**Practical interpretation:** learn a transport map \(T_\theta\) that transforms baseline samples into stress samples that maximize a target risk functional.

---

### 5.8 Bayesian scenario synthesis and entropic tilting

Institutions often need to reconcile:
- a baseline forecast distribution \(p_0(y)\) for macro variables,
- multiple narrative scenarios (partial information),
- and a desire to keep the final scenario distribution coherent and auditable.

An IMF working paper develops **scenario synthesis** methods and uses **entropic tilting** to integrate narrative scenarios with statistical forecasts [^imf2025].

#### 5.8.1 Entropic tilting math

Find \(q\) closest to baseline \(p_0\) subject to constraints:

\[
\min_q D_{KL}(q\|p_0) \quad \text{s.t.}\quad \mathbb{E}_q[g(y)]=m.
\]

Solution:

\[
q^\star(y)\propto p_0(y)\exp(\lambda^\top g(y)),
\]
where \(\lambda\) is chosen so the constraints hold.

**Practical use in stress testing:** enforce scenario constraints while remaining minimally distorted relative to a validated baseline forecast distribution.

---

### 5.9 LLM narrative → machine-readable scenarios with auditability

LLMs can generate coherent narratives quickly, but institutional stress testing requires:
- reproducibility,
- numeric machine-readable outputs,
- plausibility checks,
- audit artifacts (prompts, retrieval snapshots, hashes).

A late-2025 paper proposes an auditable pipeline for generating machine-readable macro scenarios (GDP growth, inflation, policy rates) for G7 countries using an LLM with a hybrid prompt–RAG structure, then mapping scenarios into portfolio losses via a factor-based approach for VaR/ES; it emphasizes snapshotting and hash-verified artifacts for auditability and reports variance decomposition showing prompt design and portfolio composition dominate risk variation [^llm2025].

**Recommended architecture: LLM as scenario *spec* generator, not as the sole quantitative model**
1. LLM outputs structured JSON/YAML: narrative + macro path constraints.
2. Quant engine generates distributions consistent with constraints (ET, CVAE, diffusion conditioned on constraints).
3. Diagnostics and rejection filters enforce plausibility and coherence.
4. Mapping layer translates macro → risk factors → P\&L/capital.
5. Audit layer stores prompts, data snapshots, model versions, and seeds.

---

## 6. Validation and diagnostics

### 6.1 Statistical fidelity (must-have)

For generated scenarios \(z\) (or returns \(x\)):
- **Marginals:** mean/volatility/skew/kurtosis across regimes.
- **Temporal dependence:** ACF/PACF, volatility clustering, regime persistence.
- **Cross-sectional dependence:** correlation matrices, factor exposures, tail dependence.
- **Tail metrics:** empirical ES, exceedance frequencies.
- **Distances:** Wasserstein, MMD, energy distance, CRPS (for forecast distributions).

### 6.2 Stress-testing-specific diagnostics

- **Severity–plausibility frontier:** scatter plot \((\mathrm{plaus}(z), L(z))\).
- **Scenario clustering / coverage:** verify multiple distinct regimes.
- **Internal consistency checks:** macro linkages, no impossible combinations.
- **Sensitivity analysis:** robust outputs to small prompt/model changes (unless intentionally exploring prompt sensitivity).

### 6.3 Governance and reproducibility

For institutional deployment:
- deterministic modes and fixed seeds,
- dataset and retrieval snapshotting,
- model versioning and artifact hashing (explicitly emphasized in the LLM pipeline work) [^llm2025],
- documentation of assumptions and failure modes.

---

## 7. Implementation blueprint

### 7.1 Modular architecture

**Layer A — Data**
- market risk factors (curves, FX, equity, vol),
- macro series with release-date alignment (to avoid look-ahead bias),
- exposures and sensitivities.

**Layer B — Reference models**
- baseline macro forecast distribution \(p_0(y)\),
- macro-to-market mapping (factor model; structural mapping).

**Layer C — Generator**
- conditional VAE (MacroVAE-like) for returns conditioned on macro [^macrovae2025],
- diffusion generator (optionally factor-structured) [^dfm2025],
- flow model if explicit likelihood constraints are needed,
- LLM to propose structured scenario specs with audit logging [^llm2025].

**Layer D — Filter + selection**
- plausibility scoring (likelihood or distance),
- internal consistency constraints,
- select \(K\) scenarios maximizing risk capture + diversity [^richmond2024].

**Layer E — Revaluation and reporting**
- repricing / simulation,
- VaR/ES, capital impacts,
- scenario narratives and traceability artifacts.

### 7.2 End-to-end algorithm template

```text
Input:
  - Baseline model p_ref(z) (or p_ref(y) for macro)
  - Candidate generator(s) G
  - Loss evaluator L (pricing engine or proxy)
  - Plausibility threshold τ (or ambiguity radius ε)
  - Scenario budget K

1) Generate N candidate scenarios {z_i}
   - unconditional sampling
   - conditional sampling from narratives/constraints
   - optional adversarial refinement (reverse stress search)

2) Filter for plausibility and consistency
   - plaus(z_i) ≥ τ
   - pass hard constraints and coherence checks

3) Score tail impact with cheap proxies
   - ImpactProxy(z_i) for each portfolio/exposure group

4) Select K scenarios
   - maximize tail-impact coverage + diversity

5) Full revaluation on selected scenarios
   - compute P&L, VaR/ES, capital impacts, constraint violations

6) Diagnostics + audit
   - store prompts/data snapshots/model versions/seeds/hashes
   - produce severity–plausibility frontier and coverage plots
```

### 7.3 Practical generator selection guidance (2025)

- **High-dimensional market shocks with limited data:** factor-structured diffusion is a strong candidate [^dfm2025].
- **Macro-conditioned counterfactual return generation:** conditional VAE methods like MacroVAE [^macrovae2025].
- **Narrative integration with statistical forecasts:** scenario synthesis + entropic tilting [^imf2025].
- **Adversarial robustness under distribution shifts:** Wasserstein worst-case generation [^wasserstein2025].
- **Fast narrative ideation with governance:** LLM structured scenario specs + auditable pipeline [^llm2025].

---

## 8. Best practices and open problems

### 8.1 Open problems

1. **Tail truth is scarce:** validating extreme joint tails remains difficult.
2. **Plausibility is multi-dimensional:** likelihood under one model is not truth; multi-model checks are often necessary.
3. **Endogenous feedback loops:** crises involve actions (fire sales, margin spirals); scenarios should incorporate behavior and constraints.
4. **Causal correctness of counterfactuals:** conditioning is not causality; structural constraints help.
5. **Auditability vs flexibility:** powerful generators need stronger model risk governance.

### 8.2 Best practices checklist

- Use **multiple** scenarios by default (avoid single-scenario blind spots) [^barr2023] [^ecb2941].
- Maintain a **severity–plausibility frontier** and use it to justify scenario selection.
- Separate concerns:
  - narrative spec,
  - quantitative generation,
  - portfolio impact mapping,
  - diagnostics and governance.
- Prefer methods that provide:
  - controllable conditioning,
  - mode coverage (diverse tails),
  - transparent artifacts and reproducibility.

---

## 9. References

[^richmond2024]: Abdymomunov, A., Duan, Z. (2024). **Designing Market Shock Scenarios**. Federal Reserve Bank of Richmond Working Paper 24-17.  
  - HTML: https://www.richmondfed.org/publications/research/working_papers/2024/wp_24-17  
  - PDF: https://www.richmondfed.org/-/media/RichmondFedOrg/publications/research/working_papers/2024/wp24-17.pdf

[^ecb2941]: Aikman, D., Angotti, R., Budnik, K. (2024). **Stress testing with multiple scenarios: a tale on tails and reverse stress scenarios**. ECB Working Paper Series No. 2941.  
  - PDF: https://www.ecb.europa.eu/pub/pdf/scpwps/ecb.wp2941~28e2ec1e42.en.pdf

[^imf2025]: Adrian, T., Giannone, D., Luciani, M., West, M. (2025). **Scenario Synthesis and Macroeconomic Risk**. IMF Working Paper WP/25/105.  
  - PDF: https://www.imf.org/-/media/files/publications/wp/2025/english/wpiea2025105-print-pdf.pdf

[^macrovae2025]: Kubiak, S., Weyde, T., Galkin, O., Philps, D., Gopal, R. (2025). **MacroVAE: Counterfactual Financial Scenario Generation via Macroeconomic Conditioning**. ACM ICAIF (AI in Finance). DOI: 10.1145/3768292.3770360  
  - DOI landing page: https://dl.acm.org/doi/10.1145/3768292.3770360

[^dfm2025]: Chen, M., Xu, R., Xu, Y., Zhang, R. (2025). **Diffusion Factor Models: Generating High-Dimensional Returns with Factor Structure**. arXiv:2504.06566.  
  - Abstract: https://arxiv.org/abs/2504.06566  
  - HTML: https://arxiv.org/html/2504.06566v1

[^wasserstein2025]: Cheng, X., Xie, Y., Zhu, L., Zhu, Y. (2025). **Worst-case generation via minimax optimization in Wasserstein space**. arXiv:2512.08176 (Dec 2025).  
  - Abstract: https://arxiv.org/abs/2512.08176  
  - HTML: https://arxiv.org/html/2512.08176v1

[^llm2025]: Soleimani, M. et al. (2025). **LLM-Generated Counterfactual Stress Scenarios for Portfolio Risk Simulation via Hybrid Prompt-RAG Pipeline**. arXiv:2512.07867 (Dec 2025).  
  - PDF: https://arxiv.org/pdf/2512.07867

[^barr2023]: Barr, M. S. (2023). **Speech by Vice Chair for Supervision Barr on stress testing** (Oct 19, 2023). Federal Reserve.  
  - https://www.federalreserve.gov/newsevents/speech/barr20231019a.htm

[^bcbs147]: Basel Committee on Banking Supervision (BCBS). **Principles for sound stress testing practices and supervision** (BCBS 147).  
  - https://www.bis.org/publ/bcbs147.pdf

[^breuer2009]: Breuer, T., Jandačka, M., Rheinberger, K. (2009). **How to find plausible, severe, and useful stress scenarios**. International Journal of Central Banking, 5(3).  
  - IJCB page: https://www.ijcb.org/journal/ijcb09q3a7.htm  
  - RePEc entry: https://ideas.repec.org/a/ijc/ijcjou/y2009q3a7.html

[^gms2025]: Federal Reserve Board (2025). **Supervisory Stress Test Documentation – Global Market Shock Component** (Oct 2025).  
  - https://www.federalreserve.gov/supervisionreg/files/gms-model.pdf
