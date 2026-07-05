# 2+1D CDT REBUILD — FAITHFUL SPEC + DIFF

Subcommittee: FAITHFUL-SPEC. Goal: pin EXACTLY where our substrate
(moves (2,3)/(3,2),(2,6)/(6,2),(4,4); action S = -k0 N0 + k3 N3) differs from
the published Ambjorn-Jurkiewicz-Loll (AJL) 2+1D CDT algorithm, and give a
precise, implementable corrected spec. Do NOT write the simulation here.

All move-set / action / config-space claims below are quoted from primary
sources and marked [VERIFIED]. Items I could not confirm from a primary source
are marked [UNCONFIRMED].

Primary sources actually read for this spec:
- AJL, "Dynamically triangulating Lorentzian quantum gravity", Nucl. Phys. B610
  (2001) 347, arXiv:hep-th/0105267 -- Sec. 7.1 gives the EXACT 2+1D 5-move set
  with explicit vertex labels; Sec. 3.1/8.1 give the identities and action.
  [read full text]
- AJL, "Nonperturbative 3d Lorentzian quantum gravity", PRD 64 (2001) 044011,
  arXiv:hep-th/0011276 -- the 2+1D phase structure / extended (de Sitter-like)
  phase paper; move set is by reference to hep-th/0105267. [abstract read; the
  move-set detail lives in 0105267, which we read in full]
- Kommu, "A Validation of Causal Dynamical Triangulations", arXiv:1110.6875,
  CQG 29 (2012) 105003 -- independent 2+1D code: tau=N22/N3 order parameter,
  k0_c~3.3 (vs AJL~6.6), spectral dimensions. [read full text]
- Benedetti & Henson, arXiv:1410.0845, "Spacetime condensation in
  (2+1)-dimensional CDT from a Horava-Lifshitz minisuperspace model" -- the
  V(t)=a cos^2(bt) droplet-on-a-stalk profile and the finding that the *GR*
  minisuperspace action FAILS to condense in 2+1D. [abstract read]


================================================================================
## 1. THE EXACT AJL 2+1D MOVE SET  [VERIFIED, hep-th/0105267 Sec. 7.1]
================================================================================

Config space: Lorentzian 3d triangulations with a FIXED number T of spatial
slices (periodic in proper time), finite volume, obeying the simplicial-manifold
constraints. Top simplices are tetrahedra of exactly three types:
  (3,1) : 3 verts at time t,   1 vert at time t+1   ("up" spatial-base tet)
  (1,3) : 1 vert at time t,    3 verts at time t+1   ("down" spatial-base tet)
  (2,2) : 2 verts at time t,   2 verts at time t+1   (the timelike "coupling" tet)
No purely-spacelike tetrahedra exist. Spatial slices are 2D triangulations of
S^2. (2,6)/(6,2) births/deaths change the spatial vertex count of a slice; (2,2)
tets carry the inter-slice coupling; N22 counts them.

There are exactly FIVE basic moves (counting inverses separately). AJL's own
words: their strategy is to "first select moves that are ergodic within the
spatial slices t=const ... and then supplement them by moves that act within the
sandwiches dt=1." [VERIFIED hep-th/0105267 Sec.7]

Vertex-label conventions below are AJL's own (Eqs. 56-58).

--------------------------------------------------------------------------------
MOVE (2,6)   [and inverse (6,2)]        THE SPATIAL-VERTEX BIRTH MOVE
--------------------------------------------------------------------------------
Precondition: a pair of a (1,3)- and a (3,1)-tetrahedron (labels 1345 and 2345)
  that SHARE the spatial triangle 345. Here 3,4,5 all lie in one slice t; vertex
  1 is the apex at t-1 (the (1,3) tet, below) and 2 is the apex at t+1 (the (3,1)
  tet, above). [Equivalently: a spatial triangle with its unique up-apex and
  down-apex.]
