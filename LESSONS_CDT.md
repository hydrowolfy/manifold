# LESSONS: causal-CDT scaling program (accumulated, read before touching physics)

Consolidated across five campaigns. These are the traps that cost time; roll them forward.

## Physics / measurement
1. SCORE AGAINST THE EXACT FINITE-SIZE T^3 BENCHMARK, never against the continuum 3.0. The
   Kuhn torus at size-matched N0 is the target; d_H/d_s have big finite-size offsets from 3.
2. THE ESTIMATORS ARE STOCHASTIC. `lazy_rw_sdim` (Hutchinson probe) and `ball_growth_dim`
   (random sources) depend on their `seed`. Average >=8 estimator seeds and quote the sd, for
   BOTH causal states AND the benchmark. Campaign 4 scored single-seed and the benchmark
   d_s(8-24) came out 3.42 (a high fluctuation); seed-averaged it is 3.07-3.15. Single-seed
   scoring silently biased every "vs benchmark" number. (On the torus, d_H is deterministic --
   vertex-transitive -- so only d_s needs the averaging, but do both for uniformity.)
3. THE CONTROLLING GEOMETRIC VARIABLE IS SLICE SIZE s = N3/T (spatial tets per time slice),
   NOT T alone and NOT V. d_s(8-24) and d_H(2-6) both collapse onto V-independent curves in s
   (verified across 4x in N0). Always convert (V,T) -> s before comparing aspects across volumes.
   The "balanced aspect" T ~ V^(1/3) makes s grow as V^(2/3), so its d_s excess grows with V.
4. d_H BALL-GROWTH WINDOWS NEED ENOUGH TIME SLICES. With T < ~8 the wider windows (3-8, 4-10)
   saturate (the time circle is shorter than the ball radius) and d_H(2-6) reads spuriously low.
   Exclude T<8 from slice-size fits (they are time-saturated, not on the collapse curve).
5. d_s WINDOW MATTERS. 8-24 is the trusted long window at N0>=~950. 16-48 is trustworthy only
   at N0 >~ 2000 and is noisy (sd 0.2-0.4) even then; 30-90 is size-contaminated below N0~3800.
   The short-window (8-24) d_s excess partly DISSOLVES at 16-48 -- it is partly a lattice
   artifact -- so report both windows and be explicit which one a claim rests on.
6. THE alpha (k22) LEVER CAUSES CONDENSATION. k22>0 (penalize (2,2) tets) improves both d_H and
   d_s toward benchmark but drives spatial-volume condensation: profile CV rises, one slice
   blows up, f22 -> low, and the observables slide THROUGH the joint point. Any "joint pass"
   under k22 must be checked for equilibrium (profile CV plateau, f22 plateau, stable across
   >=200 sweeps) before it counts -- transient crossings are not convergence. Track profile CV.
7. WARM-STARTING a k22=0 equilibrated state to k22!=0 has a long transient (f22 relaxes over
   ~1000-2000 sweeps at V=6000-12000). Monitor f22 AND profile CV to a plateau; do not measure
   mid-relaxation. Fresh growth also starts at f22~0.03 (grow uses k3=-0.5) and must climb.

## Engineering / sandbox
8. ONE parallel pair per bash call, budget <= ~34 s at V=24000 (2 saves of ~5.6 MB + measure
   overran a 45 s cap at 40 s), <=38 s at V<=12000. NEVER loop multiple budgeted chunks in one
   call -- it blows the 45 s wall cap and orphans a process (checkpoints from completed chunks
   survive; the interrupted one is lost but the pickle is intact).
9. USE `--grind` for V=24000 thermalization: it skips the d_s/d_H estimators (the ~5-6 s/chunk
   cost) and keeps census+checkpoint, ~1.5x more sweeps/chunk. Switch to normal chunks + an
   8-seed `remeasure.py` pass only once f22 is near its ~0.38 equilibrium.
