# 2+1D CDT de Sitter — FINAL: iterative-template registration of the wandering droplet

Subcommittee: DROPLET-REGISTRATION. Task: close the last de Sitter gap by proper
registration (iterative template / circular cross-correlation) + many more samples,
without touching the physics/moves/measure/action.

## What was done (measurement only — physics untouched)
- Added a MEASUREMENT-ONLY snapshot dump to `cdt_2plus1_faithful.c`: env var
  `CDTSNAP=<file>` appends each measured per-snapshot slice-volume vector N(t)
  (length T, comma-separated, one line per sample) across checkpointed chunks.
  It records the SAME `vol[]` already sampled by the existing measure loop — no
  change to moves, redex counters, M-H acceptance, action, or the measure.
  Verified: `dbtest` still reports DETAILED BALANCE EXACT (worst rel. imbalance
  0.000e+00, badrev=0) after the edit. `cdt_2plus1.c` and all `cdt_*.py` untouched.
- Ran the faithful binary in the extended phase (k0=-2, k3=1.2, eps=0.04),
  well thermalized, checkpoint+resume in <40s chunks.

## Samples collected
| run            | k0 | T  | N3   | therm iters | SAMPLES | file          |
|----------------|----|----|------|-------------|---------|---------------|
| 3k (primary)   | -2 | 48 | 3000 | 4000        | **8015**| snap3k.csv    |
| 6k (primary)   | -2 | 56 | 6000 | 3393        | **6024**| snap6k.csv    |
| 3k compact test| -2 | 24 | 3000 | 1500        | 1919    | snap3kT24.csv |

Total > 14,000 registered snapshots — well above the >=2000-5000 target, and
~20-40x the 200-500 samples the previous REBUILD run was limited to.

## Registration method (implemented, register.py)
Iterative template / circular cross-correlation, exactly as specified:
(a) template initialized as the COM-aligned mean; (b) each snapshot rolled by the
circular shift maximizing cross-correlation with the current template — shifts are
found on a WIDE-smoothed snapshot vs a wide-smoothed template (locks the broad
droplet, robust to per-slice Poisson noise, NOT a single peak/COM); the RAW
snapshot is accumulated at that shift to preserve amplitude; (c) re-average, (d)
iterate. Convergence reached (per-iter fractional template change fell to ~0.05-0.07
and stabilized within 3-4 iterations at both sizes).

## RESULT — the registered ensemble profile

| run          | samples | registered peak/mean (raw / smoothed) | cos^2 R^2 | cos^2 W | free-n R^2 | free-n | n_lobes |
|--------------|---------|---------------------------------------|-----------|---------|------------|--------|---------|
| 3k  T=48     | 8015    | 1.49 / **1.07**                       | 0.23      | 7.6     | 0.29       | 0.30   | 2       |
| 6k  T=56     | 6024    | 1.56 / **1.13**                       | 0.52      | 25.9    | 0.55       | 0.35   | 2       |
| 3k  T=24     | 1919    | 1.60 / **1.22**                       | 0.35      | 4.0     | 0.35       | 0.70   | 1       |

- The **registered, smoothed** ensemble profile is essentially FLAT (peak/mean
  1.07-1.22) — a ~15% ripple around a uniform tube, not a cos^2 lobe.
- The cos^2 (n=2) fit is poor (R^2 = 0.23-0.52) and the FREE-n fit does not find
  n~2: it drives n -> 0.3-0.7 (a broad, near-flat shape), NOT the de Sitter n=2.
- It is NOT a single lobe on a minimal stalk: no contiguous high-volume droplet
  and no near-minimal (4-triangle) stalk region appears in the registered profile
  or in any individual snapshot.

## W ~ N3^{1/3} check
FAILS. cos^2 W(6k)/W(3k) = 3.4 (and free-n W actually DECREASES 22.9 -> 16.1),
versus the expected (6000/3000)^{1/3} = 1.26. The fitted "width" is set by where
the noise-dominated fit happens to place a broad cosine, not by a self-similar
droplet, so the 1/3 exponent is not present.

