# Weak-drive KPZ crossover — open question 3 of the CDT emergence handoff

**Date:** 2026-07-06. **Machinery:** C port (`kpz_ring.c`) of `run_bond_current()` from
`cdt_nonequilib.py` (same proposal, same Metropolis-with-bias acceptance), cross-validated against
the Python oracle at L=64 for E=0 and E=2.0 — all lags agree within ≤1.3σ. Frozen-geometry rings =
exact biased ASEP (WASEP); a shuffled fixed-N start is the exact stationary measure, so all budget
went to measurement. Observable: connected variance of bond-current increments Var_c[Q(t₀+t)−Q(t₀)],
pooled over start times, errors from ring-to-ring scatter (2000-replicate ring bootstrap for fits).
Slope 1/2 = Edwards–Wilkinson, 2/3 = KPZ. **Run in the Cowork sandbox in checkpointed ≤45s chunks.**

## Runs

| E | L_ring | rings | meas sweeps | purpose |
|------|------|-----|---------|---------|
| 0.0 | 1024 | 16 | 3×10⁵ | EW control |
| 0.3 | 512 | 32 | 4×10⁵ | banked-null regime, L≈1.5ℓ* |
| 0.3 | 1024 | 32 | 1.5×10⁶ | the weak-drive test, L≈3ℓ* |
| 0.6 | 512 | 128 | 4×10⁵ | crossover fully inside the window |

## Results

**E=0 control:** slope 0.492 ± 0.029 over t∈[10³, 6×10⁴]; increment skewness 0.00 ± 0.07.
Gaussian EW, as required.

**E=0.6 — KPZ asymptote banked.** Over the window t∈[1.5×10⁴, 8×10⁴] (past t*≈7×10³, below
t_L≈10⁵): **slope 0.658 ± 0.021 — 7.4σ from EW 1/2, 0.4σ from KPZ 2/3.** Increment skewness is
persistently non-Gaussian across the window: −0.204 ± 0.013 (t=5×10³) through −0.19 ± 0.06 (t=6×10⁴).
Magnitude sits below the asymptotic stationary-KPZ (Baik–Rains) |0.359|, consistent with
pre-asymptotic finite time; sign-convention matching to Baik–Rains was not done rigorously, so this
is a non-Gaussianity certificate, not a distribution identification. This is the first time in the
program the KPZ exponent has been banked below the strong-drive control (E=2.0).

**E=0.3 — mid-crossover, asymptote still out of reach, but the null needs rewording.**
- Intermediate window t∈[10³, 2×10⁴]: slope 0.575 ± 0.006 (12σ above 1/2) and skewness
  −0.150 ± 0.016 (9σ non-Gaussian). The same elevated plateau appears at E=0.6 (0.573 ± 0.003) and
  is absent at E=0 (0.49). The nonlinearity is unambiguously acting at E=0.3 at accessible times.
- Asymptotic window t∈[1.5×10⁵, 3.7×10⁵] (past the predicted t*): slope 0.474 ± 0.069 — consistent
  with 1/2, 2.8σ below 2/3. The 2/3 asymptote is not resolved. Caveat: at lags approaching the
  record length the overlapping-window variance estimator with per-ring mean subtraction biases the
  slope downward, so this number is soft in the EW direction.
- Onset scaling check: the E=0.6 bend departs the plateau at t≈1.5–2.4×10⁴; t*∼E⁻⁴ predicts the
  E=0.3 bend at ≈2.4–3.8×10⁵ — exactly at the edge of our data. Consistent, not confirmed.

## What this changes

The prior session's conclusion was "genuinely non-integrable but irrelevant to the geometry at
accessible weak drive (z≈2, EW)". The refined statement: **at E=0.3 the drive is not inert — the
current-sector statistics are strongly non-Gaussian and the variance exponent is 12σ above EW at
intermediate times — but the KPZ exponent itself lies beyond t≈3×10⁵ sweeps even at L=1024≈3ℓ*.**
The earlier L=48 null saw neither effect because both signatures develop only at t≳10³. KPZ is
confirmed as the asymptotic class at E=0.6 with the full expected phenomenology (exponent + skew);
by the observed E⁻⁴ onset scaling, E=0.3 is presumably the same class with the window pushed
~16× further out.

## Honest limitations

- Frozen-geometry rings: this is exact WASEP, deliberately isolating the current sector. The
  original open question's second half — KPZ 3/2 *on the fluctuating CDT ring* (geometry-dressed or
  not) — is untouched. That is the natural next run: same measurement with relocate/flip geometry
  dynamics on (Python `run_driven`-style, or a C port of the word dynamics).
- Tracy–Widom/Baik–Rains identification not attempted beyond skewness.
- E=0.3 asymptotic-window estimate carries a known downward estimator bias.
- Single seed per (E, L) point; ring count is the replication axis.
- Raw Q(t) series (~75 MB) were not committed; `kpz_variance_curves.txt` carries the reduced
  variance curves from which all fits are reproducible.

## Files

`kpz_ring.c` (simulator, checkpoint/resume), `analyze_q.py` (variance curve + local slopes),
`bootfit.py` (ring-bootstrap window fits), `kpz_variance_curves.txt` (reduced data).
