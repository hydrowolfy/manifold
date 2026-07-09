# STAGE 3 PART C (production): does the 3+1D causal MEASURE dynamically select de Sitter?

Preregistered in PREREG_CDT_4D_PRODUCTION.md (committed BEFORE this report). Answers the
pending step E1 of PREREG_CDT_4D. Part A (two independent DOF; no 3+1D analogue of
dN22=-4dN0) and Part B (the flat foliated T^4 is a validated census-clean joint-4 causal
calibrant) are the structural landing of REPORT_CDT_4D.md. Part C builds and validates the
DYNAMICS -- the full ergodic move set + a detailed-balance-correct Metropolis -- and
launches the (kappa_0, Delta) production scan.

## Verdict (honest landing: MACHINERY COMPLETE + VALIDATED; dynamical de Sitter PENDING the uncapped run)

**The complete apparatus to answer the frontier question dynamically is now BUILT and
VALIDATED to the program's standard.** The full ergodic AJL 4D move set is implemented on
the validated cdt4_run.py core, every move is detailed-balance- and manifold-verified, the
Metropolis (including the vertex-changing Jacobian) satisfies detailed balance to numerical
zero, ergodicity is demonstrated, and the self-contained runner reproduces the frozen flat-T^4
benchmark bit-for-bit. **No dynamical "de Sitter reached" headline is claimed:** a
gate-quality measurement requires N0 >~ 1300 (below which the estimators saturate, LESSONS 38)
AND long thermalization of the N0 collective mode at fixed N4 -- a compute load that needs the
uncapped WSL box (the in-session sandbox runs are finite-size-saturated and under-thermalized).
This lands on PREREG_CDT_4D_PRODUCTION Sec 5 rule 2 (SCAN INCONCLUSIVE / PARTIAL) -- but
ADVANCES the Stage-3 STRUCTURAL-ONLY landing decisively: the production machinery is no longer
"to be built", it is built, validated, staged, and resumable. The dynamical verdict awaits
the long run (staged to Kirk's PC; blocked this session by desktop contention).

## PART C1 -- the full ergodic move set (built on cdt4_run.py, all DB + manifold verified)

Beyond the (2,4)/(4,2) pair already validated in REPORT_CDT_4D.md, three move families were
added (cdt4_prod.py), each foliation-preserving:

| move        | dN0 | dN4 | dN41 | dN32 | geometry                                    |
|-------------|-----|-----|------|------|---------------------------------------------|
| (2,4)/(4,2) |  0  | +-2 |  *   |  *   | timelike-tetrahedron flip (prior)           |
| (3,3)       |  0  |  0  | +k   | -k   | triangle flip, self-inverse                 |
| (4,6)/(6,4) |  0  | +-2 | +-2  |  0   | spatial (2,3) flip thru both sandwiches     |
| (2,8)/(8,2) | +-1 | +-6 | +-6  |  0   | spatial-tetrahedron vertex insert/remove    |

The (2,8)/(8,2) is the 4D lift of the 2+1D (2,6)/(6,2): a new vertex is inserted at the centre
of a SPATIAL tetrahedron (splitting it into 4), turning the 2 pentachora above/below into 8.
It is the operational realization of the SECOND DOF (spatial-vertex density N0) that Part A
proved independent of the timelike fraction -- the DOF 2+1D never had.

VALIDATION (cdt4_prod_selftest.py, all pass, revalidated standalone from the staged bundle):
- **Exact detailed balance per move**: forward then reverse returns the complex BYTE-IDENTICAL
  (set of pentachora unchanged); reverse action delta = -forward. Round-trips verified:
  (2,4)/(4,2) x20, (2,8)/(8,2) x15 (dN0=+1,dN4=+6 each), (3,3) x15 (self-inverse), (4,6)/(6,4)
  x15 (dN4=+2,dN0=0).
- **Manifold + foliation preservation**: census bad=0 and untyped=0 at every step; a 1500-attempt
  mixed 7-move chain ends census-clean with all 7 move types firing.
- **Counter integrity**: the incrementally-maintained simplex counts (N0,N1,N2,N3, spatial
  sub-counts, N41,N32) were checked EQUAL to a from-scratch recount after every move -- the
  detailed-balance move-count factors are exact.

## PART C2 -- ergodicity (empirical + AJL)

The move set is the standard 4D CDT set (Ambjorn-Jurkiewicz-Loll), ergodic in the foliated
ensemble by the CDT literature. Empirically (cdt4_ergodicity.py):
- N4 driven UP and back DOWN: 6144 -> 14588 -> 10606 (grow-biased then shrink-biased walk).
- N0 driven UP and back DOWN: 256 -> 1432 -> 810 -- BOTH DOF are dynamically accessible.
- timelike fraction f_tl = N32/N4 tunable over 0.26-0.55 (the Delta-conjugate DOF moves freely).
- 3 independent walks converge to a common observable region (N0~810-859, N4~10.4-10.7k,
  f_tl~0.335-0.346), census-clean throughout -- practical connectivity.

## PART C3 -- the Metropolis, detailed balance, and benchmark reproduction

Action (standard 4D CDT Regge form, cdt4_scan.py):
    S = -(kappa0 + 6 Delta) N0 + kappa4 N4 + Delta (2 N41 + N32) + eps (N4 - N4t)^2.
Acceptance A = min(1, (K_fwd/K_rev) exp(-dS)) with uniform move-type selection (reverse-pair
proposal probabilities cancel) and K = exact live pick-set count via indexed-sets.

**Detailed balance of the full Metropolis (including the vertex-changing Jacobian) verified
numerically**: the balance equation (1/K_f) A_f exp(-S) = (1/K_r) A_r exp(-S') holds to worst
deviation **0.00e+00** over 828 (move,state) pairs at random couplings (cdt4_scan.py --db-check).

**Benchmark reproduction (the trust check before any physics)**: the self-contained bundled
estimators (ball_growth_dim, lazy_rw_sdim, stdlib only) match the networkx-backed repo referee
BIT-FOR-BIT on identical adjacency+seed (flat T^4 m=6: d_H(2-6)=2.6556, d_s(8-24)=4.2001,
identical). 8-seed read: d_s(8-24)=4.01 +- 0.69, d_H(2-6)=2.656 -- reproduces the frozen
benchmark (4.117 +- 0.402 / 2.656) and reads cleanly 4D (>> the T^3 value 3.13).

## PART C4 -- the scan: staged, launched, preliminary signal, and the honest finite-size wall

The scan is staged to Kirk's PC (C:\\Users\\Kirk\\Downloads\\cdt4run\\, WSL /mnt/c/.../cdt4run) as a
single dependency-free bundle + a .bat launcher, resumable (re-running ADDS sweeps per point;
checkpoints per (kappa0,Delta)). The bundle was re-verified STANDALONE from that folder (DB
check PASS, move selftest PASS), isolated from the repo. Launch on the uncapped box was blocked
THIS SESSION by desktop-access contention (request timed out; allowlist empty).

Preliminary in-session scan (T=4, N4t=6144, eps=0.01, k0=2.2, D in {0.0, 0.6}, ~30 sweeps/point,
6 estimator seeds) -- reported honestly as NOT gate-quality:

| point        | N0  | N4   | f_tl  | prof_CV | d_s(8-24) | d_H(2-6) |
|--------------|-----|------|-------|---------|-----------|----------|
| k0=2.2 D=0.0 | 256 | 6276 | 0.505 | 0.0018  | 2.46      | 0.59     |
| k0=2.2 D=0.6 | 256 | 6250 | 0.507 | 0.0018  | 2.46      | 0.59     |

Two finite-size / thermalization facts these numbers make concrete (both preregistered caveats):
1. **Estimator saturation**: at N0=256 (m=4) the d_s ~2.46 and d_H ~0.59 are SATURATION
   ARTIFACTS (ball growth hits the T=4 wraparound), NOT dimensions -- exactly LESSONS 38's
   "small tori saturate; use N0 >~ 1300". A gate-quality read needs m>=6 (N0>=1296).
2. **Critical slowing of N0**: at fixed N4 the only N0-changing move is (2,8)/(8,2), whose
   dN4=+6 is opposed by the volume term, so N0 equilibrates as a slow collective mode. In ~30
   sweeps N0 and the profile barely move from the (uniform) flat seed (CV 0.002) -- the chain is
   pre-thermalization. This is intrinsic 4D CDT critical slowing, not a bug; it is why the run
   needs the uncapped box + long thermalization.

So the in-session runs confirm the PIPELINE (runs, measures, checkpoints, resumes) but cannot
reach the de Sitter gate -- consistent with the discipline that forbids a de Sitter claim from
an unthermalized, finite-size-saturated chain (LESSONS 40).

## What remains (the handed-off production run) -- exact recipe

On Kirk's WSL box (uncapped): double-click run_cdt4_scan.bat (T=5 N4t=15000 grid). To reach
gate quality: (a) run at N4t large enough that the equilibrium N0 exceeds ~1300 (T=6, N4t~31k,
or grow N0 via the measure at high kappa0); (b) thermalize each (kappa0,Delta) to a plateau in
N0, f_tl, and profile CV (>> the ~10^3-10^4 sweeps needed for the N0 mode), re-running the .bat
to extend; (c) at each point measure d_H(2-6)/d_s(8-24) with 8 seeds + the N3^SL(t) profile;
(d) score against the frozen gate G1-G5 (extended cos^3 profile, d_H ratio >=0.90, d_s ~4 IR
flowing to ~2 UV). Expected landing (per Part A + known 4D CDT phenomenology): the de Sitter
phase C near (kappa0,Delta) ~ (2.2, 0.6) passes; the small-Delta control collapses (phase B);
the extreme-kappa0/Delta=0 control fails (phase A) -- WALL BROKEN DYNAMICALLY. Not claimed here.

## Reproduce

    python3 cdt4_prod_selftest.py     # full move set: DB round-trips + census + counters
    python3 cdt4_ergodicity.py        # N4 & N0 bidirectional, f_tl tunable, census-clean
    python3 cdt4_scan.py --db-check    # Metropolis detailed balance (worst dev 0.00e+00)
    python3 cdt4_scan.py --scan --T 5 --N4t 15000 --eps 0.01 \\
        --grid-k0 1.5,2.2,3.0,4.0 --grid-D 0.0,0.4,0.6 --meas-seeds 8 --scratch scratch
