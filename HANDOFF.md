# HANDOFF — hypergraph physics program  (read me first)

## What this is
A multi-session collaboration deriving physics from causal-invariant **hypergraph rewriting**
(the Hořava–Wolfram program). Substrate = a multiset hypergraph + a rewriting rule; the causal
graph of rewrite events is the candidate spacetime. The work is at **v8.1** (referee-corrected v8.0),
reorganized around the program's focus: reconstructing the **classical** hierarchy (Newtonian
mechanics, thermodynamics, electrodynamics) — the layer the Wolfram / causal-set literatures skip on
the way to relativity and quantum mechanics.

## The substrate (one paragraph)
World = a **multiset** of directed edges (parallel edges distinct — load-bearing). **KEYSTONE rule:**
match any directed 2-path `x→y→z`, destroy both matched edges, write `{x→z, y→x, z→w}`, `w` fresh.
Causal graph of events = candidate spacetime. Two **BORROWED** bridges: causal invariance ⇒ local
Lorentz (Gorard); reversibility ⇒ reflection positivity ⇒ quantum `i` (Osterwalder–Schrader). One
**DERIVED** charge: first Betti number `b₁ = E − V + C` (independent loops), exactly conserved.

## Current deliverables (all current, all published)
- **`emergence_tree_v0.68.zip`** — **NEW (v0.68 = v0.67 + round 64: THE N-SCALING GATE REFUTES the r63
  3D-manifold claim on STRUCTURAL grounds. The (3,4) stack's defect density is flat in N and in annealing
  effort while a cube's interior fills with N -- a thermodynamic obstruction. Also corrects r63's dead
  d_s-vs-3 test and its step-confounded d_s-vs-N trend. The 2D result STANDS. PARTIAL, negative result.
  Tally 366.)** 97 experiments + 102 modules; test->6/6.
- **HEADLINE RESULT (round 64): the r63 3D claim FAILS its own scaling gate, but not the way r63 said it
  would. TWO CORRECTIONS FIRST: (1) 'd_s -> 3' is DEAD -- a PERFECT cube reads d_s 2.37/2.39/2.53/2.54 at
  5^3..8^3, barely moving, nowhere near 3; the integer was never a reachable target, compare to the
  cube's own point at matched N. (2) 'd_s falls with N' (grown 1.79->1.53->1.41) is STEP-CONFOUNDED -- a
  starvation control at N=512 moved d_s 1.41->1.69, so larger-N runs were under-annealed; that trend is
  RETRACTED. THE ACTUAL KILL is structural and step-independent: closed-link-at-4 is FLAT (grown
  0.31/0.28/0.29 across N=216/343/512) while the CUBE's rises (0.30/0.36/0.42, 0.56 at 8^3); fd overshoot
  flat ~18% (cube 0%); gauge deficit flat ~11 (cube 0). The grown object has a HIGH raw fd=4 fraction but
  a LOW N-independent closed-link: edges hit coordination 4 without forming closed vertex stars -- a
  locally-4-ish globally-disordered SPONGE whose interior never coheres. Doubling the N=512 anneal left
  closed-link 0.29, overshoot 18%: thermodynamic, not kinetic. MECHANISM: the symmetric |fd-4| penalty
  prices overshoot = underfill, so cheap 4s are bought by tolerating overshoot and frustration pins stars
  open; the 3D defect channel (fd up to 7) is wider than 2D's (fd=3 only, 4-7%, non-scaling). CONTRAST:
  the (2,2) 2D stack matched the quad-lattice column INCLUDING closed-link (0.69-0.77 vs 0.69) with small
  non-scaling defects. Same machinery, real dimensional asymmetry, consistent with (not proof of) r55.**
  `sec01_raw_wolfram_hypergraph_facts/s1_24_dim3_scaling_gate.py` (§1.6). PARTIAL, negative result.
- **ROADMAP STATUS after round 64 -- the 3D manifold is NOT selected by the current stack; the located
  obstruction is a defect channel with two UNTESTED candidate fixes.** The (alpha,k)=(d,2(d-1)) dial and
  the whole constraint stack still stand for d=2 (r62, quad-lattice-grade, verified through scaling-style
  closed-link matching). For d=3 the symmetric fd penalty admits an irreducible ~18% overshoot/open-star
  defect density. TWO NAMED NEXT EXPERIMENTS (round 65), in priority order: (1) ASYMMETRIC PENALTY --
  price fd>k much harder than fd<k (e.g. lambda_over * max(0,fd-k) + lambda_under * max(0,k-fd) with
  lambda_over >> lambda_under), directly targeting the overshoot channel that scaling identified; rerun
  the N-sweep and check whether closed-link now tracks the cube's rising line. (2) COLD HANDLE-CLEANUP
  PHASE -- after the anneal, a T~0 removal-only sweep targeting the deficit-11 uncovered-handle debris.
  If neither closes the closed-link gap under scaling, the honest conclusion strengthens toward '3D
  coherence is not locally enforceable by cell-gluing objectives,' which would be a substantive positive
  claim about the dimensional asymmetry rather than a null. Secondary: multi-seed error bars (everything
  to date is single-seed); larger N if a cheaper diameter estimate replaces per-move double-sweep.
  **CAUTION: /home/claude/work is WIPED between sessions -- only /mnt/user-data/outputs persists. Rebuild
  by extracting the latest zip there. All modules are deterministic (seed=11) and reproduce on clean
  extract.**
- **`emergence_tree_v0.67.zip`** — superseded by v0.68.
- **PREVIOUS (v0.67 = v0.66 + round 63: THE d=3 SANDWICH -- aligned
  (alpha=3, k=4) grows a cubic-grade 3-complex from a bare path, matching the 6^3 reference on
  extent/gluing; misaligned (k=2) builds a 2D sheet, proving the k=2(d-1) coupling. NOT a manifold:
  defects quantified, decisive N-scaling test NOT yet run. PARTIAL. Tally 366.)** 96 experiments + 101
  modules; test->6/6.
- **HEADLINE RESULT (round 63): the aligned stack (alpha=3, fd target k=4) grows cubic-grade 3D bulk
  from a bare path. THE HONEST COST, first: d=3 needs the PAIR (alpha,k)=(3,4) -- dimension enters the
  objective TWICE (cap exponent AND face-degree target), coupled by k=2(d-1). One integer twice, far
  weaker than a frame, but the "zero d inserted" purity of r62 is SPENT. CALIBRATION IS WEAK: the 6^3
  reference (N=216) has only 44% of edges at the interior value fd=4, closed-link-at-4 0.30, d_s/d_H
  2.39/2.25 -- mostly SURFACE, so matching it is a LOW bar and at N=216 a real 3-manifold is not
  distinguishable from a thick slab. RESULTS (exact audits, reproduced on clean extract): aligned
  annealed -- width 38.8 (ref 36.0), closed4 0.31 (ref 0.30), d_H 2.07 (ref 2.25): cubic-grade BULK on
  extent metrics, BUT deficit 11 (contraction-chord handle debris) and a 17% fd=5-6 OVERSHOOT tail (the
  symmetric |fd-k| penalty tolerates over-stacking). Fixed-T -- deficit 0, no overshoot, but under-dense
  and slab-ish: a schedule TRADE, neither end a manifold. MISALIGNED (k=2, alpha=3) -- 79% at fd=2,
  closed-link-at-2 0.63, d_H 1.93: a crumpled 2D SHEET filling the 3D ball. The k=2(d-1) coupling has
  teeth: alpha alone cannot raise dimension. NOT CLAIMED: a 3D manifold. CLAIMED: a cubic-grade 3-complex
  matching a boundary-dominated reference on extent/gluing, plus a two-slot dimension dial. r55
  minor-universality NOT contradicted (route is non-minor-closed by design).**
  `sec01_raw_wolfram_hypergraph_facts/s1_23_dim3_sandwich.py` (§1.6). PARTIAL; no leaf changes.
- **ROADMAP STATUS after round 63 -- the constraint stack extends to 3D but the manifold claim is NOT
  yet earned.** The dial is now the pair (alpha, k) = (d, 2(d-1)): extent (alpha) | density (C=3.5) |
  handles (deficit) | gluing (fd=k) | aspect ratio (sandwich) | cell type (k). THE DECISIVE NEXT
  EXPERIMENT (round 64), gating the 3D claim: N-SCALING at (3,4) to N=512 and 1000. Measure whether (a)
  d_s climbs toward 3 and (b) the interior fd=4 fraction grows as the boundary shrinks -- against the
  cube's OWN finite-size d_s line at each N (the cube reads 2.39 at 216, not 3). If both climb, the
  frame-free 3D result stands and the 46-64 arc closes. If d_s sticks ~1.8-2.0 while the cube's climbs,
  the defects are THERMODYNAMIC and the honest headline is "cubic-grade complex with irreducible defect
  density," a real result but not a manifold. N=216 CANNOT answer this. Secondary, only after N-scaling:
  the asymmetric-penalty fix for overshoot; a cold handle-cleanup phase for the deficit debris; multi-seed
  statistics. **CAUTION for the next session: /home/claude/work is WIPED between sessions -- only
  /mnt/user-data/outputs persists. Rebuild the tree by extracting the latest zip there. v0.67 was itself
  rebuilt this way from v0.66 + the round-63 module source; the module is deterministic (seed=11) and
  reproduced its documented numbers exactly on clean extract.**
- **`emergence_tree_v0.66.zip`** — superseded by v0.67.
- **PREVIOUS (v0.66 = v0.65 + round 62: THE ISOTROPY SANDWICH -- a
  feasibility theorem (the cap PINS the ceiling), an infeasibility diagnostic (structure-shedding vs
  freezing), and the first frame-free selection of ISOTROPIC 2D structure: the dynamics matches the quad
  lattice column for column. Module 100. PARTIAL. Tally 366.)** 95 experiments + 100 modules; test->6/6.
- **HEADLINE RESULT (round 62): the ceiling enters as ENERGY E_iso = w_iso*max(0, d_est - ceil) (path
  seed starts at diam ~ n; hard gate deadlocks; early contraction chords worth ~ -w_iso*excess/2 against
  their +5 glue+deficit cost). FEASIBILITY THEOREM: under C=3.5, |B(2)|<=14 admits the quad lattice (13)
  and FORBIDS the triangulated lattice (19; audits 0.00 vs 0.58) -- cap-legal isotropy is QUAD-type with
  diam ~ 2 sqrt(N), so the ceiling coefficient is PINNED >= ~2 by the choice of C; lower ceilings are
  EMPTY targets. Corollary: triangle-rich manifolds were never reachable inside this cap. OVER-SQUEEZE
  SIGNATURE: pushing toward the empty target (ceil 14, w_iso=5) grinds diam to 16-17 while ALL local
  invariants degrade together (deficit 0->6-9, Eg/edge 0.16->0.54-0.66, closed-link 0.73->0.30,
  planarity breaks) -- distinct from kinetic freezing (r61: acceptance collapse, invariants intact): a
  usable INFEASIBILITY DIAGNOSTIC. AT THE FEASIBLE CEILING the dynamics lands on the quad-lattice column
  (Eg/edge 0.16-0.20 vs 0.17; deficit 0-2 vs 0; fd2 85-88% vs 83%; diam 20-23 vs 21; closed-link
  0.69-0.77 vs 0.69; width 10.7-12.2 vs 12.6). The r61 tube (width 4-7, diam 37+) is GONE. RESIDUAL,
  bounded: d_s 1.22-1.32 vs the lattice's OWN finite-size 1.73 (d_H 1.49-1.58 vs 1.69) -- a 0.4-0.5
  spectral gap, candidate cause the 6-7% fd=3 defect edges.**
  `sec01_raw_wolfram_hypergraph_facts/s1_22_isotropy_sandwich.py` (§1.6). PARTIAL; no leaf changes.
- **ROADMAP STATUS after round 62 -- the constraint stack is COMPLETE and internally consistent:**
  extent (alpha, pinned <=2 by confinement r57) | density (C=3.5 calibrated r59, which PINS cceil>=~2
  r62) | handles (gauge deficit r58) | gluing (fd-2, r59-61) | aspect ratio (the sandwich, r62). Each
  term is global, dimension-agnostic, physically motivated; zero coordinates, zero forbidden-minor
  choices, zero d inserted anywhere -- and the joint dynamics now REACHES quad-lattice-grade isotropic
  2D geometry from a bare path. THE NAMED NEXT EXPERIMENT (round 63): close the spectral gap -- defect
  census (degree and fd distributions vs the lattice; the fd=3 edges are the suspects), longer anneals,
  multi-seed statistics, and N-scaling of d_s toward the lattice's finite-size line (n=150 lattice reads
  1.73; convergence there = full closure of the 46-62 arc; a persistent gap = the defects are
  thermodynamic, itself a result). Secondary: does the same stack at alpha=3 (with C recalibrated for
  cubic-lattice balls and cceil re-pinned) produce isotropic 3D structure, or does the r55
  minor-universality obstruction reappear dynamically?
- **`emergence_tree_v0.65.zip`** — superseded by v0.66.
- **PREVIOUS (v0.65 = v0.64 + round 61: ANNEALING DYNAMICS -- r60 corrected
  THREE times (energetics offset; the glass RETRACTED as audit artifact; the ground-state claim
  OVERTURNED). The triple objective's true minimizers are TUBES: locally genuine 2-manifolds of extreme
  aspect ratio. Residual = ISOTROPY; named fix = diameter CEILING. PARTIAL. Tally 366.)** 94 experiments
  + 99 modules; test->6/6.
- **HEADLINE RESULT (round 61): reversible add/REMOVE dynamics with deletion-safe exact audits (mask set
  + per-edge index; removal dE via survivor-set GF(2) re-elimination; pivots rebuilt on accepted
  removals; all counters match full recomputes exactly). THREE CORRECTIONS TO ROUND 60: (1) its dE_glue
  had a constant -2 offset per face-closing add (harmless one-way, fatal for reversibility; fixed).
  (2) its FREEZE was an artifact stack: instrumented rejections show the post-accept audit killed 63% of
  proposals by FALSE-BLAMING new edges for the seed tree's pre-existing ~10% cap violators (the r59
  leak); with a PATH seed (compliant at every radius, zero leak) the freeze VANISHES -- even fixed-T
  dynamics reaches E_glue/edge 0.16, deficit 0, cap audit 0.00. The glass-transition story is RETRACTED.
  (3) its GROUND-STATE CLAIM IS FALSE: the dynamics builds objects strictly better than the mesh on the
  full objective (E_glue/edge 0.16-0.17 vs 0.35; 86-88% of edges at EXACTLY fd=2 vs 70%; both deficit-0,
  cap-legal, planar). THE TUBE RESULT: those minimizers have d_H 0.8-1.3 and diam 37-70 at n=150 yet
  closed-vertex-link fraction 0.73-0.74 vs the mesh's 0.50 (width E/diam 4-7 vs 11.5): thin TUBES --
  locally genuine 2-manifolds (saturated vertex stars), globally rolled quasi-1D, because boundary is
  expensive and NOTHING constrains aspect ratio (the r56 cap bounds diameter only from BELOW). NEW
  POSITIVE: the triple objective selects LOCAL 2-MANIFOLDNESS, frame-free and dimension-agnostically;
  the isolated residual of the whole 46-61 arc is ISOTROPY.**
  `sec01_raw_wolfram_hypergraph_facts/s1_21_annealing_dynamics.py` (§1.6). PARTIAL; no leaf changes.
- **ROADMAP STATUS after round 61 -- the arc's residual is one inequality:** the extent constraint is
  half-installed. The r56 cap gives |B(r)| <= C r^alpha and a diameter FLOOR (kills crumples); nothing
  bounds diameter from ABOVE, so aspect ratio is free and boundary economy drives the objective's
  minimizers to tubes. THE NAMED NEXT EXPERIMENT (round 62): the ISOTROPY SANDWICH -- add a diameter
  CEILING diam <= c' N^{1/alpha} alongside the floor (still one exponent alpha, zero d inserted, zero
  coordinates) and rerun the annealed triple on the path seed. Success = isotropic 2D patch (fd
  histogram ~mesh, d_H -> 2, diam ~ sqrt(N), closed-link high, deficit 0); failure modes to register:
  the ceiling + boundary economy might force CLOSED surfaces (sphere-like, deficit still 0) or reintroduce
  frustration/freezing. Secondary: multi-seed statistics; N-scaling; whether the tube phase is itself
  physically interesting (a frame-free emergent 1+1D geometry with genuine 2-manifold microstructure).
- **`emergence_tree_v0.64.zip`** — superseded by v0.65.
- **PREVIOUS (v0.64 = v0.63 + round 60: THE TRIPLE OBJECTIVE -- the
  selection PRINCIPLE is solved, the DYNAMICS freeze. The coherent manifold is the VERIFIED ground state
  of the full dimension-agnostic objective; add-only local dynamics freeze at 5x ground-state energy.
  A glass transition. PARTIAL. No leaf changes; tally 366.)** 93 experiments + 98 modules; test->6/6.
- **HEADLINE RESULT (round 60): the r59 residual (uniform 2-face gluing) added as a proper global energy
  E_glue = sum_edges |facedeg-2| to deficit + calibrated cap -- the TRIPLE, every term global,
  dimension-agnostic, physically motivated. Registered outcomes: success / strips (would have named
  vertex-links) / stall. THE STALL FIRED, mechanistically diagnosed: the glue term kills the r59 clumps
  as designed (fd>=4 edges 32% -> 3%) but growth dies with them (b1/V 0.33 -> 0.07-0.11, 80-86% of edges
  bare, d_s ~1.15). Mechanism: a completed face POISONS its neighborhood -- nearby closures spawn
  incidental short cycles pushing satisfied edges past 2, so dE_glue > 0 and the move dies. A dilute-face
  glass of isolated, locally-perfect faces. ROBUST to proposal engineering: frontier proposals (closing
  faces ON fd=1 boundary edges, strip/patch growth by construction) give IDENTICAL results -- strips
  cannot grow through decorated neighborhoods. THE KEY MEASUREMENT -- THE GROUND STATE IS THE MANIFOLD:
  E_glue/edge = 0.35 for the r47 mesh vs 1.62 (r56 glass) and 1.81-1.82 (everything the triple dynamics
  reaches). With deficit 0 (r58) and cap compliance at C=3.5 (r59), the mesh simultaneously
  (near-)minimizes ALL THREE terms. The failure is KINETIC, not thermodynamic: a glass transition in the
  standard sense. Incremental facedeg + GF(2) bookkeeping with full rollback; end counters match full
  recomputes exactly, every run.** `sec01_raw_wolfram_hypergraph_facts/s1_20_triple_objective.py` (§1.6).
  PARTIAL; no leaf changes.
- **ROADMAP STATUS after round 60 -- the 46-60 arc closes on a clean division.** WHAT to optimize:
  SOLVED -- gauge deficit (handles, r58) + calibrated growth cap (density/extent, alpha pinned by
  confinement, r56/57/59) + uniform 2-face gluing (r59/60): three global, dimension-agnostic, physically
  motivated terms whose joint minimum is the coherent manifold, with zero coordinates, zero
  forbidden-minor choices, zero d inserted anywhere. HOW to reach it: NOT solved -- add-only local
  dynamics freeze at 5x ground-state energy, robust to proposal engineering. THE NAMED NEXT EXPERIMENT
  (round 61, a DYNAMICS question): annealing with REMOVAL/REWIRING moves -- blocked on
  incremental-GF(2)-with-deletions engineering (lazy pivot recompute on deletion batches), not on
  physics -- plus nonlocal moves and slow cooling schedules, with the honest caveat that glasses can be
  hard for ANY dynamics. Secondary: multi-seed statistics; n-scaling of the freeze; the seed-tree
  compliance leak (~10%).
- **`emergence_tree_v0.63.zip`** — superseded by v0.64.
- **PREVIOUS (v0.63 = v0.62 + round 59: DEFICIT-SELECTION EXECUTED -- a sharp
  negative with a real calibration correction. Deficit-0 is constructible on demand under the calibrated
  cap, but the objects are tree-plus-clump structures, not manifolds. The last d-specific ingredient did
  NOT fall; the residual is uniform 2-face GLUING. PARTIAL. No leaf changes; tally 366.)** 92 experiments
  + 97 modules; test->6/6.
- **HEADLINE RESULT (round 59): the r58 named experiment ("penalize deficit, drop planarity") had a design
  flaw surfaced FIRST: it is ill-posed solo by r58's own data (the uncapped crumple has deficit 0.01;
  K5's cycle space is triangle-spanned, so deficit-0 does not imply planar). Well-posed: deficit +
  the alpha=2 cap. THE CAP CALIBRATION BUG (correction to r56): interior Manhattan |B(2)|=13 but
  C=3.0 allows 12 -- the r56 cap FORBADE THE 2D LATTICE at r=2 (55% of lattice nodes, 45% of mesh nodes
  violate at C=3.0; 0% at C=3.5). The constraint excluded its own target, partially explaining r56's d_s
  undershoot; C=3.5 calibrated. MACHINERY: add-only growth from cap-compliant seed trees (naive recursive
  trees violate the cap at 17-37%), incremental GF(2) deficit with full rollback, post-accept local cap
  audit, and end audits where incremental counters match full recomputes EXACTLY. RESULTS: deficit is
  CONTROLLABLE (glass at w_def=0 uniform, ~0 under penalty/hard); the GLASS IS TRACED (targeted
  distance-2 proposals cut def/b1 to ~0.15 at w_def=0: r56's glass came from uniform proposals +
  removals, not capped growth); BUT NO MANIFOLD -- d_s stalls at 1.1-1.3 at every deficit-0 point.
  DIAGNOSIS (edge face-degree histogram): the mesh puts 70% of edges at EXACTLY 2 faces (the manifold
  gluing signature); deficit-0 objects are BIMODAL (54-77% at 0 = bare tree, 21-40% at 4+ = clumps) --
  the deficit term positively FAVORS clumps. VERDICT: deficit-0 is necessary, not sufficient; planarity
  decomposes into (1) kill handles = deficit (r58), (2) kill density = calibrated cap (r56/57), (3)
  uniform 2-face GLUING = the true residual, supplied by nothing dimension-agnostic in rounds 46-59.**
  `sec01_raw_wolfram_hypergraph_facts/s1_19_deficit_selection.py` (§1.6). PARTIAL; no leaf changes.
- **ROADMAP STATUS after round 59 -- the arc's residual is one condition:** uniform 2-face gluing (70% of
  edges bordering exactly 2 short faces). Everything else is covered dimension-agnostically: handles by
  gauge deficit, density by the calibrated growth cap, extent by alpha, transport free at alpha=2, alpha
  pinned by confinement. THE NAMED NEXT EXPERIMENT: the TRIPLE objective -- face-degree-2 target + deficit
  penalty + calibrated cap, all three together. r53's crumple objection applied to the naive face-degree
  term ALONE (no deficit, no cap); it has never been run with the other two present. If the triple
  reproduces the mesh's face-degree histogram (peak at 2) with deficit ~0 under the cap, the manifold is
  selected with zero d-specific ingredients and the 46-59 arc closes positive. If clumps persist, the
  gluing condition is provably outside this objective family and the honest claim is that manifoldhood
  requires it as a primitive. Secondary open items: multi-seed statistics; removal moves with lazy pivot
  recompute; the seed-tree compliance leak (~10%).
