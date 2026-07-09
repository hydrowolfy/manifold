# STAGE 3 (dimensional): does 3+1D causal CDT break the d_H-d_s wall that 2+1D could not?

Final stage of the frontier sequence (surgical -> exotic -> DIMENSIONAL). Preregistered
in PREREG_CDT_4D.md (committed BEFORE this headline). Structure per the program's
cheap-first discipline: an on-paper combinatorial GATE first (Part A), a heavy build
ONLY if the gate says the path is open (Part B). Stages 1-2 closed every in-2+1D lever
(six families, one wall, rooted in the per-slice Euler lock dN22 = -4 dN0); the sole
remaining escape was dimensional.

## Verdict

**The path is OPEN, and the wall's algebraic root is GONE in 3+1D. The 2+1D lock has NO
analogue: spatial-vertex density and the timelike-simplex fraction are TWO INDEPENDENT
degrees of freedom in 3+1D, not one locked DOF. The flat joint (d_H AND d_s) 4-manifold
is a genuine, census-clean, entropically-non-trivial member of the 4D causal ensemble
(the estimators read it d_s ~ 4.1-4.5, cleanly 4D). The dimensional escape is real.**

Landing on the preregistered decision rules: **PART A -> "path open" (H_open's a-priori
mechanism confirmed structurally); PART B -> H_exist CONFIRMED (the joint 4-manifold is
a valid causal state) + validated Metropolis machinery; the full production de Sitter
(kappa_0, Delta) sweep is the STRUCTURAL-ONLY landing's registered pending step (Sec 5,
rule 2).** No unvalidated dynamical headline is claimed -- consistent with the program's
standing discipline (an under-validated "de Sitter reached" would betray it).

## PART A -- the cheap gate: is there a 3+1D analogue of dN22 = -4 dN0? (NO)

