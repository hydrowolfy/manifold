# Hub / measure term: can suppressing 1-skeleton hubs open a STABLE joint d_H+d_s 3-manifold?

Seventh campaign. Preregistered in `PREREG_CDT_HUB.md` (committed BEFORE the scan). Campaigns 5-6
established the d_H-d_s tradeoff as a slice-size / f22 obstruction that holds across the whole
k0 x k22 plane; the only escape the program could still name was "a move that raises spatial
vertex density WITHOUT removing (2,2) tets -- not in the standard 2+1D move set." This campaign
does two things: (A) proves that requested move is combinatorially impossible, and (B) scans the
one lever the proof leaves open -- a hub-suppressing measure term outside standard Regge CDT.

## Verdict

**The wall holds -- even outside the standard 2+1D move set.** Two independent results:

- **(A) The "new move" is impossible.** For any foliation-preserving triangulation of S^2 x S^1
  (spatial slices are 2-spheres, F = 2V-4 per slice), the simplex counts satisfy the EXACT identity
  N31 = N13 = 2 N0 - 4 T and **N22 = N3 - 4 N0 + 8 T**. Hence at fixed volume N3 and time-extent T,
  dN22 = -4 dN0: adding one spatial vertex destroys exactly four (2,2) tets. This is an Euler-
  characteristic identity, independent of the moves that generate the state, so NO enlarged or exotic
  move set escapes it. Verified EXACTLY (integer) on seed, grown, and thermalized states at k0=2 and
  k0=5, with the finite-difference slope (dN22 - dN3)/dN0 = -4.0000. The frontier's hoped-for escape
  is closed by proof.

- **(B) The hub measure term does not open a joint pass.** Adding S += sigma * sum_v max(0, deg_v - D0)^2
  (a non-Regge term that regularizes the 1-skeleton degree distribution at FIXED simplex counts, hence
  fixed f22) lifts d_H(2-6) all the way to the benchmark AT A UNIFORM PROFILE -- something neither k0
  nor k22 could do -- but simultaneously drives d_s(8-24) DOWN through the benchmark and far below.
  The gate-passing regions are disjoint: d_H passes (>=0.90 benchmark) only for sigma >= 0.05, d_s
  passes (|.-b|<=0.20) only for sigma <= 0.02. No sigma passes both. Confirmed on two independent
  estimator-seed sets and at D0=18.

Prereg decision-rule landing: **WALL HOLDS AGAINST THE MEASURE TERM.** Combined with the identity (A),
this closes the frontier: neither a new move (impossible) nor a hub-measure term beats the wall.
The one genuine advance is that hub suppression decouples d_H from condensation -- the tradeoff is
reparameterized (hub density replaces f22 as the knob), not eliminated.

## Physics gate (trust check, before any claim)

