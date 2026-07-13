# Note: the soft N0 ceiling added to cdt4_scan.py `action_val`

The production action used by every scan in this program is:

    S = -(kappa0 + 6*Delta)*N0 + kappa4*N4 + Delta*(2*N41 + N32) + eps*(N4 - N4t)^2

STAGE 3 PART E adds one optional term, a SOFT CEILING on the spatial-vertex count:

    S += eps0 * max(0, N0 - n0max)^2          # active only when n0max>0 and N0>n0max

Defaults are n0max=0 (OFF), so every Part-D result in PHASE_SCAN_CDT_4D.md is produced by the
unmodified action and is unaffected.

## Why it exists

At kappa0=5 the spatial-vertex density RUNS AWAY: N0 climbs without settling (1563 -> 1703 -> 2125,
rho0 -> 0.050), the state balloons until each checkpoint is 1.3 GB, and the job OOMs/hangs. kappa0 in
{7,9,12} (the Part E row) would be strictly worse. The ceiling bounds the state so the run is
tractable.

## Why it does not corrupt the physics

1. It is a pure STATE FUNCTION of N0 -- exactly like the existing eps*(N4-N4t)^2 volume-fixing term.
   The Metropolis acceptance uses dS = S(after) - S(before), so detailed balance is preserved in form.
2. VERIFIED NUMERICALLY with the term ACTIVE (n0max deliberately set low so it is exercised):
   the balance equation (1/K_f) A_f exp(-S) == (1/K_r) A_r exp(-S') holds to worst deviation
   **0.00e+00** over 371 (move,state) pairs. (Same gold-standard check as LESSONS 42.)
3. It BOUNDS the runaway without MASKING it (PREREG_PHASE_SCAN_HIGHK.md Sec 3):
   - N0-PINNED (N0 >= 0.98*n0max) is REPORTED as an order parameter -- pinning is itself the
     runaway/degenerate signal and is evidence for the phase-A hypothesis.
   - Pinned points are flagged CEILING-BIASED; their N0-derived quantities are not trusted.
   - **A point that passes the phase-C gate WHILE PINNED does NOT count as phase C.**

This is the difference between a guard and a fudge: the ceiling makes the intractable computable,
and the thing it constrains is measured and reported rather than hidden.