- **`emergence_tree_v0.62.zip`** — superseded by v0.63.
- **PREVIOUS (v0.62 = v0.61 + round 58: GAUGE FLUX SECTORS CLOSE ROUTE 4 --
  coherence is PHYSICAL, gauge-selected; and the keystone's conserved b1=1 is one topologically protected
  flux qubit. PARTIAL. No leaf changes; tally 366.)** 91 experiments + 96 modules; test->6/6.
- **HEADLINE RESULT (round 58): DEFICIT(L) = b1 - rank_GF2(cycles of length <= L) = log2(topological
  ground-state degeneracy) of the Z2 gauge theory with plaquette action at scale L -- the toric-code
  construction on arbitrary graphs. Bare gauge counting sees b1, not genus (2^b1 sectors regardless of
  geometry, distinguishes nothing); the LOCAL Wilson action fixes the short-cycle span; what survives is
  protected. CALIBRATION EXACT: open lattice 0; torus deficit EXACTLY 2 = 2g (GSD 4 = toric code, digit
  for digit); r47 mesh shows the action must match face type (L<=3 deficit = b1 since no triangles; L<=4
  deficit 0). THE MATRIX (L<=4, deficit/b1): keystone 1.00, r47 mesh 0.00, r54 coherent planar 0.19, r56
  alpha=2 0.67, alpha=3 0.78, uncapped crumple 0.01. THE FILTRATION (L=3,4,5) IS THE DISCRIMINATOR: r54
  coherent MELTS (52->31->10, large-face artifact, genus-0 as it must); r56 phases PERSIST (57->43->35,
  176->149->94: flux glasses, extensive GSD ~ 2^{0.55 b1}); the crumple COLLAPSES (482->6->0: cycle-dense,
  local plaquettes trivialize everything, protects NOTHING). TWO UPGRADES: (1) registered prediction
  deficit = rotation-genus FALSIFIED by the crumple (rotation-genus ~1, deficit ~0) -- deficit is the
  BETTER invariant, embedding-free and gauge-operational; the r51 rotation number is an embedding artifact
  on dense graphs; coherence finally defined physically: deficit density -> 0 with a melting filtration.
  (2) the capped complexes are naturally occurring random toric codes. THE KEYSTONE QUBIT: b1=1 = a single
  conserved loop (length 5 at 400 steps; multiset->simple projection subtlety noted) with deficit 1: the
  conserved charge IS one protected Z2 flux (GSD=2, a gauge qubit), protected at every plaquette scale
  below the loop length -- and the loop grows while b1 stays 1, so at late times it is protected against
  ANY fixed-scale local action. The central conservation law of the program, restated in gauge language.
  ROUTE 4 CLOSED: free matter blind to coherence (r57), gauge matter sees it (r58) -- unique-vacuum
  manifold vs flux-glass complex at matched d_H. FINAL FACTORIZATION: EXTENT dialed (r56) | TRANSPORT free
  at alpha=2 (r56) | ALPHA pinned <=2 by confinement, extremal at 2 (r57) | COHERENCE gauge-selected
  (r58).** `sec01_raw_wolfram_hypergraph_facts/s1_18_gauge_flux_sectors.py` (§1.6). PARTIAL; no leaf
  changes.
- **ROADMAP STATUS after round 58 -- Route 4 is CLOSED and the program state is:** the referee-safe claim,
  upgraded: the keystone program's matter sector distinguishes coherent from incoherent geometry through
  gauge flux structure; the growth exponent is fixed by the confinement requirement (alpha <= 2, extremal
  at 2); and the keystone's own conserved charge is a single protected gauge flux. What "closed" does NOT
  mean: no coherent d=3 object exists (the r55 minor-universality theorem stands -- nothing topological
  supplies d=3 coherence). THE NAMED NEXT EXPERIMENT: deficit-minimization as the selection term in a
  global action -- reward faces, penalize DEFICIT (now a physically motivated, gauge-operational, and
  dimension-agnostic global objective, unlike planarity which was d=2-specific) -- and ask whether it can
  GROW coherent geometry at alpha=2, or even select d. If deficit-minimizing growth reproduces the r54
  manifold WITHOUT the planarity gate, the last d-specific ingredient falls. Honest limits carried
  forward: single seed per subject at N=150; deficit(L) claims live on the plateau L << system scale.
- **`emergence_tree_v0.61.zip`** — superseded by v0.62.
- **PREVIOUS (v0.61 = v0.60 + round 57: ROUTE 4 EXECUTED, THE MATTER
  BATTERY -- split verdict: coherence is INVISIBLE to Gaussian matter, but the CONFINEMENT TRANSITION
  sits on the dial at alpha=2, pinning alpha<=2. PARTIAL. No leaf changes; tally 366.)** 90 experiments
  + 95 modules; test->6/6.
- **HEADLINE RESULT (round 57): one Jacobi eigendecomposition per graph feeds four probes (IPR
  localization, Oganesyan-Huse <r>, effective-resistance R(d) profile = the round-6 confinement
  diagnostic, Casini-Huerta entanglement area law; K=L+m^2 shares eigenvectors so one decomposition does
  everything). Calibration: keystone R(d)=d EXACTLY (tree resistance = path length); lattice log-like
  slope 0.121, <r>=0.533 GOE, N<IPR>=2.3. (1) COHERENCE QUESTION -- at matched d_H~2 the r54 coherent
  planar manifold and the r56 alpha=2 incoherent complex are INDISTINGUISHABLE on every free-field probe:
  both delocalized (<r>~0.50-0.53), both marginal-confining (R_eff slopes 0.24 vs 0.22), both area-law.
  FREE MATTER SEES DIMENSION, NOT GENUS (registered prediction confirmed; honest near-negative). Detail:
  the coherent object is slightly MORE localized (N<IPR> 13.5 vs 9.8; planar disorder Anderson-localizes
  weakly in d~2, handles are delocalizing shortcuts). Named next test: GENUS IS GAUGE-VISIBLE in principle
  (a gauge field on a genus-g surface has 2g extra flux sectors; Wilson loops threading handles count
  genus) -- that experiment decides whether coherence is physical or aesthetic. (2) ALPHA QUESTION -- the
  confinement transition is a clean monotone crossover ON the dial: R_eff slope 0.22 (alpha=2, marginal,
  2D-lattice-like unbounded growth) -> 0.094 (alpha=2.5) -> 0.055 (alpha=3, nearly flat) -> 0.013
  (uncapped, deconfined). The Polya recurrence/transience boundary appears on the growth-cap knob.
  Combined with round 6 (keystone gauge confinement BECAUSE effective d<=2): if the phase must support
  confining gauge forces, alpha<=2, with alpha=2 EXTREMAL -- the dial's knob acquires a matter-sector
  selection principle. Caveat stated: presumes confinement is required (empirical input from the keystone
  arc, not a derivation).** `sec01_raw_wolfram_hypergraph_facts/s1_17_matter_viability.py` (§1.6).
  PARTIAL; no leaf changes.
- **ROADMAP STATUS after round 57:** the factorization now reads -- EXTENT dialable (r56); TRANSPORT free
  at alpha=2 (r56); ALPHA pinned <=2 by confinement, alpha=2 extremal (r57); COHERENCE invisible to free
  matter (r57), its physical status hanging entirely on the GAUGE SECTOR. The designated next experiment:
  put a Z2 (or U(1)) lattice gauge field on the two matched-d_H phases and count flux sectors / measure
  Wilson-loop behavior threading handles -- genus-g surfaces carry 2g extra flux sectors, so if the gauge
  sector distinguishes the r54 manifold (g=0) from the r56 complex (genus density ~0.9), coherence becomes
  PHYSICAL (gauge-selected), completing Route 4; if not, coherence is demoted to aesthetic and the
  referee-safe claim is that the keystone program selects extent+transport+alpha but not face structure.
  Either outcome closes the coherence question.
- **`emergence_tree_v0.60.zip`** — superseded by v0.61.
- **PREVIOUS (v0.60 = v0.59 + round 56: THE GROWTH-CAP DIAL -- the round-55
  candidate executed with verified enforcement. Dimension FACTORS into extent / transport / coherence.
  PARTIAL. No leaf changes; tally 366.)** 89 experiments + 94 modules; test->6/6.
- **HEADLINE RESULT (round 56): a dimension-agnostic ball-growth cap |B(r)|<=C r^alpha is a DIAL for the
  coarse dimension -- d_H tracks alpha essentially exactly (2.07/2.62/2.99 at alpha=2.0/2.5/3.0; uncapped
  control = crumple d_H~4). One real number tunes d_H, non-integer values included: the weakest scaffold
  yet (frame r47 >> forbidden-minor choice r54 >> ONE EXPONENT r56). At alpha=2 TRANSPORT COMES FREE:
  d_w=1.99 at N=300 and 600 -- normal diffusion, the FIRST frame-free instance in the program. BUT
  COHERENCE DOES NOT COME: non-planar, insertion genus density pinned ~0.9 (crumple level), and the
  d_s<d_H gap GROWS with N on audited data (0.46->0.69, N=300->600) -- structural, the r50/r53 pattern.
  ENFORCEMENT: naive endpoint-only cap checks LEAK (35-85% audit violations -- third nodes' geodesics
  reroute over cap, the r53 lesson recurring); fixed with endpoint caps (early-abort BFS, the cap bounds
  its own check cost) + GLOBAL diameter floor diam>=cN^{1/alpha} (double-sweep per add) + audit-and-repair
  sweeps -> final audit ~2%. An unaudited cap is not a cap. Feasibility boundary: alpha=1.5 infeasible
  (even trees grow ~r^2). Honest pipeline limit: N=900 repair over-strips; claims made at N<=600 where the
  audit holds. THE FACTORIZATION: emergent dimension is THREE problems -- EXTENT (d_H, solved cheap: a
  dial), TRANSPORT (d_w=2, free at alpha=2), COHERENCE (d_s=d_H + genus->0, the irreducible core:
  planarity supplies it at d=2 (r54), nothing topological can at d=3 (r55), no local rule ever (r52/53),
  and growth caps do not (r56)).** `sec01_raw_wolfram_hypergraph_facts/s1_16_growth_cap_dial.py` (§1.6).
  PARTIAL; no leaf changes. Pure Python except one planarity check (networkx, graceful degradation).
- **ROADMAP STATUS after round 56:** the dimension question is now FACTORED and the remaining core is
  precisely COHERENCE plus WHAT-FIXES-ALPHA. Both point at Route 4 (matter viability), which is now the
  sharpest open experiment in the program: run the existing physics stack (free scalar area law +
  localization + level statistics; confinement/effective-resistance; glider/soliton persistence) on
  matched-d_H phases -- the r54 coherent planar manifold vs the r56 alpha=2 incoherent capped complex --
  and ask whether the MATTER SECTOR distinguishes coherence; then sweep alpha and ask whether physics
  prefers a value. If matter requires coherence, coherence stops being aesthetic; if matter picks alpha,
  the dial's knob becomes emergent. This is the designated next experiment.
- **`emergence_tree_v0.59.zip`** — superseded by v0.60.
- **PREVIOUS (v0.59 = v0.58 + round 55: THE d=3 PRE-FLIGHT CHECK -- round
  54's linkless proposal REFUTED with exact certificates, upgraded to a THEOREM: 3D lattices are
  MINOR-UNIVERSAL, so NO forbidden-minor rule can ever select d=3. The surviving constraint type
  (ball-growth caps) named + calibrated. PARTIAL. No leaf changes; tally 366.)** 88 experiments + 93
  modules; test->6/6. Pure Python (exact combinatorial certificates).
- **HEADLINE RESULT (round 55): the 5^3 cubic lattice CONTAINS a K6 minor (exact certificate: 6 disjoint
  connected branch sets, all 15 pairs edge-adjacent). K6 is Petersen-family => 3D lattices of side >=5
  are NOT linklessly embeddable => the round-54 linkless gate would FORBID the very lattices it was meant
  to select. The E<=4V-10 check was necessary-only and misleading. UPGRADED TO A THEOREM (constructive):
  for every m, a large enough 3D lattice contains a K_m minor -- explicit tower-and-arms construction
  (m towers at x=3i; each pair gets its own z-level arm along y=1; box (3m-2) x 2 x C(m,2)), certificate-
  verified for m=6..10. COROLLARY: any minor-closed family containing all 3D lattices contains every K_m,
  hence EVERY finite graph -- no forbidden-minor rule of ANY kind can select d=3. Closed by mathematics,
  not implementation. THE 2D/3D ASYMMETRY, precise: 2D grids stay minor-sparse forever (planar exists);
  3D grids are minor-universal (why round 54 worked at d=2 and could never generalise). THE SURVIVING
  CONSTRAINT TYPE: must be NON-minor-closed. Candidate named + calibrated: BALL-GROWTH CAP
  (|B(r)|<=C r^alpha, equivalently diam >= c N^{1/alpha}) -- measured: lattices and keystone grow
  polynomially, the round-53 crumple SATURATES the whole graph by r~8 (expander signature). The cap
  excludes the crumple, admits d=1,2,3 alike (dimension-agnostic), and is not minor-closed (contraction
  speeds growth) -- exactly what the theorem demands.** `sec01_raw_wolfram_hypergraph_facts/
  s1_15_minor_universality_d3.py` (§1.6). PARTIAL; no leaf changes.
- **ROADMAP STATUS after round 55:** Route 2 at d=2 STANDS (r54, frame-free planar manifold). Route 2 at
  d=3 via forbidden minors is CLOSED BY THEOREM (r55). The d=3 continuation is now: GROWTH-CAP + face/
  volume reward -- does it select a 3-manifold? (dimension-agnostic, so if it selects ANY d without one
  being inserted, that is the real emergent-dimension result; if it selects d=2 or nothing, honest
  negative). Also still open: rerun matter/field modules on the round-54 planar-selected manifold (does
  physics survive on a SELECTED geometry?); and Route 4 reframed -- can matter viability select among
  growth-capped phases? Next experiment: growth-cap MCMC.
- **`emergence_tree_v0.58.zip`** — superseded by v0.59.
- **PREVIOUS (v0.58 = v0.57 + round 54: ROUTE 2 EXECUTED, POSITIVE -- the
  first FRAME-FREE manifold selection in the project. A global planarity constraint + face reward selects
  a genuine genus-0 2-manifold with NO coordinates. PARTIAL. No leaf changes; tally 366. NOTE: first
  third-party dependency in a section module -- networkx for exact planarity (pure-Python; graceful
  degradation if absent).)** 87 experiments + 92 modules; test->6/6.
- **HEADLINE RESULT (round 54): Route 2 SUCCEEDS at d=2 where every local rule failed. MCMC with a HARD
  GLOBAL planarity gate on edge adds (exact Boyer-Myrvold check) + triangle reward, degree free, zero
  coordinates. Output: certified planar (genus EXACTLY 0, not proxied), extensive faces (b1/V~0.9-1.3),
  d_s rising toward 2 with N (1.46->1.75 across N=80..500), diameter growing ~sqrt(N) (8->14+) -- the
  manifold signature Route 1's crumple (genus density 0.99, diam pinned ~9) never had. ONE change --
  local objective -> global constraint -- flips topology from maximal genus to zero, confirming round 53's
  principle positively. THE EULER-GATE SHORTCUT REFUTED: gating by E<=3V-6 alone saturates with NON-planar
  tangles (crumple) -- the bound constrains edge COUNT, planarity constrains STRUCTURE, and structure IS
  coherence; the full global test is irreplaceable. NOT A FRAME (3 ways): planarity is a forbidden-minor
  property (no K5/K3,3), assigns no labels, and CAPS d<=2 rather than fixing d (path/star/lattice all
  planar with d_s 1.0/0.8/1.8 -- the face reward selects the top of the cap). THE HONEST CATCH: the CHOICE
  of planarity smuggles in d=2 as which forbidden-minor family to use; no "3D planarity" exists (every
  graph embeds in R^3). THE d=3 DOOR: LINKLESS EMBEDDABILITY (Petersen-family forbidden minors incl. K6,
  Robertson-Seymour-Thomas; edge bound E<=4V-10) is the genuine 3D analogue -- verified: 3D lattices sit
  comfortably inside the bound (~0.6), K6 violates it (15>14). Poly-time decidable in principle, NO
  practical library test exists: the d=3 experiment (linkless gate + face/volume reward -> 3-manifold?) is
  named, edge-bound-verified, and blocked only on implementation. SCAFFOLD HIERARCHY: frame (coords/vertex,
  r47) >> planarity (one global forbidden-minor CHOICE, r54) >> nothing (impossible, r52/53). Dimension is
  demoted from "a coordinate system you install" to "a topological exclusion rule you choose".**
  `sec01_raw_wolfram_hypergraph_facts/s1_14_global_action.py` (§1.6). PARTIAL; no leaf changes.
- **ROADMAP STATUS after round 54:** Route 1 + Route 6 CLOSED (r53, local objectives cannot select
  coherence). Route 2 OPEN AND DELIVERING -- d=2 selected frame-free (r54); the d=3 continuation is the
  linkless-embeddability gate, blocked on a practical Petersen-family minor test (a real but bounded
  implementation project: 7 forbidden minors, minor-testing is poly-time; a bespoke heuristic detector +
  the E<=4V-10 bound may suffice for MCMC gating). Route 4 (matter viability) is now REFRAMED and
  strengthened: instead of "which scaffolded rank does physics prefer", ask "does physics prefer the
  planar-selected phase or the linkless-selected phase" -- i.e. let matter select the forbidden-minor
  family, which would make the LAST remaining choice emergent. Routes 5/7 unchanged (current evidence
  negative). The sharpest next experiments: (i) implement a practical linkless gate and run the d=3
  version of round 54; (ii) rerun the matter/field modules (gliders, confinement, area law, localization)
  on the round-54 planar-selected manifold to check the physics survives on a SELECTED (not constructed)
  geometry.
- **`emergence_tree_v0.57.zip`** — superseded by v0.58.
- **PREVIOUS (v0.57 = v0.56 + round 53: THE CONDENSATION ROUTE EXECUTED --
  responds to the "Remaining Routes" handoff doc by running its recommended Route-1 experiment (frame-free
  graph + local face/holonomy objective). Result: a sharp measured NEGATIVE confirming round 52 dynamically.
  PARTIAL. No leaf changes; tally 366.)** 86 experiments + 91 modules; test->6/6. Pure Python.
- **HEADLINE RESULT (round 53): the handoff's recommended local-holonomy condensation experiment is exactly
  the one that CANNOT work, now measured. THREE design corrections first: (1) "reward trivial holonomy" is
  MAXIMISED by a TREE (b1=0 => always flat; verified) -- flatness is necessary but a lattice and a tree are
  BOTH flat, so the target is FACES not flatness; (2) dimension is NOT coordination number -- degree-4 Z^2
  lattice d_s~1.98 vs degree-4 RANDOM regular d_s~3.05 (same degree, different dimension), so "rank
  competition" cannot be read off degree; (3) the real target is EXTENSIVE INDEPENDENT SHORT COHERENT faces.
  THE CORRECTED EXPERIMENT (frame-free MCMC, no coords, degree free, local face-coherence objective): cycles
  ARE built (b1/V climbs to ~1.9, d_s passes through 2.0 -- the two coarse manifold signatures reachable
  frame-free) BUT genus density PINS near 0.99 (MAXIMAL) and diameter collapses to single digits
  (small-world). SIDE BY SIDE at matched d_s~2 and matched cycle density: frame-free MCMC (genus_dens~0.99,
  diam~9, crumple) vs coordinate coherent mesh (genus_dens~0 planar, diam~36, TRUE manifold) -- SAME
  dimension and cycle density, OPPOSITE topology. DIAGNOSIS (round 52 dynamical): coherence = genus 0 = flat
  connection = consistent vertex labelling = COORDINATES; a LOCAL objective counts faces through an edge but
  cannot enforce ONE global orientation, so local face-reward builds incoherently-glued faces (max genus),
  not a flat tiling. CONSEQUENCE: LOCAL frame-free objectives (handoff Routes 1, 6) provably cannot select
  coherence; only GLOBAL selection principles (Route 2 action/measure, Route 4 matter viability, Route 5
  coarse-graining) can suppress the crumple, because coherence is GLOBAL.** `sec01_raw_wolfram_hypergraph_facts/
  s1_13_condensation_route.py` (§1.6). PARTIAL; no leaf changes.
- **ROADMAP STATUS (handoff "Remaining Routes" doc, after round 53):** the doc's recommended Route 1 (+ tile-
  grammar Route 6) are now CLOSED negatively -- local frame-free objectives hit the genus/coherence ceiling
  (measured, round 53) for the reason proven in round 52 (coherence = a global coordinate frame). The
  remaining OPEN routes are the GLOBAL-selection ones: Route 2 (action/measure over whole histories -- a
  global genus/curvature penalty CAN in principle suppress the crumple a local objective cannot), Route 4
  (matter-sector viability as a global filter -- run existing glider/field/confinement modules across
  scaffolded ranks d=1..5 and look for a preferred dimension), Route 5 (coarse-graining fixed point -- current
  evidence negative but not exhausted), Route 7 (causal-graph dimension first -- current evidence negative).
  The sharpest next experiment is now Route 2 or Route 4, NOT another local rule. Referee-safe claim holds:
  manifold spacetime is constructible with a frame but not selected by any LOCAL frame-free dynamics; the
  obstruction is coherence (genus), and it is global.
- **`emergence_tree_v0.56.zip`** — superseded by v0.57.
- **PREVIOUS (v0.56 = v0.55 + round 52: THE DISCRETE CONNECTION AND ITS
  REDUCTION -- carrying a per-edge holonomy variable to check flatness locally reduces PROVABLY to a
  per-vertex coordinate frame, NOT to bare topology; and b1=1 unifies the keystone's sphere topology with
  its sub-2D dimension. PARTIAL. No leaf changes; tally 366.)** 85 experiments + 90 modules; test->6/6.
