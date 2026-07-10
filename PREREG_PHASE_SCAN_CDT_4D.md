# Preregistration: COARSE (kappa_0, Delta) phase-diagram scan for 3+1D causal CDT

Date: 2026-07-09. STAGE 3 PART D. Registered and committed BEFORE any scan point is
measured. This document freezes the phase-classification ORDER PARAMETERS, THRESHOLDS,
grid, volume, thermalization protocol, and decision rules, so the phase map and the
"does phase C exist / was (2.2,0.6) the wrong phase" verdict cannot be tuned post hoc.

Supersedes nothing; it OPERATIONALIZES the phase-map experiment E1/E3 preregistered in
PREREG_CDT_4D_PRODUCTION.md as a COARSE grid to LOCATE phases A/B/C in the plane, rather
than to certify a single de Sitter point. The frozen action, estimators, benchmark, and
gate G1-G5 of PREREG_CDT_4D_PRODUCTION.md are inherited verbatim (Sec 1 below). The
machinery (full ergodic AJL move set + detailed-balance Metropolis + benchmark
reproduction) is built and validated (cdt4_prod.py / cdt4_scan.py; selftests re-run and
PASS this session: move-set DB+census, --db-check worst 0.00e+00, ergodicity, flat-T^4).

## 0. Motivation and the specific question

A single production point (kappa0,Delta)=(2.2,0.6) at N4=45000 (SANDBOX_PROBE_CDT_4D.md)
produced an EXTENDED, census-clean, 4-reading geometry (d_s(8-24)~4.9-5.0 at N0~1780) that
nonetheless FAILS the clean de Sitter gate: d_H(2-6)~1.9 (ratio ~0.71 < 0.90), the d_s
scale-flow runs BACKWARDS (UV window d_s(4-12)=5.54 > IR window d_s(8-24)=4.95), ~33% of
vertices are hubs (deg>40; flat T^4 is uniform deg 30), and the spatial-volume profile is a
uniform tube, not a localized cos^3 blob. That is the fingerprint of a hub-dominated /
small-world ("wrong") phase, NOT de Sitter. The OPEN question this scan answers:

  Q1. Does a genuine phase-C (de Sitter) region exist anywhere in the accessible (kappa0,
      Delta) plane at tractable N4, and if so WHERE?
  Q2. Was (2.2,0.6)@N4=45000 simply in the crumpled / bifurcation (hub) phase rather than de
      Sitter -- i.e. is the failure a WRONG-PHASE result, a FINITE-SIZE result, or both?

We do NOT brute-force volume at one coupling. We map the plane at fixed tractable N4 and read
the phase each point sits in from robust order parameters.

## 1. Inherited frozen setup (from PREREG_CDT_4D_PRODUCTION.md; unchanged)

- Action:  S = -(kappa0 + 6 Delta) N0 + kappa4 N4 + Delta (2 N41 + N32) + eps (N4 - N4t)^2.
  kappa0 couples N0 (spatial-vertex density); Delta couples the (4,1)/(3,2) split (timelike
  fraction) -- the SECOND independent DOF (Part A). eps-quadratic fixes 4-volume near N4t.
- Metropolis acceptance (DB-verified to 0.00e+00): A = min(1, (K_fwd/K_rev) exp(-dS)).
- Estimators (repo referee, bundled stdlib-only, used VERBATIM): ball_growth_dim (d_H),
  lazy_rw_sdim (d_s), on the vertex 1-skeleton. K = 8 estimator seeds; sigma = seed sd.
- Benchmark (FROZEN): flat Kuhn T^4, size-matched by N0. Score d_H/d_s vs this finite-size
  benchmark, NEVER the continuum 4.0 (LESSONS 1-2, 38).
    m=6 (N0=1296): d_s(8-24)=4.117 +- 0.402 | d_H(2-6)=2.656 (det)
    m=8 (N0=4096): d_s(8-24)=4.491 +- 0.193 | d_H(2-6)=2.840 (det)
  Flat T^3 contrast: d_s(8-24)~3.13, d_H(2-6)~2.47. d_s cleanly separates 4D(~4.1-4.5) from
  3D(~3.1) and is the discriminating observable. For a scan point at N0 between 1296 and 4096
  the matched benchmark is LINEARLY INTERPOLATED in N0 between the m=6 and m=8 values (as in
  SANDBOX_PROBE). Points below N0=1296 are flagged ESTIMATOR-SATURATED (Sec 5).

## 2. Phase labels -- STANDARD Ambjorn-Jurkiewicz-Loll convention (naming reconciled)

