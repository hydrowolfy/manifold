# Referee 2D-Manifold Validation — Results

Branch: `2d-manifold-validation`. This report is produced by two standalone scripts,
`tooling/referee_2d_topology.py` and `tooling/referee_2d_scaling.py`, plus the calibration
harness `tooling/referee_2d_selftest.py`. Raw data: `tooling/artifacts/topology_sweep.json`
and `tooling/artifacts/scaling_sweep.json`.

The object under test is the frame-free 2D candidate produced by
`sec01_raw_wolfram_hypergraph_facts.s1_22_isotropy_sandwich._sandwich` in the "feasible
ceiling" regime `(w_glue, w_def, w_iso, cceil) = (1, 3, 2, 2.1)`, `T_hi=2.0, T_lo=0.2`,
`120 N` MCMC steps — the regime the project summarizes as "quad-lattice-grade isotropic 2D
selection." Sweep: `N = 100, 150, 200, 256, 400`, seeds 0–5 (fewer at the two largest N).

## Method

A 2-manifold claim is a claim about a 2-complex, not a graph. The topology script does not
reuse the project's short-cycle face-degree proxy as the face set. It builds a canonical
2-complex by taking a planar embedding (`networkx.check_planarity`) and treating every
bounded face as a 2-cell, then measures the local and global obligations of a
2-manifold-with-boundary. The scaling script measures dimension with two estimators that are
independent of the objective and of the project's native estimator: a ball-growth slope and a
lazy random-walk return-probability spectral slope, each fit over several explicit windows.
Every quantity is compared at matched `N` against a control panel.

The tooling is calibrated: `referee_2d_selftest.py` (22 assertions, all passing) confirms the
topology layer returns χ=1, b1=b2=0, zero bridges, zero bad links and a single simple boundary
on a grid disk and a triangulated disk; b1=1 on an annulus (grid with one face left open); and
that the holdout estimators move the right way (a degree-preserving rewire raises the lazy-RW
d_s; a grid exceeds the candidate).

## Metric taxonomy

The handoff requires a clean separation of what was optimized from what is an independent
holdout. The four classes below are kept strictly apart.

### 1. Optimized metrics (the objective — cannot validate anything)

These are the terms the `_sandwich` energy minimizes, or one-to-one functions of them. They
are reported only to confirm the candidate reaches its intended phase, and at matched `N` the
candidate meets or beats the quad-lattice reference on them.

| N | E_glue/edge | deficit | fd=2 % | closed-link | (grid N=150 reference) |
|---|---:|---:|---:|---:|---|
| 100 | 0.126 | 1.25 | 91.0 | 0.805 | |
| 150 | 0.116 | 2.25 | 91.2 | 0.813 | grid: 0.167 / 0.00 / 83.3 / 0.693 |
| 200 | 0.168 | 2.0 | 87.5 | 0.738 | |
| 400 | 0.170 | 4.5 | 87.2 | 0.729 | |

The candidate reaches a lower E_glue/edge and higher fd=2 fraction than the grid. This
reproduces the project's own result and is not in dispute. (N=256 is noisier — one of three
seeds degraded, pulling E_glue/edge to 0.48 — indicating the phase is not uniformly reached at
larger N.)

### 2. Proxy metrics (fd-derived — not independent)

fd=2 fraction, E_glue, deficit, cap audit, closed-link fraction are all computed from the same
short-cycle / face-degree machinery the objective optimizes. "Closed-link fraction" is not an
independent link test; it is a short-cycle statistic. None can carry a manifold claim. They are
folded into class 1 above.

### 3. Holdout topology metrics — the 2-complex (PASS / FAIL)

Candidate, mean over seeds (fractions in parentheses). Controls (grid, tri-disk) are identical
clean disks at every N and are shown once.

| N | seeds | bridges | articulation pts | bad links | bad edge-incid. | single simple boundary | planar |
|---|---:|---:|---:|---:|---:|---:|---:|
| 100 | 6 | 4.7 (0.029) | 25.5 (0.255) | 4.0 (0.040) | 4.7 | 50% | 100% |
| 150 | 6 | 6.0 (0.025) | 38.7 (0.258) | 5.5 (0.037) | 6.0 | 33% | 100% |
| 200 | 6 | 8.5 (0.026) | 43.0 (0.215) | 6.5 (0.033) | 8.5 | 50% | 100% |
| 256 | 6 | 17.0 (0.045) | 62.3 (0.244) | 7.6 (0.030) | 18.6 | 33% | 83% |
| 400 | 3 | 18.0 (0.028) | 84.3 (0.211) | 11.7 (0.029) | 18.0 | 100%* | 100% |
| **grid / tri (all N)** | — | **0** | **0** | **0** | **0** | **100%** | **100%** |

