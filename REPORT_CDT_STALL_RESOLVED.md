# The d_H(3-8) stall: thermalization, wrap, or wall? Resolved.

Date: 2026-07-08. Third campaign in the causal CDT thread. Question on the table: the wider
ball window d_H(3-8) stalled at ~1.0 between V=3000 and V=6000 while the exact-T^3 benchmark
grew 1.60 -> 2.15. Under-thermalization or genuine extent saturation? Raw data appended to
`cdt_causal_results.jsonl`; every chunk checkpointed. Nothing committed or pushed to GitHub.

## Headline answer

The wider-window d_H does NOT recover with thermalization, because it was never a
thermalization artifact: extending the V=6000 chains to 4500 sweeps (3.2x) produced a
d_H(3-8) series that is flat to within noise across 18 measurement points spanning sweeps
148 to 4500, on both k0 values and both seeds (range 0.94-1.10, no trend). The stall is an
equilibrium property of the V=6000, T=16 ensemble.

What DOES recover it: volume and foliation aspect.

1. T-variants at fixed V=6000, k0=2 (the discriminator): fatter slices win, monotonically.
   T=12: d_H(2-6)=1.87 +/- 0.10, d_H(3-8)=1.20 +/- 0.10
   T=16: d_H(2-6)=1.66 +/- 0.06, d_H(3-8)=1.03 +/- 0.04
   T=24: d_H(2-6)=1.45 +/- 0.09, d_H(3-8)=0.99 +/- 0.05
   Shortening T (fewer, larger spatial slices) raises both windows; lengthening T lowers
   them. The binding constraint on ball growth is SPATIAL SLICE EXTENT, not the time wrap
   (T=24 has the longest time circle and reads lowest). The 3000 -> 6000 stall happened
   because the T ladder (14 -> 16) grew slices only ~30% while V doubled.

2. V=12000 (fourth slope point, k0=2, T=18, 800 sweeps, f22 converged to 0.38, bad=0):
   d_H(2-6) = 2.01 +/- 0.08 vs benchmark 2.59 -> ratio 0.78, the highest of the campaign.
   d_H(3-8) = 1.27 +/- 0.04: wide-window growth RESUMED (+0.24 over V=6000).
   d_s(8-24) = 3.23 vs torus m=12 at 3.23: on the benchmark line at the trustworthy window.

## The ratio ladder (k0=2, primary window d_H(2-6), scored against matched exact T^3)

| V     | T  | N0~  | d_H(2-6)      | bench | ratio |
|-------|----|------|---------------|-------|-------|
| 700   | 10 | 130  | 1.00 +/- 0.07 | 1.62  | 0.62  |
| 1500  | 12 | 255  | 1.06 +/- 0.10 | 1.82  | 0.58  |
| 3000  | 14 | 484  | 1.38 +/- 0.04 | 1.97  | 0.70  |
| 6000  | 16 | 938  | 1.66 +/- 0.06 | 2.43  | 0.69  |
| 6000  | 12 | 925  | 1.87 +/- 0.10 | 2.42  | 0.77  |
| 12000 | 18 | 1895 | 2.01 +/- 0.08 | 2.59  | 0.78  |

Overall d_H(2-6) slope per ln N0 across the full ladder (130 -> 1895): causal 0.377 vs
benchmark 0.362. The causal ensemble is now growing d_H at least as fast as the exact flat
manifold at matched size; the deficit is a closing offset, not a diverging gap. On the wider
3-8 window the ratio fell from 0.70 (V=1500) to 0.49 (V=6000, T=16) before stabilizing and
upticking at V=12000 (0.51), with the T=12 variant showing +0.09 of that fall was aspect
choice alone. Wall verdict: no re-assertion anywhere; the 3-8 dip is an aspect-ratio
finite-size effect with an identified lever, not an asymptotic obstruction.

## k22 probe (alpha-like lever, V=3000, k0=2, 2000 sweeps each, bad=0)

k22=+0.3 suppresses (2,2) tets (f22 0.39 -> 0.32), which fattens slices at fixed volume:
d_H(2-6) = 1.45 +/- 0.06 (ratio 0.72, above the 0.70 baseline). k22=-0.3 does the opposite
(f22 0.43, d_H 1.30 +/- 0.02, ratio 0.66). The lever works, direction consistent with the
slice-extent mechanism, magnitude modest. Note the k22 shifts N0 at fixed V (537 vs 456),
so part of the effect is size relabeling; not a clean win yet, worth a proper sweep only if
aspect-balanced ladders leave a residual gap.

## Gate evaluation

1. Census clean: PASS. Every snapshot of every chain in the campaign (including T-variants,
   k22 chains, V=12000) reports bad=0. The moves have never once broken the manifold.
2. Causal d_H(V) tracks benchmark slope: PASS on d_H(2-6), now at parity or better (0.377
   vs 0.362 per ln N0), ratio rising to 0.78. On d_H(3-8): growth resumed at V=12000 and the
   fixed-V T-study explains the dip; call it CONDITIONAL PASS pending one balanced-aspect
   ladder.
3. d_s inside benchmark band (8-24 window): PASS at V=6000 (3.43/3.51 vs 3.41) and V=12000
   (3.23 vs 3.23).
4. Euclidean controls fail jointly at every size (d_s pinned 3.87-3.98, never descending
   with the benchmark): unchanged from last campaign.

## Honest caveats

V=12000 is one seed, one T, 300 post-tune sweeps, 4 snapshots; its error bar is optimistic.
T-variants are single seeds. Snapshot spacing at V >= 6000 is ~90-250 sweeps, so consecutive
snapshots are autocorrelated and quoted sd understates true error, though the thermalization
NULL result (flatness over a 30x sweep range) is robust to exactly this concern. The
benchmark d_H(3-8) line below N0~350 is undefined (torus too small), so small-V 3-8 ratios
are not meaningful. Aspect ratio is confounded with V in the main ladder; that is the
identified systematic, not a hidden one.

## Recommended next run (needs green light)

One balanced-aspect ladder to retire the last conditional: fix T = round(1.9 * V^(1/3))
(which makes slice diameter comparable to time wrap, matching the T=12@V=6000 optimum), run
V = 6000/12000/24000 at k0=2, 2 seeds, scoring both d_H windows against matched tori
(m = 10/12/16 as needed, plus m=14). Success = d_H(3-8) ratio climbing back toward its
small-V value while d_H(2-6) ratio continues past 0.8. V=24000 costs roughly 4x the V=12000
point per sweep; budget ~2x this campaign total. Secondary: 2-3 seeds at V=12000 to firm its
error bar before trusting the 0.78.