We adopt the standard 4D-CDT literature labels. NOTE (explicit): PREREG_CDT_4D_PRODUCTION.md
Sec 2 used A/B SWAPPED relative to the literature (it called the crumpled phase "A" and the
branched-polymer phase "B"). This document uses the STANDARD convention, matching the task
framing and Ambjorn-Jurkiewicz-Loll:

- PHASE A (branched-polymer): large kappa0. The universe is a sequence of ~uncorrelated small
  sub-universes; NO single extended blob; spatial-slice volumes decoupled/multimodal; d_H ~2
  (polymer-like); LOW-to-moderate hubs. Lives at large kappa0.
- PHASE B (crumpled/collapsed): small Delta. The 4-volume collapses; almost all spatial volume
  piles into ~one time slice (single-slice spike); maximal local connectivity; VERY HIGH hub
  fraction; d_H large/ill-defined. Lives at small Delta.
- PHASE C (de Sitter, extended): Delta above the A-C / B-C lines (e.g. near (2.2,0.6) in the
  literature). A single smooth cos^3 spatial-volume blob spanning most of the time extent;
  d_H -> 4 at large scale; d_s flowing DOWN from ~4 (IR) to ~2 (UV); LOW hub fraction. TARGET.
- BIFURCATION / hub-dominated-extended (C_b): the modern CDT diagram has a bifurcation phase
  between B and C: an EXTENDED profile (not a single-slice spike) but HUB-DOMINATED with the
  d_H/d_s pathology. We allow this as a distinct classification because it is EXACTLY the
  (2.2,0.6)@45k fingerprint (extended tube + 33% hubs + backward d_s flow + low d_H).

## 3. Order parameters (FROZEN definitions). Measured per grid point at thermal plateau.

For each point, after thermalization (Sec 6), with census bad=0 required (else DISCARD):

OP1 -- SPATIAL-VOLUME PROFILE SHAPE.  N(t) = N3^SL(t) = # spatial tetrahedra per time slice
  (cdt4_prod.slice_profile). Derived scalars (all frozen):
    CV      = sd(N)/mean(N)
    R_max   = max(N)/mean(N)           R_min = min(N)/mean(N)
    n_empty = #{t : N(t) < 0.15*mean(N)}         (depleted slices)
    top_frac= max(N)/sum(N)            (fraction of spatial volume in the fullest slice)
    cos3_R2 = R^2 of a least-squares fit of N(t) to  A*cos^3((t-t0)*pi/W) + c  (A>0, c>=0,
              free t0,W), over the periodic time; compared against a CONSTANT model and a
              SINGLE-SPIKE model. (Coarse at T=6; see Sec 7 caveat.)
  Shape class (frozen):
    SPIKE (B)        : top_frac > 0.50  OR (R_max > 3 AND n_empty >= T-2)
    UNIFORM-TUBE     : CV < 0.10  AND R_max < 1.5  AND cos3_R2 not better than the constant fit
    COS3-BLOB (C)    : cos3_R2 >= 0.80  AND single-peaked AND width spans >= T-2 slices with a
                       smooth falloff to <= 2 depleted edge slices
    MULTIMODAL (A)   : >=2 comparable peaks OR cos3_R2 < 0.5 with no single dominant hump

OP2 -- HUB FRACTION and DEGREE DISTRIBUTION on the vertex 1-skeleton (cdt4_prod.skeleton_adj):
    deg_mean, deg_sd, deg_max, and
    f_hub   = fraction of vertices with degree > 40      (flat T^4 uniform deg=30 -> f_hub=0)
    f_hub30 = fraction with degree > 30                  (sensitivity companion)
  Hub class (frozen): HUB-DOMINATED if f_hub >= 0.20 ; LOW-HUB if f_hub <= 0.08 ;
    intermediate 0.08 < f_hub < 0.20 resolved by the other OPs. (Prior crumpled point: 0.33.)

OP3 -- HAUSDORFF DIMENSION.  d_H(2-6) primary, d_H(3-8) secondary. Ratio r_H = d_H(2-6)/
  benchmark(matched N0). Pass band r_H >= 0.90 (gate G3). d_H ~2 flags polymer (A).

OP4 -- SPECTRAL DIMENSION and its SCALE-FLOW.  d_s at UV window (4-12), IR primary (8-24), IR
  secondary (10-30). Flow statistic  DELTA_ds = d_s(4-12) - d_s(8-24).
  De Sitter dimensional reduction => d_s HIGHER in IR, LOWER in UV => DELTA_ds < 0.
  Hub/small-world shortcuts inflate short-scale spreading => d_s HIGHER in UV => DELTA_ds > 0.
  CRITICAL CONFOUND (frozen handling): on a SMALL flat torus the LONG window is finite-size
  (wraparound) suppressed, which by itself makes DELTA_ds > 0 (benchmark m=5: d_s(6-18)=4.52 >
  d_s(8-24)=3.70). Therefore DELTA_ds is scored ONLY at N0 >= 1300 (where the 8-24 window is
  trustworthy, LESSONS 5) and RELATIVE TO THE BENCHMARK: the de Sitter signature is
    DELTA_ds(state) < DELTA_ds(benchmark at matched N0)   AND   d_s(8-24, state) within 0.3 of
    the matched benchmark and clearly > 3.13.
  The hub signature is DELTA_ds(state) > DELTA_ds(benchmark) with d_s(4-12) inflated. Below
  N0=1300 the flow SIGN is reported but NOT used for classification (saturation-confounded).

