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

## Campaign 7 additions (hub / measure term; the frontier closer)
18. THE "ADD VERTICES WITHOUT REMOVING (2,2) TETS" MOVE IS IMPOSSIBLE, by Euler not by dynamics.
    Spatial slices are 2-spheres => F=2V-4 per slice => N31=N13=2N0-4T and N22=N3-4N0+8T exactly
    (verify_identity.py: integer-exact on seed/grown/thermalized at k0=2,5; slope (dN22-dN3)/dN0
    =-4.0000). At fixed (N3,T), dN22=-4 dN0. No enlarged/exotic move set escapes an Euler identity.
    Before proposing ANY new move to decouple N0 from f22, check it against this identity first --
    it will fail. The simplex sector has exactly one connectivity d.o.f. left at fixed counts: the
    degree DISTRIBUTION (hubs), not the counts.
19. THE HUB MEASURE TERM (sigma*sum_v max(0,deg-D0)^2, non-Regge) LIFTS d_H TO BENCHMARK AT A
    UNIFORM PROFILE -- the one thing k0/k22 never did (they only raised d_H via condensation, which
    then dropped it). deg sd 10.4->3.6, deg max 80->21 toward the regular torus; d_H(2-6) 1.84->2.43
    (ratio 0.74->0.98) at CV 0.16-0.28, bad=0. BUT it overshoots d_s: d_s(8-24) falls 3.24->2.28
    THROUGH benchmark (16-48 falls too, so real not short-window). Pass regions DISJOINT: G2 needs
    sigma>=0.05, G3 needs sigma<=0.02; crossover (0.03-0.04) misses BOTH. Hub density is a NEW order
    parameter for the SAME tradeoff, reparameterized off f22 -- not a second independent knob.
    D0 only rescales the effective sigma onto the same (d_s,d_H) locus (D0=18 sig0.10 ~ D0=14 sig0.05).
20. THE TRADEOFF NEEDS TWO KNOBS, ONE PER DIMENSION. Every lever tried (slice size, k0, k22, hub sigma)
    moves d_s and d_H TOGETHER along a one-parameter curve that crosses the two benchmarks at
    different places. hubs over-connect (d_s up) AND saturate ball growth (d_H down) simultaneously,
    so suppressing them can't separate the two. The identity (18) guarantees the simplex sector can't
    supply a second independent knob at fixed volume/topology. Next lever must hit d_s alone (e.g. a
    short-loop / spectral-gap term), or change the ensemble (higher-genus slices add (2,2)-room:
    N22=N3-4N0+8T-8*sum genus), or push V>>24000 on the thin-aspect route (orthogonal to sigma).
21. HUB-TERM DETAILED BALANCE IS FREE IF THE DELTA IS EXACT: the penalty is a state function, so
    dS_reverse = -dS_forward automatically. The only risk is a wrong incremental delta -- brute-force
    it (verify_hub_db.py: _degpen_delta == pen_after-pen_before to 0.0 over every accepted move, deg
    cache == from-scratch degree every step) BEFORE trusting the chain. Selftest asserts deg-cache
    non-drift (dict(st.deg)==rebuild); that is necessary but NOT sufficient -- also check the delta.