- **HEADLINE RESULT (round 52): the "carry a discrete connection and refuse non-flat loops" idea is fully
  characterised and does NOT break the scaffold barrier -- it reduces to a coordinate frame. THREE exact
  results: (1) FUNDAMENTAL-BASIS REDUCTION -- flatness on ALL cycles <=> flatness on a spanning-tree basis of
  just b1=E-V+1 cycles (composites are edge-set XOR / Z-linear and inherit it; verified: zeroing b1 cotree
  signs makes all fundamental AND all composite cycles flat). Only b1 checks ever needed -- the cheap/local
  part is real. (2) COBOUNDARY REDUCTION -- a flat Z_2 connection <=> edge signs s(u,v)=c(u)c(v) for a vertex
  labelling c:V->{+-1} (verified: random signs generically NOT flat, coboundary signs always flat). So a flat
  connection is EXACTLY one bit per VERTEX up to gauge -- a vertex labelling in disguise, not per-edge data.
  (3) PLANARITY UPGRADE -- Z_2 tracks only orientation; 2D flatness needs turning (Z_4) AND zero net
  translation per loop, so by (2) the flat connection = one label per vertex in the group space = a 2D
  COORDINATE. Shown: coordinate-adjacency growth (= round 47 coherent mesh) gives genus 0 under true planar
  rotation at every N; insertion order gives ~89-94% of b1/2 (crumpled). CONCLUSION: the holonomy constraint
  reduces to bare graph data but to a per-vertex COORDINATE FRAME, not pure topology -- carrying a connection
  IS the scaffold re-encoded; no frame-free route to flatness exists (why rounds 46/50 hit the ceiling).
  KEYSTONE UNIFICATION: b1=1 => exactly ONE fundamental cycle => trivially flat with one check => genus 0
  (round 51's sphere); but a plane needs an EXTENSIVE flat cycle space (b1~N), and b1=1 forbids 2D extent
  (sub-2D, rounds 1/24/46). The keystone's sphere topology AND sub-2D dimension are ONE fact: b1=1. Flatness
  is free precisely because there is almost nothing to be flat.** `sec01_raw_wolfram_hypergraph_facts/
  s1_12_connection_reduction.py` (§1.6). PARTIAL; no leaf changes.
- **THE DIMENSION QUESTION, CLOSED IN THE NEGATIVE (rounds 46-52):** 46 (keystone fails minimal edits) -> 47
  (Z^2 frame PASSES d=2, scaffolded) -> 48 (scales to d=3, boundary-limited) -> 49 (+1 needs own scaffold) ->
  50 (frame-free attempt: real progress, genuine d_s ceiling) -> 51 (ceiling = genus obstruction; b1=1 forces
  sphere; insertion-order = random) -> 52 (the connection route to escape the frame PROVABLY reduces to the
  frame; b1=1 unifies keystone topology+dimension). The arc is now COMPLETE and coherent: a 2D manifold needs
  an extensive flat cycle space; supplying it consistently IS a coordinate frame; there is no frame-free
  shortcut; and the keystone's b1=1 is the single fact behind both its sphere topology and its sub-2D
  dimension. Scaffolded constructions (47-49) work but are tuning-not-deriving; frame-free constructions
  (50) hit a now-explained ceiling (51-52). DERIVING dimension from the bare keystone remains impossible for
  the structural reason now proven: b1=1 permanently forbids the extensive flat cycle space 2D requires.
- **`emergence_tree_v0.55.zip`** — superseded by v0.56.
- **PREVIOUS (v0.55 = v0.54 + round 51: THE GENUS OBSTRUCTION -- makes round
  50's "flatness not locally verifiable" conjecture rigorous via combinatorial map theory, and yields a new
  keystone corollary. PARTIAL. No leaf changes; tally 366.)** 84 experiments + 89 modules; test->6/6. Pure Python.
- **HEADLINE RESULT (round 51): NEW KEYSTONE COROLLARY -- b1=1 conservation FORCES the keystone spacetime to
  be a TOPOLOGICAL SPHERE (genus 0) under ANY embedding whatsoever. Proof: connected graph has F>=1, and
  F=1+b1-2g (Euler), so g<=b1/2; keystone b1=1 => g<=0.5 => g=0 forced. Confirmed computationally (genus=0
  exactly, all seeds, via face-tracing of the rotation system). No rotation, however adversarial, can give
  the keystone a handle -- it can never host a torus or genus-g 2-manifold. b1=1 locks BOTH the dimension
  (sub-2D, rounds 1/24/46) AND the topology (sphere). Plus the RIGOROUS RESOLUTION of round 50's open
  conjecture: "flatness" is made exact as the GENUS of a rotation-system embedding (V-E+F=2-2g, face-traced,
  pure combinatorics, no coordinates). Tool calibrated exactly (tree->0, planar lattice->0, torus->1,
  scrambled torus->18, all respecting g<=b1/2). Then: the natural frame-free local rotation is INSERTION
  ORDER; tested on round 47's coherent mesh (which IS planar -- true coordinate rotation gives genus 0 at
  every N), insertion-order rotation gives genus growing with N (65,181,397 at N=200,500,1000), ~88-91% of
  the b1/2 maximum, INDISTINGUISHABLE from a random rotation (181 vs 190 at N=500). Even on a provably FLAT
  graph, local edge order carries almost NO flatness information -- flatness is GLOBAL, a frame supplies the
  missing global rotation. This is exactly why round 47 needed a frame. FINALLY, round 50's diamond mesh
  DIAGNOSED: its insertion-order genus grows linearly in N at a FIXED fraction ~0.70-0.72 of b1/2 (constant
  handle density that does NOT vanish) -- an independent topological confirmation of round 50's d_s ceiling
  (~1.35-1.40), using no spectral machinery. Two windows (genus + d_s) on the same ceiling.**
  `sec01_raw_wolfram_hypergraph_facts/s1_11_genus_obstruction.py` (§1.6). PARTIAL; no leaf changes.
- **THE DIMENSION QUESTION, NOW WITH AN OBSTRUCTION THEORY (rounds 46-51):** 46 (keystone fails minimal edits)
  -> 47 (Z^2 frame PASSES d=2, scaffolded) -> 48 (scales to d=3, boundary-limited) -> 49 (+1 needs its own
  scaffold) -> 50 (frame-free attempt: real progress, genuine d_s ceiling) -> 51 (the ceiling EXPLAINED:
  "coherence" = genus-0 embeddability; local insertion order gives genus ~ random; a frame is precisely the
  global rotation that achieves flatness). The obstruction to frame-free dimension is now NAMED (holonomy /
  genus) and MEASURED, not just observed. Open round-52 candidate: a carried per-edge discrete-connection
  variable (discrete parallel transport) that lets the rule CHECK holonomy locally -- the minimal structure
  that could lower the genus below the random value, more than bare topology but far less than a global frame.
- **`emergence_tree_v0.54.zip`** — superseded by v0.55.
- **PREVIOUS (v0.54 = v0.53 + round 50: FRAME-FREE DIMENSION SELECTION --
  the central open question asked directly. Local short-cycle preference measurably helps but hits a
  genuine d_s ceiling (~1.35-1.40, does not converge with N). PARTIAL. No leaf changes; tally 366.)**
  83 experiments + 88 modules; `python main.py test`->6/6. Pure Python.
- **HEADLINE RESULT (round 50): can dimension be selected with NO frame, zero coordinates anywhere?
  Diamond-completion growth (attach new nodes to graph-distance-2 partners, closing 4-cycles via LOCAL
  topology only) approximates round 47's coherence without any embedding. UNCAPPED: fails via a NEW
  failure mode -- preferential attachment (high-degree nodes have more distance-2 partners -> hub
  formation -> diameter SHRINKS as q rises, tracking log(N) not sqrt(N): genuine small-world collapse,
  distinct from round 46's fat-tree). DEGREE-CAPPED (deg_cap=4, still frame-free -- one scalar, not a
  coordinate): fixes the catastrophic failures -- no hubs, diameter stops collapsing, c and pendant
  fraction become reasonable, d_w stays near 2 across the full q sweep. GENUINE PROGRESS over every prior
  frame-free attempt. BUT d_s PLATEAUS at ~1.35-1.40 with NO upward trend over a 16-20x range in N
  (300->5000+) while d_H keeps climbing (1.87->2.40) -- the estimators DIVERGE, not converge: a real
  structural ceiling, qualitatively different from round 48's slowly-converging d=3 lag. TWO CORROBORATING
  DIAGNOSTICS: same-tree divergence shows diamond-preference beats random closure at every q (d_s=1.41 vs
  1.15 at q=0.6) -- local short-cycle preference does genuine work; level-spacing gives <r>~0.49,
  genuinely INTERMEDIATE between the keystone (Poisson ~0.4, localized) and the true coherent mesh (GOE
  ~0.56) -- partially delocalized. WHY IT FALLS SHORT: round 47's frame-based closure is automatically
  FLAT (zero holonomy by construction); the diamond rule can prefer SHORT cycles but cannot verify FLAT
  ones without an embedding -- flatness is not testable from graph distance alone. Sharpens round 47:
  the missing ingredient is specifically zero holonomy, requiring non-local consistency or a carried
  connection variable -- a minimal scaffold either way.** `sec01_raw_wolfram_hypergraph_facts/
  s1_10_frame_free_dimension.py` (§1.6). PARTIAL; no leaf changes.
- **THE 3+1D LADDER, FINAL STATUS (rounds 46-50):** round 46 (bare keystone fails any minimal edit) ->
  round 47 (Z^2 frame + coherent closure PASSES d=2, but scaffolded) -> round 48 (mechanism scales to d=3,
  PARTIAL, boundary-limited) -> round 49 (+1 causal dimension needs its own scaffold, PARTIAL) -> round 50
  (frame-free dimension selection attempted directly: real partial progress, genuine d_s ceiling, PARTIAL).
  The d+1 scaffolding requirement (rounds 47-49) is now reinforced from the OTHER direction: round 50 shows
  the alternative (zero scaffold) does not reach manifold-hood either, and DIAGNOSES why (flatness is not
  locally verifiable from topology alone). This is the most complete current picture of the dimension
  question: scaffolded constructions work but are not derivations; frame-free constructions are honest
  attempts at derivation but hit a real, diagnosed ceiling. Open: whether a carried local connection
  variable (discrete parallel transport, more structure than bare topology but far less than a global
  frame) can close this gap -- untested, a natural round-51 candidate if pursued.
- **`emergence_tree_v0.53.zip`** — superseded by v0.54.
- **PREVIOUS (v0.53 = v0.52 + round 49: CAUSAL FOLIATION -- the +1 time
  dimension does NOT emerge from the Eden growth dynamics; an explicit temporal scaffold is required.
  PARTIAL. No leaf changes; tally fixed at 366.)** 82 experiments + 87 modules; `python main.py test`->6/6.
- **HEADLINE RESULT (round 49): the Eden growth causal DAG (birth order as physical time) gives
  d_causal<2 -- far below the (2+1)D value of 3. The interval volume V<< T^3 at every T (ratio falls
  from 0.57 at T=2 to 0.06 at T=10). The growth frontier is a 1D boundary curve so causal cones are 2D
  blobs, not 3D volumes. Birth order is SPATIAL TIME, not LORENTZIAN TIME. The CDT-style explicit
  foliation (Z^2 mesh × Z time) DOES give d_causal->3: measured V(T) matches the EXACT theoretical
  formula V=sum b(min(s,T-s)), b(r)=1+2r(r+1), which is asymptotically V~T^3/6 (d_causal=3 proved);
  local log-log slope rises toward 3 as T grows. The coherent-mesh spatial slice tracks the perfect
  lattice closely. THE +1 DOES NOT EMERGE: physical time needs an explicit temporal scaffold (CDT-style
  stacking), exactly as physical space needed the Z^2 spatial frame. Total construction: Z^(d+1) in d+1
  scaffolding stages, none selected by dynamics. Round 50 asks: can ANY dimension be skipped?**
  `sec01_raw_wolfram_hypergraph_facts/s1_9_causal_foliation.py` (§1.6). PARTIAL; no leaf changes.
