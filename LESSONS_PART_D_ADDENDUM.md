# LESSONS addendum -- STAGE 3 PART D (coarse (kappa0,Delta) phase scan)

(These are appended to LESSONS_CDT.md as items 47-53. Kept also as a standalone addendum so the
Part-D traps can be read without diffing the main file.)

47. THE 4D PHASE STRUCTURE DOES NOT RESOLVE AT N4 ~ 4e4. All 12 measured points of the
    kappa0{1,2.2,3.5,5} x Delta{0,.2,.4,.6} grid land in ONE class: a hub-dominated, extended,
    structureless uniform tube (f_hub 0.28-0.47, r_H 0.59-0.72, top_frac ~0.17 everywhere).
    No phase B (no single-slice collapse anywhere), no phase A (no decoupled/multimodal profile),
    no phase C (no cos^3 blob, no low-hub point). Do NOT expect A/B/C to separate at this volume.

48. DELTA IS INERT; KAPPA0 IS THE ONLY ACTIVE LEVER (in this implementation). At fixed kappa0,
    sweeping Delta 0->0.6 barely moves any order parameter (kappa0=2.2: f_hub 0.456/0.464/0.426/
    0.426). Delta DOES tune f_tl (0.49-0.61 -- the second DOF works), but that does not translate
    into a phase change. The two-DOF unlock is real and is NOT by itself sufficient.

49. MEASURE THE ESTIMATOR'S UV BIAS ON THE FLAT CALIBRANT BEFORE READING ANY SCALE-FLOW. Flat T^4
    (m=6, N0=1296) gives d_s(4-12) - d_s(8-24) = +0.995: the short window reads ~1.0 HIGHER than the
    long one even on a genuinely-4D FLAT lattice. So a raw "UV > IR backward flow" is the LATTICE
    DEFAULT, not a hub signature -- SANDBOX_PROBE's backward-flow reading was scored against the
    continuum, not the benchmark. Always use DELTA_ds_rel = DELTA_ds(state) - DELTA_ds(flat).

50. KAPPA0 IS THE DE SITTER DIRECTION, AND THE FROZEN GRID STOPPED AT THE EDGE. Monotonic in kappa0:
    hubs 0.47->0.28, d_s(8-24) 3.9->5.2, and DELTA_ds_rel +0.66 -> +0.07 -> CROSSES ZERO
    (-0.06 at (5.0,0.2), -0.46 at (5.0,0.0)). The de Sitter flow direction first appears exactly at
    kappa0=5, the grid boundary. LESSON: choose grids so the expected transition is INTERIOR; if a
    trend is still monotonic at the boundary, the grid is too small.

51. HIGH KAPPA0 -> N0 RUNAWAY -> the practical wall. At (5.0,0.0) N0 never settles (1563->2125,
    rho0->0.050); the state balloons until the checkpoint hits 1.3 GB and the job OOMs/hangs. Any
    kappa0 > 5 follow-up NEEDS a vertex-density cap or a tighter volume term first.

52. NEVER GATE A PLATEAU TEST ON A NOISE-DOMINATED OBSERVABLE. The frozen plateau test required cv
    relative-drift < 5%; for the uniform tubes this ensemble produces, cv ~ 0.01 is pure estimator
    noise, so its RELATIVE drift never settles and every point grinds to the sweep cap. Gate on the
    PHYSICAL collective modes (N0, f_tl) and exempt an observable already at its floor (mean cv<0.05).

53. LONG-RUN ENGINEERING -- the failure modes, in the order they actually bit (cost ~3 days):
    (a) MULTI-GB CHECKPOINTS ON A MOUNTED WINDOWS DRIVE STALL. A 1.3 GB pickle written every 5
        sweeps to a nearly-full C: over drvfs HUNG the run for 11 h (and, because the saves kept
        failing, every restart resumed the SAME stale checkpoint -- the point looped for a day
        without progressing). Put checkpoints on a FAST LOCAL disk WITH SPACE (--ckpt-dir) and save
        infrequently (--ckpt-every 25). Logs (KB) can stay on the mount.
    (b) A WRAPPER THAT RESTARTS ON *EXIT* CANNOT RESCUE A *HANG*. Supervisors need a heartbeat
        WATCHDOG: kill -9 + restart when the heartbeat goes stale.
    (c) BUT A WATCHDOG THAT SEES A STALE HEARTBEAT AT STARTUP WILL KILL THE NEW PROCESS BEFORE IT
        CAN FINISH LOADING A MULTI-GB CHECKPOINT -> kill-loop (~30 kills in an hour). RESET the
        heartbeat at every launch.
    (d) `wsl.exe -e bash -lc "nohup X &"` -- bash exits, and WSL REAPS X. Run the supervisor in the
        FOREGROUND of wsl.exe (minimized window) so the WSL session stays alive.
    (e) DOUBLE-CLICKING THE LAUNCHER TWICE = two runners racing the same checkpoint (.tmp clobber ->
        corrupt .pkl). Kill-all before every relaunch; make the kill pattern self-match-proof
        (pkill -f 'cdt4_phasescan\.py' -- the backslash keeps it from matching its own cmdline).
    (f) THE COWORK MOUNT SERVES OVERWRITTEN FILES FRESH (heartbeat, RUNNER.pid) BUT CACHES
        APPEND-ONLY FILES STALE (results.jsonl, progress.txt, START.log). Read append-logs through
        the HOST path (Read tool), never through the bash mount, or you will analyse day-old data.
    (g) Desktop-approval dialogs for computer-use time out (3x here). The double-click path is the
        reliable one; build launchers that need exactly ONE click.
