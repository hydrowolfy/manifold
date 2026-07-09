# Volume profile N3(t) at the near-misses: physical extended phase, or collapse?

Side-quest (a few runs, not a campaign). Preregistered in PREREG_CDT_PROFILE.md, committed FIRST
(commit 806353, before any study-state profile was measured). Answers open item #3 in HANDOFF §5:
at the parameter points where ONE of d_H / d_s reaches the exact-T^3 benchmark, is the geometry a
genuine physical extended phase or a collapse / condensation artifact? It decides how to read the
whole program's near-misses.

## Verdict (one line)

**The two near-misses differ in KIND. The alpha/k22-condensed state where d_s hits the benchmark is a
COLLAPSE (blob-with-stalk); the high-sigma hub-suppressed state where d_H passes is a genuine PHYSICAL
EXTENDED phase.** So the d_s=benchmark "improvement" is a condensation artifact (not a real extended
3-manifold), while the d_H=benchmark crossing is a real extended geometry that simply lands the wrong
dimension. All three preregistered hypotheses (H_neutral, H_hub, H_cond) confirmed.

## Observable and method (see PREREG for the full decision rule)

Profile p(t) = # spatial triangles with all 3 vertices in slice t (`st.stris` grouped by `st.time`),
t=0..T-1 -- the standard CDT spacelike-volume-per-slice, identical to remeasure.py's `prof_cv`.
Deterministic given a snapshot; measured read-only with `profile_dump.py`, CV cross-checked vs
remeasure.py. Dimensions (d_s 8-24, d_H 2-6) seed-averaged over 8 estimator seeds (independent
seedbase 200) via remeasure.py. Every state: census bad=0 (valid simplicial 3-manifold). All study
states at V=6000, T=12 (slice size s=N3/T ~ 500) -- matched to REPORT_CDT_K0 / _HUB.

