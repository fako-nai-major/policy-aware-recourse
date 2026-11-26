# Theory for rule-verified recourse (v3) — draft for the Machine Learning manuscript

Status: draft of Section 4 ("Guarantees"), 25 Nov 2026. Every statement is matched to
the code (`recourse/exact.py`, `recourse/core.py`) and checked empirically by
`verify_bounds.py` / `analyze_bounds.py` (Section 8). Proofs are written out
in full enough to be compressed into the paper and an appendix.

---------------------------------------------------------------------------------

## 1. Setting and notation

* Features $x\in\mathbb{R}^d$; actionable set $J\subseteq[d]$, costed set $C\subseteq J$ (derived
  features such as CLTV in the structural lending domain carry no cost), immutable set $I=[d]\setminus J$.
* **Action box** $B(x_0)=\{x:\ \ell_j\le x_j\le u_j\ (j\in J),\ x_j=x_{0j}\ (j\in I)\}$ with ranges $r_j=u_j-\ell_j>0$.
* **Structural links** $L(x_0)$: a polyhedron (equalities and inequalities tying features together, e.g. CLTV follows the loan amount).
* **Rule** $\Pi$: a conjunction $P_0=\{x: Wx\le\tau\}$ and optionally a disjunction over branches $P_1,\dots,P_m$ (each a polyhedron). Writing $P=P_0\cap\bigcup_b P_b$ (or $P=P_0$ when there is no disjunction):
  $$R(x_0)=B(x_0)\cap L(x_0)\cap P\qquad\text{(rule-feasible set, a finite union of polyhedra).}$$
* **Model** $f:\mathbb{R}^d\to\{0,1\}$, favourable set $F=\{x: f(x)=1\}$.
* **Acceptable set** $A(x_0)=R(x_0)\cap F$ — exactly the vectors that pass the gate (`core.gate`).
* **Cost** $c(x)=\sum_{j\in C}|x_j-x_{0j}|/r_j\;+\;\lambda\,|\{j\in C: x_j\neq x_{0j}\}|$ with $\lambda=0.5$; write $c=e+\lambda s$ (effort + sparsity). Note $e(x)\le |C|$ on $B(x_0)$.
* $\mathrm{OPT}(x_0)=\inf_{x\in A(x_0)} c(x)$ ($+\infty$ if $A=\emptyset$).

**Model classes.**
*Linear* (logistic regression): $F=\{x:\beta^\top x+b>0\}$.
*Tree ensembles* (random forest, CatBoost): each tree routes $x$ through axis-aligned tests
$x_j\le\theta$ to a leaf value; the score is $\mathrm{sc}(x)=\alpha\sum_t v_t(x)+\beta_0$ and
$F=\{x:\mathrm{sc}(x)>\kappa\}$ (sklearn: mean leaf probability $>0.5$; CatBoost: raw score $>0$,
test "$x_j>$ border" in float32). Let $\Theta_j$ be the thresholds on feature $j$ inside
$(\ell_j,u_j)$. The thresholds cut $B(x_0)$ into finitely many **cells** (products of intervals
$(\theta_{j,k-1},\theta_{j,k}]$) on which $\mathrm{sc}$ is constant; hence $F\cap B(x_0)$ is a finite
union of half-open boxes and $A(x_0)$ is a finite union of (not necessarily closed) polyhedra.

## 2. The mixed-integer program $M_\varepsilon(x_0)$

`solve_exact` builds the program below; $\varepsilon=(\varepsilon_R,\varepsilon_S,\varepsilon_F)$ are the
safety margins in the code (`EPS_RULE`$=10^{-6}$ relative, `EPS_SCORE`$=10^{-6}$; split margin
$\varepsilon_S(\theta)=\max\{8\,\mathrm{ulp}_{32}(\theta),\,10^{-9}M_j+10^{-9}\}$, a few float32 rounding steps, because the
models compare float32 inputs). *Revision v3.1:* the first version used a fixed $\varepsilon_S=10^{-4}$ (and, for random
forests, the same margin on the left side). On Give Me Some Credit, whose ratios sit at or near 0 with random-forest
thresholds closer together than $10^{-4}$, this removed real actions from $A_\varepsilon$: 433 tree-model rows were
"optimal" yet beaten by a heuristic and one query was declared infeasible although other methods found accepted
vectors. With the ulp-based margin all tree-model rows were recomputed; on every other domain the optimal costs and
yields were unchanged.

