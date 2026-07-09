# Preregistration: the 3+1D causal CDT de Sitter (kappa_0, Delta) production scan

Date: 2026-07-09. STAGE 3 PART C (the production sweep preregistered as E1 in
PREREG_CDT_4D.md). Registered BEFORE any de Sitter production headline. Part A (two
independent DOF: no 3+1D analogue of dN22=-4dN0) and Part B (the flat foliated T^4 is
a validated census-clean joint-4 causal calibrant) are done (REPORT_CDT_4D.md). This
document fixes the move set, action, gate, phases, and decision rules for the dynamical
test -- does the causal MEASURE dynamically SELECT an extended de Sitter 4-geometry --
so the verdict cannot be tuned after the fact.

## 0. What was built to enable this (recorded; validated in-session)

The full ergodic 4D CDT move set, on the validated cdt4_run.py core (cdt4_prod.py):
  (2,4)/(4,2)  dN0=0    dN4=+/-2   timelike-tetrahedron flip           [cdt4_run.py]
  (3,3)        dN0=0    dN4=0      triangle flip (self-inverse)         [NEW]
  (4,6)/(6,4)  dN0=0    dN4=+/-2   spatial (2,3) flip thru both sandwiches [NEW]
  (2,8)/(8,2)  dN0=+/-1 dN4=+/-6   spatial-tetrahedron vertex insert/remove [NEW; the N0 DOF]
