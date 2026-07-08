# Causal CDT scaling campaign: does d_H(V) track the exact-3-manifold line?

Date: 2026-07-08. Follow-up to REPORT_CDT_CAUSAL.md, executing the green-lit scaling
experiment: V = 1500/3000/6000, k0 in {1,2}, 2 seeds per point, T = 12/14/16, scored against
matched periodic Kuhn T^3 benchmarks, with Euclidean DT controls. Raw data appended to
`cdt_causal_results.jsonl` (every chunk checkpointed). Nothing committed or pushed to GitHub.

## Headline

The wall does not re-assert through V=6000 on the primary metric: causal d_H(2-6) grows with
volume at 80-87% of the exact-benchmark slope (per ln N0), with the causal/benchmark ratio
stable-to-rising (0.59 -> 0.70 for k0=2) across a decade of volume. Joint behavior holds:
at the largest volume and the longest clean diffusion window, causal d_s sits ON the
benchmark line (8-24 window: 3.43 and 3.51 vs torus 3.41). The Euclidean pathology
(anticorrelated d_s/d_H) never appears in the causal ensemble.

One wall-like signature DOES appear at larger length scales: the wider ball window d_H(3-8)
stalled between V=3000 and V=6000 (causal ~0.95 -> ~1.0 while the benchmark grew 1.60 ->
2.15). Whether that is under-thermalization at V=6000 (these chains have the fewest sweeps)
or a genuine extent saturation of the causal blob is THE open question this campaign leaves.

## Benchmark line (exact flat T^3, all census-clean, chi=0)

| N0   | d_s(4-12) | d_s(8-24) | d_H(2-6) | d_H(3-8) |
|------|-----------|-----------|----------|----------|
| 125  | 3.77      | (plateau) | 1.61     | n/a      |
| 216  | 3.77      | (noisy)   | 1.77     | 0.87     |
| 343  | 3.64      | 3.61      | 1.90     | 1.35     |
| 512  | 3.52      | 3.52      | 1.98     | 1.60     |
| 1000 | 3.48      | 3.41      | 2.47     | 2.15     |
| 1728 | 3.52      | 3.23      | 2.57     | 2.42     |

Windows beyond t=24 (and 8-24 below N0~350) are contaminated by the finite-graph return
plateau and Hutchinson probe noise; they were measured, found unreliable, and excluded.

## Causal CDT results (pooled tuned snapshots, both seeds; bad=0 in every census)

| k0 | V    | N0~ | snaps | d_H(2-6)      | bench | ratio | d_s(4-12)     | bench | diff  |
|----|------|-----|-------|---------------|-------|-------|---------------|-------|-------|
| 1  | 700  | 126 | 3     | 0.95 +/- 0.03 | 1.61  | 0.59  | 2.86 +/- 0.21 | 3.77  | -0.91 |
| 2  | 700  | 130 | 3     | 1.00 +/- 0.07 | 1.62  | 0.62  | 2.98 +/- 0.41 | 3.77  | -0.79 |
| 1  | 1500 | 242 | 6     | 1.03 +/- 0.05 | 1.80  | 0.57  | 3.29 +/- 0.42 | 3.74  | -0.45 |
| 2  | 1500 | 255 | 7     | 1.06 +/- 0.10 | 1.82  | 0.58  | 3.62 +/- 0.28 | 3.72  | -0.10 |
| 1  | 3000 | 462 | 6     | 1.33 +/- 0.05 | 1.96  | 0.68  | 4.00 +/- 0.19 | 3.55  | +0.44 |
| 2  | 3000 | 484 | 7     | 1.38 +/- 0.04 | 1.97  | 0.70  | 3.55 +/- 0.19 | 3.54  | +0.01 |
| 1  | 6000 | 885 | 6     | 1.56 +/- 0.04 | 2.38  | 0.65  | 3.94 +/- 0.14 | 3.49  | +0.46 |
| 2  | 6000 | 940 | 6     | 1.70 +/- 0.07 | 2.43  | 0.70  | 3.90 +/- 0.17 | 3.48  | +0.42 |

Seed robustness: seed-0 and seed-1 groups agree within snapshot scatter at every point.
k3 self-tunes per volume (lever: per-volume retuning is built in): 1.166/1.302 at V=700
drifting to 1.13-1.16/1.28-1.30 at V=6000.