* variables $x\in B(x_0)$; $u_j\ge|x_j-x_{0j}|$ and binaries $\sigma_j$ with $u_j\le M_j\sigma_j$ ($j\in C$), objective $\sum_j u_j/r_j+\lambda\sum_j\sigma_j$;
* rule rows tightened: $w^\top x\le\tau-\varepsilon_R\max(1,|\tau|)$ (and the mirror for $\ge$); disjunctions with branch binaries $\delta_b$, $\sum_b\delta_b\ge1$ and big-M rows whose $M$ is the exact range of $w^\top x$ over $B(x_0)$;
* links: equalities exactly, inequalities tightened as the rule;
* linear model: $\beta^\top x+b\ge\varepsilon_F$;
* tree ensembles: one binary $a_{jk}$ per threshold $\theta_{jk}\in\Theta_j$ with
  $a_{jk}=1\Rightarrow x_j\le\theta_{jk}$, $a_{jk}=0\Rightarrow x_j\ge\theta_{jk}+\varepsilon_S$, ordered $a_{j1}\le a_{j2}\le\dots$;
  continuous leaf variables $z_{t\ell}\ge0$, $\sum_\ell z_{t\ell}=1$, and for every split node $n$ on $(j,\theta)$:
  $\sum_{\ell\in\text{left}(n)}z_{t\ell}\le a_{j\theta}$, $\sum_{\ell\in\text{right}(n)}z_{t\ell}\le1-a_{j\theta}$
  (Mišić 2020; CatBoost: the same per tree level). Score row $\alpha\sum_{t,\ell}v_{t\ell}z_{t\ell}+\beta_0\ge\kappa+\varepsilon_F$.
  Splits on immutable features, or with thresholds outside the bounds, are resolved to constants first.
* ReLU networks (two hidden layers of 20 units; the input scaler is folded into the first layer): for each
  hidden unit, pre-activation bounds $[L,U]$ are propagated by interval arithmetic over $B(x_0)$ (immutable
  features fixed, so the bounds are per query). Units with $U\le0$ are fixed to 0, units with $L\ge0$ are
  linear ($y=\text{pre}$), and the rest get one binary $\delta$ with the standard big-M rows
  $y\ge\text{pre},\ y\ge0,\ y\le\text{pre}-L(1-\delta),\ y\le U\delta$ (Tjeng et al., 2019; Anderson et al., 2020).
  The logit row is $\ge\varepsilon_F$ (sklearn predicts class 1 iff the logit is positive).
  *Numerics:* with the 1e-9 MIP feasibility tolerance used for the other models, HiGHS presolve cut off the
  optimal branch on a test case; a looser tolerance (1e-7) instead let sparsity binaries take fractional values
  so that features moved by ~1e-5 "for free" (4 OULAD queries in which a heuristic beat the reported optimum).
  Networks are therefore solved at tolerance 1e-9 with presolve off; after this all checks pass.

## 3. Soundness

**Theorem 1 (soundness).** Let $(x,u,\sigma,a,z,\delta)$ be feasible for $M_\varepsilon(x_0)$. Then $x\in A(x_0)$,
and the objective value is at least $c(x)$, with equality at every optimal solution.

