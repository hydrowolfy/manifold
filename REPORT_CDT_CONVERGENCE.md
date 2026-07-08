# Balanced-aspect ladder: does causal CDT jointly converge to a 3-manifold?

Date: 2026-07-08. Fourth campaign in the causal CDT thread, and the intended closer. The
prior session left one conditional gate item: run a balanced-aspect ladder to V=24000 and
check whether the primary Hausdorff dimension keeps converging while the spectral dimension
stays on the exact-T^3 benchmark line. This report is the verdict. Raw data appended to
`cdt_causal_results.jsonl` (204 records); every chunk checkpointed; nothing about the
physics was tuned to a target.

## What was run

- Benchmark extended: exact flat T^3 (Kuhn) at m=14 (N0=2744) and m=16 (N0=4096), same
  estimators/windows as everything else. The line now runs m=5..16.
- Balanced-aspect ("fat") ladder, constant aspect T = round(12 * (V/6000)^(1/3)):
  T=12 @ V=6000, T=15 @ V=12000, T=19 @ V=24000; k0=2; 2 seeds each. Note on the constant:
  the handoff wrote `T = round(1.9 * V^(1/3))`, which evaluates to ~35 at V=6000 and
  contradicts its own "T=12 @ V=6000 optimum" anchor. The self-consistent constant that
  holds that aspect fixed is 12/6000^(1/3) = 0.66, i.e. T ∝ V^(1/3) normalised to (12,6000).
  That is the schedule used.
- Each chain grown to volume, k3 auto-tuned to hold N3=V and f22 to its ~0.38 equilibrium,
  then >=3 post-tune snapshots. V=24000 chains carried to ~650 sweeps (f22 0.36-0.37).
- Gold-standard long-window estimator (`--measure-long`, tmax=100) on the equilibrated
  V=12000 and V=24000 states for the full d_s(window) flow.
- "Thin" chains from the prior campaign (T=16 @ V=6000, T=18 @ V=12000) re-scored against
  the extended benchmark for the aspect comparison.

## Headline verdict

**Causal CDT does NOT cleanly, jointly converge to a single real 3-manifold across the
balanced-aspect ladder — but not because anything crumples back.** The result splits:

1. The primary Hausdorff dimension d_H(2-6) converges convincingly. On the fat ladder its
   benchmark ratio climbs 0.75 -> 0.82 -> 0.93, reaching near-parity with the exact
   3-manifold at V=24000. Nothing re-asserts in d_H(2-6); the gap is still closing at the
   top of the ladder (causal slope 0.41 vs benchmark ~0.10 per ln N0 over the high-N0 tail,
   where the benchmark has plateaued and causal is catching up).

2. The spectral dimension d_s(8-24) does NOT join it. On the same fat chains d_s(8-24) sits
   +0.2 to +0.7 above the benchmark and does not close with volume (+0.41 at V=24000). The
   thin chains put d_s essentially on the line (-0.14 at V=6000, +0.28 at V=12000) but pay
   for it in d_H (ratio 0.65/0.78 vs the fat 0.75/0.82). No single aspect ratio delivers
   both d_H and d_s on the benchmark at these volumes.

3. d_H(3-8) tracks the benchmark slope but at a stuck ~0.5 ratio on both ladders; the
   wider-ball structure grows in absolute terms (1.17 -> 1.21 -> 1.40 on the fat ladder) yet
   never climbs back toward the 0.6-0.7 the gate hoped for.

So the Euclidean crumpling that the causal construction genuinely broke for d_H re-expresses,
at V=24000, as a residual **aspect-locked d_s excess plus a wider-window d_H lag** — a real
d_H–d_s finite-size tradeoff, not a collapse. It is weaker than Euclidean failure (Euclid
d_s is pinned 3.87-3.98 and never flows; the causal d_s does flow with scale) but it is not
the clean joint 3-manifold the fat ladder was meant to demonstrate.

## The ladder (k0=2, equilibrated snapshot means +/- snapshot sd, scored vs matched exact T^3)

FAT ladder (T ∝ V^(1/3), the specified balanced-aspect schedule):

| V     | T  | N0~  | d_H(2-6)      | ratio | d_H(3-8)      | ratio | d_s(8-24)     | vs bench |
|-------|----|------|---------------|-------|---------------|-------|---------------|----------|
| 6000  | 12 |  959 | 1.83 +/- 0.07 | 0.75  | 1.17 +/- 0.09 | 0.55  | 3.64 +/- 0.28 | +0.22    |
| 12000 | 15 | 1894 | 2.11 +/- 0.08 | 0.82  | 1.21 +/- 0.06 | 0.49  | 3.86 +/- 0.15 | +0.68    |
| 24000 | 19 | 3857 | 2.40 +/- 0.11 | 0.93  | 1.40 +/- 0.05 | 0.52  | 3.76 +/- 0.13 | +0.41    |

THIN ladder (prior campaign, re-scored):

| V     | T  | N0~  | d_H(2-6)      | ratio | d_H(3-8)      | ratio | d_s(8-24)     | vs bench |
|-------|----|------|---------------|-------|---------------|-------|---------------|----------|
| 6000  | 16 |  956 | 1.60 +/- 0.07 | 0.65  | 1.04 +/- 0.03 | 0.49  | 3.28 +/- 0.26 | -0.14    |
| 12000 | 18 | 1895 | 2.01 +/- 0.07 | 0.78  | 1.27 +/- 0.04 | 0.51  | 3.46 +/- 0.17 | +0.28    |

