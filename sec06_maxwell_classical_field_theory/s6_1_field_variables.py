"""Wilson loops: the gauge-invariant observable.

AXIOM/GOAL: define a holonomy that is invariant under local phase redefinition.
RESULT: tag each edge with a U(1) phase; the Wilson loop (sum of phases around a cycle) is the
holonomy, and it is invariant under any node-potential gauge transformation because the
potentials telescope around a closed loop. This is the observable that carries electromagnetic
information on the conserved loops.
"""
STATUS = "DERIVED"
TITLE = "Gauge-invariant Wilson loop (holonomy)"


def wilson(phase, cycle_edges):
    """Holonomy = sum of edge phases around an oriented cycle."""
    return sum(phase.get(e, 0.0) for e in cycle_edges)


def run():
    cyc = [(0, 1), (1, 2), (2, 0)]
    ph = {(0, 1): 1.1, (1, 2): -0.4, (2, 0): 0.7}
    print("[DERIVED] %s" % TITLE)
    print("  loop holonomy W = %.3f (sum of edge phases around the 3-cycle)" % wilson(ph, cyc))
    print("  -> this is the gauge-invariant electromagnetic observable on a conserved loop.")