*Proof.* $x\in B(x_0)$ by the variable bounds. Each rule row, link inequality and disjunction row is
the original constraint with a non-negative tightening, and the big-M of a branch is the exact
range of the row over $B(x_0)$, so an active branch ($\delta_b=1$) enforces its constraints and an inactive one
is slack; hence $x\in R(x_0)$. *Model.* Linear: immediate. Trees: given $x$, the threshold rows
force $a_{jk}=\mathbb 1[x_j\le\theta_{jk}]$ (if $\theta<x_j<\theta+\varepsilon_S$ no value of $a$ is feasible, so such $x$
are excluded). Fix a tree and let $\ell^\*$ be the leaf reached by $x$. Every other leaf $\ell$ has an ancestor
split $n$ at which $x$ goes the other way; the row of $n$ on that side has right-hand side $0$, so
$z_{t\ell}=0$; with $\sum_\ell z_{t\ell}=1$ this gives $z_{t\ell^\*}=1$. The score row therefore reads
$\mathrm{sc}(x)\ge\kappa+\varepsilon_F>\kappa$, i.e. $f(x)=1$. ReLU networks: because $L\le\text{pre}\le U$ holds on
$B(x_0)$, the four big-M rows admit exactly $y=\max(\text{pre},0)$ ($\delta=1$ forces $y=\text{pre}\ge0$, $\delta=0$ forces
$y=0\ge\text{pre}$), so by induction over layers the logit variable equals the network's logit. *Cost.* $u_j\ge|x_j-x_{0j}|$ and $\sigma_j=0$ forces
$u_j$ within the evaluation tolerance of $0$ (the same `isclose` tolerance used to count sparsity), so the objective
is $\ge c(x)$; at an optimum each $u_j$ and $\sigma_j$ is as small as allowed, giving equality. $\square$

*Remark (floating point).* Soundness is not left to the solver: every output is re-checked by the gate with a
fresh call to $f$, and solver round-off is snapped only when the snapped vector still passes the rule, the links
and the parsed model. In all 104 result files no optimal exact solution was rejected by the gate.

## 4. Completeness up to the margins, and certified abstention

Define the **$\varepsilon$-interior** of the acceptable set
$$A_\varepsilon(x_0)=\{x\in A(x_0):\ \text{every rule row and link inequality holds with slack}\ \ge\varepsilon_R\max(1,|\tau|);\ x_j\notin(\theta,\theta+\varepsilon_S)\ \forall\theta\in\Theta_j;\ \mathrm{sc}(x)\ge\kappa+\varepsilon_F\}.$$

**Theorem 2 (sandwich).** $A_\varepsilon(x_0)\subseteq\mathrm{proj}_x M_\varepsilon(x_0)\subseteq A(x_0)$. Consequently
1. the optimal value of $M_\varepsilon$ equals $\min_{x\in A_\varepsilon}c(x)$, and the minimum is attained;
2. **certified abstention:** if $M_\varepsilon$ is infeasible then $A_\varepsilon(x_0)=\emptyset$ — no acceptable vector exists
   except possibly within $\varepsilon$ of a rule, link or decision boundary;
3. **model-free abstention:** if the rule-only problem ($M_\varepsilon$ with $F$ dropped) is infeasible then
   $R_\varepsilon(x_0)=\emptyset$, so no recourse can exist for *any* model.

*Proof.* The right inclusion is Theorem 1. For the left one take $x\in A_\varepsilon$ and set
$a_{jk}=\mathbb 1[x_j\le\theta_{jk}]$ (feasible for both threshold rows because $x_j\notin(\theta,\theta+\varepsilon_S)$; the
ordering holds since thresholds are sorted), $z$ the reached-leaf indicators, $u_j=|x_j-x_{0j}|$,
$\sigma_j=\mathbb 1[x_j\ne x_{0j}]$, and $\delta_b=1$ for a branch satisfied with slack. All rows hold.
For networks the same construction works with $\delta_j=\mathbb 1[\text{pre}_j>0]$ (no $\varepsilon$ is needed on the ReLU
rows, so $A_\varepsilon$ only tightens the logit). (1): $M_\varepsilon$ is a MILP with bounded integer part; for every fixed integer assignment the
remaining problem is an LP over a closed polyhedron with a non-empty, bounded feasible set or none, so
the minimum over the finitely many assignments is attained, and by the sandwich it equals the minimum of
$c$ over $A_\varepsilon$ (Theorem 1 gives $\ge$, the construction gives $\le$). (2)–(3) are contrapositives. $\square$

