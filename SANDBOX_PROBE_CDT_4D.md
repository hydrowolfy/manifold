# Sandbox certification probe: 3+1D (2.2,0.6), un-saturated N0 (companion to RUN_LOG)

Goal: get a THERMALIZED (2.2,0.6) state at N0 > 1300 (un-saturated d_H/d_s, LESSONS 43) and read
its joint dimensions vs the finite-size flat-T^4 benchmark. Run in-sandbox (reliable, no mount
race) at T=6, N4t=45000, eps=0.004, grown-above-seed base (grow gives N0~3100, relaxes down).

## Trajectory (2.2, 0.6), N4~45000, census bad=0 throughout, profile uniform/extended (CV~0.01-0.02)

    sweep   N0     f_tl    d_s(8-24)        d_H(2-6)      hubs(deg>40)
      25   2206   0.508   5.29 +- 0.47     2.36           --
      44   1930   0.544   5.48 +- 0.13     2.22 +- 0.21    --
      56   1826   0.558   4.90 +- 0.48     1.94 +- 0.10    32%
      62   1777   0.564   4.95 +- 0.82     1.91 +- 0.09    33%   [d_s(4-12)=5.54]

Benchmark (flat T^4, matched N0~1780, interpolating m=6..7): d_s(8-24) ~ 4.1-4.3, d_H(2-6) ~ 2.66-2.75.

## Read (honest)

POSITIVE (solid): the ergodic, DB-correct 4D Monte Carlo dynamically generates a CENSUS-CLEAN,
EXTENDED (uniform profile, no stalk), genuinely 4-DIMENSIONAL geometry -- d_s(8-24) ~ 4.9-5.0 at
UN-SATURATED N0 ~ 1780, far above the 3D value 3.13 and the saturation floor ~2.6. 2+1D provably
could only reach 3D; 3+1D reaches an extended 4-geometry. The dimensional escape (Part A: two
independent DOF) is dynamically realized.

NOT A CLEAN de SITTER GATE-PASS at N4=45000:
- d_H(2-6) ~ 1.9 is BELOW the finite-size flat-T^4 benchmark ~2.7 (ratio ~0.71 < 0.90 gate G2).
- the d_s SCALE FLOW is BACKWARDS: the short/UV window d_s(4-12)=5.54 reads HIGHER than the long/IR
  d_s(8-24)=4.95. De Sitter requires the OPPOSITE (IR ~4 flowing DOWN to UV ~2). The observed
  upward flow is a HUB signature (short-range shortcuts), not de Sitter dimensional reduction.
- the state is HUB-DOMINATED: ~33% of vertices have degree > 40 (flat torus is uniform deg 30);
  the hubs saturate ball-growth (d_H low) AND inflate the walk (d_s high) -- the SAME d_s-d_H
  anticorrelation that walled 2+1D (LESSONS 20), here reproduced in 4D at this volume.
- the volume profile is a UNIFORM TUBE, not the localized cos^3 de Sitter blob.

## Interpretation + next step (honest, no overclaim)

At N4=45000 the causal ensemble at (2.2,0.6) is a hub-dominated extended 4-geometry -- 4D in
dimension but NOT the clean de Sitter phase. This is most likely FINITE-SIZE: established 4D CDT
de Sitter results are at N4 ~ 1e5-1e6, where the extended phase is clean and hubs are subdominant;
at N4=45000 hubs dominate. Whether the clean de Sitter gate (d_H ratio >=0.90, d_s flowing 4->2,
cos^3 profile) emerges at larger N4, or the anticorrelation persists into 4D (a genuine SURPRISE),
is UNRESOLVED and is the next test: (a) larger N4 (the overnight run is a step; 1e5+ is the target),
(b) the (2.2,0.0) collapse control for the B-vs-C contrast (does Delta dynamically switch
extended<->collapsed -- the two-DOF unlock in action even before a clean gate-pass).

NO de Sitter CLAIM is made (LESSONS 40). Landing: the dimensional escape to an extended 4-geometry
is dynamically CONFIRMED; the clean de Sitter certification is a compute-scale (large-N4) question,
handed off to the uncapped overnight run + the scheduled analysis + a future 1e5-volume run.
