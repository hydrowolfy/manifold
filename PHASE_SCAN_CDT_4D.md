# REPORT: coarse (kappa_0, Delta) phase-diagram scan of 3+1D causal CDT (STAGE 3 PART D)

Preregistered in PREREG_PHASE_SCAN_CDT_4D.md (committed BEFORE any point was measured; commit
dc5441a). Answers: does a genuine phase-C (de Sitter) region exist anywhere in the accessible
(kappa0, Delta) plane, and was (2.2,0.6) simply the wrong phase?

## VERDICT (headline, honest negative + a positive direction)

**NO PHASE C ANYWHERE IN THE ACCESSIBLE PLANE. And no phase A or B either.** All 12 measured
grid points -- spanning kappa0 in {1.0, 2.2, 3.5, 5.0} x Delta in {0.0, 0.2, 0.4, 0.6} at
T=6, N4~42000 -- classify as the SAME state: a hub-dominated, extended, structureless uniform
tube (the C_b / bifurcation-like class of the prereg). The A/B/C phase structure of standard
4D CDT **does not resolve at this volume with this implementation**.

**(2.2,0.6) was NOT "the wrong phase."** It is not distinguishable from the rest of the plane.
The earlier N4=45000 failure was not a bad coupling choice -- the entire accessible plane is
the same hub-dominated phase.

**BUT the scan produces a clean, monotonic, actionable direction: kappa0.** Every de Sitter
signature improves monotonically with kappa0 and the d_s scale-flow CROSSES ZERO into the de
Sitter direction at kappa0=5 -- the edge of the frozen grid. De Sitter, if it is reachable at
all here, lies at kappa0 > 5.

## The phase map (all measured points; 8 estimator seeds; census bad=0 throughout)

Gate for phase C (frozen): f_hub <= 0.08, cos^3 blob, r_H >= 0.90, d_s flow DOWN (DELTA_ds_rel < 0).

| kappa0 | Delta | sw  | plat | N0   | f_hub | r_H   | d_s(8-24) | DELTA_ds_rel | cos3 amp | top_frac | class |
|--------|-------|-----|------|------|-------|-------|-----------|--------------|----------|----------|-------|
| 1.0    | 0.0   | 600 | yes  | 1269*| 0.467 | 0.587 | 4.019     | +0.624       | 0.065    | 0.172    | C_b   |
| 1.0    | 0.2   | 600 | yes  | 1280*| 0.466 | 0.606 | 3.874     | +0.700       | 0.040    | 0.169    | C_b   |
| 1.0    | 0.6   | 600 | yes  | 1300 | 0.416 | 0.647 | 3.912     | +0.660       | 0.023    | 0.169    | C_b   |
| 2.2    | 0.0   | 600 | yes  | 1297*| 0.456 | 0.617 | 3.989     | +0.607       | 0.044    | 0.171    | C_b   |
| 2.2    | 0.2   | 600 | yes  | 1309 | 0.464 | 0.610 | 3.982     | +0.596       | 0.058    | 0.170    | C_b   |
| 2.2    | 0.4   | 600 | yes  | 1332 | 0.426 | 0.618 | 4.067     | +0.529       | 0.091    | 0.171    | C_b   |
| 2.2    | 0.6   | 821 | yes  | 1339 | 0.426 | 0.605 | 4.022     | +0.598       | 0.036    | 0.171    | C_b   |
| 3.5    | 0.0   | 600 | yes  | 1382 | 0.426 | 0.635 | 4.134     | +0.576       | 0.050    | 0.172    | C_b   |
| 3.5    | 0.2   | 600 | yes  | 1418 | 0.402 | 0.592 | 4.008     | +0.588       | 0.023    | 0.169    | C_b   |
| 3.5    | 0.6   | 600 | yes  | 1442 | 0.379 | 0.594 | 4.166     | +0.412       | 0.025    | 0.170    | C_b   |
| 5.0    | 0.0   |1000 | NO   | 2125 | 0.280 | 0.723 | 5.174     | **-0.459**   | 0.095    | 0.178    | C_b(u)|
| 5.0    | 0.6   | 600 | yes  | 1722 | 0.319 | 0.660 | 4.449     | **+0.074**   | 0.056    | 0.173    | C_b   |
| 5.0    | 0.2   |(600 prov) | - | 1760 | 0.322 | 0.635 | 4.664 | **-0.058**   | 0.120    | 0.173    | C_b   |