**Proposition 3 (the margins cost almost nothing).** Let $\bar x\in\mathrm{cl}\,A(x_0)$ with
$c(\bar x)=\mathrm{OPT}$, support $S=\{j\in C:\bar x_j\ne x_{0j}\}$, and let $Q$ be the closure of the
polyhedral piece (cell $\cap$ rule branch) that contains $\bar x$. If some $y\in Q$ with
$\mathrm{supp}(y-x_0)\subseteq S$ satisfies all tightened rows of $Q$ with slack $\delta\ge\varepsilon$ (Slater
condition on the face), then
$$\min_{A_\varepsilon}c\ \le\ \mathrm{OPT}+\tfrac{\varepsilon}{\delta}\,\big(e(y)-e(\bar x)\big)\ \le\ \mathrm{OPT}+\tfrac{\varepsilon}{\delta}\,|C|.$$
*Proof.* $x_t=(1-t)\bar x+ty$ with $t=\varepsilon/\delta$ lies in $Q$ (convex), has slack $\ge t\delta=\varepsilon$ in every
row (slacks are affine and $\bar x$ has slack $\ge0$), so $x_t\in A_\varepsilon$. Its support is inside $S$, so
$s(x_t)\le s(\bar x)$, and $e$ is convex: $e(x_t)\le(1-t)e(\bar x)+te(y)$. $\square$

With $\varepsilon$ at most a few float32 ulps (and $\varepsilon_R,\varepsilon_F\le10^{-6}$) and data on natural units (percent, mg/dL, scores out of 100) the effect is far below
the reporting precision; empirically the MILP was never beaten by any heuristic on a query it solved to optimality.

## 5. Lower bounds, the rule-binding certificate and the price of compliance

**Proposition 4.** Let $\mathrm{LB}_R=\min_{x\in R(x_0)}c(x)$ (rule only) and $\mathrm{LB}_F=\min_{x\in B\cap L\cap F}c(x)$
(unconstrained recourse, rule ignored). Then
1. $\max(\mathrm{LB}_R,\mathrm{LB}_F)\le\mathrm{OPT}$;
2. **rule-binding certificate:** if some $x_R\in\arg\min_R c$ has $f(x_R)=1$, then $x_R$ is optimal for $A(x_0)$;
3. for any accepted heuristic output $x$: $c(x)-\mathrm{OPT}\le c(x)-\max(\mathrm{LB}_R,\mathrm{LB}_F)$ — an
   a-posteriori optimality-gap certificate that needs no rule-and-model solve; with a time limit, the MILP dual
   bound of either problem may replace its optimum;
4. the **price of compliance** $\mathrm{PoC}=\mathrm{OPT}-\mathrm{LB}_F\ge0$ is the extra cost the rule imposes
   over ordinary (model-only) recourse.

*Proof.* $A\subseteq R$ and $A\subseteq B\cap L\cap F$ give (1); (2) is (1) with $x_R\in A$; (3)–(4) follow. $\square$

**Proposition 5 (separable rules: repair is the rule optimum).** If every rule constraint involves a
single feature ($x_j\le\tau_j$ or $x_j\ge\tau_j$; lending and Pima) and there are no links, then
$R(x_0)$ is a box and the point $x_R$ that moves each *violating* feature to its threshold (and clips to the
bounds) minimises effort and sparsity simultaneously over $R$, hence minimises $c$. This is exactly the
margin-0 `repair`. So whenever the model accepts the margin-0 repair, it is the exact optimum (Prop. 4.2).

