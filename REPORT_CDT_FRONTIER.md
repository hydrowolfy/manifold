# Frontier: is the causal-CDT d_H-d_s tradeoff a genuine wall, or can it be beaten?

Fifth campaign. Preregistered in `PREREG_CDT_JOINT.md` (committed BEFORE the new experiments).
Question inherited from campaign 4: on the balanced-aspect ladder, causal CDT reaches a real
3-manifold in d_H(2-6) but not simultaneously in d_s. Can any point in (foliation aspect T,
couplings, CDT asymmetry alpha) land BOTH dimensions on the exact-T^3 benchmark at large V?

## Verdict

**The d_H-d_s tradeoff is a genuine, volume-stable structural obstruction of this 2+1D
construction, governed by a single geometric parameter -- the spatial slice size s = N3/T.**
Both dimensions are (to measurement precision) V-INDEPENDENT monotonic functions of s:

    d_s(8-24) = 0.17 + 0.50 ln s   -> reaches benchmark 3.12 at s ~= 385
    d_H(2-6)  = -1.72 + 0.57 ln s  -> reaches benchmark 2.58 at s ~= 1940

The two benchmark conditions sit ~5x apart in slice size and do NOT converge with volume.
No aspect at any accessible V lands both. The alpha (k22) lever DOES move both dimensions
toward the benchmark, but only by driving spatial-volume condensation (a blob); its apparent
joint crossing is a transient during the condensation, not a stable equilibrium. The single
consolation: on the longest trustworthy diffusion window (16-48), the fattest V=24000 aspect
sits within ~0.17 of benchmark on BOTH dimensions, so the primary d_s(8-24) excess is partly a
short-window lattice artifact -- a weak long-window near-agreement, not a clean joint 3-manifold.

Prereg decision-rule landing: **GENUINE OBSTRUCTION (characterized), with a weak long-window
partial-positive.** JOINT WIN not achieved; "closes at larger V" (H3) refuted; alpha (H1)
refuted; long-window (H2) partially supported.

## Method corrections vs campaign 4 (these change the numbers)

1. SEED-AVERAGED estimators. `lazy_rw_sdim`/`ball_growth_dim` are stochastic (Hutchinson probe /
   random ball sources). Campaign 4 scored single-seed. Averaging K>=8 estimator seeds moves the
   benchmark: d_s(8-24) for exact T^3 is 3.07-3.15 +/- 0.07-0.17, NOT the 3.42 (unlucky single
   draw) used before. This makes the fat-ladder d_s excess larger and clearer.
2. Size-matched benchmark by N0; d_H on the torus is deterministic (vertex-transitive, sd~0).
3. New tool `remeasure.py` (re-measures any checkpoint pickle or exact torus with K seeds,
   error bars, profile CV, mean degree). New runner flag `--grind` (fast thermalization: skip
   the d_s/d_H estimators, keep census+checkpoint) for the V=24000 climbs. (Patch: grind.patch.)

## The slice-size collapse (the core result)

All states k0=2, alpha=0 (k22=0), equilibrated; d_s/d_H are mean +/- sd over 8 estimator seeds
(2 config seeds where available). s = N3/T = spatial tetrahedra per time slice.

|   s  |  V    | T  | N0   | d_s(8-24)    | d_s(16-48) | d_H(2-6)    | note        |
|------|-------|----|------|--------------|-----------|-------------|-------------|
|  249 | 6000  | 24 |  965 | 2.84 +-0.25  | 1.64      | 1.44 +-0.05 |             |
|  375 | 6000  | 16 |  951 | 3.14 +-0.01  | 2.00      | 1.64 +-0.01 | d_s on line |
|  500 | 6000  | 12 |  933 | 3.44 +-0.02  | 2.58      | 1.77 +-0.05 |             |
|  667 | 12000 | 18 | 1887 | 3.18 +-0.26  | 2.21      | 1.98 +-0.06 |             |
|  752 | 6000  |  8 |  957 | 3.42 +-0.36  | 2.73      | 2.04 +-0.11 | overlap chk |
|  802 | 12000 | 15 | 1879 | 3.50 +-0.05  | 2.68      | 2.11 +-0.01 |             |
|  858 | 24000 | 28 | 3992 | 3.60 +-0.21  | 2.88      | 2.10 +-0.11 | thin V24k   |
| 1000 | 24000 | 24 | 3964 | 3.57 +-0.15  | 2.82      | 2.15 +-0.08 | thin V24k   |
| 1004 | 6000  |  6 |  972 | 3.59 +-0.51  | 2.62      | 1.76 +-0.14 | TIME-SATURATED (T<8) |
| 1264 | 24000 | 19 | 3832 | 3.71 +-0.02  | 3.22      | 2.40 +-0.01 | fat V24k    |
Benchmark (exact T^3): d_s(8-24) 3.07-3.15, d_s(16-48) 3.0-3.05, d_H(2-6) 2.47-2.58.

