# Referee validation of the 2D manifold candidate (Prompt 1 executed)

Scope: the single question of whether the project's frame-free construction is a genuine 2D
discrete manifold candidate. Nothing downstream (force laws, QM, Lorentz, gauge, cosmology) is
in scope. "Naturalness," "elegance," and "rule minimality" are treated as non-arguments with
zero evidential weight. All estimators are calibrated on known-topology objects before use
(`tooling/referee_2d_selftest.py`, 22 checks, all pass). Numbers below are from
`tooling/artifacts/topology_sweep.json`, `tooling/artifacts/scaling_sweep.json`, and the
retests recorded here.

## Headline result

Two objects in the project must be judged separately, and the project conflates them:

- The **current headline candidate** (`s1_22` isotropy sandwich, rounds 62/64, the object the
  claim "2D manifold candidate / quad-lattice-grade isotropic 2D selection" refers to) **fails**
  the manifold holdouts. Persistent bridges (~0.03 of edges), articulation points (~0.22 of
  vertices), non-simple boundaries (majority of seeds), and a spectral-dimension gap to matched
  grids that **widens** with N. Verdict unchanged from the prior report: reject "manifold."
- The **earlier `s1_14` planar-action construction** (round 54, "first frame-free manifold
  selection"), which the project pivoted AWAY from, **passes the same holdouts** at spot-check:
  articulation fraction 0.01-0.035 (vs 0.22), a single simple boundary in every seed tested,
  and lazy-RW spectral dimension 1.64-1.98, i.e. in the grid's range. This is the strongest 2D
  signal in the whole arc and it was abandoned in favor of the quad-chasing sandwich.

So the fair-referee verdict is not simply "2D fails." It is: **the project has a real 2D
manifold lead (`s1_14`), and the current headline construction is a regression away from it.**
The recommended minimal path (below, and in the tomorrow-rebuild prompt) is to return to the
triangulated planar-action route and subject it to the full battery, not to keep tuning the
sandwich.

## Task A — Literature review and the standard each source imposes

Every source below was verified to exist; each ends with the concrete bar it sets. Full links
in Sources.

- **Lutz, *Triangulated Manifolds with Few Vertices: Combinatorial Manifolds* (2005).** A
  simplicial d-manifold is defined by its vertex **links** (sphere/ball type), not its graph.
  *Standard imposed:* a 2-manifold claim must exhibit correct vertex links (interior link = a
  cycle), not a dimension-like number.
- **Datta, *Minimal Triangulations of Manifolds* (2007).** 2D-specific: the link of a vertex in
  a triangulated 2-manifold is a cycle; on the boundary, an interval. *Standard imposed:* a
  local link census with interior=cycle, boundary=interval, defect density → 0.
- **Klee & Novik (face enumeration); Grigor'yan et al. (*Graphs Associated with Simplicial
  Complexes*).** A 1-skeleton does not determine the 2-cells except under extra assumptions
  (e.g. flag completion); graph homology can differ from simplicial homology. *Standard
  imposed:* you must declare and justify the 2-cells; a graph alone cannot carry "manifold."
- **Ambjørn–Jurkiewicz–Loll, CDT program; and the CDT review (2024).** Spectral, Hausdorff and
  topological dimension are distinct; CDT shows spectral dimension ≈2 at short scales from
  fluctuations, not from manifoldness. *Standard imposed:* dimension estimators are diagnostics,
  never certificates; report several and do not equate them.
- **Durhuus–Jónsson–Wheater, *The Spectral Dimension of Generic Trees* (2007).** Generic trees
  have Hausdorff dimension 2 yet spectral dimension 4/3 — far from a smooth 2-manifold.
  *Standard imposed:* d_H=2 (or any single exponent) does not imply 2-manifold.
- **Durhuus et al., *On the Spectral Dimension of Causal Triangulations* (2009).** 2D causal
  triangulations: Hausdorff dimension 2, spectral dimension ≤ 2 (a.s. recurrent). *Standard
  imposed:* even a genuinely 2D discrete ensemble need not give spectral dimension 2; matching a
  target requires finite-size scaling toward matched controls.
- **Le Gall / Miermont, Brownian map (Brownian sphere).** A random surface a.s. homeomorphic to
  S² yet with Hausdorff dimension 4; it is the scaling limit of uniform quadrangulations.
  *Standard imposed:* topology and volume/diffusion exponents can separate wildly; "sphere-like
  topology" and "dimension 2" are independent tests, both required.