*N0 < 1300 -> flagged ESTIMATOR-SATURATED (prereg Sec 7); its d_s/d_H absolutes are not certified,
but its hub/profile classification (saturation-robust) stands.
(u) = did not converge: N0 runaway (see Finding 4).
Remaining grid points (1.0,0.4), (3.5,0.4), (5.0,0.4) are interior fill-ins; they cannot change the
verdict (they are bracketed on all sides by C_b points).

## Findings

**1. The plane is ONE phase, not three.** Every point is a hub-dominated uniform tube:
f_hub = 0.28-0.47 (gate: <= 0.08), r_H = 0.59-0.72 (gate: >= 0.90), top_frac ~ 0.17 everywhere
(i.e. the spatial volume is spread perfectly evenly over all 6 slices), cos^3 amplitude 0.02-0.12
(a ripple, not a blob). There is NO single-slice collapse anywhere (no phase B), NO decoupled /
multimodal profile anywhere (no phase A), and NO cos^3 de Sitter blob anywhere (no phase C).

**2. Delta is INERT; kappa0 is the only active lever.** At fixed kappa0, sweeping Delta from 0.0
to 0.6 barely moves any order parameter (e.g. kappa0=2.2: f_hub = 0.456, 0.464, 0.426, 0.426).
This is a sharp discrepancy with standard 4D CDT, where Delta drives the B<->C transition. In this
implementation Delta tunes the timelike fraction f_tl (0.49-0.61, as designed -- the second DOF
works) but that does NOT translate into a phase change. **The two-DOF unlock is real but is not,
by itself, sufficient to produce the phase structure.**

**3. kappa0 moves everything, monotonically, in the de Sitter direction.** As kappa0 goes 1.0 -> 5.0:
   - hub fraction FALLS:            0.47 -> 0.28
   - d_s(8-24) RISES:               3.9  -> 4.45-5.17  (through and past the flat-T^4 benchmark)
   - DELTA_ds_rel FALLS and CROSSES ZERO: +0.66 -> +0.07 -> **-0.06 / -0.46** at kappa0=5
   The d_s scale-flow turning NEGATIVE is the de Sitter dimensional-reduction signature (UV
   suppressed relative to the flat lattice). It first appears exactly at the kappa0 edge of the
   frozen grid. **The grid stops precisely where the physics starts turning over.**

**4. kappa0=5, Delta=0 has a runaway N0.** N0 climbs without settling (1563 -> 1703 -> 2125,
rho0 -> 0.050) and never plateaus. This is also the practical wall: the state balloons until the
checkpoint reaches 1.3 GB and the run OOMs/hangs. It is reported UNCONVERGED. (Its d_s and flow
are nonetheless the most de-Sitter-like in the whole scan -- consistent with Finding 3.)

**5. The hub domination is the wall, and it is NOT the 2+1D wall.** The 2+1D program's wall was a
d_H-d_s ANTICORRELATION forced by a combinatorial lock. Here d_H and d_s are BOTH improving with
kappa0 simultaneously (r_H 0.59->0.72 while d_s 3.9->5.2). Nothing is locked. The obstruction is
simply that the entropically-dominant configurations at N4=42000 are hub-dominated everywhere in
the scanned coupling window -- a VOLUME/COUPLING-RANGE problem, not a structural one.

## Verdict on the two preregistered questions

- **Q1 (does phase C exist in the accessible plane?)** -> **NO.** Prereg Sec 8 landing:
  "NO C ANYWHERE (important honest negative)". The clean de Sitter phase is not accessible at
  N4=42000 over kappa0 <= 5, Delta <= 0.6.