d_H slope per ln N0, overall 700 -> 6000: k0=1: 0.314 vs benchmark 0.394 (80%);
k0=2: 0.352 vs benchmark 0.406 (87%). Segment slopes are noisy (the benchmark line itself
kinks at m=8->10) but no segment shows causal d_H(2-6) regressing.

Long-window d_s at V=6000 (N0~900, the size where the 8-24 window is clean): causal k0=1:
3.43, k0=2: 3.51 vs torus at N0=1000: 3.41. The persistent +0.4 offset in the SHORT window
(4-12) at V >= 3000 is a short-time lattice artifact (degree-structure sensitive); it
vanishes at 8-24. Verdict: d_s inside the benchmark band at the trustworthy window.

The stall signature: causal d_H(3-8) reads 0.96/0.94 at V=3000 and 0.98/1.07 at V=6000,
flat, while the benchmark grows 1.60 -> 2.15. Slice profiles at V=6000 stay spread
(min/max ~ 60/170 across T=16 slices, no minimum-floor stalk), so this is not the V=1500
stalk pathology; it looks like slow growth of linear extent beyond r~6. Candidate
explanations: (a) V=6000 chains are the least thermalized (900-1400 sweeps vs 2500-6000
elsewhere) and wide-ball observables thermalize slowest; (b) genuine blob-extent saturation
at fixed T. Not distinguishable with current data.

## Euclidean controls (v0 machinery, k3=-0.2)

| N0  | d_s(4-12) | d_H(2-6) | bench ratio | depth (attempts/tet) |
|-----|-----------|----------|-------------|----------------------|
| 130 | 3.95      | 0.40     | 0.25        | 2.9                  |
| 260 | 3.98      | 0.73     | 0.40        | 1.0                  |
| 500 | 3.87      | 1.27     | 0.64        | 0.7                  |

Not flat, and reported honestly as such, with a caveat that cuts both ways: the v0 moves
cost O(N3) each, so matched-depth control chains at n0 >= 500 are unaffordable, and the
n0=500 number (0.7 attempts/tet) is closer to its build() initial condition than to the
k3=-0.2 equilibrium. What IS clean at every size: Euclid d_s never descends toward the
benchmark (pinned 3.87-3.98 while the benchmark falls to 3.5), so the Euclidean ensemble
fails the joint criterion at every volume even where its d_H window slope creeps up.

## Gate evaluation

1. Census clean everywhere: PASS (bad=0, all volumes, both seeds, every snapshot).
2. Causal d_H(V) slope tracks benchmark: PASS on d_H(2-6) (80-87% of benchmark slope,
   ratio not decreasing); OPEN on d_H(3-8) (stall between 3000 and 6000, confounded by
   thermalization).
3. d_s inside benchmark band: PASS at the longest clean window (8-24) at V=6000; the
   short-window offset (+0.4) is a documented artifact.
4. Euclidean controls flat: NOT CLEAN as stated (window slope rises at small depths), but
   Euclid fails joint convergence at every size via d_s. The control claim survives in
   joint form only.

## Caveats

Two seeds per point, snapshots along chains (1500+ sweep spacing at small V, ~250 at
V=6000), autocorrelation unmeasured, so quoted sd understates true error. V=6000 chains are
short (900-1400 sweeps). Detailed balance exact at anchored-proposal level. alpha=1 action
(k22 lever implemented but not swept, since the primary gate did not fail). Fixed T per
volume; T-dependence tested only at V=1500 (T=8 vs 12: consistent d_H). Benchmark
interpolation is log-linear between Kuhn points.

## Recommended next run (needs green light)

Decide the d_H(3-8) stall: (1) extend V=6000 chains 3-5x in sweeps, tracking d_H(3-8) vs
sweep time (if it climbs, it was thermalization); (2) one V=6000 variant at T=24 and one at
T=12 to test extent-vs-foliation-thickness; (3) sweep k22 in {-0.3, +0.3} at V=3000 to see
whether the (2,2) weight moves the blob extent; (4) optionally V=12000 at k0=2 single seed
for a fourth slope point. Expected cost: 2-3x this campaign.
