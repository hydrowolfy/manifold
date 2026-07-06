"""Canonical rules and the program's headline results, each tagged with its grade.

Grades (the program's honest ledger):
  DERIVED     - fell out of the rule / computed, with proof or strong numerical evidence
  PARTIAL     - a real but incomplete result
  BORROWED    - relies on an external theorem (e.g. Gorard, Osterwalder-Schrader)
  CONJECTURE  - proposed, not yet tested
  OPEN        - identified target, not started
  REFUTED     - tested and failed
"""

# Keystone rule. LHS is always the directed 2-path x->y->z (both matched edges destroyed);
# RHS below; w is a fresh node minted each application.
KEYSTONE       = (('x', 'z'), ('y', 'x'), ('z', 'w'))
# Provably-confluent (development-closed) sibling, shares the charge+glider core x->z, y->x:
ALT_CONFLUENT  = (('x', 'z'), ('y', 'x'), ('y', 'w'))
# Glider 2-move operator on a directed rail (relative node offsets): translates a minimal 2-cycle.
GLIDER_OPS     = ((-1, 0, 1), (-1, 1, 0))   # fire(n-1,n,n+1) then fire(n-1,n+1,n)

RESULTS = {
    "topological_charge_b1":             ("conserved",   "DERIVED"),    # dE=dV=+1, dC=0 per step
    "emergent_dimension_keystone":       ("~2.3-2.5",    "DERIVED"),    # NON-integer; window/N-dependent, drifts up
    "dimension_is_a_free_input":         (True,          "DERIVED"),    # continuous spectrum ~0-4
    "local_confluence":                  ("joinable",    "PARTIAL"),    # crit pairs verified joinable; STRONG joinability (Plump) OPEN
    "consistency_dimension_ceiling":     ("d<1.5 (~10 rules)", "PARTIAL"),  # EMPIRICAL correlation, not a proven implication
    "dimension_eq_reconciliation_depth": (False,         "REFUTED"),    # Pearson -0.15
    "ballistic_glider_inertia":          ("v=1/2 rail",  "DERIVED"),    # constant velocity (Newton I)
    "collision_charge_conserved":        ("b1=2 exact",  "DERIVED"),    # no annihilation (SCALAR charge, not vector momentum)
    "u1_gauge_kinematics":               ("present",     "DERIVED"),    # gauge-invariant Wilson loop; cos(W) transported exactly
    "u1_gauge_force":                    ("absent",      "OPEN"),       # collisions are charge-blind
    "curvature_K":                       ("kappa~-0.37@a=0", "DERIVED"),  # MEASURED (Ollivier-Ricci, exact OT): non-positive, strongly neg at idleness 0, ~0 at 0.5; supersedes the asserted -0.048
    "lorentz_from_causal_invariance":    (True,          "BORROWED"),   # Gorard / Wolfram (dimension-agnostic)
    "quantum_i_from_reversibility":      (True,          "BORROWED"),   # reflection positivity -> OS
}
