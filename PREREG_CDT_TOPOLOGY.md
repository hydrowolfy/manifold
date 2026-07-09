# PREREG: STAGE 1 (surgical) -- break the sphere assumption, causal CDT on T^2 x S^1

Preregistered 2026-07-09, BEFORE thermalizing/measuring any torus study state (committed with the
runner `cdt_torus_run.py`, before the physics chunks). Branch `causal-cdt-scaling`. This is STAGE 1
of the topology frontier named in HANDOFF.md S5 / REPORT_CDT_HUB.md ("different spatial slice
topology -> breaks F = 2V - 4"). Sequence: surgical (this) -> exotic -> 3+1D.

## 0. Established BEFORE the experiment (analytical, not post-hoc)

Per-slice Euler for a closed orientable slice of genus g: chi = 2 - 2g and (closed surface, 2E=3F)
F = 2V - 2 chi. The foliation counting is UNCHANGED from the sphere case -- one (3,1) per spatial
triangle of the lower slice, one (1,3) per spatial triangle of the upper slice -- so summing over
the T periodic slabs:

    N31 = N13 = sum_t F_t = 2 N0 - 2 chi T
    N22 = N3 - N31 - N13   = N3 - 4 N0 + 4 chi T
    f22 = N22 / N3         = 1 - 4 (N0 - chi T) / N3

Sphere (chi=2): N22 = N3 - 4 N0 + 8 T  (the campaign-7 locked identity). Torus (chi=0): **N22 = N3 - 4 N0**.
The +8T offset generalizes to +4 chi T and VANISHES for the torus.

CRUX (registered claim). Differentiate at fixed volume N3 and fixed slice count T:
    dN22 = -4 dN0 + 4 T dchi.
chi is a topological invariant of the (fixed) slice topology, so dchi = 0 under EVERY foliation-
preserving move. Hence **dN22 = -4 dN0 holds for every genus** -- the differential lock is topology-
INDEPENDENT. Breaking F = 2V - 4 shifts only the CONSTANT term; it does NOT dissolve the lock.
Therefore "add spatial vertices without removing (2,2) tets" remains combinatorially IMPOSSIBLE on
the torus, exactly as on the sphere. (Corollary, used to reuse the core verbatim: dN22 = dN3 - 4 dN0
gives move weights 2-3:+1, 3-2:-1, 2-6/6-2/4-4:0 -- identical to the sphere runner.) Verified exact
to the integer on seed/grown/thermalized torus states in the runner selftest.

So the "new move" escape is closed on the torus by the SAME proof. What the topology change DOES
alter, and what this experiment tests, is two things the counting identity cannot decide:
  (A) the OFFSET SHIFT: at matched (N0,N3,T), f22_torus = f22_sphere - 8T/N3, moving the accessible
      band -- possibly repositioning the two benchmark crossings (d_s and d_H) relative to each other;
  (B) the DEGREE-DISTRIBUTION freedom (campaign-7's sole remaining lever) is qualitatively different:
      the sphere FORCES curvature defects (sum_v (6 - deg) = 6 chi = 12 > 0, so a uniform degree-6
      slice is impossible), whereas the torus ADMITS a uniform degree-6 flat slice (6 chi = 0). The
      flat uniform 3-torus (the benchmark's own geometry) is IN this ensemble. Campaign 7's hub term
      drove d_s down THROUGH the benchmark while d_H rose; on the torus the flat target is reachable.

## 1. Hypotheses

- H_topo (breakthrough): the T^2 x S^1 causal ensemble supports a STABLE equilibrium that meets the
  joint (d_H AND d_s) benchmark gate -- i.e. breaking F=2V-4 opens the joint 3-manifold the sphere forbids.
- H_wall (null / registered prediction): the wall REAPPEARS at chi=0. Rationale: the differential lock
  survives, so the single-locked-DOF root of the campaign 5-7 wall (N0 and f22 are one DOF) is intact,
  and hub formation is entropically favored (many hubbed triangulations vs one flat one) even though the
  flat state is now admissible. Predicted signature: the same d_H-d_s anticorrelation and heavy-tailed
  hubs (deg_max >> 14) at equilibrium, no (config) passing G2 and G3 together.

Registered prior: H_wall is the more likely outcome. A clean joint pass would REFUTE this prior and is
the breakthrough. Either way is a real STAGE-1 result.

## 2. Benchmark (matched flat 3-torus)

T^2 x S^1 IS the flat-3-torus topology foliated along one circle, so the flat T^3 is the in-topology
benchmark. Two independent exact realizations, size-matched by N0, agree (cross-validated pre-registration):
  - Kuhn T^3 m=10 (N0=1000): d_H(2-6) = 2.47 (deterministic); d_s(8-24) = 3.13 +- 0.18 (8 estimator seeds).
  - flat foliated calibrant 9x9 T=12 (N0=972, built by cdt_torus_run --calibrant): deg 14.0 sd 0.0 max 14
    (uniform, == Kuhn); d_H(2-6) = 2.43 +- 0.001; d_s(8-24) = 3.10 +- 0.21.
SCORING TARGET: d_H(2-6)_bench = 2.47, d_s(8-24)_bench = 3.13 +- 0.18. (LESSONS 1-2: score vs exact
finite-size T^3, seed-average >= 8 estimator seeds and quote sd, for BOTH state and benchmark.)

## 3. Primary configuration (apples-to-apples with campaign 7)

V (=N3 target) = 6000, T = 12, k0 = 2.0, k22 = 0, eps = 0.002, seed 0, grid seed 5x5 grown to V.
Matches the campaign-7 sphere baseline (V6000, T12, k0=2, sigma=0) for direct comparison. At
equilibrium N0 = N3 (1 - f22)/4 ~ 800-1000, matching benchmark m=10. Thermalize to an f22 / profile-CV
plateau, then measure seed-averaged (>=8 ds seeds, >=4 dh seeds).

## 4. Joint gate (G1-G5), preregistered thresholds

- G1  MANIFOLD: link census bad = 0 AND disk = 0 in every measured snapshot.
- G2  d_H:      d_H(2-6) / 2.47 >= 0.90   (i.e. d_H(2-6) >= 2.22).
- G3  d_s:      |d_s(8-24) - 3.13| <= 0.20   (i.e. d_s(8-24) in [2.93, 3.33]).
- G4  NO CONDENSATION: spatial-volume profile CV not drifting up and MIN slice not collapsing across
      the equilibrium window (compare to the ~uniform calibrant CV; flag a rising-CV / collapsing-min state).
- G5  EQUILIBRIUM: f22, N3, profile CV, and both dims stable across >= ~300 sweeps (not a transient crossing).

JOINT PASS = G1..G5 all satisfied by ONE equilibrium state.

## 5. Decision rules (fixed before the run)

1. If an equilibrium state passes G1-G5 jointly -> **H_topo SUPPORTED (breakthrough)**: torus topology
   opens the joint 3-manifold. CONFIRM before any headline: (a) a 2nd MC seed at V6000, (b) a V=12000
   check at matched slice size, (c) re-measure with an independent estimator seedbase.
2. If no state passes G2 and G3 together (they cross the benchmark at different points along the same
   anticorrelated trend, as on the sphere) -> **H_wall SUPPORTED: the wall reappears at chi=0.** Report
   the mechanism: (i) degree distribution -- does it still hub (deg_max >> 14) or stay near-uniform? and
   (ii) whether a NEW chi=0 locking identity / order parameter (f22 vs N0) governs the same tradeoff.
3. If a state passes transiently but fails G5 (drifts) -> report as condensation, NOT a pass (LESSONS 6, 14).

## 6. Preregistered diagnostics (reported regardless of outcome)

Equilibrium f22; profile and profile CV; **degree distribution (mean / sd / max)** -- the primary
discriminator between "flat like the benchmark" (deg_max ~ 14) and "hubbed like the sphere causal
state" (deg_max ~ 84, sd ~ 10); acceptance fractions; wall-clock. A short lever sweep (k22 >= 0, and/or
a slice-size / T variation) is permitted ONLY to locate the anticorrelation, and any crossing it
produces is scored against G1-G5 with the equilibrium (G5) check enforced.

## 7. Discipline (rolled from LESSONS_CDT.md)

Exact benchmark (1-2). Slice size s = N3/T is the controlling variable (3). d_H windows need T>=8 (4).
Report both d_s windows (5). k22 causes condensation -- check equilibrium, track profile CV (6-7, 14).
Detailed balance + manifold preservation verified in selftest for the new construction (done: identity
+ round-trips + orientable-torus census). One budgeted chunk per bash call, <=~34s (8, 22). Keep
pkl/floats out of git (12).
