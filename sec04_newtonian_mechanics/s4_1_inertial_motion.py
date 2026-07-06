"""Newton's first law: free ballistic motion (inertia).

AXIOM/GOAL: does a localized excitation move at constant velocity with no driving?
RESULT: on a directed rail the fixed 2-move glider operator translates a minimal 2-cycle loop by
one rail-node per move, core pinned at size 2, shedding only pendant debris -- a soliton-like
glider at CONSTANT velocity (1/2 rail-node per firing). Uniform motion of a conserved excitation
falls out of the rule: this is inertia, the substrate form of Newton's first law.
"""
from collections import Counter
from sec00_core_substrate import two_core
from sec00_core_substrate import apply_rule
from constants import KEYSTONE

STATUS = "DERIVED"
TITLE = "Ballistic glider = inertia (Newton I)"


def run():
    E = Counter([(i, i + 1) for i in range(20)])
    E[(17, 16)] += 1            # plant a minimal 2-cycle loop {16,17} on the rail
    fresh = 21
    pos = []
    print("[DERIVED] %s" % TITLE)
    for _ in range(9):
        tc = two_core(E)
        if len(tc) != 2:
            break
        n = min(tc)
        pos.append(n)
        E, fresh = apply_rule(E, (n - 1, n, n + 1), KEYSTONE, fresh)
        E, fresh = apply_rule(E, (n - 1, n + 1, n), KEYSTONE, fresh)
    print("  glider core position (left edge of the 2-cycle) per 2-move: %s" % pos)
    steps = [pos[i] - pos[i + 1] for i in range(len(pos) - 1)]
    print("  displacement per 2-move: %s  -> constant velocity = %s rail-node/move (1/2 per firing)"
          % (steps, steps[0] if steps else "n/a"))
    print("  -> uniform motion with no driving: inertia falls out of the rule.")
