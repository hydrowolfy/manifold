# HANDOFF: causal CDT scaling program (cold-start brief)

Updated 2026-07-09, SEVENTH campaign + volume-profile side-quest + STAGE 1 (topology; REPORT_CDT_TOPOLOGY.md)
+ STAGE 2 (exotic / non-local action; REPORT_CDT_ACTION.md)
+ STAGE 3 (dimensional / 3+1D; REPORT_CDT_4D.md + PART C production machinery REPORT_CDT_4D_PRODUCTION.md).
Work lives in git: branch `causal-cdt-scaling` of https://github.com/hydrowolfy/manifold (cut from `explore/3d-manifold`).
Read `LESSONS_CDT.md` (traps) and the REPORT_CDT_*.md in order.

## 0. Bottom line so far

Genuine 2+1D causal CDT is built and validated. The frontier question -- can d_H AND d_s hit the
exact benchmark JOINTLY -- is a proven NO in 2+1D (a volume-stable, topology-independent,
six-lever-family structural wall rooted in the per-slice Euler lock dN22 = -4 dN0), and the escape
is DIMENSIONAL. STAGE 3 (REPORT_CDT_4D.md) broke the wall STRUCTURALLY: 3+1D has NO analogue of
dN22=-4dN0 (a closed 3-manifold slice has f-vector DOF 2, not 1: its tetrahedron count is free of
its vertex count), so spatial-vertex density N0 and the timelike fraction N32/N4 are TWO INDEPENDENT
DOF -- matching the standard 4D CDT action's two couplings (kappa0<->N0, Delta<->the (4,1)/(3,2)
split) and its extended de Sitter phase. The flat foliated Kuhn T^4 is a validated census-clean
joint-4 calibrant (d_s~4.1-4.5). STAGE 3 PART C (this session, REPORT_CDT_4D_PRODUCTION.md) BUILT +
VALIDATED the full production apparatus; the dynamical de Sitter verdict is PENDING an uncapped run
(see section 9). Earlier stages' detail is in REPORT_CDT_FRONTIER/K0/HUB/TOPOLOGY/ACTION.md.

## 1. Environment (fresh session, Linux sandbox)

    git clone https://github.com/hydrowolfy/manifold.git /tmp/m   # or into sandbox home
    cd /tmp/m && git checkout causal-cdt-scaling
    pip install networkx --break-system-packages     # ONLY dep for the 2+1D runner (cdt4_* are stdlib-only)
    export MANIFOLD_REPO=$(pwd)
    PYTHONPATH=.:tooling python3 cdt_causal_run.py --selftest     # 2+1D core (must print ALL ... PASSED)
    PYTHONPATH=.:tooling python3 cdt4_prod_selftest.py            # 3+1D full move set (ALL PASSED)
    PYTHONPATH=.:tooling python3 cdt4_scan.py --db-check          # 3+1D Metropolis DB (worst 0.00e+00)

NOTE: git does NOT work on a mounted outputs dir (unlink EPERM) -- clone into sandbox-local home
and commit via the GitHub connector. Keep *.pkl / tarball / floats jsonl out of git.

## 2. Checkpoints & data are NOT in the repo (deliberate)

