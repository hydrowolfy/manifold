# Preregistration: does 3+1D causal CDT reach a JOINT (d_H AND d_s) 4-manifold?

Date: 2026-07-09 (STAGE 3, "dimensional escape"). Registered BEFORE any 3+1D causal
production headline. STAGE 1 (topology) and STAGE 2 (non-local action) closed every
in-2+1D lever: the 2+1D d_H-d_s wall survives aspect, k0 x k22, hub cap, spatial
topology, and non-local profile/degree terms -- six lever families, one wall, rooted
in the per-slice Euler lock dN22 = -4 dN0 (spatial-vertex density and the (2,2)
fraction are ONE DOF). The sole remaining escape is DIMENSIONAL. This document fixes
the scoring, benchmark, gate, hypotheses, and decision rules for the 3+1D test so the
headline cannot be tuned after the fact.

## 0. The cheap-first gate (PART A) -- already resolved, recorded here for the record

Before any Metropolis build, the STAGE-3 gate was the on-paper question: does 3+1D
have an analogue of the 2+1D lock dN22 = -4 dN0? VERDICT (cdt_4d_lock_check.py, all
checks pass): **NO. Path open.** Root: a closed 2-manifold slice has f-vector DOF = 1
(F = 2V - 2chi locks the top-simplex count to V), but a closed 3-manifold slice has
f-vector DOF = 2 (2F=4S and V-E+F-S=0 leave V AND S=#tetrahedra free). So in 3+1D the
"more spatial" count N41 = 2 sum_t S_t is NOT locked to N0 = sum_t V_t: spatial-vertex
density and the timelike-simplex fraction are TWO independent DOF. This matches the
standard 4D CDT action carrying two independent bulk couplings (kappa_0 <-> N0 and
Delta <-> the (4,1)/(3,2) split) and an extended de Sitter phase. Part A is the
decisive structural result; the sections below preregister the empirical confirmation.

## 1. Estimators, windows, benchmark (frozen)

- Estimators: repo referee `ball_growth_dim` (d_H) and `lazy_rw_sdim` (d_s, lazy-RW
  return prob) used VERBATIM (tooling/referee_2d_scaling.py). Graph = vertex 1-skeleton.
- Error bars: mean over K>=8 ESTIMATOR seeds; sigma = seed sd (d_H is deterministic on
  the vertex-transitive torus, sd 0; both averaged for uniformity). LESSONS 1-2 carried
  forward: score vs the exact finite-size benchmark, NEVER the continuum 4.0.
- Benchmark: exact flat 4-torus, Coxeter-Freudenthal-Kuhn triangulation of (Z/m)^4,
  size-matched by N0. Validity PROVEN: census bad=0 (every tetrahedron in exactly 2
  pentachora), chi=0, Dehn-Sommerville exact, uniform vertex degree 30. It is also a
  valid FOLIATED causal state (Kuhn T^4 sliced along one axis: spatial slices are Kuhn
  T^3, types (4,1):(3,2):(2,3):(1,4) = 1:1:1:1) -- i.e. the flat joint 4-manifold is a
  genuine member of the causal ensemble (the calibrant). Benchmark numbers (8 seeds),
  FROZEN here:
    m=6 (N0=1296): d_s(8-24)=4.117 +- 0.402 | d_H(2-6)=2.656 (det)
    m=8 (N0=4096): d_s(8-24)=4.491 +- 0.193, d_s(10-30)=4.354 +- 0.285 | d_H(2-6)=2.840,
                   d_H(3-8)=2.482 (det)
  For contrast the flat T^3 benchmark reads d_s(8-24)~3.13, d_H(2-6)~2.47: d_s cleanly
  separates 4D (~4.1-4.5) from 3D (~3.1); it is the discriminating observable.
- Primary d_s window: 8-24 (matched-benchmark ~4.1-4.5). Primary d_H window: 2-6.
  Secondary: d_s 10-30, d_H 3-8.

## 2. The joint gate (PASS criteria, frozen)

A causal 3+1D configuration (fixed T, kappa_0, Delta, at volume N4) "jointly reaches a
4-manifold" iff ALL of:
  (G1) census bad = 0 in the measured snapshot(s) (every tetrahedron in exactly 2
       pentachora; every pentachoron foliated/typed; spatial slices closed 3-manifolds).
  (G2) d_H(2-6) ratio to the matched-N0 T^4 benchmark >= 0.90.
  (G3) |d_s(8-24) - matched-N0 T^4 benchmark| <= 0.30 (~1.5x the combined benchmark sd;
       and CLEARLY above the T^3 value 3.13 -- d_s must read 4D, not 3D).
  (G4) equilibrium + no condensation: spatial-volume profile CV plateau (non-drifting),
       stable over >= 200 sweeps (LESSONS 6/14 carried forward from 2+1D).
The de Sitter (C) phase of standard 4D CDT is expected to pass this gate; phases A/B
(crumpled / branched-polymer) fail it. The frontier question is whether the causal
measure SELECTS a gate-passing configuration -- which 2+1D provably never did.

## 3. Hypotheses (each with a pre-set confirm/refute)

H_open (PRIMARY, favored by Part A). 3+1D causal CDT has a region of (kappa_0, Delta)
   whose equilibrium ensemble meets the full joint gate (Sec 2): d_H AND d_s both on
   the T^4 benchmark, census-clean, non-condensing. The two-DOF structure (Part A) is
   the mechanism -- Delta independently tunes the timelike fraction that N0 cannot fix.
   CONFIRM: a (kappa_0, Delta, T, N4) meeting G1-G4, surviving independent re-measure.
   REFUTE: across the scanned (kappa_0, Delta) plane, every point that brings d_s onto
   the T^4 benchmark drops d_H ratio < 0.90 or condenses (a 2+1D-style reparameterized
   tradeoff reappearing in 3+1D despite the two DOF).

H_exist (already CONFIRMED, recorded). The flat joint 4-manifold EXISTS as a valid
   census-clean state of the 4D causal ensemble (the flat foliated T^4 calibrant) and
   the estimators read it as joint-4 (d_s 4.1-4.7, d_H 2.66). CONFIRM = a census-clean
   foliated T^4 reading the benchmark band (DONE, cdt4_causal.py). This is the 4D analogue
   of the 2+1D calibrant; the OPEN question H_open is whether it is entropically SELECTED.

H_phase. If a gate-passing region exists, its volume profile is EXTENDED (de Sitter,
   4D blob across the time extent), not a stalk/collapse (contrast the 2+1D alpha
   "d_s pass" which was a condensation; LESSONS 23). CONFIRM: profile CV low + stable,
   volume spread across slices. REFUTE: the d_s=benchmark region is a condensate.

## 4. Experiments (pre-specified)

E1 (production de Sitter sweep, H_open): build the full ergodic 4D CDT move set
   ((2,4)/(4,2) [validated: cdt4_run.py] + (3,3) + the vertex-changing moves needed for
   ergodicity), warm/grow to target N4, scan (kappa_0, Delta) around the literature de
   Sitter point (e.g. near (2.2, 0.6)); at each point re-equilibrate (monitor N0/N41
   split AND profile CV to a plateau, >=200 sweeps past settling); measure d_H, d_s with
   8 estimator seeds. Volume fixed by the standard N4-quadratic term. Uncapped run on
   Kirk's WSL box (LESSONS 17); checkpoint resumably (LESSONS 8-11).
E2 (phase map, H_phase): at the gate-passing point, dump the spatial-volume profile
   N3^SL(t); classify extended vs collapsed (profile_dump analogue).
E3 (negative control): a point in phase A or B (large kappa_0 / negative Delta) must
   FAIL the gate -- confirms the estimators + gate discriminate phases, not just size.

## 5. Decision rules (which verdict we land)

- WALL BROKEN (the Stage-3 headline): a (kappa_0, Delta) region passes G1-G4 and
  survives re-measure -> "3+1D causal CDT reaches the joint (d_H AND d_s) 4-manifold
  that 2+1D provably could not; the escape was dimensional, and the two-DOF unlock
  (Part A) is the mechanism." Report with full error bars + finite-size caveats.
- STRUCTURAL-ONLY (weaker, still positive): Part A (two DOF) + H_exist (calibrant is a
  valid census-clean joint-4 causal state) hold, but a full production sweep is not
  completed in-session -> report the structural break + calibrant as the Stage-3 result
  and preregister the production sweep as the pending confirmation. (Honest landing if
  the full ergodic move set / long run is not finished here.)
- SURPRISE NEGATIVE (low prior): the two DOF exist but the causal measure still fails
  the joint gate in 3+1D (a reparameterized tradeoff survives the extra DOF). Would be a
  major result -- characterize why (which of G2/G3/G4 fails, and the (kappa_0,Delta) map).

Scoring, benchmark, windows, and gate above are frozen as of this commit.
