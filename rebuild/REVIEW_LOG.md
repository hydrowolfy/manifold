# Review log — rebuild/2d-manifold-minimal

Protocol: reviewers examine the work in the voice of the paper's primary author, cite a real
paper for each critique, and the primary agent must resolve each before merge. Merge to `main`
is gated on all reviewers signing off. **Status: NOT signed off — round 1 only.** One review
round is recorded here (performed by the orchestrator standing in as reviewer); the full
multi-agent reviewer panel is the next step and is required before any merge.

## Round 1

**R1 — Declare the 2-cells; a graph is not a complex.**
Source: Klee & Novik, face enumeration; Grigor'yan et al., *Graphs Associated with Simplicial
Complexes*. A 1-skeleton does not fix the 2-cells, and graph homology can differ from simplicial
homology.
Primary agent: Accepted. The construction's 2-cells are declared as the bounded faces of the
planar embedding, computed deterministically in `tooling/referee_2d_topology.py`; all link and
incidence tests run on that declared complex, not on a short-cycle proxy. **Resolved.**

**R2 — A spectral dimension near the grid is necessary, not sufficient.**
Source: Ambjørn–Jurkiewicz–Loll (CDT); Durhuus–Jónsson–Wheater (generic trees: d_H=2, d_s=4/3);
Le Gall/Miermont (Brownian sphere: S² topology, Hausdorff dim 4). A single exponent, or even a
pair, cannot certify manifoldness.
Primary agent: Accepted, and this is why the branch reports link-correctness, edge incidence,
and boundary structure alongside d_s. At N=140 the planar route gives articulation fraction
0.019 and 100% simple boundary, not merely a matching d_s. **Partially resolved — the defect
densities must still be shown to → 0 with N (open).**

**R3 — The boundary must be a stable simple cycle across sizes.**
Source: Datta, *Minimal Triangulations of Manifolds* (boundary vertex links are intervals).
Primary agent: 100% single simple boundary at N=140 and at N=120/170 in the validation report.
**Partially resolved — N-scaling of boundary stability is open.**

**R4 — Discriminate against the degree-preserving null.**
Source: Maslov & Sneppen (Science 2002), degree-preserving rewiring at 10×|E| swaps.
Primary agent: The prior null panel shows the s1_22 candidate fails this (rewire *raises* d_s).
The planar route has not yet been run against its own rewire on the topology holdouts.
**Open — required before sign-off.**

### Round-1 outcome
Two of four comments resolved; two require an N-scaling sweep of the planar route and a rewire
comparison. Reviewer sign-off withheld. Per the merge gate, `rebuild/2d-manifold-minimal` does
**not** merge to `main` yet.

## Round 2 — full reviewer panel (4 sub-agents, author-persona, citation-backed)

**Overall outcome: SIGN-OFF WITHHELD. 4/4 reviewers return CHANGES REQUIRED. The branch does
NOT merge to `main`.** The panel overturned the branch thesis: on scrutiny the `s1_14` planar
route also fails the manifold holdouts, and the ablation that motivated it is methodologically
circular. This is the review process working — the round-1 stand-in review was too lenient.

### Reviewer 1 — substrate / 2-complex (VERDICT: CHANGES REQUIRED)
- The tooling discriminates correctly (grid PASS, s1_22 FAIL) and is honest that global homology
  is non-discriminating, but the write-up over-claims. Grid and candidate BOTH return χ=1,
  b1=b2=0 — filling every bounded face forces a disk for any connected planar graph. — [Euler
  relation V−E+F=2 for connected planar graphs].
- "Triangulated planar disk" is wrong: `face_spectrum` classifies faces as length-3 closed
  *walks*, with no distinct-vertex/2-simplex check, so the object is a polygonal **CW** complex,
  not a simplicial/triangulated one. — [Klee & Novik, Face enumeration on simplicial complexes,
  arXiv:1505.06380].
- The 2-cells are the embedding's bounded faces — one choice among many over the same
  1-skeleton — and must be *declared and justified*, not assumed; graph vs simplicial homology
  can differ. — [Grigor'yan, Muranov, Yau, Graphs Associated with Simplicial Complexes, HHA
  16(1) 2014]; [Lutz, Triangulated Manifolds with Few Vertices, arXiv:math/0506372].

### Reviewer 2 — local topology / defect-density decay (VERDICT: CHANGES REQUIRED)
- Ran `_mcmc_planar` at N=120/180/240, 3 seeds. Defect fractions **RISE, not decay**: bridge
  0.0024→0.0120→0.0128; articulation 0.0055→0.0278→0.0264; bad-link 0.0055→0.0259→0.0264. Grid
  is 0 at all N. The N=120–170 spot-check that motivated "return to s1_14" was a lucky window.