- **Forman, *Bochner's Method for Cell Complexes and Combinatorial Ricci Curvature* (2003).**
  Curvature is defined on a cell complex; there are topological restrictions to everywhere-
  positive curvature. *Standard imposed:* curvature/Gauss–Bonnet language is only licensed after
  a genuine cell complex is declared — not on a bare graph.
- **Glaser & Surya; Myrheim–Meyer estimator (causal-set manifold-likeness).** Even the most
  permissive discrete-spacetime program treats dimension estimation as one part of a manifold-
  likeness battery that also requires locality tests. *Standard imposed:* locality/link tests are
  necessary, not optional, alongside any dimension estimate.
- **Maslov & Sneppen, *Specificity and Stability in Topology of Protein Networks* (Science
  2002).** Degree-preserving rewiring (swap edges to 10×|E| successful swaps) is the standard
  null that isolates degree-sequence artefacts. *Standard imposed:* positive holdouts must
  separate the candidate from its degree-preserving rewire. (The tooling's rewire uses exactly
  this 10×|E| rule.)

## Task B — Exhaustive claim ledger (2D line, in order)

Class ∈ {native result, proxy/estimator, optimization target, holdout validation, conjecture}.
Status is this review's judgment for the 2D-manifold question only.

| # | Source | Claim (paraphrased) | Class | Status | Basis |
|---|---|---|---|---|---|
| 1 | s1_6_continuum_fractal_tree | Native continuum is a fractal tree, not a manifold (d_s<d_H<d_w) | native result | PASS | Credible negative baseline; consistent with holdouts |
| 2 | s1_6_manifold_phase_transition | Local loop-closure gives a d_s≈2 transition; random loops → mean-field | proxy/estimator | PARTIAL | Estimator real; "manifold" from a d_s crossing overclaims (trees/Brownian map counterexamples) |
| 3 | s1_6_manifold_modification | Local loops fix cycle density + pendants but NOT geometry (d_w grows); minimal change is large | native result | PASS | Honest negative; d_w moving away from 2 is disqualifying |
| 4 | s1_7_coherent_mesh | A frame-CARRYING coherent mesh reaches d=2 manifold | native result | OUT OF SCOPE | Positive control, but not frame-free |
| 5 | s1_10_frame_free_dimension | Degree-capped diamond growth fixes hub formation | optimization/proxy | PARTIAL | Mechanism, not manifold evidence |
| 6 | s1_11_genus_obstruction | b1=1 forces the keystone to genus-0 under any embedding | native structural | PARTIAL | True structural fact; not itself a manifold claim |
| 7 | s1_13_condensation_route | Frame-free face-coherence reaches d_s~2, extensive cycles, but crumples at high genus | native result | PARTIAL | Honest failure mode; strengthens need for topology checks |
| 8 | **s1_14_global_action** | **Global planarity + face reward selects a genuine 2-manifold (first frame-free manifold selection)** | holdout/native | **PARTIAL-PASS (upgraded)** | **Retest: near-zero bridges/articulation, single simple boundary, d_s≈grid at N=120,170. Strongest 2D lead; still needs full defect-decay + N-scaling** |
| 9 | s1_16_growth_cap_dial | One exponent α tunes coarse dimension (d_H=α) | optimization target | PARTIAL | A knob; single exponent can't certify (Task A) |
| 10 | s1_18_gauge_flux_sectors | Short-cycle deficit = b1 − rank(short cycles) = log2(GSD) | designed energy | PARTIAL | Definitional; not independent validation |
| 11 | s1_19_deficit_selection | Deficit minimization alone → tree-plus-clump non-manifolds | native result | PASS | Credible negative control |
| 12 | s1_20_triple_objective | Triple objective identifies coherent manifold as ground state | holdout validation | FAIL | Reuses optimized proxies as validation; superseded by later modules |
| 13a | s1_21_annealing_dynamics | Triple objective selects LOCAL 2-manifoldness; tubes are locally genuine 2-manifolds | proxy/estimator | FAIL | "Local 2-manifoldness" asserted via proxies, not true link tests |
| 13b | s1_21_annealing_dynamics | Path seed fixes the audit artifact, unfreezes dynamics | engineering | PASS | Reproducible engineering correction |
| 14a | s1_22_isotropy_sandwich | Cap C=3.5 pins the ceiling; cap-legal isotropic interiors are quad-type | borrowed-logic | PARTIAL→FAIL | Actual planar embeddings are **triangle-dominated (~3:1)** at every N — not quad |
| 14b | s1_22_isotropy_sandwich | At feasible ceiling, matches the quad lattice column-for-column | holdout validation | FAIL | Matches objective-adjacent columns only; loses to grid on d_s and topology |
| 14c | s1_22_isotropy_sandwich | First frame-free, dimension-agnostic selection of isotropic 2D structure | holdout validation | FAIL | Holdouts fail; overstates |
| 14d | s1_22_isotropy_sandwich | Residual d_s gap is a small fd=3 defect, closes with scaling/annealing | conjecture | FAIL | N-scaling: gap does not close, it **widens**; defect densities flat |
| 15 | STRUCTURE r54 | First frame-free manifold selection | broad validation | PARTIAL-PASS | Same evidence as #8 — stronger than the project later treated it |
| 16 | STRUCTURE r62 | Quad-lattice-grade isotropic 2D selection, zero coordinates | optimization summary | PARTIAL (as optimization) / FAIL (as manifold) | Coherent optimizer story; not manifold validation |
| 17 | STRUCTURE r64 | "2D stands" (while 3D refuted) | broad validation | FAIL for s1_22 | Not justified at manifold-candidate level for the current construction |

