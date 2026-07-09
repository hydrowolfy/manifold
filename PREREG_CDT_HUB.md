# Preregistration: can a hub-suppressing measure term open a STABLE joint d_H+d_s 3-manifold?

Date: 2026-07-09 (seventh campaign, "hub / measure term"). Registered BEFORE the sigma scan.
Campaigns 5-6 established the d_H-d_s tradeoff as a slice-size / f22 obstruction that holds across
the whole k0 x k22 plane. This campaign first proves a structural result, then tests the single
lever that result leaves open.

## 0. The locked-identity result (primary deliverable, proven not scanned)

For any foliated triangulation of S^2 x S^1 in this ensemble, each spatial slice is a triangulated
2-sphere, so per slice F = 2V - 4 (Euler, chi=2). Summing and using that each spatial triangle is
the base of exactly one (3,1) and one (1,3):

    N31 = N13 = 2 N0 - 4 T,     N22 = N3 - 4 N0 + 8 T,     f22 = 1 - 4 (N0 - 2 T) / N3.

Verified EXACT on seed, grown, and thermalized states at k0=2 and k0=5 (matches to the integer;
reproduces the campaign-6 k0-map f22 values from (N0, N3, T)). Consequence: at fixed volume N3 and
fixed T, dN22 = -4 dN0. Spatial-vertex density and (2,2)-fraction are ONE locked degree of freedom.

**Therefore the frontier move requested by the program -- "add spatial vertices WITHOUT removing
(2,2) tets" -- is combinatorially impossible at fixed volume.** Adding one spatial vertex destroys
exactly four (2,2) tets. Every foliation-preserving local move (standard or exotic) preserves the
identity, so no enlarged move set escapes it. The only ways to raise N0 while holding N22 are to
raise N3 (adds volume -> raises slice size s = N3/T -> climbs the d_s curve: the known slice-size
wall) or to raise T (lowers s: the known aspect ladder). Neither decouples the two benchmark
crossings. This closes the "new move" branch of the frontier by proof.

## 1. The one lever the identity leaves open (what this scan tests)

The identity pins simplex counts and the mean degree (sum_v deg = 2 N1 = 2 (N0 + N3), also fixed),
but NOT the degree DISTRIBUTION. Measured: a k0=2 uniform causal state (N0=957, f22=0.38) has
degree mean 14.6, sd 10.2, max 84 -- heavy-tailed HUBS -- whereas the size-matched exact torus is
perfectly regular (deg 14, sd 0). Hubs are the only connectivity freedom left at fixed counts.

New lever (modified action / measure term, outside standard Regge CDT):

    S = k3 N3 - k0 N0 + k22 N22 + sigma * sum_v max(0, deg_v - D0)^2

It suppresses hub over-connection at FIXED simplex counts, hence at fixed f22 (identity). Detailed
balance verified: the term is a state function, proposals are unchanged, Metropolis uses the exact
per-move delta (checked == brute force for all five moves; reverse delta = -forward delta). Manifold
+ foliation preserved under sigma>0 (census bad=0, slices remain 2-spheres). Implementation:
cdt_frontier2_run.py (core verbatim from cdt_causal_run.py + the degree machinery).

## 2. Frozen benchmark, estimators, windows (carried verbatim from campaigns 5-6)

- Estimators VERBATIM: lazy_rw_sdim (d_s), ball_growth_dim (d_H) on the vertex 1-skeleton; each
  value = mean over 8 estimator seeds, report sd.
- Seed-averaged exact-T^3 benchmark, size-matched by N0 (FROZEN):
  m=10 (N0=1000): d_s(8-24)=3.135 +-0.172, d_H(2-6)=2.473
  m=13 (N0=2197): d_s(8-24)=3.071 +-0.160, d_H(2-6)=2.579
  (16-48 secondary: 3.0-3.05; trust only N0 >~ 2000.)
- Primary windows: d_s 8-24, d_H 2-6. Match each state to the benchmark at ITS OWN N0.

## 3. Joint gate (G1-G5, carried from campaign 6)

A config (sigma, D0, V) is a STABLE JOINT 3-MANIFOLD pass iff ALL of:
  (G1) census bad = 0.
  (G2) d_H(2-6) ratio to N0-matched benchmark >= 0.90.
  (G3) |d_s(8-24) - N0-matched benchmark| <= 0.20.
  (G4) NO CONDENSATION: profile CV stable (no upward drift over the measured snapshots), no single
       slice runaway. Baseline k0=2,sigma=0 CV ~ 0.16-0.31.
  (G5) EQUILIBRIUM: f22, d_s, d_H, CV stable over the snapshots; survives an independent-seed
       re-measure (and a V=12000 check if a pass appears).

## 4. Hypothesis + scan (pre-specified)

H_hub: suppressing hubs reduces the over-connection inflating d_s and/or de-saturates ball growth
to lift d_H, at a stable uniform state -> a joint pass. (Direction on d_H is genuinely uncertain:
hubs could inflate or saturate ball growth; the gate, not intuition, decides.)
- CONFIRM: some (sigma, D0) meets G1-G5 at V=6000 and holds under independent re-measure (+V=12000).
- REFUTE: across the scan, d_s and d_H do not BOTH reach benchmark; OR any improvement rides
  condensation (G4 fail) / manifold degradation (G1) / a forced f22 move -- the term merely
  reparameterizes the tradeoff.

Scan: V=6000, T=12 (slice size s=500, the campaign-6 reference). Warm-start each from the sigma=0
equilibrated reference and re-equilibrate. sigma in {0, 0.02, 0.05, 0.10, 0.20}; D0=14 (torus degree)
primary, D0=18 secondary spot-check. Record seed-averaged d_s(8-24), d_s(16-48), d_H(2-6), profile
CV, deg mean/sd/max, f22, census, per snapshot; checkpoint resumably.

## 5. Decision rules

- STABLE JOINT PASS (overturns the wall): some (sigma, D0) meets G1-G5 -> report as headline win.
- WALL HOLDS AGAINST THE MEASURE TERM (completes the negative): every sigma fails G2/G3, or improves
  one dimension only by breaking G4/G5. Combined with the impossibility identity (Sec 0), this closes
  the frontier: neither a new move (impossible) nor a hub-measure term beats the wall.
- PARTIAL: sigma narrows the miss without a full pass -> report the trend with the finite-size caveat.

The identity (Sec 0) is the campaign's primary result regardless of the scan outcome. Gate, windows,
benchmark, and grid above are frozen as of this commit.