## WHY registration does not resolve a lobe — the decisive diagnostic
Registration is working; there is simply no coherent droplet to lock. Per-snapshot
structure:
- Raw per-snapshot peak/mean ~ 1.6-1.8, BUT after smoothing over even ~4-5 slices
  it collapses to **1.06-1.16**. Mass in a T/4 window around the (smoothed) peak
  is 0.284 vs the uniform value 0.271 — essentially NO spatial concentration.
- Individual N(t) vectors are noisy near-uniform tubes: highs and lows are
  scattered slice-to-slice with no contiguous blob and no minimal stalk
  (per-snap min ~ 8 at 3k, far above the 4-triangle minimal 2-sphere).

Null-model control (uniform tube + Poisson slice noise, matched mean):
| run     | DATA raw / smoothed pk/mn | POISSON-UNIFORM raw / smoothed pk/mn |
|---------|---------------------------|--------------------------------------|
| 3k T=48 | 1.76 / 1.06               | 1.65 / 1.10                          |
| 6k T=56 | 1.76 / 1.10               | 1.49 / 1.07                          |
| 3k T=24 | 1.63 / 1.16               | 1.37 / 1.10                          |

The measured `snap_peakmean` (~1.6-2.0) is almost entirely explained by per-slice
Poisson/statistical fluctuation of a roughly UNIFORM tube. It is a max-of-T single-
slice statistic, not evidence of a de Sitter droplet. The earlier REBUILD reading
of "snap_peakmean ~ 2.0 => a droplet-on-a-minimal-stalk forms in every config" was
a misinterpretation of that noise statistic: smoothing (the physically correct
scale for a droplet spanning many slices) removes essentially all of it.

## VERDICT
**Still unresolved — and the correct diagnosis is that there is NO resolvable de
Sitter cos^2 blob in these configurations, not merely a statistics/alignment
shortfall.** With proper iterative-template cross-correlation registration and
8015 / 6024 samples (20-40x the prior budget), the registered ensemble profile is
flat (peak/mean 1.07-1.13), the cos^2 fit is poor (R^2 0.23-0.52), the free-n fit
gives n~0.3 (not 2), it is not a single lobe on a minimal stalk, and W does not
scale as N3^{1/3}. A null uniform-tube+Poisson model reproduces the per-snapshot
`snap_peakmean` almost exactly, so the previously-claimed per-configuration droplet
is a per-slice-noise artifact. The registration/statistics gap is therefore CLOSED:
adding samples or better alignment will not produce a cos^2 lobe, because the
underlying per-snapshot geometry is a near-uniform spatial tube, not a condensed
droplet.

What WOULD be needed to obtain a genuine de Sitter blob (i.e. what is actually
missing, beyond measurement): a regime/parameters where the extended-phase
geometry actually CONDENSES a macroscopic spatial droplet. Concretely: (i) deeper
into the extended phase and/or larger volumes (AJL/Kommu use N3 ~ 10^4-10^5 with
~10^5-10^6 sweeps) so the droplet is many-slice-wide and rises well above Poisson
slice noise; (ii) a genuine near-minimal stalk (slice volume approaching the
4-triangle 2-sphere) must appear in individual snapshots — it does not here. Until
a smoothed per-snapshot peak/mean clearly exceeds the uniform+Poisson null (which
it does not at any size tested, up to smoothed 1.13-1.22), no amount of registration
can synthesize a cos^2 lobe. The measure/action/detailed-balance are correct and
untouched; the missing ingredient is the physical droplet condensation itself in
the accessible volume/thermalization budget.

(Note: this SUPERSEDES the REBUILD "droplet forms in every configuration" reading,
which rested on the unsmoothed snap_peakmean statistic now shown to be noise.)