- **`emergence_tree_v0.52.zip`** — superseded by v0.53.
- **PREVIOUS (v0.52 = v0.51 + round 48: d=3 COHERENT MESH -- the Z^d
  mechanism scales to d=3 on four robust signals (same-tree divergence, level-spacing GOE, d_w->2, d_H
  tracks 3D lattice), but d_s lags due to 3D Eden boundary effects (N^{-1/3} decay vs 2D's N^{-1/2}),
  requiring estimated N>>5000 for a clean PASS. PARTIAL. No leaf changes; tally fixed at 366.)** Entry:
  `python main.py {tree|status|section N|run 1.6|test|map}`. Verified: 81 experiments + 86 section
  modules; `python main.py test` -> 6/6. Pure Python.
- **HEADLINE RESULT (round 48): Z^d mechanism CONFIRMED to scale to d=3 on all N-independent controls --
  same-tree divergence shows coherent d_w FALLS (2.41->1.79 at q=1) while random d_w RISES (2.42->2.74);
  Z^3 level-spacing is GOE-leaning (<r>~0.50) vs random's Poisson-leaning (<r>~0.42); d_H tracks the 3D
  lattice at every N; d_w->2 (normal diffusion confirmed). BUT d_s lags: 2.24 at N=2500 vs lattice 2.76
  (gap ~0.52 vs d=2 gap ~0.10 at same N). Root cause: 3D Eden boundary fraction decays as N^{-1/3} (vs
  N^{-1/2} in 2D), so pendant-like boundary nodes persist much longer; estimated N>>5000 for a clean PASS.
  The three dimensions (d_s, d_H, d_w/2) also disagree more than in d=2 (0.32 gap at N~900). MULTI-d
  SUMMARY: Z^2 PASSES (d=2 gate, round 47); Z^3 PARTIAL (mechanism confirmed, d_s blocked). The 'derive
  d' problem (round 50) is orthogonal -- even a confirmed d=3 enters via the frame rank z, not dynamics.**
  `sec01_raw_wolfram_hypergraph_facts/s1_8_manifold_d3.py` (§1.6). Grade: PARTIAL; no leaf changes.
- **`emergence_tree_v0.51.zip`** — superseded by v0.52.
- **PREVIOUS (v0.51 = v0.50 + round-47 UPGRADE: three new diagnostics added to
  `s1_7_coherent_mesh.py` -- same-tree divergence, level-spacing statistics, and honest Eden-boundary caveats on
  d_s. The d=2 MANIFOLD GATE result is now confirmed by FOUR independent diagnostics. No keystone result changes;
  no leaf grade changes; tally fixed at 366).** Entry: `python main.py {tree|status|section N|run 1.7|test|map}`.
  Verified: `python main.py test` -> 6/6; 80 experiments + 85 section modules clean. Pure Python.
- **HEADLINE RESULT (round 47, upgraded v0.51): the d=2 MVS gate PASSES -- confirmed by four independent
  diagnostics:** (1) the 2x2 table (only frame+coherent hits the lattice row); (2) the q-knob (coherent d_w falls,
  fat-tree d_w rises); **(3) NEW -- SAME-TREE DIVERGENCE: starting from the IDENTICAL Eden base tree, coherent closure
  drops d_w 2.2->1.9 while random closure raises it 2.2->2.5 (diverging in opposite directions at every q); random
  always adds MORE cycles but achieves WORSE geometry -- the topological TYPE of loop (flat plaquette vs irregular
  shortcut) is the decisive variable, not the count; (4) NEW -- LEVEL-SPACING STATISTICS: coherent mesh <r>~0.56
  (GOE/delocalized, like a thermalizing 2D lattice), frame+random <r>~0.38 (sub-Poisson, MORE localized than the
  keystone despite c=1.35), keystone <r>~0.39-0.46 (Poisson -- consistent with rounds 35/36). Spectral phase and
  geometry agree: only frame-coherent closure both delocalizes the spectrum AND brings d_w->2.** The coherent mesh
  and the keystone are OPPOSITE spectral phases: GOE/thermalizing vs Poisson/localized. **(NEW HONEST CAVEAT on
  d_s):** d_s sits ~0.10-0.15 below the true lattice at N~500 (Eden boundary bias: ~4% pendant-like edge nodes vs 0%
  for the lattice), persistent across N=100-1600. The finite-size-safe signals are d_w~2 and the three dimensions
  AGREEING; d_s converges in trend. **LOCALITY RESTATEMENT:** the rule is local in execution but Z^d is a globally-
  consistent flat coordinate system (a flat background metric); "scaffolded" means "local execution, global flat
  frame." **d=3 NOTE: c=1.18 vs lattice c=1.63 at N~500 -- boundary effects worse in 3D; round 48 needs N>1500.**
  **`sec01_raw_wolfram_hypergraph_facts/s1_7_coherent_mesh.py` (§1.6; sections C/D new, E = old C).
  Grade: PASS; no leaf changes; tally fixed at 366. Pure Python.**
- **THE 3+1D LADDER (rounds 46-47, and what is next):** round 46 = the bare keystone CANNOT become a manifold by any
  minimal local edit (fat-tree / small-world). Round 47 = a DIFFERENT, frame-carrying rule CAN reach a d=2 manifold,
  confirming coherence is the missing ingredient -- but d is SCAFFOLDED, not selected. OPEN (per the scoping doc
  roadmap, awaiting Kirk go/no-go): round 48 d=3 (Z^3, larger N>1500); round 49 the +1 causal/foliation (round-30
  diagnostics, CDT-style); round 50 the hard one -- can d be SELECTED with no frame hard-coded (the unsolved "why
  3+1 dimensions" problem). 3+1D is now CONSTRUCTIBLE as a scaffolded manifold phase, still NOT derived.
- **`emergence_tree_v0.50.zip`** — superseded by v0.51.
- **HEADLINE RESULT (round 47, original v0.50): YES -- a LOCAL frame-carrying rule reaches a d=2 MANIFOLD
  (d_s=d_H~2, d_w~2, c~1); coherence (trivial loop holonomy) is the missing ingredient; d=2 is SCAFFOLDED into
  the Z^2 frame. 2x2 + q-knob confirmed at N~500. See v0.51 for the three additional diagnostics.
- **THE 3+1D LADDER (rounds 46-47, and what is next):** round 46 = the bare keystone CANNOT become a manifold by any
  minimal local edit (fat-tree / small-world). Round 47 = a DIFFERENT, frame-carrying rule CAN reach a d=2 manifold,
  confirming coherence is the missing ingredient -- but d is SCAFFOLDED, not selected. OPEN (per the scoping doc
  roadmap, awaiting Kirk go/no-go): round 48 d=3 (Z^3, larger N); round 49 the +1 causal/foliation (round-30
  diagnostics, CDT-style); round 50 the hard one -- can d be SELECTED with no frame hard-coded (the unsolved "why
  3+1 dimensions" problem). 3+1D is now CONSTRUCTIBLE as a scaffolded manifold phase, still NOT derived.
- **`emergence_tree_v0.49.zip`** — superseded by v0.50.
- **HEADLINE RESULT (round 46): the minimal modification to move the keystone off its sub-2D fractal character toward a
  manifold is LARGE -- local loop-closure fixes the structural INVARIANTS but NOT the GEOMETRY, so 3+1D is not reached
  by any minimal local edit of the b1=1 tree.** `sec01_raw_wolfram_hypergraph_facts/s1_6_manifold_modification.py`
  (§1.6; builds on rounds 24/25/29/30). Manifold criterion (round-24 fractal Einstein relation d_s=2d_H/d_w): a
  d-manifold has d_s=d_H=d AND d_w=2 (normal diffusion); the keystone is a fractal whose three dimensions DISAGREE.
  **THE OBSTRUCTION, EXACT (no fitting):** cycle density c=b1/V -> 0 for the keystone (one loop in a tree) vs EXTENSIVE
  c=(d-1) for a d-lattice (2D->1, 3D->2, measured exactly); pendant fraction ~57% vs 0; and d_w must fall from ~2.6 to
  2. **THE KNOB (close distance-2 'elbows' into LOCAL loops, p=0->1, raising c AND killing pendants):** c rises
  0->2.26 (lattice-like), pendants 52%->0%, diameter 21->11 -- the INVARIANTS reach lattice values -- BUT d_s stays
  sub-2 (1.21->1.55) and **d_w GROWS 2.70->3.42 (more anomalous, AWAY from 2)**: closing local elbows makes a clustered
  FAT-TREE (the triangles trap the random walk), still fractal/hyperbolic at large scales. **LOCALITY (reproduces round
  25):** random (non-local) loops at matched density COLLAPSE the diameter (21->5) = small-world / mean-field, not a
  manifold. **VERDICT:** the obstruction is NOT the loop COUNT (locally fixable) but the absence of native
  d-dimensional MESH connectivity -- a directional structure the b1=1 tree does not possess. Reaching d_s=d_H=d with
  d_w=2 needs an EXTERNALLY-imposed d-dimensional mesh, which REPLACES the rule's tree character rather than perturbing
  it. So 3+1D (and the +1 causal/time dimension, which round 30 already found ~1D non-manifold) is not derivable from a
  minimal local deformation. **Validation:** exact lattice benchmarks (2D c=1 d_w~1.95, 3D c=1.63 d_w~2.2); the
  invariants (c, pendants, diameter) are exact/combinatorial; the random-loop locality control reproduces round 25; the
  companion HTML recomputes c, pendants, diameter, d_s, d_w in JavaScript and reproduces the failure (p=1: c~2.4, pend
  0%, d_s~1.55, d_w~3.1 growing; random: diameter collapses to 5). Honest caveat: ball-growth d_H is finite-size-biased,
  so the robust signals are the EXACT invariants and d_w. **Grade: characterization (a quantified NEGATIVE result; no
  keystone result changes, no leaf change). Tally fixed at 366.** Pure Python.
- **THE 3+1D VERDICT (rounds 1, 24, 25, 29, 30, 41, 46):** the bare keystone is sub-2D and non-manifold at every probe
  -- three disagreeing fractal dimensions (1), a random-fractal-tree continuum (24), a non-manifold ~1D causal order
  (30), sub-2D spectral dimension (41), negatively curved and tree-like (44/45). Round 46 quantifies the fix: local
  edits CAN make the structural invariants (cycle density, pendants) lattice-like but CANNOT make the geometry
  manifold-like (d_w grows the wrong way); a true d-manifold requires replacing the b1=1 tree with an externally-imposed
  d-mesh. 3+1D is not selected, not derived, and not reachable by a minimal local deformation -- it would be a wholesale
  change to the rule's central object. (Kirk to weigh in before any such change.)
- **`emergence_tree_v0.48.zip`** — superseded by v0.49.
- **HEADLINE RESULT (round 45): the keystone is HYPERBOLIC AT ALL SCALES -- the Gromov 4-point delta (large-scale
  curvature) is BOUNDED (=1, exactly its single b1=1 loop) and does NOT grow with N, while the lattices' delta GROWS
  (flat); trees give delta=0 EXACTLY.** `sec10_general_relativity/s10_2_hyperbolicity.py` (§10.2). For four points the
  three pairing-sums of distances S1,S2,S3; delta = max over quadruples of (largest - 2nd largest)/2; a tree has
  delta=0 (the metric characterization of trees). **Measured:** chain/path delta=0 and 3-regular tree delta=0 (EXACT
  benchmarks); KEYSTONE delta=1 (its single loop), flat at 0->1->1 over N=120->500 (BOUNDED => hyperbolic at every
  scale); 3-regular graph delta~log N (2.5->3.5, weakly hyperbolic, its short cycles); cycle/2D/3D lattice delta GROWS
  with N (~sqrt(N) or N/4 => NOT hyperbolic, FLAT). **SIZE SCALING is the discriminator** (bounded delta = hyperbolic;
  growing = flat). With round 44 this shows the keystone is hyperbolic LOCALLY (Ollivier kappa<0) AND GLOBALLY (delta
  bounded) -- the same negative curvature at both scales; the lattices flat at both. **Validation:** the tree delta=0
  benchmark to 0; the size-scaling (keystone bounded vs lattice growing); the companion HTML recomputes Gromov delta in
  JavaScript and reproduces it (chain 0, cycle 15, 2D 7, tree 0, 3-regular 3, keystone 1). **Grade: characterization
  (no leaf change). Tally unchanged.** Pure Python (BFS all-pairs + the 4-point condition).
- **THE EMERGENT GEOMETRY, COMPLETE (rounds 2, 41, 44, 45):** the substrate's emergent Riemannian geometry now has all
  four pieces -- a METRIC (graph distance), a DIMENSION (round 41), a LOCAL curvature (round 44: Ollivier kappa), and a
  GLOBAL hyperbolicity (round 45: Gromov delta). The keystone is a THIN HYPERBOLIC RAMIFIED TREE: sub-2D (d_s~1.5),
  negatively curved (kappa<0), tree-like at all scales (delta bounded) -- one consistent geometry behind the whole
  scrambling/localization arc.
- **`Quantum-Dynamics-and-Emergent-Geometry_v1.0.md`** — **NEW (the SYNTHESIS WHITEPAPER).** A self-contained paper
  folding rounds 35-45 into one narrative: the free theory does not scramble (35-38); a genuine localization transition
  (39: AA lc=2, nu=1; Anderson crossover); the anomalous multifractal critical point (40: beta~D2~0.5, z~2); the
  emergent geometry (41/44/45: dimension, curvature, hyperbolicity); and interactions/MBL (42-43: static Poisson+area,
  dynamical log-t). Abstract, sections, a results-at-a-glance table, the methods/validation standard, honest
  limitations, and open frontiers. Companion to the master whitepaper v8.2.
- **`emergence_tree_v0.47.zip`** — superseded by v0.48.
- **HEADLINE RESULT (round 44): an emergent Ricci curvature separates the substrates, validated against EXACT values
  -- flat lattices (kappa=0), the positively-curved complete graph/sphere (kappa=(n-2)/(n-1)), and the NEGATIVELY
  curved keystone (-0.33) and 3-regular expander (-0.58); with the spectral dimension (round 41) this is the
  substrate's emergent Riemannian geometry, and the keystone is a THIN HYPERBOLIC ramified tree.**
  `sec10_general_relativity/s10_2_emergent_curvature.py` (§10.2; extends the round-2 keystone-only measurement). The
  emergent METRIC is the graph distance; its Ricci curvature is the Ollivier-Ricci kappa(x,y)=1-W1(mu_x,mu_y)/d(x,y)
  (exact integer min-cost-flow optimal transport, pure Python). **EXACT benchmarks (machine precision):**
  chain/cycle/2D/3D lattice kappa=0 (every edge flat); complete K5=+0.750, K8=+0.857 = (n-2)/(n-1); d-regular
  tree/expander kappa<0. **Measured:** keystone -0.33 (reproducing round 2's -0.37; ZERO positively-curved edges),
  3-regular graph -0.58, ideal 3-regular tree -0.34. **CURVATURE x DIMENSION = EMERGENT GEOMETRY:** kappa=0 +
  integer d_s = a flat MANIFOLD (lattices); kappa<0 + non-manifold d_s = the keystone (d_s~1.5, a THIN hyperbolic
  ramified tree) and the 3-regular (d_s=INFINITE, a FAT expander) -- same curvature SIGN, opposite dimension;
  curvature is the LOCAL bending, dimension the GLOBAL spreading. **LICHNEROWICZ link to round 41:** positive
  curvature lower-bounds the spectral gap (K_n: lambda_1=n/(n-1) >= (n-2)/(n-1), holds); for the negatively-curved
  keystone the bound is vacuous, consistent with its gapless/recurrent diffusion (round 41) -- curvature and the gap
  cohere. **Validation:** exact benchmarks to machine precision; idleness convention stated (keystone -0.33 at
  alpha=0, ~0 at alpha=0.5, sign non-positive, as round 2); the companion HTML recomputes the Ollivier-Ricci
  curvature in JavaScript (its own min-cost-flow optimal-transport solver) and reproduces the exact benchmarks
  (chain 0, K5 0.750, K8 0.857) and the keystone (-0.35). **Grade: characterization (no leaf change -- systematic,
  exactly-benchmarked curvature extending the round-2 DERIVED result). Tally unchanged.** Pure Python.
- **THE EMERGENT GEOMETRY (rounds 2, 41, 44):** the substrate carries an emergent Riemannian geometry -- a metric
  (the graph distance), a DIMENSION (round 41: chain 1, keystone sub-2D, lattices d, 3-regular infinite), and now a
  CURVATURE (round 44: flat lattices, positive sphere, negative keystone/expander). The keystone is a THIN HYPERBOLIC
  ramified tree: negatively curved (kappa<0), sub-2D (d_s~1.5), recurrent and non-scrambling -- one consistent
  geometry behind the whole arc. Reusable: exact Ollivier-Ricci curvature (pure-Python optimal transport) on
  arbitrary substrate graphs, with the round-41 dimension machinery.
- **`emergence_tree_v0.46.zip`** — superseded by v0.47.
- **HEADLINE RESULT (round 43): the dynamical fingerprint that separates FREE Anderson localization from MANY-BODY
  localization -- after a Neel quench, free (Delta=0) gives BOUNDED entanglement, interacting MBL (Delta=1) grows
  ~log(t), thermal grows ~linearly to volume law; demonstrated cleanly on the chain.**
  `sec05_statistical_mechanics_and_thermodynamics/s5_3_mbl_dynamics.py` (§5.3). Quench |up dn up dn ...> under the
  round-42 random-field Heisenberg, evolve EXACTLY by the spectral decomposition (no time-step error, arbitrary t),
  measure the half-cut entanglement S(t). **CHAIN (clean benchmark, N=12):** thermal (W=0.5) S rises fast to a VOLUME
  law (~2.8); free Anderson (Delta=0, W=5) is BOUNDED (log-t slope ~0.001, saturates ~0.35); interacting MBL
  (Delta=1, W=5) grows ~log(t) (slope ~0.073, ~74x the free value), and the gap S_MBL - S_free grows ~log t
  (0 -> 0.73) = the interaction-induced l-bit dephasing (Bardarson-Pollmann-Moore). So free localization (rounds
  35-39) gives bounded entanglement; interactions make it grow -- the dynamical proof that the localized phase is
  genuinely many-body. **KEYSTONE:** thermal -> VOLUME (~3.5); the free version is BOUNDED (~1.3, dynamically
  confirming the rounds 35-39 free localization) vs the thermal volume; round 42 already established its STATIC MBL
  (Poisson + area law). **Validation:** unitarity |||psi(t)||-1| ~ 1e-15; the three benchmarks recovered (thermal
  volume, Anderson bounded slope~0, MBL log-t slope>0); the companion HTML re-evolves the quench in JavaScript at
  N=8 and reproduces both S(t) and the imbalance (independent codebase, complex-Hermitian entanglement via a real
  2n-embedding). **HONEST:** at N=12 the keystone's dynamical log-t window is too short to sharply separate
  interacting from free (both still approaching finite-size saturation) -- the CHAIN is the clean dynamical
  benchmark, round 42's static diagnostics remain the clearer keystone MBL evidence; no precise localization length
  or thermodynamic-limit claim. **Grade: characterization (no leaf change). Tally unchanged.** numpy required.
- **THE FREE-VS-INTERACTING BRIDGE (rounds 35-43):** rounds 35-41 were the FREE theory (the keystone localizes,
  bounded entanglement); round 42 turned on interactions (STATIC MBL: Poisson + area law); round 43 gives the
  DYNAMICAL distinction -- free localization is bounded, interacting MBL grows ~log(t). The same Neel quench, with vs
  without the Sz-Sz interaction, separates "Anderson" from "MBL". Reusable: an exact-spectral quench evolver with
  entanglement + imbalance diagnostics on arbitrary substrate graphs.
- **`emergence_tree_v0.45.zip`** — superseded by v0.46.
- **HEADLINE RESULT (round 42): the keystone's single-particle localization SURVIVES interactions as MANY-BODY
  LOCALIZATION -- at accessible sizes it shows Poisson level statistics AND area-law entanglement at strong disorder,
  and thermalizes (GOE + volume law) at weak disorder, like the chain and 3-regular; the crossover disorder shifts
  with geometry/connectivity.** `sec05_statistical_mechanics_and_thermodynamics/s5_3_mbl.py` (§5.3). The canonical
  random-field Heisenberg H = sum_{edges}[1/2(S+S-+h.c.) + Sz Sz] + sum_i h_i Sz_i, h_i in [-W,W], Delta=1, on the
  substrate graphs; fixed Sz=0 sector; DENSE exact diagonalization. **The 2^N wall is real and stated:** even with Sz
  conservation the sector is C(N,N/2), capping us at N<=12-14 (C(12,6)=924). **Two diagnostics, both with exact
  benchmarks, that AGREE:** (1) the level-spacing ratio <r> (GOE 0.531 thermal -> Poisson 0.386 MBL) slides from GOE
  at small W to Poisson at large W for every substrate (chain 0.53->0.39, keystone 0.53->0.40, 3-regular 0.52->0.40);
  (2) the mid-spectrum entanglement S(L_A) is VOLUME-law at W=1 (grows with the cut, ->~3) and AREA-law at W=8
  (saturates: chain ~0.2, keystone ~0.8, 3-regular ~1.0). Wherever <r> is Poisson the entanglement is area-law -- the
  same phase from two independent observables. **Geometry shifts the crossover:** the disorder where <r> crosses 0.45
  is CONNECTIVITY-ORDERED -- chain ~1.9 (sparse 1D, easiest to localize), keystone ~3.5, 3-regular ~3.7 (the
  infinite-dimensional expander of round 41, hardest) -- more connectivity / higher effective dimension => harder to
  many-body-localize, tying round 42 back to round 41. **Sanity checks (all pass):** Hermiticity |H-H^T|=0, total-Sz
  conservation (built sector-by-sector), trace sum-rule |sum(E)-Tr H| ~ 1e-13; the chain is thermal at moderate W
  (GOE) and MBL at strong W (Poisson) = the textbook 1D phenomenology (the W=0 clean point is integrable/symmetric,
  Poisson, excluded from the clean comparison). **Independent cross-checks:** the two diagnostics agree (one), and the
  companion MBL-Explorer.html rebuilds and diagonalizes the same Hamiltonian in JavaScript at N=8 and reproduces the
  spectrum/<r> (a second codebase). **HONESTY GUARDRAILS (this round needs them most):** MBL at finite size is
  contested and the transition drifts with size; the thermal and deep-MBL anchors are stable (N=8->12: 0.50->0.52 and
  0.385->0.39) but the crossover W drifts -- so we claim MBL-LIKE behavior at accessible sizes, NOT a sharp transition
  or a precise W_c, and NOT a settled thermodynamic-limit phase. **Grade: characterization (no leaf change --
  interacting ED with two agreeing diagnostics + exact sanity checks, explicitly size-limited). Tally unchanged.**
  numpy required (the one such module).
- **THE STANDING LIMITATION ADDRESSED (round 42):** every prior round (35-41) was the FREE/Gaussian theory; round 42
  takes the model INTERACTING. The result: the keystone's no-scrambling/localization is not a free-theory artifact --
  it has a genuine many-body-localized counterpart at accessible sizes (Poisson + area law), while weak disorder
  thermalizes (GOE + volume). The geometry/connectivity story carries over (chain easiest, expander hardest to
  localize). Reusable: a numpy-based random-field-Heisenberg ED with <r> + entanglement diagnostics on arbitrary
  substrate graphs.
- **`emergence_tree_v0.44.zip`** — superseded by v0.45.
- **HEADLINE RESULT (round 41): the spectral dimension d_s is an emergent effective dimension that cleanly SEPARATES
  the substrates and explains the dynamics -- chain d_s=1, keystone sub-2D (~1.2-1.9, fractal), 2D lattice d_s=2, 3D
  lattice d_s=3, and the random 3-regular graph d_s=INFINITE -- validated against the EXACT lattice values.**
  `sec05_statistical_mechanics_and_thermodynamics/s5_3_spectral_dimension.py` (§5.3). Two independent routes: (A) the
  heat-kernel RETURN PROBABILITY P(t)=Tr(e^{-tL})/N ~ t^{-d_s/2} via real-time diffusion (stochastic-trace estimator,
  NO eigensolver); (B) the low-frequency LAPLACIAN DOS N(lambda)~lambda^{d_s/2} (exact analytic lattice spectra + the
  s9_5 Jacobi for the graphs). **Exact benchmarks recovered:** chain d_s=1.00 (return 1.01+-0.01), 2D d_s=1.99, 3D
  d_s=2.94 -- the DOS on the exact lattice spectra hits 1/2/3, and the two routes agree at matched N (the return
  method being finite-size-biased low). **3-regular = INFINITE:** its spectral GAP PERSISTS under N-doubling
  (0.21->0.20) -- a gapped expander with a transient return probability and exponential volume growth, the geometric
  reason for its ~log N flooding (rounds 36-37). **Keystone = sub-2D:** its gap SHRINKS (0.014->0.005) so it is
  gapless and FINITE; d_s(return)~1.2, d_s(DOS)~1.9 -> sub-2D (d_s<2, recurrent), probe-dependent -- reproducing the
  program's long-standing running/probe-dependent keystone dimension (transport ~1.3-1.5 vs static ~1.9-2.5).
  **HONEST framing:** d_s is the GEOMETRIC dimension of diffusion, NOT a lone scrambling predictor -- the clean chain
  has d_s=1 yet scrambles ballistically; the Aubry-Andre/Anderson chains share the chain graph (d_s=1) and localize
  via the on-site potential, a mechanism distinct from geometry. What d_s does: give an emergent effective dimension
  with exact benchmarks, explain the 3-regular flooding (d_s=infinite), and quantify the keystone's ramified sub-2D
  geometry -- the classical-diffusion face of the same b1=1 pendant tree that localizes quantum-mechanically (rounds
  35-38). Error bars from sliding the fit window (d_s fits have finite-size/window subtleties -- reported, not
  hidden). **Grade: characterization (no leaf change -- d_s measured + validated against exact values; reproduces the
  program's keystone d_s). Tally unchanged.** Pure Python (real-time diffusion + exact lattice spectra + s9_5 Jacobi).
  The companion `Spectral-Dimension-Explorer.html` diffuses the heat kernel on each substrate (toggle) and fits d_s
  live on a log-log P(t) plot against slope -1/2,-1,-3/2 references; its JS reproduces the Python (chain 0.97 vs 1.01,
  2D 1.75 vs 1.78).
- **NEW THREAD -- EMERGENT GEOMETRY (round 41 opens it):** with the scrambling arc closed (rounds 35-40), round 41
  opens the geometry thread by measuring the substrates' emergent spectral dimension. It connects back: the
  3-regular's infinite d_s is why it floods/scrambles (rounds 36-37), and the keystone's sub-2D ramified geometry
  (d_s<2, recurrent) is the classical-diffusion counterpart of its quantum localization (rounds 35-38). Reusable
  pure-Python tools: heat-kernel return-probability d_s (stochastic-trace diffusion), exact-lattice-spectrum DOS d_s,
  and a spectral-gap-scaling infinite-D detector.
- **`emergence_tree_v0.43.zip`** — superseded by v0.44.
- **HEADLINE RESULT (round 40): at the round-39 critical point lambda_c=2 the dynamics is ANOMALOUS and the states
  MULTIFRACTAL, both ~0.5 -- the scrambling/frozen boundary is a clean power law, not a discontinuity.**
  `sec05_statistical_mechanics_and_thermodynamics/s5_3_critical_dynamics.py` (§5.3). **(1) Dynamical spreading
  exponent.** Release a wavepacket at one site of the Aubry-Andre chain (for a free system this IS the operator
  front of rounds 37-38) and fit its width sigma(t)~t^beta: lambda=1 beta=0.95 (BALLISTIC ->1, scrambling), lambda=3
  beta=0.02 (FROZEN ->0, localized), and **lambda_c=2 beta=0.52+-0.03 (ANOMALOUS ~0.5)**. The dynamical exponent
  z=1/beta~1.93~2; with the round-39 nu=1 this fixes the scrambling-boundary scaling. The participation number
  N_p(t)~t^beta_P is also anomalous at lambda_c (beta_P~0.33, < beta -> the spreading itself is multifractal).
  **(2) Multifractality.** The generalized dimensions from eigenstate inverse participation ratios
  I_q~N^{-(q-1)D_q}: D_2 = 0.93 (lambda=1, extended ->1), **0.51 (lambda=2, critical)**, 0.03 (lambda=3, localized
  ->0); and D_1 > D_2 (q-dependent => genuinely multifractal) MAXIMAL at lambda_c (gap ~0.18) and vanishing off it
  (extended/localized states are not multifractal). **COHERENCE:** the dynamical beta and the static D_2 are both
  ~0.5 -- two completely different methods (real-time leapfrog vs diagonalization) giving the same critical number;
  the multifractal states are the static origin of the anomalous spreading. **Validated:** the exact limits
  (beta->1 ballistic, beta->0 frozen; D_q->1 extended, ->0 localized) are recovered and bracket the anomaly; the two
  independent methods agree at lambda_c; beta_P is a second (different) anomalous dynamical exponent; D_1>D_2
  confirms multifractality; and ~0.5 matches the known golden-mean Aubry-Andre critical values. Error bars from
  bootstrapping phase samples; the AA critical dynamics has golden-mean log-periodic oscillations, so exponents are
  fit over a broad window and averaged -- reported honestly (beta(lambda=1)=0.95 not exactly 1 is a finite-window/
  quasiperiodic effect). **Grade: characterization (no leaf change -- characterizes the critical point that rounds
  37-39 located). Tally unchanged.** Pure Python (real-time leapfrog + the s9_5 Jacobi). The companion
  `Critical-Dynamics-Explorer.html` evolves the front live and fits beta on a log-log plot against slope-1/half/0
  references, with a multifractal eigenstate panel; its JS reproduces the Python beta (0.95/0.52/0.04).
- **THE CRITICAL POINT, CHARACTERIZED (rounds 37-40):** the keystone does not scramble (35-38); that no-scrambling
  is one side of a genuine PHASE TRANSITION (39: Aubry-Andre lambda_c=2, nu=1; Anderson a crossover); and the
  transition point itself is ANOMALOUS + MULTIFRACTAL (40: beta~0.5, D_2~0.5, z~2). The localization/scrambling
  boundary is a continuous critical point with a clean sub-ballistic/sub-frozen power law, not a discontinuous jump.
  Reusable pure-Python tools: real-time wavepacket/operator evolution + spreading-exponent fit, multifractal D_q
  from eigenstate IPR scaling, on top of the round 35-39 machinery.
- **`emergence_tree_v0.42.zip`** — superseded by v0.43.
- **HEADLINE RESULT (round 39): the round-38 scrambling order parameter is the order parameter of a real PHASE
  TRANSITION — SHARP (lambda_c=2, nu=1) for a quasiperiodic knob, a CROSSOVER for random disorder.**
  `sec05_statistical_mechanics_and_thermodynamics/s5_3_localization_transition.py` (§5.3). Tune a 1D tight-binding
  chain's on-site potential and finite-size-scale two order parameters: P_K/N (round-38 Krylov participation, via
  Haydock recursion) and Lambda=xi/N (dimensionless localization length from the transfer-matrix Lyapunov exponent
  gamma=1/xi; O(N), no eigensolver). **Aubry-Andre quasiperiodic (eps_i=lambda*cos(2*pi*PHI*i+phase), PHI the golden
  mean):** a TRUE transition — the Lambda(lambda) curves for N=256..2048 are size-INDEPENDENT at the critical point
  (they cross), and FSS gives **lambda_c = 1.995 +- 0.002** (data collapse) and **nu = 0.96 +- 0.02** from the
  divergence xi~(lambda-lambda_c)^-nu, with nu -> 1 as the fit window approaches lambda_c (the ~4% gap is the
  ANALYTIC correction nu = 1 - <lambda-2>/4 from xi=1/ln(lambda/2)) -- matching the EXACT Aubry-Andre values
  lambda_c=2, nu=1. P_K/N is N-independent (~0.65) in the delocalized phase and -> 0 in the localized phase,
  transitioning at the same point. **Anderson random disorder (eps_i ~ uniform[-W/2,W/2]):** NO size-independent
  crossing -- Lambda decreases with N for every W (xi ~ 1/W^2): a CROSSOVER, not a transition, exactly as 1D
  Anderson requires. **Validated five independent ways:** (1) the transfer-matrix gamma matches the EXACT
  Aubry-Andre gamma=ln(lambda/2) to ~3e-4 on the localized side; (2) lambda_c~2.0 and nu~1.0 recovered = the known
  exact values; (3) the transfer-matrix localization length agrees with the band-center eigenstate-IPR length from a
  direct diagonalization (ratio O(1)); (4) the Aubry-Andre self-duality (lambda <-> 4/lambda, localized <->
  extended) holds; (5) both order parameters (P_K/N and Lambda) transition at the same lambda_c, and the Anderson
  crossover shows in both. Error bars from bootstrapping the phase samples; the collapse residual is reported (no
  exponent claimed beyond what the data supports). **Grade: characterization (no leaf change -- promotes the
  round-38 order parameter to a phase transition, validated against an exact solution). Tally unchanged.** Pure
  Python (transfer matrix + the round-38 Lanczos/Haydock). The companion `Localization-Transition-Explorer.html`
  sweeps the knob live, shows the FSS crossing, and lets you drag (lambda_c, nu) to collapse the curves (collapsing
  at 2, 1 for AA; never for Anderson); its JS transfer matrix reproduces gamma=ln(lambda/2) to ~1e-5.
- **THE SCRAMBLING ARC AS A PHASE DIAGRAM (rounds 35-39):** rounds 35-38 established four independent ways that the
  b1=1 keystone does not scramble (real-space localization, Poisson spectrum, OTOC v_B=0, Krylov localization), and
  round 38 distilled them into a scalar order parameter P_K/N. Round 39 shows that order parameter is the order
  parameter of a genuine localization/scrambling PHASE TRANSITION: sharp (lambda_c=2, nu=1) for a quasiperiodic knob
  -- validated against the exact Aubry-Andre solution -- and an honest crossover for random disorder. The keystone
  sits firmly on the localized/non-scrambling side. Reusable pure-Python tools: transfer-matrix Lyapunov +
  localization length, FSS data-collapse / nu-extraction, on top of the round 35-38 machinery.
- **`emergence_tree_v0.41.zip`** — superseded by v0.42.
- **HEADLINE RESULT (round 38): operator growth in the keystone is KRYLOV-LOCALIZED — the recursion-method Lanczos
  chain is LONG (D_K~126) but the operator occupies only ~12 of its sites (P_K/N~0.15) and Krylov complexity K_c(t)
  SATURATES (~7), so it does not scramble; the clean chain spreads ballistically down its Krylov chain (P_K/N~1.0,
  K_c grows ~linearly to ~40). Krylov participation P_K is a clean ORDER PARAMETER.** `sec05_statistical_mechanics_
  and_thermodynamics/s5_3_krylov_complexity.py` (§5.3). Method (Parker-Cao-Avdoshkin-Scaffidi-Altman 2019): operator
  growth of A=p_{i0} under the Liouvillian L=[H,.] reduces, for the free scalar (K=L+m²), to the recursion method on
  the operator power spectrum Φ(ω)=Σ_k V_{i0,k}² δ(ω∓√ev_k); Lanczos with full reorthogonalization (a_n=0 by ±ω
  symmetry) gives the hoppings b_n of a 1D Krylov chain, and K_c(t)=Σ_n n|φ_n(t)|² measures how far the operator
  spreads along it. **Order parameters (m²=0.05, N~60-80):** Krylov participation P_K/N = clean chain 1.02, KEYSTONE
  0.15, Anderson chain 0.11, random 3-regular 1.47 — localized substrates small, delocalized large (~7-13×). K_c
  saturates (keystone ~7, Anderson ~3) vs grows ~linearly (chain ~40, 3-regular ~54). The keystone Krylov chain is
  LONG (D_K~126: the hub couples to every frequency) yet the operator occupies only ~12 sites — a genuine ANDERSON
  LOCALIZATION IN KRYLOV SPACE (long disordered chain, localized wavefunction), the operator-space mirror of round
  35's real-space localization; its Lanczos coefficients are disordered (cov(b_n) keystone 0.43, Anderson 0.57) vs
  smooth (chain 0.10). **Validated FIVE independent ways, all at machine precision:** (1) sum rule b_1²=⟨ω²⟩
  (~1e-15); (2) the autocorrelation rebuilt from the Krylov chain equals the direct spectral sum Σ_k w_k cos(ω_k t)
  (~1e-10); (3) ⟨ω⁴⟩ chain==direct (~1e-9); (4) the Krylov-chain band edge == max ω (~1e-13); (5) the eigen-average
  P_K matches an INDEPENDENT time-sampled P_K (to a few %). Consistency: the round-35 real-space mode participation
  tracks P_K across all four substrates (keystone/Anderson small; chain/3-regular large) — two independent
  localization probes agreeing. **Grade: characterization (no leaf change — a fourth, basis-independent confirmation
  of the no-scrambling/localization already graded at §5.3 "Thermalization"; sharpened into a quantitative order
  parameter). Tally unchanged.** Pure Python (Lanczos with full reorthogonalization; reuses the s9_5 Jacobi). The
  companion `Krylov-Complexity-Monitor.html` eigendecomposes K, runs Lanczos, and evolves the operator on the Krylov
  chain live (its b_1²=⟨ω²⟩ pipeline matches Python to ~1e-15), rendering the Krylov cone (ballistic vs frozen),
  K_c(t), and the b_n sequence, switchable across substrates.
- **THE SCRAMBLING ORDER PARAMETER (rounds 35-38, the arc closes from FOUR independent sides):** real-space
  localization (35: IPR/quench, area-law-capped entanglement), spectral (36: Poisson level statistics, massive exact
  degeneracy), dynamical (37: OTOC butterfly velocity v_B≈0, frozen cone), and operator-growth (38: Krylov
  localization, K_c saturated). Round 38 supplies the clean ORDER PARAMETER the earlier probes lacked — Krylov
  participation P_K (equivalently the saturated K_c): small for the non-scrambling substrates (keystone, Anderson),
  large for the delocalized ones (chain, 3-regular). The b₁=1 sparse, pendant-heavy keystone tree does not scramble
  information — now established four independent ways. Reusable pure-Python tools: the recursion-method Lanczos
  (with reorthogonalization) + Krylov-complexity evolver, plus the OTOC/quench/level-statistics machinery from 35-37.
- **`emergence_tree_v0.40.zip`** — superseded by v0.41.
- **HEADLINE RESULT (round 37): the keystone's OTOC butterfly cone never opens — the squared commutator
  C_ij(t)=⟨|[W_i(t),V_j(0)]|²⟩ stays pinned to ~7 sites (v_B≈0), so a distant operator never learns the
  perturbation happened: the DIRECT, dynamical confirmation of rounds 35-36.** `sec05_statistical_mechanics_
  and_thermodynamics/s5_3_otoc_scrambling.py` (§5.3). The rule's free scalar (H=½p²+½xᵀKx, K=L+m², rounds
  27/31/35) has Heisenberg operators that evolve by the SAME round-35 symplectic propagator
  M(t)=exp(t[[0,I],[−K,0]]); since [x_i(t),p_j]=i(Mxx)_ij is a c-number, the OTOC is EXACTLY
  C_ij(t)=(cos√K·t)²_ij — a wave released from a point, no state/thermal average (being free/Gaussian there is
  no exponential Lyapunov growth: correct, the substrate is integrable per 35-36; the question is purely whether
  the operator SPREADS). Calibrated controls (m²=0.05): clean chain v_B≈1.1 (a textbook ballistic light cone,
  N_eff grows with the cone volume); a disordered (Anderson) chain COLLAPSES the cone (mechanism = localization);
  a random 3-regular graph (the round-36 chaotic reference) floods all sites in ~log N. Keystone: v_B≈0.18→0,
  mean spread ⟨d⟩≈1.4 (flat), N_eff≈7 of ~120 sites, far-site OTOC ~10⁻⁶ for all time — the commutator cannot
  escape the localized region. **Grade: characterization (no leaf change — directly confirms the localization/
  no-scrambling already graded at §5.3 "Thermalization" and rounds 35-36). Tally unchanged.** Pure Python
  (reuses the s9_5 Jacobi + round-35 M(t); chain/Anderson/3-regular controls built locally). The companion
  visualizer `OTOC-Scrambling-Monitor.html` integrates the OTOC live by c̈=−Kc (sparse Verlet, validated against
  exact cos√K·t to ~10⁻⁵) and renders the butterfly cone, network glow, wavefront radius R(t) (slope=v_B) and
  radial profile, switchable across substrates; its JS keystone port reproduces the program signatures (b₁=1, ~57% pendants).
- **`emergence_tree_v0.39.zip`** — superseded by v0.40.
- **HEADLINE RESULT (round 36): the keystone Laplacian has POISSON level statistics (gap ratio <r>~0.39, no
  level repulsion) and ~1/4-1/3 EXACTLY degenerate eigenvalues -- the spectral fingerprint of a localized/
  integrable system, decisively NOT quantum-chaotic.** `sec05_statistical_mechanics_and_thermodynamics/
  s5_3_level_spacing_statistics.py` (§5.3). The canonical quantum-chaos diagnostic, confirming round 35 from
  the spectrum side. Sort the Laplacian eigenvalues; the Oganesyan-Huse gap ratio
  `r_n=min(s_n,s_{n+1})/max(s_n,s_{n+1})` (no unfolding) is `<r>~0.39` (-> Poisson 0.386 as N grows), where a
  random 3-regular graph (chaotic/delocalized control) gives `~0.53`, matching a GOE matrix (0.536). Plus a
  striking structural feature: ~25-35% of keystone eigenvalues are EXACTLY degenerate (chaos: ZERO) --
  `lambda=1` carries huge multiplicity (~292 at N~1500) from antisymmetric pendant-pair modes, and golden-
  ratio eigenvalues (2.618, 0.382 from two-pendant "cherry" motifs) and `2+-sqrt(3)` (longer pendant paths)
  recur as the "molecular-orbital" spectrum of the tree's repeating motifs. Spacing shape: keystone many tiny
  gaps (P(s<0.1)~0.36, no repulsion) vs chaotic graph ~0.01 (strong repulsion). **Three independent spectral
  signatures -- Poisson <r>, massive exact degeneracy, clustered spacings -- all certify LOCALIZED/INTEGRABLE.
  Grade: characterization (no leaf change -- confirms localization/integrability already in 5.3). Tally
  unchanged.** Pure Python (Jacobi; random regular graph + GOE built locally).
- **THE SPECTRAL VERDICT (rounds 35-36 are one story):** the keystone is localized and non-chaotic, shown two
  independent ways -- real-space (IPR + quench: modes localized, entanglement area-law-capped, no
  thermalization) and spectral (level statistics: Poisson, massive degeneracy, no level repulsion). The b1=1
  sparse, pendant-heavy, motif-repeating tree is an integrable/localized substrate; it does not scramble at any
  level. Reusable pure-Python tools now include the gap-ratio/degeneracy analyzer, a random-regular-graph
  generator, and a GOE builder.
- **`emergence_tree_v0.38.zip`** — superseded by v0.39.
- **HEADLINE RESULT (round 35): the keystone field's eigenmodes are ANDERSON-LOCALIZED, so a quench does NOT
  thermalize -- entanglement is area-law-capped (no volume-law thermalization, no scrambling), unlike a chain
  that thermalizes to volume-law.** `sec05_statistical_mechanics_and_thermodynamics/s5_3_quench_localization.py`
  (§5.3). Turns the static Page curve (round 34) into a Page PROCESS: prepare a product state, switch on the
  keystone couplings at t=0, evolve unitarily (Gaussian covariance `sigma(t)=M(t)sigma0 M(t)^T`,
  `M=exp(t[[0,I],[-K,0]])`); entanglement via Renyi-2 `S2(A)=(1/2)ln det(sigma_A)` (determinant-based, pure
  Python). **(1) Localization (IPR `sum|psi|^4`):** the random tree (degree disorder, ~57% pendants)
  localizes the modes -- mean mode covers ~30 of ~800 sites (~5 of ~110 small-N), ~1/4-1/3 strongly localized
  (<5 sites); a 1D chain is EXTENDED (~2/3 of sites, 0% strongly localized). **(2) No volume-law
  thermalization:** chain quench `S2_sat` grows with `|A|` (volume-law, thermalizes); keystone `S2_sat` is
  FLAT (area-law cap, only a few x the cold ground state) -- localized modes cannot transport entanglement.
  **Reading:** the keystone is a LOCALIZED, non-thermalizing system; local tree dynamics cannot scramble
  information into a volume of entanglement, hot or cold -- OPPOSITE of black-hole fast scrambling, and the
  hot (volume-law) Page tent of round 34 is UNREACHABLE by its own dynamics (it needed a non-local
  Hamiltonian). **Caveat:** the free scalar is Gaussian (integrable -> GGE); the point is geometric (same
  field reaches volume-law on a CHAIN but is localization-capped on the keystone TREE). **Grade:
  characterization (no leaf change -- refines "Thermalization" PARTIAL). Tally unchanged.**
- **THE DYNAMICAL VERDICT (round 35 closes the entanglement arc):** the keystone is LOCALIZED and does not
  scramble. Cold -> area law (31), bond-local entanglement (33), suppressed Page curve (34); and now the
  DYNAMICS can't escape it -- a quench stays area-law-capped (35). The `b1=1` sparsity gives mode localization,
  so the substrate is a non-thermalizing, non-scrambling system at every level. The pure-Python machinery now
  includes a Gaussian quench evolver + Renyi-2 (det-based) entropy + IPR, reusable for further dynamics.
- **`emergence_tree_v0.37.zip`** — superseded by v0.38.
- **HEADLINE RESULT (round 34): the keystone field's radiation entropy traces a PAGE CURVE — it rises and
  falls (unitarity / information return); the cold ground state gives a suppressed AREA-LAW curve, a scrambled
  state gives the full VOLUME-LAW Page tent.** `sec10_general_relativity/s10_5_page_curve.py` (§10.5), using
  the round-31 Casini-Huerta machinery. The Page curve's mechanism is purity: `S(A)=S(complement)`, so a
  region grown from empty to full has `S` rise from 0 and return to 0. **Calibration** (cold curve encodes the
  horizon dimension): 1D chain (d=1) FLAT (boundary=2, no peak); 2D grid (d=2) rounded TENT peaking near half.
  **Keystone COLD** (ground state): rises-and-falls (unitarity), peaks near half (like the grid -- `d_H~2.3`
  gives growing region-boundaries), irregular, AREA-LAW height (peak set by the horizon). **Keystone HOT**
  (scrambled volume-law pure state = ground state of a dense random Hamiltonian): the maximal SYMMETRIC Page
  TENT peaking at half, height ~11x the cold curve. **Reading:** both rise and fall -- unitarity holds
  regardless; only the AMOUNT differs. The natural (cold) state radiates AREA-LAW entropy (suppressed Page
  curve, small tree horizons); a scrambled state radiates VOLUME-LAW (full tent). Same `b1=1` sparsity behind
  the area law keeps the cold horizon small. **Caveat:** this is the Page-curve STRUCTURE (pure-state growing
  subsystem), not a dynamical evaporation with island/QES dynamics. **Grade: §10.5 "Information paradox
  analogues" CONJECTURE->PARTIAL. Tally: CONJECTURE 28->27, PARTIAL 124->125.**
- **THE ENTANGLEMENT ARC (rounds 31-34, one coherent story):** (31) true Gaussian-field entropy obeys an area
  law `S~|dA|`, IR divergence in coefficient; (32) monogamy VIOLATED -> not holographic (generic free field);
  (33) quantum entanglement is nearest-neighbor (bond-local) -> microscopic origin of the area law; (34) the
  Page curve rises and falls (unitarity), cold area-law (suppressed) vs scrambled volume tent. Everything
  flows from one fact -- a gapped lattice field on a sparse (`b1=1`) tree: bond-local entanglement -> area law
  -> suppressed (boundary-set) Page curve; generic (non-holographic) entanglement throughout. The pure-Python
  Casini-Huerta + negativity + Page machinery is reusable.
- **`emergence_tree_v0.36.zip`** — superseded by v0.37.
- **HEADLINE RESULT (round 33): quantum entanglement in the keystone ground state is NEAREST-NEIGHBOR (the
  logarithmic negativity), while classical correlation is long-ranged — this is the microscopic origin of the
  area law.** `sec09_quantum_mechanics/s9_5_entanglement_negativity.py` (§9.5), reusing the round-31 machinery.
  Mutual information counts quantum+classical; the logarithmic NEGATIVITY E_N is a genuine entanglement
  monotone (zero on separable mixed states). For a Gaussian state the partial transpose is Gaussian:
  `E_N = sum_{nu~<1} -ln(nu~)`, `nu~ = sqrt(eig(sigma_xx . D sigma_pp D))`, D flips B's momenta. **Validated**
  (1D chain: adjacent sites entangled `E_N~0.29`, every separated pair `E_N=0` EXACTLY while `I` decays --
  entanglement sudden death). **Keystone:** quantum entanglement is essentially NEAREST-NEIGHBOR -- single-site
  `E_N~0.26` at d=1 (100% of pairs), small tail at d=2 (`~0.017`, ~38% of pairs, irregular branching, grows as
  m->0), dead by d=3; classical correlation (`I`) decays far slower (`0.24, 0.05, 0.015, 0.004`). Adjacent
  subtrees across one edge strongly entangled (`E_N~0.32`). **The MICROSCOPIC ORIGIN of the area law:**
  entanglement lives on the BONDS, so a region is entangled with the rest only across its boundary EDGES ->
  `S~|dA|`; each boundary edge carries one nearest-neighbor entangled bond. The long-range mutual information
  is purely CLASSICAL. **Grade: §9.5 "Correlation structure" OPEN->PARTIAL. Tally: PARTIAL 123->124, OPEN
  100->99.**
- **THE ENTANGLEMENT PICTURE (rounds 31-33, complete and consistent):** (31) the true Gaussian-field entropy
  obeys an area law `S~|dA|`, IR divergence in the coefficient; (32) monogamy of mutual information VIOLATED
  -> not holographic (generic free field, no RT bulk); (33) quantum entanglement is nearest-neighbor
  (bond-local), classical correlation long-ranged -> the microscopic origin of the area law. One coherent
  story: a gapped lattice field on a sparse (`b1=1`) tree -- bond-local entanglement giving an area law,
  generic (non-holographic) entanglement, static-side entanglement dimension. The pure-Python Casini-Huerta +
  negativity machinery (`s9_5_entanglement_entropy_area_law`, `s9_5_entanglement_negativity`) is reusable for
  Page-curve analogues or mutual-information phase structure.
- **`emergence_tree_v0.35.zip`** — superseded by v0.36.
- **HEADLINE RESULT (round 32): the keystone free scalar VIOLATES the monogamy of mutual information (I3>0),
  so its entanglement has NO classical Ryu-Takayanagi bulk dual — it is not holographic in the strong sense,
  despite the area law.** `sec13_speculative_extensions_appendices/s13_5_monogamy_mutual_information.py`
  (§13.5), using the round-31 Casini-Huerta machinery. Holographic states (classical RT bulk) satisfy
  monogamy `I3(A:B:C)=I(A:B)+I(A:C)-I(A:BC) = S_A+S_B+S_C-S_AB-S_AC-S_BC+S_ABC <= 0`; generic free fields
  violate it. **Tempting hypothesis REFUTED:** the `b1=1` TREE geometry is what MERA / holographic tensor
  networks live on, so maybe the keystone entanglement is monogamous (holographic). It is NOT -- computed `I3`
  for nearby tripartitions and the cleanest HUB tripartitions (3 subtree branches off one high-degree node):
  **1D chain (a tree) violates MMI (I3>0 every config); 2D grid violates MMI (I3>0 every config); keystone
  violates MMI** (hub `I(A:B)~0.1-0.15`, `I3~+0.02..+0.08>0`, substantial). The keystone is a generic free
  field: area law YES (`s9_5`), RT geometry NO. The area law is necessary but not sufficient for holography;
  the keystone fails the sufficient (MMI) test exactly as the chain/grid do. **Holography is a property of the
  STATE**, not the geometry -- the tree is MERA-friendly, but the rule's natural state is a free Gaussian
  field, not a holographic tensor network. **Grade: §13.5 "Entanglement geometry" CONJECTURE->REFUTED (no
  consistent minimal-surface bulk); sharpens "Limits of the analogy". Tally: CONJECTURE 29->28, REFUTED
  4->5.**
- **THE HOLOGRAPHY VERDICT (rounds 31-32, sharp):** the keystone free scalar has a genuine entanglement
  AREA LAW (`S~|boundary|`, the necessary condition) but VIOLATES monogamy of mutual information (fails the
  sufficient condition for a classical RT bulk). So it is "area-law but not holographic" -- exactly a generic
  free field. The `b1=1` tree geometry does not make it holographic; that would need a special (MERA-like)
  state, not the free-field ground state.
- **`emergence_tree_v0.34.zip`** — superseded by v0.35.
- **HEADLINE RESULT (round 31): the true Gaussian-field entanglement entropy obeys an area law S ~ |boundary|;
  the round-27 IR divergence reappears in the COEFFICIENT, not the scaling.** `sec09_quantum_mechanics/
  s9_5_entanglement_entropy_area_law.py` (§9.5, also §13.5). The holography module (s13_5) had measured only
  the GEOMETRIC boundary (`|dR|~|R|^0.7`) and explicitly left undone "a true entanglement entropy
  (Casini-Huerta, which needs spectral linear algebra)." This round does it in pure Python (a small Jacobi
  eigensolver). Method: the free scalar is the oscillator system with `K=L+m^2`; the Gaussian ground state has
  `X=<phi phi>=(1/2)K^{-1/2}`, `P=<pi pi>=(1/2)K^{1/2}`; region entropy from eigenvalues `nu>=1/2` of
  `sqrt(X_A P_A)`. **Calibrated** (1D chain single-edge cut: S constant ~0.25-0.30 = area law; 2D grid ball:
  S grows `0.58->2.04` with perimeter = area law, growing boundary). **Keystone:** the true entropy obeys
  `S ~ |dA|` -- single-edge cuts (boundary=1 for any subtree, a tree property) give **S CONSTANT in |A|**
  (slope `dS/dln|A| ~ -0.03`) at every mass, so S tracks the boundary not the volume. **The IR divergence is
  in the COEFFICIENT:** per-edge entropy grows `~ln(1/m^2)` as `m->0` (`S` mean `0.13->0.28`), NOT as critical
  (`log|A|`) or volume-law growth -- the area-law SCALING is mass-independent. **Dimension split:** since
  `S~|dA|` and the boundary scales sub-extensively (static side `~|R|^0.7`), entanglement entropy is a STATIC /
  boundary-counting probe (6th measurement on the static side); the `b1=1` signature is that a 2-manifold's
  growing perimeter makes S grow while a tree subtree's `O(1)` boundary makes S saturate. **Grade: §9.5
  "Entanglement entropy" OPEN->PARTIAL (entropy computed, area law established + calibrated; precise bulk
  exponent and exact `m->0` law loosely pinned); also corroborates §13.5 "Area-law behavior". Tally: PARTIAL
  122->123, OPEN 101->100.**
- **METHOD NOTE for next session:** the Gaussian-field entanglement entropy is now available in pure Python
  (Jacobi eigensolver in `s9_5_entanglement_entropy_area_law`); reuse it for mutual information, Page-curve
  analogues, or entanglement-geometry tests. Single-edge cuts (boundary=1) are the clean area-law probe on a
  tree; balls give growing-boundary regions.
- **THE STATIC vs DYNAMIC DIMENSION SPLIT (now SIX measurements):** STATIC/counting -- volume ball-growth
  `~2.3-2.5`, area-law geometric boundary `~2.5-3.5`, and now entanglement entropy (follows the boundary,
  static side). DYNAMIC/transport -- spectral `~1.3-1.5`, causal interval-volume `~1.2`, entropy-rate `~1.6`.
  Static probes (how much stuff / boundary) see a higher dimension than dynamic probes (how a walker or signal
  spreads); that gap is the quantitative content of the ramified `b1=1` geometry.
- **`emergence_tree_v0.33.zip`** — superseded by v0.34.
- **HEADLINE RESULT (round 30): the causal graph does NOT give 3+1 spacetime either — its estimators disagree
  (longest-chain ~4.2, cone-volume ~2.3, interval-volume ~1.2), so the causal order is non-manifold.**
  `sec10_general_relativity/s10_1_causal_set_dimension.py` (§10.1). After history-enrichment failed for the
  SPATIAL manifold, the natural move: spacetime dimension lives in the CAUSAL graph (the partial order of
  rewrite events), not the spatial slice. Each event consumes 2 edges (produced by earlier events) and
  produces 3 (consumed by later events); linking producer→consumer builds the causal DAG. Its dimension,
  measured two CALIBRATED ways: **(A) longest-chain** `L~N^{1/d}` (calib recovers d=2→1.86, d=4→3.91) gives the
  keystone `L~N^{0.238}` → **apparent d~4.2, looks like 3+1**; **(B) interval-volume** `V~ell^d` (calib recovers
  d=2→1.93, d=4→2.88) gives the keystone **`V~ell^{1.18}` → CHAIN-LIKE ~1D**. The two calibrated estimators
  **DISAGREE (4.2 vs 1.2)**; a faithful manifold needs them to AGREE, so the causal order is **NON-MANIFOLD** —
  a wide, shallow fan of nearly-parallel ~1D causal chains (height `~N^{1/4}` forces width `~N^{3/4}`). The
  longest-chain "4D" is an **aspect-ratio FALSE POSITIVE**; the interval-volume (`~1.2`) sees the sparse,
  tree-like (`b₁=1`) causal structure and matches the diffusion dimension (`~1.3`). So **3+1 spacetime is NOT
  recovered from the causal graph either**; the same `b₁=1` sparsity that makes the spatial slice a fractal
  tree makes the causal order a non-manifold fan of chains. **Grade: characterization (no leaf change — the
  §10.1 PARTIALs already reflect partial, non-manifold spacetime structure); module attached to §10.1. Tally
  unchanged.** Caught a flaky 2-point longest-chain calibration mid-round → fixed to a 4-point fit;
  interval-volume is the decisive, well-calibrated estimator.
- **METHOD NOTE for next session:** a causal-set / spacetime dimension claim needs ≥2 calibrated estimators
  that AGREE. Longest-chain alone is fooled by aspect ratio (a tall thin fan reads `N^{1/4}` = "4D"); always
  cross-check with interval-volume (`V~ell^d`), which probes local manifold structure. Calibrate every
  estimator on Minkowski sprinklings of known dimension before trusting it on the keystone.
- **THE UNIFYING THEME — d_s and the d_s=2 boundary organize everything (now SEVEN phenomena):** d_s≈1.5
  confines quarks (round 21), keeps the bare continuum a fractal tree (24/25), binds the molecule (26), kills
  the free massless scalar = confinement (27), is a scale-invariant RG fixed point (28), caps history-enriched
  thickening at the marginal d_s=2 (29), and now makes the CAUSAL order non-manifold too — its interval
  dimension (~1.2) matches diffusion (~1.3) and the longest-chain "4D" is an artifact (30). The `b₁=1`
  sparsity is one fact with consequences in space, in the continuum limit, in QFT, in the RG, and in the
  causal/spacetime order: this substrate is too sparse for 3+1 in EVERY structure derived from it.
- **`emergence_tree_v0.32.zip`** — superseded by v0.33.
- **HEADLINE RESULT (round 29): history-enriched geometry does NOT derive 3+1 spacetime — un-cut it is
  small-world, locality-cut it is only a marginal-2D thickened tree.** `sec01.../s1_6_history_enriched_geometry.py`
  (§1.6). A referee doc proposed reaching a spatial manifold by retaining the rule's CONSUMED spokes (the rule
  slides `x→y→z` to the diagonal `x–z` while severing `y–z`) as causal-history memory edges. At one size it
  looks promising (1500 steps: instantaneous `b₁=1, d_s~1.4, diam~45`; all-history `b₁~1150, d_s~2.4,
  diam~10`). But the **diameter-scaling discriminator** (round 25: manifold `diam~N^{1/d}` vs small-world
  `diam~log N`) decides it: **all-history scales as `~log N`** (exponent ≈0.16 ≪ the 1/3 a 3D manifold needs)
  → **small-world, NOT a manifold**. Cause (locality test): ~83% of memory edges are local triangle closures,
  but a thin tail of EARLY consumed spokes whose endpoints drifted apart (to distance ~20) act as long-range
  shortcuts (Watts-Strogatz) — unavoidable. A **locality cutoff** (retain a spoke only if endpoints stay
  within distance D=4) cures the collapse (diameter polynomial again, exponent ≈0.5) — but a random CRT-like
  tree ALREADY scales `~N^{1/2}`, so `b_cut ~ b_inst ~ 1/2`: the cutoff doesn't beat the substrate's
  large-scale geometry, only hanging local loops (`b₁/V~0.6`) on the tree backbone, lifting d_s toward the
  marginal 2 at SHORT scales (the round-28 scale-dependent effect). At most **marginal-2D thickened tree,
  decisively NOT 3D**; pushing further reintroduces the shortcuts. Grade: §1.6 "Effective macrovariables"
  OPEN→**PARTIAL** (effective history-geometry characterized); 3+1 derivation REFUTED for this route. Overlay,
  not the bare rule. **Tally: PARTIAL 121→122, OPEN 102→101.** 3+1 Lorentzian spacetime + the causal/time
  dimension (§10) remain OPEN.
- **METHOD NOTE for next session:** the manifold-vs-mean-field discriminator is DIAMETER SCALING with N
  (`N^{1/d}` polynomial = manifold of dim d; `log N` = small-world). A random CRT-like tree already scales
  `~N^{1/2}`, so a polynomial diameter exponent near 1/2 does NOT by itself prove a 2D manifold — it can be a
  locally-thickened tree; combine with d_s and the running d_s (round 28) to tell uniform-manifold from
  thickened-tree. This caught an over-claim mid-round (don't grade locality-cutoff as a clean "2D manifold").
- **THE UNIFYING THEME — d_s and the d_s=2 boundary organize everything:** d_s≈1.5 confines the quarks (round
  21), keeps the bare continuum a fractal tree (rounds 24/25), binds the molecule (26), kills the free
  massless scalar = confinement (27), is a scale-invariant RG fixed point (28), and now CAPS history-enriched
  thickening at the marginal d_s=2 (29: local closure lifts the tree only to the d_s=2 margin without
  non-local shortcuts; 3+1 not reached). The d_s=2 line is the deconfinement / fractal→manifold / binding /
  massless-scalar / RG-separatrix / history-thickening-ceiling, all at once.
- **Open frontiers:** the INTERACTING correlators (scattering amplitudes, Feynman-diagram analogues, §11.2
  OPEN); non-Abelian gauge structure (§11.3); 3+1 Lorentzian spacetime + the causal/time dimension (§10
  OPEN); coarse-graining flow proper (§11.4); the Standard-Model bridge (§11.5).
- **`emergence_tree_v0.31.zip`** — superseded by v0.32.
- **HEADLINE RESULT (round 28): the running spectral dimension settles to a scale-invariant fractal IR fixed
  point d_s≈1.5 — the substrate is its own coarse-graining fixed point, with NO dimensional flow.**
  `sec11.../s11_4_running_spectral_dimension.py` (§11.4). Reading the local exponent `d_s(t)=−2 d log
  P_return/d log t` along the diffusion time (small t=UV, large t=IR), with 1D/2D controls that come out flat
  (validating the method reads a constant for scale-invariant geometries): the keystone shows a non-universal
  UV crossover settling to a **scale-invariant fractal IR fixed point d_s≈1.5** across a decade. So there is
  **no running of d_s in the IR** (unlike CDT's 4→2 dimensional flow); the long-distance physics is the
  random-tree continuum (round 24), lattice details RG-irrelevant (roughly seed-universal). **Loop structure
  is the relevant coupling** (IR exponent climbs with loop density: 1.30→1.52→1.56), driving toward the
  manifold fixed point past the d_s=2 separatrix — but local nearest-shell loops don't push the IR across 2
  (round 25's crossing was a shorter-scale exponent; a uniform manifold needs loops at every scale; only the
  DIRECTION and the bare IR fixed point are robust, the loop-added exponent being window-sensitive). Grades:
  §11.4 "Scale dependence" PARTIAL→**DERIVED**, "Fixed points" OPEN→**PARTIAL**, SUB OPEN→PARTIAL. **Tally:
  DERIVED 77→78, PARTIAL 121 (unchanged), OPEN 103→102.**
- **THE UNIFYING THEME — d_s (recurrence, d_s<2) and the d_s=2 boundary organize everything:** d_s≈1.5 confines
  the quarks (round 21), keeps the continuum a fractal tree not a manifold (rounds 24/25), binds the meson
  molecule with no threshold (round 26), and makes the propagator IR-divergent so there's no free massless
  scalar — the IR divergence being confinement (round 27); and d_s is a SCALE-INVARIANT RG fixed point (round
  28). The d_s=2 line is simultaneously the deconfinement / fractal→manifold / binding-threshold /
  massless-scalar-existence transition, and the separatrix between the fractal and manifold RG fixed points,
  with loop-density the relevant coupling. One spectral-dimension structure organizes confinement, geometry,
  binding, the propagator, and the RG flow.
- **Open frontiers:** the INTERACTING correlators (scattering amplitudes, Feynman-diagram analogues, §11.2
  OPEN); non-Abelian gauge structure (§11.3); coarse-graining flow proper + continuum effective action
  (§11.4 partially OPEN); §10 GR (curvature Ollivier-Ricci, continuum fractal not Lorentzian); the
  Standard-Model bridge (§11.5).
- **`emergence_tree_v0.30.zip`** — superseded by v0.31.
- **HEADLINE RESULT (round 27): the free scalar propagator on the keystone — there is no free massless scalar
  (the IR divergence is confinement), and a mass gaps it.** `sec11.../s11_2_propagator_and_spectral_density.py`
  (§11.2, also §11.1). The natural free field is the Gaussian theory of the rule's Laplacian (round 3);
  propagator `G_m(x,y)=⟨x|(L+m²)⁻¹|y⟩=Σ_t e^{−m²t}p(x,y;t)`, fixed by the spectral density `ρ(E)~E^{d_s/2−1}`.
  d_s≈1.4–1.5<2 ⇒ ρ(E) diverges as E→0. Consequences: (i) **no free massless scalar** — `G_m(x,x)=Σ_t
  e^{−m²t}P_return(t)` diverges as m→0 (massless sum = divergent return sum, recurrence), scaling
  (m²)^{d_s/2−1}=m^{d_s−2}; the IR divergence IS confinement; (ii) the **regularized massless 2-pt function
  is the linear potential** — on the tree R(x,y)=graph distance, so R(r)~r (rising string, not Coulomb);
  (iii) a **mass gaps the IR** — G_m finite for m>0, finite correlation length; as m→0 the gap closes. A
  propagating massless scalar would need d_s>2 (the manifold phase, round 25). Grades: §11.2
  "Green-function analogues" OPEN→**DERIVED** (free Green's function + IR structure, native from the Laplacian
  heat kernel); §11.1 "Correlation functions" OPEN→**PARTIAL** (free 2-pt done; interacting OPEN); SUB 11.2
  OPEN→PARTIAL. **Tally: DERIVED 76→77, PARTIAL 120→121, OPEN 105→103.**
- **THE UNIFYING THEME — d_s≈1.5 (recurrence, d_s<2) now does FIVE things:** confines the quarks (round 21);
  keeps the continuum a fractal tree not a manifold (rounds 24/25); binds the meson molecule with no
  threshold (round 26); makes the spectral DOS IR-divergent so there's no free massless scalar — the IR
  divergence being confinement (round 27); and the d_s=2 boundary is simultaneously the deconfinement /
  fractal→manifold / binding-threshold / massless-scalar-existence transition. One spectral-dimension
  boundary organizes confinement, geometry, binding, and the propagator.
- **Open frontiers:** the INTERACTING correlators (scattering amplitudes, Feynman-diagram analogues, §11.2
  still OPEN — the free propagator is done, the interacting theory is not); non-Abelian gauge structure
  (§11.3); §10 GR (curvature Ollivier-Ricci, continuum fractal not Lorentzian); §11.4 renormalization flow.
- **`emergence_tree_v0.29.zip`** — superseded by v0.30.
- **HEADLINE RESULT (round 26): the round-22 string-flip attraction binds a meson molecule / tetraquark,
  guaranteed by recurrence (d_s<2) — the same property that confines the quarks.**
  `sec04.../s4_6_tetraquark_binding.py` (§4.6). A short-range attraction binds for arbitrarily weak coupling
  iff the zero-energy Green's function `G(0)=Σ_t P_return(t)` diverges, iff recurrent, iff d_s≤2
  (Economou-Cohen / the Pólya boundary, same as confinement). Measured: keystone (d_s≈1.5) G(T) grows
  (recurrent) → threshold 1/G(0)→0 (no threshold); 3D (d_s=3) G saturates → finite threshold ~0.34; at a
  weak well (V0=0.2) the keystone BINDS (E_b>0) while 3D does not. So the attraction always binds a molecule
  on the keystone — but d_s≈1.5 just below the marginal 2 makes G(0) diverge slowly, so the binding is
  **shallow**: a loosely-bound, extended molecule (two color singlets, the two flux-tube pairings mixed = a
  genuine four-quark state in the molecular regime), NOT a compact tetraquark (which would need stronger
  attraction or lower d_s). Status PARTIAL (conditional: the recurrence→no-threshold-binding step is rigorous
  and native; the attraction is the round-22 overlay; binding shallow; no native leaf claimed). **Tally
  unchanged.**
- **UNIFYING THEME — recurrence (d_s<2) does four things:** (1) confines the quarks (round 21: V(L)=R(L)
  grows iff recurrent); (2) keeps the continuum a fractal tree, not a manifold (rounds 24/25: manifold needs
  d_s>2, reachable only by local loop-closure); (3) binds the meson molecule with no threshold (round 26);
  and the d_s=2 boundary itself is the deconfinement / fractal→manifold / binding-threshold transition. One
  spectral-dimension boundary organizes confinement, geometry, and binding.
- **THE EMERGING PICTURE:** one rewrite rule → a growing tree (continuum = random fractal tree at d_s≈1.5,
  NOT a manifold) of massless chiral Weyl fermions (mass an irreducible Higgs-like input) whose ±v0 zigzag
  reproduces the Dirac equation (E²=p²+m², v=p/E, zitterbewegung, time dilation) → confined into unbreakable
  mesons on Regge trajectories → short-range string-flip nuclear force (rearrangement scattering) that binds
  shallow meson molecules; particle number conserved; all of confinement/geometry/binding governed by the
  d_s=2 recurrence boundary. Irreducible inputs: β and mass/handedness; plus the continuum prescription.
  **Open frontiers:** the deeper §11 QFT layer (propagators, correlators still OPEN); §10 GR (curvature
  Ollivier-Ricci, continuum fractal not Lorentzian); whether a stronger/native attraction could give a
  compact tetraquark.
- **`emergence_tree_v0.28.zip`** — superseded by v0.29.
- **HEADLINE RESULT (round 25): minimal LOCAL loop-closure pushes the substrate across d_s=2 into a
  finite-dimensional manifold-like phase; random loops give mean-field; neither is native.**
  `sec01.../s1_6_manifold_phase_transition.py` (§1.6). The bare rule conserves b₁=1 (tree, sub-2D fractal),
  so a manifold needs added loops — and HOW matters. (1) **Local loop-closure** (edges between nodes at small
  tree-distance r — closing r=2 elbows into triangles): d_s rises smoothly and **crosses 2** at modest
  density (r=2 → d_s≈2 at p≈0.5), the **diameter stays large** (~N^{1/d}, polynomial), and range tunes the
  dimension (r=2→d_s≈2, r=3→d_s≈2.8). A finite-dimensional, manifold-like phase. (2) **Random long-range
  edges**: d_s → ∞ (3.8, 5.2…) and the **diameter collapses** toward log N (~8) — mean-field/small-world,
  NOT a manifold. So crossing d_s=2 is easy, but manifold (finite-dim, large diameter) vs mean-field
  (collapsed) depends on **locality**: a manifold needs local connectivity against a metric. The keystone
  supplies the metric (graph distance) but not the closure (b₁=1), so the manifold phase is reachable by
  **one local rule addition** — in principle, not natively (consistent with round 24). Status PARTIAL
  (constructive; conditional on non-native structure; no native leaf claimed). **Tally unchanged.**
- **THE EMERGING PICTURE & PHASE DIAGRAM:** a single rewrite rule → a growing tree whose continuum is a
  random fractal tree at d_s≈1.5 (NOT a manifold); the d_s=2 boundary (= the Pólya recurrence/confinement
  threshold of §6) separates this fractal/confining phase from a manifold phase (reachable only by local
  loop-closure) and a mean-field phase (random loops). The matter sector on the fractal substrate: massless
  chiral Weyl fermions (mass an irreducible Higgs-like input) whose ±v0 zigzag reproduces the Dirac equation
  (E²=p²+m², v=p/E, zitterbewegung, time dilation) → confined into unbreakable mesons on Regge trajectories
  → short-range string-flip nuclear force (rearrangement scattering); particle number conserved. Irreducible
  inputs: β and mass/handedness; plus the continuum prescription. **Open frontiers:** a tetraquark/meson
  molecule; deeper §11 QFT (propagators/correlators OPEN); §10 GR (curvature Ollivier-Ricci, continuum
  fractal not Lorentzian).
- **`emergence_tree_v0.27.zip`** — superseded by v0.28.
- **HEADLINE RESULT (round 24): the keystone's continuum limit is a random fractal tree (Lévy/CRT class),
  NOT a Riemannian/Lorentzian manifold.** `sec01.../s1_6_continuum_fractal_tree.py` (§1.6). The substrate is
  one loop in a growing tree (b₁=1 conserved; 2-core a vanishing fraction), so its scaling limit is a random
  REAL tree. The three diffusion dimensions — Hausdorff d_H (volume `N(r)~r^{d_H}`), spectral d_s (return
  `P0(t)~t^{-d_s/2}`), walk d_w (`<r²>~t^{2/d_w}`) — measure NON-integer with **d_s < d_H < d_w** (a smooth
  d-manifold gives the integer triple (d,d,2) with d_s=d_H) and satisfy the fractal **Einstein relation
  d_s=2d_H/d_w**. Measured: d_H≈2.4 (robust across seeds), d_s≈1.5, d_w≈3.2. Universality class = random
  fractal trees (Lévy/CRT): Aldous's CRT has exactly (2, 4/3, 3); the keystone's larger d_H points to a
  stable tree α=d_H/(d_H−1)≈1.7 (exact member unpinned at finite size). **Hauptvermutung verdict:** a
  continuum exists and is essentially unique but is fractal, NOT a manifold — the bare rule does not smooth
  into Euclidean/Lorentzian spacetime; a manifold phase would need the 2-core to dominate (it provably does
  not, b₁=1; cf. the d_s>2 deconfinement boundary, §6). Grade: §1.6 "Continuum limits" PARTIAL→**DERIVED**
  (qualitative characterization robust; exact dimensions carry finite-size uncertainty ±0.1–0.3). **Tally:
  DERIVED 75→76, PARTIAL 121→120.**
- **THE EMERGING PICTURE:** a single rewrite rule → a growing tree vacuum whose continuum limit is a random
  fractal tree (not a manifold) holding massless chiral Weyl fermions (mass an irreducible Higgs-like input)
  whose ±v0 zigzag reproduces the Dirac equation (E²=p²+m², v=p/E, zitterbewegung, time dilation) → confined
  into unbreakable mesons on Regge trajectories → interacting via a short-range string-flip nuclear force
  (rearrangement scattering); particle number absolutely conserved; confinement = recurrence of the
  substrate's diffusion (deconfines above d_s=2). Irreducible inputs: β and mass/handedness; plus the
  continuum prescription. **Open frontiers:** a meson "molecule"/tetraquark bound state; deeper §11 QFT
  (propagators, correlators OPEN); §10 GR (curvature is Ollivier-Ricci, the continuum is fractal not
  Lorentzian); whether any extra structure yields a manifold phase (more loops / d_s>2).
- **`emergence_tree_v0.26.zip`** — superseded by v0.27.
- **HEADLINE RESULT (round 23): the relativistic dispersion E²=p²+m², the relativistic velocity v=p/E, and
  time dilation all EMERGE from the zigzag — round 14's hand-assumed `v=p/√(1+p²)` is now derived.**
  `sec07.../s7_4_zitterbewegung_dispersion.py` (§7.4, also attached to §7.3). The `±v0` zigzag (rounds 13–14)
  taken as a discrete quantum walk — SHIFT (R hops +1, L hops −1) + mass coin `C=[[cos m,i sin m],[i sin m,
  cos m]]` (coin angle m = the irreducible Weyl→Dirac mass input, round 16) — is the Feynman checkerboard.
  Its dispersion is a theorem: `det U(k)=1`, `2 cos E = tr U = 2 cos k cos m`, so **`cos E = cos k cos m` ⇒
  `E²=p²+m²`** (verified to 3–4 digits; `m=0` ⇒ luminal Weyl `E=k`). Group velocity `v=dE/dk=p/E`
  (relativistic, sub-luminal, →v0 as m→0). Zitterbewegung: a single-chirality state trembles between `±v0`
  (band interference) while drifting at `p/E`. **Time dilation:** the bands at `±E` make the trembling a
  clock at the gap `2E=2γm` (measured freq tracks 2E at low momentum) with proper rate fixed at `2m`, so
  `dτ/dt=m/E=1/γ`. Grades: §7.4 "Mass-energy relation" BORROWED→**DERIVED**; §7.3 "Time dilation"
  BORROWED→**PARTIAL**. Mass *value* stays an irreducible input; only its *kinematics* is now the Dirac
  equation. **Tally: DERIVED 74→75, PARTIAL 120→121, BORROWED 17→15.**
- **THE EMERGING PICTURE (matter sector, end-to-end):** massless chiral Weyl fermions (mass an irreducible
  Higgs-like input) whose `±v0` zigzag, as a quantum walk, reproduces the Dirac equation — dispersion
  `E²=p²+m²`, sub-luminal `v=p/E`, zitterbewegung, time dilation → confined into unbreakable mesons on Regge
  trajectories → interacting via a short-range string-flip nuclear force (rearrangement scattering); particle
  number absolutely conserved; confinement = recurrence of the substrate's diffusion (deconfines above
  `d_s=2`). Irreducible inputs: β and mass/handedness; plus the continuum limit. **Open frontiers:** the
  continuum limit / Hauptvermutung; a meson "molecule"/tetraquark bound state; deeper §11 QFT (propagators,
  correlators); §10 GR (curvature is Ollivier-Ricci, not yet Lorentzian).
- **`emergence_tree_v0.25.zip`** — superseded by v0.26.
- **HEADLINE RESULT (round 22): the force between two color-neutral mesons mirrors the QCD nuclear force.**
  `sec04.../s4_6_meson_meson.py` (§4.6). The free S-matrix is trivial (round 19), so the only nontrivial
  dynamics is between confined states. (1) **No long-range force; range = meson size.** Two neutral mesons
  feel exactly **zero** residual force beyond ~2L (L = flux-tube length): measured `L=2 → range ~4`,
  `L=5 → range ~10`. Confinement screens the force (a color singlet has no long-range field), so it is
  strictly short-range with range set by the hadron size — like the nuclear force, unlike Coulomb. (2)
  **Short-range attraction from flux-tube recombination (string flip).** Within range, the four charges
  re-route their two tubes (original vs recombined pairing, whichever is shorter); overlap favors
  recombination (gain to `~-0.9σ`, peak at `R~L`) — the string-flip model of the nuclear force (singlets
  attract by swapping quarks). (3) **Scattering is REARRANGEMENT** — the recombined state is two different
  mesons (quarks swapped), up to ~30% of close encounters; t-channel quark exchange, characteristic of
  confining theories. Status PARTIAL (tree distances native; "no force beyond 2L" from geometry + neutrality;
  the energy/string-flip is the overlay/model; scattering inferred from static energetics). **No leaf
  changed** (tally: DERIVED 74, PARTIAL 120, OPEN 105, REFUTED 4).
- **THE EMERGING PICTURE (now end-to-end for the matter sector):** massless chiral Weyl fermions (mass an
  irreducible Higgs-like input) → confined into unbreakable mesons on Regge trajectories → interacting via a
  short-range string-flip nuclear force (rearrangement scattering); particle number absolutely conserved;
  confinement = recurrence of the substrate's diffusion (deconfines above `d_s=2`). Irreducible inputs: β and
  mass/handedness; plus the continuum limit. **Open frontiers:** whether E²=p²+m² emerges from the
  zitterbewegung zigzag; the continuum limit; a possible meson "molecule"/tetraquark bound state.
- **`emergence_tree_v0.24.zip`** — superseded by v0.25.
- **HEADLINE RESULT (round 21): the confinement/deconfinement transition is Pólya's recurrence/transience
  boundary at spectral dimension 2.** `sec06.../s6_3_deconfinement_dimension.py` (§6.3). The static potential
  `V(L)=R(L)` grows (confining) **iff the substrate's random walk is recurrent**, which by Pólya holds **iff
  `d_s ≤ 2`**. Measured (spectral dim from return prob `P0(t)~t^(-d_s/2)`, resistance by relaxation): 1D
  `d_s≈1.0` `R~L` (linear, confine); 2D `d_s≈2.0` `R~log L` (marginal); 3D `d_s≈2.5–3` `R→const` (Coulomb,
  deconfined); **keystone `d_s≈1.0` (tree-like) `R~L` → CONFINING.** So the keystone confines because its
  geometry is sub-2D in transport (recurrent walks); a >2D substrate deconfines (round 6). **Confinement is
  not a strong coupling — it is the recurrence of the rule's own diffusion** (the flux can't escape a
  recurrent geometry). Status PARTIAL (spectral dims & resistance measured — keystone native, lattices as
  comparison; the potential reading uses the overlay; the rule is charge-blind). **No leaf changed** (tally:
  DERIVED 74, PARTIAL 120, OPEN 105, REFUTED 4).
- **THE EMERGING PICTURE:** a growing tree vacuum with a growing/coalescing 2-core of matter (massless chiral
  Weyl fermions; mass an irreducible Higgs-like input); charges confined into unbreakable mesons on Regge
  trajectories; particle number absolutely conserved; confinement = recurrence of the substrate's diffusion
  (deconfines above `d_s=2`). Irreducible inputs: β and mass/handedness; plus the continuum limit. **Open
  frontiers:** meson–meson scattering; whether E²=p²+m² emerges from the zitterbewegung zigzag; the
  continuum limit.
- **`emergence_tree_v0.23.zip`** — superseded by v0.24.
- **ROUND 20 — addressed six referee threads on the tree/confinement picture; two CORRECT earlier claims.**
  `sec11.../s11_1_loop_defects_and_vacuum.py` (new), plus edits to `s6_3_confinement_flux_tube.py` and
  `s4_3_dirac_mass_obstruction.py`.
  - **(1) Generalized ICs:** `b₁=0` (a path) stays a pure tree forever → **the vacuum is a pure tree, no
    matter**; for `b₁=1,2,3` the non-loop part is 96–100% of nodes (tree-like vacuum always).
  - **(2) Two-core bound — CORRECTED:** the round-17 "bounded 2–11" was a short-run artifact; the 2-core
    **grows sub-linearly** (`~steps^0.4`, `7.5→13.5→22.7` at `500→2000→8000`) — NOT bounded — but `loop/V→0`,
    so matter is a **vanishing fraction** of the universe, not a fixed-size particle.
  - **(3) Multi-defect interactions:** two loops started far apart **coalesce** (attract/fuse) into one
    2-core cluster; they do not stay independent (`b₁` stays 2 — they fuse, never annihilate).
  - **(4) String breaking — already done:** `b₁` exactly conserved → no loop-pair creation → string can't
    break (the sharp QCD distinction).
  - **(5) Native vs overlay — sharpened:** the bare rule is **charge-blind** (redexes depend on the edge
    multiset alone, round 5), so it cannot feel the tube; the flux-tube PATH is native, the confining
    force/energy is **irreducibly overlay**.
  - **(6) Reproducible chirality search:** the bounded reversal search now runs **live** in
    `s4_3_dirac_mass_obstruction` (2 types × 2500 states default; `EMERGENCE_FULL=1` → 4 × 6000) →
    reversal found = False (the Weyl obstruction is tested, not asserted).
  - **Grades:** §11.1 **Vacuum state → DERIVED** (pure tree); **Creation/annihilation analogues → REFUTED**
    (definitively absent — `b₁` conserved, a superselection rule). Tally: **DERIVED 73→74, PARTIAL 121→120,
    OPEN 106→105, REFUTED 3→4.**
- **THE EMERGING PICTURE (refined):** a growing tree vacuum holding a small *growing, coalescing* 2-core of
  matter (massless chiral Weyl fermions; mass an irreducible Higgs-like input); charges confined into
  unbreakable mesons on Regge trajectories; particle number absolutely conserved (no pair processes).
  Irreducible inputs: β and mass/handedness; plus the continuum limit. **Open frontiers:** meson–meson
  scattering; the deconfinement/dimension boundary; whether E²=p²+m² emerges from the zitterbewegung zigzag.
- **`emergence_tree_v0.22.zip`** — superseded by v0.23.
- **HEADLINE RESULT (round 19): the substrate's S-matrix is strongly constrained — particle number is
  conserved (no annihilation), and free gliders don't collide.** `sec04.../s4_6_scattering.py` (§4.6).
  (1) **Particle number conserved (topological protection).** `Δb₁ = ΔE − ΔV = 0` every firing → loop
  number (the matter quanta, round 17) is an absolute conserved charge (verified for b₁=1,2,3 over 500
  random firings): **no pair creation, no annihilation, matter perfectly stable** — a superselection rule
  *stronger* than the Standard Model's, and the same law behind the unbreakable string (round 18). (2)
  **Free-glider S-matrix trivial.** Single speed → **co-propagating gliders move in lockstep** (separation
  measured exactly constant, never interact); uni-chirality → **counter-propagating gliders pin** at the
  orientation wall (both stop, never reach each other). No 2→2 collision scattering. (3) **Interactions are
  field-mediated; asymptotic states are mesons.** Glider-through-potential gating (round 7, Boltzmann
  transmission); charges confined (round 18) → in/out states are neutral mesons, not free charges (as in
  QCD). Status PARTIAL (b₁ conservation DERIVED-native; lockstep/pinning native-measured; field scattering +
  meson asymptotics overlay). **No leaf grade changed** (tally: DERIVED 73, PARTIAL 121, OPEN 106, REFUTED 3).
- **THE EMERGING PICTURE:** one wandering loop of matter in a growing tree; matter = massless chiral Weyl
  fermions (mass an irreducible Higgs-like input); charges confined into mesons on Regge trajectories;
  particle number absolutely conserved (no pair processes). The two irreducible inputs are β and
  mass/handedness; plus the continuum limit. **Open frontiers:** meson–meson (string–string) scattering;
  the deconfinement/dimension boundary; whether E²=p²+m² emerges from the zitterbewegung zigzag.
- **`emergence_tree_v0.21.zip`** — superseded by v0.22.
- **HEADLINE RESULT (round 18): the bound states of the confining force are MESONS — pure-linear,
  unbreakable strings on linear Regge trajectories.** `sec04.../s4_5_mesons_confined_bound_states.py` (§4.5).
  (1) **Pure-linear potential, no Coulomb piece.** A ± charge pair (ρ=in−out) at separation r has energy
  `V(r)=R(r)=σ·r` with intercept ~0 — no short-range `−a/r` (a tree has no short-range alternative paths,
  unlike QCD's Cornell potential). (2) **Unbreakable string.** Massless Weyl matter (round 16) has no
  pair-creation channel, so the tube never screens/breaks: `V=σr` for ALL r. (3) **Flux tube** = the
  one-edge-wide tree geodesic, uniform tension; the meson is neutral and bound (isolating a charge costs
  `~σr→∞`). (4) **Spectrum:** virial `2⟨T⟩=⟨V⟩` (linear, vs Kepler's `−⟨V⟩`); radial Airy tower
  `M_n~σ^{2/3}m^{−1/3}`; and the **Regge trajectory** `J = M²/(2πσ)` (spin ∝ mass², slope `α'=1/(2πσ)`) from
  a rotating relativistic string whose ends move at the substrate's universal speed `v0` — built from two
  native ingredients (confining tension σ + the one speed limit). **Inverse-square / Kepler are REFUTED** on
  the native tree geometry (recovered only on a 3D lattice, round 6). Status PARTIAL (the linear potential
  and flux tube are native-measured; the energy/spectrum use the field-energy overlay; the Regge step is
  string mechanics on the native (σ, v0)). Tally: §4.5 OPEN(5) → Inverse-square REFUTED, Kepler REFUTED,
  Orbital-trajectories PARTIAL, Virial PARTIAL, Radial-symmetry OPEN; net **PARTIAL 119→121, OPEN 110→106,
  REFUTED 1→3** (EXPECTED_TALLY updated; the Regge addition changed no leaf).
- **THE EMERGING PICTURE (unchanged in kind):** the keystone universe = one small wandering loop (matter) in
  a growing tree (vacuum); matter = massless chiral Weyl fermions (mass an irreducible Higgs-like input,
  round 16); charges confined by flux tubes into mesons on Regge trajectories (round 18). The two irreducible
  inputs are β and mass/handedness; plus the continuum limit. Remaining native targets: scattering/many-body
  (§4.6); the deconfinement/dimension relation; whether E²=p²+m² emerges from the zitterbewegung zigzag.
- **`emergence_tree_v0.20.zip`** — superseded by v0.21.
- **HEADLINE RESULT (round 17): the keystone universe is ONE LOOP IN A TREE, which forces QCD-like
  confinement.** `sec06.../s6_3_confinement_flux_tube.py`. (1) **One loop in a tree.** b1 is conserved
  (round 1); from the triangle it stays **b1 = 1 forever** (verified: undirected edges == nodes at all
  sizes → a spanning tree + one edge). That single loop is the lone **matter particle**: a small *bounded*
  cycle (length 2–11, never growing) that *wanders* through an ever-growing tree of vacuum. (2)
  **Confinement / flux tube.** Tree-like ⇒ `R(a,b)` = graph distance (series resistors, R/d~0.93–0.98) ⇒
  **linear potential, constant string tension**; the current concentrates on `~d` of hundreds of edges = a
  **flux tube** on the unique tree geodesic. (3) **QCD scenario:** **no free charge** (isolating one costs
  `~tension·distance` → ∞); **physical spectrum = neutral states only** (the photon = neutral 2-cycle,
  s6_7; neutral pairs); **phase is substrate-specific** — a 3D lattice deconfines to Coulomb (s6_3), the
  keystone confines because its geometry is tree-like (b1=1, `d_s~1.3<2`). **Confinement is geometry, not a
  coupling.** Status PARTIAL (the tree/flux-tube facts are native-measured; the energy/tension reading uses
  the s6_3 field-energy overlay); **no leaf grade changed** (tally: DERIVED 73, PARTIAL 119, OPEN 110).
- **THE EMERGING PICTURE.** The keystone universe = one small wandering loop (matter) in a growing tree
  (vacuum); charges confined by flux tubes; matter = massless chiral Weyl fermions (round 16); the two
  irreducible inputs are β (EM coupling) and mass/handedness (the Higgs-like L↔R coupling); plus the
  continuum limit. Remaining native targets: §4.5 bound states in the confining potential ("mesons"); the
  deconfinement/dimension relation; §11 topological matter (numpy).
- **`emergence_tree_v0.19.zip`** — superseded by v0.20.
- **HEADLINE RESULT (round 16): trying to derive the Dirac mass term -> a structural obstruction; the
  keystone is a chiral (Weyl) world.** `sec04.../s4_3_dirac_mass_obstruction.py`. Round 14 showed mass =
  zitterbewegung with one missing ingredient: a chirality flip (the Dirac mass term coupling `±v0`
  movers). Attacking it directly: (1) **the rule is CHIRAL** — for a path `x→y→z` it writes
  `((x,z),(y,x),(z,w))`, treating head/tail asymmetrically; applied to a path vs its reverse it gives
  mirror images, never the same structure (a fixed handedness — the glider inherits it, uni-chiral). (2)
  **No native L↔R coupling exists:** end-to-end junctions **pin** the glider (a 6000-state search across
  boundaries, domain walls, and 5 junction/defect types finds no reversal); side-by-side rungs (the
  natural mass term) **delocalize** it (2-core jumps from 2 to the whole ladder, size 24). (3)
  **Conclusion — a WEYL world:** the keystone gives massless single-chirality gliders; a Dirac mass term
  is an **irreducible input**, joining the rule's handedness and `β`. **Mirrors the Standard Model
  exactly:** chiral fermions get mass from a Higgs/Yukawa coupling, not the kinetic term. Status OPEN (a
  characterized obstruction from a bounded search, not a proof of impossibility); **no leaf grade changed**
  (tally unchanged: DERIVED 73, PARTIAL 119, OPEN 110).
- **DEEP STATE OF THE PROGRAM:** the mechanics frontier resolved in a deep way — `F=ma` is not blocked by
  "no force" (it exists) but by mass being an **irreducible input** (the substrate is a massless chiral
  world; the zitterbewegung model shows any granted mass input closes §4.2/§4.3). The two irreducible
  inputs are now `β` (EM coupling) and mass/handedness (the Higgs-like L↔R coupling); plus the continuum
  limit. Remaining native targets: §4.5 orbits (field is local + radiative); §11 topological matter (numpy).
- **`emergence_tree_v0.18.zip`** — superseded by v0.19.
- **ROUND 15 — incorporated an external investigation and attacked the round-14 frontier.**
  - **PHOTON = a chargeless gauge loop** (`s6_7_photon_and_radiation.py`, §6.7). A neutral 2-cycle
    `(v,w,φ),(w,v,−φ)` on a fresh node has holonomy **exactly 0 for any φ** (verified; basis-independent) →
    no charge, no static force: a massless, chargeless gauge excitation. **Honest correction** to the
    source note: it inferred "Wilson-energy-free" from a spanning-tree Wilson action `S`, but `S` over a
    spanning-tree basis is **basis-dependent** (varies under edge reordering — shown), so a graph Wilson
    "energy" is ill-defined; the robust invariant is the holonomy/charge.
  - **Static force = emergent-graph effective resistance** (added to §6.3). Confirms round 6 on a larger
    graph (653 nodes): `R(d) ~ d^0.985` → confining. **Clarified:** the exponent `~1` is set by the
    *transport (spectral)* dimension `d_s~1.3`, NOT Hausdorff `D~2.3` (a naive `R~d^{2-D}` with Hausdorff
    wrongly predicts saturation, slope `−0.3`).
  - **§6.7 radiation consolidated** to PARTIAL (wave equation, propagation speed, radiation from
    accelerating charges, Poynting flux) — rounds 10-11 had shown these on an auxiliary lattice but §6.7
    was still all-OPEN. Polarization, Dispersion remain OPEN.
  - **Native chirality reversal — NEGATIVE (the round-14 frontier).** Driven into a hard boundary the
    glider **pins** (no left-move possible, no rightward move exists); into an orientation domain wall it
    pins at the wall. It does **not** reflect: the glider is robustly **uni-chiral**. So the zitterbewegung
    flip (the Dirac mass term) is not provided by simple rail features and stays a model — a clean negative
    sharpening rounds 13-14. (`s4_3_mass_as_zitterbewegung.py`, reversal-attempt added.)
  - Tally: PARTIAL 115→119, OPEN 114→110 (the §6.7 corrections; photon and negative add no leaves).
- **TOP OPEN ITEM (unchanged in kind):** a **native chirality reversal** mechanism (the Dirac mass term
  from the rule) — now known *not* to come from boundaries or simple orientation walls; candidates are
  glider–glider (left+right) interaction or a more structured reflector. Then §4.5 orbits.
- **`emergence_tree_v0.17.zip`** — superseded by v0.18.
- **HEADLINE RESULT (round 14): mass = zitterbewegung — the single causal speed FORCES a massive particle
  to be a zigzagging glider (Feynman checkerboard / Dirac).** `sec04.../s4_3_mass_as_zitterbewegung.py`.
  Two **measured native facts**: (A) **both chiralities exist at `v0`** — the glider runs `−v0` on a rail
  `i→i+1` and `+v0` on the mirror rail `i+1→i` (verified velocities `−1`, `+1`; the rule's mirror symmetry);
  (B) **`v0` is the only speed** (round 13). These *force* the conclusion: a sub-luminal particle (in
  particular one at rest) cannot sit at an intermediate speed — it must **zigzag between `±v0`**, its lower
  velocity the average of genuine `±v0` motion. Demonstrated (as averages of real `±v0` steps): (1) **rest
  mass = zigzag rate** (no flips → massless at `v0`; flips → trembles in place, at rest); (2) **sub-luminal
  & relativistic for free** — a chirality bias drifts but `|⟨v⟩| < v0` always (can't average `±1` past 1),
  asymptoting to `v0`; (3) **`a~F`** — a force changing a persistent chirality-momentum (`F=dp/dt`) makes
  `⟨v⟩` grow (0.41→0.84→0.92), asymptote to `v0`, and persist (inertia). **Unlike the round-13 overlay**,
  the sub-luminal velocity and the `v0` ceiling are *grounded in native `±v0` motion*, not asserted — the
  relativistic limit is automatic. NATIVE: both chiralities + the single speed. CONSTRUCTED: the
  chirality-flip dynamics (the Dirac mass term) and the force coupling — a model, **no leaf grade inflated**
  (tally unchanged). This connects the substrate to the 1D Dirac equation and resolves the round-13 puzzle.
- **NEW TOP OPEN ITEM:** a **native chirality reversal** — a glider that *natively* flips `±v0` (e.g.
  bouncing off a rail orientation domain wall) would make the zigzag (hence mass and `a~F`) native rather
  than a model, and close §4.2/§4.3. Then §4.5 orbits. Mechanics frontier: the **Dirac mass term from the
  rule** (a native reversal mechanism).
- **`emergence_tree_v0.16.zip`** — superseded by v0.17.
- **HEADLINE RESULT (round 13): why the force is overdamped — the native glider is a fixed-speed soliton —
  and what `a~F` needs.** `sec04.../s4_3_inertia_and_acceleration.py`. The minimal 2-cycle glider advances
  one rail-node per 2-move at the causal speed `v0`; the field can only **gate** it (`P(F)=1/(1+exp(βΔE))`,
  `v=P·v0`). Measured: (1) **constant force → constant velocity** (overdamped `v~F`, no acceleration); (2)
  **fixed-speed ceiling = `v0`** — velocity saturates at 1 node/tick however strong the force ("massless-
  like"; `v0` a universal speed limit); (3) **no velocity memory** — drive hard, cut force, `v` drops to
  baseline instantly. So the native force is **Ohmic/overdamped because the glider has no velocity state**
  — a precise obstruction to `F=ma`, a negative in the spirit of round 5. **What `a~F` needs:** a velocity-
  **carrying** ("massive") excitation with persistent momentum `p` the force changes (`F=dp/dt`); with the
  relativistic map `v=p/√(1+p²)` it accelerates (`a~F`: 0.30→0.66→0.83), asymptotes to `v0` (a massive
  particle is relativistic for free), and the velocity persists when force is removed (inertia); inertial
  mass `m=1/α`. This is a **postulated overlay**, not native. Resistance-to-acceleration (§4.3) OPEN →
  PARTIAL (characterized: native obstruction + overlay path). Tally OPEN 115→114, PARTIAL 114→115.
- **NEW TOP OPEN ITEM:** a **native massive excitation** — a structured glider carrying a persistent
  *sub-luminal* speed the force can advance, which would make `a~F` native (rather than a momentum overlay)
  and complete §4.2/§4.3. Then §4.5 central-force/orbits (field is now local + radiative). The mechanics
  frontier is now sharply stated: not "find the force" (it exists) but "build a genuinely massive,
  accelerable, sub-luminal particle."
- **`emergence_tree_v0.15.zip`** — superseded by v0.16.
- **HEADLINE RESULT (round 12): Maxwell is closed — and its shape is three identities + two equations of
  motion.** `sec06.../s6_5_continuity.py` derives the last equation, **continuity** `∂_tρ+∇·J=0`, as the
  same `d²=0`: (a) FIELD level — `div` of Ampère's `(∂_yB,−∂_xB)` is `∂_x∂_yB−∂_y∂_xB = 0` (mixed partials
  commute), verified 5.6e-17 for arbitrary `B`; (b) RULE level — the structural charge `ρ=in−out` is
  conserved by the bare keystone *locally* (40 random firings: worst `|Σ Δρ|=0`, worst out-of-`{x,y,z,w}`
  change `=0`), so a conserved local current exists. Continuity → **DERIVED**; §6.2 charge-current
  continuity → **DERIVED**; §6.5 OPEN → **PARTIAL**. **THE CLOSING SHAPE:** three of Maxwell's relations
  are kinematic **IDENTITIES** (no-monopole `∇·B=0`, Faraday `∇×E=−∂_tB`, continuity `∂_tρ+∇·J=0` — all
  `d²=0` from `F=dA`, all **DERIVED**); two are the dynamical **EOM** `d⋆F=J` (Gauss `∇·E=ρ`, Ampère
  `∇×B=J+∂_tE` — both **PARTIAL**, resting on the one field action whose coupling `β` is independent within
  the construction, r9). EM is closed as far as it can be: kinematic half fully DERIVED, dynamical half PARTIAL and
  reduced to one number. Also tightened Ampère (Gauss-Seidel, circulation 0.982). Tally DERIVED 71→73,
  OPEN 117→115. Whitepaper §3 (flow invariants) + §6 updated.
- **MAXWELL STATUS NOW (CLOSED):** Gauss PARTIAL, no-monopole DERIVED, Faraday DERIVED, Ampère PARTIAL,
  continuity DERIVED. The field is local/retarded (r10), an accelerating charge radiates (r11). The
  classical hierarchy §1–§6 is now substantially built.
- **NEW TOP OPEN ITEM:** **inertial F = m a** — the one remaining classical-mechanics gap; round 7's
  force is OVERDAMPED drift (v∼F), and lifting it to genuine acceleration (a∼F) would complete §4.2/§4.3.
  Then §4.5 central-force / orbit tests (the field is now local + radiative). Off the force track: the
  §11 topological-matter block (optional, numpy).
  Force/EM arc (now complete): REFUTED (r5) → static law (r6) → force ON MATTER (r7) → coupling DERIVED
  to one constant (r8) → β IRREDUCIBLE (r9) → field LOCAL/retarded (r10) → magnetic sector + Faraday =
  Bianchi + radiation (r11) → **continuity + Maxwell closed (r12)**.
- **`emergence_tree_v0.13.zip` (round 11):** the magnetic sector. `s6_4_magnetic_and_induction.py`:
  Faraday `∇×E=−∂_tB` is `d²=0` (exact to 4.4e-16, the same identity that forbids monopoles), so the two
  *homogeneous* Maxwell equations are automatic from `B=dA`; Faraday + Curl-operators → DERIVED. A wire's
  current sources a circulating B (Ampère, PARTIAL); an oscillating dipole radiates (causal outward flux,
  PARTIAL). Superseded by v0.14.
- **HEADLINE RESULT (round 10): the force is now LOCAL (retarded); electrostatics is its static limit.**
  Round 9's honesty debt was that the round-6/7 force used the *instantaneous* global field energy
  (non-local). `sec06.../s6_5_retarded_field.py` pays it: a local field `φ` obeys a discrete damped-wave
  (telegrapher) equation `φ[t+1]=(2−g)φ[t]−(1−g)φ[t−1]−h²(Lφ−ρ)` on the rule's own Laplacian `L` (round
  3) — local, finite-speed. Two clean results: (1) **retardation** — a pulse's field is exactly zero
  beyond a sharp causal front advancing ~1 node/step (a disturbance reaches distance d only after ~d
  steps); (2) **static limit = electrostatics** — with a held charge `ρ`, the field relaxes to the exact
  Poisson potential `L V = ρ` of round 6 (mismatch ~1e-30, identical). So the Coulomb/confining force is
  the long-time limit of a genuinely local, retarded process — the non-locality was an artifact of
  taking the static limit first. (3) **speed = causality** — the front travels at the graph's hopping
  speed = the causal-cone speed (round 1) = 'c'. Graded PARTIAL, no leaf inflation (the spatial operator
  is the rule's; the wave temporal structure is the minimal local field dynamics). Whitepaper §6 updated.
- **NOT claimed (honestly):** full radiation (an accelerating charge's outward flux — subtle in 1D, no
  geometric fall-off; my 1D monopole tests were confounded) and the magnetic sector remain OPEN.
- **NEW TOP OPEN ITEMS:** (1) the **magnetic sector** in ≥2D — a *moving* charge's retarded field has a
  transverse (magnetic) component and an accelerating one radiates (with geometric fall-off in 2D+); this
  is the path to Faraday/Ampère (§6.4/§6.5); (2) lift OVERDAMPED drift (v∼F) to inertial **F = m a**
  (a∼F); (3) §4.5 orbits.
  Force/EM arc: holonomy-bias REFUTED (r5) → static field law (r6) → force ON MATTER (r7) → coupling
  DERIVED to one constant (r8) → β proven IRREDUCIBLE (r9) → field made LOCAL/retarded (r10).
- **`emergence_tree_v0.11.zip`** — superseded by v0.12.
- **HEADLINE RESULT (round 9): β is independent within the present construction (not fixed by bare rule or overlay). The
  derivation closes here, honestly.** Round 8 left one residual (the coupling constant β); the hope was
  the amplitude track might induce it. `sec06.../s6_5_coupling_constant.py` proves it does NOT, with a
  demonstration (the whole force is the deviation of β from 0: Glauber `P(hop)=1/(1+exp(β·ΔE))` gives
  `P=1/2` and no force at β=0) and **three independent reasons**: (1) β is an INVERSE TEMPERATURE — the
  keystone's uniform firing IS the β=0/infinite-T state, provably forceless; a finite β is a temperature
  the rule doesn't specify; (2) β is a TWO-BODY coupling (multiplies the field energy's cross term) but
  the rule's one-body generator (Laplacian, round 3) has none → fields superpose → no force at any T;
  (3) the force is CLASSICAL (static energy + real Glauber drift, no `i`), while the amplitude track
  buys the quantum `i` (kinematics, not interaction), which can't supply a classical coupling. So β,
  exactly like α and like the amplitude track's handedness bit ("possessed, not derived"), is a
  necessary input. Graded PARTIAL (characterization, no inflation; tally unchanged). Whitepaper §6
  updated. **Honesty note surfaced:** the round-6/7 force is the *instantaneous* electrostatic limit
  (non-local); a strictly local rule permits only a *retarded, mediated* force.
- **THE FORCE/EM ARC IS NOW COMPLETE (as far as it honestly goes):** holonomy-bias REFUTED (r5) →
  static field-energy law (r6) → force ON MATTER (r7) → coupling DERIVED to one constant (r8) → that
  constant β proven IRREDUCIBLE (r9). The EM coupling is derived in full except for one necessary number.
- **NEW TOP OPEN ITEMS (β is closed):** (1) **retardation / radiation** — build the *mediated* (local)
  version of the force, the path to Faraday/Ampère (§6.4/§6.6) and the honest completion of locality;
  (2) lift OVERDAMPED drift (v∼F) to inertial **F = m a** (a∼F); (3) §4.5 orbits.
- **`emergence_tree_v0.10.zip`** — superseded by v0.11.
- **HEADLINE RESULT (round 8): the field coupling is DERIVED from the rule — down to a single constant.**
  `sec06.../s6_2_charge_like_quantities.py` asks the program's deepest question (can the postulated
  coupling be derived from the keystone rule?) and gives the honest partial answer: **four derived
  pieces, one input independent of the construction.** (1) THE OBSTRUCTION: `redexes(E)` is a function of the edge
  multiset alone, so the loop-HOLONOMY charge is invisible to the rule — the principled reason round 5
  was byte-identical. (2) DERIVED: the right charge is the structural divergence `ρ=in−out degree` —
  rule-visible, **auto-neutral** (`Σρ=0`), and actively moved by the rule (`Δρ={x:+1,y:−1,z:−1,w:+1}`);
  §6.2 source/sink → DERIVED. (3) DERIVED: this charge reproduces the force (opposite attract/like
  repel). (4) DERIVED: the field operator `L` (graph Laplacian) is the rule's OWN diffusion generator
  (round 3's `π∼degree` H-theorem) — the field is the substrate's relaxation functional, not borrowed.
  (5) DERIVED: the Boltzmann coupling FORM `exp(−βΔE)` is the unique detailed-balance-preserving
  reweighting (round 3 reversibility). **IRREDUCIBLE POSTULATE: β≠0** — the bare rule fires uniformly
  (diffuses charge, no force); β≠0 (biased selection) is what moves charges. So the coupling is derived
  to ONE constant: operator+charge+form are the rule's own; only β's existence is input — the substrate
  analog of "why is there EM". Graded PARTIAL; DERIVED 67→69. Whitepaper §6 + ledger updated.
- **NEW TOP OPEN ITEM:** **derive β** — the one residual. The lead: the rewriting-amplitude / quantum
  track (`The-Price-of-an-Amplitude`) already weights histories; does that weighting induce an effective
  β? Then (2) lift overdamped drift to inertial F=ma; (3) §4.5 orbits.
  Force/EM arc so far: holonomy-bias REFUTED (r5) → static field law (r6) → force ON MATTER (r7) →
  coupling DERIVED to one constant (r8).
- **`emergence_tree_v0.9.zip`** — superseded by v0.10.
- **HEADLINE RESULT (round 7): the force now acts ON MATTER, charge-dependently.**
  `sec04.../s4_2_force_coupling.py` couples the round-6 field energy *back to the rewriting*: the
  glider's real left-hop operator (the §4.1 inertia move) is biased by the field-energy change it would
  cause, `P(hop)=1/(1+exp(β·ΔE))`. Because ΔE depends on the charge-sign *product*, the motion is
  charge-DEPENDENT (where the round-5 holonomy bias was byte-identical). Results, glider a real coherent
  2-core in 100% of runs: **single glider + fixed source** — opposite charges drive it toward the source
  (34→3 as β grows), like away (34→29), identical at β=0; **two mobile gliders** — opposite separation
  CLOSES (16.6→3.7), like OPENS (16.6→22.9), growing with β = exactly the Paper I §8 conjecture's
  (a),(b),(c), now satisfied with the corrected (field-energy) action. **§4.2 Force: OPEN → PARTIAL**
  (module dispatches the full arc — mechanism A REFUTED, mechanism B WORKS). Tally PARTIAL 112→115,
  OPEN 122→120. Whitepaper §4 + ledger updated.
  **Honest limits:** field coupling POSTULATED (BORROWED, not derived from the rule); regime OVERDAMPED
  (drift v∼F, not Newtonian a∼F).
- **NEW TOP OPEN ITEMS (force track):** (1) lift the overdamped drift to genuine inertial **F = m a**
  (force changes velocity over time, a∼F); (2) **derive** the field coupling from the keystone rule
  instead of postulating it (the deepest open problem); (3) §4.5 central-force / orbit tests now that a
  force exists. The force arc so far: holonomy-bias REFUTED (r5) → static field-energy law (r6) →
  field-energy force ON MATTER (r7).
- **`emergence_tree_v0.8.zip`** — superseded by v0.9.
- **HEADLINE RESULT (round 6): the force law, take two — a field energy that WORKS.** Following the
  round-5 refutation's redirect, `sec06.../s6_3_electric_field_analogues.py` builds standard discrete
  U(1) electrostatics on the substrate graph (structure BORROWED): potential `V` solving the discrete
  Poisson/Gauss law `L·V = ρ` (graph Laplacian, pure-python conjugate gradient), field `E = −∇V`, and
  interaction energy `E_int = −½ q_a q_b R(a,b)` (R = effective resistance — the cross/interference term
  the refutation said was missing). **It produces a charge-dependent force with the CORRECT signs:
  opposite attract, like repel** — the thing the refuted holonomy-bias could not do. And a falsifiable
  **substrate-specific prediction**: on the keystone `R ~ distance^1.0`, so the force is **CONFINING**
  (linear potential, constant force ~0.5), not Coulomb 1/r — because the transport dimension d_s~1.3 < 2
  (validated: 1D chain → confining, 3D lattice → Coulomb). Graded PARTIAL (field theory postulated;
  potential/Gauss-identity/sign-law/confining-form derived). Tally DERIVED 64→67. §6.3 leaves upgraded
  (Gradient/Divergence/Electric-potential → DERIVED; Gauss-law/Coulomb-behavior → PARTIAL); §6.5 Gauss
  law → PARTIAL. Whitepaper §6 + ledger updated (`Reconstructing-the-Physics-Hierarchy_v8.2.md`).
- **NEW TOP OPEN ITEM (force on matter):** couple the round-6 field energy *back* to the rewriting —
  bias redex choice by `exp(−β·ΔE_field)` so two charged gliders dynamically drift together (opposite)
  or apart (like). That is the step from a force LAW to a force *on the gliders*, and the genuine
  resolution of §4.2/§6.5. (The round-5 holonomy-bias coupling is REFUTED; this is the field-energy
  coupling, expected to work since the energy now has the right sign structure.)
- **`emergence_tree_v0.7.zip`** — superseded by v0.8.
- **HEADLINE RESULT (round 5): the program's central open conjecture — the force law — was TESTED and
  REFUTED.** Paper I §8 pre-registered: bias redex selection at glider contact by `exp(−β·ΔS)`,
  `ΔS` = change in loop-holonomy mismatch; predict opposite charges close faster, like slower, growing
  with β. A faithful implementation was built (`sec04.../s4_2_force.py`: phase-aware keystone with
  holonomy-preserving transport — verified to conserve a glider's charge exactly — two charged gliders,
  the biased selection). **Result: REFUTED in the strongest form — like and opposite dynamics are
  byte-identical at every β and every seed.** Structural reasons (all proven in the module):
  (1) the action is sign-blind for separated charges (`|+q|+|−q| = |+q|+|+q|`); (2) so the evolution is
  identical for like/opposite (150 seeds × β∈{1,3,8}); (3) the only sign-sensitive quantity (total
  signed holonomy) is conserved → ΔS=0. **Constructive redirect:** a Coulomb force is an interference
  term `2∫E₁·E₂` between *overlapping* fields; loop holonomies are localized with no cross term, so no
  holonomy-mismatch action can work. The real route is an **extended per-charge connection + a field
  energy with the interference term** — this is the new top open item. Recorded as a REFUTED leaf in
  §4.2 (force itself stays OPEN; tally now shows REFUTED=1). **Paper I §8 updated to close the
  pre-registration; whitepaper §4/§6 + ledger updated** (`Newtonian-Mechanics-from-Causal-Order_v1.0.md`
  and `Reconstructing-the-Physics-Hierarchy_v8.2.md`, both refreshed in outputs).
- **`emergence_tree_v0.6.zip`** — superseded by v0.7.
- **NEW FINDING (round 4): the area law holds *qualitatively* on the bare keystone graph, and the
  substrate's dimension splits into two families.** The monolith's `scaling`/`coefficient` are
  continuum *sprinkling* calculations (not the graph); the native measurement shows the edge boundary
  is **sub-extensive** (`|∂R|/|R|` falls from ~1.26 at |R|~8 to ~0.51 at |R|~98 — an area law holds,
  the graph is not a pure expander), but the exponent is noisy (`|∂R|~|R|^0.74`, R²~0.63), giving an
  area dimension ~2.5–3.5 on the static side. **The synthesis (the real payoff):** dimension is now
  measured five ways and splits cleanly — **STATIC/counting** (volume ~2.3–2.5, area ~2.5–3.5) vs
  **DYNAMIC/transport** (spectral ~1.3–1.5, causal-cone ~1.3, entropy-rate d_s/2 ~1.6). Static probes
  see more dimension than transport probes; that gap *is* the ramified geometry, and it now organizes
  every dimension result. **Candidate synthesis note for whitepaper §1.**
- **`emergence_tree_v0.5.zip`** — superseded by v0.6.
- **NEW FINDING (round 3): a rigorous, quantitative second law for the substrate — and its rate is the
  geometry.** For the reversible lazy random walk on the keystone graph, the relative entropy
  `D(p_t‖π)` to the degree-stationary distribution **decreases monotonically to zero** — a genuine
  discrete H-theorem, verified monotone for *every* one of 30 sampled start nodes. Equivalently the
  Shannon entropy `H(p_t)` rises monotonically, growing as `H(t) ~ (d_s/2)·ln t`: the measured
  entropy-production rate (0.82, implied d_s ≈ 1.6) **matches the independently-measured spectral
  dimension** at the same scale. So the second law and the substrate geometry are the same fact.
  Equilibrium is exact (π∝degree stationary to 1e-18, detailed balance to 0); the degree-distribution
  macrostate equilibrates in ~200 rewrite steps. This ties §5 (thermodynamics) to §1.3 (dimension)
  rigorously. **Folded into whitepaper v8.2 (§5).**
- **`emergence_tree_v0.4.zip`** — superseded by v0.5 (the full restructure that v0.5 builds on).
- **NEW FINDING (round 2): the curvature is MEASURED, not asserted — and it closes a referee gap.**
  The referee pass flagged `K = −0.048` as an asserted constant produced by no shipped code.
  `gravity.curvature` now computes exact Ollivier-Ricci curvature (W₁ via pure-python integer min-cost
  flow; validated: K5→+0.75, lattices→0, tree edge→neg). Measured on the keystone: **idleness 0 → mean
  κ ≈ −0.37 with ZERO positively-curved edges** (~55% flat = the pendant edges, ~45% negative core);
  **idleness 0.5 → mean κ ≈ 0**. The asserted −0.048 is reproduced by neither convention. So curvature
  is **non-positive, strongly negative at idleness 0**, magnitude idleness-dependent. The ~55% flat-edge
  fraction tracks the ~57% pendant fraction: curvature, degree distribution, and the low transport
  dimensions are **one consistent ramified-geometry picture, now all measured**. `constants.RESULTS`
  updated. **Folded into whitepaper v8.2 (§10 — −0.048 withdrawn, curvature now measured).**
- **NEW FINDING (round 1): the keystone has three disagreeing effective dimensions, coherently.**
  Volume/ball-growth `d_H ~ 2.3-2.5`; diffusion/spectral `d_s ~ 1.3-1.5`; causal-cone spacetime
  `D ~ 2.3` (⇒ spatial ~1.3). The two *transport* probes agree at ~1.3 and sit **below** the volume
  count ~2.4 — a **ramified-geometry** signature, cause measured directly: degree distribution is
  **~57% pendants**. Spectral estimator calibrated on lattices (1D→0.98, 2D→1.93, 3D→2.83). "The
  dimension" is not single-valued even for a *single* rule. **Folded into whitepaper v8.2 (§1).**
- **`STRUCTURE.md`** — three layers, usage, leaf scoreboard, full monolith→leaf map, rounds 1-2 log.
- **`emergence_package_v8.1.zip`** — the prior lab (domain-organized), referee-corrected. Still the
  implementation library inside the tree package (note: the tree package's `gravity.curvature` and
  `constants.py` are now ahead of this frozen zip — curvature measured). 67 modules; no third-party deps.
- **`Reconstructing-the-Physics-Hierarchy_v8.2.md`** — **NEW (master whitepaper, current).** Top-down
  by hierarchy §0–§13, every claim graded. v8.2 folds in the *measured* findings from porting rounds
  1–3: §1 ramified geometry (3-way dimension + ~57% pendant degree distribution), §10 measured
  Ollivier–Ricci curvature (−0.048 withdrawn), §5 rigorous arrow of time + formal entropy at rate
  d_s/2 + exact equilibrium. Headline leaf tally updated to DERIVED 64 (50→64 over v8.1, +14 leaves on
  measurement). v8.1 remains as the referee-corrected prior version.
- **`REFEREE_REPORT_v1.md`** — **NEW.** Adversarial re-check of all math and analytical reasoning.
  Verifies the solid core (b₁ conservation re-proved + 38k per-step checks; glider; cos-Wilson
  transport re-implemented, exactly 0 drift) and documents the 5 corrections now folded into v8.1.
  Read this to see *why* the grades changed.
- **`What-Falls-Out-of-a-Rewriting-Rule_v7.9.md`** — detailed derivation log (narrative, cumulative;
  contains all earlier v7.x content). Unchanged by the referee pass.
- **`emergence.py`** — the v7.9 monolith: all 64 experiment commands (complete archive). The package
  ports only the ~13 load-bearing experiments so far; the rest still live here.
- **`The-Core-Substrate_v1.0.md`** — **NEW.** Paper 0 of the paper series (master whitepaper §0 + the
  confluence material of §1). The foundational/formalism paper: defines the multiset hypergraph, the
  keystone rule, the exact causal-graph construction, and the observables, separating *definitional*
  from *forced*. Proves the substrate's two exact facts (linear growth; `b₁` conservation, full proof)
  and that the causal graph is an exactly-reconstructed acyclic partial order. Its core is the honest,
  referee-corrected treatment of the substrate's one open problem — causal invariance / confluence
  (critical pairs verified joinable but not yet a local-confluence theorem per Plump; global OPEN).
  Written to the v8.1 standard; Paper I builds on its Theorem 1.
- **`Newtonian-Mechanics-from-Causal-Order_v1.0.md`** — Paper I of the paper series (master whitepaper
  §3–§4). Predates the referee pass but is **unaffected by it**: every claim it makes is in the
  verified-solid bucket (conserved charge, inertia, no-annihilation, composite body). Self-contained,
  with fresh numerical output, a 200-trial robustness check, and the force-law gap pre-registered as a
  falsifiable conjecture for the next session. Builds on Paper 0's Theorem 1.

## Scoreboard — what is real vs open
Tally: **DERIVED 11 · PARTIAL 14 · BORROWED 4 · CONJECTURE 4 · OPEN 14.**

**DERIVED (the classical beachhead — these fell out, reproducible):**
- Topological charge `b₁` exactly conserved (the conserved quantity).
- **Inertia**: a conserved loop ("glider") moves at constant velocity with no driving — Newton I.
- **Momentum / no annihilation**: two charges sum to conserved total `b₁`; collisions can't destroy
  them. NB this is a conserved *scalar* charge, the bookkeeping precursor of momentum — a momentum
  *vector* (direction, additive velocities, center-of-mass) is still OPEN.
- **Composite body**: gliders bind into a stable compact bound state.
- **U(1) gauge KINEMATICS**: gauge-invariant Wilson loop + conserved gauge-invariant charge + neutral pairs.
- Ball-growth dimension: keystone is robustly **non-integer** (R² ~ 0.99), but the value is window/N-
  dependent — quote **~2.3–2.5, drifting up with scale** (a curvature signature), not "2.34".

**Key foundational / negative results (honest, load-bearing):**
- Dimension is a **continuous, tunable, generically-fractional INPUT** (~0–4 across the rule family),
  NOT predicted; 3+1 is not selected.
- **Consistency–dimension ceiling** `[PARTIAL, empirical]`: across ~10 sampled development-closed
  (provably confluent) rules, all had spatial `d < 1.5`. This is a finite-sample correlation, *not* a
  proven implication; its mechanism is `[CONJECTURE]`. (v8.0 overstated this as a DERIVED ⇒; corrected.)
- **REFUTED**: "dimension = reconciliation depth" (Pearson −0.15, if anything inverse) — this was the
  ceiling mechanism's first proposed form. Proposed in v7.8, killed by measurement in v7.9.
- Keystone **global confluence is OPEN**. Local confluence is **not yet a theorem**: the four critical
  pairs are *verified joinable* (3 at depth 1, the 3-path at depth 2), but hypergraph local confluence
  needs *strong* joinability (Plump 2005), which is not yet checked — and confluence is undecidable in
  general (Plump 1993). All 4 standard *global* techniques are defeated by the non-development-closed
  3-path. (v8.0 called local confluence a THEOREM via the term-rewriting CPL; corrected.)

**BORROWED:** Lorentz (Gorard, dimension-agnostic); quantum `i` + Born rule (OS); Minkowski metric (causal-set order).
**PARTIAL:** arrow of time; curvature **sign** `K ≤ 0` (negative plausible; the number −0.048 is
*asserted*, not produced by any shipped code — sign only); Einstein eq in de Sitter minisuperspace;
holographic area law; branchial space.
**CONJECTURE:** decoherence via de Sitter / circuit-complexity (branch-swap complexity monotonicity);
dark sector (measurement-loss → dark energy).

## The decisive open targets (highest leverage first)
1. **`electrodynamics/maxwell` = `mechanics/force`** — a charge-responsive Wilson action the rule
   actually READS, turning the passive U(1) label into a FORCE (opposite attract, like repel). One
   ingredient that converts the most PARTIAL/OPEN entries at once. **Start here.** A specific,
   falsifiable form of this is now pre-registered in `Newtonian-Mechanics-from-Causal-Order_v1.0.md`
   §8 (weight redex choice at glider contact by `exp(−β·ΔS)`, `ΔS` = holonomy-mismatch change) —
   untested, ready to run.
2. **Non-Abelian gauge** — SU(2)/SU(3) holonomy on loops (non-commuting, ordered traversal). Owed.
   **Watch-out (from referee pass):** the current rule transports only cos(Wilson)/unsigned holonomy;
   it does NOT track a consistent loop *orientation* (signed W preserved only up to W→W̄). Harmless for
   abelian U(1) but substantive here, since tr(holonomy) ≠ tr(reverse). Define and carry an oriented
   loop basis *first*.
3. **Geodesic motion** — a glider in a curved background; the missing link from mechanics to gravity.
4. **Formal entropy / second law** — owed (the arrow is shown, entropy is n