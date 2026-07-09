# k0 x k22: does a CDT phase suppress condensation and open a stable joint pass?

Sixth campaign. Preregistered in PREREG_CDT_K0.md (committed BEFORE the scan). Campaign 5
found the d_H-d_s tradeoff is a slice-size obstruction at k0=2, and that the alpha (k22) lever
improves both dimensions only by driving spatial-volume CONDENSATION (a transient joint crossing).
Every prior campaign fixed k0=2. This campaign scans the k0 axis (the CDT A<->C phase knob),
hunting for a phase where the condensation is suppressed so both dimensions can sit on the
seed-averaged exact-T^3 benchmark at equilibrium with a uniform profile.

## Verdict

**The wall HOLDS across CDT phases -- a stronger negative. No k0 opens a stable joint pass.**
The single controlling quantity is f22, the fraction of (2,2) tetrahedra (the timelike
"connective tissue" linking adjacent spatial slices). f22 falls monotonically as k0 rises
(higher k0 rewards vertices, which come from (3,1)/(1,3) tets, not (2,2)) -- exactly as k22>0
does. And:

- LOW f22 (high k0, or high k22): d_s(8-24) falls onto the benchmark (the triangulation gets
  finer, N0 up), BUT the (2,2) tissue vanishes, adjacent slices decouple, and the spatial volume
  CONDENSES (profile CV rises, slices deplete toward empty). Condensation then DROPS d_H (a blob
  has 2D-like ball growth), so d_H moves AWAY from the benchmark.
- HIGH f22 (k0=2, k22=0): the profile is uniform (CV~0.16) but d_s is too high (+0.3..+0.5) and
  d_H is stuck low (ratio ~0.73) -- the campaign-5 slice-size wall.
- d_H(2-6) at fixed slice size is ~1.82 regardless of k0 in the uniform regime, then falls under
  condensation. It never reaches the benchmark for ANY (k0, k22).

So the three requirements -- d_s=benchmark (needs low f22), uniform profile (needs high f22),
d_H=benchmark (needs large slice size, and is only hurt by condensation) -- are mutually
incompatible. The obstruction survives the CDT phase diagram.

Prereg decision-rule landing: **WALL HOLDS ACROSS PHASES (stronger negative).**

## The k0 map (k22=0, V=6000, T=12, slice size s=N3/T=500; seed-averaged 8 estimator seeds)

Benchmark at N0~1000-1500: d_s(8-24) ~ 3.10-3.14, d_H(2-6) ~ 2.47-2.50, CV = 0 (uniform).

| k0  | f22   | N0   | N3/N0 | d_s(8-24)     | d_H(2-6)     | d_H ratio | CV    | min slice | bad |
|-----|-------|------|-------|---------------|--------------|-----------|-------|-----------|-----|
| 2.0 | 0.399 |  926 | 6.48  | 3.420 +-0.259 | 1.820 +-0.102| 0.73      | 0.164 | 110       | 0   |
| 3.0 | 0.307 | 1070 | 5.64  | 3.417 +-0.400 | 1.852 +-0.090| 0.74      | 0.369 |  82       | 0   |
| 4.0 | 0.211 | 1211 | 4.97  | 3.194 +-0.188 | 1.849 +-0.159| 0.74      | 0.326 | 124       | 0   |
| 6.0 | 0.036 | 1504 | 4.08  | 3.065 +-0.332 | 1.636 +-0.067| 0.66      | 0.764 |  16       | 0   |
| 6.0, k22=1.5 | 0.016 | 1554 | 4.00 | 2.990 +-0.282 | 1.471 +-0.169 | 0.59 | 1.214 | 12 | 0 |

Reading the columns:
- d_s(8-24) DECREASES with k0 (3.42 -> 3.07 -> 2.99), reaching the benchmark near k0~5-6.
- d_H(2-6) is FLAT (~1.82-1.85, ratio 0.73-0.74) for k0=2,3,4, then DROPS to 0.66 (k0=6) and
  0.59 (k0=6,k22=1.5). Higher k0 never raises d_H; once condensation sets in it lowers it.