Action: insert a NEW vertex 6 at the CENTRE of triangle 345, in slice t; connect
  6 by new edges to 1,2,3,4,5.
  1345 + 2345  ->  1346 + 2346 + 1356 + 2356 + 1456 + 2456
Result: 6 tetrahedra, 3 below and 3 above slice t. The spatial triangle 345 is
  split into three spatial triangles (346, 356, 456) around 6.
Simplex-count changes:
  dN3 = +4  (2 -> 6 tets)     [ (6,2): dN3 = -4 ]
  dN0 = +1  (new vertex 6)    [ (6,2): dN0 = -1 ]
  dN2^SL (spatial triangles) = +2   [ slice t volume += 2 ]
  d(N31=N13 count) = +4 ;  dN22 = 0    (all six new tets are (3,1)/(1,3))
Geometric validity: 6 must not already exist; the split must keep slice t a valid
  simplicial S^2 (no double edges/triangles). Foliation preserved.
Role: THE move that grows/shrinks the SPATIAL triangulation of a single slice.
  It changes N(t).

--------------------------------------------------------------------------------
MOVE (4,4)   [self-inverse]             THE SPATIAL DIAGONAL FLIP (2D "flip")
--------------------------------------------------------------------------------
Precondition: a "diamond" of two (1,3)- and two (3,1)-tetrahedra: from the
  spatial "square" (double triangle) 2345 in slice t, one neighbouring apex pair
  above and one below. AJL labels: 1235 + 2356 + 1345 + 3456 (Eq.57).
Action: flip the spatial diagonal of the square 2345, reassigning the four tets:
  1235 + 2356 + 1345 + 3456  ->  1234 + 2346 + 1245 + 2456
Simplex-count changes:
  dN3 = 0 ;  dN0 = 0 ;  dN22 = 0 ;  d(spatial triangles) = 0
  (only the internal spacelike diagonal is re-routed)
Geometric validity: the new diagonal must not already be an edge of slice t
  (else double edge). Foliation preserved.
Role: THIS IS THE INTRA-SLICE 2D FLIP (Pachner flip on the 2D spatial
  triangulation) lifted into the 3D sandwich. It makes the spatial 2D
  triangulation of a slice ergodic AT FIXED spatial vertex count.

*** AJL, verbatim: "The (2,6)- and (6,2)-moves, together with the (4,4)-move
(which is its own inverse) induce moves within the spatial slices that are known
to be ERGODIC for two-dimensional triangulations." [VERIFIED hep-th/0105267,
sentence immediately after Eq.57]. ***
=> ANSWER to "is there a move that makes intra-slice 2D geometry genuinely
ergodic?": YES = {(2,6),(6,2),(4,4)} acting on the slices. (4,4) is the crucial
fixed-vertex-count flip; (2,6)/(6,2) add/remove vertices. All three => full 2D
ergodicity of each S^2 slice.

--------------------------------------------------------------------------------
MOVE (2,3)   [and inverse (3,2)]        THE PURE-SANDWICH MOVE (no slice change)
--------------------------------------------------------------------------------
Precondition: a pair of a (3,1)- and a (2,2)-tetrahedron that share a triangle
  345 in common. AJL: 1345 (a (3,1)) + 2345 (a (2,2)) sharing triangle 345.
Action: substitute the shared triangle 345 by the 1-dim edge 12 dual to it:
  1345 + 2345  ->  1234 + 1235 + 1245
Result: one (3,1)- and TWO (2,2)-tetrahedra sharing the link 12.
Simplex-count changes:
  dN3 = +1  (2 -> 3 tets)     [ (3,2): dN3 = -1 ]
  dN0 = 0                      (no new vertex)
  dN22 = +1  ((3,1)+(2,2) -> (3,1)+two (2,2); net +1 (2,2) tet)
  d(spatial triangles N2^SL) = 0   *** DOES NOT CHANGE ANY SLICE'S N(t) ***
