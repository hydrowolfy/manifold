# Minimal reconstruction to a 2D discrete manifold

Branch `rebuild/2d-manifold-minimal` (feature branch; `main` stays clean until a reviewed
merge). Goal only: reach a 2D-manifold-grade object in the minimum number of justified
construction steps. Naturalness/elegance are not arguments.

## Thesis

The minimum step is a single one: **frame-free growth under a global planarity constraint**
(the `s1_14 _mcmc_planar` move). Everything the project added afterward — growth-cap dial
(s1_16), gauge/flux deficit (s1_18), deficit selection (s1_19), triple objective (s1_20),
annealing (s1_21), isotropy sandwich (s1_22) — is **ablatable**: it does not improve the
manifold holdouts, and the isotropy arc actively regresses them.

## Ablation (this branch: `rebuild/ablation_planarity.py`, N=140, seeds 11/1/2)

| construction | planar | bridge frac | articulation frac | bad-link frac | simple boundary | lazy-RW d_s |
|---|---:|---:|---:|---:|---:|---:|
| grid (reference) | 100% | 0 | 0 | 0 | 100% | 1.73 |
| **PLANAR — step present (s1_14)** | 100% | 0.009 | **0.019** | 0.019 | **100%** | **1.66** |
| EULER-GATE — step altered (s1_14) | 0% | — | — | — | 0% | 3.97 |
| SANDWICH — arc added (s1_22) | 100% | 0.046 | **0.238** | 0.055 | 67% | **1.05** |

Reading, two directions of the ablation:
- Remove the planarity constraint (euler-gate over-connects): planarity is destroyed and the
  spectral dimension blows up to ~4. The step is **necessary**.
- Add the later arc (sandwich): articulation jumps 0.019 → 0.238 (~12×) and the spectral
  dimension collapses 1.66 → 1.05, away from the grid. The arc is not just unnecessary, it is
  **harmful**. This is the empirical death of the "cap forces quad-isotropy" rationale.

The planar-constrained object alone sits next to the grid on the decisive holdouts.

## Minimal pipeline

Step 1 (only justified step): frame-free MCMC growth with a global planarity constraint,
producing a triangulated planar disk. Ablation test: `rebuild/ablation_planarity.py`
(fails without the step; regresses with the later arc).

## What is NOT yet earned

This is a spot check (N=140, plus N=120/170 in the validation report), not a proof. Before
"2D manifold candidate" is claimed for this route it still owes, per the acceptance criterion:
declared 2-cells; defect densities (bridges, articulation, bad links, bad incidences)
demonstrably → 0 with N; a stable simple boundary across N; d_s and d_H converging to matched
grids under increasing N and longer runs; and separation from the degree-preserving rewire and
the null panel on these holdouts. Those are the next steps on this branch. Until they pass and
the review below signs off, nothing merges to `main`.

## STATUS after review round 2 (panel): THESIS NOT SUPPORTED AS WRITTEN

The 4-reviewer panel (REVIEW_LOG.md, round 2) overturned the thesis above. Extended to N=240 the
planar route's defect densities RISE, not decay (articulation 0.006→0.028→0.026), d_s does not
convergently approach the grid (seed-noise-dominated, estimators disagree), and the ablation's
"planarity holdout" is circular (planarity is the generator's own acceptance gate). The planar
route remains the *best* object in the project and cleanly beats its degree-preserving rewire,
but on this evidence it is "a disk-like planar graph with a growing set of pinch points," not a
proven 2D manifold candidate. The recommendation "return to s1_14" was based on a spot-check that
did not probe N-scaling — the exact facet that fails. See the consolidated required changes.