*the N=400 boundary rate is over only 3 seeds.

Reading:

- **Global homology is not discriminating here, and should not be quoted as evidence.** Because
  the construction fills every bounded face, any planar connected candidate is forced to
  χ = V − E + F = 1, b1 = b2 = 0, orientable. The candidate "passes" Euler/Betti/orientability
  trivially, by construction, not because it is manifold-like. The real tests are local.
- **Bridges: FAIL.** A 2-manifold (with or without boundary) has none. The candidate has 4–18,
  a fraction ≈ 0.025–0.045 that does not fall with N.
- **Articulation points: FAIL.** Interior of a manifold-with-boundary has none. The candidate
  sits at ≈ 0.21–0.26 of all vertices at every size.
- **Vertex links: mostly clean but not zero-defect.** good-link fraction ≈ 0.97; 4–12 vertices
  per instance have a link that is neither a cycle (interior) nor an interval (boundary). The
  bad-link fraction drifts 0.040 → 0.029 across N — a shallow decline, not a trend to zero.
- **Boundary: FAIL.** A disk-like patch needs one simple boundary cycle. The candidate produces
  a single simple boundary cycle in only 30–50% of seeds (interior seeds excepted at N=400,
  small sample); the rest have pinched or multi-component boundaries.
- **Planarity is not guaranteed.** It held everywhere except one N=256 seed, where the graph was
  non-planar and no canonical 2-cell set exists at all.
- **Face spectrum: not quad-like.** Triangles outnumber quads roughly 3–4:1 at every size
  (e.g. N=150: 48 triangles vs 14 quads), with recurrent large stray faces (largest bounded
  face 16–48 nodes). The "quad-lattice-grade" description does not survive the actual embedding.

### 4. Holdout scaling metrics — dimension (does the gap close with N?)

Native `_d_s`/`_d_H` are shown for continuity with the project; the load-bearing numbers are the
two independent estimators. Candidate vs matched grid:

| N | cand d_s (native) | grid d_s | cand lazy-RW [8–24] | grid lazy-RW | cand ball [3–8] | grid ball |
|---|---:|---:|---:|---:|---:|---:|
| 100 | 1.230 | 1.581 | 1.209 | 1.613 | 1.394 | 1.333 |
| 150 | 1.285 | 1.827 | 1.111 | 1.750 | 1.417 | 1.421 |
| 200 | 1.319 | 1.941 | 1.175 | 1.777 | 1.326 | 1.457 |
| 256 | 1.192 | 1.868 | 1.107 | 1.765 | 1.206 | 1.535 |
| 400 | 1.231 | 1.899 | 1.072 | 1.838 | 1.377 | 1.596 |

The candidate's spectral dimension is flat at ≈ 1.2–1.3 (native) and ≈ 1.1 (lazy-RW) across the
whole range. The grid climbs toward ≈ 1.9. **The gap does not close; it widens** (native gap
0.35 at N=100 → 0.67 at N=400). The independent lazy random-walk estimator gives the same
verdict as the native one, so the shortfall is not an artifact of the project's estimator. The
project's stated expectation — that the residual d_s gap closes with scaling/annealing — is not
supported by these larger-N runs. (A separate longer-anneal effort is not included here; the
report being validated already noted 2×/3× anneals did not remove the gap.)

## Null-model panel (N=150; N=200 consistent)

| model | d_s (native) | lazy-RW [8–24] | ball [3–8] | bridges | note |
|---|---:|---:|---:|---:|---|
| candidate | 1.285 | 1.11 | 1.42 | 6 | the object under test |
| grid | 1.827 | 1.75 | 1.42 | 0 | 2D reference |
| triangulated disk | 1.913 | 1.64 | 1.32 | 0 | 2D reference |
| degree-preserving rewire | 1.781 | 2.66 | 1.40 | 4 | destroys the local face structure yet **raises** d_s |
| tree + loops | 1.352 | 1.38 | 1.71 | 98 | tree-like |
| random regular (d=3) | 2.104 | 2.47 | 2.10 | 0 | expander |
| preferential attachment | 1.237 | 2.94 | 0.69 | 0 | small-world |
| random geometric | 1.339 | 0.90 | 1.15 | 9 | (largest component, N≈55) |

