# Next-session brief (start here)

## What just happened (overnight desktop run)
The verified 2+1D sampler ran on the user's 20-core desktop (WSL) via `run_desitter_gate.sh`.
All 18 replicas COMPLETED: N3 = 2000/4000/8000, seeds 1..6, each hitting 300000 thermalization
sweeps + 30000 measurements. Data lives on the user's machine at:
`~/cdt_run/manifold/tooling/handoff_cdt_emergence/gate_out/`  (v<N3>_s<seed>.{json,snap,ck,log})
Reachable from a Windows-side session via the Read tool at the UNC path:
`\\wsl.localhost\Ubuntu\home\hydrowolfy\cdt_run\manifold\tooling\handoff_cdt_emergence\gate_out\...`
(Do NOT request_cowork_directory on a UNC/\\wsl path -- it wedges the bash workspace. Read the
JSONs directly, or have the user copy gate_out into C:\Users\Kirk\Downloads and mount that.)

## Headline result (from the JSON summaries; encouraging but preliminary)
Properly thermalized (vs the ~1e3 sweeps the sandbox could manage), the spectral dimension d_s
runs from ~1.6 (short scale) up toward 3, and the PEAK climbs monotonically and seed-consistently
with volume:

| N3   | tau=N22/N3 | d_s peak | d_H  |
|------|-----------|----------|------|
| 2000 | 0.57      | 2.46     | 1.66 |
| 4000 | 0.57      | 2.71     | 1.88 |
| 8000 | 0.56      | 2.91     | 2.15 |

At 8k, seeds 1 and 3 give d_s-peak 2.907 / 2.910 (reproducible to 3 digits); 4k seeds 1/2 give
2.71 / 2.715. This is the known 2+1D CDT dimensional-reduction signature (d_s -> 3 = emergent
3D geometry) and it confirms the earlier sandbox "flat, no blob" was UNDER-THERMALIZATION, not a
broken ensemble.

## Honest open items (do NOT overclaim)
- The PRE-REGISTERED gate was the de Sitter cos^2 BLOB, and it is NOT yet resolved: the raw
  COV-aligned volume profiles are still lumpy (peak/mean ~1.5-1.9), not a single clean lobe.
  d_s->3 is a complementary signal, not the blob.
- d_s->3 in a 2+1D (3-dimensional) spacetime is the EXPECTED value -> this validates the
  corrected sampler produces genuine 3D-like geometry (entry ticket), it is not a novel result.
- Reached only 2k-8k (the O(N)-per-move code ceiling). d_s-peak is climbing toward 3 but not
  there; d_H well below 3 (finite-size). Short-scale d_s ~1.6 vs canonical ~2 needs checking.

## Teed-up plan (priority order)
### Tier 1 -- mine existing data (cheap, uses gate_out/, needs sandbox recovered)  [task #35]
1. Run `gate_register.py` (in repo) on every `v*_s*.snap`: iterative cross-correlation
   registration + cos^2 fit + Poisson-null baseline -> the pre-registered blob verdict per volume.
2. Full d_s-peak vs N3 across ALL 18 replicas with seed error bars (not just spot seeds).
3. Check the short-scale d_s ~1.6 vs ~2: fit-window artifact or real discrepancy?
4. Extrapolate d_s-peak vs N3 (fit 3 - c*N3^-a): does it head to exactly 3 or plateau below?

### Tier 2 -- the decisive experiment  [task #36]
5. Implement the O(1)-per-move optimization per `OPTIMIZATION_TODO.md` (dynamic redex sets).
   MANDATORY verify: selftest + dbtest + independent recount (`recount_db_verify.py`, via the
   `enumdump` command) on >=1000 states in BOTH phases before trusting it.
6. Extend `run_desitter_gate.sh` to N3 = 16000, 32000; launch on the desktop.
7. Decisive: does d_s reach 3, does the cos^2 blob condense, does the d_s-peak extrapolation land
   on 3?

### Tier 3/4 -- independent adversarial checks + systematics  [task #37]
8. k0 scan: locate the tau=N22/N3 transition; confirm the known extended-vs-degenerate 2+1D
   phase structure at k0_c (Kommu ~3.3 / AJL ~6.6).
9. Quantitative overlay of our d_s(sigma) curve vs published 2+1D CDT.
10. Re-run the deep-research adversarial referee on the new d_s->3 series.
11. Systematics: thermalization-doubling drift, hot/cold init-independence, d_H fit-window
    sensitivity, aspect-ratio (T) dependence.

## Practical notes
- The run is COMPLETE (machine free). To resume/extend: `bash run_desitter_gate.sh 16` re-runs
  and resumes from gate_out checkpoints; edit VOLS to add 16000/32000 (after the O(1) opt).
- snap_peakmean reads 0.0000 in the JSONs (that accumulator field didn't populate) -- ignore it;
  it was a noise-artifact metric anyway. The real profile is in `Nt_profile` + the `.snap` files.
