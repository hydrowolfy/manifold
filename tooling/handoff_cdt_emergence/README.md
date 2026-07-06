# CDT Emergence — Handoff Package

Self-contained handoff for the emergent-geometry (Causal Dynamical Triangulations) investigation.
Start with **CONSOLIDATED_REPORT.md** — it is the full scientific record, open questions, and the HPC run spec.

## Layout
- `CONSOLIDATED_REPORT.md` — the arc (2D refutation → 1+1D calibration → 2+1D substrate + faithful rebuild), verified citations, open questions, and the HPC handoff spec. Feed this into a deep-research pass.
- `src/` — source code:
  - `cdt_1plus1.py` — validated 1+1D CDT substrate (d_H → 2, Ambjørn–Loll).
  - `cdt_1plus1_topch.py` — faithful spatial-topology-change move (off-manifold; reproduces ALWZ 3/2 exponent + Liouville d_s = 2).
  - `cdt_offmanifold.py` — earlier graft-proxy off-manifold (kept for comparison; unfaithful, gives wrong exponent).
  - `cdt_nonequilib.py` — nonequilibrium winding-current drive (Kolmogorov-violating; WASEP null + positive KPZ control).
  - `cdt_2plus1.py` — pure-Python 2+1D CDT reference oracle.
  - `cdt_2plus1_faithful.c` — **the artifact to scale**: corrected 2+1D Monte Carlo (exact detailed balance via Metropolis–Hastings proposal factors, vertex-link manifold gate, AJL-targeted moves).
- `docs/` — technical records: the AJL move-set spec (vs literature), the faithful-rebuild results, the de Sitter registration/null-model final, the theory note, and the narrative verdict/diagnosis docs.

## Build & run (2+1D, the HPC target)
```
gcc -O3 -o cdt2p1_faithful src/cdt_2plus1_faithful.c -lm
./cdt2p1_faithful selftest         # closed/foliated/manifold self-tests
./cdt2p1_faithful dbtest 6 -1 1.2  # detailed-balance check -> imbalance ~1e-16
# de Sitter run: extended phase (k0 < k0_c, tau=N22/N3 ~ 0.3-0.5), heavy thermalization,
# per-sample registration of N(t), fit cos^2 (n=2). See CONSOLIDATED_REPORT.md §7 for the full spec.
```
The 1+1D scripts are pure Python: `python3 src/cdt_1plus1.py` etc.

## Status in one line
1+1D fully calibrated (off-manifold ALWZ-validated; nonequilibrium a clean WASEP null). 2+1D substrate built, optimized (C, N3~10^4), and corrected to the faithful AJL measure (exact detailed balance, coupled volume-flat order parameter) — but the de Sitter blob does not condense at sandbox volumes; reaching it needs HPC scale (N3~10^4–10^5, 10^5–10^6 sweeps). See CONSOLIDATED_REPORT.md.
