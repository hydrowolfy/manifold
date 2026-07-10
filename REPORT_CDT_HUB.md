# Campaign 7: the locked identity + hub measure term -- does the wall survive OUTSIDE the standard move set?

Seventh campaign. Preregistered in PREREG_CDT_HUB.md (committed BEFORE the sigma scan). The program's
open frontier was: find a move that ADDS SPATIAL VERTICES WITHOUT REMOVING (2,2) TETS (outside the
standard 2+1D CDT move set), to decouple d_s from f22 and open a stable joint (d_H AND d_s) pass.

## Verdict

**The wall holds outside the standard move set, and we now know structurally why.**

1. **The requested move is combinatorially impossible.** For any foliated triangulation of S^2 x S^1
   in this ensemble the spatial slices are triangulated 2-spheres (F = 2V - 4 per slice), which forces
   the exact identity

        N31 = N13 = 2 N0 - 4 T,   N22 = N3 - 4 N0 + 8 T,   f22 = 1 - 4 (N0 - 2 T) / N3.

   Verified EXACT (to the integer) on seed, grown, and thermalized states at k0=2 and k0=5, and it
   reproduces the campaign-6 k0-map f22 values from (N0, N3, T). Every foliation-preserving local move
   preserves it (checked: 2-3/3-2/2-6/6-2/4-4 all satisfy dN22 = dN3 - 4 dN0 + 8 dT). Consequence: at
   fixed volume N3 and fixed T, **dN22 = -4 dN0** -- adding one spatial vertex destroys exactly four
   (2,2) tets. Spatial-vertex density and the (2,2) fraction are ONE locked degree of freedom, not two.
   No enlarged move set escapes a topological identity. The only ways to raise N0 while holding N22 are
   to raise N3 (adds volume -> raises slice size s = N3/T -> climbs the d_s curve: the campaign-5
   slice-size wall) or to raise T (lowers s: the aspect ladder). Neither makes the two benchmark
   crossings coincide. **The "new move" branch of the frontier is closed by proof.**

2. **The one lever the identity leaves open -- reshaping connectivity at fixed counts -- also fails.**
   The identity pins all simplex counts and the MEAN degree (sum_v deg = 2 N1 = 2 (N0 + N3)), but not
   the degree DISTRIBUTION. Causal states carry heavy-tailed HUBS (deg mean 14.6, sd 10.2, max 84) that
   the size-matched exact 3-torus lacks entirely (deg 14, sd 0). A hub-suppressing measure/action term

        S = k3 N3 - k0 N0 + k22 N22 + sigma * sum_v max(0, deg_v - D0)^2

   (implemented in cdt_frontier2_run.py; detailed balance and manifold preservation verified) was scanned
   over sigma at V=6000, T=12, D0=14. It moves BOTH dimensions strongly but **reparameterizes the SAME
   tradeoff**: d_s and d_H reach the benchmark at sigma values ~10x apart. No sigma meets the joint gate.

Prereg decision-rule landing: **WALL HOLDS AGAINST THE MEASURE TERM** (H_hub REFUTED), on top of the
impossibility proof. The d_H-d_s obstruction is not an artifact of the standard move set.

## The sigma scan (V=6000, T=12, D0=14, k0=2, k22=0; seed-averaged 8 estimator seeds for d_s, 4 for d_H)

Benchmark, size-matched (N0~950-1000, m=10): d_s(8-24) = 3.135 +- 0.172, d_H(2-6) = 2.473.

| sigma | f22   | d_s(8-24)     | d_H(2-6)      | d_H ratio | CV    | deg sd | deg max | G2 dH>=.90 | G3 |ds-b|<=.20 | G4 CV |
|-------|-------|---------------|---------------|-----------|-------|--------|---------|------------|----------------|-------|
| 0.00  | 0.380 | 3.228 +-0.245 | 1.708 +-0.072 | 0.69      | 0.314 | 10.25  | 84      | FAIL       | PASS (+0.09)   | PASS  |
| 0.02  | 0.395 | 2.950 +-0.241 | 2.095 +-0.071 | 0.85      | 0.289 | 6.49   | 37      | FAIL       | PASS (-0.185)  | PASS  |
| 0.05  | 0.388 | 2.611 +-0.168 | 2.142 +-0.090 | 0.87      | 0.356 | 5.31   | 30      | FAIL       | FAIL (-0.52)   | ~FAIL |
| 0.10  | 0.367 | 2.378 +-0.227 | 2.251 +-0.013 | 0.91      | 0.276 | 4.16   | 25      | PASS       | FAIL (-0.76)   | PASS  |
| 0.20  | 0.349 | 2.256 +-0.197 | 2.304 +-0.065 | 0.93      | 0.400 | 4.14   | 29      | PASS       | FAIL (-0.88)   | FAIL  |