The collapse is the load-bearing evidence, demonstrated across a 4x range of N0:
- d_H at fixed s is V-INDEPENDENT: V6000 T8 (s752, N0 957) d_H=2.04 sits on the same curve as
  V12000 T18/T15 (s667/802, N0 1887) d_H=1.98/2.11; V12000 (s802, N0 1879) d_H=2.11 == V24000
  T28 (s858, N0 3992) d_H=2.10 despite 2x the vertices.
- d_s at fixed s is V-INDEPENDENT: V6000 T6 (s1004, N0 972) d_s=3.59 == V24000 T24 (s1000,
  N0 3964) d_s=3.57 despite 4x the vertices.
- The lone violator (V6000 T6, d_H=1.76 vs the s~1000 trend of 2.1) is time-saturated: with
  only 6 slices, ball-growth windows 3-8/4-10 collapse (slopes 0.58/0.03) -- d_H(2-6) windows
  need T >~ 8. Excluded from the fit.

Consequences (linear-in-ln-s fits on adequate-T points):
- d_s(8-24)=benchmark at s ~= 385; d_H(2-6)=benchmark at s ~= 1940. Ratio ~5x.
- At s=385 (d_s on the line): d_H=1.66, ratio 0.64.
- At the fattest measured aspect s=1264 (V24000 T19, d_H ratio 0.93): d_s(8-24)=+0.59 excess.
Because both curves collapse on s (no residual V dependence), growing V cannot close the gap:
larger V only buys access to larger s (higher on BOTH curves), never a shift that makes the two
benchmark slice-sizes coincide. **This refutes H3 (tradeoff narrows with V).** The campaign-4
apparent narrowing (deficit 0.94 @ V6k -> 0.63 @ V12k) was a slice-size confound: the V12000
"d_s on line" point (T18) has s=667, not the s~=385 where d_s truly equals benchmark; read at
matched slice size the d_H deficit is volume-stable.

## The alpha (k22) lever (H1): moves both dimensions, but by condensation

k22 is the coefficient on N22 in S = k3 N3 - k0 N0 + k22 N22 -- the discretized CDT asymmetry
(alpha). Fixed at 0 the entire program. Warm-starting equilibrated k22=0 states and scanning
k22 (checkpoint tag separated per-k22):

- k22 > 0 (penalize (2,2) tets) lowers f22, raises N0, RAISES d_H(2-6) and LOWERS d_s(8-24) --
  both toward benchmark. k22 < 0 does the opposite (both worse). The lever is real and points
  the right way. At V=12000 T=15, a transient snapshot at k22=+1.5 hit d_H(2-6)=2.49 (ratio
  0.965) with d_s(8-24)=3.18 (benchmark 3.20) -- an apparent JOINT PASS.
- But it is NOT an equilibrium. Following the same chain, the spatial volume CONDENSES: profile
  CV rises monotonically 0.26 -> 0.30 -> 0.50, one slice blows up (max slice 444 -> 640 -> 902
  while others deplete to the minimal sphere), f22 keeps falling (0.21 -> 0.086). The observables
  slide THROUGH the joint point: d_s(8-24) 3.18 -> 3.00 (now below benchmark), d_s(16-48) 2.95 ->
  2.35 (well below). Both config seeds reproduce the condensation.
- Milder k22=+1.0 is less condensed (CV ~0.25) and reaches d_H(2-6) ratio 0.91 (passes) but
  leaves d_s(8-24) at +0.25 (fails). No STABLE k22 at k0=2 passes both G2 and G3.