- `bad_links_noncut = 0` at every N ⇒ the bad links ARE the articulation points — genuine local
  pinch points with disconnected links, disqualifying for a manifold, and their density grows
  with N. — [Datta, Minimal Triangulations of Manifolds, arXiv:math/0701735]; [Bagchi & Datta,
  arXiv:math/0506536]; [Lutz, arXiv:math/0506372].
- "Small at one N" was asserted as "→ 0"; it is not. If articulation keeps rising, the honest
  conclusion is "a disk-like planar graph with a growing set of pinch points," i.e. NOT a 2D
  manifold candidate — and the minimal-step thesis must be revised, not re-emphasized.

### Reviewer 3 — scaling / finite-size / null discrimination (VERDICT: CHANGES REQUIRED)
- Ran N=120/180/240. d_s does **not** converge to the grid: per-seed trajectories disagree in
  sign (seed 11: 2.00→1.70, away from grid; seeds 1/2 rise from below). Seed spread at N=240
  (~0.28) is ~9× the candidate–grid mean gap (~0.03): "sits next to the grid" is an averaging
  artifact. Ball-growth d_H rises 1.48→2.04 while lazy d_s falls on the same graphs — estimator
  disagreement. — [Ambjørn–Jurkiewicz–Loll, spectral dimension is scale dependent,
  arXiv:hep-th/0505113]; [Cooperman, renormalization of CDT, arXiv:1406.4531]; [Durhuus–Jónsson–
  Wheater, generic trees d_H=2/d_s=4/3, arXiv:math-ph/0607020]; [Le Gall / Miermont Brownian map].
- One clean pass: the candidate separates decisively from its Maslov–Sneppen degree-preserving
  rewire (d_s ~1.7–2.0 vs ~3.3–4.2, gap widening). Necessary, not sufficient. — [Maslov &
  Sneppen, Science 2002, arXiv:cond-mat/0205380].

### Reviewer 4 — minimality / methodology (VERDICT: CHANGES REQUIRED)
- **Circularity:** `_mcmc_planar` only accepts planarity-preserving edges; `analyze()` reports
  planarity from the same `nx.check_planarity`. So the ablation's PLANAR=100% / EULER-GATE=0%
  row is a tautology — the optimizer's own constraint re-served as a "holdout." Train-on-the-
  test-metric leakage; the same error the report indicts s1_20 for.
- **Confounded ablation:** euler-gate changes the gate AND the density (planar E≈305–312 vs
  euler-gate E≈405–408, ~33% more edges); the d_s blow-up is consistent with density alone, so
  planarity is not isolated. — [controlled-ablation methodology: single-variable isolation].
- **Minimality not established:** only one removed component (s1_22) and one degraded step
  (euler-gate) were tested; s1_16/s1_18/s1_19/s1_20/s1_21 are declared ablatable by assertion
  with no per-step drop test. Downgrade "minimum steps" to "smallest configuration tried."
- `_mcmc_planar` optimizes a triangle/face reward (`exp(dtri/T)`), so triangle count and fd
  proxies are optimization targets, disqualified as validation. — [causal-set manifold-likeness
  requires a battery incl. locality: Surya, Living Reviews in Relativity 22:5 (2019); Glaser &
  Surya, arXiv:1309.3403].

### Consolidated required changes (union; all must clear before re-review)
1. Remove the circular `planar` metric (and any generator-optimized face/triangle/fd quantity)
   from the holdout column; validate planarity/genus with independent code on held-out statistics.
2. Re-run the ablation with a single-variable "remove planarity" arm at matched edge count.
3. Run a proper finite-size-scaling ladder (≥5–6 sizes to N~1–2k, ≥10–20 seeds, CIs, fitted
   approach-to-limit) for BOTH defect densities and d_s/d_H on identical seeds/sizes. Current
   evidence: defect densities rise 120→240 and d_s is seed-noise-dominated — near-fatal.
4. Declare and justify the 2-cell set; relabel "triangulated"→"polygonal CW"; demote global
   homology wherever the passing disk line is quoted.
5. Complete the minimality experiment: per-step leave-one-out drop tests for s1_16/18/19/20/21.
6. Reconcile the ball-growth d_H vs lazy d_s estimator disagreement.

Until 1–6 clear and all four reviewers sign off, `rebuild/2d-manifold-minimal` does NOT merge.
