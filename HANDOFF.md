# HANDOFF: causal CDT scaling program (cold-start brief)

Updated 2026-07-08, end of the fourth campaign. The work now lives in git: branch
`causal-cdt-scaling` of https://github.com/hydrowolfy/manifold (cut from `explore/3d-manifold`).
A fresh session clones the repo instead of relying on a mounted folder.

## 1. Environment setup (fresh session, Linux sandbox)

    git clone https://github.com/hydrowolfy/manifold.git /tmp/m
    cd /tmp/m && git checkout causal-cdt-scaling
    pip install networkx --break-system-packages        # the ONLY dependency (no numpy)

All campaign code, reports and the results log are committed on the branch (no copy step).
Selftest gate before any physics (must print ALL CAUSAL SELF-TESTS PASSED):

    cd /tmp/m && PYTHONPATH=.:tooling python3 cdt_causal_run.py --selftest

## 2. Checkpoints are NOT in the repo (deliberate)

The 24 chain-state pickles (~9.3 MB `cdt_checkpoints.tar.gz`) are intentionally left out of
git (binary, large; the connector can't attach release assets or LFS pointers). They are
also not required:
- Every measurement is in `cdt_causal_results.jsonl` (204 records); the physics conclusions
  are fully reproducible from it.
- To resume mid-chain, regenerate pickles by rerunning the exact `--chunk` command for a
  chain (fixed `--seed`); the runner grows to volume and re-thermalizes deterministically per
  seed. `.gitignore` excludes `scratch/`, `*.pkl`, and the tarball.
If a session still has the tarball locally: `tar xzf cdt_checkpoints.tar.gz -C /tmp/m` creates
`/tmp/m/scratch/*.pkl`. Checkpoints unpickle ONLY inside `cdt_causal_run.py` run as __main__
(the Causal class lives in __main__); resume = rerun the same `--chunk` command with
`--scratch <dir>` pointing at the pickles.

## 3. Runner usage (important flags)

    PYTHONPATH=.:tooling python3 cdt_causal_run.py --chunk \
      --k0 2.0 --T 19 --V 24000 --seed 0 --tune 500 --sweeps 1400 \
      --budget-s 36 --scratch <writable-dir>/scratch --log <writable-dir>/rec.jsonl

- Default `--scratch` is `/tmp/m/scratch`; pass a WRITABLE dir if the clone is read-only.
- Each `--chunk` resumes the pickle by (k0,T,V,seed) tag, advances within `--budget-s`
  wall-clock, measures, appends one JSON line, re-pickles. Fully resumable.
- Keep budget so sweep-loop + measurement + save < ~44 s: ~40 s solo, ~36 s for a
  2-parallel pair at V=24000 (heavier measure + two 3.3 MB saves overran a 45 s cap at 40 s).
- `--measure-long` (tmax=100) measures the current pickle state (no advance) and writes a
  `long_measure` record with d_s windows 4-12/8-24/16-48/30-90 and d_H 2-6/3-8/4-10.
- Windows 16-48 and 30-90 are size-contaminated below N0~2000 (and 30-90 still is at
  N0~3800); 8-24 is the trustworthy long d_s window.

## 4. State of evidence (see the four REPORT_CDT_*.md, in order)

Genuine 2+1D causal CDT: typed (3,1)/(2,2)/(1,3) tets on S^2 x S^1, foliation-preserving
Pachner moves, Metropolis with k3 auto-tune; census bad=0 in every snapshot ever taken.
Breaks Euclidean crumpling (Euclid controls: d_s pinned 3.87-3.98, never flow).

Balanced-aspect ladder (T ∝ V^(1/3) normalised to T=12@V=6000; k0=2, 2 seeds) verdict
(REPORT_CDT_CONVERGENCE.md): NOT a clean joint 3-manifold convergence, but no crumple-back:
- d_H(2-6) CONVERGES: fat-ladder ratio 0.75 -> 0.82 -> 0.93 (V=6000/12000/24000), near
  parity at V=24000, gap still closing.
- d_s(8-24) does NOT join it on the d_H-optimal (fat) ladder: excess +0.22/+0.68/+0.41, not
  closing. Thin chains (T=16@6000, T=18@12000) put d_s on the line (-0.14/+0.28) but d_H
  lags (0.65/0.78). No single aspect gives both -> real d_H-d_s finite-size tradeoff.
- d_H(3-8): tracks benchmark slope but ratio stuck ~0.5 on both ladders.
Benchmark = exact flat T^3 (Kuhn), now m=5..16; score against it, never against 3.0.

NB: the handoff formula `T=round(1.9*V^(1/3))` was wrong (gives ~35 at V=6000); the
aspect-preserving constant is 0.66, i.e. T = round(12*(V/6000)^(1/3)) = 12/15/19.

## 5. What remains

One thin-aspect point at V=24000 (T ~ 22-23, k0=2, 2 seeds) to confirm d_s(8-24) stays on
the benchmark line at the top of the ladder while d_H(2-6) lags — pinning the tradeoff as
volume-stable. Optional: a Euclid control at matched large size (n0~1000, tets~7000) to
extend the negative-control arm above its current n0<=500.

## 6. Cost calibration (measured)

Throughput ~ 8 sweeps/s at V=6000, ~2.4-3.2/s at V=12000 (2-parallel), ~1.1/s at V=24000.
Grow-to-volume is fast (~4-12 s, first chunk only; use a small first `--budget-s` at V=24000
so the grown state checkpoints). Measurement+save overhead ~2-4 s even at V=24000. A V=24000
seed to ~650 sweeps (f22 0.36-0.37 equilibrium + 3 post-tune snapshots) took ~16-18 chunks.
The bash/exec sandbox does NOT keep background processes alive between calls, and each call is
capped ~45 s wall, so chunks must run foreground; checkpoint every chunk.

## 7. File inventory (repo, branch causal-cdt-scaling)

- cdt_causal_run.py: the 2+1D causal CDT implementation + selftest + chunked runner.
- euclid_control.py: chunked Euclidean control (negative control).
- torus_benchmark.py: exact periodic Kuhn T^3 benchmark (--ms m --long).
- track38.py, summarize_scaling.py: d_H-vs-sweeps tracker and aggregation.
- cdt_causal_results.jsonl: all measurements, four campaigns (204 records). kinds: causal
  chunk (default), torus_benchmark, euclid_control, long_measure.
- REPORT_CDT_CAUSAL / _SCALING / _STALL_RESOLVED / _CONVERGENCE .md: the four campaign
  reports in order; CONVERGENCE is the closer with the joint-gate verdict.
- tooling/: referee estimators (link_census, lazy_rw_sdim, ball_growth_dim, to_graph).