Zero-dependency + networkx runners both PASS the causal self-test (typed (3,1)/(2,2)/(1,3) seed,
five foliation-preserving Pachner moves, census bad=0, slices are 2-spheres) and reproduce the
frozen seed-averaged benchmark EXACTLY: exact T^3 Kuhn torus m=13 -> d_s(8-24) = 3.071 +- 0.160
(== the frozen 3.071). Hub-term detailed balance verified directly: over a 6000-step sigma>0 chain,
_degpen_delta == (pen_after - pen_before) to max error 0.0 on all 394 accepted moves, and the
incremental degree cache equalled the from-scratch degree at every step (the penalty is a state
function, so an exact delta gives detailed balance; the reverse move's delta is its negation).

## (A) The locked-identity impossibility result (proven, then verified)

Each spatial slice is a triangulated 2-sphere, so F_slice = 2 V_slice - 4 (Euler, chi=2). Each
spatial triangle is the base of exactly one (3,1) tet (pointing up) and one (1,3) (pointing down),
so summing over the T slices:  N31 = N13 = sum_slices (2 V_slice - 4) = 2 N0 - 4 T. With
N3 = N31 + N22 + N13,  N22 = N3 - 4 N0 + 8 T,  and  f22 = 1 - 4 (N0 - 2 T)/N3.

Independent check (`verify_identity.py`), recomputing every count from the census:

| k0  | state              | N0  | N3   | N31=N13 (pred) | N22 (pred)  | identity |
|-----|--------------------|-----|------|----------------|-------------|----------|
| 2.0 | seed               | 72  | 288  | 96 (96)        | 96 (96)     | EXACT    |
| 2.0 | grown ~2400        | 675 | 2761 | 1302 (1302)    | 157 (157)   | EXACT    |
| 2.0 | thermalized +300sw | 417 | 2554 | 786 (786)      | 982 (982)   | EXACT    |
| 5.0 | thermalized +300sw | 608 | 2673 | 1168 (1168)    | 337 (337)   | EXACT    |

Finite-difference across the grown->thermalized step (fixed T): (dN22 - dN3)/dN0 = -4.0000 both k0.
**Spatial-vertex density and (2,2)-fraction are one locked degree of freedom.** The only ways to raise
N0 while holding N22 are to raise N3 (adds volume -> climbs the slice-size d_s curve: the campaign-5
wall) or raise T (lowers slice size: the aspect ladder). Neither decouples the two benchmark crossings.
No move set escapes an Euler identity. The "add vertices without removing (2,2) tets" branch is closed.

## (B) The hub measure-term scan (V=6000, T=12, k0=2, s=N3/T=500)

Warm-started from the same k0=2 sigma=0 equilibrated reference (N0=933, f22=0.393, CV 0.215),
re-equilibrated at each sigma (f22 + profile-CV to a plateau, ~600-780 sweeps), seed-averaged over
8 estimator seeds (seedbase 200). Benchmark (m=10, N0~1000): d_s(8-24)=3.135, d_H(2-6)=2.473.
Gate: G2 d_H >= 0.90*b = 2.226 ; G3 |d_s(8-24) - 3.135| <= 0.20 -> d_s in [2.935, 3.335].

| D0 | sigma | N0  | f22   | CV    | deg sd | deg max | d_s(8-24)    | d_s(16-48) | d_H(2-6)     | G2 | G3 |
|----|-------|-----|-------|-------|--------|---------|--------------|-----------|--------------|----|----|
| 14 | 0.00  | 933 | 0.393 | 0.215 | 10.43  | 80      | 3.243+-0.414 | 2.42      | 1.843+-0.131 | F  | P  |
| 14 | 0.02  | 924 | 0.401 | 0.253 |  6.47  | 36      | 2.981+-0.260 | 2.45      | 2.131+-0.092 | F  | P  |
| 14 | 0.03  | 932 | 0.396 | 0.215 |  ~5.5  | 30      | 2.784+-0.274 | 2.32      | 2.173+-0.100 | F  | F  |
| 14 | 0.04  | 925 | 0.398 | 0.216 |  ~5.0  | 30      | 2.661+-0.386 | 2.04      | 2.215+-0.092 | F  | F  |
| 14 | 0.05  | 936 | 0.391 | 0.227 |  4.96  | 28      | 2.836+-0.265 | 2.38      | 2.229+-0.116 | P  | F  |
| 14 | 0.10  | 956 | 0.380 | 0.236 |  4.21  | 23      | 2.430+-0.300 | 2.04      | 2.312+-0.089 | P  | F  |
| 14 | 0.20  | 997 | 0.354 | 0.275 |  3.61  | 21      | 2.279+-0.198 | 1.92      | 2.426+-0.075 | P  | F  |
| 18 | 0.10  | 918 | 0.403 | 0.237 |  ~4.6  | 26      | 2.837+-0.225 | 2.32      | 2.197+-0.114 | F  | F  |

census bad=0 in every row. Reading it:
- The term does exactly what it should to the connectivity: deg sd collapses 10.4 -> 3.6 and deg max
  80 -> 21 (toward the regular torus, deg 14 sd 0), while deg mean stays ~14-15 (fixed by the identity).
- **d_H(2-6) rises monotonically to the benchmark: 1.84 -> 2.43 (ratio 0.74 -> 0.98) at a UNIFORM
  profile** (CV 0.16-0.28, no upward drift, min slice never collapses -> G4 passes everywhere). This is
  the campaign's one real advance: k0/k22 could only raise d_H by CONDENSING (which then dropped it);
  the hub term raises it with the profile intact.
- **d_s(8-24) falls monotonically THROUGH the benchmark and keeps going: 3.24 -> 2.28.** It is already
  within gate at sigma=0 (+0.11) and overshoots below by sigma=0.05. The long window (16-48) falls too
  (2.42 -> 1.92), so the overshoot is real, not a short-window lattice artifact.
- **The pass regions are disjoint.** G2 needs sigma >= 0.05; G3 needs sigma <= 0.02. At the crossover
  (sigma 0.03-0.04) BOTH miss (d_s ~2.7 |.|~0.4 low; d_H ratio ~0.88-0.90). No sigma sits both on
  benchmark. D0=18 (a weaker constraint) rescales the effective coupling onto the SAME (d_s,d_H) locus
  (sigma=0.10,D0=18 ~ sigma=0.05,D0=14) and also fails both -- the tradeoff curve is D0-independent.

Robustness (G5): an independent estimator-seed re-measure (seedbase 700) reproduces every trend within
the quoted sd (d_s: 3.29/2.84/2.84/2.26 ; d_H: 1.75/2.09/2.22/2.38 at sigma 0/0.02/0.05/0.20). On that
seed set even sigma=0.02 gives d_s=2.84 (fails G3) and d_H=2.09 (fails G2), i.e. the G3 window is even
narrower -- tightening, not loosening, the negative.

## Mechanism (the clean statement)

Heavy-degree HUB vertices are the only connectivity freedom the identity leaves free (it pins the
simplex counts and the mean degree sum_v deg = 2 N1 = 2(N0+N3), but not the degree DISTRIBUTION; a
k0=2 causal state has deg mean 14.6 sd 10.4 max 84 vs the perfectly regular torus deg 14 sd 0). Hubs
do two opposing things at once: they OVER-CONNECT the 1-skeleton (fast return probability -> d_s too
high) and they SATURATE ball growth (a few high-degree vertices reach everything in a few steps ->
d_H too low). Suppressing them therefore moves both dimensions toward the benchmark from OPPOSITE
sides. But the single knob sigma crosses the two benchmarks at ~10x-different couplings: d_s is only
+0.1 above benchmark at sigma=0 and overshoots immediately as the skeleton over-regularizes, whereas
d_H starts at ratio 0.74 and needs strong suppression (sigma~0.2) to desaturate. There is no sigma
where the already-near d_s still sits on benchmark while the far d_H has caught up. Hub density is a
new order parameter for the SAME tradeoff -- reparameterized off f22, not removed.

## Honest caveats

- V=6000, T=12 only (s=500, N0~920-1000). The identity (A) is exact at every V; the scan (B) is a
  finite-size result at one slice size. Campaign 5 showed d_s/d_H collapse on slice size (V-independent),
  and the hub mechanism is local, so the disjointness is not expected to close at larger V -- but this
  is an argument, not a measured V=12000 confirmation (no pass appeared, so the prereg's V=12000 check
  was not triggered).
- Equilibration is 600-780 warm-started sweeps per point with f22 + CV plateau; the monotone d_s/d_H
  trends and bad=0 are the load-bearing evidence, not any single point's third decimal.
- d_s(16-48) is the noisy secondary window (sd 0.3-0.6); it is used only to confirm the d_s overshoot
  is not a short-window artifact, which it does.
- The gate is deliberately strict (G3 half-width 0.20 ~ one benchmark sd). Loosening it would not
  produce a joint pass: the crossover point still misses BOTH, because d_s is ~0.3-0.5 below benchmark
  exactly where d_H first reaches ratio 0.90.

## What would move it next (open, ranked)

1. A term that lowers d_s WITHOUT touching d_H (e.g. penalize short-range 1-skeleton loops / spectral
   gap directly) rather than hubs, which move both -- the tradeoff needs TWO independent knobs, one per
   dimension, and the identity guarantees the simplex sector cannot supply the second.
2. V >> 24000 with a genuinely thin large-T aspect (s~385, T~60), to put a measured d_H at the
   d_s-benchmark slice size at top volume -- the campaign-5 route, orthogonal to the hub knob.
3. A different discrete target (higher-genus spatial slices) changes the identity to N22 =
   N3 - 4N0 + 8T - 8*sum_slice(genus); this ADDS (2,2)-room but requires abandoning S^2 x S^1 -- a
   different ensemble, worth a separate program, not a move within this one.