Preregistered thresholds (T=12): EXTENDED = all of {max/mean<=2.5 & C1<=0.20; min/mean>=0.5 & stalk=0;
blob width>=8 & smooth; CV<=0.35}. COLLAPSE = any of {max/mean>=3.0 or C1>=0.30 or C2>=0.45; stalk>=3
& min/mean<=0.25; CV>=0.6}. (stalk = #slices <= 0.25*mean; blob width = #slices >= 0.5*max.)

## Results

| state (V6000,T12)             | f22  | CV        | max/mean | min/mean | C1    | C2    | stalk | blob w | d_s(8-24)      | d_H(2-6) [ratio]   | census | profile verdict |
|-------------------------------|------|-----------|----------|----------|-------|-------|-------|--------|----------------|--------------------|--------|-----------------|
| exact-T^3 torus (m=10, bench) | --   | ~0 (unif) | 1.00     | 1.00     | --    | --    | 0     | all    | 3.033 +-0.279  | 2.473 [1.00]       | 0      | (reference)     |
| (c) NEUTRAL k0=2 k22=0 s=0    | 0.399| 0.164     | 1.16     | 0.73     | 0.096 | 0.193 | 0     | 12/12  | 3.392 +-0.243  | 1.789 [0.72]       | 0      | **EXTENDED**    |
| (b) HUB sigma=0.10 (d_H pass) | 0.380| 0.236     | 1.43     | 0.71     | 0.119 | 0.236 | 0     | 11/12  | 2.430 +-0.300  | 2.312 [**0.935**]  | 0      | **EXTENDED**    |
| (a) COND k0=6 (d_s hits bench)| 0.044| 0.68->0.99| 3.35     | 0.11     | 0.279 | 0.486 | 3     | 3/12   | 3.135 +-0.466  | 1.597 [0.65]       | 0      | **COLLAPSE**    |

Actual N3(t) curves (spatial triangles per slice, t=0..11):

    (c) NEUTRAL k0=2      : [174,160,174,160,118,114,124,158,168,110,174,170]   spread across all 12 slices
    (b) HUB sigma=0.10    : [134,118,128,168,164,148,190,218,222,148,110,116]   one broad gentle hump, floor never emptied
    (a) COND k0=6  177 sw : [ 42,324,230,150,336, 50,518,444, 92, 52,514,250]   CV 0.683
    (a) COND k0=6  319 sw : [ 56, 78, 66,194,606, 26,212,432,134, 30,820,282]   CV 0.989 -- spikes (820,606,432) + depleted floor (26,30,56,66)

## Per-state scoring against the preregistered rule

**(c) NEUTRAL (k0=2, k22=0)** -- CV 0.164, max/mean 1.16, min/mean 0.73, C1 0.096, stalk 0, blob width
12/12, single smooth undulation. E1-E4 all satisfied => **EXTENDED**. A uniform S^2 x S^1 tube: volume
spread evenly across every slice (thermal ripple only). Corroborated by a 2nd snapshot (s1: CV 0.198,
stalk 0, blob 12/12). Dimensions: d_s +0.36 high, d_H ratio 0.72 -- the campaign-5 slice-size wall;
neither dimension on benchmark, but the geometry is a real extended 3-manifold. H_neutral CONFIRMED.

**(b) HUB sigma=0.10 (d_H PASSES: ratio 0.935 >= 0.90)** -- CV 0.236, max/mean 1.43, min/mean 0.71,
C1 0.119, C2 0.236, stalk 0, blob width 11/12, one broad gentle hump with the floor never depleted.
E1-E4 all satisfied => **EXTENDED**. The whole hub ladder is extended (single-snapshot CV: sigma=0.00
0.215, 0.02 0.253, 0.05 0.227, 0.10 0.236, 0.20 0.275; stalk 0 throughout, blob width 9-12), and
REPORT_CDT_HUB already showed sigma=0.10 stable across 1213->1643 sweeps (CV 0.30->0.28, not drifting).
So the d_H gain from hub suppression is a *connectivity reshaping at fixed extended geometry* -- it
de-saturates ball growth without condensing the volume. H_hub CONFIRMED.

**(a) COND k0=6 (d_s HITS BENCHMARK: 3.135 +-0.466 vs benchmark 3.03-3.14)** -- CV 0.683 at 177 sweeps
rising to 0.989 at 319 sweeps (K3, and still drifting => a live collapse/instability, matching the
REPORT_CDT_K0 "CV 0.59->0.76 and rising"); max/mean 3.35 (K1), C2 0.486 (K1), stalk 3 slices with
min/mean 0.106 (K2). K1 + K2 + K3 all tripped => **COLLAPSE**. f22 sits at its k0=6 equilibrium (0.044)
while the volume piles into 2-3 spike slices (820, 606, 432) and the rest deplete toward the minimal
2-sphere floor (a blob-with-stalk). census bad=0 throughout: still a valid manifold, but a condensing
one, not an extended de Sitter-like geometry. H_cond CONFIRMED.

## Cross-lever / cross-volume corroboration (that (a) is the lever, not the coupling)

Campaign 6 proved k0(up) and k22(up) are the SAME f22 lever; the collapse reproduces across the lever
and down in volume (single-snapshot profiles): alpha k0=2/k22=1.0 (V1500,T8) CV 0.533, C2 0.443,
min/mean 0.269; k0=5 (V700,T10) CV 0.562, stalk 1; k0=4 (V700,T10) CV 0.652 (K3), stalk 2, min/mean
0.161. Every low-f22 state condenses; every extended (neutral / hub) state stays uniform. Condensation
tracks f22 (the order parameter), not k0-vs-k22-vs-sigma.

## Comparison to the reference shapes

- Exact-T^3 torus (the d_H/d_s benchmark) is translation-invariant => a flat profile (CV=0) by symmetry:
  the maximally-uniform extended reference. NEUTRAL and HUB sit just off it (CV 0.16-0.24, thermal),
  firmly on the extended side.
- Known 2+1D CDT de Sitter profile (Ambjorn-Jurkiewicz-Loll): a single smooth extended hump fit to the
  Euclidean de Sitter solution -- moderate peak, broad support, at most a short minimal stalk. That is an
  EXTENDED shape (it lives inside E1-E4). NEUTRAL/HUB here are extended but *uniform* (a tube), not a
  de Sitter hump per se -- this alpha=1, S^2 x S^1 ensemble at these couplings gives an extended uniform
  phase, not phase-C de Sitter. Both are extended; neither is a collapse.
- The COND state is the opposite pole: a spiked blob-with-stalk, exactly the collapse the task names.

## What this means for the program (preregistered reading, so not post-hoc)

Landing: **H_cond = COLLAPSE and H_hub = EXTENDED => the two near-misses differ in KIND.**
- The **d_s = benchmark** crossing (alpha / k22 / high-k0, low f22) is a **condensation artifact**: at the
  point where d_s sits on the benchmark, the spatial volume has collapsed into a few slices (CV ~1, K1+K2+K3),
  so it is NOT a real extended 3-manifold. It should not be read as "nearly a physical universe" -- it is the
  d_s estimator responding to a blob, precisely the trap LESSONS 6/14 flagged (a d-gain riding rising CV).
- The **d_H = benchmark** crossing (hub suppression) is a **genuine extended geometry** (CV 0.24, no stalk,
  volume across 11/12 slices, stable) that simply lands d_H rather than d_s. It is the physically meaningful
  near-miss.
So the d_H-d_s wall is even more robust than the raw gate table suggests: one side of it (d_s via alpha/k22)
is not a candidate physical phase at all, it is collapse. The frontier worth pushing is the extended
hub/d_H side (lift d_s back up at fixed extended geometry) -- not the alpha/d_s side, which only "improves"
d_s by destroying the 3-manifold's extension.

## Honest caveats

- V=6000, T=12, s~500 (sandbox, chunked). Profiles are single equilibrium snapshots (p(t) deterministic per
  snapshot); NEUTRAL corroborated by a 2nd snapshot, the COND CV trend by the 177->319-sweep trajectory,
  and CVs cross-checked against the seed-averaged CV in REPORT_CDT_K0/_HUB. My single-snapshot hub CVs run
  a little below the reports' seed-averaged CVs (e.g. sigma=0.10: 0.236 vs 0.276; sigma=0.20: 0.275 vs 0.400
  -- the latter would be marginal on E4) but sigma=0.10, the d_H-passing point, is extended either way.
