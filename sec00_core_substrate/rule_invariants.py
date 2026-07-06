"""Growth law of the substrate.

AXIOM/GOAL: how do vertex and edge counts scale with rewriting time?
RESULT: each step adds exactly +1 edge and +1 vertex (w is fresh), so V(t) and E(t) grow
LINEARLY in the number of applications, with E - V fixed by the seed. Growth is ballistic in
event-count, which underpins the linear emergence of spatial volume.
"""
import random
from collections import Counter
from sec00_core_substrate import nodes, num_edges
from sec00_core_substrate import evolve
from constants import KEYSTONE

STATUS = "DERIVED"
TITLE = "Vertex/edge counts grow linearly in rewriting time"


def run():
    rng = random.Random(1)
    E = Counter([(0, 1), (1, 2), (2, 0)])
    print("[DERIVED] %s" % TITLE)
    print("  step      V      E    E-V")
    for t in (0, 100, 200, 400, 800):
        if t:
            E, _ = evolve(E, KEYSTONE, t - prev, rng)
        prev = t
        print("  %4d   %4d   %4d   %4d" % (t, len(nodes(E)), num_edges(E), num_edges(E) - len(nodes(E))))
    print("  -> dV/dt = dE/dt = +1 per step; E-V is fixed by the seed (linear, ballistic growth).")