*Proof.* On a box $c$ is a sum of one-dimensional terms $|x_j-x_{0j}|/r_j+\lambda\mathbb 1[x_j\ne x_{0j}]$, each minimised
independently: by $x_{0j}$ if feasible (cost 0), else by the nearest feasible value, whose cost
$\mathrm{dist}_j/r_j+\lambda$ is unavoidable. $\square$

**Proposition 6 (one monotone constraint: greedy fill).** If the rule is a single constraint
$w^\top x\ge\tau$ with $w_j\ge0$ on its actionable features (OULAD), the minimum-effort point of $R$ at target
$\tau+m$ is obtained by filling features in decreasing order of $w_jr_j$ (fractional knapsack). The resulting
path $m\mapsto x(m)$ is continuous, piecewise linear and coordinatewise non-decreasing, and $e(x(m))$ is convex
in $m$ with slopes $1/(w_jr_j)$. (It minimises effort, not necessarily sparsity.)

## 6. When does escalation succeed?

`repair_esc` follows the repair path $x(m)$ of Prop. 5 or 6 on the grid $m_k=k\Delta|\tau|$,
$k=0,\dots,K$ ($\Delta=1/16$, $K=24$), and returns the first $x(m_k)$ that $f$ accepts. Let
$\bar m$ be the largest margin the bounds allow and $\varsigma_j=+1$ if the path increases feature $j$, $-1$ if
it decreases it.

**Theorem 7 (escalation for sign-aligned linear models).** Let the rule be separable (Prop. 5) or single
monotone (Prop. 6), and let $f$ be linear with score $g(x)=\beta^\top x+b$ such that
$\varsigma_j\beta_j\ge0$ for every feature $j$ the path moves (*the model and the rule push in the same
direction*). Then
1. $m\mapsto g(x(m))$ is non-decreasing, so the margins that $f$ accepts form an interval $[m^\*,\bar m]$ (or none);
2. escalation succeeds **iff** the end point $x(\min(m_K,\bar m))$ is accepted — a single LP/greedy fill decides it;
3. on success it returns $x(m_k)$ with $k=\lceil m^\*/(\Delta|\tau|)\rceil$, and
   $e(x(m_k))-e(x(m^\*))\le\Delta|\tau|/\min_j w_jr_j$ (Prop. 6) or $\le\Delta\sum_j|\tau_j|/r_j$ (Prop. 5);
4. escalation is nevertheless not optimal in general: for linear $f$ the optimum over $A$ is an LP with two
   active constraints whose solution may move features in a different order (by $|\beta_j|r_j$ rather than
   $w_jr_j$); Prop. 4.3 bounds the loss a posteriori.

*Proof.* (1) $g(x(m))=\sum_j\beta_jx_j(m)+b$ with each $x_j(m)$ monotone in direction $\varsigma_j$ and
$\varsigma_j\beta_j\ge0$. (2) By (1) some grid point is accepted iff the last one is. (3) Between $m^\*$ and the next
grid point the rule target grows by at most $\Delta|\tau|$; along the path one unit of rule value costs at most
$1/\min_jw_jr_j$ effort (Prop. 6), or $|\tau_j|/r_j$ per unit margin for each separable constraint. (4) Example:
two rule features with $w=(1,1)$, $r=(1,1)$ and $\beta=(1,10)$: the greedy fill raises $x_1$ first while the
cheapest acceptable point raises $x_2$. $\square$

**What fails without the assumptions.** (i) *Trees are not monotone*: a single tree that accepts only for
$x_j\in(a,b]$ with $b-a<\Delta|\tau|$ is jumped over by the grid, so escalation can fail although the path
meets $A$; and $A$ may contain only points off the path (that move non-rule features). (ii) *Misaligned
linear models* ($\varsigma_j\beta_j<0$ for some moved $j$): $g(x(m))$ can rise and then fall, so the end-point test
is only sufficient. In both cases the exact solver still decides $A(x_0)\neq\emptyset$ (Theorem 2).