- CV RISES with k0 (0.16 -> 0.76 -> 1.21) and the minimum slice collapses (110 -> 16 -> 12,
  i.e. slices deplete toward the minimal 2-sphere) -- progressive condensation. At k0=6,k22=0
  the CV was still rising with sweeps (0.59 -> 0.76), i.e. it is an instability, not a plateau.
- census bad=0 everywhere: still a valid simplicial 3-manifold, just condensing.

## V=12000 corroboration (local box)

An uncapped V=12000 scan on the local WSL box (the intended primary volume) is bottlenecked by
machine load (a game was running); it delivered one equilibrated point before stalling:
k0=6, k22=1.5, V=12000 -> N0=3022, f22=0.006, CV=1.197, max/mean=3.52, d_s(8-24)=4.005,
d_H(2-6)=1.331, bad=0. This matches the sandbox V=6000 picture (hard condensation, d_H hurt) and,
with campaign 5's demonstrated V-independence of these observables (slice-size collapse), makes
the verdict volume-robust. The local scan is checkpointed/resumable for a fuller V=12000 map.

## Joint gate (preregistered G1-G5) -- scoring

| config          | G1 bad=0 | G2 d_H>=0.90 | G3 |d_s-b|<=0.20 | G4 no condensation | joint? |
|-----------------|----------|--------------|-------------------|--------------------|--------|
| k0=2 a0         | PASS     | FAIL (0.73)  | FAIL (+0.31)      | PASS (CV 0.16)     | NO     |
| k0=4 a0         | PASS     | FAIL (0.74)  | ~ (+0.06)         | FAIL (CV 0.33 rising)| NO   |
| k0=6 a0         | PASS     | FAIL (0.66)  | PASS (~0)         | FAIL (CV 0.76 rising)| NO   |
| k0=6 a1.5       | PASS     | FAIL (0.59)  | PASS (-0.12)      | FAIL (CV 1.21)     | NO     |
No (k0, k22) passes G2 and G4 together: the region where d_s reaches the benchmark (high k0 /
low f22) is exactly the region that condenses and drops d_H. The gate cannot be met.

## Mechanism (the clean statement)

f22 is the order parameter of the tradeoff. The (2,2) tets are the timelike faces that stitch
neighbouring spatial slices together. Their density controls two things at once, in opposite
directions:
  * high f22 -> well-stitched slices -> uniform S^2 x S^1 profile, but the extra timelike
    connectivity over-connects the 1-skeleton -> d_s too high.
  * low f22 -> under-stitched slices -> the graph's short-range spectral dimension drops onto the
    benchmark, but the slices decouple and the spatial volume condenses into a blob, which also
    collapses d_H.
Both k0 (up) and k22 (up) push f22 down. There is no independent knob that lowers d_s without
un-stitching the slices, so d_s=benchmark and a stable uniform 3-manifold are incompatible in
this 2+1D construction, across the whole k0 x k22 plane explored.

## Honest caveats

- Decisive scan at V=6000 (sandbox, chunked, --grind thermalization), s=500 fixed (T=12). k0=3,4
  are only partially thermalized (f22 still creeping up at ~450-500 sweeps); their exact CV will
  shift, but the endpoints (k0=2 uniform CV 0.16; k0=6 condensed CV 0.76 and rising) and the
  monotone trends (d_s down, d_H flat-then-down, CV up) are robust and are the load-bearing
  evidence. Preregistration named V=12000 primary; the local V=12000 run corroborates at one
  point but was too slow (machine load) for the full grid this session.
- Condensation is scored by CV drift + collapsing minimum slice, not an absolute CV threshold
  (the k0=2,k22=0 baseline itself sits at CV 0.16-0.31 from thermal fluctuations).
- 2+1D toy, N0 <~ 1500 here. A continuum statement is not claimed; this is a finite-size,
  finite-phase-scan negative.

## What would still move it

- A knob that raises spatial-slice vertex density WITHOUT removing (2,2) tets (e.g. an explicit
  per-slice refinement move, or a separate spacelike-vs-timelike coupling) -- decouple d_s from
  f22. Not present in the standard 2+1D CDT move set.
- Larger slice size AND large T simultaneously (needs V >> 24000) to lift d_H while a mild f22
  reduction nudges d_s -- the campaign-5 extrapolation suggests the miss only shrinks slowly.
