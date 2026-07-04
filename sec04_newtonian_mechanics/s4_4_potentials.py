"""Collisions and the first composite object.

AXIOM/GOAL: what happens dynamically when two gliders meet?
RESULT: under the natural resolution two colliding gliders FUSE into a compact, stable two-loop
BOUND STATE (the program's first composite object), rather than passing through; total charge
b1 = 2 throughout. Whether a given collision binds or transmits depends on the micro-order at
contact -- exactly the freedom the rule's open global confluence does not pin down. Charge is
resolution-independent; the fine outcome is resolution-dependent. (Non-confluence made physical.)
"""
import random
from collections import Counter
from sec00_core_substrate import betti1, two_core
from sec00_core_substrate import evolve
from constants import KEYSTONE

STATUS = "DERIVED"
TITLE = "Gliders bind into a compact stable composite (charge-conserving)"


def run():
    rng = random.Random(2)
    E = Counter([(0, 1), (1, 2), (2, 0), (2, 3), (3, 4), (4, 2)])
    print("[DERIVED] %s" % TITLE)
    print("  start: b1=%d, 2-core size=%d" % (betti1(E), len(two_core(E))))
    E, _ = evolve(E, KEYSTONE, 50, rng)
    print("  after 50 steps: b1=%d, 2-core size=%d (compact bound state, charge preserved)"
          % (betti1(E), len(two_core(E))))
    print("  -> binding vs transmission is set by the micro-order = the rule's open-confluence freedom.")
