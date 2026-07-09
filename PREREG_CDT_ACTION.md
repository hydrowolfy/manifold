# PREREGISTRATION -- STAGE 2 (exotic): can a NON-LOCAL action/measure term select the flat joint 3-manifold?

Committed BEFORE the lambda scan (discipline LESSONS 13). Runner: cdt_frontier3_run.py
(cdt_frontier2_run.py core VERBATIM + two non-local terms; DB + manifold verified in --selftest).
Frozen benchmark and primary config are fixed here and MUST NOT be changed post-hoc.

## 0. Question and prior

STAGE 1 (REPORT_CDT_TOPOLOGY.md) proved the 2+1D d_H-d_s wall has a topology-INDEPENDENT root:
(i) the differential lock dN22 = -4 dN0 (spatial-vertex density and f22 are ONE DOF at fixed
counts), and (ii) an ENTROPIC / diffusion-geometry root -- the causal ensemble fills the only free
DOF (the degree distribution) with hubs. Crucially, stage 1 also showed the flat joint 3-manifold
EXISTS in the ensemble (an exact flat calibrant reproduces the benchmark) but is ENTROPICALLY
UNSELECTED. Every LOCAL lever (k0, k22 in c6; a per-vertex one-sided hub cap in c7) only slides
BOTH dimensions along the SAME anticorrelation line -- d_H up <=> d_s down -- crossing the benchmark
~10x apart, never jointly. This is a SELECTION/measure problem, not an existence problem.

STAGE 2 asks the one question left inside 2+1D: can a genuinely NON-LOCAL term -- one that SEES and
penalizes GLOBAL structure (which no per-simplex/per-vertex term can) -- re-weight the measure to
SELECT the flat joint 3-manifold that is already present, pulling BOTH d_H and d_s onto benchmark
with a UNIFORM (un-condensed, low-CV) profile?

REGISTERED PRIOR (honest): after four failed in-2+1D levers incl. topology, H_reparam (below) is the
strong prior -- even a non-local term likely reparameterizes the same tradeoff and the real escape is
DIMENSIONAL (3+1D). A joint pass here would be a genuine breakthrough; a clean failure sharpens the
"must go 3+1D" conclusion. Either outcome is a real result.

## 1. Candidate non-local terms (added to S = k3 N3 - k0 N0 + k22 N22 + eps(N3-V)^2)

NL-P (non-local profile-uniformity; the flagship non-local term):
    S_P = lam_p * sum_t ( n(t) - nbar )^2 ,   n(t) = #spatial triangles in slice t,  nbar = N_stris/T.
  NON-SEPARABLE across the foliation (nbar couples every slice); minimized only by a GLOBALLY uniform
  spatial-volume profile. This is exactly "couple the spatial-volume profile across slices to penalize
  condensation / re-weight toward uniform slices" -- unexpressible by any local per-simplex weight.
  Only (2,6)/(6,2) change n(t) (by +-2 in one slice); (2,3)/(3,2)/(4,4) leave the profile fixed.

NL-D (symmetric global degree-distribution counter-term; the entropic-hub counter-term):
    S_D = lam_d * sum_v ( deg_v - D0d )^2 ,   D0d = 14 (the flat-torus degree).
  Penalizes hubs AND under-connected vertices, driving the FULL degree distribution to the flat delta
  at 14 -- strictly STRONGER than campaign 7's one-sided cap sigma*sum max(0,deg-D0)^2, which only
  capped the high tail (never reached the flat signature). Directly offsets the entropic hub preference.

Combinations scanned: NL-D + NL-P; NL-P + k22 (anti-condensation on the d_s lever); NL-D + NL-P + k22.

DEFERRED (designed, not run at V=6000 unless a hint appears): a spectral/return-probability term
lam_s * (P_return(t*) - P_flat)^2 evaluated per-SWEEP as a multicanonical reweight -- genuinely
non-local on the diffusion operator but O(N*t) per evaluation, and its DB requires a sweep-level
Hastings correction. Justification for deferral: cost + the registered prior; escalate only on a hint.

Detailed balance: both implemented terms are STATE FUNCTIONS; proposals are unchanged, so Metropolis
on exp(-dS_total) preserves DB. The per-move deltas equal S(new)-S(old) exactly and reverse=-forward
-- VERIFIED against brute force over all 5 move types in --selftest (2500+ moves). Manifold preserved
(census bad=0 asserted every snapshot).