So alpha reparameterizes the tradeoff and even improves both dimensions, but the only
joint-passing states are transients on the way to a condensed (blob) phase, which is a different
geometry from the uniform benchmark. **H1 refuted in its strong (stable-config) form.** Whether a
different k0 (a different CDT phase) suppresses the condensation and lets alpha work cleanly is
the top open lever -- untested here (k0 fixed at 2 throughout).

## The long-window nuance (H2): the short-window excess is partly a lattice artifact

Scored on 8-24, the fat-ladder d_s excess GROWS with V (+0.30 @ V6k, +0.43 @ V12k, +0.56 @
V24k). But on the longest trustworthy window at the largest size (16-48 at V=24000, N0~3830),
the fat aspect gives d_s=3.22 +/- 0.31 vs benchmark 3.05 +/- 0.11 -- excess only +0.17 (<1
sigma). At that same fattest aspect d_H(2-6) ratio is 0.93. So on (16-48, 2-6) the fattest
V=24000 point is within ~0.17-0.18 of benchmark on BOTH dimensions. This is the strongest
positive available and is consistent with the standing methodology lesson that the short-window
d_s offset dissolves at longer diffusion times. It is a WEAK result: 16-48 is noisy and flagged
finite-size-sensitive, d_H is still ~2 sigma low, and d_s(8-24) at that aspect is still +0.56.
It supports "the residual is a short-scale lattice artifact," not "a clean joint 3-manifold."

## Joint gate (preregistered G1-G4) -- final scoring

| config                         | G1 census | G2 d_H>=0.90 | G3 |d_s(8-24)-b|<=0.20 | joint? |
|--------------------------------|-----------|--------------|------------------------|--------|
| V24000 fat T19 (s1264)         | PASS      | PASS (0.93)  | FAIL (+0.59)           | NO     |
| V24000 thin T24 (s1000)        | PASS      | FAIL (0.83)  | FAIL (+0.42)           | NO     |
| V6000 thin T16 (s375, d_s ok)  | PASS      | FAIL (0.64)  | PASS (~0)              | NO     |
| V12000 k22=+1.5 (transient)    | PASS      | PASS (0.97)  | PASS (-0.02) but UNSTABLE (condensing) | NO* |
| V12000 k22=+1.0 (stable-ish)   | PASS      | PASS (0.91)  | FAIL (+0.25)           | NO     |
*The only G1-G3-passing config is a non-equilibrium transient; it fails the JOINT-WIN clause
"survives independent re-measurement" (it drifts as it condenses). No stable config passes.

## Honest caveats

- 2+1D toy at N0 <~ 4000; "V-independent collapse" is demonstrated over 950 <= N0 <= 4000 (4x),
  a finite-size trend, not a continuum proof. The slice-size fits are log-linear over
  250 <= s <= 1264; the s~1940 d_H crossing is a modest extrapolation.
- Thin V=24000 (T24,T28) equilibrated to f22~0.345 (equilibrium ~0.38); slightly under-thermal.
  Direction of the residual bias makes d_s a lower bound, i.e. it strengthens "d_s stays high."
- 16-48 window is noisy (sd 0.2-0.4) and finite-size-sensitive below N0~2000; the H2
  near-agreement is suggestive, not decisive.
- alpha condensation was mapped at k0=2 only. A k0 scan (CDT phase structure) is the untested
  lever that could, in principle, change the verdict.
- Census bad=0 in every snapshot of every chain in this campaign (fat/thin ladder, alpha scan,
  V=24000 climbs). The construction never leaves the manifold; the obstruction is dimensional,
  not topological.

## What would move this next

1. k0 scan x alpha: does a different CDT phase suppress the condensation so alpha lands a STABLE
   joint pass? (Top lever; ~1 day of chains.)
2. Push a genuinely thin, large-T V=24000 (T~60, s~385) to put a measured d_H at the d_s=benchmark
   slice size at the top volume -- directly nails the volume-stability of the 0.64 d_H ratio.
3. A uniform-profile constraint (or measure the de Sitter volume profile properly) to decide
   whether the alpha-condensed states are the physical CDT extended phase or a collapse.