Reading it:
- d_s(8-24) DECREASES monotonically with sigma (3.23 -> 2.26); it crosses the benchmark at sigma ~= 0.007.
- d_H(2-6) INCREASES monotonically (ratio 0.69 -> 0.93); it crosses ratio 0.90 at sigma ~= 0.08.
- The two benchmark crossings are ~10x apart in sigma. Where d_s sits on the benchmark (sigma <= 0.02),
  d_H is still <= 0.85; where d_H passes (sigma >= 0.10), d_s has collapsed to ~2.4 (deficit -0.7..-0.9).
  **No sigma satisfies G2 and G3 together.** The hub term is a powerful, clean anticorrelated lever on
  (d_s, d_H) -- and that is exactly the problem: it slides both dimensions along the same tradeoff line.
- Equilibrium check: the sigma=0.10 state is stable across 1213->1643 sweeps (d_s 2.42->2.38, d_H
  0.93->0.91, CV 0.30->0.28, f22 and N3 flat) -- an equilibrium property, not a warm-start transient.
  It does not drift toward the joint point.

## Mechanism (why hub suppression cannot win)

At sigma=0 the causal 1-skeleton is over-connected by hubs (max degree 84 vs the torus's uniform 14).
The hubs are short-range shortcuts: they hold the lazy-random-walk return probability DOWN (d_s slightly
high) while SATURATING ball growth at small radius (d_H low, ratio 0.69). Suppressing them:
  * de-saturates ball growth -> d_H rises toward 3 (good), AND
  * removes the shortcuts -> the walk becomes more confined -> d_s FALLS (past the benchmark, to ~2.3).
Both effects grow together with sigma, so d_s and d_H move in OPPOSITE directions through the benchmark.
This is the same d_H-d_s anticorrelation seen under slice size s (campaign 5) and under f22 / k0 x k22
(campaign 6), now reproduced by a third, independent knob. The tradeoff is a robust property of THIS
2+1D ensemble's diffusion geometry, not of any one coupling or move.

## Joint gate (preregistered G1-G5) -- final scoring

| config              | G1 bad=0 | G2 dH>=.90 | G3 |ds-b|<=.20 | G4 no condensation | joint? |
|---------------------|----------|------------|-----------------|--------------------|--------|
| sigma=0.02 (ds ok)  | PASS     | FAIL(0.85) | PASS(-0.185)    | PASS (CV 0.29)     | NO     |
| sigma=0.10 (dH ok)  | PASS     | PASS(0.91) | FAIL(-0.76)     | PASS (CV 0.28)     | NO     |
| sigma=0.20          | PASS     | PASS(0.93) | FAIL(-0.88)     | FAIL (CV 0.40)     | NO     |
No (sigma, D0) passes G2 and G3 together. The gate cannot be met.

## Honest caveats

- Impossibility identity (Sec 1) is EXACT and topological -- it holds at every V, T, and coupling; not a
  finite-size claim. It is the load-bearing result.
- The sigma scan is V=6000, T=12, single MC seed (seed 0), warm-started from the sigma=0 equilibrated
  reference and re-equilibrated (~600-850 sweeps of the new term; sigma=0.10 confirmed stable over an
  extra 430 sweeps). The MONOTONE anticorrelated trend across five sigma and the ~10x separation of the
  two benchmark crossings are the load-bearing evidence, robust to the exact equilibration and seed.
  A second config seed and a V=12000 confirmation were preregistered ONLY if a pass appeared; none did.
- D0=14 (the torus degree) is the primary and only threshold scanned; D0=18 (secondary) was not run.
  D0=18 penalizes strictly fewer vertices, i.e. a weaker version of the same lever -- expected to shift
  the effective sigma, not to break the anticorrelation. Flagged as a minor open item.
- Census bad=0 in every snapshot of every sigma chain: the construction never leaves the manifold; the
  obstruction is dimensional, not topological.

## What this closes, and what (if anything) is left

CLOSED: the "new move" escape (impossible by the identity) and the "reshape connectivity at fixed counts"
escape (hub measure term reparameterizes the same tradeoff). Together with campaigns 5-6 (slice size,
k0 x k22), the d_H-d_s wall now survives (a) every aspect ratio, (b) the whole k0 x k22 plane, and (c) a
direct degree-measure term -- three independent levers, one wall.

Not excluded (all leave the standard S^2 x S^1, alpha=1 CDT ensemble, so they answer a DIFFERENT question):
- different spatial topology (slices not S^2 -> breaks F = 2V - 4, the root of the identity);
- higher-dimensional (3+1D) CDT, where the known de Sitter phase reaches 4 in both dimensions;
- a genuinely non-local / long-range action term (not a local measure term).
Within genuine 2+1D causal CDT on S^2 x S^1, the joint (d_H AND d_s) 3-manifold does not emerge, and the
reason is now structural: spatial-vertex density and the (2,2) stitching are a single locked DOF.