- COND is a *live* collapse (CV still rising at 319 sweeps); the d_s=benchmark value is a crossing during
  condensation, not a stable equilibrium -- which is itself the point (there is no stable d_s=benchmark
  extended state). d_s(8-24) at the measured snapshot = 3.135 +-0.466, squarely on benchmark.
- "Physical extended phase" here means a real, non-collapsed, volume-spread 3-geometry (the extended side of
  the task's dichotomy), not a claim that the uniform tube is specifically phase-C de Sitter.
- 2+1D toy, N0 ~ 900-1500. Finite-size, in-ensemble; consistent with the campaign-5/6/7 V-independence.

## Reproduce

    PYTHONPATH=.:tooling python3 cdt_causal_run.py --chunk --k0 6.0 --T 12 --V 6000 --seed 0 \
      --tune 400 --sweeps 100000 --budget-s 30 --scratch <dir>/scratch --log <dir>/rec.jsonl   # x3 chunks
    PYTHONPATH=.:tooling python3 profile_dump.py --pkl <dir>/scratch/causal_k0+6.00_T12_V6000_s0.pkl --tag COND
    PYTHONPATH=.:tooling python3 remeasure.py --pkl <pkl> --seeds 8 --tmax 50 --dswin 8-24 --seedbase 200
    PYTHONPATH=.:tooling python3 remeasure.py --torus 10 --seeds 8 --tmax 50 --dswin 8-24 --seedbase 200
    # hub sigma=0.10 + neutral k0=2 profiles: profile_dump.py on the cached V6000/T12 pickles.
