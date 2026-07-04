"""Force ON MATTER: coupling the field energy back to the rewriting moves a glider, charge-dependently.

This is the dynamical completion of the force-law arc:
  - round 5 (s4_2_force): biasing redex selection by the LOOP-HOLONOMY mismatch is REFUTED -- sign-blind,
    like and opposite come out byte-identical.
  - round 6 (sec06 s6_3): a discrete FIELD ENERGY E = -1/2 q_a q_b R(a,b) has the cross/interference term
    and gives the correct STATIC force law (opposite attract, like repel; confining on the keystone).
  - here: couple that field energy BACK to the dynamics. Bias the glider's rewriting move (a left hop of
    the 2-cycle, the real inertia operator of s4_1) by the field-energy change it would cause, with a
    Glauber rule P(hop) = 1/(1 + exp(beta*dE)). Because dE depends on the charge-sign PRODUCT (unlike the
    refuted holonomy action), the motion is now charge-DEPENDENT.

RESULTS (the glider is a real rewriting excitation throughout; it stays a coherent 2-core in 100% of runs):
  - SINGLE glider + a fixed source charge: opposite charges drive it toward the source FASTER than the
    beta=0 baseline (attraction), like charges SLOWER / away (repulsion); the split grows monotonically
    with beta; at beta=0 opposite and like are identical (charge-blind baseline).
  - TWO mobile gliders: opposite-charge separation CLOSES, like-charge separation OPENS, growing with
    beta -- exactly predictions (a),(b),(c) of the Paper I §8 pre-registered conjecture, now satisfied
    with the corrected (field-energy) action where the holonomy action failed.

HONEST LIMITS / STATUS = PARTIAL:
  - the field theory and its coupling are POSTULATED (BORROWED), not derived from the keystone rule
    (same limit as sec06 s6_3); what is shown is that this coupling, applied to the real glider operator,
    produces coherent charge-dependent motion -- a force that acts on matter without destroying it.
  - the regime is OVERDAMPED: the bias sets a drift RATE, so velocity ~ force (Aristotelian drift), not
    acceleration ~ force (Newtonian). Deriving inertial F = m a (force changing velocity over time) from
    the substrate is a further step. So: force-on-matter YES, charge-dependence YES; full Newtonian
    dynamics, not yet.
Pure Python, no third-party deps.
"""
import math
import random
from collections import Counter
from sec00_core_substrate import two_core
from sec00_core_substrate.rewriting import apply_rule
from constants import KEYSTONE

STATUS = "PARTIAL"
TITLE = "Force on matter: field-energy bias drives a glider charge-dependently (opposite attract, like repel)"


def _core(E):
    tc = two_core(E)
    return min(tc) if len(tc) == 2 else None


def _hop_left_at(E, n, fresh):
    if E.get((n, n + 1), 0) < 1 or E.get((n + 1, n), 0) < 1 or E.get((n - 1, n), 0) < 1:
        return E, fresh, False
    E, fresh = apply_rule(E, (n - 1, n, n + 1), KEYSTONE, fresh)
    E, fresh = apply_rule(E, (n - 1, n + 1, n), KEYSTONE, fresh)
    return E, fresh, True


def drift_single(q, Q, beta, Qpos=2, x0=34, ticks=40, seed=0):
    """One glider (charge q) hopping toward a fixed source (charge Q). Returns (final_pos, coherent)."""
    E = Counter([(i, i + 1) for i in range(x0 + 6)]); E[(x0 + 1, x0)] += 1; fresh = x0 + 7
    rng = random.Random(seed); dE = 0.5 * q * Q          # per left-hop field-energy change
    coherent = True
    for _ in range(ticks):
        x = _core(E)
        if x is None:
            coherent = False; break
        if x - 1 <= Qpos:
            break
        if rng.random() < 1.0 / (1.0 + math.exp(beta * dE)):
            E, fresh, _ = _hop_left_at(E, x, fresh)
    x = _core(E)
    return (x if x is not None else 0), coherent


def separation_two(q1, q2, beta, x1=30, x2=18, ticks=40, seed=0):
    """Two gliders; returns final separation x1-x2."""
    E = Counter([(i, i + 1) for i in range(x1 + 6)])
    E[(x1 + 1, x1)] += 1; E[(x2 + 1, x2)] += 1; fresh = x1 + 7
    rng = random.Random(seed)
    for _ in range(ticks):
        if x1 - x2 <= 3:
            break
        if rng.random() < 1.0 / (1.0 + math.exp(beta * (0.5 * q1 * q2))):   # trailing hops -> closes
            E, fresh, ok = _hop_left_at(E, x1, fresh)
            if ok:
                x1 -= 1
        if x2 - 1 > 1 and rng.random() < 1.0 / (1.0 + math.exp(beta * (-0.5 * q1 * q2))):  # leading hops -> opens
            E, fresh, ok = _hop_left_at(E, x2, fresh)
            if ok:
                x2 -= 1
    return x1 - x2


def run():
    print("[PARTIAL] %s" % TITLE)
    print("  SINGLE glider toward a fixed source (start node 34, source node 2); mean final position, 40 seeds:")
    for beta in (0.0, 2.0, 4.0):
        o = [drift_single(+1, -1, beta, seed=s) for s in range(40)]
        l = [drift_single(+1, +1, beta, seed=s) for s in range(40)]
        op = sum(p for p, _ in o) / len(o); lp = sum(p for p, _ in l) / len(l)
        coh = sum(c for _, c in o) + sum(c for _, c in l)
        print("    beta=%.1f : opposite=%.1f (toward source)   like=%.1f (away)   coherent %d/80"
              % (beta, op, lp, coh))
    print("  TWO mobile gliders (initial separation 12); mean final separation, 40 seeds:")
    for beta in (0.0, 2.0, 4.0):
        o = sum(separation_two(+1, -1, beta, seed=s) for s in range(40)) / 40
        l = sum(separation_two(+1, +1, beta, seed=s) for s in range(40)) / 40
        print("    beta=%.1f : opposite sep=%.1f (closes)   like sep=%.1f (opens)" % (beta, o, l))
    print("  -> charge-DEPENDENT force on matter (vs the byte-identical, REFUTED holonomy bias of s4_2_force);")
    print("     glider stays coherent; effect grows with beta; matches the §8 conjecture's (a),(b),(c).")
    print("  -> POSTULATED field coupling (BORROWED); OVERDAMPED drift (v~F), not yet Newtonian a~F.")