OP5 -- TIMELIKE FRACTION and VERTEX DENSITY.  f_tl = N32/N4 (the Delta-conjugate order
  parameter) and rho0 = N0/N4 (the kappa0-conjugate). Reported for every point; used to trace
  the transition lines (f_tl responds to Delta; rho0 to kappa0). Not a pass/fail by itself.

## 4. Classification decision tree (FROZEN). Applied per point after the plateau check.

  0. If census bad>0  -> DISCARD (invalid).
  1. If not thermalized (Sec 6 plateau test fails) -> UNCONVERGED (not classified; keep running).
  2. Else assign by:
     PHASE B (crumpled)   := HUB-DOMINATED (f_hub>=0.20) AND SPIKE profile (top_frac>0.50 or
                             R_max>3 with n_empty>=T-2).
     PHASE C_b (bifurc.)  := HUB-DOMINATED (f_hub>=0.20) AND profile EXTENDED (UNIFORM-TUBE or
                             a hub-riddled blob) AND (r_H < 0.90 OR DELTA_ds>benchmark). [the
                             (2.2,0.6)@45k fingerprint: extended but hubbed, backward flow.]
     PHASE A (branched)   := LOW-HUB (f_hub<=0.08) AND MULTIMODAL/decoupled profile AND
                             d_H(2-6) ~2 AND d_s(8-24) not reaching the 4D band (< ~3.5).
     PHASE C (de Sitter)  := ALL: census clean; LOW-HUB (f_hub<=0.08); COS3-BLOB profile;
                             r_H >= 0.90; d_s(8-24) within 0.3 of matched benchmark and >3.13;
                             DELTA_ds < benchmark (flow DOWN to UV); plateau stable.
     C-CANDIDATE (partial):= LOW-HUB AND EXTENDED (tube or blob) AND d_s(8-24) in the 4D band,
                             BUT N0<1300 so r_H / DELTA_ds are saturation-deferred. -> FLAG as
                             the point to push volume (the honest compute-bound landing).

  Intermediate hub fractions (0.08-0.20) or borderline profiles: report the OP vector and
  classify by nearest-signature, explicitly noting the ambiguity. This is a COARSE map.

## 5. Expected phase locations and negative controls (pre-set, so the map is a real test)

Standard AJL diagram => C occupies the upper region (larger Delta), B the lower-left (small
Delta), A the right (large kappa0). Pre-set expectations (to be confirmed or refuted):
- (2.2,0.6) : literature de Sitter point -> H_deSitter predicts C or C-candidate; the 45k
  result predicts C_b (hub-dominated) if finite-size dominates. Re-measured first.
- (2.2,0.0) : B control (small Delta) -> predict PHASE B (crumpled spike, high hubs).
- (5.0,0.0) : A control (large kappa0, Delta=0) -> predict PHASE A (branched, low hubs, d_H~2).
- Delta=0.6 row across kappa0 : if C exists, it is here; expect a kappa0 window that is C /
  C-candidate, flanked by C_b (low kappa0) and A (high kappa0).
An E3 negative control (a B and an A point) MUST fail the C gate, confirming the OPs
discriminate PHASES, not merely size.

## 6. Grid, volume, thermalization (FROZEN)

- Time slices: T = 6 (matches the validated m=6 benchmark; seed_flat(6) has N4=24*6^4=31104).
- Volume: N4t = 42000  (> seed 31104, so the grow phase runs and IRREGULARIZES the dense
  regular Kuhn seed -- RUN_LOG lessons 1-2; a tight volume term on the regular seed freezes
  the chain). eps = 0.002 (holds N4 near N4t without freezing; RUN_LOG used 0.004 at N4~24k).
  Rationale: at the high-Delta C-candidate region eq. N0 clears ~1300 (Delta RAISES N0 via the
  -(kappa0+6Delta)N0 term), so the estimators are un-saturated exactly where C is expected;
  low-Delta/low-kappa0 points may sit below N0=1300 -> flagged ESTIMATOR-SATURATED, but their
  classification (B via hubs+spike, A via low-hub+multimodal) rests on saturation-ROBUST OPs.