## 7. Consequences for the experiments

**Corollary 8 (yield ordering).** For every query and every gated method $\mathcal M$:
accepted($\mathcal M$) $\Rightarrow A(x_0)\ne\emptyset\Rightarrow R(x_0)\ne\emptyset$. Hence
$\text{yield}(\mathcal M)\le\text{yield(exact)}+\Pr[A\neq\emptyset=A_\varepsilon]+\Pr[\text{time limit without incumbent}]\le\Pr[R\neq\emptyset]$
— the *rule-attainable ceiling*. Observed: no method ever accepted a query that the exact solver
rejected (McNemar "only baseline" = 0 in every comparison), and exact yield equals the ceiling up to the
model-infeasible share.

*Complexity remark.* For linear $f$ the MILP has only $|C|$ binaries (plus branch binaries) and is solved by
at most $2^{|C|}$ LPs — instantaneous in practice. For tree ensembles optimal recourse is NP-hard in general
(Cui et al., 2015; Kanamori et al.), which is why time limits and the dual bound of Prop. 4.3 matter on OULAD.

## 8. Empirical verification (`verify_bounds.py`, `analyze_bounds.py`)

For every query of the 104 result files `verify_bounds.py` computes $\mathrm{LB}_R$ (rule-only MILP),
$\mathrm{LB}_F$ (model-only MILP, with its dual bound), the escalation end-point test, and the margin-0 repair.
Checks: (a) $\mathrm{LB}_R\le$ exact cost and $\mathrm{LB}_F$-bound $\le$ exact cost on every query (Prop. 4.1);
(b) share of rule-binding queries and agreement with repair optimality (Props. 4.2, 5);
(c) Theorem 7.2: on linear models with aligned signs, repair_esc success $\Leftrightarrow$ end-point accepted;
(d) price of compliance per domain.

### Results (all 76 result files, 9,911 queries)

*Update after the ReLU network, the Adult / GMSC benchmarks and the v3.1 split-margin fix (179 files, 20,812 queries,
7 domains, 4 model classes):* both lower bounds remain valid on every query (0 violations); the exact solver is never
beaten where it proves optimality, never infeasible where another method found an accepted vector, and no optimal
solution is rejected by the gate. Abstentions: 3,472, of which 88 have an empty rule-feasible set and 3,384 (mostly
Adult, where the action limits do not reach the income threshold) are rule-feasible but model-infeasible. The
tables below are those of the first 76 files; per-domain tables for all files are in `results_v3/tables/`.

**(a) Bounds are valid.** $\mathrm{LB}_R\le$ exact cost on every query, and the model-only dual bound
$\le$ exact cost on every query where it was computed (0 violations each).

**Abstention (Theorem 2).** The exact solver abstained on 70 queries: 68 have an empty rule-feasible set
(certified without the model — no recourse exists for any model) and 2 are rule-feasible but have no
acceptable vector for the given model.

**(b) Rule-binding queries and repair optimality.**

| Domain | Model | Rule-binding (OPT = LB_R) | Margin-0 repair optimal when f accepts it (Prop. 5) | Repair+esc optimal |
|---|---|---|---|---|
| HMDA (separable) | lr / rf / cat | 100 / 99.9 / 98.7 % | 100 % | 100 / 100 / 98.8 % |
| HMDA_OR, HMDA_S | all | 98–100 % | (not separable) | 96–100 % |
| PIMA (separable) | lr / rf / cat | 61 / 52 / 44 % | 100 % | 61 / 52 / 44 % |
| OULAD aligned | lr / rf / cat | 25 / 79 / 74 % | (single constraint) | 11 / 22 / 18 % |
| OULAD floor | lr / rf / cat | 15 / 25 / 39 % | | 15 / 14 / 23 % |

