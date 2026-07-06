"""Numerical sanity battery: the load-bearing claims, asserted.

Checks: (1) b1 conserved over many steps; (2) glider translates at constant velocity;
(3) Wilson loop gauge-invariant; (4) emergent dimension finite and ~2.3.
"""
import random
from collections import Counter
from sec00_core_substrate import betti1, ball_dimension, two_core
from sec00_core_substrate import evolve, apply_rule
from sec06_maxwell_classical_field_theory.s6_1_field_variables import wilson
from constants import KEYSTONE

STATUS = "DERIVED"
TITLE = "Sanity battery for the load-bearing claims"


def run():
    print("[DERIVED] %s" % TITLE)
    ok = {}
    # 1 charge conservation
    rng = random.Random(0)
    E = Counter([(0, 1), (1, 2), (2, 0)]); b0 = betti1(E)
    E, _ = evolve(E, KEYSTONE, 200, rng)
    ok["b1 conserved"] = (betti1(E) == b0)
    # 2 glider constant velocity
    E = Counter([(i, i + 1) for i in range(20)]); E[(17, 16)] += 1; fresh = 21; pos = []
    for _ in range(5):
        tc = two_core(E)
        if len(tc) != 2:
            break
        n = min(tc); pos.append(n)
        E, fresh = apply_rule(E, (n - 1, n, n + 1), KEYSTONE, fresh)
        E, fresh = apply_rule(E, (n - 1, n + 1, n), KEYSTONE, fresh)
    steps = [pos[i] - pos[i + 1] for i in range(len(pos) - 1)]
    ok["glider constant velocity"] = (len(set(steps)) == 1 and steps and steps[0] == 1)
    # 3 gauge invariance
    cyc = [(0, 1), (1, 2), (2, 0)]; ph = {(0, 1): 1.1, (1, 2): -0.4, (2, 0): 0.7}
    lam = {0: 0.5, 1: -1.3, 2: 2.0}
    phg = {(a, b): ph[(a, b)] + lam[a] - lam[b] for (a, b) in cyc}
    ok["Wilson gauge-invariant"] = abs(wilson(ph, cyc) - wilson(phg, cyc)) < 1e-9
    # 4 dimension finite
    rng = random.Random(0)
    E = Counter([(0, 1), (1, 2), (2, 0)]); E, _ = evolve(E, KEYSTONE, 1000, rng)
    d = ball_dimension(E, seed=0)
    ok["dimension ~2.3"] = (d is not None and 1.8 < d < 2.9)
    for k, v in ok.items():
        print("  [%s] %s" % ("PASS" if v else "FAIL", k))
    print("  all passed: %s" % all(ok.values()))
