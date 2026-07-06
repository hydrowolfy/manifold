# 2+1D de Sitter Failure — Diagnosed (three converging findings)

The "de Sitter blob fails" conclusion was mostly a measurement + phase + fit-function problem, not a fundamental model defect. Three parallel diagnostics converged.

## Finding 1 (theory) — we fit the WRONG function
The 2+1D de Sitter spatial-volume profile is **N(t) ~ cos²(t/(B·N^{1/3}))**, exponent **n=2**, width N^{1/3}. cos³ is the 3+1D result. Fitting 2+1D data to cos³ is wrong by construction. Verified: Kommu arXiv:1110.6875, AJL hep-th/0011276.

## Finding 2 (ergodicity) — the "tube" is a wandering single lobe, mis-averaged
The decisive test: a blob-start (volume piled in central slices) and a flat-tube-start both evolve to the **same** equilibrium — a single dominant lobe (peak/mean ~2–3) whose center **wanders around the periodic time ring**. Raw time-averaged N(t) is multi-lobe (R²≈−1.2) — the reported "tube" — but the **center-of-volume-aligned** ensemble profile is a **single lobe (R²≈0.71)**. A wandering lobe smeared by naive averaging fabricates a fake multi-lobe tube. The volume dynamics is ergodic (τ_int ≈ 35 sweeps for the shape, finite and decaying); no move is missing for ergodicity. The C-port measurement did not align per-sample correctly.

## Finding 3 (phase scan) — we were on the wrong side of k0_c
The (2,2) tetrahedra carry the timelike inter-slice coupling; a de Sitter blob needs them abundant. At the default k0=2 the fraction is **0.09** (vs ~0.33 balanced) — a decoupled, (2,2)-poor geometry. Lowering k0 to ≈ −1…−2 restores it to **~0.4**. Theory confirms: the lumpy decorrelated tube is the defining signature of the **k0 > k0_c decoupled phase** ("uncorrelated 2d gravity / foam of baby universes"); the de Sitter blob lives at **k0 < k0_c**, order parameter τ = N22/N3. The "worsens with volume" symptom is exactly the decoupled phase (the extended phase would improve with N).

## Ruled out (theory, verified) — the asymmetry α is NOT missing
In 2+1D a triangulation has only two independent bulk DOF, so the action is always −k0·N0 + k3·N3 regardless of α; α only shifts k0_c, it does not create or destroy the phase. (Unlike 3+1D, where Δ is an essential axis.) No missing action term. Source: Kommu arXiv:1110.6875.

## The corrected protocol (converged prescription)
1. **Phase:** run at k0 below k0_c — locate k0_c via the N22/N3 jump; get τ = N22/N3 onto the extended (coupled, ~0.4) side.
2. **Measurement:** center-of-volume-align **each sample** before averaging N(t) (a single wandering lobe, not a tube).
3. **Fit:** cos², not cos³.
4. **Geometry:** T ≳ 3–5·N3^{1/3}; soft ε so N3 fluctuates ~√Nbar.
5. **Success =** τ on the extended side, single cos² lobe on a thin stalk, fit R² **improving** with volume.

## Honest tension to resolve in the re-test
The scan agent, even at restored (2,2)≈0.4, still saw 2–3 lobes (R²~0.4–0.63) COV-aligned, while the ergodicity agent saw a clean single lobe (R²~0.71). The difference is most likely per-sample alignment + thermalization (the scan was under-thermalized by its own caveat) + being well below k0_c + the cos² (not cos³) fit. The corrected-protocol run settles whether the blob is genuinely there.

Citations verified: AJL hep-th/0011276 (extended phase, k0_c, decoupled phase); Kommu arXiv:1110.6875 (two-coupling 2+1D action, α absorbed, τ=N22/N3 order parameter, cos² de Sitter). Note: arXiv:1108.3932/1205.1229 are primarily the 3+1D phase-order papers — the canonical 2+1D refs are hep-th/0011276 and Kommu.