Chain-state pickles (scratch/*.pkl) and measurement jsonls are gitignored (binary/large). They
regenerate deterministically per seed. Every measurement is reproducible from the seeds.

## 3. 2+1D runner + tools (key flags)

    PYTHONPATH=.:tooling python3 cdt_causal_run.py --chunk \\
      --k0 2.0 --T 19 --V 24000 --seed 0 --k22 0.0 --tune 600 --sweeps 100000 \\
      --budget-s 34 --scratch <dir>/scratch --log <dir>/rec.jsonl
- `--grind` fast thermalization (skips estimators); `--k22 X` the CDT asymmetry; `--measure-long`
  measures current pickle; `remeasure.py` seed-averaged re-measure; `torus_benchmark.py` exact Kuhn T^3.
- Budgets: V=24000 pair <= 34 s, V<=12000 <= 38 s. ONE pair per bash call (45 s wall cap).

## 3b. 3+1D runner (STAGE 3 PART C -- cdt4_prod.py + cdt4_scan.py, stdlib-only)

    python3 cdt4_scan.py --db-check                     # Metropolis detailed balance (0.00e+00)
    python3 cdt4_scan.py --scan --T 5 --N4t 15000 --eps 0.01 \\
        --grid-k0 1.5,2.2,3.0,4.0 --grid-D 0.0,0.4,0.6 --meas-seeds 8 --scratch scratch
  --grow/--thermalize/--scan/--measure; checkpoint+resume per (k0,D); results.jsonl + progress.txt.
  Needs N0 >~ 1300 (T>=6) for un-saturated d_s/d_H (LESSONS 43); thermalize N0 to a plateau (LESSONS 44).

## 4. Throughput (2+1D, measured)

~8 sweeps/s @ V6000, ~2.3-3/s @ V12000, ~1.1/s @ V24000 (pair). 3+1D: ~4-5k mstep/s in-sandbox at
N4~6k (native WSL faster); N0 equilibration is the slow mode (LESSONS 44), budget long runs.

## 5. What remains (ranked)

1. THE 3+1D DE SITTER PRODUCTION RUN (primary; section 9). Machinery built + validated; run it on
   the uncapped WSL box to gate quality (N0>1300, thermalize each (k0,D) to a plateau) and score vs
   the frozen gate G1-G5 (PREREG_CDT_4D_PRODUCTION.md). Expected: phase C ~ (2.2,0.6) passes.
2. 2+1D in-ensemble leftover: genuinely thin large-T V>>24000 to put a MEASURED d_H at the
   d_s=benchmark slice size (campaign-5 extrapolation says the miss shrinks slowly; likely futile).
3. [DONE] volume-profile side-quest (section 7); STAGE 1 topology (section 8); STAGE 2 non-local;
   STAGE 3 Part A/B structural (REPORT_CDT_4D.md).

## 6. File inventory (branch causal-cdt-scaling) -- 3+1D additions

- cdt_4d_lock_check.py : STAGE 3 PART A gate (no 3+1D analogue of dN22=-4dN0; 4D Dehn-Sommerville).
- cdt4_benchmark.py : exact flat T^4 benchmark (validity + estimator calibration d_s~4.1-4.5).
- cdt4_causal.py : foliated Kuhn T^4 causal calibrant + two-DOF demonstration.
- cdt4_run.py : minimal 3+1D causal core + (2,4)/(4,2) pair (FOUNDATION; 200 round-trips + 4000 chain).
- cdt4_prod.py : STAGE 3 PART C self-contained core = cdt4_run Causal4 + FULL ergodic move set
  ((3,3),(4,6)/(6,4),(2,8)/(8,2)) + Kuhn seed + bundled estimators (indexed-sets + incidence maps).
- cdt4_prod_selftest.py : every move DB round-trip + census + counters==recount + mixed chain (ALL PASS).
- cdt4_ergodicity.py : N4 & N0 bidirectional, f_tl tunable 0.26-0.55, census-clean (PASS).
- cdt4_scan.py : Metropolis + (k0,Delta) scan driver + --db-check (0.00e+00) + checkpoint/resume.
- PREREG_CDT_4D.md / REPORT_CDT_4D.md : stage-3 structural prereg + verdict (path open; calibrant valid).
- PREREG_CDT_4D_PRODUCTION.md / REPORT_CDT_4D_PRODUCTION.md : PART C prereg (gate G1-G5) + verdict
  (machinery complete + validated; dynamical de Sitter pending the uncapped run).
- (2+1D files: cdt_causal_run.py, cdt_frontier2/3_run.py, cdt_torus_run.py, remeasure.py, tooling/ ...)

## 7. Volume-profile side-quest resolved (2026-07-09)

The two 2+1D near-misses differ in KIND: the alpha/k22 state where d_s hits benchmark (k0=6 V6000 T12,
CV 0.68->0.99 rising, blob-with-stalk) is a COLLAPSE; the hub sigma=0.10 state where d_H passes (CV 0.24,
extended across 11/12 slices) is a GENUINE EXTENDED phase. Read alpha/d_s gains as condensation.

## 8. STAGE 1 (topology frontier) resolved (2026-07-09)

Making each spatial slice a 2-TORUS: the identity generalizes to N22=N3-4N0+4chiT but the DIFFERENTIAL
dN22=-4dN0 is topology-independent (dchi=0), so the wall reappears at every genus and the ensemble hubs
anyway. Topology is CLOSED; the escape is DIMENSIONAL -> STAGE 3.

## 9. STAGE 3 PART C (production machinery) resolved 2026-07-09 -- MACHINERY COMPLETE, de Sitter run PENDING

The production de Sitter apparatus (PREREG_CDT_4D E1) is BUILT and VALIDATED; the dynamical
verdict awaits an uncapped run (staged, blocked this session by desktop contention). Built:
- The FULL ergodic AJL move set on cdt4_run.py: (2,4)/(4,2) + (3,3) + (4,6)/(6,4) + the vertex-
  changing (2,8)/(8,2) [the N0 DOF; 4D lift of 2+1D (2,6)]. Each DB-verified (byte-identical round-
  trip, reverse dS=-forward) + census bad=0 (cdt4_prod_selftest.py). Ergodicity shown (N4 & N0
  bidirectional 6144<->14588; 256<->1432; f_tl 0.26-0.55). Metropolis DB (with the vertex Jacobian)
  verified to 0.00e+00 over 828 pairs (cdt4_scan.py --db-check). Bundled estimators reproduce the
  frozen flat-T^4 benchmark bit-for-bit (d_H=2.6556, d_s=4.2001 vs networkx referee; 8-seed 4.01+-0.69).
- NO de Sitter claim: gate-quality needs N0>~1300 (else estimators saturate, LESSONS 43) + long N0
  thermalization at fixed N4 (LESSONS 44). In-session sandbox runs are finite-size-saturated +
  under-thermalized -> PREREG_CDT_4D_PRODUCTION Sec 5 rule 2 (partial/honest landing).

STAGED for the uncapped run: C:\Users\Kirk\Downloads\cdt4run\ (WSL /mnt/c/Users/Kirk/Downloads/
cdt4run) = cdt4_prod.py + cdt4_scan.py + cdt4_prod_selftest.py + run_cdt4_scan.bat (double-click ->
minimized WSL job, resumable/extendable) + kill_cdt4.bat + README_RESUME.txt. Bundle re-verified
STANDALONE there (DB check PASS, selftest PASS). NEXT SESSION: get desktop access (clear any other
Claude session), double-click run_cdt4_scan.bat, watch scratch/results.jsonl + progress.txt; run at
N4t large enough that eq. N0>1300 (T>=6) and thermalize each point to an N0/f_tl/CV plateau; score
vs the gate. Expected (Part A + AJL): phase C ~ (2.2,0.6) passes = WALL BROKEN DYNAMICALLY.
