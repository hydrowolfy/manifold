# Preregistration: the high-kappa0 follow-up row (STAGE 3 PART E)

Date: 2026-07-13. Registered and committed BEFORE any high-kappa0 point is measured.
Follows PHASE_SCAN_CDT_4D.md, whose result was: across kappa0 in {1,2.2,3.5,5} x Delta in
{0,.2,.4,.6} at N4~42000, EVERY point is one hub-dominated uniform tube -- no phase C, and no
A or B either. The one clean, monotonic signal was in kappa0, and the frozen grid stopped exactly
at the edge where it turns over.

## 0. The question

Every de Sitter signature improves monotonically with kappa0, and the benchmark-relative d_s
scale-flow CROSSES ZERO into the de Sitter direction at kappa0 = 5 (DELTA_ds_rel = -0.06 at
(5.0,0.2), -0.46 at (5.0,0.0)) -- the grid boundary. Does extending kappa0 past 5 at Delta=0.6:
  (a) reveal PHASE C, or
  (b) reveal PHASE A (branched polymer), i.e. did we sail past C, or
  (c) neither -- the hub tube simply persists?
Any of the three LOCATES us in the phase diagram, which the Part D scan could not do at all.

## 1. Hypotheses (pre-set confirm/refute)

- **H_C (phase C found).** Some kappa0 in {7,9,12} at Delta=0.6 passes the FROZEN phase-C gate of
  PREREG_PHASE_SCAN_CDT_4D.md Sec 4: f_hub <= 0.08 AND cos^3 blob (cos3_r2>=0.80, amp>=0.40,
  single-peaked) AND r_H >= 0.90 AND d_s(8-24) within 0.30 of the matched flat-T^4 benchmark AND
  DELTA_ds_rel < 0 AND a stable plateau.
  CONFIRM -> phase C located; flag it as the point to push volume.
- **H_A (phase A found; branched polymer).** rho0 = N0/N4 DIVERGES (the point pins at the N0
  ceiling, Sec 3) AND the geometry degenerates: profile becomes multimodal / decoupled (peaks >= 2,
  or n_empty grows), d_H(2-6) falls toward ~2, and d_s(8-24) falls away from the 4D band.
  CONFIRM -> we have passed/bracketed C: the A-C line lies between kappa0=5 and that point, and the
  next probe is the interval kappa0 in (5, that point) and/or larger Delta.
- **H_null (trend continues).** Hubs keep falling monotonically but no gate is passed and no phase-A
  signature appears. CONFIRM -> the coupling grid is still too small, OR N4 (not kappa0) is the
  binding constraint; the next lever is N4, not kappa0.

## 2. Frozen setup (inherited verbatim from PREREG_PHASE_SCAN_CDT_4D.md)

Action, Metropolis, estimators (8 seeds), the flat-T^4 benchmark (incl. the measured UV-bias
baseline DELTA_ds(flat) = +0.995), the order parameters OP1-OP5, and the classification decision
tree are UNCHANGED. Only the grid, the volume, and the N0 ceiling below are new.

## 3. NEW: the soft N0 ceiling (a computational guard that does NOT mask the physics)

At kappa0=5, Delta=0 the vertex density RUNS AWAY (N0 -> 2125 and climbing, never settling;
1.3 GB checkpoints; OOM/hang). kappa0 >= 7 will be worse. We therefore add to the action:

    S += eps0 * max(0, N0 - n0max)^2         with n0max = 3000, eps0 = 0.01

This is a pure STATE FUNCTION (exactly like the existing eps volume term), so detailed balance is
unaffected in form -- and it was RE-VERIFIED NUMERICALLY with the term active: worst
|log lhs - log rhs| = **0.00e+00** over 371 (move,state) pairs.

**The ceiling BOUNDS the runaway; it does not HIDE it.** N0-PINNED (defined: N0 >= 0.98 * n0max) is
reported as an order parameter. A pinned point is a RUNAWAY / degenerate signal (evidence for H_A),
and its N0-derived quantities (rho0, and any d_s/d_H read at a ceiling-distorted vertex density) are
flagged as CEILING-BIASED and are NOT used to claim a phase-C pass. A point that passes the phase-C
gate while PINNED is NOT counted as phase C.

## 4. Grid and volume (frozen)

- kappa0 in {7, 9, 12}, Delta = 0.6.  T = 6.
- N4t = 30000 (reduced from 42000). Rationale: at the elevated vertex density of high kappa0
  (rho0 0.05-0.10 observed/extrapolated), N4=30000 puts the equilibrium N0 in the band ~1500-3000 --
  ABOVE the N0 >= 1300 estimator-validity floor (LESSONS 43) and BELOW the ~3000 tractability
  ceiling. At N4=42000 the same rho0 would give N0 ~ 2100-4200 (intractable; that is what broke
  Part D).
  CAVEAT (stated in advance): N4=30000 is a SMALLER volume than Part D's 42000, so its finite-size
  offsets are LARGER. Absolute d_s/d_H are therefore scored ONLY against the matched-N0 flat-T^4
  benchmark, never against Part D's numbers or the continuum.
- eps = 0.002, ckpt-every 25, cap-sweeps 1000, plateau test as amended (LESSONS 52).

## 5. Decision rules (which verdict we land)

- **PHASE C FOUND** -> a non-pinned point passes the frozen gate and survives an independent
  re-measure. Report where; this becomes the volume-push point. (Would be the program's first
  dynamical de Sitter.)
- **PHASE A FOUND** -> pinning + degenerate geometry (multimodal/decoupled profile, d_H -> ~2).
  Report that C is BRACKETED between kappa0=5 and that point; next probe is that interval.
- **TREND CONTINUES / NEITHER** -> hubs still falling, no gate, no A. Conclude the coupling range is
  not the binding constraint and pivot to N4 (toward 1e5). This is the honest "kappa0 was not the
  answer" landing, and it is a real result: it would say the hub domination is a VOLUME effect.

Grid, volume, ceiling, hypotheses and decision rules above are FROZEN as of this commit.