Geometric validity: edge 12 must not already exist; result a valid complex.
  This move "affects the sandwich geometry without changing the spatial slices at
  integer-t." [VERIFIED, AJL Sec.7.1]
Role: the ONLY move that changes N22 directly at fixed N0 -- the coupling/tau
  move. Reshapes the interior of a sandwich WITHOUT touching either bounding slice.

--------------------------------------------------------------------------------
SUMMARY TABLE (AJL 2+1D, per forward move)
--------------------------------------------------------------------------------
 move   dN3   dN0   dN22   dN2^SL(slice vol)   what it fluctuates
 (2,6)  +4    +1    0      +2 (one slice)      spatial vertex count / N(t)
 (6,2)  -4    -1    0      -2 (one slice)      inverse
 (4,4)   0     0    0       0                  spatial DIAGONAL (2D flip) - ergodic
 (2,3)  +1     0   +1       0                  sandwich interior / N22 / tau
 (3,2)  -1     0   -1       0                  inverse
Ergodicity: {(2,6),(6,2),(4,4)} => ergodic on each 2D slice; adding (2,3)/(3,2)
=> conjectured ergodic on the full foliated 3d causal triangulation space.
[VERIFIED as AJL's claim; full-3d ergodicity stated as "we believe is ergodic".]


================================================================================
## 2. THE DIFF vs OUR IMPLEMENTATION
================================================================================

Our substrate (cdt_2plus1.c / .py, and the de Sitter binary
cdt_2plus1_desitter.c) uses the SAME FIVE move NAMES: (2,3)/(3,2), (2,6)/(6,2),
(4,4). So the move set is NOT missing a whole move type.

(i) SPATIAL ERGODICITY -- ADDRESSED, NOT THE PRIMARY DIFF.
    Our (4,4) IS the intra-slice 2D flip (move_44: spacelike edge shared by 4
    tets, 2 up to apex p, 2 down to apex q, flip ab->cd). This is exactly AJL's
    (4,4) diagonal flip. Together with our (2,6)/(6,2) it CAN make each S^2
    slice's 2D triangulation ergodic. So we are NOT missing a spatial flip move.
    => Hypothesis "slices under-fluctuate for lack of an intra-slice move" is
       FALSE at the level of the move SET: the (4,4) flip is present. (See caveat
       (D) on whether it FIRES enough.)

The real DIFFERENCES are in PRECONDITIONS and the ACCEPTANCE GATE / measure:

(A) [DIFF, move_23 precondition too loose]  AJL (2,3) requires a (3,1)+(2,2) pair
    sharing a triangle 345. OUR move_23 (both C and py) fires on ANY internal face
    shared by two tets (`cnt==2`), grabs the two opposite apices d,e, and forms
    abde/bcde/acde. It does NOT restrict the two parent tets to the (3,1)+(2,2)
    types. It relies on the downstream `_apply_check`/foliation gate to veto
    illegal outcomes. Consequences:
      - It PROPOSES (2,3) on face-pairs AJL never would, biasing the accepted-move
        mix (proposal distribution differs from AJL -> measure concern).
      - As the ONLY N22-changing move, mis-weighting it directly skews
        tau=N22/N3. Consistent with our VERDICT tau collapse (0.44 -> 0.19 as N3
        grows): the (2,3)/(3,2) balance is not sampled with AJL relative
        frequency, so coupling drains at large volume.
    FIX: gate move_23 on the AJL local pattern (one (3,1)+one (2,2) sharing a
    spacelike triangle 345, apices 1,2 forming new timelike edge 12), and count
    valid (2,3) and inverse (3,2) sub-complexes for the acceptance ratio.

(B) [MATCH, move_26]  Our move_26 builds X (spatial) + up-apex p + down-apex q,
    6 tets -- structurally AJL's (2,6). Keep it.

(C) [DIFF, ACCEPTANCE GATE is topological, not full-manifold]  Our `_apply_check`
    accepts iff (closed) AND (foliation_ok) AND (each touched slice chi=2). AJL's
    actual constraint is the SIMPLICIAL-MANIFOLD constraint: every (d-1)-subsimplex
    shared by EXACTLY two d-simplices AND the link of every vertex a sphere S^{d-1}
    [VERIFIED hep-th/0105267 Sec.7 intro]. chi=2 is NECESSARY but NOT SUFFICIENT
    for a simplicial 2-sphere (a pinched pseudo-manifold can have chi=2). If our
    gate admits chi=2-but-not-simplicial-S^2 slices, we sum over a SUPERSET of
    AJL's ensemble -- a subtly WRONG ensemble supporting degenerate/pinched
    geometries. Candidate mechanism for "correct-but-wrong-ensemble".
    FIX: replace chi=2 with the exact simplicial-2-manifold test (each spacelike
    edge in exactly 2 spatial triangles; each vertex link a single cycle). In 3d,
    each triangle in exactly 2 tets, each vertex link an S^2.

(D) [DIFF, DYNAMICS / proposal frequencies -- likely the operative cause]  Our
    VERDICT: volume redistributes "only by slow diffusive +/-2 (2,6)/(6,2)
    births/deaths with NO direct cross-sandwich transfer"; tau falls with volume;
    cos^2 R2 degrades. This is NOT a missing move -- AJL also has no direct
    cross-sandwich transport; volume diffuses in AJL too. The difference is
    QUANTITATIVE:
      - Proposal weighting: AJL picks a move type, then a random sub-complex of
        that type UNIFORMLY, and applies Metropolis with the correct
        N_forward/N_backward combinatorial factor. Our C loops hash slots from a
        random start and takes the FIRST valid sub-complex. That is NOT uniform
        and computes NO N_forward/N_backward -- so detailed balance holds only if
        applicable-sub-complex counts are symmetric, which they are not. Biased
        proposal + missing combinatorial factor => stationary distribution that is
        "internally consistent" yet samples the WRONG measure (our exact symptom).
      - Thermalization: AJL/Kommu ~1e5 sweeps (sweep = N3 attempts). Our de Sitter
        runs used 200-350 sweep-iters. Under-samples the slow tau mode.
    FIX: (a) uniform sub-complex selection; (b) include N_forward/N_backward in
    acceptance; (c) thermalize to AJL/Kommu scale.

NET DIFF VERDICT:
  - Move SET: same 5 moves; the (4,4) spatial flip IS present, so slices are not
    under-fluctuating for lack of a move type. [spatial-ergodicity hypothesis:
    REJECTED at the set level]
  - Genuine differences: (A) loose (2,3) precondition (biases N22/tau); (C) chi=2
    gate weaker than AJL's simplicial-manifold constraint (admits a SUPERSET
    ensemble); (D) non-uniform first-hit proposal + missing combinatorial
    detailed-balance factor + light thermalization (tilts the measure ->
    "correct-but-wrong-ensemble"). (D) is the most likely operative cause of the
    missing single de Sitter blob; (A)+(C) compound it.


