# Tier-1 mining of the overnight de Sitter gate run (gate_out/, 18 replicas)

**Date:** 2026-07-08. **Data:** the completed desktop run (N3 = 2000/4000/8000, seeds 1-6, each
300,000 thermalization sweeps + 30,000 measurement samples), copied from WSL and analyzed with
`gate_mine.py` (in repo; validated on synthetic blob/flat controls — recovers a planted wandering
cos² lobe to 2% in W and A at R²=0.9998; a flat Poisson tube reads R²=0.42).
`gate_register.py` named in NEXT_SESSION.md does not exist in the repo; gate_mine.py implements
the method described in CONSOLIDATED_REPORT.md §4.2. Nothing here changes the sampler or its data.

## 1. Spectral dimension across all 18 replicas (was: spot seeds only)

| N3 | d_s peak (mean ± seed sd, n=6) | peak σ | d_H (ball fit) | frac22 |
|------|------------------|--------|----------------|--------|
| 2000 | 2.497 ± 0.036 | 14-17 | 1.650 ± 0.012 | 0.576 |
| 4000 | 2.702 ± 0.026 | 21-23 | 1.877 ± 0.003 | 0.573 |
| 8000 | 2.945 ± 0.030 | 26-28 | 2.152 ± 0.011 | 0.562 |

All replicas completed the full thermalization; frac22 flat in volume (coupled extended phase);
seed scatter ~0.03 — the climb is real and reproducible, now across the full ensemble.

## 2. Extrapolation: does d_s peak head to exactly 3?

**Not decidable from these three volumes, and the naive fit misleads.** A fixed-asymptote power law
ds(N3) = 3 − c·N3^−a returns χ²=51 (1 dof) — formally "tension with 3" — but the increments GROW
with volume (+0.205 then +0.243 per doubling), which no monotone power-law approach to a finite
asymptote can produce. The diagnosis is in the ds(σ) curves: the peak location moves out
(σ ≈ 15→22→27, window capped at σ=39) while the finite-size downturn past the peak truncates the
peak height from the right at every volume. The measured peak is therefore a volume-dependent
UNDERestimate whose bias shrinks as N3 grows — exactly what makes small-volume increments look
anomalously small. Honest verdict: **monotone climb through 2.95 with no visible saturation below
3; convergence to 3 is neither certified nor contradicted. The 16k/32k points (Tier 2, needs the
O(1)-move optimization) are decisive.**

## 3. Short-scale d_s: artifact resolved

ds(σ=3) = 1.94-1.98 across all volumes — consistent with the canonical CDT short-scale value ~2.
The previously flagged "~1.6" is specifically ds(σ=2), the first computable lattice-step point,
which sits below the continuum trend at every volume. Fit-window artifact, not a discrepancy.

## 4. Preregistered de Sitter cos² blob: still NOT condensed (0/18 single lobes)

Iterative cross-correlation registration of all 30,000 raw N(t) snapshots per replica, cos² and
free-exponent fits, Poisson-null baseline per replica:

| N3 | cos² R² (range) | single lobe | peak/mean (mean) | Poisson null |
|------|------|------|------|------|
| 2000 | 0.08-0.19 | 0/6 | 1.59 | 1.71 |
| 4000 | 0.01-0.20 | 0/6 | 1.73 | 1.59 |
| 8000 | 0.05-0.23 | 0/6 | 1.79 | 1.47 |

The gate FAILS at all three volumes: no seed shows a cos² lobe. One genuinely new signal: the
registered concentration peak/mean now EXCEEDS the Poisson null at 4k and clearly at 8k
(1.79 vs 1.47), whereas at 2k it sits at/below the null. The earlier sandbox-era conclusion
("peak/mean ~2 is pure noise artifact") no longer fully holds at 8k — there is above-null volume
concentration developing with N3, just no coherent droplet shape yet. This is what condensation
onset should look like from below, and matches Benedetti-Henson: the full ensemble condenses, but
at larger volumes than these.

## Verdict

The properly-thermalized substrate produces reproducible, volume-improving 3D signatures
(d_s → 2.95, above-null concentration onset) while the preregistered blob remains unmet at
N3 ≤ 8000. Nothing in the data contradicts "correct code, needs volume." The decisive experiment
is unchanged: O(1)-per-move optimization, then N3 = 16000/32000 on the desktop, gate = single
cos² lobe + W ~ N3^(1/3) + d_s extrapolation landing on 3.

## Files
`gate_mine.py` (repo), raw data in Kirk's `Downloads/gate_out/` and WSL `~/cdt_run/.../gate_out/`.
