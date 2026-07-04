# Preregistrations: the two novel branches (per per-branch-subcommittee policy)

Each branch got a subcommittee (designer + auditor). Both auditors independently reached the same
meta-lesson: the naive "does the extended phase survive?" binary is FOREGONE; the real result is a
SCALING/THRESHOLD object, and each needs well-posedness fixes + a killer control against the
"you just changed the ensemble" collapse. (Branch B ran on Opus -- Fable's safeguard blocked the
detailed-balance prompts twice.) Citations are the seats' (verified); re-verify before formal use.

## BRANCH A -- OFF-MANIFOLD: does local causality tame crumpling without the manifold scaffold?

**Construction.** 2+1D locally-causal CDT ensemble (Ambjorn-Jurkiewicz-Loll; (3,1)/(2,2)/(1,3)
tets, s/t edge labels, Regge action, couplings k0,k3,Delta). Add a tunable penalty mu on a defect
measure D = sum_v |2-chi(lk v)| + 2(comp(lk v)-1) + sum_e (circle-comps(lk e)-1); D=0 iff simplicial
manifold. Weight exp(-S_Regge - mu*D). mu=inf = pure CDT (CALIBRATION target: Jordan-Loll extended
de Sitter, PRD 88 044055); mu=0 = pure causal pseudomanifold. Relaxation ladder R0(inf)->R3(mu-scan).
Add a pinch/unpinch move to reach the enlarged class.