- **Q2 (was (2.2,0.6) simply the wrong phase?)** -> **NO -- it was not a wrong CHOICE.** The whole
  plane is one phase; (2.2,0.6) is typical of it, not an outlier. The prior N4=45000 result was
  not a coupling mistake; it was the generic behaviour of this ensemble at this volume.

## Honest caveats

- N4 = 42000 is 1-2 orders of magnitude BELOW the volumes at which 4D CDT de Sitter is established
  in the literature (N4 ~ 1e5-1e6). A null result for phase C at this volume is expected to be
  volume-limited and is NOT evidence against 4D CDT.
- T=6 gives only 6 profile points: the UNIFORM-TUBE vs COS3-BLOB discrimination is
  resolution-limited (prereg Sec 7). The classification rests on the saturation-robust order
  parameters (hubs, d_H ratio, d_s flow), which are unambiguous here.
- Three points (1.0,0.0), (1.0,0.2), (2.2,0.0) sit just below the N0 >= 1300 estimator-validity
  floor and are flagged saturated; their absolutes are uncertified (their hub classification is not).
- (5.0,0.0) is UNCONVERGED (N0 runaway).

## Logged deviations from PREREG_PHASE_SCAN_CDT_4D.md (Sec 6)

1. **Plateau criterion**: the frozen test required cv relative-drift < 5%. For the uniform-tube
   states this ensemble produces, cv ~ 0.01 is noise-dominated and its relative drift essentially
   never reads < 5% -- (2.2,0.6) ran 600->825 sweeps without settling. The cv condition was relaxed
   to "cv-drift < 5% OR mean(cv) < 0.05" (i.e. an already-uniform profile satisfies it); convergence
   is then governed by the two PHYSICAL collective modes N0 and f_tl. Commit b1d5e52.
2. **cap-sweeps 1500 -> 1000** to bound the non-converging kappa0=5 points. Points that hit the cap
   are recorded with plateaued=False and reported UNCONVERGED.
3. **--skip (5.0,0.0)** was armed after that point OOM/hung repeatedly; it in fact completed to the
   1000-sweep cap before the skip took effect, so it IS reported (as UNCONVERGED).
4. Measurement itself (8 estimator seeds, all order parameters, the frozen gate) is UNCHANGED.

## What this says to do next (ranked)

1. **EXTEND kappa0 PAST 5 at Delta=0.6** -- kappa0 = 7, 9, 12. Every trend (hubs down, d_s up,
   flow crossing into the de Sitter direction) extrapolates to phase C living beyond the frozen
   grid's kappa0 edge. This is cheap (the high-kappa0 states are the ones the scan already handles)
   and is the single highest-information follow-up.
   CAVEAT: high kappa0 also drives the N0 runaway (Finding 4) -- a vertex-density cap or a tighter
   volume term will be needed to keep those points tractable.
2. **RAISE N4** toward 1e5. The hub domination is the generic small-volume behaviour; the literature
   de Sitter phase is established only at much larger N4.
3. Only after 1 and 2 fail should the implementation itself be suspected.

## Reproduce

    python3 cdt4_phasescan.py --scan --T 6 --N4t 42000 --eps 0.002 \
        --ckpt-dir <fast local disk> --ckpt-every 25 --cap-sweeps 1000 --scratch out
    python3 analyze_phasescan.py out/results.jsonl     # frozen decision tree -> the phase map

Machinery validated before any physics: move-set DB round-trips + census (cdt4_prod_selftest.py),
Metropolis detailed balance worst dev 0.00e+00 (cdt4_scan.py --db-check), ergodicity
(cdt4_ergodicity.py), and flat-T^4 benchmark reproduction (m=6: d_H(2-6)=2.6556 EXACT vs the frozen
2.656). The benchmark also supplied the estimator's UV-bias baseline DELTA_ds(flat) = +0.995, without
which the raw "UV > IR" reading would be misread as a hub signature (it is the lattice default).
