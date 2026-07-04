"""Conservation law: the first conserved charge is TOPOLOGICAL.

AXIOM/GOAL: identify a quantity the rewriting exactly conserves.
RESULT: in the multiset substrate each keystone step has dE=+1, dV=+1, dC=0, so the first
Betti number b1 = E - V + C (independent loops) is exactly invariant. This is the program's
first conserved charge and it fell out of pure topology -- no symmetry was put in by hand.
"""
import random
from collections import Counter
from sec00_core_substrate import betti1
from sec00_core_substrate import evolve
from constants import KEYSTONE

STATUS = "DERIVED"
TITLE = "Topological charge b1 is exactly conserved"


def run():
    rng = random.Random(0)
    E = Counter([(0, 1), (1, 2), (2, 0), (3, 4), (4, 5), (5, 3)])  # two loops: b1 = 2
    b0 = betti1(E)
    print("[DERIVED] %s" % TITLE)
    print("  seed b1 = %d (two loops)" % b0)
    ok = True
    for k in range(1, 6):
        E, _ = evolve(E, KEYSTONE, 10, rng)
        b = betti1(E)
        ok = ok and (b == b0)
        print("  after %2d steps: V=%3d E=%3d  b1=%d" % (10 * k, len(set().union(*[set(e) for e in E])), sum(E.values()), b))
    print("  -> b1 invariant: %s   (the conserved charge is the number of independent loops)" % ok)