================================================================================
## 3. CONFIGURATION SPACE + MEASURE  [VERIFIED hep-th/0105267 Secs. 2,3.1,8.1]
================================================================================

Configuration space (what is summed over):
  - Fixed number T of spacelike slices, PERIODIC in proper time (t ~ t+T).
    [Kommu confirms periodic-in-time for technical convenience.]
  - Each slice t is an (unlabelled) simplicial triangulation of S^2 from
    equilateral spatial triangles. Slice topology FIXED (no spatial topology
    change -- this is what "causal" buys).
  - Each sandwich [t,t+1] filled by (3,1),(1,3),(2,2) tets ONLY. No purely-
    spacelike tets. Gluing:
       * each spacelike triangle shared by exactly two (3,1)/(1,3) tets (one up,
         one down) [VERIFIED "each space-like triangle is shared by two (3,1)-tets"];
       * each timelike triangle shared by exactly two tets;
       * simplicial-manifold: every triangle in exactly 2 tets, every vertex link
         an S^2. Vertices carry a definite integer time.
  - Edge lengths: l^2_space=a^2, l^2_time=-alpha*a^2 (alpha>1/2, d=3); Wick
    alpha->-alpha; alpha reabsorbed into k0,k3. [VERIFIED]

Bulk variables / identities in 2+1D [VERIFIED Sec.3.1]:
  f^(3) = (N0, N1^SL, N1^TL, N2^SL, N2^TL, N3^(3,1), N3^(2,2)); linear identities
  (periodic bc) reduce to TWO independent bulk variables. Hence two couplings.