## 2. Frozen benchmark (size-matched flat T^3, m=10, seed-averaged 8 estimator seeds, seedbase 100)

    d_s(8-24) = 3.135 +- 0.172   (primary d_s window)
    d_s(16-48)= 3.014 +- 0.405   (secondary, noisy)
    d_H(2-6)  = 2.473 +- 0.000   (deterministic; vertex-transitive torus)
Reproduced this session to the digit via remeasure.py --torus 10 --seeds 8 --seedbase 100. This is
the ONLY scoring target (LESSONS 1-2: never the continuum 3.0; always seed-averaged).

## 3. Primary config and measurement protocol

Config: V = 6000, T = 12, k0 = 2.0, k22 = 0.0 (matched to the c7 / stage-1 baseline), MC seed 0.
Warm-start each lambda point from the k0=2 baseline equilibrium; re-equilibrate to a PLATEAU
(monitor f22, profile CV, both dims across >= 300 sweeps -- NOT a warm-start transient; LESSONS 6,7,14).
Score seed-averaged: d_s over >= 8 estimator seeds (windows 8-24 primary, 16-48 secondary), d_H over
>= 4 seeds (window 2-6 primary), via remeasure.py (scan seedbase 100; independent verification of any
candidate at seedbase 200). Report deg mean/sd/max and profile CV alongside every point.

## 4. Preregistered JOINT GATE (a pass must meet ALL of G1-G5)

  G1  census bad = 0                          (valid simplicial 3-manifold)
  G2  d_H(2-6) ratio >= 0.90                  (d_H >= 2.226)
  G3  | d_s(8-24) - 3.135 | <= 0.20           (d_s in [2.935, 3.335])
  G4  NO condensation: profile CV <= 0.35 AND non-drifting AND min/mean >= ~0.5 (stalk = 0)
  G5  GENUINE SELECTION (anti-triviality, NEW this stage):
        (a) stable EQUILIBRIUM -- d_s, d_H, f22, CV plateau over >= 300 sweeps (seed-averaged), and
        (b) NOT a frozen delta-projector -- the pass is reached at a MODERATE coupling where the term
            is a bounded perturbation, deg_sd remains > 0, and the state re-equilibrates (fluctuates),
            i.e. the ENSEMBLE selects flat, we do not hand-place it via lambda -> infinity.
  JOINT PASS  ==  G1 AND G2 AND G3 AND G4 AND G5.
G2-G4 are IDENTICAL to the campaign-7 gate (no threshold shopping); G5 is added because a non-local
term strong enough to force flatness could otherwise trivially "pass" by projection.

## 5. Decision rules (hypotheses, registered)

  H_select   -- some lambda (single or combined) meets G1-G5: the non-local term SELECTS the flat
                joint 3-manifold. => BREAKTHROUGH. Escalate to Kirk's WSL box for confirmation:
                seed-averaged repeat at seedbase 200, a second MC seed, and V=12000.
  H_reparam  -- the term moves d_H and d_s but their benchmark crossings stay SEPARATED (no lambda
                meets G2 and G3 together), OR any joint-looking point fails G4 (condensation) or G5
                (frozen/projector). => wall holds against the non-local term; escape is dimensional.
  H_null     -- the term does not move the observables (registered prediction for NL-P on the already-
                uniform baseline: it should be a near-no-op there; its role is the k22 combo).

ESCALATION TRIGGER (compute discipline): run the WSL box ONLY if a V=6000 point meets G1-G5, OR lands
within 0.05 of BOTH G2 and G3 simultaneously on a low-CV state. Otherwise the V=6000 sandbox verdict
stands (consistent with the campaign 5-7 V-independence).

## 6. Preregistered scan grid (may be pruned toward the interesting region, not extended past it)

  NL-D alone:   lam_d in {0.003, 0.008, 0.02, 0.05}      (calibrate to move deg_sd across its range)
  NL-P alone:   lam_p in {0.02, 0.1}                      (negative control on the uniform baseline)
  NL-P + k22:   (lam_p in {0.1}) x (k22 in {0.5, 1.0})    (does anti-condensation de-collapse k22's d_s pass?)
  NL-D + NL-P:  best lam_d x lam_p in {0.1}               (remove hubs AND hold uniform: the joint shot)
  NL-D+NL-P+k22: best combo x k22 in {0.5}                (all three: hubs down, uniform, d_s lever)
Any point that appears to approach G2 and G3 together is repeated at a second seedbase and longer
equilibration before being called a pass (LESSONS 6/14: transient crossings are not convergence).