- Grid (FROZEN, coarse 4x4 + the literature point already inside it):
    kappa0 in {1.0, 2.2, 3.5, 5.0}   x   Delta in {0.0, 0.2, 0.4, 0.6}   = 16 points.
- Measurement ORDER (FROZEN, so a PARTIAL run still yields the core map). Each point warm-starts
  from a SHARED over-grown base (grown above N4t then relaxed -> approaches every equilibrium
  from above; no inter-point hysteresis):
    1  (2.2,0.6)  candidate         2  (2.2,0.0)  B control      3  (5.0,0.0)  A control
    4  (1.0,0.6)  5  (3.5,0.6)  6  (5.0,0.6)   [Delta=0.6 row: the C search]
    7  (2.2,0.4)  8  (2.2,0.2)   [kappa0=2.2 column: B->C transition]
    9  (1.0,0.0) 10 (3.5,0.0) 11 (1.0,0.2) 12 (3.5,0.2) 13 (5.0,0.2)
    14 (1.0,0.4) 15 (3.5,0.4) 16 (5.0,0.4)  [fill]
- Thermalization protocol (FROZEN). Per point: run Metropolis; checkpoint every sweep
  (resumable); record N0, f_tl, CV, acc, census each sweep to a per-point jsonl; a single
  overwritten heartbeat.txt line per sweep. PLATEAU test: measured only when N0, f_tl, and CV
  each have |relative linear drift over the last 300 sweeps| < 5% AND >= 600 sweeps have run
  past the grow phase. At plateau: measure OP1-OP5 with 8 estimator seeds (report sd). Any
  point that classifies as C or C-candidate gets an INDEPENDENT re-measure (different estimator
  seed base) before being reported as such.
- Compute: uncapped WSL box, one uncontended scan (RUN_LOG: two big scans starve each other).
  Resumable; the run may span multiple sessions. Distinct scratch dir + filenames from the 9am
  scheduled task / the prior cdt4run bundle.

## 7. Caveats frozen in advance (honesty)

- T=6 gives only 6 profile points: UNIFORM-TUBE vs COS3-BLOB discrimination is
  profile-resolution-limited. The ROBUST de Sitter discriminators at this resolution are
  hubs (OP2) + d_H ratio (OP3) + d_s flow (OP4, at N0>=1300) + f_tl (OP5); profile SHAPE (OP1)
  is corroborating. A flagged C / C-candidate point is confirmed with a larger-T, larger-N4
  follow-up (the "push volume" step), NOT declared de Sitter from this coarse map.
- N0<1300 points are estimator-saturated: their d_s/d_H ABSOLUTES are not certified; only
  hubs/profile/f_tl classify them. Stated per point.
- d_s-flow sign is confounded by finite-size long-window suppression below N0~1300 (Sec 3 OP4);
  handled by benchmark-relative scoring at N0>=1300 only.
- No "de Sitter reached" headline from an unthermalized or saturated chain (LESSONS 40). This
  scan LOCATES phases and FLAGS a push point; certification is the subsequent large-N4 run.

## 8. Decision rules / verdicts (which landing we report)

- C EXISTS: >=1 grid point meets the PHASE C classification (Sec 4) and survives re-measure ->
  report WHERE (kappa0,Delta) C sits, its boundaries vs B/C_b/A, and flag it as the push point.
- C-CANDIDATE ONLY (compute-bound honest landing): a low-hub extended region with d_s(8-24) in
  the 4D band exists but N0<1300 defers r_H/flow -> flag that (kappa0,Delta) as the volume-push
  point; report the map from the robust OPs.
- NO C ANYWHERE (important honest negative): every high-Delta point is hub-dominated (C_b/B) or
  branched (A); the (2.2,0.6) fingerprint persists across the accessible plane -> conclude the
  clean de Sitter phase is NOT accessible at this N4 with this implementation; the resolution is
  either larger N4 (>10^5, literature scale) or a standard 4D-CDT refinement (e.g. explicit
  bifurcation-phase handling, better N0 thermalization) -- documented as the next step.
- VERDICT ON (2.2,0.6): classify it FROM THIS SCAN. If it reads C_b (hub-dominated extended)
  while some other (kappa0,Delta) reads C/C-candidate -> "(2.2,0.6)@45k was the wrong (hub/
  bifurcation) phase; C lives at <where>." If (2.2,0.6) is the LEAST-hubbed extended point and
  still fails -> "finite-size, not wrong-phase; push volume at (2.2,0.6)." Both are honest,
  pre-committed outcomes.

Order parameters, thresholds, grid, volume, thermalization, and decision rules above are FROZEN
as of this commit. Any later deviation is logged as a deviation with reason.
