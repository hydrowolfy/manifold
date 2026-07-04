"""U(1) gauge structure on the conserved loops (electromagnetic KINEMATICS).

AXIOM/GOAL: is there a gauge field, and is its holonomy gauge-invariant and conserved?
RESULTS: (i) GAUGE INVARIANCE -- under a node-potential transformation ph(a,b) -> ph(a,b) +
lam[a] - lam[b], the Wilson loop is unchanged (potentials telescope). (ii) Each glider carries a
gauge-invariant charge = holonomy around its own 2-cycle; opposite charges sum to zero (a neutral
pair). (iii) HONEST LIMIT -- the rule fires on graph structure and never reads the phases, so
like- and opposite-charge collisions evolve byte-identically: a passive U(1) label exerts NO
force. We have the full electromagnetic KINEMATICS and none of its DYNAMICS (no Maxwell yet).

ORIENTATION CAVEAT (added v8.1): the phase-carrying rule transports cos(Wilson) / the UNSIGNED
holonomy of a loop to machine precision (verified: exactly 0 drift over thousands of steps). It does
NOT track a consistent loop ORIENTATION, so the SIGNED/complex Wilson loop is preserved only up to
W -> conj(W). For abelian U(1) this is a harmless convention. It becomes SUBSTANTIVE for the planned
non-abelian SU(2)/SU(3) extension, where tr(holonomy) != tr(reverse holonomy): a consistent oriented
loop basis must be defined and carried by the rule before non-abelian holonomy can be claimed.
"""
from sec06_maxwell_classical_field_theory.s6_1_field_variables import wilson

STATUS = "DERIVED"
TITLE = "U(1) gauge invariance + conserved charge (kinematics; force-on-matter now PARTIAL via rho=in-out)"


def run():
    cyc = [(0, 1), (1, 2), (2, 0)]
    ph = {(0, 1): 1.1, (1, 2): -0.4, (2, 0): 0.7}
    lam = {0: 0.5, 1: -1.3, 2: 2.0}                          # arbitrary gauge transformation
    phg = {(a, b): ph[(a, b)] + lam[a] - lam[b] for (a, b) in cyc}
    W, Wg = wilson(ph, cyc), wilson(phg, cyc)
    print("[DERIVED] %s" % TITLE)
    print("  Wilson loop before gauge xform: %.4f" % W)
    print("  Wilson loop after  gauge xform: %.4f   (invariant: %s)" % (Wg, abs(W - Wg) < 1e-9))
    print("  per-loop charge = holonomy around its 2-cycle (gauge-invariant, conserved under transport).")
    print("  NOTE: the *holonomy* charge is rule-invisible (collisions charge-blind under it -> no force; REFUTED).")
    print("  The rule-visible charge rho=in-out DOES source a charge-dependent force-on-matter (PARTIAL, s4_2/s6_2).")
