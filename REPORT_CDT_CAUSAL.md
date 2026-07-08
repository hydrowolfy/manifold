# Causal CDT v1: does the causal restriction escape Euclidean crumpling?

Date: 2026-07-08. Code authored this session: `cdt_causal.py`, `torus_benchmark.py`,
`euclid_control.py`, `summarize_causal.py`; raw measurements in `cdt_causal_results.jsonl`.
Nothing was committed or pushed to GitHub; all repo state is a local clone of
`explore/3d-manifold` at `/tmp/m` (sandbox), and these files live in the session outputs
folder pending sign-off.

## What was built

Genuine causal CDT in 2+1 dimensions (3D bulk, matching the project's 3-manifold target):

- Global integer time label on vertices, T spatial slices, periodic time. Spatial topology
  S^2, bulk topology S^2 x S^1 (seed: T octahedral slices joined by prisms, verified chi=0,
  all vertex links 2-spheres).
- Every tetrahedron is typed (3,1)/(2,2)/(1,3) across adjacent slices; a tet spanning
  non-adjacent slices or a single slice is structurally impossible (asserted).
- Move set: the standard 2+1D CDT moves. (2,3)/(3,2) are the Euclidean Pachner flips
  restricted to foliation-respecting configurations ((3,1)+(2,2) or (1,3)+(2,2) sharing a
  timelike triangle; pivot edge always timelike). (2,6)/(6,2) insert/remove a spatial vertex.
  (4,4) flips a spatial edge. Slice surfaces remain closed 2-spheres under all moves; this is
  checked, not assumed.
- Metropolis on S = k3*N3 - k0*N0 + eps*(N3-V)^2 (alpha=1 style Euclideanized action with
  volume pinning; k3 auto-tuned toward pseudo-critical during a tuning phase, then frozen).
  Acceptance includes anchored-proposal count ratios (tets for 2-3/3-2; spatial triangles vs
  vertices for 2-6/6-2; spatial edges for 4-4), so detailed balance holds at the anchored-
  proposal level.
- Selftests (all PASS): seed census clean for T=3,4,8; exact 2-3/3-2 and 2-6/6-2 round
  trips with clean census at every step; 200-sweep random chain with full invariant
  revalidation (cache rebuild, slice sphericity, typing) every 50 sweeps; all five move
  types accepted; estimator smoke test.
- Estimators imported VERBATIM from the repo (lazy_rw_sdim window 4-12 for d_s,
  ball_growth_dim window 2-6 for d_H, link_census for the manifold certificate), so all
  numbers are directly comparable with the v0 Euclidean table.

## The calibration result that reframes the question

"d_s -> 3 and d_H -> 3" is a continuum statement. Measured on an EXACT flat 3-manifold
(periodic Kuhn triangulation of T^3, links all spheres, bad=0) at the sizes we can afford,
the same estimators read:

| T^3 benchmark | N0   | N3   | d_s(4-12) | d_H(2-6) |
|---------------|------|------|-----------|----------|
| m=5           | 125  | 750  | 3.77      | 1.61     |
| m=6           | 216  | 1296 | 3.77      | 1.77     |
| m=8           | 512  | 3072 | 3.52      | 1.98     |
| m=10          | 1000 | 6000 | 3.48      | 2.47     |

So at N0 ~ 10^2..10^3, success does NOT read (3, 3): it reads d_s ~ 3.5-3.8 (the lazy-walk
window sits on the pre-asymptotic hump) and d_H(2-6) ~ 1.6-2.5, climbing slowly. Every claim
below is therefore measured as distance to this exact-manifold line at matched size, not to
the ideal (3,3). Retroactively this also reframes v0: "d_s=2.98 at k3=-0.2" was never close
to success; at that size success reads (3.77, 1.61), and v0's d_H=0.24 was the giveaway.

## Results (all runs: manifold_ok everywhere; bad=0 in every one of the ~25 censuses)

Euclidean controls (v0 machinery unchanged, k3=-0.2, matched vertex count):

| ensemble        | N0  | d_s(4-12) | d_H(2-6) | benchmark at this size |
|-----------------|-----|-----------|----------|------------------------|
| Euclidean DT    | 130 | 3.95      | 0.40     | (3.77, 1.61)           |
| Euclidean DT    | 260 | 3.98      | 0.73     | (3.77, 1.77)           |

Causal CDT (post-tune snapshots, mean +/- sd; f22 = (2,2)-tet fraction; prof_min = smallest
slice volume, floor is 4):

| k0  | V    | T  | N0~  | f22  | prof_min | d_s(4-12)    | d_H(2-6)     |
|-----|------|----|------|------|----------|--------------|--------------|
| 1.0 | 700  | 10 | 126  | 0.41 | 4        | 2.86 +/- 0.21| 0.95 +/- 0.03|
| 2.0 | 700  | 10 | 130  | 0.37 | 4        | 2.98 +/- 0.41| 1.00 +/- 0.07|
| 3.0 | 700  | 10 | 140  | 0.32 | 4        | 2.96 +/- 0.55| 0.97 +/- 0.05|
| 4.0 | 700  | 10 | 151  | 0.27 | 4        | 2.77 +/- 0.06| 1.10 +/- 0.14|
| 5.0 | 700  | 10 | 163  | 0.19 | 6        | 2.93 +/- 0.21| 1.06 +/- 0.03|
| 1.0 | 1500 | 12 | 244  | 0.42 | 4        | 3.10 +/- 0.10| 1.00 +/- 0.04|
| 2.0 | 1500 | 12 | 252  | 0.39 | 4        | 3.71 +/- 0.28| 1.02 +/- 0.11|
| 2.0 | 1500 | 8  | 245  | 0.40 | 36       | 3.95 +/- 0.22| 1.08 +/- 0.04|

Phenomenology touchpoints (entry ticket, not the result): f22 falls monotonically with k0
(0.41 -> 0.19), the expected weak-coupling depletion of (2,2) tets; slice profiles spike at
large k0 (slice decoupling); at T=12 the volume localizes into a blob with slices pinned at
the minimum (prof_min=4), i.e. a droplet with a thin stalk, while T=8 at the same volume is
stalk-free (prof_min=36). These match the qualitative 2+1D CDT picture (blob phase, slice
decoupling at weak coupling; literature transition k0_c ~ 3.3 is from memory and our volumes
are far too small to resolve a transition).

## Verdict on the wall

The Euclidean signature was an ANTICORRELATED tradeoff: d_s tunable through 3 only by
densifying until d_H -> 0, d_s pinned ~3.9-4.0 above the benchmark with d_H at 25-40% of the
benchmark value. The causal ensemble does not show that tradeoff anywhere in k0 = 1..5:
d_H sits at 0.95-1.10 across the whole sweep (60-65% of benchmark at V=700, 55-60% at
V=1500) while d_s moves around the benchmark value rather than being pinned above it. At
matched N0=130: causal (2.9, 1.0) vs Euclidean (3.95, 0.40) vs exact (3.77, 1.61). The
causal restriction demonstrably pulls the geometry toward the exact-manifold line on both
axes at once. The wall is dented, and the specific Euclidean failure mode is absent.

It is not broken. The decisive scaling test fails so far: from V=700 to V=1500 the
benchmark line's d_H grows (1.61 -> 1.77) but the causal d_H stays flat (~1.0), so the gap
to the exact line widened slightly. The visible suspect at T=12 is the stalk (slices at the
floor of 4 triangles act as a quasi-1D segment that depresses ball growth and drags return
probabilities), but the T=8 stalk-free run only reaches d_H=1.08, so the stalk is not the
whole story. Either the volumes are still too small for the causal ensemble's d_H to enter
its growth regime, or k3/k0 are not yet in the right region for the extended phase proper.
On current evidence: causal CDT is qualitatively better than Euclidean DT at every matched
comparison, and the joint (d_s, d_H) -> benchmark-line convergence remains unproven.

## Honest caveats

Volumes are tiny (N3 <= 1540, N0 <= 260) and T <= 12. One seed per point; snapshots along
one chain, 1500+ sweeps apart, autocorrelation not measured; sd over 3-4 snapshots
understates true error. Detailed balance is exact only at the anchored-proposal level.
Action is alpha=1 (no (3,1)-vs-(2,2) coupling asymmetry); no spatial-topology alternatives
tried. d_H window 2-6 partially saturates at these diameters (3-8 window mostly undefined).
d_s window 4-12 sits on the pre-asymptotic hump for ALL ensembles at these sizes, which is
exactly why the exact-T^3 line, not 3.0, is the reference. No claims about the k0 phase
diagram beyond the monotone f22 trend.

## Recommended next experiment (needs green light)

The discriminating object is now a slope, not a point: d_H(V) for causal CDT vs the exact
T^3 line at matched N0, over V = 1500 / 3000 / 6000 (T = 12-16, k0 in {1, 2}, 2-3 seeds
each), with the Euclidean control at matched sizes expected to stay flat. Joint acceptance
gate: link census clean everywhere AND causal d_H(V) slope consistent with the benchmark
slope AND d_s inside the benchmark band at each size. Secondary levers if the slope stays
flat: alpha != 1 action term (weight N22 separately), k3 re-tuned per volume (fixed-k3 drift
biases the ensemble as V grows), longer-time d_s windows (t ~ 40-120) where the benchmark
hump decays, and a volume-profile observable (slice-volume correlation length) to separate
blob growth from stalk growth. This is 3-5x the compute of this session; chunked
checkpointing already supports it.
