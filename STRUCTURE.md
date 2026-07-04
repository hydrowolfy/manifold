# Project structure — aligned to document 0

This package is the hypergraph-physics laboratory **organized around the canonical reconstruction
hierarchy** (document 0): 14 sections (0 substrate → 13 appendices), each with subsections and
leaf-level claims, **every node carrying an honest grade**. The filesystem *is* the hierarchy.

## Layout

```
emergence/
  sec00_core_substrate/        <- the shared ENGINE (hypergraph, rewriting, causal_graph, observables)
  sec01_raw_wolfram_hypergraph_facts/
  sec02_pre_newtonian_kinematics/
  ...                          <- one folder per document-0 section
  sec13_speculative_extensions_appendices/
  tree.py                      <- single source of truth for the GRADES (the scoreboard)
  main.py                      <- renders the hierarchy and dispatches experiments
  constants.py  config.py
  emergence_monolith.py        <- the v7.9 archive (bundled whole)
  tooling/                     <- dev tools only (regression checks, figure stubs) -- NOT physics
```

Inside each section folder is **one module per subsection**, named `sNN_M_<slug>.py`, holding the real
implementation code (`STATUS`, `run()`, and helpers). The modules import the engine from
`sec00_core_substrate` (which re-exports `betti1`, `evolve`, `apply_rule`, `redexes`,
`build_causal_graph`, `two_core`, `ball_dimension`, `degree_sequence`). **Section 0 is the engine** —
it both *is* the substrate (document-0 §0) and is the shared library every other section imports;
those two roles are the same modules, so there is no separate "core". A module that informs more than
one subsection (e.g. the gauge experiment, §6.2/§6.6/§11.3, or the causal cones, §1.1/§7.1) lives in
its primary section and the others reference it via `tree.py`.

**Why `tooling/` is the one non-section folder.** Regression-test batteries and figure generators are
dev infrastructure, not part of the physics hierarchy — like `tests/` in any repo. Everything that is
physics lives in a section.

## The grade source of truth

`tree.py` encodes the entire hierarchy as data: 14 sections, 72 subsections, 364 leaves, each with a
grade (`DEF / DERIVED / PARTIAL / BORROWED / CONJECTURE / OPEN / REFUTED / EXT`), aligned to
`Reconstructing-the-Physics-Hierarchy_v8.1.md` and `REFEREE_REPORT_v1.md` — i.e. **post-referee**
(local confluence PARTIAL not "theorem"; consistency–dimension ceiling PARTIAL/empirical; curvature
measured, not asserted; dimension a range; nothing graded on a "3+1" assumption). Each subsection points
to the module(s) that implement it (`exp`, str or list) and the monolith commands that back it (`mono`).
**Change a grade here and the whole project updates** — no grade is hand-duplicated, and section modules
read their grade back from `tree.py`.

## The v7.9 archive

`emergence_monolith.py` is the original 64-experiment monolith, bundled whole; 63 of its commands map to
tree leaves (table below). **Caveat:** its *inline* grades predate the v8.1 referee corrections (it
still calls local confluence a "theorem via the Critical Pair Lemma"); the `mono` dispatcher prints a
banner saying so, and the current honest grade is always the one in `tree.py`.

## Usage

```
python main.py tree            # the full document-0 hierarchy, every node graded  (primary view)
python main.py status          # grade rollup: per-section, subsection tally, leaf tally
python main.py section 4       # one section expanded to leaves, with code/monolith pointers
python main.py run 4.1         # run the experiment in sec04.../s4_1_inertial_motion.py
python main.py map             # subsection -> module / monolith command map
python main.py mono glider     # run a monolith archive experiment (some need numpy/scipy)
```

## Current scoreboard (leaf granularity)

```
 leaf tally:  DEF=12   DERIVED=74   PARTIAL=120   BORROWED=17   CONJECTURE=29   OPEN=105   REFUTED=4   EXT=5
 total leaves: 364   subsections: 72   sections: 14
 subsections with native code: 55   backed by monolith archive: 38   (section modules: 102)
```

The headline is unchanged from v8.1 — this is a **reorganization and a finer-grained scoreboard**, not
new physics. The DERIVED leaves are the same beachhead (substrate facts: linear growth, `b₁`
conservation, exact acyclic causal graph; mechanics: inertia, scalar-charge collision conservation,
composite body; EM kinematics: gauge invariance, conserved charge, cos-Wilson transport; plus the
borrowed Lorentz/OS bridges and the partial thermodynamic arrow). Everything else is honestly PARTIAL,
CONJECTURE, or OPEN, now located precisely in the hierarchy.

## Monolith command → tree leaf map

All 64 archive experiments, mapped to the document-0 node(s) they inform:

| monolith `cmd` | document-0 subsection(s) |
|---|---|
| `fronts` | 7.1 Invariant speed |
| `cone` | 1.4 Symmetry; 7.1 Invariant speed |
| `rp` | 9.2 Amplitudes |
| `jw` | 11.5 Standard Model bridge |
| `heisenberg` | 3.4 Energy-like quantities; 9.2 Amplitudes |
| `z` | 7.5 Symmetry restoration; 13.2 Horava-like interpretation |
| `specdim` | 1.3 Dimensionality |
| `bott` | 11.5 Standard Model bridge |
| `nodecreate` | 3.1 Counting invariants |
| `dome` | 11.5 Standard Model bridge |
| `edge` | 11.5 Standard Model bridge |
| `grow` | 10.1 Metric emergence |
| `op7` | 11.5 Standard Model bridge |
| `grid` | 1.5 Statistics; 12.4 CMB analogues; 13.1 Boost-Fano statistics |
| `source` | 1.5 Statistics; 13.1 Boost-Fano statistics |
| `hunt` | 1.5 Statistics; 13.1 Boost-Fano statistics |
| `branch` | 1.5 Statistics; 3.1 Counting invariants; 13.1 Boost-Fano statistics |
| `horizon` | 10.5 Strong gravity; 13.5 Holography / AdS-CFT analogues |
| `lrule` | 2.2 Time proxies |
| `relaxer` | 2.2 Time proxies |
| `sprinkle` | 1.6 Coarse-graining; 2.4 Measurement |
| `channel` | 1.2 Locality; 7.1 Invariant speed |
| `rapidity` | 1.2 Locality; 2.4 Measurement; 7.3 Lorentz behavior |
| `cosmos` | 12.1 Expansion; 12.4 CMB analogues |
| `twoplus` | 1.4 Symmetry |
| `threeplus` | 1.4 Symmetry |
| `dynamic` | 1.5 Statistics; 13.1 Boost-Fano statistics |
| `fulldist` | 1.5 Statistics; 13.1 Boost-Fano statistics |
| `midi` | 0.4 Observables |
| `bridge` | 0.3 Evolution history; 1.1 Causal structure |
| `overlap` | 0.3 Evolution history; 1.1 Causal structure |
| `hypergraph` | 0.1 Hypergraph state; 0.2 Rewrite rule |
| `keystone` | 0.1 Hypergraph state; 0.2 Rewrite rule |
| `grain` | 1.5 Statistics; 13.1 Boost-Fano statistics |
| `round` | 1.5 Statistics; 13.1 Boost-Fano statistics |
| `weld` | 9.1 Multiway evolution; 9.2 Amplitudes |
| `action` | 9.1 Multiway evolution; 9.2 Amplitudes |
| `genesis` | 10.1 Metric emergence |
| `climb` | 10.1 Metric emergence |
| `closing` | *(archive-only: cross-cutting wrap-up, not a single leaf)* |
| `foliation` | 10.1 Metric emergence |
| `lightcone` | 7.1 Invariant speed; 7.4 Minkowski structure |
| `curvature` | 10.2 Curvature |
| `desitter` | 10.2 Curvature; 12.1 Expansion |
| `scaling` | 10.5 Strong gravity; 13.5 Holography / AdS-CFT analogues |
| `coefficient` | 10.5 Strong gravity; 13.5 Holography / AdS-CFT analogues |
| `ricci` | 10.2 Curvature |
| `einstein` | 10.4 Einstein limit |
| `branchial` | 9.1 Multiway evolution |
| `pathintegral` | 11.2 Propagators |
| `closure` | 1.4 Symmetry; 7.5 Symmetry restoration; 13.2 Horava-like interpretation |
| `doors` | 7.5 Symmetry restoration; 13.2 Horava-like interpretation |
| `confluence` | 1.1 Causal structure |
| `matter` | 3.1 Counting invariants; 6.2 Charge-like quantities; 11.3 Gauge theories |
| `particle` | 2.3 Motion |
| `glider` | 2.3 Motion; 4.1 Inertial motion |
| `collide` | 3.3 Momentum-like quantities; 4.6 Many-body mechanics |
| `charge` | 6.2 Charge-like quantities; 6.6 Gauge structure; 11.3 Gauge theories |
| `family` | 1.3 Dimensionality |
| `dimension` | 1.3 Dimensionality |
| `tension` | 1.3 Dimensionality |
| `knob` | 1.3 Dimensionality |
| `depth` | 1.3 Dimensionality |

*(`closing` is a cross-cutting "bring every remaining thread to rest" round and is archive-only.)*

## Porting log — round 1 (native experiments ported & re-verified)

Each port is re-implemented against `core/` (pure Python, no third-party deps), re-verified with a
fresh measurement, calibrated where possible, and only then graded. Three landed this round, and
together they produced a genuine result.

| Library module | Subsection(s) | Was | Now | What it measures |
|---|---|---|---|---|
| `foundations.spectral_dimension` | 1.3 | (missing) | DERIVED | spectral dim `d_s ~ 1.3-1.5` via lazy-walk return prob; calibrated 1D->0.98, 2D->1.93, 3D->2.83 |
| `relativity.light_cones` | 7.1, 1.1 | stub | DERIVED | exact causal cones; cone-volume spacetime dim `D ~ 2.3` from pure order |
| `foundations.degree_distribution` | 1.5 | OPEN stub | DERIVED | pendant-dominated (~57% degree-1), bounded tail |

**The finding (a real one): the keystone has three different effective dimensions, and they disagree
in a coherent way.**
- **Volume / ball-growth** (`foundations.dimensionality`): `d_H ~ 2.3-2.5`.
- **Diffusion / spectral** (`foundations.spectral_dimension`): `d_s ~ 1.3-1.5`.
- **Causation / causal-cone** (`relativity.light_cones`): spacetime `D ~ 2.3` => spatial `~ 1.3`.

The two *transport* probes (diffusion and causation) agree at ~1.3 and sit well below the *volume*
count of ~2.4. That gap `d_s, D-1 < d_H` is the signature of a **ramified geometry** -- much volume,
poor connectivity -- and `foundations.degree_distribution` supplies the mechanism: the rule mints a
degree-1 pendant every step, so a majority-pendant tree-with-loops is forced. Four leaves moved to
DERIVED on the strength of these measurements (tally: DERIVED 50->54). This sharpens the program's
dimension story: "the dimension" is not single-valued even for a *single* rule -- it depends on whether
you count volume or probe transport. (Candidate addition to whitepaper section 1; flagged in HANDOFF.)

## Porting log — round 2 (curvature, measured)

| Library module | Subsection | Was | Now | What it measures |
|---|---|---|---|---|
| `gravity.curvature` | 10.2 | PARTIAL (clustering proxy + asserted −0.048) | DERIVED (sign) | exact Ollivier-Ricci curvature via pure-python optimal transport |

**This port closes a referee finding directly.** The v8.1 referee pass flagged that the headline
curvature `K = −0.048` was an *asserted constant produced by no shipped code*. This module replaces it
with a real measurement: the exact Ollivier-Ricci curvature `kappa(x,y) = 1 − W1(mu_x,mu_y)/d(x,y)`,
with the Wasserstein-1 distance solved exactly by an integer **min-cost flow** (no third-party deps).
Validated on known graphs (complete K5 → +0.75; cycle/path/grid → 0; internal tree edge → negative;
star leaf edge → 0 at idleness 0). Measured on the keystone:
- **idleness 0** (neighbour-uniform): mean `kappa ≈ −0.37`, with **zero positively-curved edges** —
  ~55% flat (the pendant edges) and ~45% negative (the tree-with-loops core). Uniformly non-positive.
- **idleness 0.5** (lazy): mean `kappa ≈ 0` (slightly negative); the lazy measure lifts leaf edges
  positive and roughly cancels the negative core.

The asserted −0.048 is reproduced by *neither* convention. The honest result: the curvature is
**non-positive, strongly negative at idleness 0**, with the mean's magnitude idleness-dependent and
quoted with its convention. And the ~55% flat-edge fraction tracks the ~57% pendant fraction — so the
curvature, the degree distribution, and the low transport dimensions are **one consistent
ramified-geometry picture**, now all measured rather than asserted. Two leaves moved to DERIVED
(tally 54→56); `constants.RESULTS["curvature_K"]` updated from the asserted −0.048 to the measured
result. (Candidate update to whitepaper §10; flagged in HANDOFF.)

## Porting log — round 3 (thermodynamics: a rigorous arrow of time)

| Module | Subsection | Was | Now | What it establishes |
|---|---|---|---|---|
| `s5_2_entropy` | 5.2 | stub | DERIVED | a formal entropy H(p_t); grows monotonically at rate d_s/2 |
| `s5_5_irreversibility` | 5.5 | PARTIAL (qualitative) | DERIVED | rigorous H-theorem: D(p_t‖π) monotone decreasing, verified per-start |
| `s5_3_equilibrium` | 5.3 | stub | DERIVED | π∝degree exact stationary; detailed balance exact; macrostate equilibrates ~200 steps |

**The result: a rigorous, quantitative second law for the substrate — and its rate is the geometry.**
For the (reversible) lazy random walk on the keystone graph, the relative entropy `D(p_t‖π)` to the
degree-stationary distribution **decreases monotonically to zero** — a genuine discrete H-theorem,
verified monotone for every one of 30 sampled start nodes (not just on average). Equivalently the
Shannon entropy `H(p_t)` increases monotonically, and in the spreading regime grows as
`H(t) ~ (d_s/2)·ln t`: the measured entropy-production rate is **0.82**, giving an implied
`d_s ≈ 1.6` that **matches the independently-measured spectral dimension** at the same scale. So the
second law and the substrate geometry are the same fact — entropy increases exactly as fast as a walker
explores the ramified graph. Equilibrium is exact (`π∝degree` stationary to 1e-18, detailed balance to
0), and the degree-distribution macrostate equilibrates within ~200 rewrite steps even as the graph
keeps growing. **Eight leaves moved to DERIVED (tally 56→64)** — the most substantial single round so
far, tying §5 (thermodynamics) to §1.3 (dimension) rigorously. (Candidate addition to whitepaper §5.)

Also this round: **structural cleanup** — the 5 redundant unwired stub modules left by the v0.4
migration (duplicate filenames in §5.3/§5.5/§7.3/§9.4/§12.5) were removed; their subsections are
covered by the primary module. Section modules: 47 → 42.

## Porting log — round 4 (holographic area law on the bare graph; the dimension dichotomy)

| Module | Subsection | Was | Now | What it establishes |
|---|---|---|---|---|
| `s13_5_holography_area_law` | 13.5 | unwired (continuum sprinkling only) | PARTIAL (native) | the area law holds *qualitatively* on the bare keystone graph; the dimension splits static vs dynamic |

The monolith's area-law experiments (`scaling`, `coefficient`) are continuum causal-set *sprinkling*
calculations — random points in Minkowski space, not the keystone graph — so they say nothing about the
substrate itself. This round adds the keystone-*native* measurement: how a region's edge boundary
scales with its volume. **Honest result, graded PARTIAL:** the boundary is **sub-extensive** — the
ratio `|∂R|/|R|` falls steadily as regions grow (~1.26 at |R|~8 down to ~0.51 at |R|~98), so an area
law qualitatively holds and the graph is *not* a pure expander. But the exponent is only loosely pinned
(`|∂R| ~ |R|^0.74`, R² ~ 0.63 — noisy, because the ramified graph is locally irregular), giving an area
dimension `~2.5–3.5` on the **static/volume** side. No grade was inflated; sub-extensivity is robust,
the sharp exponent and a true entanglement entropy are not done on the bare graph.

**The payoff is the synthesis.** The substrate's effective dimension has now been measured five ways,
and they fall into **two clean families**:
- **Static / counting** — volume ball-growth `~2.3–2.5`, area-law boundary `~2.5–3.5`.
- **Dynamic / transport** — spectral `~1.3–1.5`, causal-cone `~1.3`, entropy-production rate `d_s/2 ~1.6`.

Static probes (how much stuff, how much boundary) see a *higher* dimension than dynamic probes (how a
walker or signal actually spreads). That gap **is** the quantitative content of the ramified geometry,
and it now organizes every dimension result in the program. (Candidate synthesis note for whitepaper §1.)

## Porting log — round 5 (the force law: pre-registered conjecture TESTED and REFUTED)

| Module | Subsection | Was | Now | Result |
|---|---|---|---|---|
| `s4_2_force` | 4.2 | OPEN stub | the test (REFUTED leaf added) | the highest-leverage open conjecture, falsified |