10. V=24000 thermalization is inherently ~18-20 chunk-pairs: fresh growth leaves f22~0.03 and it
    must climb to ~0.38, rate-limited by (2,3)-move acceptance. Budget for it. Checkpoint every
    chunk; the tag is (k0,T,V,seed) -- ADD k22 (or a separate scratch dir) when scanning k22, or
    different-k22 runs collide on the same pickle.
11. CHECKPOINT PICKLES ARE WORLD-READABLE ACROSS SESSIONS but the results jsonl was mode 600.
    If a prior /tmp/work exists, COPY its scratch/*.pkl into your own scratch immediately (robust
    against it vanishing) -- they resume exactly if `cdt_causal_run.py` is byte-identical (it is
    on the branch). This saved regenerating every campaign-4 state this campaign.
12. GIT DOES NOT WORK on the mounted outputs dir (unlink/lock EPERM). Clone into the sandbox-
    local home (/sessions/.../work_manifold) and commit via the GitHub connector. Keep pickles
    (*.pkl), the tarball, and the floats jsonl OUT of git (.gitignore); commit code/text only.
    Never hand-relay the dense-float jsonl through the connector (not byte-exact).

## Discipline
13. PREREGISTER the gate, windows, benchmark, and hypotheses BEFORE the new experiment; commit
    it first (PREREG_CDT_JOINT.md was committed before the alpha scan). It stops post-hoc window/
    seed shopping -- which matters a lot here because the verdict depends on window and seed choice.
14. A "joint pass" needs: census bad=0, equilibrium (not a transient), seed-averaged error bars,
    AND a stable profile. Report profile CV alongside d_H/d_s -- a d_H gain that rides rising CV
    is condensation, not 3-manifold convergence.

## Campaign 6 additions (k0 x k22)
15. f22 IS THE ORDER PARAMETER of the d_H-d_s tradeoff. The (2,2) tets are the timelike tissue
    stitching adjacent spatial slices. High f22 -> uniform profile but d_s too high; low f22 ->
    d_s onto benchmark but slices decouple and the volume CONDENSES (and d_H drops). BOTH k0(up)
    and k22(up) push f22 down, so they are the SAME lever, not independent phases. Equilibrium f22
    at V6k T12: k0=2->0.40, k0=3->0.31, k0=4->0.21, k0=6->0.03. No k0 escapes the tradeoff.
16. HIGHER k0 DOES NOT SUPPRESS CONDENSATION -- it worsens it (CV rises with k0: 0.16/0.37/0.33/
    0.76/1.21 for k0=2/3/4/6/6+a1.5). Score condensation by CV DRIFT + collapsing MIN slice (110
    ->16->12), not an absolute CV threshold (the uniform k0=2 baseline already sits at CV 0.16-0.31).
17. LOCAL UNCAPPED RUNS (Kirk's WSL box, via a mounted Downloads folder): stage a SINGLE
    dependency-free .py (bundle physics+estimators verbatim via ast.get_source_segment; the
    estimators need NO networkx if you pass adjacency dicts directly) + a .bat that does
    `start "title" wsl.exe -e bash -lc "cd /mnt/c/... && mkdir -p out && python3 runner.py ... > out/run.log 2>&1"`;
    double-click the .bat in File Explorer (full tier; terminals are click-only so you cannot type).
    Watch out/results.jsonl + out/progress.txt through the mount. VERIFY the bundled runner
    reproduces the frozen benchmark + a known pickle in-sandbox BEFORE launching (it did: torus
    m=13 d_s 3.0706 == 3.071). Gotchas: (a) do NOT run two big scans at once on a loaded gaming
    box -- they starve each other (~1 sweep/s each); one uncontended scan is far better. (b) a
    `bash -lc "pkill -f runner.py; ..."` SELF-MATCHES (its own cmdline contains the pattern) and
    kills its own launcher -- kill instead with `bash kill.sh` where kill.sh greps a pattern NOT
    in the bash cmdline (e.g. a unique arg like 'equil 2000'). (c) mkdir the outdir BEFORE the
    `> out/run.log` redirect or the shell redirect fails and python never starts.

## Campaign 7 additions (the locked identity + hub measure term)
18. THE LOCKED IDENTITY (the big one). Per-slice Euler on the S^2 slices (F = 2V - 4) forces, for the
    WHOLE foliated complex: N31 = N13 = 2 N0 - 4 T and **N22 = N3 - 4 N0 + 8 T**, i.e.
    f22 = 1 - 4 (N0 - 2 T) / N3. Verified EXACT to the integer on seed/grown/thermalized states (k0=2,5)
    and it reproduces the campaign-6 k0-map f22 from (N0,N3,T). Consequence: at fixed volume and T,
    dN22 = -4 dN0. Spatial-vertex density and the (2,2) fraction are ONE locked DOF. So "add spatial
    vertices WITHOUT removing (2,2) tets" is COMBINATORIALLY IMPOSSIBLE -- no move (standard or exotic)
    escapes it, because every foliation-preserving local move preserves the identity. Check any proposed
    escape against this identity FIRST; it kills the whole "new move" branch by proof.
19. THE ONLY FREEDOM LEFT AT FIXED COUNTS IS THE DEGREE DISTRIBUTION. The identity pins simplex counts
    and the mean degree (sum_v deg = 2 N1 = 2(N0+N3)); the variance is free. Causal states have hubs
    (deg max ~84, sd ~10) absent in the regular torus (14, sd 0). The hub-suppression measure term
    S += sigma * sum_v max(0, deg_v - D0)^2 is the sole non-excluded lever. It is DB-safe (state
    function; proposals unchanged; per-move delta == brute-force; reverse delta = -forward) and manifold-
    preserving (census bad=0). But it REPARAMETERIZES THE SAME TRADEOFF: d_s(8-24) falls and d_H(2-6)
    rises monotonically with sigma, crossing the benchmark ~10x apart in sigma (d_s at ~0.007, d_H at
    ~0.08). No sigma passes G2+G3. Powerful lever, same wall. (Implementation: cdt_frontier2_run.py.)
20. HUBS SET BOTH DIMS OPPOSITELY: they saturate ball growth (d_H low) AND add walk shortcuts (d_s high);
    removing them de-saturates d_H up and confines the walk so d_s falls THROUGH the benchmark. This is
    the campaign-5/6 d_H-d_s anticorrelation reproduced by a third independent knob -- it is a property of
    the ensemble's diffusion geometry, not of any one coupling.
21. RESUME-COMPAT: cdt_frontier2_run.py rebuilds the deg cache from st.ecnt on load, so pre-campaign-7
    pickles resume cleanly. Pickles from a `python3 script.py` run store class as __main__.Causal and
    unpickle as whatever __main__ currently is (frontier2 instance gains the new methods; state migrates).
22. ENGINEERING (re-learned, cost one call): do NOT loop two budgeted --chunk runs in one bash call --
    the 45 s wall cap kills the second and times out the whole call (lesson 8). One chunk per call.

## Volume-profile side-quest (physical-extended vs collapse)
23. THE TWO NEAR-MISSES DIFFER IN KIND (measured N3(t) profiles; PREREG_CDT_PROFILE.md -> REPORT_CDT_PROFILE.md).
    At the alpha/k22-condensed point where d_s hits benchmark (k0=6, V6000 T12) the spatial-volume profile is a
    COLLAPSE: blob-with-stalk, CV 0.68->0.99 and RISING, max/mean 3.4, 3 depleted floor slices (K1+K2+K3) -- even
    though census bad=0 and d_s(8-24)=3.14 is dead on benchmark. At the hub-sigma point where d_H passes
    (sigma=0.10, ratio 0.935) the profile is EXTENDED: CV 0.24, no stalk, volume across 11/12 slices, stable.
    So a d_s "improvement" via low f22 is CONDENSATION, not a real extended 3-manifold; only the hub/d_H near-miss
    is a genuine extended geometry (it merely lands the wrong dimension). Read alpha/d_s gains as collapse.

## STAGE 1 additions (surgical -- torus spatial slices, T^2 x S^1; cdt_torus_run.py)
24. TOPOLOGY DOES NOT UNLOCK THE IDENTITY -- ONLY ITS CONSTANT. Generalized Euler for a genus-g slice:
    chi=2-2g, F=2V-2chi, so N31=N13=2N0-2chiT and **N22=N3-4N0+4chiT** (sphere +8T, torus +0). BUT chi is a
    topological invariant, dchi=0 under every foliation-preserving move, so **dN22=-4dN0 at fixed (N3,T) holds
    for EVERY genus**: the differential lock -- the ROOT of the wall -- is topology-INDEPENDENT. Changing slice
    topology moves only the constant term. So "add spatial vertices without removing (2,2) tets" stays impossible
    on any closed-surface slice, and N0/f22 are never two independent knobs. Corollary: move weights (2-3:+1,
    3-2:-1, 2-6/6-2/4-4:0) are UNCHANGED, so cdt_torus_run.py reuses the S^2 Metropolis core VERBATIM -- only the
    seed (flat torus grid) and the per-slice census (chi=0 + orientability) differ. Verified exact in --selftest.
25. THE TORUS HUBS TOO (the empirical half). Even though the torus ADMITS a uniform degree-6 flat slice (6chi=0;
    the sphere FORBIDS it, 6chi=12) and that flat state IS the benchmark, the causal ensemble at the matched
    baseline (V6000 T12 k0=2 k22=0) equilibrates to hubs deg 15.4/sd 11.0/max 79 -- essentially identical to the
    S^2 baseline 14.6/10.2/84 -- with d_H(2-6)=1.68 (ratio 0.68) and d_s(8-24)=3.48: the sphere's exact FAILING
    corner. Hub formation is ENTROPIC (many hubbed triangulations, one flat one), not curvature-forced, hence
    topology-independent. The k22 lever reproduces the anticorrelation + condensation (k22=1: d_s 3.48->3.27 onto
    benchmark, d_H 1.68->1.93, CV 0.10->0.22). No joint pass. VERDICT: the 2+1D wall is a property of DIMENSION +
    diffusion geometry, not of the spatial slice topology.
26. FLAT CALIBRANT recipe (an in-topology exact benchmark): T identical flat m x n torus grids (uniform deg 6)
    stacked by the SAME ordered-prism split (lower-vertex->higher-vertex diagonal) the octahedral seed uses --
    that split is globally consistent for ANY ordered surface triangulation, sphere or torus. Gives an exact flat
    T^2xS^1 (== flat T^3): f22=1/3 EXACTLY, deg 14 sd 0, census bad=0, and it reproduces Kuhn T^3 d_s/d_H at
    matched N0 (a second, independent benchmark: d_s 3.10+-0.21, d_H 2.43 vs Kuhn 3.13+-0.18 / 2.47). Always check
    slice ORIENTABILITY in selftest (chi=0 alone is torus OR Klein bottle; Pachner moves can't flip it, but verify).
27. STAGE ORDERING, revised by the stage-1 result. TOPOLOGY IS CLOSED: higher genus won't help (lesson 24), so
    stop varying spatial topology. Remaining escapes are DIMENSIONAL (3+1D CDT, the de Sitter phase reaches 4 in
    both dims) or NON-LOCAL (a long-range action on the diffusion geometry, not a local per-vertex term). The
    stage-1 result RE-RANKS 3+1D above the non-local probe: the wall survives every in-2+1D lever incl. topology,
    which is the evidence to change the DIMENSION rather than keep reshuffling 2+1D.
