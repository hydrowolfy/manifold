# Preregistration: can causal CDT jointly reach a 3-manifold in (d_H AND d_s)?

Date: 2026-07-08 (fifth campaign, "frontier"). Registered BEFORE running the two new levers
(the CDT asymmetry k22/alpha, and a fine aspect sweep at large V). Prior campaigns established
a real d_H-d_s finite-size tradeoff on the balanced-aspect ladder at alpha=1 (k22=0). This
document fixes the scoring, gate, hypotheses, and decision rules so the headline cannot be
tuned to a target after the fact.

## 0. What changed from campaign 4 (and why it matters)

Re-analysis of the campaign-4 states with SEED-AVERAGED estimators (8 estimator seeds, not the
single default seed the prior reports used) corrects the benchmark and sharpens the gap:

- Exact-T^3 benchmark d_s(8-24) is 3.07-3.15 +/- ~0.07-0.17 (size-matched), NOT ~3.42. The
  report's 3.42 (m=16, single seed) was a high fluctuation. The properly averaged line is lower.
- Consequently the fat-ladder d_s(8-24) EXCESS is larger and clearly GROWS with V:
  +0.30 (V6k) -> +0.43 (V12k) -> +0.56 (V24k). It does not close on the balanced ladder.
- d_s(16-48) at V=24000 is 3.22 +/- 0.31 vs benchmark 3.05 +/- 0.11: excess only +0.17 (<1 sigma).
  The excess is a SHORT/MEDIUM-window phenomenon that largely dissolves by 16-48.
- Mean vertex degree is ~14.5 across every causal config AND the Kuhn T^3 (14). The d_s excess
  is therefore not mean coordination; it is local cycle/typed-simplex structure -> the f22 (alpha)
  lever is the physically-motivated knob.

## 1. Estimators, windows, benchmark (frozen)

- Estimators: repo `lazy_rw_sdim` (d_s, lazy-RW return prob, tmax=50 unless stated) and
  `ball_growth_dim` (d_H), used VERBATIM. Graph = vertex 1-skeleton of the triangulation.
- Error bars: every measurement is the mean over K>=8 ESTIMATOR seeds; sigma is the seed sd.
  Where two Monte-Carlo (config) seeds exist, the reported value averages both and the sd
  combines them. Estimator-seed sd is the primary bar (measurement noise); config spread noted.
- Benchmark: exact periodic Kuhn triangulation of the flat 3-torus T^3, size-matched by N0:
  V=6000 <-> m=10 (N0=1000), V=12000 <-> m=13 (N0=2197), V=24000 <-> m=16 (N0=4096).
  Benchmark numbers (8 seeds), FROZEN here:
    m=10: d_s 8-24=3.135+-0.172, 16-48=3.014+-0.405 | d_H 2-6=2.473 (deterministic)
    m=13: d_s 8-24=3.071+-0.160, 16-48=3.006+-0.264 | d_H 2-6=2.579
    m=16: d_s 8-24=3.149+-0.068, 16-48=3.052+-0.108 | d_H 2-6=2.579
- Primary d_s window: 8-24 (handoff-trusted at N0>=~950). Secondary: 16-48 (trust only N0>=~2000).
- Primary d_H window: 2-6. Secondary: 3-8.

## 2. The joint gate (PASS criteria, frozen)

A single configuration (fixed T, k0, k22, at volume V) "jointly converges to a 3-manifold" iff
ALL of:
  (G1) census bad = 0 in the measured snapshot(s).
  (G2) d_H(2-6) ratio to matched benchmark >= 0.90  (equiv. deficit <= ~0.26).
  (G3) |d_s(8-24) - matched benchmark| <= 0.20  (~2x the combined V=24000 sigma).
  (G4) sign check: d_s(16-48) also within its (wider) benchmark band, not overshooting the
       opposite way.
No campaign-4 config passes: fat V24k has G2 (0.93) but fails G3 (+0.56); thin V12k T18 has
G3 (+0.11) but fails G2 (0.77). The frontier question is whether ANY (T,k0,k22,V) passes all.