Benchmark (exact flat T^3), for reference: d_H(2-6) plateaus at 2.47/2.58/2.58/2.58 for
N0 = 1000/1728/2744/4096; d_s(8-24) is noisy across size (3.41/3.24/2.95/3.42 for the same
m), which widens its band and is the main reason the mid-ladder "vs bench" wobbles.

The same-volume aspect contrast is the cleanest single fact here: at V=12000, matched N0~1894,
fat (T=15) gives d_H(2-6)=2.11 with d_s(8-24)=3.86, thin (T=18) gives d_H(2-6)=2.01 with
d_s(8-24)=3.46. Fatter slices buy ~+0.1 of d_H and cost ~+0.4 of d_s. The lever is real and
the two objectives pull opposite ways.

## Spectral-dimension flow (measure-long, tmax=100)

| state                | ds 4-12 | 8-24 | 16-48 | 30-90 |
|----------------------|---------|------|-------|-------|
| causal V=12000 T=15  | 4.05    | 3.92 | 3.65  | 3.25  |
| causal V=24000 T=19 s0 | 3.98  | 3.74 | 3.27  | 2.46  |
| causal V=24000 T=19 s1 | 3.91  | 3.64 | 3.12  | 2.34  |
| exact T^3 m=16       | 3.53    | 3.42 | 3.49  | 3.61  |

The exact manifold holds d_s ~ 3.4-3.6 flat across all windows. The causal chain instead
falls steeply, 3.9 -> 3.3 -> ~2.4, crossing 3 only because the 30-90 window at N0~3800 is
system-size-limited (the brief flags 16-48 and 30-90 as size-contaminated below N0~2000; at
N0~3800 the 30-90 point is still not trustworthy). Read on the trustworthy 8-24 window, the
causal d_s is ~0.3-0.4 too high and not descending toward the line with volume. This short-
scale excess with a finite-size long-scale droop is the signature of a lattice that is
locally over-connected (fat slices) rather than a clean d~3 continuum.

## Joint gate

1. Census clean (bad=0): PASS. Every snapshot of every chain across all four campaigns,
   including the new V=24000 pair (~15 sweeps to ~650, both seeds), reports bad=0.
2. d_H(2-6) tracks/reaches the benchmark: PASS, and strengthened — ratio 0.93 at V=24000.
3. d_s(8-24) inside the benchmark band on the d_H-optimal ladder: FAIL. It stays ~0.3-0.7
   high on the fat ladder and does not close through V=24000. It only sits on the line on
   the thin ladder, where criterion 2 is weaker.
4. d_H(3-8) ratio climbing back toward 0.6-0.7: FAIL. Flat at ~0.5 on both ladders.
5. Euclidean controls fail jointly: PASS. d_s pinned 3.87-3.98 at every logged size, never
   flowing with scale.

Two of the joint-gate arms (3 and 4) do not pass on the balanced-aspect ladder. The gate as
a conjunction is therefore not met: causal CDT reaches a real 3-manifold in its primary
Hausdorff dimension but not simultaneously in its spectral dimension and wider-ball growth.

## Honest caveats

- V=24000 is 2 seeds x 3 post-tune snapshots each; snapshots are ~50 sweeps apart and
  autocorrelated, so the quoted sd understates the true error. The key claim (a +0.4
  d_s(8-24) excess) is several snapshot-sd's in size and robust to this, as is the d_H(2-6)
  climb to ~0.93; the d_H(3-8)=0.52 ratio is the least protected number but is corroborated
  by the flat 0.49-0.55 across the whole ladder and both seeds.
- The benchmark d_s(8-24) line is itself noisy (m=14 dips to 2.95). Absolute d_s comparisons
  inherit that noise; the aspect *contrast* at fixed N0 (fat 3.86 vs thin 3.46 at V=12000)
  is immune to it and is the load-bearing evidence.
- The thin aspect was not carried to V=24000. The d_H–d_s tradeoff is established at two
  volumes (V=6000 and V=12000, matched N0), and the fat V=24000 point confirms the d_s
  excess persists at the top; a thin V=24000 (T~22-23) would close the demonstration by
  showing d_s stays on the line there too. That is the single clean follow-up.
- This is a 2+1D toy at N0 ~ 4000. "Convergence" here is a finite-size trend statement, not
  a continuum proof.

## Recommended next step

One thin-aspect point at V=24000 (T ~ 22-23, k0=2, 2 seeds) to confirm d_s(8-24) stays on
the benchmark line at the top of the ladder while d_H(2-6) lags — pinning the tradeoff as
volume-stable rather than a V=24000 artifact. If confirmed, the honest write-up is: causal
CDT in 2+1D reaches the correct Hausdorff dimension of a 3-manifold and breaks Euclidean
crumpling, but exhibits a persistent aspect-ratio tradeoff that prevents d_H and d_s from
landing on the continuum value simultaneously at accessible volumes — a quantified residual,
not a clean joint convergence.