Each is foliation-preserving; each was validated in cdt4_prod_selftest.py by EXACT
forward/reverse round-trips (complex byte-identical after move+inverse), reverse action
delta = -forward, and census bad=0 + full typing throughout. The maintained simplex
counters were checked equal to a from-scratch recount after every move. ERGODICITY was
demonstrated empirically (N4 AND N0 each driven up and down; timelike fraction tunable
0.26-0.55; independent walks mix; census-clean throughout) and rests otherwise on the
standard AJL 4D CDT result that this move set is ergodic in the foliated ensemble.
Detailed balance of the full Metropolis (including the vertex-changing Jacobian) was
verified numerically: the balance equation (1/K_f) A_f exp(-S) = (1/K_r) A_r exp(-S')
holds to 0.00e+00 over 828 (move,state) pairs at random couplings (cdt4_scan.py --db-check).

## 1. Action, ensemble, estimators (frozen)

- Action (standard 4D CDT Regge form):
    S = -(kappa0 + 6 Delta) N0 + kappa4 N4 + Delta (2 N41 + N32) + eps (N4 - N4t)^2
  kappa0 couples the vertex number N0; Delta couples the (4,1)/(3,2) split (the timelike
  fraction) -- the SECOND independent axis 2+1D never had (Part A). The eps-quadratic
  fixes the 4-volume near N4t (auto-tuning the effective kappa4); the scan is at ~fixed
  N4 -- the standard way to map the CDT phase diagram. Metropolis weight exp(-S).
- Acceptance (DB-verified): A = min(1, (K_fwd/K_rev) exp(-dS)); uniform move-type
  selection makes reverse-pair proposal probabilities cancel; K = exact live pick-set count.
- Estimators: repo referee ball_growth_dim (d_H) and lazy_rw_sdim (d_s), used VERBATIM
  (bundled stdlib-only in cdt4_prod.py), on the vertex 1-skeleton. K>=8 estimator seeds;
  sigma = seed sd. LESSONS 1-2, 38: score d_s/d_H vs the finite-size flat-T^4 benchmark,
  NEVER the continuum 4.0.
- Benchmark (frozen, PREREG_CDT_4D Sec 1): flat Kuhn T^4.
    m=6 (N0=1296): d_s(8-24)=4.117 +- 0.402 | d_H(2-6)=2.656 (det)
    m=8 (N0=4096): d_s(8-24)=4.491 +- 0.193, d_s(10-30)=4.354 +- 0.285 | d_H(2-6)=2.840
  Flat T^3 for contrast: d_s(8-24)~3.13, d_H(2-6)~2.47. d_s cleanly separates 4D (~4.1-4.5)
  from 3D (~3.1) and is the DISCRIMINATING observable.
- Primary windows: d_s 8-24, d_H 2-6. Secondary: d_s 10-30, d_H 3-8.

## 2. The three phases (frozen definitions) and what "de Sitter reached" means

Standard 4D CDT has three phases in (kappa0, Delta):
- Phase A (crumpled): no extended geometry; d_H large/ill-defined, spatial slices maximally
  connected; NOT de Sitter.
- Phase B (branched-polymer / bifurcation, small Delta): the 4-volume collapses to a thin
  stalk in time; the spatial-volume profile N(t) is a single spike / degenerate; d_H -> ~2
  (polymer), NOT de Sitter.
- Phase C (de Sitter, extended, Delta above the A-C/B-C lines, e.g. near (2.2, 0.6)): a
  smooth extended 4-geometry. THIS is the target.

"DE SITTER REACHED" (phase C) PASS gate -- ALL of:
  (G1) census bad = 0 in the measured snapshot(s); every pentachoron foliated/typed;
       spatial slices closed 3-manifolds.
  (G2) EXTENDED volume profile: N(t)=N3^SL(t) is a single smooth hump spanning most of the
       time extent, fitting N(t) ~ cos^3( (t - t0) / (B N4^{1/4}) ) (R^2 >= 0.8 over the
       extended support), NOT a stalk/collapse (phase B) and NOT flat/uniform-maximal (A).
  (G3) d_H(2-6) ratio to the matched-N0 T^4 benchmark >= 0.90 (d_H -> 4 at large scale,
       scored vs the finite-size benchmark, not 4.0).
  (G4) d_s flow consistent with de Sitter: d_s in the IR (long window) reads ~4 (within 0.30
       of the matched T^4 benchmark and clearly > the T^3 value 3.13), FLOWING DOWN to ~2 in
       the UV (short window) -- the expected dynamical-dimension reduction, EXPECTED PHYSICS.
  (G5) equilibrium + no drift: N0/N41 split and profile CV on a non-drifting plateau over
       >= the measurement window (LESSONS 6/14).
Phases A/B fail this gate (A fails G2/G3 by over-connection; B fails G2 by collapse).

## 3. Hypotheses (pre-set confirm/refute)

H_deSitter (PRIMARY, favored by Part A + known 4D CDT phenomenology). There is a
  (kappa0, Delta) region whose equilibrium ensemble meets G1-G5: an extended de Sitter
  4-geometry with the cos^3 profile, d_H->~4, d_s flowing 4->2. Mechanism: the two-DOF
  structure (Part A) lets Delta tune the timelike fraction independently of N0.
  CONFIRM: a (kappa0, Delta) point meeting G1-G5, surviving independent-seed re-measure.
  REFUTE: across the scanned plane, every point that brings d_s onto the T^4 benchmark
  either collapses (phase B stalk) or over-connects (phase A) -- the SURPRISE NEGATIVE.

H_phase_map. The scan resolves the three phases and the transition lines (A/B/C), with the
  observables (N0/N4, f_timelike, profile CV, d_H, d_s) discriminating them -- not merely
  tracking size. E3 negative control: a phase-A or phase-B point must FAIL the gate.

## 4. Experiments (pre-specified)

E1 (production scan): full ergodic move set (built), grow/seed to target N4t, scan a
  (kappa0, Delta) grid across A/B/C, at each point re-equilibrate (monitor N0/N41 split +
  profile CV to a plateau) then measure d_H, d_s (8 seeds), N(t) profile. Uncapped WSL box
  (LESSONS 17). Checkpoint resumably every sweep (LESSONS 8-11).
E2 (profile classification): at the candidate de Sitter point dump N3^SL(t); fit cos^3;
  classify extended (C) vs stalk (B) vs flat (A).
E3 (negative control): a deep phase-A or phase-B point must FAIL the gate.

## 5. Decision rules (which verdict we land)

- WALL BROKEN DYNAMICALLY (headline): a (kappa0, Delta) region passes G1-G5 and survives
  re-measure -> "3+1D causal CDT DYNAMICALLY GENERATES an extended de Sitter 4-manifold; the
  causal measure SELECTS the joint (d_H AND d_s) 4-geometry 2+1D provably never did; the
  two-DOF unlock (Part A) is the mechanism." Report with error bars, profile, finite-size caveats.
- SCAN INCONCLUSIVE / PARTIAL (honest landing if compute-bound): machinery built + validated
  (moves + DB + ergodicity + benchmark), scan launched, but a point cannot be equilibrated to
  gate quality within the session's compute (4D CDT has severe critical slowing of the N0
  collective mode from the flat seed at fixed N4). Report the phase-structure SIGNAL, the
  trajectory, and hand off resumable checkpoints + the exact resume command. Do NOT claim de
  Sitter from an unthermalized chain (LESSONS 40).
- SURPRISE NEGATIVE (low prior): the two DOF exist but the causal measure still fails the
  joint gate in 3+1D. Major result -- characterize which of G2-G4 fails and the map.

## 6. Scan grid + volumes (frozen)

- Volume: fix N4t via eps-quadratic. Sandbox validation: N4t ~ 6144 (T=4). Uncapped
  production: N4t ~ 15000-40000 (T=5-6), larger if throughput allows. Larger N4 -> sharper
  separation (finite-size caveat). Estimators need N0 >~ 1300 (m>=6) or they saturate (LESSONS 38).
- Grid (frozen): kappa0 in {0.8, 1.5, 2.2, 3.0, 4.0, 5.0}; Delta in {0.0, 0.2, 0.4, 0.6}. The
  literature de Sitter point (2.2, 0.6) is primary; small-Delta rows = phase-B control; large-
  kappa0 / Delta=0 = phase-A control.
- Thermalization: >= a plateau in N0, f_timelike, profile CV past settling; measure only on the
  plateau. Seed-averaged (8 seeds) + sd. Independent re-measure (different seed base) for any
  gate-passing point.

Scoring, action, benchmark, windows, gate, phases, and grid above are frozen as of this commit.