Proposition 5 holds without exception: on lending and Pima, whenever the model accepts the margin-0
repair it is the exact optimum. This explains why repair is near-optimal on lending (the rule is the binding
requirement on ~99 % of queries) and not on Pima (the model binds on about half). On OULAD the rule-only
optimum *value* is often the true optimum (74–79 % on aligned tree models) but repair+escalation reaches it
on only 18–22 %.

**Degenerate rule optima (tested, not a fix).** We tested whether a *sparsity-aware repair* closes this gap:
`exact.repair_sparse` solves the rule-only MILP (min effort + 0.5·sparsity over $R(x_0)$, no model) and escalates
the margin on the same grid (conditions `repair_sparse0`, `repair_sparse`). On the 618 OULAD rule-binding
queries it returned a rule-optimal vector every time (cost = $\mathrm{LB}_R$), yet the model rejected it on 61 %
(lr 24–40 %, CatBoost 60–64 %, RF 58–79 %). The reason is degeneracy: the OULAD rule weights every assessment
equally on the same 0–100 scale, so the minimum-cost compliant actions form a large tie set, and *only the
model* can tell which of them it accepts — Proposition 4.2 needs *some* rule optimum to be accepted, and a
model-free method has no way to pick it. Across all domains sparse repair matched repair+escalation on
lending and Pima (where the rule optimum is unique, Prop. 5), was slightly closer to optimal on HMDA_OR and
OULAD-CatBoost aligned (optimal on 27.5 % vs 17.5 %), and slightly worse elsewhere on OULAD (yield 92–95 %
vs 91–96 %; its escalation path is not monotone, so Theorem 7 does not apply). It is never better than the
exact solver (McNemar "only baseline" = 0). Conclusion for the paper: when rule optima are degenerate the
choice among them must be made jointly with the model, which is precisely what the exact formulation does.

**(c) Theorem 7.2 (escalation end-point test).** On every linear-model query of the separable (HMDA, Pima)
and single-constraint (OULAD) domains, repair+escalation succeeded exactly when the end point of the path was
accepted: agreement 100 % (HMDA 492, Pima 427, OULAD 600 queries; 0 disagreements in either direction). On
OULAD seed 0 the logistic coefficient of Test_7 is slightly negative (−0.03), so the alignment assumption fails
for paths that move Test_7; the end-point test still agreed on all 60 queries, i.e. the assumption is sufficient,
not necessary.

**(d) Price of compliance (OPT − LB_F, both proven optimal).**

| Domain | lr | rf | cat |
|---|---|---|---|
| HMDA | +64 % | +15 % | +16 % |
| HMDA_OR | +83 % | +26 % | +27 % |
| HMDA_S | +66 % | +15 % | +16 % |
| PIMA | +65 % | +61 % | +57 % |
| OULAD aligned | +1.6 % (76 % of queries free) | n/a* | n/a* |
| OULAD floor | +0.2 % (88 % free) | n/a* | n/a* |

\*Model-only MILPs on OULAD trees rarely close within 20 s (no rule to prune the search); only seed 0 was run and
too few queries were proven optimal (3–36) to report. Reading: ordinary (model-only) recourse would be
15–83 % cheaper on lending and ~60 % on Pima, but its optimum violates the rule on 98–100 % of lending and 86–92 % of Pima queries — the cost
of compliance is real and mostly unavoidable; on OULAD with a linear model the rule rarely adds cost.

**(e) A-posteriori gap certificate (Prop. 4.3).** $c(x)-\max(\mathrm{LB}_R,\mathrm{LB}_F)$ equals the true gap
on 100 % of lending and OULAD-lr queries (so the heuristic's sub-optimality is certified without the joint
solve), 58–70 % on Pima and 36–84 % on OULAD trees; on average the certificate overstates the true gap by
0.04–0.15 cost units.

Tables: `results_v3/tables/theory_checks_v3.md`, `rule_binding_v3.csv`, `escalation_theorem_v3.csv`,
`price_of_compliance_v3.csv`, `gap_certificate_v3.csv`; per-query data in `results_v3/bounds/`.

