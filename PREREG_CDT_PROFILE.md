# PREREG: spatial-volume profile N3(t) at the near-miss points -- physical extended phase or collapse?

Preregistered BEFORE measuring any study-state profile (discipline lesson 13). Committed first,
then measured. Side-quest, not a campaign: it decides how to READ the program's near-misses.

## Question

Standard 2+1D causal CDT (S^2 x S^1, alpha=1) puts EITHER d_H or d_s on the exact-T^3 benchmark
but not both (REPORT_CDT_FRONTIER / _K0 / _HUB). The two near-misses live at:
- the **alpha/k22-condensed** states (low f22 / high k0 or k22) where **d_s** falls onto the benchmark;
- the **high-sigma hub-suppressed** states where **d_H** passes (ratio >= 0.90).
At each near-miss, is the geometry a GENUINE physical extended phase (a real de Sitter-like spatial-
volume profile spread across the time slices) or a COLLAPSE / condensation artifact (a blob-with-stalk:
most volume piled into a few slices)? This preregisters the quantitative signature that decides it.

## Observable and estimator

For a foliated state, the spatial-volume profile is
  **p(t) = N3^SL(t) = #{ spatial triangles whose 3 vertices all lie in slice t }, t = 0..T-1**
i.e. `st.stris` grouped by `st.time` -- the standard CDT spacelike-2-volume-per-slice, identical to
the profile `remeasure.py` already reduces to `prof_cv`. Deterministic given a state snapshot (no
estimator seed). Measured with `profile_dump.py` (read-only); CV cross-checked against `remeasure.py`.

Derived shape metrics (all on p(t), mean = mean(p), max/min over slices, total = sum(p)):
- **CV** = std(p)/mean (population std, matches remeasure `prof_cv`).
- **max/mean**, **min/mean** (peak height and floor depth in units of the mean).
- **C1** = max(p)/total, **C2** = (top-2 slices)/total (volume concentration).
- **stalk length** = #{ slices with p(t) <= 0.25*mean } (slices depleted toward the minimal 2-sphere floor).
- **blob width** = #{ slices with p(t) >= 0.5*max } (how many slices carry the peak).
- **shape**: unimodal-smooth hump/plateau vs isolated spike (# interior local maxima >= 0.5*max).

Error bars: p(t) is a deterministic functional of a snapshot. For states generated here, >=2
decorrelated equilibrium snapshots; CV also cross-checked against the seed-averaged CV in the reports.
Every scored state must have census bad=0 (still a valid simplicial 3-manifold) and be at equilibrium
(no upward CV drift / collapsing min slice across the last sweeps) -- a transient crossing does not count.

## Reference shapes (the two poles)

- **Exact-T^3 Kuhn torus** (the d_H/d_s scoring benchmark): translation-invariant => FLAT profile,
  CV=0, max/mean=1, no stalk. Extreme uniform/extended reference.
- **Known 2+1D CDT de Sitter profile** (the physical extended phase in standard CDT): a single smooth
  extended hump (cos-power-ish; the exact power is NOT load-bearing here), spanning most slices, with a
  moderate peak and at most a short minimal "stalk" (a lattice cutoff of a few slices). A genuine de
  Sitter hump therefore sits INSIDE the extended box below (moderate peak, broad, smooth, no long stalk).
- **Collapse / condensation**: most volume piled into 1-2 slices (a "blob") with the remaining slices
  depleted to the minimal-2-sphere floor (a "stalk"): high CV, high max/mean, long stalk.

## Decision rule (FIXED before measuring)

Score a profile **PHYSICAL EXTENDED PHASE** iff ALL of:
- **E1 (no dominant spike):** max/mean <= 2.5 AND C1 <= 0.20 (no single slice holds > 20% of the volume; uniform T=12 => 1/12 ~ 0.083).
- **E2 (no stalk):** min/mean >= 0.5 AND stalk length = 0.
- **E3 (broad, smooth support):** blob width >= ceil(2T/3) (= 8 of 12 at T=12) AND the profile is a single smooth hump/plateau (<= 1 interior local max >= half-max; no isolated spikes).
- **E4 (dispersion near thermal):** CV <= 0.35 (within ~1-2x the uniform k0=2 thermal baseline; well below the condensed regime).

Score **COLLAPSE / CONDENSATION ARTIFACT** iff ANY of:
- **K1 (spike):** max/mean >= 3.0 OR C1 >= 0.30 OR C2 >= 0.45 ("most volume in a few slices").
- **K2 (stalk):** stalk length >= ceil(T/4) (= 3 of 12) with min/mean <= 0.25 (a depleted tube of minimal slices).
- **K3 (dispersion):** CV >= 0.6 (the condensed regime; reports put condensed states at 0.76-1.21).
Dynamical confirmation: a K-tripping state that is ALSO still drifting (CV rising / min slice collapsing
across sweeps) is a live collapse; one that is K-tripping but CV-stable is a settled condensed equilibrium.
Both count as COLLAPSE. Neither E-set-complete nor any K tripped => **MARGINAL / TRANSITIONAL** (reported as such).

## Study states (all V=6000, T=12, slice size s=N3/T~500 -- matched to the reports)

- **(c) NEUTRAL** k0=2, k22=0, sigma=0 (cached `causal_k0+2.00_T12_V6000_s0.pkl`). Report: uniform, CV 0.16-0.31.
- **(b) HUB-SUPPRESSED, d_H passes** sigma=0.10, k0=2, k22=0, D0=14 (cached `hubscan/sig_0.100.pkl`); d_H ratio 0.91. Full sigma ladder 0.00-0.20 also profiled (cached).
- **(a) ALPHA/k22-CONDENSED, d_s hits benchmark** the low-f22 lever. Canonical point k0=6, k22=0 (REPORT_CDT_K0: d_s 3.065 ~ benchmark 3.10-3.14, CV 0.76, min slice collapsing 110->16). Campaign 6 proved k0(up) and k22(up) are the SAME f22 lever, so this IS the alpha/k22-condensed regime; generated fresh at V6000/T12 (fresh growth starts near its equilibrium f22~0.036) and d_s re-confirmed on benchmark by remeasure. Cached smaller alpha exemplars (k0=2,k22=1.0 V1500/T8; k0=5 V700/T10) profiled as cross-lever corroboration.

## Hypotheses (preregistered)

- **H_neutral:** NEUTRAL is EXTENDED (uniform), E-set holds.
- **H_hub:** the sigma=0.10 hub-suppressed state where d_H passes is EXTENDED -- its d_H gain is a
  connectivity reshaping at fixed extended geometry, NOT bought by condensation (report CV 0.276, stable).
- **H_cond:** the alpha/k22-condensed state where d_s hits benchmark is COLLAPSE -- its d_s gain IS a
  condensation artifact, not a physical 3-manifold (report CV 0.76 rising, min slice collapsing).

## Reading (preregistered, so the verdict is not post-hoc)

- If **H_cond = COLLAPSE and H_hub = EXTENDED**: the two near-misses differ in KIND. The d_s=benchmark
  (alpha/k22) crossing is a collapse artifact -- not a real extended 3-manifold -- so that near-miss should
  NOT be read as "almost a physical universe"; the d_H=benchmark (hub) crossing is a genuine extended
  geometry that simply lands the wrong dimension. The physically meaningful frontier is the hub/d_H side.
- If **BOTH COLLAPSE**: both near-misses are artifacts; neither is a candidate physical phase.
- If **BOTH EXTENDED**: both are genuine 3-manifolds that merely miss jointly; the wall is purely dimensional.