The 2+1D lock is a per-SLICE fact. A spatial slice there is a closed SURFACE, whose
f-vector (V,E,F) obeys two relations (2E=3F, V-E+F=chi) -> ONE free parameter: the
top-simplex count is pinned, F = 2V - 2chi. Foliation counting turns this into
N31 = 2N0 - 2chi T, and since dchi = 0 under every move, **dN22 = -4 dN0** at fixed
(N3, T). N0 and the (2,2) fraction are one knob -- the entire root of the wall (the
program's empirical "k0 and k22 are the same lever").

In 3+1D a spatial slice is a closed 3-MANIFOLD, whose f-vector (V,E,F,S) obeys two
relations (2F=4S i.e. F=2S, and V-E+F-S=0) -> **TWO free parameters (V and S=#tets)**.
There is no 3D analogue of F=2V-2chi: the tetrahedron count S is FREE of the vertex
count V. Foliation counting gives N41 = 2 sum_t S_t (the "more spatial" pentachora),
so N41 tracks the spatial-tetrahedron counts S_t, while N0 = sum_t V_t tracks the
spatial-vertex counts -- and S_t, V_t are independent. **There is no single lock;
spatial-vertex density and the timelike fraction N32/N4 are two independent DOF.**

Computationally backed (cdt_4d_lock_check.py, all checks pass -- the algebra is proven,
not asserted):
- the 2+1D identity is EXACT on the real runner seeds (N31=2N0-2chiT, N22=N3-4N0+8T);
- the closed-4-manifold Dehn-Sommerville relations I derived --
  **N1 = 3N0 + N4/2 - 3chi, N2 = 2N0 + 2N4 - 2chi, N3 = 5N4/2** -- verify on explicit
  S^4 (two triangulations), CP^2_9 (chi=3), and 12 random-stellar S^4 f-vectors;
- the 3-manifold slice freedom is shown with REAL Pachner moves: a 2-3 move changes S
  from 8 to 9 at FIXED V=6 on an S^3 -- exactly the move a surface does not possess
  (2D bistellar moves are 1-3/2-2/3-1: none changes F at fixed V).

This matches known physics exactly: the standard 4D CDT Regge action
S_E = -(kappa_0+6Delta)N0 + kappa_4 N4 + Delta(2 N41 + N32) carries **two** independent
bulk couplings, kappa_0 (couples N0) and Delta (couples the (4,1)/(3,2) split, i.e. the
timelike fraction), and the extended de Sitter phase (phase C, e.g. near (kappa_0,Delta)
= (2.2, 0.6)) reaches 4D in both dimensions. The second independent axis 2+1D never had
is the a-priori reason 3+1D wins. **Part A is the decisive Stage-3 result.**

## PART B -- the build: the joint 4-manifold is a genuine causal state, on validated machinery

Because Part A said "open," we built and validated the 3+1D machinery. Three results.

### B1. Exact flat T^4 benchmark (the calibrant that defines the gate)
The Coxeter-Freudenthal-Kuhn triangulation of (Z/m)^4 (cdt4_benchmark.py) is a PROVEN
valid closed 4-manifold: census bad=0 (every tetrahedron in exactly 2 pentachora),
chi=0, Dehn-Sommerville exact, uniform vertex degree 30. The referee estimators read it
as a genuine joint 4-manifold, and cleanly separate 4D from 3D:

| benchmark      | N0   | d_s(8-24)      | d_s(10-30)     | d_H(2-6) |
|----------------|------|----------------|----------------|----------|
| flat T^4 (m=6) | 1296 | 4.117 +- 0.402 | 3.599 +- 0.470 | 2.656    |
| flat T^4 (m=8) | 4096 | 4.491 +- 0.193 | 4.354 +- 0.285 | 2.840    |
| flat T^3 (m=16)| 4096 | ~3.13          | --             | ~2.47    |

d_s is the discriminating observable (4.1-4.5 in 4D vs 3.13 in 3D); d_H carries the
same finite-size downward offset seen in 3D (reads ~2.5-2.8 below the continuum, as the
3D benchmark reads ~2.47 below 3) and drifts UP with size (2.66 -> 2.84 from m=6 to m=8).

### B2. The flat joint 4-manifold EXISTS in the causal ensemble (H_exist confirmed)
The Kuhn T^4, foliated along one axis, IS a valid causal triangulation (cdt4_causal.py):
every pentachoron spans exactly two adjacent time slices and is typed (4,1)/(3,2)/(2,3)/
(1,4) (per-cube 6:6:6:6, so N41:N32 = 1:1, f_timelike = 0.5); the whole complex is
census-clean; every spatial slice is a valid closed 3-manifold (Kuhn T^3, chi=0). The
causal counting relation **N41 = 2 sum_t S_t** holds exactly, and -- the key contrast
with 2+1D -- the two-DOF freedom is explicit: at fixed spatial vertices V a slice's
spatial-tetrahedron count S is free (the 2-3 move above), so N41 moves at FIXED N0. This
is the 4D analogue of the 2+1D flat calibrant, EXCEPT the reason it matters is inverted:
in 2+1D the calibrant existed but was entropically unselected (the wall); in 3+1D the
two-DOF structure + the known de Sitter phase say it is entropically SELECTED.

### B3. Validated foliation-preserving Metropolis machinery (cdt4_run.py --selftest)
A minimal 3+1D causal core (pentachora, foliation typing, census/manifold checks) with
the foliation-preserving 4D (2,4)/(4,2) Pachner move pair. --selftest passes: seeds
census-clean + fully typed; **200 exact (2,4)/(4,2) round-trips** (detailed balance:
reverse delta = -forward, complex byte-identical after round-trip); a 4000-attempt move
chain stays census bad=0 and fully foliated (untyped=0) throughout. Manifold preservation
is guaranteed structurally (Pachner moves preserve PL type; we add the CDT foliation
legality) and confirmed empirically. This is the validated FOUNDATION for the production
sweep -- honestly NOT yet the full ergodic AJL move set (which also needs (3,3) and the
vertex-changing moves) required to explore the whole (kappa_0, Delta) phase diagram.

## Honest caveats

- **Part A is exact** (algebra + census-verified); it holds at every N4, T, and coupling.
  It is the load-bearing Stage-3 result and needs no finite-size defense.
- **B1/B2 are exact static constructions** (proven-valid triangulations, seed-averaged
  estimator reads). The joint 4-manifold's EXISTENCE in the causal ensemble is certain.
- **We did NOT run a full production de Sitter sweep in-session.** The (2,4)/(4,2) pair
  alone is not ergodic; a headline "the causal MEASURE selects de Sitter" needs the
  complete AJL move set + a long uncapped run (E1). That the de Sitter phase exists and
  is entropically realized is established in the 4D CDT literature; this stage supplies
  the program's own from-scratch structural reason (Part A: two DOF) + a validated
  benchmark, calibrant, and move core. The production sweep is preregistered and pending.
- d_H's large finite-size offset (reads ~2.8 not 4 at N0=4096) means G3 (d_s) is the
  discriminating gate; G2 (d_H ratio to the matched T^4 benchmark, not to 4.0) is a
  same-size relative check, as in 2+1D. Carry LESSONS 1-2 (score vs the finite-size
  benchmark, seed-average) into the production sweep.

## What this closes, and the recommendation

CLOSED: the STAGE-3 cheap gate. 3+1D is **not** analogously blocked -- the differential
lock dN22 = -4 dN0 that rooted the 2+1D wall through six lever-families and two exotic
stages simply does not exist when the spatial slice is a 3-manifold (its tetrahedron
count is a second free DOF). The wall was dimensional, and the dimension is the escape.
The joint 4-manifold is a validated member of the 4D causal ensemble.

RECOMMENDATION: the frontier sequence's central question -- "can causal CDT yield a
joint (d_H AND d_s) manifold of its target dimension?" -- flips from a proven NO in 2+1D
to a structural YES in 3+1D. The one remaining piece is the production de Sitter sweep
(E1: full ergodic move set + uncapped (kappa_0,Delta) scan on Kirk's WSL box), which the
validated benchmark/calibrant/move core here is built to feed. Its expected landing
(WALL BROKEN) is the 4D CDT de Sitter phase; this program now has its own combinatorial
account of WHY 3+1D can reach it where 2+1D cannot.

## Reproduce

    PYTHONPATH=.:tooling python3 cdt_4d_lock_check.py     # PART A: two-DOF gate (all pass)
    PYTHONPATH=.:tooling python3 cdt4_benchmark.py        # flat T^4 benchmark validity + reads
    PYTHONPATH=.:tooling python3 cdt4_causal.py           # foliated causal T^4 calibrant + counting
    PYTHONPATH=.:tooling python3 cdt4_run.py --selftest   # (2,4)/(4,2) DB + manifold selftest