This round attacked the program's **central open problem** — the missing force — by testing the
mechanism Paper I §8 *pre-registered*: weight redex selection at glider contact by `exp(−β·ΔS)`,
`ΔS` = change in loop-holonomy mismatch; predict opposite charges close faster, like slower, growing
with β. A faithful implementation was built (phase-aware keystone with holonomy-preserving transport,
verified to conserve a glider's charge exactly; two charged gliders; the biased selection).

**Result: REFUTED, in the strongest possible form** — like- and opposite-charge dynamics are
*byte-identical* at every β and every seed (not merely statistically indistinguishable). The failure is
structural, and the module proves all three obstructions:
1. the registered action is **sign-blind for separated charges**: `S = |+q|+|−q| = |+q|+|+q|`;
2. so the biased evolution is identical for like and opposite (all 150 seeds × β∈{1,3,8});
3. the only sign-sensitive quantity (total *signed* holonomy) is **conserved** → ΔS = 0.

Deeper reason and **constructive redirect**: a Coulomb force is an interference term `2∫E₁·E₂` between
*overlapping* fields; loop holonomies are localized and have no cross term, so no holonomy-mismatch
action can produce a force. The fix is an **extended connection + a field energy with the interference
term**, not a bias tweak. This is exactly what pre-registration is for: the top open item, tested
faithfully, fails for a precise reason that redirects the work. Recorded as a **REFUTED** leaf in §4.2
(force itself stays OPEN); Paper I §8 updated to close the pre-registration; whitepaper §4/§6 + ledger
updated.

## Porting log — round 6 (the force law, take two: a field energy that WORKS)

| Module | Subsection | Was | Now | Result |
|---|---|---|---|---|
| `s6_3_electric_field_analogues` | 6.3 | all OPEN | PARTIAL (+3 DERIVED leaves) | a charge-dependent force with correct signs; confining on the keystone |

The round-5 refutation pointed at the fix — an *extended* field with an interference term — and this
round builds it. Standard discrete U(1) electrostatics on the substrate graph (the structure is
**BORROWED**): charge density `ρ` on nodes, electric potential `V` solving the discrete Poisson / Gauss
law `L·V = ρ` (graph Laplacian, solved by a pure-python conjugate-gradient iteration), field
`E = −∇V`, and the interaction energy `E_int(a,b) = −½·q_a·q_b·R(a,b)` with `R` the effective
resistance — exactly the cross term the refutation said was missing.

**Results (the consequences are DERIVED):**
- **Correct sign law** — opposite charges ATTRACT (`E_int = +R/2` rises with separation), like charges
  REPEL (`−R/2` falls). This is the charge-dependent force the refuted holonomy-bias could *not*
  produce — confirming the refutation's diagnosis was right and its redirect is viable.
- **A substrate-specific prediction** — on the keystone, `R(a,b) ~ (graph distance)^1.0`, so the force
  is **CONFINING**: a linear potential and a constant attractive force (~0.5), *not* Coulomb 1/r. The
  reason ties straight back to the dimension synthesis: the transport dimension `d_s ~ 1.3 < 2`, and
  below two dimensions a field cannot spread out, so it confines. (Validated by the same code: 1D chain
  → linear/confining; 3D lattice → saturating Coulomb.)

**Honest grade — PARTIAL.** The field theory is *postulated* (BORROWED), not derived from the keystone
rule; the potential, the Gauss-law identity, the sign law, and the confining distance-law (forced by
the measured ramified geometry) are derived. Still OPEN: coupling this field energy *back* to the
rewriting so gliders dynamically move — the step from a force LAW to a force on matter, and the natural
next round. Tally: DERIVED 64→67. Across two rounds the force problem went from one named mechanism to a
refuted one (round 5) **and** a working field-energy law with a falsifiable substrate-specific form
(round 6).

## Porting log — round 7 (force ON MATTER: the field energy moves a glider)

| Module | Subsection | Was | Now | Result |
|---|---|---|---|---|
| `s4_2_force_coupling` | 4.2 | OPEN (one REFUTED mechanism) | PARTIAL | the field energy, coupled back to the rewriting, moves a glider charge-dependently |

The dynamical completion of the arc. Round 6 gave the static field-energy force law; this round
**couples it back to the rewriting**: the glider's real left-hop operator (the §4.1 inertia move) is
biased by the field-energy change it would cause, Glauber-style `P(hop)=1/(1+exp(β·ΔE))`. Because `ΔE`
depends on the charge-sign *product*, the motion is charge-DEPENDENT — exactly where the round-5
holonomy bias was charge-blind.

**Results (the glider is a real rewriting excitation; it stays a coherent 2-core in 100% of runs):**
- **Single glider + fixed source:** opposite charges drive it toward the source (final position 34→3 as
  β grows), like charges away (34→29); split grows monotonically with β; **identical at β=0**
  (charge-blind baseline).
- **Two mobile gliders:** opposite-charge separation CLOSES (16.6→3.7), like-charge OPENS (16.6→22.9) —
  exactly predictions (a),(b),(c) of the Paper I §8 pre-registered conjecture, now satisfied with the
  *corrected* (field-energy) action where the holonomy action failed.

**Honest grade — PARTIAL.** Field theory + coupling are POSTULATED (BORROWED), not derived from the
rule; and the regime is OVERDAMPED (the bias sets a drift rate, so v∼F, not Newtonian a∼F). So:
force-on-matter and charge-dependence — yes; full Newtonian dynamics — not yet. §4.2 Force moved
**OPEN → PARTIAL**; its module now dispatches the whole story (mechanism A REFUTED, mechanism B WORKS).
Tally: PARTIAL 112→115, OPEN 122→120. The force — the program's central classical gap — now has a
working, falsifiable, charge-dependent mechanism acting on matter.

## Porting log — round 8 (deriving the field coupling from the rule, as far as it honestly goes)

| Module | Subsection | Was | Now | Result |
|---|---|---|---|---|
| `s6_2_charge_like_quantities` | 6.2 | source/sink PARTIAL | DERIVED (+derivation) | the coupling derived down to one constant; charge = structural divergence |

Round 7 left the field coupling postulated; this round asks whether it can be DERIVED from the keystone
rule, and gives the honest partial answer — four derived pieces and one input independent of the construction.

**The obstruction (proven):** `redexes(E)` is a function of the edge multiset alone, so a U(1) phase tag
is invisible to the rule. The loop-HOLONOMY charge can *never* be read — the principled reason round 5
was byte-identical (not the action's fault; the charge was invisible in principle). A derivable charge
must be structural.

**Derived 1 — the right charge is the divergence** `ρ(node) = in_degree − out_degree`: rule-visible (a
function of the edges), **automatically neutral** (`Σρ=0`, every edge is +1 in and +1 out), and actively
moved by the rule (`Δρ = {x:+1, y:−1, z:−1, w:+1}` at a firing). Charge here is transported by the bare
rule, not a passive label. §6.2 source/sink defects → **DERIVED**.

**Derived 2 — it reproduces the force.** Feeding `ρ=in−out` from real in/out-degree defects into the
field energy gives opposite-attract / like-repel — the same law as the postulated point charges of §6.3.
The substrate's electromagnetic charge *is* the directed-flow divergence.

**Derived 3 — the field operator is the rule's own diffusion generator.** The energy `½VᵀLV` uses the
graph Laplacian `L`, which is exactly the generator of the lazy walk whose `π∼degree` H-theorem was
derived in round 3 (§5). The field is not borrowed Maxwell — it is the substrate's relaxation functional
(run() confirms diffusion under `L` lowers the field energy monotonically, 2.5→0.005).

**Derived 4 — the coupling form is forced.** Round 3 derived reversibility (detailed balance) w.r.t.
`π∼degree`; the unique reweighting that preserves it while biasing by an energy is the Boltzmann/Glauber
factor `exp(−β·ΔE)`. So the `P(hop)=1/(1+exp(β·ΔE))` of round 7 is the *only* detailed-balance-preserving
coupling — its form is derived; only the constant β is free.

**The independent input — β ≠ 0.** The bare rule fires *uniformly* (β=0): it diffuses charge but
exerts no interaction force (charges don't move by sign). Only β≠0 makes them move. Why matter couples to
its own field at all is not fixed by the rule — the substrate analog of "why is there electromagnetism,"
and the natural place to look is the rewriting-amplitude / quantum track (OPEN).

**Net (honest):** the coupling is derived from the rule **down to a single constant** — operator, charge,
and form are all the rule's own; only the existence/strength β is input. That reduces "an entire borrowed
field theory plus an arbitrary bias" to one number. Graded **PARTIAL**; DERIVED 67→69.

## Porting log — round 9 (attacking beta: the honest terminus)

| Module | Subsection | Was | Now | Result |
|---|---|---|---|---|
| `s6_5_coupling_constant` | 6.5 | — | added | beta is independent within the present construction (deeper fixing open) |

Round 8 left exactly one residual: the coupling constant β. The hope was that the amplitude track (which
buys the quantum `i` from reversibility) might also induce β, closing the derivation. **It does not — and
this round proves why**, a clean negative in the spirit of the round-5 refutation.

**The demonstration:** the entire force is the deviation of β from 0. Under the Glauber coupling
`P(hop)=1/(1+exp(β·ΔE))`, β=0 gives `P=1/2` — *no force at all*; the glider drifts only once β≠0.

**Three reasons β is not fixed by the rule OR the current construction (NOT a proof it is unconstrainable in principle):**
1. **β is an inverse temperature.** The keystone is *defined* by uniform redex selection — that *is* the
   β=0, infinite-temperature state: maximum entropy, no energy bias, provably forceless. A finite β is a
   finite temperature the bare rule does not specify. (Consistent with round 3: at infinite T the
   equilibrium is π∼degree with no energy tilt.)
2. **β is a two-body coupling.** It multiplies the field energy's cross/interference term `2⟨E₁,E₂⟩`; the
   rule's one-body generator (the Laplacian, round 3) has no two-body term, so fields superpose and there
   is no force at *any* temperature unless β is added by hand. β is orthogonal to everything the generator
   fixes.
3. **The force is classical.** A static field energy plus a real Glauber drift — no `i`. The amplitude
   track buys the quantum `i` (e^{−iHt} propagation vs e^{−Ht} diffusion), which is *kinematics*, not
   interaction; a Coulomb/confining force survives the classical limit, so the `i` cannot supply β.

**Verdict.** β is independent within the present construction — not fixed by the bare rule or the field-energy overlay,
which, exactly like α in physics and exactly like the handedness bit in the amplitude track ("possessed,
not derived") is suggestive but NOT a theorem of impossibility: whether a deeper principle (a finer rule, a branchial/amplitude consistency condition, a continuum or RG fixed point) fixes β is OPEN. The derivation closes here, honestly, at one number independent of the present construction.
(Honesty note surfaced: the round-6/7 force uses the *instantaneous* global field energy — the
electrostatic, non-local limit; a strictly local rule permits at most a retarded, mediated force —
radiation/magnetism, still OPEN.)

## Porting log — round 10 (making the field LOCAL: a retarded field, electrostatics as its static limit)

| Module | Subsection | Was | Now | Result |
|---|---|---|---|---|
| `s6_5_retarded_field` | 6.5 | — | added | the force is local/retarded; electrostatics is its static limit |

Round 9 left an honesty debt: the round-6/7 force uses the *instantaneous* global field energy
(non-local) — a strictly local rule can only carry a *retarded* force. This round pays it. A local field
`φ` on the nodes obeys a discrete damped-wave (telegrapher) equation `φ[t+1] = (2−g)φ[t] − (1−g)φ[t−1] −
h²(Lφ[t] − ρ)` with `L` the rule's own Laplacian (round 3) — a local, second-order-in-time update, so
disturbances propagate at finite speed.

**Two clean results:**
- **Retardation (a light cone).** A pulse produces a field that is *exactly zero* beyond a sharp causal
  front advancing at ~1 node/step; a disturbance reaches distance d only after ~d steps. The finite-speed
  local field round 9 demanded — not instantaneous reach.
- **Static limit = electrostatics.** With a held charge `ρ`, the damped field relaxes to the solution of
  `L V = ρ` — the *exact* instantaneous Poisson potential of round 6 (mismatch ~1e-30, identical). So the
  round-6/7 Coulomb/confining force is the **long-time limit of a genuinely local, retarded process**;
  the non-locality was an artifact of taking the static limit first.
- **Speed = causality.** The front advances at the graph's hopping speed (1 node/step), the same speed as
  the causal cone (round 1) — field disturbances and causal information share one `c`, both set by the
  graph.

**Honest grade — PARTIAL, no leaf inflation.** The spatial operator is the rule's own; the wave/temporal
structure is a postulated local field equation (the minimal local dynamics with a finite speed). What is
established: the electrostatic force *can* be carried locally and reduces to round 6 in the static limit.
Full radiation (an accelerating charge's outward flux — subtle in 1D, no geometric fall-off) and the
magnetic sector (a moving charge's retarded field) remain OPEN and are *not* claimed.

## Porting log — round 11 (the magnetic sector: Faraday is automatic; current → B; charges radiate)

| Module | Subsection | Was | Now | Result |
|---|---|---|---|---|
| `s6_4_magnetic_and_induction` | 6.4 | PARTIAL | +2 DERIVED leaves | Faraday = Bianchi identity; current sources circulating B; accelerating charge radiates |

Discrete exterior calculus on a 2D lattice — vector potential `A` on edges, `B = dA` (curl) on plaquettes,
`E = −dφ − ∂_t A` on edges — yields three results, one of them a genuine identity.

- **FARADAY'S LAW IS AUTOMATIC — the discrete Bianchi identity.** Because `B = dA` and `E = −dφ − ∂_t A`,
  `dE = −d(dφ) − ∂_t(dA) = −∂_t B` *identically* (`d²=0`), verified to **4.4e-16** for an arbitrary field
  history. This is the *same* `d²=0` that forbids magnetic monopoles. So the two **homogeneous** Maxwell
  equations (Faraday, no-monopole) are both automatic consequences of "the field is the curl of a
  potential" — only the two **inhomogeneous** ones (Gauss, Ampère) are dynamical (the EOM `d⋆F = J`).
  **Half of Maxwell is kinematics, not law.** Faraday induction → **DERIVED**; Curl-like operators (§6.4)
  → **DERIVED**.
- **AMPÈRE — a moving charge sources a circulating B.** Solving `L A_z = J_z` for a wire and forming
  `B = (∂_y A_z, −∂_x A_z)`, the circulation of B around a small loop enclosing the wire equals the
  enclosed current (~0.94≈1); the field is tangential, not radial. (Circulation falls for larger loops
  because the lattice boundary carries the return current — correct physics.) Ampère-Maxwell → **PARTIAL**.
- **RADIATION — an accelerating charge radiates.** An oscillating dipole's outward Poynting flux through a
  far circle is **exactly zero until the wavefront arrives** (causality) and **sustained positive after**
  (energy to the far zone), at the causal speed. 2D geometric spreading makes this clean — resolving the
  round-10 1D confound (a monopole can't radiate; total energy ≠ flux; both fixed here).

**Honest grade.** Faraday is DERIVED (an exact identity); Ampère and radiation are PARTIAL (demonstrated,
but the precise magnetostatic field shape and full radiation reaction are solver/lattice-limited and not
claimed). The spatial operator throughout is the rule's own Laplacian (round 3). Tally: DERIVED 69→71,
OPEN 120→117.

**Scope caveat (per referee).** These are a graph-gauge/cochain reconstruction, not bare-rule derivations.
The kinematic identities (no-monopole/Faraday/continuity-field-level) are the single fact `d²=0`, true on
*any* cell complex — DERIVED *conditional on* the overlay, not keystone-specific. The magnetic/Ampère/
radiation demonstrations run on an **auxiliary 2D square lattice**, not the native keystone graph; they are
PARTIAL toy models showing the formalism *can* support these behaviours. The genuinely bare-rule result in
this arc is the rule-level local charge conservation (continuity) and the structural-divergence charge. See
the bare-rule-vs-overlay table in the whitepaper.

## Porting log — round 12 (closing Maxwell: the continuity equation, and the unifying structure)

| Module | Subsection | Was | Now | Result |
|---|---|---|---|---|
| `s6_5_continuity` | 6.5 | OPEN→PARTIAL | Continuity DERIVED | Maxwell closed: 3 identities + 2 equations of motion |

The last Maxwell relation — **continuity** (`∂_tρ + ∇·J = 0`, charge conservation) — is, like Faraday and
no-monopole, the single identity `d²=0`, shown at two levels:

- **Field level.** The inhomogeneous equation is `d⋆F = J`; taking `d` gives `dJ = d(d⋆F) = 0` — continuity.
  In 2D, `div` of Ampère's `(∂_yB, −∂_xB)` is `∂_x∂_yB − ∂_y∂_xB = 0` (mixed partials commute), verified to
  **5.6e-17** for an arbitrary `B`.
- **Rule level.** The structural charge `ρ = in−out` (§6.2) is conserved by the bare keystone rule not just
  globally but **locally**: at every firing `Δρ` sums to zero *and* is supported only on the rewrite's own
  nodes `{x,y,z,w}` — charge that leaves a node lands on a neighbour, a conserved local current. (40 random
  firings on evolved graphs: worst `|Σ Δρ| = 0`, worst out-of-neighbourhood change `= 0`.)

Continuity equation → **DERIVED**; §6.2 charge-current continuity → **DERIVED**; §6.5 OPEN → **PARTIAL**.

**The closing shape of Maxwell on the substrate.** The four equations split cleanly:

- **Three are kinematic IDENTITIES** — the single fact `d²=0`, given `F=dA`: no-monopole `∇·B=0`, Faraday
  `∇×E=−∂_tB`, continuity `∂_tρ+∇·J=0`. All **DERIVED**.
- **Two are the dynamical equation of motion** `d⋆F=J`: Gauss `∇·E=ρ` and Ampère `∇×B=J+∂_tE`. Both
  **PARTIAL** — and they rest on the one field action whose single coupling constant `β` is the
  input independent of the present construction (§6.5 coupling_constant, round 9).

So the electromagnetic sector is closed as far as it can be: its **kinematic half is fully derived**, its
**dynamical half is PARTIAL and reduces to one number**. Tally: DERIVED 71→73, OPEN 117→115.

## Porting log — round 13 (Newton II: why the force is overdamped, and what a~F needs)

| Module | Subsection | Was | Now | Result |
|---|---|---|---|---|
| `s4_3_inertia_and_acceleration` | 4.3 | OPEN leaf | Resistance-to-acceleration PARTIAL | native glider is fixed-speed (overdamped v~F, capped at the causal speed); a~F needs a "massive" excitation |

The force-on-matter (round 7) is overdamped: `v ~ F`, not `a ~ F`. This round finds the **structural reason**
and ties it to the causal speed, with measurements on the actual glider.

- **The native glider is a fixed-speed soliton.** The minimal 2-cycle glider advances exactly one rail-node
  per 2-move — one speed `v0` (the causal speed, 1 node/tick). The field can only **gate** it: hop
  probability `P(F)=1/(1+exp(βΔE))`, so time-averaged `v = P(F)·v0`, set *instantaneously* by the force.
  Three measured consequences: (1) **constant force → constant velocity** (overdamped `v~F`; no
  acceleration — verified for favorable/zero/opposing force); (2) **fixed-speed ceiling = the causal
  speed** — however strong the force, `v` saturates at `v0=1` and never exceeds it (`P→1`); the glider is
  "massless-like"; (3) **no velocity memory** — drive it hard, cut the force, and `v` drops instantly to
  the unbiased baseline `~v0/2`. So the native force is **Ohmic/overdamped because the minimal glider has
  no velocity state to accumulate** — a precise obstruction to inertial `F=ma`, a negative in the spirit
  of round 5.
- **What `a~F` requires (and a relativistic bonus).** A velocity-**carrying** ("massive") excitation: an
  internal momentum `p` the force *changes* (`F = dp/dt`) and that *persists*. With the relativistic map
  `v = p/√(1+p²)` (which saturates at `v0`), one gets Newtonian behaviour: constant force → velocity
  **grows** over time (`a~F`: 0.30→0.66→0.83) and asymptotes to `v0`; force off → velocity **persists**
  (inertia). Inertial mass `m = 1/α`. **A massive particle is relativistic for free** — it asymptotes to
  the substrate's speed of light `v0`.
- **Honest grade.** The NATIVE result is the obstruction (overdamped, fixed-speed, no memory, capped at
  `v0`) — measured. The `a~F` demonstration uses a **postulated momentum variable** (an overlay, like the
  field energy of §6.3), not derived from the rule. Resistance-to-acceleration → **PARTIAL** (now
  characterized: native obstruction + overlay path). Building a *native* massive excitation (a structured
  glider with a persistent sub-luminal speed the force can advance) is the open mechanics frontier. Tally:
  OPEN 115→114, PARTIAL 114→115.

## Porting log — round 14 (mass as zitterbewegung: the single causal speed forces a Dirac/checkerboard particle)

| Module | Subsection | Was | Now | Result |
|---|---|---|---|---|
| `s4_3_mass_as_zitterbewegung` | 4.3 | added (no grade change) | — | a single causal speed forces a massive particle to be a zigzagging glider |

Round 13 left the puzzle: the native glider is fixed-speed, so where is a sub-luminal massive particle?
This round resolves it from two **measured native facts** and lands on the Feynman-checkerboard / Dirac
picture of mass.

- **Both chiralities are native.** The glider on a rail `i→i+1` moves toward `−index` at `v0`; the same
  glider on the mirror rail `i+1→i` moves toward `+index` at `v0`. Left- and right-movers are the one
  glider under the rule's mirror symmetry (verified: velocities `−1` and `+1`). Combined with round 13's
  "`v0` is the only speed", this **forces** the conclusion:
- **A sub-luminal particle must ZIGZAG between `±v0`.** Since `v0` is the only speed, a particle at rest
  cannot sit at an intermediate speed — it is a glider trembling between the two chiralities, its lower
  velocity the *average* of genuine `±v0` motion. This is **zitterbewegung**, made unavoidable by the
  substrate. Three consequences (all as averages of real `±v0` steps): (1) **rest mass = zigzag rate**
  (no flips → moves at `v0`, massless; flips → trembles in place, at rest); (2) **sub-luminal &
  relativistic for free** — a chirality bias drifts but `|⟨v⟩| < v0` always, asymptoting to `v0`, because
  you cannot average `±1` to more than `1`; (3) **`a~F`** — a force changing a persistent chirality-
  momentum (`F = dp/dt`) makes `⟨v⟩` grow (0.41→0.84→0.92), asymptote to `v0`, and persist when the force
  is removed (inertia).
- **Honest grade.** NATIVE and measured: both chiralities at `v0`, the single speed. CONSTRUCTED: the
  chirality-flip dynamics (the "mass term") and the force coupling — a model on top of native motion, like
  the §6.3 field energy. What is genuinely shown: the native single-speed structure **forces** the
  zitterbewegung form of mass and yields the relativistic speed limit for free, connecting the substrate to
  the 1D Dirac equation. Building a glider that *natively* reverses (e.g. off an orientation domain wall) is
  the open step. **No leaf grade inflated** (tally unchanged: DERIVED 73, PARTIAL 115, OPEN 114).

## Porting log — round 15 (incorporated gauge/photon findings; native-reversal NEGATIVE)

| Module | Subsection | Was | Now | Result |
|---|---|---|---|---|
| `s6_7_photon_and_radiation` | 6.7 | OPEN | PARTIAL (4 leaves) | the photon = chargeless gauge loop; radiation sector consolidated |
| `s4_3_mass_as_zitterbewegung` | 4.3 | — | (negative added) | native chirality reversal attempted; glider PINS, does not reflect |
| `s6_3_electric_field_analogues` | 6.3 | — | (clarified) | resistance exponent set by transport (spectral) dim, not Hausdorff |

Incorporated an external investigation (`gauge_photon_investigation.py`) and attacked the round-14 frontier.

- **The photon = a chargeless gauge loop (PART A).** A neutral 2-cycle `(v,w,phi),(w,v,-phi)` on a fresh
  node has holonomy **exactly 0 for any phase** (verified; basis-independent, the phases cancel) -> it
  carries no charge and sources no static force: a massless, chargeless gauge excitation. **Honest
  correction** to the original note: it inferred "Wilson-energy-free" from a spanning-tree Wilson action
  `S`, but `S` over a spanning-tree basis is **basis-dependent** (varies under edge reordering, shown), so
  a graph Wilson "energy" is not well defined; the robust invariant is the holonomy/charge. §6.7 module.
- **The static force = emergent-graph effective resistance (PART B).** Confirms round 6 on a larger graph
  (653 nodes): `R(d) ~ d^0.985` -> **confining** (linear potential). **Clarification incorporated:** the
  exponent `~1` is set by the **transport (spectral) dimension** `d_s~1.3`, *not* the Hausdorff `D~2.3`; a
  naive `R~d^(2-D)` with Hausdorff would wrongly predict saturation (slope `-0.3`). Added to §6.3.
- **§6.7 radiation consolidated.** Rounds 10-11 had demonstrated wave propagation, the causal speed,
  radiation from an oscillating dipole, and a Poynting flux (on an auxiliary lattice) but §6.7 was still
  all-OPEN; corrected to PARTIAL for those four leaves (Polarization, Dispersion remain OPEN).
- **Native chirality reversal -- NEGATIVE (the round-14 frontier).** Driven into a hard boundary the glider
  **pins** (cannot do its left-move, no rightward move exists); into an orientation domain wall it pins at
  the wall. It does **not** reflect: the glider is robustly **uni-chiral**. So the zitterbewegung flip (the
  Dirac mass term) is **not** provided by simple rail features and stays a model -- a clean negative that
  sharpens rounds 13-14 (the glider is fixed-speed AND cannot turn around). Native reversal remains OPEN.

Tally: PARTIAL 115->119, OPEN 114->110 (the §6.7 radiation corrections; the photon and the negative add no
leaves). No DERIVED inflated.

## Porting log — round 16 (trying to derive the Dirac mass term: a Weyl-world obstruction)

| Module | Subsection | Was | Now | Result |
|---|---|---|---|---|
| `s4_3_dirac_mass_obstruction` | 4.3 | added (no grade change) | — | the chirality flip (Dirac mass term) is not derivable; the keystone is a chiral Weyl world |

Attacked the round-14/15 frontier head-on: derive the chirality flip (the Dirac mass term) that would make
zitterbewegung native. It cannot be found, and the reason is a result.

- **The rule is CHIRAL.** For a path `x→y→z` the keystone writes `((x,z),(y,x),(z,w))` -- head `x` and tail
  `z` are treated asymmetrically. Applied to a path and its reverse it gives mirror-image results, never the
  same structure: a fixed handedness. The glider inherits it (uni-chiral; no rightward firing -- round 7).
  This is the same handedness bit the amplitude track calls "possessed, not derived."
- **No native L↔R coupling exists.** Both chiralities exist (the glider runs `+v0` on a rail `i+1→i`, `−v0`
  on `i→i+1`), so a massive particle would convert between them. But every coupling fails: **end-to-end
  junctions** pin the glider (the 2-path it needs breaks) -- a bounded 6000-state search across boundaries,
  domain walls, and five junction/defect types found no reversal; **side-by-side rungs** (the natural mass
  term) make the whole ladder one 2-core, **delocalizing** the glider (its 2-core jumps from 2 to 24).
- **Conclusion -- a WEYL world; mass is an irreducible input.** The keystone produces massless,
  single-chirality gliders (Weyl-like fermions). A Dirac mass term -- the `L↔R` coupling that would give
  zitterbewegung, hence a sub-luminal accelerable particle -- is **not derivable** from the bare rule; it is
  an irreducible input, joining the rule's handedness and `β`. **This mirrors the Standard Model exactly:**
  fermions are chiral in the kinetic term and get mass from a Higgs/Yukawa coupling, not the kinetics. The
  substrate is, at this level, a massless chiral world; mass is added structure.
- **Honest grade.** OPEN (a characterized obstruction, not a derivation): empirical evidence from a bounded
  search, not a proof of impossibility. Established: the rule's chirality (exact), junction pinning, rung
  delocalization. **No leaf grade changed** (tally unchanged: DERIVED 73, PARTIAL 119, OPEN 110).

## Porting log — round 17 (the structure of the keystone universe: one loop in a tree -> confinement)

| Module | Subsection | Was | Now | Result |
|---|---|---|---|---|
| `s6_3_confinement_flux_tube` | 6.3 | added (no grade change) | — | one loop in a tree; charges joined by a flux tube; QCD-like confinement from geometry |

Pulled on the b1-conservation thread (round 1) and found it organizes the whole picture.

- **The keystone universe is ONE LOOP IN A TREE.** b1 = E - V + C is conserved (round 1); from the triangle
  it stays **b1 = 1 forever** -- verified at many sizes, the undirected edge count always equals the node
  count, so the graph is a spanning tree plus exactly one extra edge. That single loop is the universe's
  **lone matter particle**: a small **bounded** cycle (length 2-11 across evolution, never growing
  unboundedly) that **wanders** through the graph -- one localized particle in an ever-growing tree of
  vacuum (~57% pendants).
- **Confinement and the flux tube.** Because the graph is tree-like, the effective resistance equals the
  graph distance (`R(a,b) ~ d`, R/d~0.93-0.98 -- series resistors), so the potential is **linear** and the
  force **constant** (a string tension). The current concentrates almost entirely on the single tree
  geodesic: ~d of the hundreds of edges carry 90% of the field = a **flux tube**, exactly the QCD picture.
- **Consequences (the QCD scenario):** **no free charge** (isolating one costs energy `~tension*distance`
  -> diverges); **physical spectrum = neutral states only** (the photon = neutral 2-cycle, s6_7; neutral
  pairs); **phase is substrate-specific** -- a 3D lattice deconfines to Coulomb (s6_3), the keystone
  confines because its geometry is tree-like (b1=1, `d_s~1.3<2`). **Confinement here is geometry, not a
  coupling.**
- **Honest grade:** PARTIAL. NATIVE and measured: b1=1 (tree + one loop), the bounded wandering matter
  loop, the unique-path transport, the flux-tube concentration -- all properties of the bare-rule graph.
  The energy/tension/Coulomb-limit reading uses the postulated field energy (the s6_3 overlay): native
  geometry clothed in an overlay field. **No leaf grade changed** (synthesis + new native measurements
  supporting the existing §6.3 force result). Tally unchanged: DERIVED 73, PARTIAL 119, OPEN 110.

## Porting log — round 18 (mesons: bound states of the confining force)

| Module | Subsection | Was | Now | Result |
|---|---|---|---|---|
| `s4_5_mesons_confined_bound_states` | 4.5 | OPEN (all 5) | PARTIAL | bound states are mesons: pure-linear, unbreakable string; inverse-square/Kepler REFUTED natively |

The confining force (round 17) has bound states, and they are mesons -- with two features that sharply
distinguish them from QCD, both forced by the substrate.

- **Pure-linear potential, no Coulomb piece.** A +/- charge pair (rho=in-out) at separation r has energy
  `V(r) = R(r) = sigma*r` with intercept ~ 0 (measured: `V/r = 1.00` out to r~4-6; full-mode fit
  `sigma~0.98, intercept~-0.08`). No short-range `-a/r` term -- unlike QCD's Cornell potential -- because a
  **tree has no short-range alternative paths**. A pure string.
- **Unbreakable string, no screening.** QCD's flux tube breaks at long range by popping a light
  quark-antiquark pair (screening). The keystone's matter is massless chiral Weyl fermions with **no
  pair-creation channel** (round 16), so the tube never breaks: `V=sigma*r` for ALL r. Stable mesons.
- **The flux tube** is the tree geodesic: ~1 edge wide, nearly uniform current (constant tension). The meson
  is **neutral** (total rho=0) and **bound** (separating costs `~sigma*r -> inf`): only neutral mesons are
  physical asymptotic states.
- **Consequences:** virial `2<T>=<V>` (linear; vs Kepler's `-<V>`); radial spectrum `M_n ~ sigma^(2/3) m^(-1/3)`
  (Airy levels, given the constituent mass input). **Inverse-square and Kepler-like laws are REFUTED on the
  native tree geometry** (the force is linear, not `1/r^2`); they are recovered only on an auxiliary 3D
  lattice (round 6).
- **Regge trajectory (rotational).** Model the meson as a rotating relativistic string of tension `sigma`
  whose ends move at the substrate's **universal speed `v0`** (the same causal speed the glider saturates,
  round 13). Both ingredients are native -- `sigma` from confinement, `v0` from the causal cone. Integration
  gives `M = pi*sigma*L`, `J = pi*sigma*L^2/2`, hence the **linear Regge trajectory `J = M^2/(2*pi*sigma)`**
  (verified: `J/M^2` constant to 4 digits): **meson spin grows as mass squared**, slope `alpha'=1/(2*pi*sigma)`
  fixed by the one tension. THE QCD meson signature, here a consequence of (confining tension + one speed
  limit). Honestly: semi-classical string mechanics applied to the substrate's measured `sigma` and `v0`, not
  a first-principles lattice spectrum.
- **Honest grade:** PARTIAL. NATIVE-measured: the pure-linear potential (intercept~0), the thin uniform flux
  tube. The energy/tension/spectrum reading uses the field-energy overlay (and a granted constituent mass);
  the unbreakable-string claim is inferred from the round-16 Weyl obstruction, not directly simulated; the
  Regge trajectory is a string-mechanics consequence of the native (sigma, v0). No leaf changed by the Regge
  addition.
- Tally: §4.5 OPEN(5) -> Inverse-square REFUTED, Kepler REFUTED, Orbital-trajectories PARTIAL, Virial
  PARTIAL, Radial-symmetry OPEN. Net PARTIAL 119->121, OPEN 110->106, REFUTED 1->3. (EXPECTED_TALLY updated.)

A performance note: the meson module uses Gauss-Seidel resistance and is gated by `EMERGENCE_FULL` (fast
~3s default on a ~220-node graph; `EMERGENCE_FULL=1` for the cleaner ~480-node measurement).

## Porting log — round 19 (scattering: a conserved particle number and a trivial free S-matrix)

| Module | Subsection | Was | Now | Result |
|---|---|---|---|---|
| `s4_6_scattering` | 4.6 | (shared s4_4 + mono) | (dedicated module, no grade change) | particle number conserved (no annihilation); free S-matrix kinematically trivial; interactions field-mediated |

Asked what happens when the substrate's excitations meet. Three facts, in decreasing order of rigor.

- **Particle number is conserved (topological protection).** Every firing has `db1 = dE - dV = +1 - +1 = 0`,
  so `b1` is conserved by EVERY step (verified for `b1 = 1, 2, 3` over 500 random firings -- never moves).
  The loops are the matter quanta (round 17), so particle number is an **absolute conserved charge**: no pair
  creation, no annihilation, matter perfectly stable. A **superselection rule stronger than the Standard
  Model** (where particle number changes via pair processes) -- the same law behind the unbreakable string
  (round 18) and the eternal single loop (round 17).
- **The free-glider S-matrix is trivial (kinematics).** Single speed + one chirality (rounds 13-16) =>
  **co-propagating gliders move in lockstep** (measured: separation stays exactly constant -> never
  interact) and **counter-propagating gliders pin** at the orientation wall (measured: both stop at the
  wall, never reach each other). So no `2->2` collision scattering; the free theory is effectively
  non-interacting.
- **Interactions are field-mediated; asymptotic states are mesons.** A glider crossing a field region is
  gated, transmission `~ 1/(1+exp(beta*dE))` (round 7) = potential scattering; charges are confined
  (round 18) so in/out states are neutral **mesons**, not free charges -- as in QCD (scatter hadrons, not
  quarks). Meson-meson (string-string) scattering is the genuine many-body frontier, not built here.
- **Honest grade:** PARTIAL. DERIVED-native: `b1` conservation -> no creation/annihilation (round 1's
  invariant read as a selection rule). Native-measured: the lockstep and the pinning. The field-mediated
  scattering and meson asymptotics rest on the overlay/confinement. **No leaf grade changed** (synthesis +
  characterization). Tally unchanged: DERIVED 73, PARTIAL 121, OPEN 106, REFUTED 3.

## Porting log — round 20 (referee-thread cleanup: targeted validation of the tree/confinement picture)

Addressed six referee threads (one was already done); two of them CORRECT earlier claims.

| Module | Change |
|---|---|
| `s11_1_loop_defects_and_vacuum` (NEW, 11.1) | generalized ICs, the two-core growth law, multi-defect coalescence |
| `s6_3_confinement_flux_tube` | corrected the loop-size claim; sharpened native-vs-overlay (charge-blind) |
| `s4_3_dirac_mass_obstruction` | ported the reversal search to run LIVE (not merely described) |

- **(1) Generalized ICs.** `b1=0` (a path) stays a pure tree forever -> the **vacuum is a pure tree, no
  matter**; for `b1=1,2,3` the non-loop remainder is 96-100% of nodes (tree-like vacuum in every case).
- **(2) Two-core bound -- CORRECTED.** The round-17 "bounded length 2-11" was a short-run artifact. Over
  long evolution the 2-core **grows sub-linearly** (`~steps^0.4`, measured `7.5 -> 13.5 -> 22.7` at
  `500 -> 2000 -> 8000`), i.e. **NOT bounded** -- but `loop/V -> 0`, so matter is a **vanishing fraction**
  of the universe, not a fixed-size particle.
- **(3) Multi-defect interactions.** Two loops started far apart (distance ~18) **coalesce** (attract/fuse)
  into a single connected 2-core cluster -- they do NOT stay independent (though `b1` stays 2: they fuse,
  never annihilate). A multi-loop state is one growing cluster in a tree vacuum.
- **(4) String breaking -- already done.** `b1` is exactly conserved, so no loop-pair creation: the string
  cannot break (rounds 18-19). The sharp distinction from QCD stands.
- **(5) Native vs overlay -- sharpened.** The bare rule is **charge-blind** (redexes depend on the edge
  multiset alone, round 5), so it cannot feel the tube on its own. The flux-tube PATH (tree geodesic) is
  native; the confining force/energy that makes it a "tube" is **irreducibly the field-energy overlay**.
- **(6) Reproducible chirality search.** The bounded reversal search now runs **live** inside
  `s4_3_dirac_mass_obstruction` (2 defect types x 2500 states by default; `EMERGENCE_FULL=1` -> 4 types x
  6000): reversal found = False, so the Weyl obstruction is tested, not just asserted.
- **Grades:** §11.1 **Vacuum state PARTIAL -> DERIVED** (the vacuum is a pure tree); **Creation/annihilation
  analogues OPEN -> REFUTED** (definitively absent -- `b1` strictly conserved, a superselection rule, like
  inverse-square is REFUTED in favor of confinement). Tally: **DERIVED 73->74, PARTIAL 121->120, OPEN
  106->105, REFUTED 3->4.**

## Porting log — round 21 (the deconfinement transition is Polya recurrence: d_s=2)

| Module | Subsection | Was | Now | Result |
|---|---|---|---|---|
| `s6_3_deconfinement_dimension` | 6.3 | added (no grade change) | — | confinement iff the substrate's walk is recurrent (d_s<=2); transition at spectral dim 2 |

Answered "what flips the keystone's confinement to Coulomb?" -- and the boundary is a classical theorem.

- **The static potential `V(L)=R(L)` grows (confining) IFF the substrate's random walk is RECURRENT.** A
  charge's field "returns" rather than escaping. By **Polya's theorem** recurrence is set by the spectral
  dimension: recurrent for `d_s <= 2`, transient for `d_s > 2`. So `d_s<2`: `R~L^(2-d_s)` grows (confining);
  `d_s=2`: `R~log L` (marginal); `d_s>2`: `R->const` (Coulomb, deconfined).
- **Measured** (spectral dim from the return probability `P0(t)~t^(-d_s/2)`; resistance by relaxation):
  1D `d_s~1.0`, `R~L` (linear, confine); 2D `d_s~2.0`, `R~log L` (marginal); 3D `d_s~2.5-3`, `R->const`
  (Coulomb, deconfined); **keystone `d_s~1.0` (tree-like), `R~L` -> CONFINING.**
- **So the keystone confines because its emergent geometry is sub-2D in transport (tree-like, recurrent
  walks); the same field theory deconfines on a >2D substrate (round 6).** Confinement here is NOT a strong
  coupling -- it is the **recurrence of the rule's own diffusion**, and the deconfinement transition sits at
  the Polya boundary `d_s=2`. (Quark confinement mapped onto a random-walk recurrence theorem: the flux
  cannot escape a recurrent geometry.)
- **Honest grade:** PARTIAL. Spectral dimensions and resistance scalings are measured (keystone natively,
  lattices as the dimensional comparison); identifying `R(L)` with the inter-charge potential uses the
  field-energy overlay, and the rule is charge-blind (round 5). **No leaf grade changed.** Tally unchanged:
  DERIVED 74, PARTIAL 120, OPEN 105, REFUTED 4.

## Porting log — round 22 (meson-meson scattering: the string-flip nuclear force)

| Module | Subsection | Was | Now | Result |
|---|---|---|---|---|
| `s4_6_meson_meson` | 4.6 | added (no grade change) | — | no long-range force between neutral mesons; short-range string-flip nuclear force; rearrangement scattering |

The free S-matrix is trivial (round 19), so the only nontrivial dynamics is between confined states. The
force between two color-neutral mesons mirrors the QCD nuclear force.

- **No long-range force; range set by the meson SIZE.** Two neutral mesons feel exactly **zero** residual
  force once their separation exceeds the reach of their flux tubes: a meson of tube length `L` interacts
  only out to `~2L` (measured: `L=2 -> range ~4`; `L=5 -> range ~10`), zero beyond. Confinement screens the
  force -- a color singlet has no long-range field -- so the inter-meson force is strictly short-range with
  a range set by the hadron size (the analog of why the nuclear force is short-ranged, not Coulombic).
- **Short-range ATTRACTION from flux-tube recombination (string flip).** Within range the four charges
  re-route their two tubes -- original `(A-Abar, B-Bbar)` vs recombined `(A-Bbar, B-Abar)`, whichever is
  shorter. When the mesons overlap, recombination lowers the energy (gain down to `~-0.9 sigma`, peaking at
  `R~L`): an attractive residual force = the **string-flip model of the nuclear force** (singlets attract by
  exchanging quarks through a tube rearrangement).
- **Scattering is REARRANGEMENT.** The recombined state is two *different* mesons (quarks swapped), so
  meson-meson scattering is dominated by rearrangement (t-channel quark exchange), not a smooth potential:
  up to ~30% of close encounters flip the pairing -- characteristic of confining theories.
- **Honest grade:** PARTIAL. NATIVE: the tree geometry / graph distances (flux-tube lengths) are measured on
  the bare-rule graph, and "no force beyond 2L" follows from tree geometry + neutrality. OVERLAY/MODEL: the
  energy = tension x tube-length and the string-flip selection use the confining-string picture; the
  scattering reading is inferred from static energetics. **No leaf grade changed.** Tally unchanged:
  DERIVED 74, PARTIAL 120, OPEN 105, REFUTED 4.

## Porting log — round 23 (attack the zigzag: E^2=p^2+m^2 and time dilation emerge, no longer assumed)

| Module | Subsection | Was | Now | Result |
|---|---|---|---|---|
| `s7_4_zitterbewegung_dispersion` | 7.4 (+7.3) | "Mass-energy relation" BORROWED; "Time dilation" BORROWED | DERIVED; PARTIAL | the relativistic dispersion + sub-luminal drift + zitterbewegung + time dilation all emerge from the zigzag |

Round 14 modelled mass as a glider zigzagging between the two native chiralities at +/-v0 but PUT IN the
relativistic velocity `v = p/sqrt(1+p^2)` by hand. Taking the zigzag as a discrete quantum walk derives it.

- **The walk.** Two chiralities at the single speed `v0=1` (rounds 13-14): a right-mover and a left-mover.
  One step = SHIFT (R hops +1, L hops -1) then a mass COIN `C=[[cos m, i sin m],[i sin m, cos m]]` mixing
  them (coin angle `m` = the chirality-flip amplitude = the irreducible Weyl->Dirac mass input, round 16).
  This is the Feynman checkerboard.
- **Dispersion (DERIVED).** In Fourier space `U(k)=diag(e^{-ik},e^{+ik}).C`, `det U=1`, so `2 cos E = tr U =
  2 cos k cos m`, i.e. **`cos E = cos k cos m` => `E^2 = k^2 + m^2`** for small `k,m` (verified to 3-4 digits).
  At `m=0`: `E=k`, a massless luminal Weyl mode. The **relativistic dispersion emerges** from two chiralities
  + one speed + a flip amplitude + unitarity.
- **Group velocity (DERIVED).** `v=dE/dk = sin k cos m / sin E = p/E`: relativistic, strictly sub-luminal for
  `m>0`, `-> v0` as `m->0` -- exactly the relation round 14 had to assume.
- **Zitterbewegung.** A single-chirality state mixes the `+/-E` bands; their interference makes the
  instantaneous velocity TREMBLE between `+/-v0` (measured) while the packet drifts at `p/E`.
- **Time dilation (PARTIAL).** The two bands sit at `+/-E(k)`, so the trembling oscillates at the gap
  `2E=2*gamma*m` in lab time (measured frequency tracks `2E` at low momentum: `0.994` vs `1.000`, `1.153` vs
  `1.153`); the proper-time rate stays at the rest value `2m`, so **`dtau/dt = m/E = 1/gamma`** -- time
  dilation from the zitterbewegung (de Broglie) clock. (Equivalently the invariant phase `Et-kx=m*tau` on
  `x=vt` gives `tau=t/gamma`.)
- **Honest grade:** "Mass-energy relation" BORROWED -> **DERIVED** (the dispersion is a clean theorem of the
  walk); "Time dilation" BORROWED -> **PARTIAL** (the clock rate `2E=2*gamma*m` is derived from the
  dispersion, but the proper-time identification is partly assumed). The quantum-walk (amplitude) structure
  is the amplitude track (round 9); the mass VALUE stays an irreducible input (round 16) -- only its
  KINEMATICS is now the Dirac equation. Tally: **DERIVED 74->75, PARTIAL 120->121, BORROWED 17->15.**

## Porting log -- round 24 (attack the continuum: the continuum limit is a random fractal tree, not a manifold)

| Module | Subsection | Was | Now | Result |
|---|---|---|---|---|
| `s1_6_continuum_fractal_tree` | 1.6 | "Continuum limits" PARTIAL | DERIVED | the continuum limit is a random fractal tree (Levy/CRT class), not a manifold |

The Hauptvermutung asks whether the substrate has a well-defined continuum limit. For the keystone the
answer is **yes -- but it is NOT a manifold.** The graph is one loop in a growing tree (`b1=1` conserved;
2-core a vanishing fraction, round 20), so its scaling limit is a random REAL tree.

- **Three diffusion dimensions**, related on any fractal by the **Einstein relation `d_s = 2 d_H / d_w`**:
  Hausdorff `d_H` (volume `N(r)~r^{d_H}`), spectral `d_s` (return prob `P0(t)~t^{-d_s/2}`), walk `d_w`
  (`<r^2>~t^{2/d_w}`). A smooth `d`-manifold gives the integer triple `(d,d,2)` with `d_s=d_H`; a fractal
  tree gives a NON-integer triple with `d_s < d_H < d_w`.
- **Measured (per seed):** `d_H ~ 2.4` (robust across seeds); `d_s` and `d_w` individually scattered by
  finite size but **co-varying so `d_s = 2 d_H/d_w` holds**, and always with the fractal ordering
  **`d_s < d_H < d_w`** -- never the manifold triple. Means `d_H~2.35, d_s~1.5, d_w~3.2`.
- **Universality class: random fractal trees (Levy / CRT).** Aldous's Continuum Random Tree -- the universal
  scaling limit of critical finite-variance branching -- has exactly `(d_H,d_s,d_w)=(2, 4/3, 3)`. The
  keystone sits in this class; `d_H` a little above 2 points to a slightly heavier-tailed branching (a stable
  tree of index `alpha = d_H/(d_H-1) ~ 1.7`), though the exact member is not pinned at finite size.
- **Hauptvermutung verdict:** a continuum limit EXISTS and is essentially unique, but it is a random fractal
  tree, NOT a Riemannian/Lorentzian manifold. **The bare rule does not smooth into Euclidean/Lorentzian
  spacetime.** A manifold phase would need the loop content (the 2-core) to dominate the large-scale
  geometry; it provably does not (`b1` conserved `=1`; 2-core sub-linear). If a manifold phase exists it must
  come from extra structure -- more loops / higher effective dimension (cf. the `d_s>2` deconfinement
  boundary, section 6) -- not from the bare keystone.
- **Honest grade:** "Continuum limits" PARTIAL -> **DERIVED** for the qualitative characterization (fractal
  tree, Einstein relation, not a manifold); the exact dimension values and the precise universality member
  carry finite-size uncertainty (+/- 0.1-0.3). All three dimensions measured natively. Tally: **DERIVED
  75->76, PARTIAL 121->120.**

## Porting log -- round 25 (the d_s=2 manifold transition: what minimal extra structure crosses it)

| Module | Subsection | Was | Now | Result |
|---|---|---|---|---|
| `s1_6_manifold_phase_transition` | 1.6 | added (no grade change) | -- | LOCAL loop-closure crosses d_s=2 into a manifold; random loops give mean-field; neither is native |

The follow-on to round 24: the bare continuum is a sub-2D fractal tree; what MINIMAL extra structure crosses
the d_s=2 boundary (the deconfinement/manifold threshold of section 6) into a manifold, and does the rule
supply it? The bare rule conserves b1=1 (tree), so it does not -- loops must be added, and HOW matters:

- **LOCAL loop-closure** (add edges between nodes at small tree-distance r -- e.g. close r=2 'elbows' into
  triangles): `d_s` rises smoothly and **CROSSES 2** at modest density (r=2 hits `d_s~2` at `p~0.5`), the
  **diameter stays large** (`~N^{1/d}`, polynomial volume growth), and the range tunes the target dimension
  (`r=2 -> d_s~2`, `r=3 -> d_s~2.8`). A finite-dimensional, MANIFOLD-LIKE phase.
- **RANDOM long-range edges**: `d_s` shoots up without bound (3.8, 5.2, ...) and the **diameter COLLAPSES**
  toward `log N` (~8) -- the small-world / MEAN-FIELD phase (infinite-dimensional), NOT a manifold.
- **So crossing `d_s=2` is easy; landing in a MANIFOLD (finite-dim, large diameter) vs MEAN-FIELD (collapsed
  diameter) depends on LOCALITY.** A manifold needs local connectivity against a metric. The bare keystone
  already supplies the metric (graph distance); the minimal manifold-building structure is local loop-closure
  against it -- **one local rule addition**. But the bare rule does not perform it (`b1` stays 1), so the
  manifold phase is reachable IN PRINCIPLE, not natively -- consistent with round 24 (bare = fractal tree).
- **Honest grade:** PARTIAL. The `d_s` crossing and the manifold-vs-mean-field separation (via the diameter)
  are clearly measured; the result is constructive (the phase diagram of an added local rule) and conditional
  on non-native structure, so **no native physics leaf is claimed.** Tally unchanged.

## Porting log -- round 26 (does the string-flip attraction bind a tetraquark? yes -- a shallow molecule, by recurrence)

| Module | Subsection | Was | Now | Result |
|---|---|---|---|---|
| `s4_6_tetraquark_binding` | 4.6 | added (no grade change) | -- | the round-22 attraction binds a meson molecule, guaranteed by recurrence (d_s<2); shallow, not compact |

Follow-on to round 22: is the short-range string-flip attraction deep enough to BIND a four-quark state? The
answer is a theorem -- and it is the SAME recurrence that confines the quarks (round 21).

- **The criterion (Economou-Cohen / the Polya boundary).** A short-range attraction binds for ARBITRARILY
  WEAK coupling iff the zero-energy Green's function `G(0)=sum_t P_return(t)` DIVERGES, iff the walk is
  recurrent, iff `d_s<=2`. If `G(0)` converges (transient, `d_s>2`) there is a THRESHOLD depth instead.
- **Measured** (keystone `d_s~1.5` vs 3D `d_s=3`): keystone `G(T)` keeps GROWING (recurrent) -> threshold
  `1/G(0) -> 0` (no threshold); 3D `G(T)` SATURATES -> finite threshold `~0.34`. At a weak well (`V0=0.2`)
  the **keystone BINDS** (`E_b>0`) while the **3D lattice does not** -- the keystone binds where a manifold
  cannot.
- **So the residual string-flip attraction ALWAYS binds a meson molecule on the keystone -- guaranteed by
  recurrence, the very property that confines the quarks.** But `d_s~1.5` sits just below the marginal `2`,
  so `G(0)` diverges only slowly and the binding energy is small for moderate coupling: the bound state is a
  loosely-bound, spatially extended **MOLECULE** (two color singlets, with the two flux-tube pairings mixed
  = a genuine four-quark state in the molecular regime), **not a compact tetraquark** -- which would need a
  stronger short-range attraction or a lower spectral dimension.
- **Honest grade:** PARTIAL (conditional). The recurrence => no-threshold-binding step is rigorous and
  natively measured (`G(0)` on the bare-rule graph); the attraction itself is the round-22 overlay and the
  binding is shallow, so **no native physics leaf is claimed.** Tally unchanged.

## Porting log -- round 27 (into QFT: the free scalar propagator -- no massless scalar, the IR divergence is confinement)

| Module | Subsection | Was | Now | Result |
|---|---|---|---|---|
| `s11_2_propagator_and_spectral_density` | 11.2 (+11.1) | "Green-function analogues" OPEN; "Correlation functions" OPEN; SUB 11.2 OPEN | DERIVED; PARTIAL; SUB PARTIAL | the free scalar Green's function and its IR structure, all fixed by d_s |

Into the QFT layer. The natural free field is the Gaussian theory of the rule's own Laplacian (round 3); its
propagator is the resolvent `G_m(x,y) = <x|(L+m^2)^{-1}|y> = sum_t e^{-m^2 t} p(x,y;t)`, and everything about
it is fixed by the spectral density, which the spectral dimension controls: `rho(E) ~ E^{d_s/2-1}`.

- **Spectral density** (heat-kernel trace `P_return(t)~t^{-d_s/2}`): `d_s~1.4-1.5` so `rho(E)~E^{-0.25}`
  **DIVERGES as E->0** -- an IR pile-up of low-energy modes (because `d_s<2`).
- **No free massless scalar.** The on-diagonal propagator `G_m(x,x)=sum_t e^{-m^2 t}P_return(t)` **DIVERGES
  as `m->0`** (the massless sum is `sum_t P_return`, divergent -- recurrence, round 26), with the
  spectral-dimension scaling `G_m(x,x) ~ (m^2)^{d_s/2-1} = m^{d_s-2}` (measured exponent consistent with
  `d_s` up to truncation). **A massless free scalar does not exist on this substrate; the IR divergence IS
  confinement.**
- **The regularized massless two-point function is the LINEAR confining potential.** On the tree (`b1=1`) the
  effective resistance equals the graph distance (unique path), so `R(r) ~ r` -- a rising string, not a
  Coulomb tail. So "the massless two-point function" is confining.
- **A mass gaps the IR.** For `m>0` the resolvent is finite (`sum_t e^{-m^2 t}P_return` converges); the
  massive field has a finite correlation length / mass gap. As `m->0` the gap closes and the IR divergence
  returns. A genuinely propagating massless scalar would need `d_s>2` -- the manifold phase (round 25).
- **Honest grade:** "Green-function analogues" OPEN -> **DERIVED** (the FREE scalar Green's function and its
  IR structure are computed natively from the Laplacian heat kernel on the bare-rule graph); "Correlation
  functions" OPEN -> **PARTIAL** (the free two-point function done; interacting/higher-point correlators
  remain OPEN); SUB 11.2 OPEN -> PARTIAL. Tally: **DERIVED 76->77, PARTIAL 120->121, OPEN 105->103.**

## Porting log -- round 28 (the RG flow of d_s: a scale-invariant fractal IR fixed point, no dimensional flow)

| Module | Subsection | Was | Now | Result |
|---|---|---|---|---|
| `s11_4_running_spectral_dimension` | 11.4 | "Scale dependence" PARTIAL; "Fixed points" OPEN; SUB OPEN | DERIVED; PARTIAL; SUB PARTIAL | the running d_s settles to a scale-invariant fractal IR fixed point ~1.5; loops are RG-relevant |

Opening the renormalization section. The free propagator (round 27) is fixed by `rho(E)~E^{d_s/2-1}`, so the RG
question is how `d_s` RUNS with scale -- the "dimensional flow" of asymptotic safety / CDT. Probe with the
diffusion time (`t ~ 1/mu^2`: small `t` = UV, large `t` = IR), reading the local exponent
`d_s(t) = -2 d log P_return / d log t`.

- **Controls (the method does not manufacture a flow):** a 1D chain gives `d_s(t)~1` and a 2D grid `d_s(t)~1.8`
  (finite-size-suppressed) **flat across all scales** -- the flatness is the test: a constant for
  scale-invariant geometries.
- **The keystone flow:** a non-universal UV crossover at short scales (the bare lattice / branch-point
  structure) settles to a **SCALE-INVARIANT fractal IR fixed point `d_s ~ 1.5`** across a decade. So the
  long-distance physics sits at a fractal RG fixed point (the random-tree continuum, round 24), and the bare
  rule is its own coarse-graining fixed point -- roughly seed-universal (lattice details IRRELEVANT).
  **There is NO running of `d_s` in the IR** (unlike CDT's `4 -> 2` flow); the substrate is scale-invariant.
- **Loops are an RG-RELEVANT perturbation:** the IR exponent climbs with local-loop density
  (`d_s(IR): 1.30 -> 1.52 -> 1.56` as `p: 0 -> 0.5 -> 1`). Loop structure is the relevant coupling that lifts
  the dimension. But the effect is scale-dependent and the exact loop-added exponent is window-sensitive:
  local nearest-shell loops do NOT push the IR across 2, so round 25's `d_s=2` crossing was the shorter-scale
  exponent, and a UNIFORM manifold fixed point (`d_s>2` at ALL scales) needs loops at EVERY scale. Only the
  DIRECTION (loops raise `d_s`) and the bare IR fixed point are quoted as robust.
- **RG picture:** dimensional flow from a non-universal UV to a scale-invariant fractal IR fixed point
  (`d_s~1.5`); loop-density is the relevant coupling toward the manifold fixed point past the `d_s=2`
  separatrix; lattice details irrelevant.
- **Honest grade:** "Scale dependence" PARTIAL -> **DERIVED** (running `d_s` measured with validated controls);
  "Fixed points" OPEN -> **PARTIAL** (fractal IR fixed point identified; manifold fixed point only
  multi-scale); SUB 11.4 OPEN -> PARTIAL. Tally: **DERIVED 77->78, PARTIAL 121 (unchanged), OPEN 103->102.**

## Porting log -- round 29 (referee response: does history-enriched geometry give 3+1 spacetime? No)

| Module | Subsection | Was | Now | Result |
|---|---|---|---|---|
| `s1_6_history_enriched_geometry` | 1.6 | "Effective macrovariables" OPEN | PARTIAL | all-history = small-world; locality-cutoff = marginal-2D thickened tree; NOT 3+1 |

A referee status doc proposed reaching a spatial MANIFOLD by retaining the rule's CONSUMED spokes (the rule
slides x->y->z to the diagonal x-z while severing y-z) as causal-history memory edges: `effective =
instantaneous adjacency + consumed spokes`. At one size this looks promising (1500 steps: instantaneous
`b1=1, d_s~1.4, diam~45`; all-history `b1~1150, d_s~2.4, diam~10`). This module runs the decisive test the
single size cannot settle -- the **manifold-vs-mean-field discriminator (round 25): how the DIAMETER scales
with N** (`diam ~ N^{1/d}` polynomial = manifold; `diam ~ log N` = small-world).

- **All-history is SMALL-WORLD, not a manifold.** Measured diameter exponent `b ~ 0.16` (`diam ~ log V`): the
  diameter grows only 9 -> 13 while V goes 500 -> 8000. d_s saturates near 2 (local thickening) but the
  diameter has collapsed. **Locality test:** ~83% of memory edges are local (endpoints within graph-distance
  4 -- triangle closures), but a thin tail of EARLY consumed spokes, whose endpoints drifted apart as the
  tree grew (out to distance ~20), act as long-range shortcuts. Textbook Watts-Strogatz, and UNAVOIDABLE
  (early spokes necessarily become non-local). So the single-size `d_s~2.7` is the small-world regime.
- **The locality cutoff cures the collapse -- but only to a MARGINAL-2D thickened tree, not 3D.** Retaining a
  consumed spoke only when its endpoints stay within distance D=4 restores polynomial diameter (`b ~ 0.5`).
  But a random CRT-like tree ALREADY scales `diam ~ V^{1/2}` (NOT `V`), so `b_cut ~ b_inst ~ 1/2`: the cutoff
  does NOT beat the substrate's large-scale geometry -- it only hangs local loops (`b1/V ~ 0.6`) on the tree
  backbone, lifting d_s toward the marginal 2 at SHORT scales (the round-28 scale-dependent effect). At most
  marginal-2D, decisively NOT 3D (`b=1/3`); pushing further reintroduces the drifted tail -> small-world.
- **Verdict:** the history-enrichment route does NOT derive 3+1 spacetime. Un-cut = small-world (no manifold);
  cut = marginal-2D thickened tree (large-scale still the bare random tree). The marginal-2D ceiling matches
  the substrate's `d_s=2` boundary (the same one organizing confinement and the propagator): local closure
  lifts the fractal tree at most to the `d_s=2` margin without non-local shortcuts. 3+1 Lorentzian spacetime
  and the time/causal dimension (sec10) remain OPEN.
- **Honest grade:** "Effective macrovariables" OPEN -> **PARTIAL** (effective history-geometry characterized:
  small-world / marginal-2D); the 3+1 derivation is REFUTED for this route. Overlay, not the bare rule.
  Tally: **PARTIAL 121->122, OPEN 102->101.**

## Porting log -- round 30 (the causal-set / spacetime dimension: a 4D longest-chain reading that is a FALSE POSITIVE)

| Module | Subsection | Was | Now | Result |
|---|---|---|---|---|
| `s10_1_causal_set_dimension` | 10.1 | (no native sec10 module) | added (no leaf change) | causal order is non-manifold; longest-chain "4D" refuted by interval-volume "~1D" |

After history-enrichment failed to give a 3D SPATIAL manifold, the natural next move: spacetime dimension
lives in the CAUSAL graph (the partial order of rewrite events), not the spatial slice. Each event consumes
two edges (produced by earlier events) and produces three (consumed by later events); linking
producer->consumer builds the causal DAG. Its dimension was measured TWO independent ways, each CALIBRATED on
Minkowski sprinklings of known dimension:

- **(A) Longest-chain (height):** `L ~ N^{1/d}`. Calibration recovers d=2 -> 1.86, d=4 -> 3.91. The keystone
  gives `L ~ N^{0.238}` => **apparent d ~ 4.2 -- looks like 3+1 spacetime.**
- **(B) Interval-volume:** a causal interval `[p,q]` has `V ~ ell^d`. Calibration recovers d=2 -> 1.93,
  d=4 -> 2.88. The keystone gives **`V ~ ell^{1.18}` -- intervals are CHAIN-LIKE (~1D).**
- **The two calibrated estimators DISAGREE (4.2 vs 1.2).** A faithful d-manifold requires them to AGREE; the
  disagreement is the diagnosis -- the causal order is **NON-MANIFOLD**. The picture: a wide, shallow causal
  structure (height `~ N^{1/4}` forces width `~ N^{3/4}`) built from nearly-parallel ~1D causal chains. The
  longest-chain "d~4" is purely the global ASPECT RATIO (a tall fan of thin chains gives `L ~ N^{1/4}`); the
  interval-volume sees the truth -- the sparse, tree-like (`b1=1`) causal structure carried from the spatial
  graph. So **3+1 spacetime is NOT recovered from the causal graph either**; the same `b1=1` sparsity that
  makes the spatial slice a fractal tree makes the causal order a non-manifold fan of chains.
- **Grade:** characterization (cautionary) -- the causal-set dimension is now measured and calibrated; the
  causal/Lorentzian continuum (a faithful manifold with `V ~ ell^d` matching `L ~ N^{1/d}`) is NOT present
  and stays OPEN. No leaf status change (the sec10.1 PARTIALs already reflect partial, non-manifold spacetime
  structure); module attached to 10.1 as evidence. **Tally unchanged.** Caught a flaky 2-point longest-chain
  calibration mid-round (fixed to a 4-point fit; the interval-volume is the decisive, well-calibrated estimator).

## Porting log -- round 31 (the TRUE entanglement entropy: a real area law S ~ |boundary|)

| Module | Subsection | Was | Now | Result |
|---|---|---|---|---|
| `s9_5_entanglement_entropy_area_law` | 9.5 (+13.5) | "Entanglement entropy" OPEN | PARTIAL | Gaussian-field entropy obeys the area law S ~ |boundary| |

The holography module (`s13_5`) had measured only the GEOMETRIC boundary (`|dR| ~ |R|^0.7`) and explicitly
left undone "a true entanglement entropy (Gaussian-field / Casini-Huerta, which needs spectral linear
algebra)." This round does it in pure Python (a small Jacobi eigensolver), so it runs at modest n.

Method (Casini-Huerta / Bombelli-Koul-Lee-Sorkin): the free scalar is the oscillator system with `K = L +
m^2`; the Gaussian ground state has `X = <phi phi> = (1/2)K^{-1/2}`, `P = <pi pi> = (1/2)K^{1/2}`, and the
region entropy uses the eigenvalues `nu >= 1/2` of `sqrt(X_A P_A)`.

- **Calibration (clean):** a 1D chain single-edge cut has boundary = 1 for ANY interval length -> `S` is
  CONSTANT (area law); recovered `S ~ 0.25-0.30` flat. A 2D grid ball has a GROWING perimeter -> `S` grows at
  fixed `S/|dA|` (area law, growing boundary = the holographic case); recovered `S` `0.58 -> 2.04` as `|dA|`
  `12 -> 32`.
- **Keystone result:** the true entanglement entropy obeys the area law `S ~ |dA|`. Decisive demonstration via
  SINGLE-EDGE cuts (a tree property -- one edge severs an arbitrarily large subtree, boundary = 1 regardless
  of `|A|`): `S` is CONSTANT in `|A|` (fitted slope `dS/dln|A| ~ 0`, e.g. `-0.03`) at every mass. So `S`
  tracks the BOUNDARY, not the volume -- now shown for the actual field entropy, not just geometry.
- **IR divergence in the COEFFICIENT:** the per-edge entropy grows `~ ln(1/m^2)` as `m -> 0` (`S` mean
  `0.13 -> 0.28` from `m^2 = 0.05 -> 0.005`). The round-27 IR divergence (massless scalar = confinement)
  reappears here as a logarithmically divergent area-law coefficient -- NOT as critical (`log|A|`) or
  volume-law growth. The area-law SCALING is mass-independent.
- **Placement in the dimension split:** because `S ~ |dA|` and the geometric boundary scales sub-extensively
  (static side, `~|R|^0.7`), entanglement entropy is a STATIC / boundary-counting probe (a 6th measurement on
  the static side), not a dynamic-transport one. The grid contrast is the `b1=1` signature: a 2-manifold's
  growing perimeter makes `S` grow, while a tree subtree's `O(1)` boundary makes `S` saturate. The area law
  holds either way.
- **Grade:** "Entanglement entropy" OPEN -> **PARTIAL** (the entropy is computed and the area law established
  and calibrated; the precise bulk exponent and exact `m->0` law remain loosely pinned); also attached to
  `13.5` Holography as corroboration of "Area-law behavior". **Tally: PARTIAL 122->123, OPEN 101->100.**

## Porting log -- round 32 (monogamy of mutual information: the free scalar is NOT holographic)

| Module | Subsection | Was | Now | Result |
|---|---|---|---|---|
| `s13_5_monogamy_mutual_information` | 13.5 | "Entanglement geometry" CONJECTURE | REFUTED | free-scalar entanglement violates MMI -> no classical RT bulk |

A sharp holographic diagnostic, using the round-31 Casini-Huerta machinery. States with a classical
Ryu-Takayanagi (minimal-surface) bulk dual satisfy the MONOGAMY of mutual information (Hayden-Headrick-
Maloney): `I3(A:B:C) = I(A:B)+I(A:C)-I(A:BC) = S_A+S_B+S_C - S_AB-S_AC-S_BC + S_ABC <= 0`. Generic free
fields VIOLATE it (`I3 > 0`). So the sign of `I3` tests holographic (RT-geometric) vs merely area-law.

- **The tempting hypothesis (REFUTED):** the keystone's `b1=1` TREE geometry is exactly what MERA /
  holographic tensor networks live on, so maybe the keystone entanglement is monogamous (holographic).
- **Result:** it is NOT. Computed `I3` for nearby tripartitions and for the cleanest signal -- HUB
  tripartitions (three subtree branches off one high-degree node): **1D chain (a tree) violates MMI (I3>0,
  every config); 2D grid violates MMI (I3>0, every config); keystone violates MMI** -- hub tripartitions give
  `I(A:B) ~ 0.1-0.15` and `I3 ~ +0.02..+0.08 > 0`, a substantial, unambiguous violation.
- **Resolution:** the keystone free scalar is a generic free field -- area law YES (`s9_5`), RT geometry NO.
  The area law is necessary but not sufficient for holography, and the keystone fails the sufficient (MMI)
  test exactly as the chain and grid do. The tree GEOMETRY is MERA-friendly, but holography is a property of
  the STATE; the rule's natural state is a free Gaussian field, not a holographic tensor network.
- **Grade:** "Entanglement geometry" CONJECTURE -> **REFUTED** (monogamy violated for the natural free-scalar
  realization -> no consistent minimal-surface bulk); sharpens "Limits of the analogy" (area law yes, RT no).
  **Tally: CONJECTURE 29->28, REFUTED 4->5.**

## Porting log -- round 33 (entanglement negativity: quantum entanglement is nearest-neighbor -> the area-law origin)

| Module | Subsection | Was | Now | Result |
|---|---|---|---|---|
| `s9_5_entanglement_negativity` | 9.5 | "Correlation structure" OPEN | PARTIAL | quantum entanglement nearest-neighbor; classical correlation long-ranged |

Mutual information counts quantum entanglement AND classical correlation; the logarithmic NEGATIVITY E_N is a
genuine entanglement monotone (zero on separable mixed states), so the two together separate quantum from
classical. For a Gaussian state the partial transpose is Gaussian: E_N comes from the partial-transposed
symplectic eigenvalues `nu~ = sqrt(eig(sigma_xx . D sigma_pp D))` (D flips B's momenta), `E_N = sum_{nu~<1}
-ln(nu~)`. Reuses the round-31 Casini-Huerta machinery; pure-Python Jacobi.

- **Validation (1D chain, gapped):** adjacent sites entangled (`E_N ~ 0.29`), every separated pair `E_N = 0`
  EXACTLY while `I` stays positive and decays (`0.09, 0.04, ...`) -- "entanglement sudden death" with distance.
- **Keystone:** quantum entanglement is **essentially NEAREST-NEIGHBOR** -- single-site `E_N` is `~0.26` at
  d=1 (100% of pairs), a small tail at d=2 (`~0.017`, only ~38% of pairs, from the irregular branching, growing
  as `m -> 0`), and dead by d=3. Classical correlation (`I`) decays far more slowly (`0.24, 0.05, 0.015,
  0.004`). Adjacent subtrees across one edge are strongly entangled (`E_N ~ 0.32`, every pair).
- **The microscopic ORIGIN of the area law:** because entanglement lives on the BONDS (nearest-neighbor edges),
  a region is entangled with the rest only across its boundary EDGES, so `S ~ |dA|`. The negativity explains
  why the round-31 entropy counts boundary edges -- each boundary edge carries one nearest-neighbor entangled
  bond. The same `b1=1` sparsity that makes boundaries small (single-edge subtree cuts) makes the entanglement
  bond-local; the long-range mutual information is purely CLASSICAL correlation.
- **Grade:** "Correlation structure" OPEN -> **PARTIAL** (entanglement-vs-correlation range structure computed
  and calibrated, giving the area law a microscopic origin; precise d=2 tail loosely pinned). **Tally: PARTIAL
  123->124, OPEN 100->99.**

## Porting log -- round 34 (a Page-curve analogue: radiation entropy rises and FALLS = unitarity)

| Module | Subsection | Was | Now | Result |
|---|---|---|---|---|
| `s10_5_page_curve` | 10.5 | "Information paradox analogues" CONJECTURE | PARTIAL | Page curve rises and falls (unitarity); cold area-law vs scrambled volume tent |

The Page curve is the signature of unitary evaporation: the radiation entropy rises, peaks at the Page time,
falls to zero. The mechanism is purity -- for a global pure state `S(A) = S(complement)`, so as a region grows
from empty to full, `S` rises from 0 and returns to 0. The SHAPE encodes the entanglement: a VOLUME-law
(scrambled) state gives the maximal symmetric Page TENT peaking at half-system; an AREA-law state gives a
SUPPRESSED curve set by the boundary (horizon). Radiation grows in geometric (BFS) order; `S(A)` via the
round-31 Casini-Huerta machinery (using `S(A)=S(complement)` to keep every matrix `<= N/2`).

- **Calibration (the cold curve encodes the horizon dimension):** 1D chain (d=1) is FLAT (boundary=2, no Page
  peak); 2D grid (d=2) is a rounded TENT peaking near half (perimeter grows then shrinks).
- **Keystone COLD (ground state):** a Page curve that RISES AND FALLS (unitarity), peaking near half-system
  (like the 2D grid -- Hausdorff dim ~2.3 gives geometric regions a growing boundary), but irregular (the
  ramified tree) and with AREA-LAW height (set by the horizon, not the volume).
- **Keystone HOT (scrambled volume-law pure state = ground state of a dense random Hamiltonian):** the maximal
  symmetric Page TENT, peaking at half-system, height ~11x the cold curve.
- **Reading:** both rise and fall -- unitarity (information return) holds regardless; only the AMOUNT of
  entanglement differs. The keystone's natural (cold) state radiates AREA-LAW entropy (a suppressed Page curve
  set by the small tree horizons); a scrambled state radiates VOLUME-LAW entropy (the full tent). The same
  `b1=1` sparsity that gives the area law and bond-local entanglement keeps the cold horizon small.
- **Caveat:** this is the Page-curve STRUCTURE (entanglement of a pure state's growing subsystem), not a
  dynamical evaporation with horizon emission; island / QES dynamics are not computed.
- **Grade:** "Information paradox analogues" CONJECTURE -> **PARTIAL** (Page-curve rise-and-fall demonstrated
  with the cold/scrambled contrast calibrated; dynamical evaporation not done). **Tally: CONJECTURE 28->27,
  PARTIAL 124->125.**

## Porting log -- round 35 (the Page PROCESS: a quench shows the keystone is LOCALIZED and does not thermalize)

| Module | Subsection | Was | Now | Result |
|---|---|---|---|---|
| `s5_3_quench_localization` | 5.3 | (characterization, no leaf change) | added | modes LOCALIZED; quench entanglement area-law-capped (no volume-law thermalization) |

The static Page curve (round 34) grew a region on a frozen graph; this turns it into a Page PROCESS -- the
field evolves in TIME. Prepare a product (ultralocal) state, switch on the keystone couplings at t=0, evolve
unitarily. The Gaussian covariance evolves exactly: `sigma(t)=M(t) sigma0 M(t)^T`, `M(t)=exp(t[[0,I],[-K,0]])`,
from the eigendecomposition of `K=L+m^2`. Entanglement via the Renyi-2 entropy `S2(A)=(1/2)ln det(sigma_A)`
(determinant-based -> pure-Python-friendly).

- **(1) LOCALIZATION (inverse participation ratio `sum_i |psi(i)|^4`):** the keystone's random tree (degree
  disorder, ~57% pendants) ANDERSON-LOCALIZES its Laplacian modes -- mean mode covers only ~30 of ~800 sites
  (~5 of ~110 at small N), with ~1/4-1/3 of modes strongly localized (<5 sites). A 1D chain is the opposite:
  modes are EXTENDED (cover ~2/3 of all sites, 0% strongly localized).
- **(2) NO VOLUME-LAW THERMALIZATION:** after the quench, a 1D chain's entanglement grows and saturates to a
  VOLUME law (`S2_sat` grows with `|A|` -- extended modes carry entanglement ballistically, full
  thermalization). The keystone's `S2_sat` saturates FLAT -- essentially independent of region size (area-law
  cap), only a few times the cold ground state -- because LOCALIZED modes cannot transport entanglement.
- **Reading:** the keystone field is a LOCALIZED, non-thermalizing system; the local tree dynamics cannot
  scramble information into a volume of entanglement, hot or cold. This is the dynamical face of the `b1=1`
  sparsity (area law + bond-local entanglement + mode localization), and the OPPOSITE of black-hole fast
  scrambling -- the volume-law (hot) Page tent of round 34 is UNREACHABLE by the keystone's own dynamics (it
  needed an artificial non-local Hamiltonian).
- **Caveat:** the free scalar is Gaussian (integrable) -> a GGE not a true thermal state; the point is
  geometric -- the SAME free field reaches volume-law on a CHAIN but is localization-capped on the keystone TREE.
- **Grade:** characterization (no leaf change -- the field's localization refines "Thermalization" PARTIAL);
  module attached to 5.3. **Tally unchanged.**

## Porting log -- round 36 (level-spacing statistics: the spectrum is POISSON with massive degeneracy = localized, not chaotic)

| Module | Subsection | Was | Now | Result |
|---|---|---|---|---|
| `s5_3_level_spacing_statistics` | 5.3 | (characterization, no leaf change) | added | keystone spectrum POISSON (<r>~0.39, no level repulsion) + ~1/4-1/3 exact degeneracy => localized/integrable |

The spectral confirmation of round 35's localization, using the canonical quantum-chaos diagnostic. Sort the
Laplacian eigenvalues and measure the Oganesyan-Huse gap ratio `r_n = min(s_n,s_{n+1})/max(s_n,s_{n+1})` (no
unfolding needed). Chaotic/delocalized => level repulsion, `<r>~0.536` (GOE), no degeneracies. Integrable/
localized => uncorrelated levels, `<r>~0.386` (Poisson), symmetry-forced degeneracies allowed.

- **Gap ratio:** keystone `<r>~0.39-0.43` (-> Poisson 0.386 as N grows), NOT GOE. A random 3-regular graph
  (chaotic reference) gives `<r>~0.53`, matching a GOE matrix. => keystone spectrum is POISSON: localized/
  integrable, no level repulsion.
- **Massive exact degeneracy:** ~25-35% of keystone eigenvalues are EXACTLY degenerate (chaotic graph: ZERO --
  level repulsion forbids it). Structural: `lambda=1` carries huge multiplicity (~292 at N~1500) from the
  antisymmetric modes of the ~57% pendant pairs; golden-ratio eigenvalues (2.618, 0.382 from two-pendant
  "cherry" motifs) and `2+-sqrt(3)` (longer pendant paths) recur -- the molecular-orbital spectrum of the
  tree's repeating motifs.
- **Spacing shape:** keystone has many tiny gaps (`P(s<0.1)~0.36`, no repulsion); chaotic graph almost none
  (`~0.01`, strong repulsion).
- **Reading:** three independent spectral signatures -- Poisson gap ratio, massive exact degeneracy, clustered
  spacings -- all say the keystone is LOCALIZED/INTEGRABLE, not chaotic. Spectrum-side confirmation of round 35
  (no scrambling, no thermalization), tracing to the `b1=1` sparse, pendant-heavy, motif-repeating tree.
- **Grade:** characterization (no leaf change -- confirms the localization/integrability already in 5.3);
  module attached to 5.3. **Tally unchanged.**

## Porting log -- round 47 UPGRADE (s1_7_coherent_mesh: three new diagnostics sharpen the d=2 MANIFOLD GATE result)

The round-47 module (`sec01_raw_wolfram_hypergraph_facts/s1_7_coherent_mesh.py`) was upgraded in-place
with three additional diagnostics that were missing from the initial port. No keystone result changes;
no leaf grade changes; tally remains at 366. Section modules: 74 -> 85 (rounds 37-47 had already been
ported in the sessions between STRUCTURE.md entries; this entry records the r47 module upgrade only).

**(C) SAME-TREE DIVERGENCE.** Starting from the **identical Eden base tree** and adding the same edge
density via two methods at each q value (coherent frame-aligned plaquettes vs graph-distance-2 elbow
shortcuts, a.k.a. random), coherent closure drops `d_w` monotonically `2.2 -> 1.9` (toward manifold)
while random closure raises it `2.2 -> 2.5` (fat-tree direction) -- **diverging in opposite directions
from the same base at every q**. Random always has HIGHER cycle density `c` yet WORSE `d_w`, isolating
the topological TYPE of loop (flat plaquette vs irregular shortcut) as the decisive variable, not the
count.

**(D) LEVEL-SPACING STATISTICS (Oganesyan-Huse `<r>`; Poisson=0.386 localized, GOE=0.536 delocalized):**
- **Coherent mesh:** `<r>~0.56` -- GOE/Wigner-Dyson, delocalized modes, zero spectral degeneracy. A
  2D manifold background that thermalizes and diffuses normally; the opposite spectral phase from the
  keystone.
- **Frame+random (same base tree):** `<r>~0.38` -- sub-Poisson, MORE localized than the keystone
  despite `c=1.35` and 0% pendants. The wrong kind of loops clusters modes more tightly than a tree.
- **Keystone:** `<r>~0.39-0.46` (finite-size) -- Poisson/localized, confirming rounds 35/36.
- **Reading:** spectral phase and geometry agree exactly. Only frame-coherent closure both delocalizes
  the spectrum AND brings `d_w -> 2`; random closure fails both tests simultaneously.

**(Honest d_s caveat added.)** The `d_s` of the coherent mesh sits ~0.10-0.15 below the true 2D
lattice at `N~500` (Eden boundary bias: ~4% pendant-like boundary nodes vs 0% for the lattice), and
this gap is persistent across `N=100-1600`. Both converge toward `d=2` with N but the mesh converges
more slowly. The finite-size-safe signals -- `d_w~2` and the three dimensions *agreeing* -- are the
claimed result; `d_s=d_H~2` is confirmed in trend, not pinned to 3 significant figures at `N~500`.
The `d=3` note was also updated: `c=1.18` vs lattice `c=1.63` at `N~500`, boundary effects worse in
3D; round 48 needs `N>1500` before the d=3 result can be quoted confidently.

**Locality restatement (docstring and verdict):** the rule is local *in execution* (each node consults
only its own coordinate's neighbours), but `Z^d` is a globally-consistent flat coordinate system --
equivalent to assuming a flat background metric. The updated title makes this explicit: "local in
execution, globally flat frame." This is the precise meaning of "scaffolded."


## Porting log -- round 48 (d=3 coherent mesh: Z^d mechanism scales but d_s blocked by Eden boundary effects -- PARTIAL)

| Module | Subsection | Was | Now | Result |
|---|---|---|---|---|
| `s1_8_manifold_d3` | 1.6 | (characterization, no leaf change) | added | d=3 Z^d mechanism confirmed on robust signals; d_s lags -- PARTIAL |

The round-47 Z^2 manifold gate PASSES; round 48 asks whether the same Z^d mechanism (local Eden cluster
growth + coherent frame plaquette closure) scales to d=3. It does on every N-independent control, but the
3D Eden boundary causes d_s to lag so severely that a clean PASS is not achievable at reachable N.

**What scales (confirmed):**
- **Same-tree divergence (d=3):** starting from the identical Z^3 Eden base tree, coherent closure drops
  `d_w` (2.41→1.79 at q=1, toward manifold) while random closure raises it (2.42→2.74 at q=1,
  fat-tree direction) -- exactly the same-direction split as in d=2. The active-ingredient result is
  dimension-free.
- **Level-spacing (d=3):** Z^3 coherent mesh `<r>~0.50` (GOE-leaning/delocalized), Z^3 frame+random
  `<r>~0.42` (Poisson-leaning/localized) -- separated from each other and from the keystone (`~0.39-0.46`).
  Spectral phase tracks geometry in d=3 as in d=2.
- **d_w → 2:** converging across N=200..2500 (1.71→1.88), approaching normal diffusion.
- **d_H tracks the 3D lattice** at comparable N across the full tested range (d_H~2.33 at N~500 vs
  lattice 2.29; d_H~2.56 at N~2500 vs lattice 2.50).
- **q-knob:** same pattern as d=2: c rises, pendants fall, d_s/d_H grow, d_w stays ~2.

**What doesn't converge:**
- **d_s lags badly:** 2.24 at N=2500 vs lattice 2.76 (gap ~0.52, vs d=2 gap ~0.10 at same N). Cause:
  Eden boundary fraction scales as N^{-1/3} in 3D (vs N^{-1/2} in 2D) -- border pendants persist much
  longer. A clean PASS (d_s=d_H=d_w/2≈3, all agreeing) needs estimated N>>5000.
- **c lags:** 1.46 at N=2500 vs target d-1=2 and lattice 1.79. Same boundary cause.
- The three dimensions (d_s, d_H, d_w/2) disagree more than in d=2 at the same N (0.32 gap vs ~0).

**Multi-d summary:** Z^2 PASSES (all three agreeing ~2 at N~500); Z^3 PARTIAL (d_w~2, d_H~lattice,
mechanism confirmed, but d_s needs estimated N>>5000). The 'derive d' problem (round 50) is orthogonal:
even if d=3 were fully confirmed, the dimension enters via the frame rank z, not the dynamics.

**Grade: PARTIAL (characterization) -- no leaf change. Tally fixed at 366. Section modules: 85 -> 86.**

## Porting log -- round 49 (causal foliation: the +1 time dimension does NOT emerge -- needs a second scaffold)

| Module | Subsection | Was | Now | Result |
|---|---|---|---|---|
| `s1_9_causal_foliation` | 1.6 | (characterisation, no leaf change) | added | Eden DAG d_causal<2 (NOT time); CDT exact V~T^3 confirmed; +1 needs scaffold |

Rounds 47-48 established a d=2 spatial manifold. This round asks whether the +1 Lorentzian time dimension
arises naturally from the Eden growth dynamics.

**APPROACH A -- Eden growth causal DAG (birth order as physical time):** node u causally precedes v if u was
born before v AND they are spatially adjacent. RESULT: interval volume V << T^3 at every T (ratio
V/V_theory falls from 0.57 at T=2 to 0.06 at T=10); d_causal < 2 << 3. The growth frontier is a 1D
boundary curve, not a 2D spatial volume; the causal cones are 2D blobs, not 3D. Birth order is SPATIAL
TIME (which region grew first), not LORENTZIAN TIME. Compare: keystone native causal graph (round 30)
gives d_causal ~1.2; Eden DAG gives similar sub-2D behaviour.

**APPROACH B -- CDT-style explicit foliation (Z^2 mesh × Z time):** stack n_t copies of the Z^2 coherent
mesh with causal edges (v,t)->(v,t+1) and (w,t+1) for spatial neighbours w. RESULT: the measured V(T)
matches the EXACT theoretical formula V(T)=sum_{s=0}^T b(min(s,T-s)) with b(r)=1+2r(r+1) (the 2D
Manhattan ball), which is asymptotically V~T^3/6 (d_causal=3). The local log-log slope rises toward 3
as T grows (pre-asymptotic crossover at small T gives slope ~1.3-2.8 before reaching the T^3 regime).
The coherent-mesh spatial slice tracks the perfect lattice closely (Eden boundary causes small V deficits:
V_mesh/V_lattice ≈ 0.82-0.92).

**THE MAIN FINDING:** the +1 time dimension does NOT emerge from the Eden growth. Physical time requires an
explicit temporal scaffold -- CDT-style stacking with forward causal edges -- just as physical space
required the Z^2 spatial frame (round 47). The complete construction is Z^(d+1) imposed in d+1 stages.
**Grade: PARTIAL (characterisation). No leaf changes. Tally fixed at 366. Section modules: 86 -> 87.**

## Porting log -- round 50 (frame-free dimension selection: local short-cycle preference helps but hits a real d_s ceiling)

| Module | Subsection | Was | Now | Result |
|---|---|---|---|---|
| `s1_10_frame_free_dimension` | 1.6 | (characterisation, no leaf change) | added | local diamond-closing improves on every diagnostic but d_s plateaus ~1.35-1.40, never converges |

The central round-50 question, asked directly: can dimension be SELECTED by a purely local, frame-free
rule -- zero coordinates, zero embedding, nothing but graph topology?

**THE RULE -- diamond-completion growth:** when adding a new node, with probability q attach it to TWO
existing nodes already at graph-distance 2 (closing a 4-cycle via local distance-2 lookups only); else
ordinary tree growth. This approximates round 47's coherence (flat-plaquette closure) via a frame-free
heuristic: prefer short cycles using only local topology.

**UNCAPPED -- a NEW failure mode (preferential attachment):** high-degree nodes have far more distance-2
partners, so they get picked disproportionately, creating a rich-get-richer hub-formation feedback loop.
Max degree climbs 11->23 (q: 0->0.9, N=500) and the DIAMETER SHRINKS as q rises (21->11) while the lattice
at comparable N has diameter ~37. N-scaling confirms small-world collapse: diameter tracks `log(N)`
(5.3->7.3 as N: 200->1500) far more closely than `sqrt(N)` (14->39). A distinct failure mode from round
46's fat-tree or random-shortcut small-world -- here the bias is intrinsic to unweighted distance-2
candidate selection.

**DEGREE-CAPPED (deg_cap=4) -- the motivated fix:** removes the hub bias by construction (still
frame-free; a scalar cap, not a coordinate). Fixes the catastrophic failures: no hub formation, diameter
no longer collapses, cycle density climbs smoothly 0.00->0.72, pendant fraction falls smoothly 46%->6%,
`d_w` stays near 2 (2.1-2.5) across the full sweep -- genuine progress over every prior frame-free attempt.

**BUT `d_s` hits a real ceiling.** Tested over a 16-20x range in N (300 to 5000-6000), `d_s` is FLAT
(1.43, 1.36, 1.37, 1.35, 1.34 -- spread 0.09) while `d_H` keeps climbing (1.87->2.40) over the same range.
This is qualitatively different from round 48's d=3 lag, which rose monotonically with N: here the three
estimators DIVERGE from each other as N grows rather than converging together -- a genuine structural
ceiling, not a finite-size gap awaiting more compute.

**Two corroborating diagnostics:**
- **Same-tree divergence:** diamond-preferential closure gives consistently HIGHER `d_s` and `c` than
  degree-capped RANDOM closure at every q (e.g. `d_s=1.41` vs `1.15` at q=0.6) -- local short-cycle
  preference is doing genuine work, just not enough alone.
- **Level-spacing:** the capped diamond mesh gives `<r>~0.49`, genuinely INTERMEDIATE between the
  keystone (Poisson, `~0.39-0.46`, localized) and the true frame-coherent mesh (GOE, `~0.56`,
  delocalized) -- partially delocalized, neither fully localized nor fully manifold-like.

**Why it falls short (the physical reason):** round 47's coordinate-based closure only closes plaquettes
that are automatically FLAT (zero holonomy by construction of the frame). The diamond rule has no way to
verify flatness -- it can prefer SHORT cycles but not FLAT ones, since flatness is not testable from graph
distance alone without an embedding. This sharpens round 47: the missing ingredient is specifically zero
holonomy, which appears to require either non-local consistency checking or a carried per-edge connection
variable -- itself a (much more minimal) form of scaffold, not bare topology.

**Grade: PARTIAL -- a genuine, four-diagnostic-consistent characterisation of real progress (fixes
catastrophic failure modes, improves every metric) AND a real ceiling (d_s never converges). No leaf
change. Tally fixed at 366. Section modules: 87 -> 88.**

## Porting log -- round 51 (the genus obstruction: b1=1 forces sphere topology; frame-free flatness is not verifiable)

| Module | Subsection | Was | Now | Result |
|---|---|---|---|---|
| `s1_11_genus_obstruction` | 1.6 | (characterisation, no leaf change) | added | new keystone corollary (b1=1 => genus=0 forced) + rigorous resolution of round-50 conjecture |

Round 50 conjectured that a frame-free rule can prefer SHORT cycles but cannot verify FLAT ones. This round
makes "flatness" exact via combinatorial map theory -- the GENUS of a rotation-system embedding, computed by
face tracing (V-E+F=2-2g), pure integer combinatorics with NO coordinates.

**Tool + calibration (all exact, no fitting):** trees -> genus 0 for any rotation; open 2D lattice with true
planar rotation -> genus 0 (F = unit-square count); torus with toroidal rotation -> genus 1 EXACTLY; same
torus graph scrambled -> genus 18 (rotation-dependent, respects the bound g <= b1/2).

**NEW KEYSTONE COROLLARY (zero computation):** for a connected graph F>=1, and F = 1 + b1 - 2g, so
g <= b1/2. The keystone conserves b1=1 EXACTLY => g <= 0.5 => **g=0 FORCED under ANY rotation whatsoever.**
The keystone spacetime is a TOPOLOGICAL SPHERE no matter how it is embedded -- no rotation, however
adversarial, can give it a handle; it can never host a torus or genus-g 2-manifold. Confirmed computationally
(genus=0 exactly for real keystone instances, all seeds). A new result complementary to the sub-2D fractal
dimensions: b1=1 locks BOTH the dimension (sub-2D) AND the topology (sphere).

**ROUND-50 RESOLUTION (quantitative):** the natural frame-free local rotation is INSERTION ORDER (order each
node's edges were added; no coordinates). Tested on round 47's coherent mesh, which IS planar (its true
coordinate rotation gives genus 0 at every N):
- TRUE planar rotation: genus 0 exactly.
- INSERTION-ORDER rotation: genus grows with N (65, 181, 397 at N=200,500,1000), reaching ~88-91% of the
  maximum b1/2 -- essentially INDISTINGUISHABLE from a RANDOM rotation (genus 181 insertion vs 190 random at
  N=500). Even on a provably FLAT graph, local edge order carries almost NO flatness information: its
  embedding is as crumpled as random. Flatness is GLOBAL; a frame supplies exactly the missing global rotation.

**ROUND-50 DIAMOND MESH DIAGNOSED:** under insertion-order rotation the diamond mesh's genus grows LINEARLY
in N at a FIXED fraction ~0.70-0.72 of b1/2 (0.705, 0.707, 0.714, 0.723 across N=300..3000) -- a constant,
non-vanishing handle DENSITY. A manifold needs handle density -> 0; here it is pinned constant, so the object
retains extensive handles and cannot become a 2-manifold. This is an INDEPENDENT confirmation of round 50's
d_s ceiling (~1.35-1.40) from pure topology, using no spectral machinery -- two windows (genus and d_s) on
the same ceiling.

**Grade: PARTIAL -- a new exactly-computed topological diagnostic yielding a new keystone corollary and a
theorem-backed resolution of round 50's open conjecture. No leaf change. Tally fixed at 366. Section modules:
88 -> 89.** Natural next step (round 52): a carried per-edge discrete connection to check holonomy locally.

## Porting log -- round 52 (the discrete connection reduces to a per-vertex FRAME, not bare topology; b1=1 unifies the keystone)

| Module | Subsection | Was | Now | Result |
|---|---|---|---|---|
| `s1_12_connection_reduction` | 1.6 | (characterisation, no leaf change) | added | three exact reductions proving the connection = a coordinate frame; b1=1 unifies keystone topology+dimension |

Round 51 named the obstruction (flatness = genus-0; insertion-order rotation = random). This round tests
Kirk's idea -- carry a discrete connection (a group element per edge), close only trivial-holonomy loops --
and asks whether it reduces to bare topology or to the frame we were avoiding. Answer: it reduces, provably,
to ONE COORDINATE LABEL PER VERTEX (a frame). Three exact results:

1. **Fundamental-basis reduction (verified):** flatness on ALL cycles <=> flatness on a spanning-tree
   fundamental basis of just `b1 = E-V+1` cycles (one per cotree edge). Composite cycles are edge-set XOR
   (Z-linear) combinations, so they inherit flatness. Confirmed: zeroing the b1 fundamental cycles makes all
   fundamental AND all composite (XOR) cycles flat. Only b1 checks are ever needed -- the "cheap/local" part
   the connection idea hoped for is real.
2. **Coboundary reduction (the catch):** a flat Z_2 connection <=> edge signs are a coboundary
   `s(u,v)=c(u)c(v)` for a vertex labelling `c:V->{+-1}`. Verified (random signs generically NOT flat;
   coboundary signs always flat). So a flat connection carries EXACTLY one bit per VERTEX up to gauge -- a
   vertex labelling in disguise, not independent per-edge data.
3. **Planarity upgrade:** Z_2 tracks only orientation flips; 2D flatness needs turning (Z_4) AND zero net
   translation around every loop. By (2) that flat connection is gauge-equivalent to one label per vertex in
   the group's space = a 2D COORDINATE. Demonstrated: the coordinate-adjacency growth rule (= round 47's
   coherent mesh) gives genus 0 under the true planar rotation at every N; without coordinates (insertion
   order) the same graph reads ~89-94% of b1/2 (crumpled). Flat connection = consistent coordinates = a frame.

**CONCLUSION:** the holonomy constraint DOES reduce to bare graph data -- but to a per-vertex coordinate frame,
NOT pure topology. Carrying a connection does not escape the scaffold; it IS the scaffold re-encoded. No
frame-free route to flatness exists, which is why rounds 46/50 hit the ceiling and round 47 needed a frame.

**KEYSTONE UNIFICATION (b1=1 ties the whole 46-52 arc into one fact):** the keystone has b1=1, so (by result 1)
exactly ONE fundamental cycle -> trivially flat with one check -> genus 0 (round 51's forced sphere). But a
plane of N sites needs an EXTENSIVE flat cycle space (b1 ~ N); b1=1 forever forbids 2D extent (the sub-2D
dimension, rounds 1/24/46). So the keystone's sphere topology AND its sub-2D dimension are ONE fact -- b1=1
gives a single trivially-flat loop and forbids the extensive flat cycle space a plane requires. Flatness is
free precisely because there is almost nothing to be flat.

**Grade: PARTIAL -- three exactly-verified reduction results closing the "can we avoid the scaffold?" question
in the negative, and unifying the keystone's topology and dimension under b1=1. No leaf change. Tally fixed at
366. Section modules: 89 -> 90.**

## Porting log -- round 53 (the condensation route executed: frame-free reaches d_s~2 but pins at max genus; coherence is global)

| Module | Subsection | Was | Now | Result |
|---|---|---|---|---|
| `s1_13_condensation_route` | 1.6 | (characterisation, no leaf change) | added | executes handoff Route 1; frame-free local objective reaches d_s~2 + extensive cycles but maximal genus = crumple, not manifold |

Responds to the handoff document's recommended experiment (Route 1+2: unframed graph + local holonomy/face
objective + topology penalties, "can rank emerge?"). Three design corrections established first, then the
corrected experiment run.

**Correction 1:** "reward trivial holonomy" is MAXIMISED by a TREE -- trees have b1=0, no holonomy
constraints, so every connection on them is flat (verified). Flatness is necessary but a lattice (b1/V~0.87)
and a tree (b1/V=0) are BOTH flat; flatness does not discriminate. The target is FACES, not flatness.

**Correction 2:** dimension is NOT coordination number. Degree-4 Z^2 lattice has d_s~1.98; a degree-4 RANDOM
regular graph has d_s~3.05 (verified) -- same degree, different dimension. Geometry (short coherent faces),
not degree, sets d. So "rank competition" cannot be read off the degree.

**The corrected experiment (frame-free, no coordinates):** random sparse start; MCMC edge moves at inverse
temperature beta scored by a LOCAL face-coherence objective (reward each edge for bordering ~2 short faces =
the manifold interior-edge condition; penalise hubs/pendants); degree FREE. RESULT: cycles ARE built (b1/V
climbs to ~1.9, d_s passes through 2.0) -- the two coarse manifold signatures are reachable frame-free. BUT
genus density PINS near 0.99 (maximal) and diameter collapses to single digits (small-world). Side by side at
matched d_s~2 and matched cycle density: frame-free MCMC (genus_dens~0.99, diam~9, crumple) vs coordinate
coherent mesh (genus_dens~0 planar, diam~36, TRUE manifold). SAME dimension and cycle density, OPPOSITE
topology.

**Diagnosis (round 52 confirmed dynamically):** coherence = genus 0 = flat connection = consistent vertex
labelling = COORDINATES. A LOCAL objective counts faces through an edge but cannot enforce ONE global
orientation for all of them -- a global constraint invisible locally. So local face-reward builds faces glued
incoherently (max genus), not a flat tiling. CONSEQUENCE: LOCAL frame-free objectives (handoff Routes 1, 6)
provably cannot select coherence -- they hit the genus ceiling. Only GLOBAL selection principles over the
whole configuration (Route 2 action/measure, Route 4 matter viability, Route 5 coarse-graining) can suppress
the crumple, because coherence is a GLOBAL property. The recommended local-holonomy experiment is exactly the
one that cannot work, now measured.

**Grade: PARTIAL -- executes the handoff's Route-1 experiment with three corrections and delivers a sharp
measured negative that confirms round 52 dynamically and narrows the remaining routes to global selection.
No leaf change. Tally fixed at 366. Section modules: 90 -> 91.**

## Porting log -- round 54 (Route 2 executed: a GLOBAL planarity action selects a genuine 2-manifold -- first frame-free manifold selection)

| Module | Subsection | Was | Now | Result |
|---|---|---|---|---|
| `s1_14_global_action` | 1.6 | (characterisation, no leaf change) | added | global planarity gate + face reward -> genus-0 manifold (d_s->2, diam~sqrtN), NO coordinates |

Round 53 proved coherence is GLOBAL (local objectives crumple at max genus). Route 2 makes the action's
constraint global: MCMC over edge moves where edge ADDS are gated by a HARD, EXACT planarity check
(Boyer-Myrvold via networkx -- first third-party dependency in a section module, sanctioned; graceful
degradation if absent), triangles rewarded at temperature T, degree free (cap 6), NO coordinates anywhere.

**RESULT -- ROUTE 2 SUCCEEDS at d=2 where Route 1 failed:** output is a certified planar 2-complex --
genus EXACTLY 0 (not proxied), extensive faces (b1/V ~ 0.9-1.3), d_s rising toward 2 with N (1.46 -> 1.67
across N=80..320; 1.75 at N=500 in sandbox), and the DIAMETER GROWS ~sqrt(N) (8 -> 14+), the manifold
signature Route 1's crumple (diam pinned ~9, genus density 0.99) never had. One change -- local -> global --
flips the topology from maximal genus to zero.

**The Euler-gate shortcut REFUTED:** gating adds only by the necessary condition E <= 3V-6 saturates the
budget with NON-planar tangles (planar=False everywhere, diam ~5, crumple). The bound constrains edge
COUNT; planarity constrains edge STRUCTURE (no K5/K3,3 minors) -- structure IS coherence. The full global
test is irreplaceable; there is no cheap counting proxy.

**NOT a frame (verified 3 ways):** planarity is a forbidden-minor property (Kuratowski), checkable with
zero coordinates and assigning none; it CAPS dimension rather than fixing it (path d_s~1, star d_s~0.8,
lattice d_s~1.8 are ALL planar -- the face reward selects the top of the cap); the emergent dimension is
selected by (global topological cap)+(face maximisation), not input as a coordinate rank. Genuinely
different mechanism from rounds 47-49.

**The honest catch + the d=3 door:** planarity is d=2-specific (the CHOICE of forbidden-minor family
smuggles in the 2). No "3D planarity" exists (every graph embeds in R^3). BUT: LINKLESS EMBEDDABILITY
(no two disjoint cycles linked; Petersen-family forbidden minors incl. K6; Robertson-Seymour-Thomas) is
the genuine 3D-flavoured finite-forbidden-minor constraint, with edge bound E <= 4V-10. Verified: 3D
lattices sit comfortably inside it (E/(4V-10)~0.6) and K6 violates it (15>14, correctly excluded).
Poly-time decidable in principle; NO practical library test exists. The d=3 experiment (linkless gate +
face/volume reward) is named, edge-bound-verified, blocked only on implementation.

**Scaffold hierarchy after this round:** frame (coords/vertex, r47) >> planarity (one global
forbidden-minor CHOICE, r54) >> nothing (impossible for local rules, r52/53). Dimension is demoted from
"a coordinate system you install" to "a topological exclusion rule you choose". Making the exclusion rule
ITSELF emerge (Route 4 matter viability: does physics prefer the planar- or linkless-selected phase?) is
the remaining question.

**Grade: PARTIAL -- first frame-free manifold selection; the strongest positive result of the 46-54 arc.
No leaf change. Tally fixed at 366. Section modules: 91 -> 92.**

## Porting log -- round 55 (minor-universality of 3D lattices: the forbidden-minor route to d=3 CLOSED BY THEOREM)

| Module | Subsection | Was | Now | Result |
|---|---|---|---|---|
| `s1_15_minor_universality_d3` | 1.6 | (characterisation, no leaf change) | added | 5^3 lattice contains K6 minor (linkless proposal REFUTED); K_m minors for all m (constructive) -> NO forbidden-minor rule can select d=3 |

The d=3 pre-flight check round 54 skipped: round 54 verified 3D lattices satisfy the linkless EDGE BOUND
(E<=4V-10) but never checked the MINORS.

**RESULT 1 -- REFUTATION (exact certificates):** the 5^3 cubic lattice CONTAINS a K6 minor -- found by a
randomized greedy branch-set grower, verified by an exact certificate checker (6 disjoint connected branch
sets, all 15 pairs edge-adjacent). K6 is Petersen-family, so 3D lattices of side >=5 are NOT linklessly
embeddable. The round-54 linkless gate would have FORBIDDEN the lattices it was meant to select. The edge
bound was necessary-only, and misleading. Control: no K5 minor found in a 2D grid (planar), correct.

**RESULT 2 -- THEOREM (constructive):** for every m, a large enough 3D cubic lattice contains a K_m minor.
Explicit tower-and-arms construction: m towers at x=3i, each pair (i,j) gets its own z-level carrying an
arm along y=1; box (3m-2) x 2 x C(m,2), a subgraph of any k^3 lattice with k >= max(3m-2, C(m,2)).
Certificate-verified for m = 6,7,8,9,10 (boxes 480-2520 vertices, all valid).

**COROLLARY (impossibility):** any minor-closed family containing all 3D lattices contains every K_m,
hence EVERY finite graph. No forbidden-minor rule of ANY kind -- linkless, knotless, or otherwise -- can
select d=3. Closed by theorem, not implementation. **The 2D/3D asymmetry, precise:** 2D grids stay
minor-sparse forever (planar); 3D grids are MINOR-UNIVERSAL. This is exactly why round 54's mechanism
worked at d=2 and could never have generalised.

**RESULT 3 -- the surviving constraint type, named + calibrated:** the d=3 constraint must be
NON-minor-closed. Candidate: BALL-GROWTH CAP (|B(r)| <= C r^alpha, equivalently diameter >= c N^{1/alpha}).
Measured profiles: 2D/3D lattices and even the keystone tree grow polynomially, while the round-53 crumple
SATURATES the whole graph by r~8 (|B(8)|=N, the expander signature). A growth cap excludes the crumple,
admits d=1,2,3 alike (dimension-AGNOSTIC), and is not minor-closed (contraction speeds growth) -- exactly
what the theorem demands. Growth-cap + face/volume reward as a d=3 selector is the named next experiment.

**Scorecard:** round 54's d=2 result STANDS; its d=3 proposal is REFUTED with a theorem; the replacement
constraint type is identified with calibrated evidence. The methodology working as designed.

**Grade: PARTIAL. No leaf change. Tally fixed at 366. Section modules: 92 -> 93. Pure Python (exact
combinatorial certificates, no third-party deps).**

## Porting log -- round 56 (the growth-cap dial: dimension FACTORS into extent / transport / coherence)

| Module | Subsection | Was | Now | Result |
|---|---|---|---|---|
| `s1_16_growth_cap_dial` | 1.6 | (characterisation, no leaf change) | added | d_H = alpha (one-real-number dial); d_w~2 free at alpha=2; coherence does NOT come (structural gap) |

The round-55 continuation: MCMC with short-cycle reward subject to a polynomial ball-growth cap
|B(r)| <= C r^alpha -- dimension-agnostic, non-minor-closed, one real number, no coordinates. Predictions
registered before running: dial vs plateau vs failure.

**Enforcement (the r53 lesson recurring, then fixed):** naive endpoint-only cap checks LEAK (final audits
showed 35-85% of nodes violating -- third nodes' geodesics reroute over cap). Fixed: endpoint caps with
early-abort BFS (the cap bounds its own check cost) + a GLOBAL diameter floor diam >= c N^{1/alpha} via
double-sweep BFS per add + periodic audit-and-repair. Final audit ~2% for alpha >= 2. An unaudited cap is
not a cap.

**RESULT 1 -- THE DIAL:** d_H tracks alpha essentially exactly (2.07 / 2.62 / 2.99 at alpha = 2.0 / 2.5 /
3.0; uncapped control = the crumple, d_H ~ 4). Coarse dimension is tunable by ONE real number, non-integer
values included. Scaffold hierarchy: frame (r47) >> forbidden-minor choice (r54) >> ONE EXPONENT (r56) --
the weakest scaffold yet. Feasibility boundary: alpha = 1.5 infeasible (even trees grow ~r^2).

**RESULT 2 -- TRANSPORT FREE AT alpha=2:** d_w = 1.99 at N = 300 and 600 -- NORMAL DIFFUSION, the first
frame-free instance in the program (fat-tree 3.4, diamond mesh ~2.4, crumple breaks the estimator).

**RESULT 3 -- COHERENCE DOES NOT COME, AND IT IS STRUCTURAL:** the alpha=2 object is non-planar with
insertion-rotation genus density pinned ~0.88-0.90 (crumple level; r54 planar manifold ~0), and the
d_s < d_H gap GROWS with N on audited data (0.46 at N=300 -> 0.69 at N=600). By the round-24 criterion
these are NOT manifolds: right volume scaling, right transport, wrong face structure. The cap constrains
how much sits at each radius, not how faces glue. Honest engineering limit: at N=900 the repair
over-strips (audit fails) -- pipeline limit, not physics; claims made where the audit holds (N <= 600).

**THE FACTORIZATION (the round's contribution):** emergent dimension is three problems, not one --
EXTENT (d_H): solved cheap, one dial. TRANSPORT (d_w=2): free at alpha=2. COHERENCE (d_s=d_H, genus->0):
the irreducible core -- supplied by planarity at d=2 (r54), provably unsuppliable topologically at d=3
(r55), by any local rule (r52/53), and NOT by growth caps (here). Remaining question, sharpened: what
fixes alpha and what supplies coherence at d=3 -- both point at Route 4 (matter viability): run existing
physics on the dial's phases vs the r54 coherent manifold at matched d_H, ask whether the matter sector
distinguishes them.

**Grade: PARTIAL. No leaf change. Tally fixed at 366. Section modules: 93 -> 94.** Pure Python except one
planarity check (networkx, graceful degradation).

## Porting log -- round 57 (Route 4 executed: coherence invisible to free matter; the confinement transition sits on the dial at alpha=2)

| Module | Subsection | Was | Now | Result |
|---|---|---|---|---|
| `s1_17_matter_viability` | 1.6 | (characterisation, no leaf change) | added | Gaussian matter cannot distinguish coherence at matched d_H; R_eff confinement transition crosses the dial at alpha=2, pinning alpha<=2 |

Route 4 from the roadmap, reframed by rounds 54-56: does the MATTER SECTOR distinguish coherence (r54
planar manifold vs r56 capped complex at matched d_H), and does physics prefer an alpha? The battery: ONE
Jacobi eigendecomposition of L per subject feeds four probes (K=L+m^2 shares eigenvectors) -- IPR
localization, Oganesyan-Huse <r>, effective-resistance profile R(d) (the round-6 confinement diagnostic),
and Casini-Huerta entanglement S(ball) area-law check. Calibration: 2D lattice (N<IPR>=2.3, <r>=0.533 GOE,
R log-like slope 0.121, area law) and keystone tree (N<IPR>=31.1, strong-loc 0.39, <r>=0.458, R(d)=d
EXACTLY -- tree resistance is path length, the purest confinement signature).

**RESULT 1 -- coherence is INVISIBLE to Gaussian matter (registered prediction confirmed):** at matched
d_H~2, the coherent planar manifold and the incoherent alpha=2 complex are indistinguishable on every
free-field probe -- both delocalized (<r> ~0.50-0.53), both marginal-confining (R_eff slopes 0.24 vs
0.22), both area-law. Free matter sees DIMENSION, not GENUS. Detail: the coherent object is slightly MORE
localized (N<IPR> 13.5 vs 9.8) -- planar disorder Anderson-localizes weakly in d~2; the incoherent
object's handles are delocalizing shortcuts. Whether coherence is GAUGE-visible is the named next test: a
gauge field on a genus-g surface has 2g extra flux sectors, so Wilson loops threading handles can count
genus -- that experiment decides whether coherence is physical or aesthetic.

**RESULT 2 -- the confinement transition sits ON the dial, at alpha=2:** R_eff slope is a clean monotone
crossover 0.22 (alpha=2, marginal/2D-lattice-like, unbounded growth) -> 0.094 (alpha=2.5) -> 0.055
(alpha=3, nearly flat) -> 0.013 (uncapped, flat/deconfined). The Polya recurrence/transience boundary
appears directly on the growth-cap knob. Combined with round 6 (keystone gauge confinement BECAUSE
effective d<=2): if the phase must support confining gauge forces, alpha<=2, and alpha=2 is EXTREMAL (max
extent compatible with confinement) -- the dial's knob acquires a matter-sector selection principle.
Caveat stated: this presumes confinement is required (an empirical input from the keystone arc, not a
derivation).

**The factorization, updated:** EXTENT dialable (r56); TRANSPORT free at alpha=2 (r56); COHERENCE
invisible to free matter (r57), physical status hangs on gauge flux sectors (named next); ALPHA no longer
free -- confinement pins alpha<=2, alpha=2 extremal.

**Grade: PARTIAL. No leaf change. Tally fixed at 366. Section modules: 94 -> 95.** Pure Python except the
r54 subject build (networkx via s1_14, graceful degradation with recorded results).

## Porting log -- round 58 (gauge flux sectors CLOSE Route 4: coherence is physical, and the keystone charge is a protected qubit)

| Module | Subsection | Was | Now | Result |
|---|---|---|---|---|
| `s1_18_gauge_flux_sectors` | 1.6 | (characterisation, no leaf change) | added | deficit = b1 - rank(short cycles) = log2(GSD); coherent MELTS vs incoherent PERSISTS; keystone b1=1 = one protected flux qubit |

Round 57 left coherence invisible to free matter, hanging entirely on the gauge sector. The invariant: a
Z2 gauge field on a bare graph has 2^b1 flux sectors (sees b1, not genus -- distinguishes nothing here).
The Wilson plaquette action is LOCAL, built on SHORT cycles, and at low temperature fixes every flux in
the GF(2) span of cycles of length <= L. What survives is **DEFICIT(L) = b1 - rank_GF2(short cycles) =
log2(topological ground-state degeneracy)** -- the toric-code construction applied to arbitrary graphs.
Deficit(L) is a filtration; topology = plateau over L << system scale.

**Calibration (exact):** open lattice deficit 0; TORUS deficit EXACTLY 2 = 2g at both sizes (b1=65 on 8x8,
64 unit squares with one GF(2) dependency -> rank 63; GSD = 4 = the toric code digit for digit); r47 mesh
deficit(L<=3) = b1 = 105 (no triangles -- action must match face type) but deficit(L<=4) = 0.

**The matrix (L<=4, matched N, deficit/b1):** keystone 1/1 (1.00); r47 mesh 0/105 (0.00); r54 coherent
planar 31/161 (0.19); r56 alpha=2 43/64 (0.67); r56 alpha=3 149/190 (0.78); uncapped crumple 6/596 (0.01).

**The filtration (L = 3,4,5) -- the discriminator:** r54 coherent MELTS (52->31->10: large-face artifact,
genus-0 planar as it must be); r56 phases PERSIST (57->43->35 and 176->149->94: real protected structure,
flux glasses with extensive GSD ~ 2^{0.55 b1} even at L<=5); the crumple COLLAPSES (482->6->0: so
cycle-dense that local plaquettes trivialize everything -- it protects NOTHING).

**Two upgrades:** (1) the registered prediction deficit = rotation-genus is FALSIFIED by the crumple
(rotation-genus density ~1, gauge deficit ~0): deficit is the BETTER invariant -- embedding-free,
gauge-operational -- and exposes the r51 rotation number as an embedding artifact on dense graphs.
Coherence gets its physical definition: deficit density -> 0 with a melting filtration. (2) the capped
complexes are naturally occurring random toric codes (extensive topological GSD).

**THE KEYSTONE QUBIT:** b1=1 projects to a single conserved loop (length 5 at 400 steps; multiset
subtlety noted -- the invariant lives in the directed multiset, some simple projections collapse the loop
through a doubled edge). Deficit(L<=4) = 1: the conserved charge IS one topologically protected Z2 flux
(GSD=2, a single gauge qubit), protected at every plaquette scale below the loop length -- and the loop
grows while b1 stays 1, so at late times it is protected against ANY fixed-scale local action. The
program's central conservation law, restated in gauge language.

**ROUTE 4 CLOSED:** free matter blind to coherence (r57); gauge matter SEES it (r58). Coherence is
PHYSICAL: the absence of extensive protected flux debris, gauge-selected. Final factorization: EXTENT
dialed (r56) | TRANSPORT free at alpha=2 (r56) | ALPHA pinned <=2 by confinement, extremal at 2 (r57) |
COHERENCE gauge-selected (r58). Named next question: deficit-minimization as the SELECTION term in an
action (global, now physically motivated) to GROW coherent geometry. Honest limits: single seed per
subject; deficit(L) scale-dependent (plateau claims only); "closed" answers the coherence question, it
does not build the still-nonexistent coherent d=3 object (r55 theorem stands).

**Grade: PARTIAL. No leaf change. Tally fixed at 366. Section modules: 95 -> 96.** Pure Python except the
r54 subject build (networkx via s1_14, graceful degradation with recorded results).

## Porting log -- round 59 (deficit-selection executed: a sharp negative, a calibration correction to r56, and the residual named)

| Module | Subsection | Was | Now | Result |
|---|---|---|---|---|
| `s1_19_deficit_selection` | 1.6 | (characterisation, no leaf change) | added | deficit-0 constructible on demand but yields tree-plus-clump structures, NOT manifolds; C=3.0->3.5 cap correction; residual = uniform 2-face gluing |

The round-58 named experiment executed, with its design flaw surfaced first: "penalize deficit, drop
planarity" is ill-posed SOLO by r58's own data (the uncapped crumple has deficit 0.01; K5 is
triangle-spanned, so deficit-0 does not imply planar). Well-posed version: deficit penalty COMBINED with
the alpha=2 growth cap (pinned by confinement, r57).

**THE CAP CALIBRATION BUG (correction to r56):** the interior Manhattan ball at r=2 has 13 nodes; the
r56 constant C=3.0 allows 12 -- the cap FORBADE THE 2D LATTICE ITSELF at r=2. Measured: 55% of lattice
nodes and 45% of mesh nodes violate C=3.0; both are 0% at C=3.5. The constraint excluded its own target,
retroactively explaining part of r56's d_s undershoot. C=3.5 is the calibrated value. Also: the naive
recursive seed tree violates the cap at 17-37% of nodes; seeds are now grown UNDER the cap.

**Machinery (all audited):** add-only growth, incremental GF(2) deficit (pivot dict with FULL rollback on
rejection), post-accept local cap audit with rollback, and mandatory end audit -- incremental counters
match a full recompute EXACTLY in every run.

**RESULTS:** deficit is CONTROLLABLE (uniform proposals: glass at w_def=0 with def/b1 ~0.5, deficit -> 0
under penalty or hard gate). THE GLASS IS TRACED: targeted distance-2 proposals cut def/b1 to ~0.15
already at w_def=0 -- r56's flux glass came from its uniform proposals + removals, not capped growth per
se. BUT NO SETTING REACHES A MANIFOLD: d_s stalls at 1.1-1.3 across every deficit-0 point, nonplanar or
trivially sparse.

**THE DIAGNOSIS (edge face-degree histogram, %% of edges bordering k short faces):** the coherent mesh
puts 70% of edges at EXACTLY 2 (the manifold gluing signature); the glass peaks at 0; the deficit-0
objects are BIMODAL (54-77% at 0 = bare tree skeleton, 21-40% at 4+ = dense clumps). The deficit term
positively FAVORS clumps (a clump edge closes many mutually dependent cycles, rank coverage stays
perfect). Nothing in cap + deficit + face-count says "spread faces uniformly at 2 per edge."

**VERDICT -- the last d-specific ingredient did NOT fall.** Deficit-0 is necessary, not sufficient (trees,
clumps, K5 pockets all qualify). Planarity's job decomposes into three parts: (1) kill handles -- deficit
does it (r58); (2) kill density -- the calibrated cap does it (r56/57); (3) uniform 2-face GLUING --
nothing dimension-agnostic in rounds 46-59 does it. (3) is the true residual of the arc. Named next
question: face-degree-2 target + deficit + cap together (r53's crumple objection applied to the naive
term ALONE). Honest limits: single seed per setting; add-only moves; seed-tree gate leaks ~10%.

**Grade: PARTIAL. No leaf change. Tally fixed at 366. Section modules: 96 -> 97.**

## Porting log -- round 60 (the triple objective: selection principle SOLVED, dynamics freeze -- a glass transition)

| Module | Subsection | Was | Now | Result |
|---|---|---|---|---|
| `s1_20_triple_objective` | 1.6 | (characterisation, no leaf change) | added | the manifold is the verified ground state of gluing+deficit+cap; add-only dynamics freeze at 5x ground energy |

The r59 residual (uniform 2-face gluing) added as a proper global energy E_glue = sum_edges |facedeg-2|
to deficit + calibrated cap. Registered outcomes: success / strips (would name vertex-links) / stall.

**THE FREEZE:** the glue term kills the r59 clumps as designed (fd>=4 edges: 32% -> 3%) but growth dies
with them: b1/V collapses 0.33 -> 0.07-0.11, 80-86% of edges stay bare, d_s ~1.15. Mechanism: a completed
face POISONS its neighborhood -- nearby closures spawn incidental short cycles pushing satisfied edges
past 2, so the move is rejected. A dilute-face glass of isolated, locally-perfect faces. ROBUST to
proposal engineering: frontier proposals (closing faces ON fd=1 boundary edges, strip/patch growth by
construction) give IDENTICAL results. The stall outcome fires, mechanistically diagnosed.

**THE GROUND STATE IS THE MANIFOLD (key measurement):** E_glue/edge = 0.35 for the r47 mesh vs 1.62 for
the r56 glass and 1.81-1.82 for everything the triple dynamics reaches. With deficit 0 (r58) and cap
compliance at C=3.5 (r59), the mesh simultaneously (near-)minimizes ALL THREE terms. The failure is
KINETIC, not thermodynamic: a glass transition in the standard sense.

**VERDICT -- the 46-60 arc closes on a clean division.** WHAT to optimize: SOLVED -- gauge deficit
(handles) + calibrated growth cap (density/extent, alpha pinned by confinement) + uniform 2-face gluing:
three global, dimension-agnostic, physically motivated terms whose joint minimum is the coherent
manifold, with zero coordinates, zero forbidden-minor choices, zero d inserted anywhere. HOW to reach it:
NOT solved -- add-only local dynamics freeze at 5x ground-state energy. Named residual: a DYNAMICS
question (removal/rewiring annealing -- blocked on incremental-GF(2)-with-deletions engineering, not
physics; nonlocal moves; slow cooling), with the honest caveat that glasses can be hard for ANY dynamics.
Limits: single seed, n=150, add-only move set named as binding.

**Grade: PARTIAL. No leaf change. Tally fixed at 366. Section modules: 97 -> 98.**

## Porting log -- round 61 (annealing dynamics: r60 corrected three times; the triple's minimizers are TUBES; residual = isotropy)

| Module | Subsection | Was | Now | Result |
|---|---|---|---|---|
| `s1_21_annealing_dynamics` | 1.6 | (characterisation, no leaf change) | added | reversible add/remove with deletion-safe audits; r60 glass RETRACTED; ground-state claim OVERTURNED (tubes win); residual = aspect ratio |

**Engineering:** reversible add/REMOVE dynamics -- mask set + per-edge index, removal dE via survivor-set
GF(2) re-elimination, pivots rebuilt on accepted removals, bridges rejected, facedeg/E_glue deltas exact
negatives of adds. End audits: incremental (b1, rank, deficit, E_glue) match full recomputes EXACTLY,
every run.

**CORRECTION 1 (r60 energetics):** r60's dE_glue charged face-closing adds |dfk-2| MINUS 2 (constant -2
offset vs the true global E_glue). Harmless for its one-way freeze direction (a fortiori), fatal for
reversibility. Fixed; enforced by the E_glue audit.

**CORRECTION 2 (r60's freeze was an artifact stack):** instrumented rejections: the post-accept local
audit rejected 63% of proposals, FALSE-BLAMING new edges for the seed tree's pre-existing ~10% cap
violators (the r59 leak). Fix at source: a PATH seed (|B(r)|=2r+1, compliant at every radius, zero leak).
With it, cap audits read 0.00 and the freeze VANISHES: even fixed-T dynamics reaches E_glue/edge 0.16,
deficit 0. The glass-transition story is RETRACTED.

**CORRECTION 3 (r60's ground-state claim is FALSE):** the dynamics builds objects at E_glue/edge
0.16-0.17 with 86-88% of edges at EXACTLY fd=2 -- strictly better than the mesh (0.35, 70%) -- at
deficit 0, planar, cap-legal. The mesh is NOT the minimum of glue + deficit + cap(floor).

**THE TUBE RESULT (the r60-registered strip mode, refined):** the minimizers have d_H 0.8-1.3, diam
37-70 at n=150, yet closed-vertex-link fraction 0.73-0.74 vs the mesh's 0.50 and width E/diam 4-7 vs
11.5: thin TUBES -- locally genuine 2-manifolds (saturated vertex stars), globally rolled quasi-1D.
Boundary is expensive; a ribbon minimizes boundary per edge; NOTHING constrains aspect ratio (the r56
cap bounds diameter only from below).

**VERDICT:** STANDS -- every objective term (deficit r58, calibrated cap r59, glue r59/60). RETRACTED --
the glass transition and mesh-as-ground-state. NEW POSITIVE -- the dynamics works, and the triple
objective selects LOCAL 2-MANIFOLDNESS frame-free; the isolated residual is ISOTROPY. **Round 62,
named:** diameter CEILING diam <= c' N^{1/alpha} alongside the floor (the isotropy sandwich, one
exponent, zero d inserted): does glue + deficit + floor + ceiling select the isotropic 2D patch?
Limits: single seed per setting; n=150; closed-link is a conservative interior proxy; tree-seed regime
superseded rather than repaired.

**Grade: PARTIAL. No leaf change. Tally fixed at 366. Section modules: 98 -> 99.**

## Porting log -- round 62 (the isotropy sandwich: a feasibility theorem, an infeasibility diagnostic, and quad-lattice-grade isotropic selection)

| Module | Subsection | Was | Now | Result |
|---|---|---|---|---|
| `s1_22_isotropy_sandwich` | 1.6 | (characterisation, no leaf change) | added | cap PINS the ceiling (C=3.5 forbids triangulated interiors); at the feasible ceiling the dynamics matches the quad lattice column for column |

**FEASIBILITY THEOREM (constraint-set consistency):** under C=3.5, |B(2)| <= 14 admits the quad lattice
(13) and FORBIDS the triangulated lattice (19); measured audits 0.00 vs 0.58. Cap-legal isotropic patches
are QUAD-type with diam ~ 2 sqrt(N): the ceiling coefficient is PINNED >= ~2 by the choice of C. Lower
ceilings define EMPTY target sets. Corollary: triangle-rich manifolds were never reachable inside this
cap; the target was always the quad mesh.

**THE OVER-SQUEEZE SIGNATURE:** pushing toward an empty target (ceil 14 < the forced ~21, w_iso=5)
grinds diameter to 16-17 while ALL local invariants degrade together (deficit 0 -> 6-9, E_glue/edge
0.16 -> 0.54-0.66, closed-link 0.73 -> 0.30, planarity breaks). Distinct from kinetic freezing (r61:
acceptance collapse with invariants intact): a usable INFEASIBILITY DIAGNOSTIC.

**THE RESULT AT THE FEASIBLE CEILING:** ceiling as an energy term E_iso = w_iso * max(0, d_est - ceil)
(the path seed starts at diam ~ n; a hard gate would deadlock; early contraction chords are worth
~ -w_iso * excess/2 against their +5 glue+deficit cost). At cceil >= the forced value the dynamics lands
on the quad-lattice column: Eg/edge 0.16-0.20 vs 0.17, deficit 0-2 vs 0, fd2 85-88% vs 83%, diam 20-23
vs 21, closed-link 0.69-0.77 vs 0.69, width 10.7-12.2 vs 12.6. The r61 tube (width 4-7, diam 37+) is
GONE. First frame-free, dimension-agnostic selection of ISOTROPIC 2D structure.

**RESIDUAL, bounded:** d_s 1.22-1.32 vs the reference lattice's OWN finite-size 1.73 (d_H 1.49-1.58 vs
1.69) -- a 0.4-0.5 spectral gap, candidate cause the 6-7% fd=3 defect edges scattering the walk. Named
next: defect census + longer anneals + N-scaling toward the lattice's finite-size line.

**The constraint stack is now COMPLETE and internally consistent:** extent (alpha) | density (C, which
pins cceil) | handles (deficit) | gluing (fd-2) | aspect ratio (the sandwich) -- each one
dimension-agnostic, physically motivated term; zero coordinates, zero forbidden-minor choices, zero d
inserted anywhere. Limits: single seed; n=150; ceiling acts on the double-sweep estimate.

**Grade: PARTIAL. No leaf change. Tally fixed at 366. Section modules: 99 -> 100.**

## Porting log -- round 63 (the d=3 sandwich: cubic-grade 3-complex reached, but dimension now enters TWICE and the target is boundary-dominated)

| Module | Subsection | Was | Now | Result |
|---|---|---|---|---|
| `s1_23_dim3_sandwich` | 1.6 | (characterisation, no leaf change) | added | aligned (alpha=3, k=4) reaches the 6^3 reference column on extent/gluing; misaligned (k=2) builds 2D sheet -- k=2(d-1) coupling has teeth |

**THE HONEST COST (stated first):** the r62 2D result ran on (alpha, k) = (2, 2) with only ONE cap
exponent inserted. d=3 needs (3, 4): dimension now enters the objective TWICE -- cap exponent AND
face-degree target -- coupled by k = 2(d-1). One integer expressed twice, still far weaker than a
coordinate frame, but the "zero d inserted" purity of r62 is SPENT. Said up front because a referee sees
it instantly.

**CALIBRATION -- the reference is WEAK at this size:** 6^3 cube (N=216) has cap audit 0.00, deficit 0,
but only 44% of edges at the interior value fd=4, closed-link-at-4 just 0.30, d_s/d_H 2.39/2.25. The cube
is mostly SURFACE at N=216; "success = match this column" is a low bar, and at this N a genuine
3-manifold is not instrument-distinguishable from a thick slab.

**RESULTS (path seed, exact audits, reproduced on clean extract):** aligned annealed -- b1/V 1.34 (ref
1.50), width 38.8 (ref 36.0), closed4 0.31 (ref 0.30), diam 13, d_H 2.07 (ref 2.25): cubic-grade BULK on
extent metrics. BUT deficit 11 (uncovered contraction-chord handles) and a 17% fd=5-6 OVERSHOOT tail (the
symmetric |fd-k| penalty tolerates over-stacking). Fixed-T -- deficit 0, closed4 0.44, no overshoot, but
under-dense (b1/V 1.02) and slab-ish (diam 19, width 22.9): a schedule TRADE (bulk vs cleanliness),
neither end a manifold. MISALIGNED (k=2, alpha=3) -- 79% at fd=2, closed-link-at-2 0.63, d_H 1.93: a
crumpled 2D SHEET filling the 3D ball. The k=2(d-1) coupling is physical: alpha alone cannot raise
dimension.

**RESIDUALS, numbered:** (i) ~17% fd-overshoot defects (fix: asymmetric penalty); (ii) deficit-11 handle
debris under annealing (fix: cold cleanup phase); (iii) d_s gap ~0.6 (vs 0.4-0.5 in 2D). NOT CLAIMED: a
3D manifold. CLAIMED: a cubic-grade 3-complex matching a boundary-dominated reference on extent/gluing,
plus a demonstrated two-slot dimension dial. r55 minor-universality NOT contradicted (route is
non-minor-closed by design).

**DECISIVE TEST NOT YET RUN:** N-scaling (512, 1000). If d_s climbs toward 3 and the interior fd=4
fraction grows as boundary shrinks, the frame-free 3D result stands. If d_s sticks ~1.8-2.0 while the
cube's own d_s climbs, the defects are thermodynamic and the honest headline is "cubic-grade complex with
irreducible defect density," not a manifold. N=216 cannot answer this.

**Grade: PARTIAL. No leaf change. Tally fixed at 366. Section modules: 100 -> 101.**

## Porting log -- round 64 (the N-scaling gate REFUTES the r63 3D-manifold claim on structural grounds; corrects r63's test design)

| Module | Subsection | Was | Now | Result |
|---|---|---|---|---|
| `s1_24_dim3_scaling_gate` | 1.6 | (characterisation, no leaf change) | added | (3,4) defect density FLAT in N and effort while a cube's interior FILLS -- thermodynamic obstruction; r63 3D claim refuted; 2D stands |

**Two corrections to r63's framing (before trusting any result):** (1) "d_s -> 3" is DEAD ON ARRIVAL --
a PERFECT cube reads d_s 2.37/2.39/2.53/2.54 at 5^3..8^3 (N=125..512), barely moving and nowhere near 3;
compare grown objects to the cube's OWN point at matched N, never to the integer. (2) "d_s falls
monotonically with N" (grown 1.79->1.53->1.41) is STEP-CONFOUNDED -- a starvation control at N=512 moved
d_s 1.41->1.69 (larger-N runs were under-annealed at fixed steps/node); the d_s-vs-N trend is RETRACTED
and the verdict rests only on step-independent structural metrics.

**The structural kill (unconfounded):** three defect metrics are FLAT in N and in annealing effort while
the cube's interior measure RISES:
- closed-link-at-4: grown 0.31/0.28/0.29 vs cube 0.30/0.36/0.42 (0.56 at 8^3)
- fd overshoot (5-6): grown 17%/15%/19% vs cube 0%
- gauge deficit: grown 11/12/10 vs cube 0

The grown object keeps a HIGH raw fd=4 fraction (58-61%, above the cube) but a LOW N-independent
closed-link fraction: edges reach coordination 4 without organizing into closed vertex stars -- a
locally-4-ish globally-disordered SPONGE, not a filling 3-complex. Doubling the N=512 anneal left
closed-link 0.29 and overshoot 18%: thermodynamic, not kinetic. Mechanism: the symmetric |fd-4| penalty
prices overshoot = underfill, so the dynamics buys cheap 4s by tolerating overshoot and frustration pins
stars open; the 3D defect channel (fd can reach 5,6,7) is wider than 2D's (fd=3 only, 4-7%, non-scaling).

**Scope:** REFUTED -- the r63 protocol (symmetric penalty, annealed 2->0.2, single seed) yields a 3D
manifold. NOT REFUTED -- that some protocol could (asymmetric penalty + cold handle-cleanup, both
untested). **Contrast with 2D:** the (2,2) stack matched the quad-lattice column INCLUDING closed-link
(0.69-0.77 vs 0.69) with small non-scaling defects; the same machinery fails at (3,4) with ~18% flat
defects. A real dimensional asymmetry, consistent with (not proof of) r55's minor-universality intuition.

**Grade: PARTIAL (negative result). No leaf change. Tally fixed at 366. Section modules: 101 -> 102.**

## What "starting the process" delivered, and what remains

**Done this pass:** the full document-0 skeleton with every node graded and verified-consistent with
v8.1; the implementation library wired in; the monolith bundled and mapped (63/64); the on-disk
section mirror generated; the renderer/dispatcher/scoreboard; and **rounds 1-2 porting** (4 native experiments re-verified; 42 subsections run native code; DERIVED 50->56).

**Remaining (the actual build-out):** continue porting the monolith's load-bearing experiments into
the library, section by section, each re-verified to the v8.1 standard. Next candidates: (1) the mechanics frontier is now resolved in a deep way -- round 16 found the Dirac mass
term is **not derivable** (the keystone is a chiral Weyl world; mass is an irreducible input, like the
Standard-Model Higgs). The remaining native mechanics question is whether ANY irreducible mass input, once
granted, closes §4.2/§4.3 -- which the zitterbewegung model (round 14) already shows it does. (2) §4.5
central-force / orbit tests now that the field is local and radiative; (3) the §11 topological-matter block
(optional, numpy). The classical hierarchy §1-§6 is substantially built; the deep open questions are now the
two irreducible inputs (`β` and mass/handedness) and the continuum limit. (geometry/thermo; coupling; Maxwell; mass; photon; Dirac-mass=Weyl world; confinement=one loop in a tree; mesons = unbreakable Regge strings; scattering = conserved particle number; validation: loop grows; deconfinement = Polya recurrence; meson-meson = string-flip nuclear force; zigzag => E^2=p^2+m^2 & time dilation; continuum = random fractal tree; d_s=2 manifold transition (local loop-closure crosses it); tetraquark/molecule binds by recurrence; QFT free scalar propagator (no massless scalar = confinement); RG running d_s a scale-invariant fractal IR fixed point ~1.5; history-enriched geometry NOT 3+1 (small-world / marginal-2D); causal-set dimension non-manifold (longest-chain ~4 a FALSE POSITIVE, interval-volume ~1.2); entanglement obeys an area law S ~ |boundary| (static side); monogamy VIOLATED -> not holographic; negativity: quantum entanglement is NEAREST-NEIGHBOR -- the microscopic origin of the area law; Page curve rises and FALLS (unitarity), cold=area-law vs scrambled=volume tent; r35 Page PROCESS (quench): keystone modes ANDERSON-LOCALIZED, field does NOT thermalize (quench entanglement area-law-capped, no scrambling); r36 LEVEL-SPACING statistics: the Laplacian spectrum is POISSON (<r>~0.39, no level repulsion) with ~1/4-1/3 of eigenvalues exactly degenerate (lambda=1 from pendant pairs) -- the spectral fingerprint of a localized/integrable system, decisively not quantum-chaotic.) Each port should update its grade in
`tree.py` only after a fresh re-run warrants it.