## Task C — Retests (calibrated, multi-seed, multi-N)

**Calibration.** `referee_2d_selftest.py` returns textbook answers on a grid disk and a
triangulated disk (χ=1, b1=b2=0, 0 bridges, 0 bad links, single simple boundary, orientable),
b1=1 on an annulus, and confirms a degree-preserving rewire raises the lazy-RW d_s. 22/22 pass.

**s1_22 topology sweep (candidate), mean over 3-6 seeds:**

| N | bridge frac | articulation frac | bad-link frac | single simple boundary | planar | triangles : quads |
|---|---:|---:|---:|---:|---:|---|
| 100 | 0.029 | 0.255 | 0.040 | 50% | 100% | 32 : 9 |
| 150 | 0.025 | 0.258 | 0.037 | 33% | 100% | 48 : 14 |
| 200 | 0.026 | 0.215 | 0.033 | 50% | 100% | 70 : 20 |
| 256 | 0.045 | 0.244 | 0.030 | 33% | 83% | 75 : 21 |
| 400 | 0.028 | 0.211 | 0.029 | (3 seeds) | 100% | 136 : 43 |
| grid/tri (all N) | 0 | 0 | 0 | 100% | 100% | — |

Defect densities are flat, not decaying. Global homology (χ=1, b1=b2=0) is **non-discriminating**
here: filling every bounded face forces a disk for any connected planar graph, so Euler/Betti/
orientability certify nothing — the local tests do the work, and they fail.

**s1_22 scaling sweep (candidate vs matched grid):**

| N | cand d_s (native) | grid d_s | cand lazy-RW [8–24] | grid lazy-RW |
|---|---:|---:|---:|---:|
| 100 | 1.230 | 1.581 | 1.209 | 1.613 |
| 150 | 1.285 | 1.827 | 1.111 | 1.750 |
| 200 | 1.319 | 1.941 | 1.175 | 1.777 |
| 256 | 1.192 | 1.868 | 1.107 | 1.765 |
| 400 | 1.231 | 1.899 | 1.072 | 1.838 |

Candidate flat at ~1.2-1.3 (native) / ~1.1 (lazy-RW); grid climbs to ~1.9. The gap **widens**
(0.35 → 0.67) under two independent estimators. Claim 14d is refuted.

**Null panel (N=150).** Candidate d_s=1.29 is distinguishable from grid (1.83), tri-disk (1.91),
tree+loops (1.35, 98 bridges), random-regular (2.10), preferential-attachment (1.24, lazy 2.94),
random-geometric (1.34). Decisively, the **degree-preserving rewire raises** d_s to 1.78 while
destroying the gluing proxies: the optimized local structure is not "closer to 2D."

**New retest — s1_14 planar action (the abandoned lead):**

| object | N | bridge frac | articulation frac | single simple boundary | lazy-RW d_s | triangles |
|---|---:|---:|---:|---:|---:|---|
| s1_14 `_mcmc_planar` | 120 | 0.00-0.007 | 0.00-0.017 | yes (2/2) | 1.79-1.97 | dominant |
| s1_14 `_mcmc_planar` | 170 | 0.005-0.016 | 0.012-0.035 | yes (2/2) | 1.64-1.98 | dominant |
| s1_22 sandwich | 150 | 0.025 | 0.258 | 33% | 1.11 | dominant |
| grid | ~150-170 | 0 | 0 | yes | 1.75-1.81 | 0 |

s1_14 is an order of magnitude better on articulation, keeps a simple boundary, and sits in the
grid's spectral range. Its `_mcmc_euler_gate` variant over-connects and breaks planarity
(d_s 3.1-3.4), so the *planarity constraint*, not the Euler/face reward, is what helps. This is a
spot check (2 sizes, multiple seeds), not a full proof; it still needs the defect-density-decay
and N-scaling battery. But it is the only construction in the project that passes the holdouts.