The candidate is cleanly distinguishable from every null on the optimized local structure — that
part is fine. The decisive point is the rewire: scrambling edges while preserving the degree
sequence destroys the candidate's gluing proxies but pushes d_s **up** toward the grid. So the
package of local structure the objective buys is not "closer to a 2D manifold" in the metric that
matters. Being better than a bad null is not the bar; the bar is manifold-grade holdouts, and the
candidate does not clear it.

## Defect-density scaling — the pivotal question

A manifolding story requires local and boundary defect densities to fall toward zero with N.
They do not:

- bridge fraction: 0.029, 0.025, 0.026, 0.045, 0.028 — flat.
- articulation fraction: 0.255, 0.258, 0.215, 0.244, 0.211 — flat.
- bad-link fraction: 0.040, 0.037, 0.033, 0.030, 0.029 — shallow decline, far from zero.
- single-simple-boundary rate: 50%, 33%, 50%, 33%, (100% at 3 seeds) — no clean improvement.

## Verdict

The phrase **"2D manifold candidate" is not supported and is removed** on this branch, per the
acceptance rule that link and boundary defects must trend to zero. They do not. Three independent
obstructions each suffice on their own, and all three hold together:

1. **Substrate.** The delivered object is a graph. Its only canonical 2-complex (planar
   face-filling) is a topological disk by construction, so global homology certifies nothing;
   and even that construction fails on the non-planar seeds.
2. **Local topology.** Bridges (≈0.03 of edges), articulation points (≈0.22 of vertices),
   non-simple boundaries (majority of seeds), and a small but non-vanishing bad-link / bad-edge-
   incidence population persist at every N and do not decay.
3. **Scaling.** Spectral dimension is stuck at ≈1.1–1.3 while matched grids reach ≈1.9; the gap
   widens with N under two independent estimators.

What survives review, stated without inflation: the `_sandwich` construction reproducibly
produces a **planar sparse-graph phase with strong local 2-face-gluing proxies and improved
aspect ratio** relative to the earlier tube phase, and it is distinguishable from standard sparse
null models. A defensible claim is: "a planar graph phase with strong local 2-face-gluing proxies
under this objective; whether it defines a 2D cell/simplicial manifold remains open." The words
"manifold," "quad-lattice-grade" (as topology), and "isotropic 2D selection" overstate the
evidence.

## What would flip this result

A future version overturns this only by (a) declaring a deterministic 2-cell construction that is
not the short-cycle proxy and justifying it; (b) showing bridges, articulation points, bad links
and bad edge-incidences all trend to zero with N; (c) producing a stable simple-boundary
structure; (d) showing d_s and d_H move toward matched 2D controls under increasing N — not just
away from trees and poor nulls; (e) surviving the same holdouts against degree-preserving rewires.
Curvature and continuum language should wait until (a)–(d) hold.

## Reproducibility

```bash
# from the emergence/ project root, with networkx installed
pip install networkx --break-system-packages

# calibration (must all pass before trusting any number below)
PYTHONPATH=. python3 tooling/referee_2d_selftest.py

# topology sweep (chunk by N to taste; results checkpoint per seed)
PYTHONPATH=. python3 tooling/referee_2d_topology.py \
    --sizes 100 150 200 256 400 --seeds 6 --steps-per-n 120 --controls \
    --out tooling/artifacts/topology_sweep.json

# scaling sweep with the full null panel
PYTHONPATH=. python3 tooling/referee_2d_scaling.py \
    --sizes 100 150 200 256 --seeds 4 --steps-per-n 120 --nulls \
    --out tooling/artifacts/scaling_sweep.json
```

Environment: Python 3.10, networkx 3.4.2, numpy 2.2.6. Generator output is unchanged whether or
not networkx is present (it is used only for the holdout embedding, never by `_sandwich`).

## Files on this branch

- `tooling/referee_2d_topology.py` — 2-complex construction + topology census.
- `tooling/referee_2d_scaling.py` — independent holdout dimension estimators + null panel.
- `tooling/referee_2d_selftest.py` — calibration on known-topology objects (22 checks).
- `tooling/_merge_artifacts.py` — merges chunked per-N runs into one sweep file.
- `tooling/artifacts/topology_sweep.json`, `tooling/artifacts/scaling_sweep.json` — raw data.
- `tooling/REFEREE_2D_RESULTS.md` — this file.