**PREREGISTERED HEADLINE (auditor's reframe -- NOT the foregone binary):** the manifoldness
THRESHOLD mu_c(N) and its finite-size scaling.
- **PUBLISHABLE POSITIVE:** mu_c(N) stays FINITE as N->inf ==> local causal labels tame the
  log-diameter/singular-vertex attractor WITHOUT a manifold scaffold (a statement about causal-graph
  ensembles underivable on-manifold; bears on whether CDT-Horava is a property of causality vs the
  triangulation class).
- **PUBLISHABLE NEGATIVE:** mu_c(N) DIVERGES (e.g. ~log N) ==> manifoldness is a fine-tuned,
  measure-zero input to CDT (clean negative), only licensed if a full k0/Delta scan at mu=0 finds NO
  extended region anywhere.
- Secondary observables (not pass/fail): (d_H, nu) with d_H from ball growth B(r)~r^d_H and diameter
  D~N3^nu (nu=1/3 extended), z(mu).

**WELL-POSEDNESS (mandatory before any run -- auditor):** the causality condition (circling a
spacelike hinge crosses 2 lightcones) and the Regge deficit angle (2pi - sum theta) are UNDEFINED
off-manifold (no cyclic link order; no single 2pi wedge). Preregister an off-manifold generalization
(per-sheet cone condition OR an order-theoretic no-closed-timelike-edge-loop condition; a per-sheet
deficit convention) that reduces to Jordan-Loll at mu=inf. Fix d=3; fix the complex class.

**CONTROLS:** hot/cold-start agreement per (N,mu); autocorrelation bounded; replica overlap P(q)
single-peaked/self-averaging; structure factor S(k) no k!=0 peak; transition order (double-peak
histograms + Lee-Kosterlitz); max-vertex-order scaling p_max~N^alpha (alpha>0.8 = singular-vertex
condensation = crumpled) as an INDEPENDENT crumpling discriminator so "survival" needs d_H~3 AND
non-extensive degree. Two structurally different move mixtures must agree (ergodicity off-manifold is
unproven -- stated as the paper's limitation, not a fixable nuisance).

**NOVELTY vs prior art (narrow but real = the threshold's finite-vs-divergent scaling):** off-manifold
graph d_H already exists (Trugenberger combinatorial QG, arXiv:1610.05934; Kelly-Trugenberger
arXiv:1811.12905); action-suppression of Kleitman-Rothschild orders exists (Loomis-Carlip
arXiv:1709.00064; Carlip et al. arXiv:2209.00327); tunable causality relaxation in 2D CDT exists WITH
a coupling-scaling caveat (Ambjorn-Loll-Westra-Zohren arXiv:0709.2784); quantum graphity crumpled
(Konopka-Markopoulou-Severini arXiv:0801.0861); degenerate triangulations (Bilke-Thorleifsson). So
preregister mu_c(N) as the headline, not the endpoints.

**MINIMAL FIRST IMPLEMENTATION:** refactor referee_3d.py link census -> local incremental
delta_defect(star); in cdt_experiment.py replace the manifold veto with exp(-mu*Delta D) + pinch/
unpinch; calibrate estimators on Freudenthal/_lat3 controls. First point: N3 in {4k,8k,16k}, T=32,
mu in {inf,0}, >=100 decorrelated configs, hot+cold; deliver log-log D vs N3 (with N^1/3 and log N
references) + p_max(N).

## BRANCH B -- NONEQUILIBRIUM: does the extended phase survive irreversible local dynamics?

**Construction.** Same CDT state space + action; replace the global-sweep Metropolis with an
ASYNCHRONOUS event-driven (Gillespie) local process. Break detailed balance with an irreversible
chirality factor g(orientation)=exp(+/-epsilon) on foliation-directed expand/contract moves -- a
NON-GRADIENT current source that CANNOT be folded into a redefined action.

**CONFIRM DB BROKEN (mandatory):** (a) Kolmogorov cycle test -- exhibit a closed move-loop with
prod(forward rates)/prod(reverse) = exp(2 epsilon * net chirality) != 1, vanishing as epsilon->0;
(b) measured nonzero steady-state cyclic current J in a coarse observable plane, sign-locked to
epsilon, ~epsilon at small drive. NULL CURRENT ==> NO RESULT.

**PREREGISTERED HEADLINE (auditor's reframe -- a static-exponent shift alone is FOREGONE / "different
ensemble"):** a TWO-PART claim: (i) the STATIC extended-geometry order parameter (de Sitter volume
profile; dimensionful d_H) SURVIVES in the NESS (robustness -- the extended phase is not an artifact
of detailed balance); AND (ii) the RELAXATIONAL DYNAMIC exponent z_dyn (tau ~ xi^z_dyn of a named
order parameter) DIFFERS from equilibrium-CDT z_dyn beyond error, shown UNIVERSAL (robust across
DB-breaking rate rules) and placed relative to the Hohenberg-Halperin (RMP 49 435, 1977) /
directed-percolation (Janssen-Grassberger) / active-matter taxonomies. The NEGATIVE (extended
geometry does NOT survive irreversible dynamics) is pre-committed as equally publishable.

**THE KILLER CONTROL (auditor):** for any observed z_NESS, attempt to reproduce it with an
EQUILIBRIUM DB run scanning the CDT asymmetry coupling Delta. If some Delta* jointly matches z_NESS
AND d_H AND the full volume profile, the "nonequilibrium" claim COLLAPSES to a coupling shift and is
WITHDRAWN. The result stands only if NO equilibrium coupling jointly reproduces the NESS observables
while J != 0. Plus: epsilon->0 must recover equilibrium CDT exactly (calibration gate); unique steady
state (hot/cold/equilibrium-seeded starts converge, J and z converged not drifting).

**WELL-POSEDNESS (auditor):** "no global sweep + fixed volume/topology/causality" is in tension --
specify exact (paired non-local moves) vs soft (fluctuating-volume ensemble) volume constraint; fully
specify + seed the async scheduler and conflict resolution (different schedulers = different steady
states = different exponents); argue + demonstrate uniqueness of pi_ss.

**GLASS/ABSORBING GUARDS:** monitor the minimal-triangulation absorbing state (survival prob vs
event-time; an absorbing DP transition in epsilon is a distinct, also-publishable outcome, labeled as
such); replica overlap; aging/FDT VIOLATION is REQUIRED as the NESS fingerprint (X != 1) BUT with
time-translation invariance restored in steady state (else glass); structure factor keeps the
de Sitter low-k envelope.

**MINIMAL FIRST IMPLEMENTATION:** fork cdt_experiment.py -> cdt_async.py (Gillespie driver + active-
site queue + g-factor, one epsilon), seed from a thermalized equilibrium extended config, reuse the
estimators unchanged. First point: N3 ~ 8-16k, one epsilon; deliver the triple {epsilon, J-estimate,
d_H_NESS vs d_H_eq} + the Kolmogorov cycle ratio (with its epsilon->0 vanishing check).

## Shared meta-lesson (both auditors)
On each branch the binary is foregone; the result is a SCALING object (mu_c(N) finite-vs-divergent;
z_dyn deviation + static survival) protected by a control that rules out "you changed the ensemble"
(the k0/Delta scan at mu=0; the Delta-scan reproduction test). Matching CDT is the entry ticket, never
the result. Both minimal first implementations are small (one driver swap each) and are the next build.