## 3. Hypotheses (each with a pre-set confirm/refute)

H1 - ALPHA DECOUPLES. There exists k22 != 0 (alpha != 1) at a d_H-good (fat) aspect that lowers
   d_s(8-24) onto the benchmark while d_H(2-6) stays at/above its k22=0 value.
   CONFIRM: a (T,k22,V) meeting the full joint gate (Sec 2). REFUTE: across the scanned k22
   range, every k22 that brings d_s(8-24) to benchmark also drops d_H(2-6) ratio below 0.90
   (tradeoff merely reparameterized, not broken).

H2 - LONG-WINDOW DISSOLVES. The d_s excess is a short-window lattice artifact; on the longest
   trustworthy window at large V (16-48 at V=24000) causal d_s already equals benchmark, and
   d_H is near benchmark there -> "joint on the long window".
   CONFIRM: at V=24000, d_s(16-48) within benchmark band AND d_H(2-6) ratio>=0.90 (both already
   near-true: +0.17 and 0.93) AND this holds up under a longer/independent re-measure with more
   config seeds. REFUTE: 16-48 agreement is an artifact of that window's large finite-size noise
   (fails to hold with more seeds / at matched benchmark), or d_s keeps drooping below benchmark.

H3 - TRADEOFF NARROWS WITH V. The aspect-tradeoff curve (d_s(8-24), d_H(2-6)) parameterized by
   T moves toward the joint target as V grows: at the aspect where d_s(8-24)=benchmark, the
   d_H(2-6) deficit shrinks with V (seen so far: ~0.94 at V6k -> ~0.63 at V12k).
   CONFIRM: a thin V=24000 point continues the shrink (deficit < ~0.5 at d_s=benchmark) and a
   2-3 point extrapolation in 1/V^(1/3) projects the deficit to ~0 at finite V. REFUTE: the
   deficit stalls or grows at V=24000 (tradeoff is volume-stable / a genuine obstruction).

## 4. Experiments (pre-specified)

E1 (alpha scan, H1): warm-start equilibrated k22=0 states; at fixed V and fixed d_H-good aspect
   (V=6000 T=12 first; then V=12000 T=15), scan k22 in {-1.0,-0.5,0,+0.5,+1.0,+2.0}; re-equilibrate
   (monitor f22 plateau AND d_s stability, >=200 sweeps past f22 settling); measure with 8
   estimator seeds x 2 config seeds. Also scan a thin aspect to trace the whole k22 x T sheet if
   a promising k22 appears. Checkpoint tag MUST include k22 (bugfix: campaign-4 tag omitted it).

E2 (aspect sweep, H3): at V=6000 and V=12000, add intermediate T so the (d_s,d_H)-vs-T curve is
   mapped by >=4 aspects each; locate the d_s(8-24)=benchmark aspect and read the d_H deficit.

E3 (thin V=24000, H3 + flagged): grow thin V=24000 (T in {22,24,26} as needed to bracket the
   d_s=benchmark aspect), k0=2, 2 seeds; the top-of-ladder point for the narrowing extrapolation.

## 5. Decision rules (which verdict we land)

- JOINT WIN (emergent 3-manifold): some config passes the Sec-2 gate AND survives independent
  re-measurement. Report it as the headline with full error bars.
- LONG-WINDOW WIN (weaker): H2 confirmed and robust even if H1 fails -> "d_H and d_s agree with
  the 3-torus on all trustworthy windows at V=24000; the residual is a short-window lattice
  artifact." Stated with the 16-48 finite-size caveat.
- CLOSES AT LARGER V / WITH ALPHA: H3 (or H1-trend) confirmed as a shrinking-but-nonzero deficit
  with a defensible 1/V^(1/3) extrapolation to zero. Report the extrapolation + its uncertainty.
- GENUINE OBSTRUCTION (clean negative): H1, H2, H3 all refuted -> the d_H-d_s tradeoff is a real
  finite-V obstruction of this 2+1D construction; characterize it (the tradeoff curve, its
  volume trend, the k22 sheet) as the deliverable.

Scoring, benchmark, windows, and gate above are frozen as of this commit.