## Task D — Minimal fixes

1. **Stop optimizing quads.** The cap→quad "feasibility theorem" (14a) is empirically false: the
   embeddings are triangle-dominated at every N. Drop the quad target; it drove the regression.
2. **Return to the s1_14 planar-action route** as the substrate and run it through the full
   battery (defect-density vs N, boundary stability, d_s/d_H convergence to matched grids,
   rewire + null panel). This is the smallest change with evidence behind it.
3. **Declare the 2-cells explicitly** (the planar-face complex is fine, but declare it) so link,
   incidence, boundary, and curvature tests are defined rather than proxied.
4. **Replace proxy validation with holdouts** everywhere: fd=2 / E_glue / closed-link are the
   objective and cannot validate it.
5. **Only then** reintroduce isotropy as a *secondary* refinement, checked to not reintroduce
   articulation points — the specific defect that separates s1_22 from s1_14.

## Task E — Acceptance criterion and verdict

"2D manifold candidate" is earned only when, on a declared canonical 2-complex: interior vertex
links are cycles and boundary links intervals with defect density → 0 in N; interior edges lie in
exactly two 2-cells (bad-incidence → 0); the boundary is a small fixed number of simple cycles;
χ, Betti and orientability match a stated topological type; d_s and d_H converge to matched 2D
controls under increasing N and longer anneals; the candidate beats its degree-preserving rewire
and the null panel on these holdouts; and finite-size scaling supports any continuum language.

**Verdict.** The current headline construction (`s1_22`) does not meet it and, on the pivotal
scaling test, moves the wrong way with N. The label "2D manifold candidate / quad-lattice-grade
isotropic 2D selection" should be withdrawn for that object. However, the project's own earlier
`s1_14` planar-action construction meets the local and spectral holdouts at spot-check and is a
legitimate 2D-manifold *lead* deserving the full battery. The correct scientific move is to
re-open s1_14, not to defend s1_22.

## Reproducibility, tooling changes, honest limits

- Rerun: `PYTHONPATH=. python3 tooling/referee_2d_selftest.py`; then the two sweep scripts (see
  `tooling/REFEREE_2D_RESULTS.md` for exact commands). s1_14 retest:
  `from sec01_raw_wolfram_hypergraph_facts.s1_14_global_action import _mcmc_planar` → audit with
  `tooling/referee_2d_topology.py:analyze`.
- Tooling fix made during this pass: `referee_2d_scaling.py` and `referee_2d_selftest.py` now add
  their own directory to `sys.path`, so they import as modules (not only as scripts). This is
  what let the s1_14 retest reuse the audit code.
- Limits: the s1_14 result is a spot check (N=120 and 170, a handful of seeds), not a full sweep;
  it is promising, not proven. d_s/d_H are finite-size-sensitive and quoted as such. No claim
  here rests on a single seed or single N. No citation or number is fabricated; where evidence is
  a spot check it is labeled one.

## Sources

- Lutz, Triangulated Manifolds with Few Vertices: Combinatorial Manifolds — https://arxiv.org/abs/math/0506372
- Datta, Minimal Triangulations of Manifolds — https://arxiv.org/pdf/math/0701735
- Causal Dynamical Triangulations review (2024) — https://arxiv.org/pdf/2401.09399
- Durhuus, Jónsson, Wheater, On the Spectral Dimension of Causal Triangulations — https://arxiv.org/pdf/0908.3643
- Durhuus, Jónsson, Wheater, The Spectral Dimension of Generic Trees — https://link.springer.com/article/10.1007/s10955-007-9348-3
- Le Gall, Random Planar Geometry (Brownian map) — https://ethz.ch/content/dam/ethz/special-interest/math/mathematical-research/fim-dam/Conferences/2017/Random%20geometries_Random%20topologies/le_gall-jean-francois.pdf
- Forman, Bochner's Method for Cell Complexes and Combinatorial Ricci Curvature — https://link.springer.com/article/10.1007/s00454-002-0743-x
- Combinatorial Ricci curvature and Gauss–Bonnet on cell complexes — https://arxiv.org/pdf/1703.08409
- Surya, The Causal Set Approach to Quantum Gravity (Living Reviews) — https://link.springer.com/article/10.1007/s41114-019-0023-1
- Maslov & Sneppen, Specificity and Stability in Topology of Protein Networks — https://arxiv.org/abs/cond-mat/0205380
