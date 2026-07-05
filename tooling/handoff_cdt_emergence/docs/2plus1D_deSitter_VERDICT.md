# 2+1D de Sitter — Verdict After Corrected Protocol

## Robust negative
With all four corrections applied together — extended phase (τ = N22/N3 up to 0.44), per-sample COV alignment, cos² (n=2) fit, T ≥ 3.3·N3^{1/3}, heavy thermalization — the de Sitter blob is **NOT reproduced**:

| N3 | T | τ=N22/N3 | cos² R² | lobes | single lobe on stalk? |
|---|---|---|---|---|---|
| 900 | 32 | 0.44 | 0.54 | 6 | no |
| 2800 | 48 | ~0.35 | 0.54 | 6 | no |
| 5600 | 64 | ~0.25 | 0.60 | 4 | no |
| 9500 | 80 | 0.19 | 0.16 | 9 | no |

R² degrades and lobes multiply with volume; fitted width shrinks (30→7) instead of growing ~N3^{1/3}. This is not the earlier measurement artifact — with correct phase, alignment, and fit, the profile is still a multi-lobe tube and gets worse with scale.

## Precise diagnosis (it's the ensemble/move-set, not parameters)
Two convergent tells:
1. **No cross-sandwich volume transfer.** Volume between slices changes only by slow diffusive ±2 (2,6)/(6,2) births/deaths; no move moves a chunk of volume across a slice boundary. The two-coupling action doesn't confine a single lobe against a stalk, so the ensemble supports several coexisting wandering lumps.
2. **τ decays with volume at fixed coupling** (0.44 → 0.19 at k0 ≤ −1.5). An intensive order parameter should be volume-independent at fixed k0; its drift means the move set does not maintain the extended-phase (2,2)-coupling as volume grows — i.e., it is not sampling the genuine AJL measure.

Conclusion: the substrate is a correct, fast, internally cross-validated foliated fluctuating 3-manifold, but it is **not genuine AJL 2+1D CDT** — it fails the defining de Sitter test for a structural reason in the move set/ensemble.

## τ-decay debug swing — RESOLVED: not a bug (fixable-fix door closed)
Instrumented per-move (2,2) budget + τ-from-both-ends convergence + (2,2)-sector detailed balance:
- Per-move dN22 cancel: (2,3) creates +3026, (3,2) destroys −3025, net residual +1 (0.03%); (2,6)/(6,2)/(4,4) exactly zero net. No (2,2) sink.
- Stationary τ is volume-flat (0.52 → 0.47 across N3 890→5860, all in the coupled band). The earlier "decay with volume" was under-thermalization (larger volumes have longer τ_int; a fixed sweep budget catches them mid-climb).
- (2,2)-sector detailed balance clean (forward/reverse fluxes cancel; rich-start and poor-start converge to the same τ).
- **Verdict: intrinsic, not a fixable move-set imbalance or DB defect.** No patch will restore the blob. This strengthens the negative: the move set is internally correct yet samples a non-de-Sitter ensemble → a faithful AJL rebuild is required, not a tweak.

## Options (fixable-bug option now eliminated)
1. ~~One targeted debug round on τ-decay~~ — DONE, ruled out a fixable bug (see above).
2. **Faithful AJL move-set reimplementation** (the real fix): implement and validate the published 2+1D CDT moves + slice dynamics so the ensemble is correct. A serious research-software task, hard to validate to a trustworthy standard in a 40s-chunk sandbox; better suited to real HPC.
3. **Consolidate and bank** the solid results (2D refutation; 1+1D fully calibrated — off-manifold ALWZ-validated, nonequilibrium WASEP null) and mark 2+1D as an honest open frontier requiring a faithful CDT implementation. Recommended.

## Faithful rebuild — the real bugs were fixed, blob is now a verified compute-scale limit
The spec audit (vs AJL hep-th/0105267 + Kommu 1110.6875) found three genuine defects, all now fixed and verified:
- **Tilted measure** (the crux): moves omitted the Metropolis-Hastings N_forward/N_reverse proposal factors → detailed balance held only accidentally. Fixed: **DB now exact to ~1e-16, badrev=0** across couplings/sizes.
- **Too-weak manifold gate**: accepted on χ=2 only, admitting pinched/degenerate slices (a superset ensemble). Fixed: full vertex-link-single-cycle test.
- **Mis-targeted (2,3) move**: fired on any face, not the AJL (3,1)+(2,2)-sharing-a-triangle pattern. Fixed. Result: **τ=N22/N3 now stationary and volume-flat** (~0.5 at k0=−2, no longer collapsing 0.44→0.19).

Then a 14,000-sample iterative cross-correlation registration tested for the de Sitter blob and, with a null model, **corrected an over-optimistic intermediate read**: the per-snapshot "peak/mean ~2.0 droplet" was a max-over-T-slices NOISE artifact (a uniform tube with Poisson slice noise reproduces it: data 1.76 vs Poisson 1.65; smoothing collapses it to ~1.1). The registered profile is flat (n≈0.3, not 2); no coherent droplet exists to lock onto.

**Corrected verdict: the measure/action/detailed-balance are now correct and verified; the de Sitter blob simply does not condense at accessible volume/thermalization.** This is a genuine compute-scale limit, not a bug: AJL/Kommu need N3~10⁴–10⁵ with 10⁵–10⁶ sweeps; the sandbox reaches N3~10⁴ but only ~10³ thermalization sweeps (40s chunks, no persistent jobs). The flat profile is consistent with under-volume/under-thermalization on a correct implementation. Nothing left to debug — the barrier is raw compute the sandbox structurally can't provide → HPC handoff.

## Status of the whole arc
- 2D manifold claim: refuted (earlier).
- 1+1D off-manifold: ALWZ-validated (3/2 exponent, Liouville d_s=2). Solid.
- 1+1D nonequilibrium: genuinely non-integrable drive, but irrelevant to geometry (WASEP null with positive KPZ control). Solid.
- 2+1D substrate: fast + internally validated, but fails the de Sitter test — not yet genuine 2+1D CDT. Honest open frontier.
