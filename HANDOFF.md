# HANDOFF: causal CDT scaling program (cold-start brief)

Updated 2026-07-09, end of the FIFTH campaign (the "frontier" campaign). Work lives in git:
branch `causal-cdt-scaling` of https://github.com/hydrowolfy/manifold (cut from `explore/3d-manifold`).
Read `LESSONS_CDT.md` (traps) and the REPORT_CDT_*.md in order; `REPORT_CDT_FRONTIER.md` is the
current closer, `PREREG_CDT_JOINT.md` the preregistration it answers.

## 0. Bottom line so far

Genuine 2+1D causal CDT is built and validated (typed (3,1)/(2,2)/(1,3) tets on S^2 x S^1,
five foliation-preserving Pachner moves, census bad=0 everywhere). It breaks Euclidean crumpling
(d_H(2-6) converges; Euclid d_s never flows). The frontier question -- can d_H AND d_s hit the
exact-T^3 benchmark JOINTLY at large V -- is answered:

**No, not cleanly. The d_H-d_s tradeoff is a genuine, VOLUME-STABLE structural obstruction,
controlled by slice size s = N3/T. Both dims are V-independent monotonic functions of s;
d_s(8-24)=benchmark at s~=385, d_H(2-6)=benchmark at s~=1940 (~5x apart) -- no aspect at any V
lands both. The alpha (k22) lever moves both toward benchmark but only by driving spatial-volume
condensation (transient crossing, not a stable 3-manifold). On the long window (16-48) the
fattest V=24000 aspect is within ~0.17 of benchmark on both -- a weak long-window near-agreement
suggesting the short-window excess is partly a lattice artifact.** Full detail + gate table +
caveats in REPORT_CDT_FRONTIER.md.

Top untested lever: k0 (the CDT phase). All five campaigns fixed k0=2; alpha's condensation was
mapped only there. A k0 x k22 scan could in principle suppress the condensation.

## 1. Environment (fresh session, Linux sandbox)

    git clone https://github.com/hydrowolfy/manifold.git /tmp/m   # or into sandbox home
    cd /tmp/m && git checkout causal-cdt-scaling
    pip install networkx --break-system-packages     # ONLY dependency (no numpy)
    export MANIFOLD_REPO=$(pwd)
    PYTHONPATH=.:tooling python3 cdt_causal_run.py --selftest     # must print ALL ... PASSED

NOTE: git does NOT work on a mounted outputs dir (unlink EPERM) -- clone into sandbox-local home
and commit via the GitHub connector. Keep *.pkl / tarball / floats jsonl out of git.

## 2. Checkpoints & data are NOT in the repo (deliberate)

Chain-state pickles (scratch/*.pkl) and the measurement jsonls are gitignored (binary/large,
connector can't attach). They regenerate deterministically per seed. If a prior session's
/tmp/work exists, its scratch/*.pkl are usually world-readable -- COPY them into your scratch to
resume campaign-4/5 states without regrowing (the runner is byte-identical on the branch, so they
unpickle). Every measurement is reproducible from the seeds.

## 3. Runner + tools (key flags)

    PYTHONPATH=.:tooling python3 cdt_causal_run.py --chunk \
      --k0 2.0 --T 19 --V 24000 --seed 0 --k22 0.0 --tune 600 --sweeps 100000 \
      --budget-s 34 --scratch <dir>/scratch --log <dir>/rec.jsonl
- `--grind` : fast thermalization -- runs sweeps, keeps census + checkpoint, SKIPS the d_s/d_H
  estimators (~5-6 s/chunk saved). Use for the V=24000 f22 climb; switch to normal chunks near
  equilibrium (f22 ~0.38). NEW this campaign (see grind.patch).
- `--k22 X` : the CDT asymmetry (coeff on N22). k22>0 penalizes (2,2) tets -> lowers f22, raises
  N0/d_H, lowers d_s, and (crucially) drives profile condensation. Separate scratch dir per k22
  (the checkpoint tag is (k0,T,V,seed) and omits k22 -- collisions otherwise).
- `--measure-long` : measure current pickle (no advance), windows d_s 4-12/8-24/16-48/30-90,
  d_H 2-6/3-8/4-10, tmax=100.
- `remeasure.py` (NEW): re-measure any pickle OR exact torus with K estimator seeds -> error bars,
  profile CV, mean degree. `--pkl <p> --seeds 8 --tmax 50 --dswin 8-24,16-48 --seedbase 100`
  (use a different --seedbase for independent verification). `--torus m` for the benchmark.
- `torus_benchmark.py` : exact Kuhn T^3; size-match by N0 (V6000<->m10, V12000<->m13, V24000<->m16).
- Budgets: V=24000 pair <= 34 s (2x5.6MB saves + measure overran 45s at 40s); V<=12000 <= 38 s.
  ONE pair per bash call (looping budgeted chunks blows the 45 s cap).

## 4. Throughput (measured)

~8 sweeps/s @ V6000, ~2.3-3/s @ V12000, ~1.1/s @ V24000 (pair). V=24000 fresh thermalization is
~18-20 chunk-pairs (grow leaves f22~0.03, must climb to ~0.38). alpha warm-start re-equilibration
~1000-2000 sweeps. Benchmark m<=16 remeasure with 8 seeds is a few seconds.

## 5. What remains (ranked)

1. k0 x k22 phase scan: does a different CDT phase suppress alpha's condensation and permit a
   STABLE joint pass? Untested; the highest-value lever.
2. Genuinely thin large-T V=24000 (T~60, s~385) to put a MEASURED d_H at the d_s=benchmark slice
   size at the top volume -- nails the volume-stability of the 0.64 d_H ratio directly.
3. Measure the de Sitter volume profile of the alpha-condensed states -- physical extended phase
   or a collapse? (Decides how to read the alpha "improvement".)
4. Euclid control at matched large size (negative-control arm above n0<=500).

## 6. File inventory (branch causal-cdt-scaling)

- cdt_causal_run.py : the 2+1D causal CDT implementation + selftest + chunked runner (+ `--grind`).
- remeasure.py : seed-averaged re-measurement of pickles/tori with error bars + profile CV + degree.
- euclid_control.py : Euclidean negative control. torus_benchmark.py : exact Kuhn T^3.
- PREREG_CDT_JOINT.md : campaign-5 preregistration (gate, benchmark, H1/H2/H3, decision rules).
- REPORT_CDT_FRONTIER.md : campaign-5 verdict (slice-size obstruction; alpha condensation; long-window).
- REPORT_CDT_CAUSAL / _SCALING / _STALL_RESOLVED / _CONVERGENCE .md : campaigns 1-4 in order.
- LESSONS_CDT.md : accumulated traps (READ FIRST). tooling/ : referee estimators (verbatim).