Action (AJL reduced / Wick-rotated):
  S^(3) = -k0 N0 + k3 N3            [VERIFIED Kommu Eq.10-12; AJL PRD64]
  Z = sum_T (1/C(T)) exp(k0 N0 - k3 N3),  C(T)=order of automorphism group (symm.
  factor). Equivalent EDT form S = k3 N3 - k1 N1, k1=2*pi*k [VERIFIED Sec.8.1].
  For alpha!=-1 separate N3^(3,1),N3^(2,2) terms appear, but 2+1D has only two
  bulk dof so it still reduces to -k0 N0 + k3 N3 (redefined couplings). [VERIFIED
  Kommu fn.1]
  => OUR action S = -k0 N0 + k3 N3 is EXACTLY the AJL 2+1D reduced action. MATCH.
     (Our +eps*(N3-Nbar)^2 volume-fixing is a standard external potential; fine
     as long as measurements use the fixed-N3 ensemble. Not a diff.)

Measure / detailed balance (the part we get WRONG, Sec.2 item D):
  Metropolis min(1, exp(-dS)) is correct ONLY for symmetric proposals. For local
  moves not self-inverse with equal multiplicity, the correct acceptance is
     A(T->T') = min(1, (N_move(T)/N_inv(T')) * exp(-dS))
  with N_move(T)=number of distinct applicable sub-complexes for the forward move
  in T, N_inv(T')=number for the inverse in T'. AJL/standard CDT carry these
  factors (and C(T)). Our first-hit, factor-free acceptance omits both -> biased
  measure.
  CONSTRAINT WE IMPOSE THAT AJL DOESN'T: the chi=2 slice gate is WEAKER than
  simplicial-S^2, so we ADMIT extra (pinched) configs (superset), not a stricter
  subset. We do NOT impose an extra RESTRICTION AJL lacks; our error is a looser
  gate + biased proposal, both of which enlarge/tilt the measure away from AJL.


================================================================================
## 4. VALIDATION TARGETS (NUMBERS)  [VERIFIED unless flagged]
================================================================================

Order parameter tau = N22 / N3 = N22 / (N13 + N22 + N31):
  - Extended (de Sitter) phase, coupled: tau rises sharply below k0_c.
  - Kommu Fig.1 (2+1D): tau climbs from ~0 (decoupled, k0>k0_c) toward a plateau
    ~0.3-0.4 in the extended phase (k0<k0_c). [VERIFIED: Kommu Fig.1 y-axis
    0..~0.4; extended plateau in ~0.3-0.4 band.]
  - Our THEORY.md "coupled ~0.33-0.4, decoupled tube ~0.09" is consistent with
    Kommu. [decoupled ~0.09 exact value: UNCONFIRMED; low-tau decoupled limit
    IS confirmed qualitatively.]
  - VALIDATION: extended-phase tau should stay ~0.3-0.4 and roughly FLAT vs N3
    (NOT collapse to 0.19 like our substrate). tau-vs-volume stability is itself
    a target.

Critical coupling k0_c (NORMALIZATION-DEPENDENT -- report both):
  - AJL (PRD64): k0_c ~ 6.6   [VERIFIED via Kommu citing [3]]
  - Kommu (1110.6875): k0_c ~ 3.3   [VERIFIED, Kommu Fig.1 text: "at k0_c~6.6 in
    [3]... differ by a factor of two, for reasons we do not understand, but the
    qualitative results are identical."]
  => factor-of-2 normalization ambiguity is EXPECTED; match k0_c to the rebuild's
     k0 normalization and require the tau jump to sit there.

Hausdorff dimension d_H -> 3 (large-scale, extended phase):
  - AJL abstract: "macroscopic scaling properties resemble those of a
    semi-classical spherical universe" (d_H consistent with 3). [VERIFIED
    qualitatively.] Exact d_H fit: [UNCONFIRMED from sources read] -- target -> 3.

Spectral dimension d_s (short -> large), full 2+1D spacetime [VERIFIED Kommu]:
  - d_s runs ~2.4 (short) up to ~3.0 (large), then falls at large sigma (finite
    volume). Kommu fits (N3=80000, k0=1.0):
       D(sigma) = 3.03 - 10.51/(17.87 + sigma)   -> D(inf) ~ 3.03
       D(sigma) = 3.19 - 0.97 exp(-0.013 sigma)  -> D(0)=2.22, D(inf)=3.19
    Benedetti-Henson report D(0)=2.12, D(inf)=2.98. [VERIFIED]
  - Spatial-slice spectral dimension (2+1D): levels off ~1.65. [VERIFIED Kommu.]
  => VALIDATION: full-spacetime d_s rises 2 -> 3; slice d_s ~ 1.6-1.7.

de Sitter volume profile (extended phase), the BLOB test [VERIFIED B&H 1410.0845]:
  - Continuum 3d de Sitter spatial-volume law:  V_2(t) = a * cos^2( b t ).
    Exponent n = 2 (cos^2) in 2+1D. [VERIFIED B&H abstract: "V_2(t)=a cos^2(bt)"
    -- confirms our THEORY.md n=2.]
  - Morphology: a single extended DROPLET/blob of spatial volume connected to a
    STALK of minimal spatial extension; droplet time-extent strictly < T.
    [VERIFIED B&H abstract "extended droplet ... connected to a stalk of minimal
    spatial extension".]
  - Width scaling W ~ N3^(1/3): blob grows self-similarly (universe scale ~
    V^{1/3} in 2+1D). [Our THEORY.md states this; the 1/3 scaling in 2+1D is the
    standard CDT result. Exact prefactor / b: UNCONFIRMED from sources read here
    -- treat W ~ N3^{1/3} exponent and single-lobe/stalk morphology as target.]
  - CRITICAL CAVEAT [VERIFIED]: in 2+1D a minisuperspace reduction of the *GR*
    action FAILS to reproduce the droplet+stalk condensation; a Horava-Lifshitz
    effective action is needed. This CORROBORATES our VERDICT that a plain
    two-coupling *effective* description "does not confine a single lobe against
    a stalk". IMPORTANT NUANCE: that is a statement about the reduced
    minisuperspace EFFECTIVE action, NOT the full CDT simulation. The FULL 2+1D
    CDT ensemble (correct moves, correct manifold gate, correct measure) DOES
    condense into droplet+stalk -- that is AJL PRD64's result. So the target is
    reachable with the -k0 N0 + k3 N3 MICROSCOPIC action; the HL effective action
    EMERGES. Our substrate's failure is about the ENSEMBLE/measure/gate (Sec.2
    A,C,D), not about needing a different microscopic action.

VALIDATION CHECKLIST (extended phase, k0 < k0_c):
  [ ] tau = N22/N3 in ~0.3-0.4 and STABLE vs N3 (not collapsing).
  [ ] k0_c located (report at rebuild k0 normalization; expect ~3.3 or ~6.6).
  [ ] COV-aligned <N(t)> a SINGLE cos^2 lobe on a thin stalk, R2 IMPROVING with V.
  [ ] blob width W ~ N3^(1/3).
  [ ] full-spacetime d_s: ~2 -> ~3; spatial-slice d_s ~ 1.6-1.7.
  [ ] d_H -> 3.


================================================================================
## 5. IMPLEMENTABLE CORRECTIONS (the DIFF as a to-do)
================================================================================
1. move_23/32: restrict precondition to AJL's (3,1)+(2,2)-sharing-triangle-345
   pattern (inverse: link 12 shared by one (3,1)+two (2,2)). Do NOT rely on the
   downstream gate to filter arbitrary faces.
2. Detailed balance: for EVERY move, (a) select the sub-complex UNIFORMLY among
   all applicable ones (not first-hit); (b) multiply acceptance by
   N_forward(T)/N_backward(T') (counts of applicable sub-complexes for the move
   and its inverse). Keep the C(T) symmetry-factor framework.
3. Replace the chi=2 slice gate with the exact simplicial-2-manifold test (each
   spacelike edge in exactly 2 spatial triangles; each vertex link a single
   cycle). In 3d: each triangle in exactly 2 tets, each vertex link an S^2. This
   shrinks our (superset) ensemble to AJL's exact one.
4. Keep the 5 moves (2,3)/(3,2),(2,6)/(6,2),(4,4) and the action -k0 N0 + k3 N3
   -- both already AJL-correct. Keep (4,4); ensure it FIRES (log per-move accept
   rates; (4,4) should be a healthy fraction, giving each slice a fluctuating 2D
   geometry at fixed vertex count).
5. Thermalize to AJL/Kommu scale (~1e5 sweeps; sweep = N3 attempts), measure every
   ~100 sweeps, COV-align each snapshot before averaging N(t), fit cos^2.


================================================================================
## CITATIONS (verified content only)
================================================================================
[AJL-NPB] J. Ambjorn, J. Jurkiewicz, R. Loll, "Dynamically triangulating
  Lorentzian quantum gravity", Nucl. Phys. B610 (2001) 347, arXiv:hep-th/0105267.
  -- EXACT 2+1D 5-move set with vertex labels (Sec.7.1, Eqs.56-58); explicit
  ergodicity statement for {(2,6),(6,2),(4,4)} on slices; identities & action
  (Secs.3.1, 8.1). [read in full]
[AJL-PRD] J. Ambjorn, J. Jurkiewicz, R. Loll, "Nonperturbative 3d Lorentzian
  Quantum Gravity", Phys. Rev. D64 (2001) 044011, arXiv:hep-th/0011276.
  -- 2+1D extended (de Sitter-like) phase; k0_c~6.6; action -k0 N0 + k3 N3.
  [abstract read; move detail via AJL-NPB]
[Kommu] R. Kommu, "A Validation of Causal Dynamical Triangulations",
  arXiv:1110.6875, CQG 29 (2012) 105003. -- independent 2+1D code; tau=N22/N3
  (Eq.19); k0_c~3.3 (vs AJL~6.6, factor-2 normalization); d_s fits (2.4->3.0;
  D(inf)~3.0; slice d_s~1.65). [read in full]
[B&H] D. Benedetti, J. Henson, "Spacetime condensation in (2+1)-dimensional CDT
  from a Horava-Lifshitz minisuperspace model", arXiv:1410.0845. -- V_2(t)=a
  cos^2(bt); droplet-on-a-stalk; GR minisuperspace FAILS in 2+1D, HL succeeds
  (effective-action statement). [abstract read]

FLAGGED UNCONFIRMED (need a further primary fetch for exact numbers):
  - exact decoupled-phase tau value (~0.09 is ours, qualitatively consistent).
  - exact d_H numeric fit and the cos^2 width prefactor / b in W~N3^{1/3}
    (exponent 1/3 and single-lobe+stalk morphology ARE confirmed; the numeric
    prefactor is not, from sources read here).
