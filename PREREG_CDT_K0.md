# Preregistration: does a k0 phase open a STABLE joint d_H+d_s 3-manifold pass?

Date: 2026-07-09 (sixth campaign, "k0 x k22"). Registered BEFORE the scan. Campaign 5
(REPORT_CDT_FRONTIER.md) found: (a) the d_H-d_s tradeoff is a volume-stable, slice-size-controlled
obstruction at k0=2; (b) the alpha (k22) lever moves BOTH dimensions onto the benchmark but only
by driving spatial-volume CONDENSATION -- the joint crossing is a transient, not a stable
equilibrium. Every campaign fixed k0=2. This campaign asks: does a different CDT phase (different
k0) suppress the condensation and permit a STABLE joint pass? New resource: uncapped chains on a
local WSL box (no 45 s sandbox cap), so chains can be properly thermalized with real MC statistics.

## 1. Frozen benchmark, estimators, windows (carried from campaign 5)

- Estimators VERBATIM: `lazy_rw_sdim` (d_s), `ball_growth_dim` (d_H) on the vertex 1-skeleton.
  Every value = mean over >=8 estimator seeds (report sd). Plus MC error from >=6 decorrelated
  snapshots per equilibrated config.
- Seed-averaged exact-T^3 benchmark, size-matched by N0 (FROZEN):
  m=10 (N0=1000): d_s(8-24)=3.135+-0.172, d_H(2-6)=2.473
  m=13 (N0=2197): d_s(8-24)=3.071+-0.160, d_H(2-6)=2.579
  m=16 (N0=4096): d_s(8-24)=3.149+-0.068, d_H(2-6)=2.579
  (16-48 secondary: 3.0-3.05; trust only N0>~2000.)
- Primary windows: d_s 8-24, d_H 2-6. NOTE: k0 and k22 change N0 at fixed N3 -- match each state
  to the benchmark at ITS OWN N0.

## 2. Joint gate (adds an anti-condensation criterion G4 this campaign)

A config (k0, k22, V) is a STABLE JOINT 3-MANIFOLD pass iff ALL of:
  (G1) census bad = 0.
  (G2) d_H(2-6) ratio to N0-matched benchmark >= 0.90.
  (G3) |d_s(8-24) - N0-matched benchmark| <= 0.20.
  (G4) NO CONDENSATION: over the equilibrated (second-half) window the spatial-volume profile is
       STABLE -- (i) profile CV shows no significant upward drift (linear slope over the window
       consistent with zero within the snapshot scatter), and (ii) no single slice runs away
       (max_slice/mean_slice not monotonically increasing). The k0=2,k22=0 baseline CV is
       0.16-0.31 (thermal, size-dependent); a pass must be comparable AND non-drifting, NOT the
       0.26->0.50 monotone rise that flagged the k22 condensation in campaign 5.
  (G5) EQUILIBRIUM: f22 and both dimensions stable across the last >=1000 sweeps (measured, not
       assumed); the pass must survive an independent-seed re-measure and a larger-V check.

Campaign 5 showed no k0=2 config passes (fat fails G3, thin fails G2, k22>0 transiently passes
G1-G3 but fails G4/G5 by condensing). The question is whether any k0 != 2 changes this.

## 3. Scan (pre-specified)

- k0 grid: {0.5, 1.0, 2.0, 3.0, 4.0, 5.0} (spans the 2+1D A<->C phase structure; higher k0
  favors more vertices / a more branched, less condensed geometry).
- k22 grid: {0.0, 0.5, 1.0, 1.5, 2.0} (the asymmetry that improved both dims but condensed).
- Aspect: near-balanced fat T (T=15 @ V=12000) -- the d_H-favorable side; the hunt is for a k0
  that lets k22 fix d_s there WITHOUT condensing.
- Volume: PRIMARY V=12000 (N0~1900-2600, 8-24 trustworthy, thermalizes in reasonable local wall
  time). Any config passing G1-G4 at V=12000 is re-run at V=24000 (and a second seed) for G5.
- Protocol (uncapped, local): grow to V; tune k3 to hold N3=V; equilibrate LONG (>=2000 sweeps
  past f22 plateau); then take >=6 snapshots spaced >=200 sweeps, each measured with 8 estimator
  seeds; record d_s(8-24), d_s(16-48), d_H(2-6), profile CV, max/mean slice, f22, census. Two MC
  seeds per config. Checkpoint every snapshot (resumable).

## 4. Decision rules (the verdict)

- STABLE JOINT PASS (the win / overturns the wall): some (k0,k22) meets G1-G5 at V=12000 AND
  holds at V=24000 with a second seed and independent estimator seeds -> a genuine emergent 3-
  manifold in a k0 phase. Report with full error bars.
- WALL HOLDS ACROSS PHASES (stronger negative): across the whole k0 x k22 grid, every config
  either fails G2/G3, or (if it reaches the joint point) fails G4 by condensing / G5 by drifting.
  -> the d_H-d_s obstruction is not a k0=2 artifact; it survives the CDT phase diagram. Report the
  k0 x k22 map (d_H, d_s, CV, drift) as the deliverable.
- PARTIAL: a k0 that reduces the condensation and narrows the joint miss but does not fully pass;
  report the trend + an honest extrapolation.

## 5. Discipline / execution

Seed-averaged benchmark; honest error bars (estimator + MC) and finite-size caveats; checkpoint
resumably; roll lessons + results onto branch causal-cdt-scaling via the GitHub connector (code/
text only; pickles and float logs stay out of git). Uncapped chains run on the local WSL box; the
runner is a single dependency-free file verified in-sandbox to reproduce the committed estimators
before launch. This gate and grid are frozen as of this commit.
