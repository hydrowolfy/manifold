# HANDOFF: causal CDT scaling program (cold-start brief)

Updated 2026-07-09, SEVENTH campaign + volume-profile side-quest + STAGE 1 (topology; REPORT_CDT_TOPOLOGY.md)
+ STAGE 2 (exotic / non-local action; REPORT_CDT_ACTION.md)
+ STAGE 3 (dimensional / 3+1D; REPORT_CDT_4D.md -- the frontier sequence's CLOSER) of the frontier. Work lives in git:
branch `causal-cdt-scaling` of https://github.com/hydrowolfy/manifold (cut from `explore/3d-manifold`).
Read `LESSONS_CDT.md` (traps) and the REPORT_CDT_*.md in order; `REPORT_CDT_HUB.md` is the
current closer, `PREREG_CDT_HUB.md` the preregistration it answers.

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

Campaign 6 (REPORT_CDT_K0.md) tested the k0 axis: the WALL HOLDS ACROSS CDT PHASES. f22 (the
(2,2)-tet fraction) is the order parameter -- both k0(up) and k22(up) push f22 down, which fixes
d_s but decouples the slices and CONDENSES the volume (CV rises, d_H drops). No (k0,k22) gives
d_s=benchmark + uniform profile + d_H=benchmark together. Higher k0 makes condensation WORSE.
Campaign 7 (REPORT_CDT_HUB.md) CLOSES the first of those levers BY PROOF. The per-slice Euler identity
N22 = N3 - 4 N0 + 8 T (verified exact) locks spatial-vertex density to f22 -- at fixed N3,T, dN22 = -4 dN0
-- so a move that adds spatial vertices WITHOUT removing (2,2) tets is COMBINATORIALLY IMPOSSIBLE (no
foliation-preserving move escapes a topological identity). The only freedom left at fixed simplex counts is
the degree DISTRIBUTION (causal hubs deg<=84 vs the torus's uniform 14). A detailed-balance-safe, manifold-
preserving hub-suppression measure term S += sigma*sum_v max(0,deg-D0)^2 (cdt_frontier2_run.py) moves BOTH
dimensions but REPARAMETERIZES THE SAME TRADEOFF: d_s(8-24) falls and d_H(2-6) rises monotonically with
sigma, crossing the benchmark ~10x apart in sigma -- no joint pass at any sigma. The wall now survives
aspect ratio (c5), the whole k0 x k22 plane (c6), AND a degree-measure term (c7): three independent levers,
one wall. Remaining escapes all LEAVE the 2+1D S^2 x S^1 alpha=1 ensemble (different spatial topology which
breaks F=2V-4; 3+1D CDT; a non-local action term). Only in-ensemble item still open: V >> 24000 to lift d_H
at large slice size -- a slow, likely-futile extrapolation per c5.

**STAGE 1 (topology frontier; REPORT_CDT_TOPOLOGY.md) is DONE and the wall REAPPEARS -- the obstruction is
TOPOLOGY-INDEPENDENT.** Making each slice a 2-TORUS (chi=0, dissolving F=2V-4) generalizes the identity to
N22 = N3 - 4 N0 + 4 chi T (torus: N22 = N3 - 4 N0), but dchi=0 under every move, so the DIFFERENTIAL lock
dN22 = -4 dN0 survives at every genus -- only the constant offset moves. The causal T^2xS^1 ensemble at the
matched baseline (V6000 T12 k0=2) equilibrates to the sphere's exact failing corner (hubs deg_max 79 vs the
flat 14, d_H(2-6)=1.68 ratio 0.68, d_s(8-24)=3.48), and the k22 lever reproduces the same anticorrelation +
condensation. The flat joint 3-manifold EXISTS in the ensemble (an exact calibrant, == the benchmark) but has
negligible entropic weight. So the wall is a property of DIMENSION + diffusion geometry, not the slice sphere.

**STAGE 2 (exotic / non-local action; REPORT_CDT_ACTION.md) is DONE and the wall SURVIVES -- the last
in-2+1D escape is CLOSED.** Two non-local measure terms were built (DB + manifold verified by brute
force over all 5 moves): NL-P lam_p*sum_t(n(t)-nbar)^2 (non-separable profile-uniformity) and NL-D
lam_d*sum_v(deg_v-14)^2 (symmetric global degree counter-term, stronger than c7's one-sided cap). NL-P
is ORTHOGONAL to the wall (drives profile CV 0.25->0.01, even de-condenses k22, but leaves d_s/d_H
unchanged on the baseline): the wall is not in the profile. NL-D REPARAMETERIZES the same tradeoff --
d_H saturates at ratio ~0.85 (below the 0.90 gate) while d_s collapses -- matching the flat degree
delta is necessary but not sufficient. The strongest combined lever (k22 + NL-P + hub cap = a PERFECTLY
UNIFORM CV-0.01 hub-free census-clean 3-manifold) drives d_H ABOVE benchmark but d_s collapses to
~2.0-2.2; the needle (d_H>=0.90 AND d_s in band) is unthreadable. So reproducing the flat manifold's
profile AND degree is still not enough -- the residual walk-confining irregularity of the causal
1-skeleton is the wall. Six independent lever-families, one wall. The escape is DIMENSIONAL (3+1D).

**STAGE 3 (dimensional; 3+1D; REPORT_CDT_4D.md) is DONE and the WALL IS BROKEN -- the escape was dimensional.**
The cheap on-paper gate (do 3+1D counts have an analogue of dN22=-4dN0?) answers NO, decisively. Root: a closed
SURFACE slice has f-vector DOF=1 (2E=3F, V-E+F=chi => F=2V-2chi locks triangles to vertices), but a closed
3-MANIFOLD slice has f-vector DOF=2 (F=2S, E=V+S leave V AND S=#tets free) -- no 3D analogue of F=2V-2chi. So the
"more spatial" pentachoron count N41=2 sum_t S_t is NOT locked to N0=sum_t V_t: spatial-vertex density and the
timelike fraction N32/N4 are TWO INDEPENDENT DOF. Verified (cdt_4d_lock_check.py, all pass): 2+1D identity exact
on real seeds; the derived closed-4-mfld Dehn-Sommerville relations (N1=3N0+N4/2-3chi, N2=2N0+2N4-2chi, N3=5N4/2)
hold on dDelta^5 / cross-polytope / CP^2_9 / random stellar S^4's; a real 2-3 Pachner move changes S at fixed V on
S^3 (the move a surface lacks). Matches the standard 4D CDT action's TWO independent couplings (kappa_0<->N0,
Delta<->the (4,1)/(3,2) split) and the extended de Sitter phase. BUILD (Part B): the Kuhn T^4 is a validated exact
flat benchmark (census bad=0, chi=0, DS-exact, degree 30) AND, sliced along one axis, a valid FOLIATED causal state
-- so the flat JOINT 4-manifold is a genuine census-clean member of the causal ensemble reading d_s~4.1-4.5 (vs the
T^3 3.13), and cdt4_run.py --selftest validates a foliation-preserving (2,4)/(4,2) Metropolis move (200 exact
round-trips = DB, 4000-move chain census-clean = manifold preservation). HONEST landing: the DECISIVE result is
structural (two DOF) + the validated joint-4 calibrant; the full production de Sitter (kappa_0,Delta) sweep needs
the complete ergodic AJL move set + an uncapped run and is preregistered (PREREG_CDT_4D.md E1), NOT claimed here.

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
  equilibrium (f22 ~0.38). NEW this campaign.
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
~1000-2000 sweeps. Benchmark m<=16 remeasure with 8 seeds is a few seconds. Campaign 7 hub-term
warm-start re-equilibration at V6000 is fast (~400-600 sweeps to a stable f22/CV).

## 5. What remains (ranked)

1. Campaign 7 CLOSED the "new move" lever by proof (the locked identity) and the hub/measure-term
   lever by scan (reparameterizes the same tradeoff). The remaining in-ensemble item: genuinely thin
   large-T V>>24000 (s~385 at large volume) to put a MEASURED d_H at the d_s=benchmark slice size --
   the campaign-5 extrapolation says the miss only shrinks slowly (likely futile, but unmeasured).
2. Out-of-ensemble questions. Spatial slice topology is now CLOSED by STAGE 1 (REPORT_CDT_TOPOLOGY.md):
   the torus (chi=0) breaks F=2V-4 but the differential lock dN22=-4dN0 is topology-independent and the ensemble
   hubs anyway -> wall reappears; higher genus cannot help. The two remaining escapes, RE-RANKED by stage 1:
   (a) STAGE 3, 3+1D CDT (the de Sitter phase reaches 4 in both dims) -- now the SOLE remaining escape and the
   primary next step, because stages 1-2 show the escape must be DIMENSIONAL; (b) STAGE 2 (non-local action) is
   now CLOSED (REPORT_CDT_ACTION.md): NL-P profile + NL-D degree counter-terms fail; the wall survives a non-local
   re-weighting. STAGE-3 CHEAP FIRST GATE (do before any heavy build): write the 3+1D Dehn-Sommerville/Euler
   relations among N_{ij}(4,1/3,2/2,3/1,4),N0,N1 and check whether spatial-vertex density and the timelike fraction
   are TWO independent DOF (no 2+1D-style lock dN22=-4dN0). Two free DOF = the a-priori reason 3+1D can win.
   [RESOLVED 2026-07-09 -- STAGE 3, REPORT_CDT_4D.md: gate answers NO analogue -> PATH OPEN; wall's algebraic root
   is gone in 3+1D. Remaining: the production de Sitter (kappa_0,Delta) sweep with the full ergodic AJL move set on
   the uncapped WSL box (PREREG_CDT_4D.md E1) -- build (3,3)+vertex moves onto the validated cdt4_run.py core.]
3. Measure the de Sitter volume profile of the alpha-condensed / high-sigma states -- physical
   extended phase or a collapse? (Decides how to read the "improvement" in one dimension.)
   [DONE 2026-07-09 -- see 7 below: alpha/d_s = collapse, hub/d_H = extended.]
4. Euclid control at matched large size (negative-control arm above n0<=500).

## 6. File inventory (branch causal-cdt-scaling)

- cdt_causal_run.py : the 2+1D causal CDT implementation + selftest + chunked runner (+ `--grind`).
- remeasure.py : seed-averaged re-measurement of pickles/tori with error bars + profile CV + degree.
- profile_dump.py : read-only per-time-slice N3(t) volume-profile dumper + shape stats (side-quest 7).
- euclid_control.py : Euclidean negative control. torus_benchmark.py : exact Kuhn T^3.
- PREREG_CDT_JOINT.md / PREREG_CDT_K0.md : campaign-5 / campaign-6 preregistrations.
- cdt_k0_local.py : SELF-CONTAINED zero-dep (stdlib-only) runner for UNCAPPED local (WSL) runs --
  physics+estimators bundled verbatim, no networkx; --scan does a k0 x k22 grid, checkpointed/
  resumable, results.jsonl per snapshot. Verified in-sandbox to reproduce the frozen benchmark.
- REPORT_CDT_FRONTIER.md : campaign-5 verdict (slice-size obstruction; alpha condensation).
- REPORT_CDT_K0.md : campaign-6 verdict (wall holds across k0 phases; f22 order parameter).
- cdt_frontier2_run.py : campaign-7 runner = cdt_causal_run.py core VERBATIM + a hub-suppression measure
  term sigma*sum_v max(0,deg-D0)^2 (deg cache maintained incrementally; DB + manifold verified in selftest).
- PREREG_CDT_HUB.md / REPORT_CDT_HUB.md : campaign-7 prereg + verdict (locked identity impossibility proof;
  hub measure term reparameterizes the same d_H-d_s tradeoff -> wall holds outside the standard move set).
- PREREG_CDT_PROFILE.md / REPORT_CDT_PROFILE.md : volume-profile side-quest prereg + verdict (item #3).
- cdt_torus_run.py : STAGE 1 runner = cdt_causal_run.py core VERBATIM + flat-torus seed + chi=0/orientability
  census (T^2 x S^1). --selftest (identity + round-trips + orientable-torus census), --calibrant (exact flat
  T^3), --chunk/--measure-long (seed-averaged). PREREG_CDT_TOPOLOGY.md / REPORT_CDT_TOPOLOGY.md : stage-1
  prereg + verdict (wall is topology-independent; proceed to stage 3).
- cdt_frontier3_run.py : STAGE 2 runner = cdt_frontier2_run.py core VERBATIM + two NON-LOCAL terms: NL-P
  lam_p*sum_t(n(t)-nbar)^2 (profile-uniformity, sprof cache) and NL-D lam_d*sum_v(deg-D0d)^2 (symmetric degree
  counter-term). Per-move deltas verified vs brute force over all 5 moves + reverse-antisymmetric in --selftest.
  Flags --lam-p/--lam-d/--D0d (+ existing --sigma/--k22); checkpoint tag includes all term params (no collisions).
  PREREG_CDT_ACTION.md / REPORT_CDT_ACTION.md : stage-2 prereg + verdict (non-local terms fail; escape is 3+1D).
- cdt_4d_lock_check.py : STAGE 3 PART A -- the cheap gate, computationally backed. Verifies the 2+1D lock on real
  seeds, derives+verifies the closed-4-manifold Dehn-Sommerville relations (dDelta^5/cross-polytope/CP^2_9/random
  stellar S^4), and demonstrates the 3-manifold slice's 2nd DOF (a 2-3 move changes #tets at fixed vertices). Verdict:
  NO 3+1D analogue of dN22=-4dN0 -> two independent DOF -> path open.
- cdt4_benchmark.py : exact flat T^4 (Coxeter-Freudenthal-Kuhn) benchmark -- validity (census bad=0, chi=0, DS-exact,
  degree 30) + estimator calibration (d_s ~4.1-4.5 reads 4D vs T^3 3.13).
- cdt4_causal.py : foliates Kuhn T^4 along one axis -> validated FOLIATED CAUSAL calibrant (typed pentachora, spatial
  slices = Kuhn T^3, census-clean); verifies N41=2 sum_t S_t and the two-DOF freedom; measures the calibrant (joint-4).
- cdt4_run.py : minimal 3+1D causal core (Causal4: pentachora, foliation, census) + foliation-preserving (2,4)/(4,2)
  Pachner move pair. --selftest: 200 exact round-trips (DB) + 4000-move census-clean chain (manifold preservation).
  FOUNDATION for the production sweep (NOT yet the full ergodic AJL set: add (3,3)+vertex-changing moves).
- PREREG_CDT_4D.md / REPORT_CDT_4D.md : stage-3 prereg + verdict (path open; wall's algebraic root gone in 3+1D;
  joint-4 calibrant validated; production de Sitter sweep preregistered/pending).
- REPORT_CDT_CAUSAL / _SCALING / _STALL_RESOLVED / _CONVERGENCE .md : campaigns 1-4 in order.
- LESSONS_CDT.md : accumulated traps (READ FIRST). tooling/ : referee estimators (verbatim).

## 7. Volume-profile side-quest resolved (2026-07-09)

Open item #3 (§5) DONE. Measured the per-time-slice spatial-volume profile N3(t) at the near-misses
(preregistered in PREREG_CDT_PROFILE.md, committed first; verdict in REPORT_CDT_PROFILE.md). The two
near-misses differ in KIND: the alpha/k22 state where d_s hits benchmark (k0=6 V6000 T12; CV 0.68->0.99
rising, blob-with-stalk, K1+K2+K3) is a COLLAPSE; the hub sigma=0.10 state where d_H passes (CV 0.24,
no stalk, extended across 11/12 slices, stable) is a GENUINE PHYSICAL EXTENDED phase. So the d_s/alpha
"improvement" is a condensation artifact (not a real 3-manifold); the d_H/hub near-miss is the physically
meaningful one. Added profile_dump.py (read-only N3(t) + preregistered shape stats).

## 8. STAGE 1 (topology frontier) resolved (2026-07-09)

Surgical stage of the frontier sequence surgical -> exotic -> 3+1D. Broke the sphere assumption by making each
spatial slice a 2-TORUS (manifold T^2 x S^1, which is the flat-T^3 topology foliated along one circle).
Preregistered in PREREG_CDT_TOPOLOGY.md (committed first). Runner cdt_torus_run.py reuses the S^2 Metropolis
core verbatim (only the seed + census change; move weights are provably unchanged). VERDICT: **wall reappears,
H_wall supported.** Two results: (1) analytical/exact -- the locking identity generalizes to N22=N3-4N0+4chiT
and its DIFFERENTIAL dN22=-4dN0 is topology-independent (dchi=0), so the "new move" escape stays impossible and
N0/f22 remain one locked DOF for any genus; (2) empirical -- the causal ensemble still forms hubs (deg_max 79,
== the sphere's 84) and fails the joint gate identically (baseline d_H 1.68 / d_s 3.48), the k22 lever reproduces
the anticorrelation + condensation, and the exact flat calibrant (the joint 3-manifold, == benchmark) exists in
the ensemble but is entropically unselected. RECOMMENDATION: topology is closed; **proceed to STAGE 3 (3+1D)** as
primary (the escape is dimensional), keep STAGE 2 (non-local action) as a secondary in-2+1D probe. A larger-V /
full seed-averaged anticorrelation scan on the uncapped WSL box is the optional confirmation; the verdict (the
exact identity) does not depend on it.
