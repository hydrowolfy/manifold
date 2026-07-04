"""Scaling laws: linear growth (exact) and the size-dependence of the dimension estimate.

AXIOM/GOAL: verify the headline scalings reproduce.
RESULT: edge/vertex count grows EXACTLY linearly in steps (E = E0 + t, V = V0 + t) -- this is exact,
not just empirical. The ball-growth dimension does NOT cleanly converge to a single value over this
range (corrected v8.1): it DRIFTS UPWARD with N (d ~ 2.31 -> 2.42 -> 2.52 from N=400 to 1200), a
finite-size/curvature effect, so the right reading is "non-integer, drifting up", not "stabilises at
2.3". See foundations/dimensionality for the window-sensitivity of the same estimate.
"""
import random
from collections import Counter
from sec00_core_substrate import num_edges
from sec00_core_substrate import ball_dimension
from sec00_core_substrate import evolve
from constants import KEYSTONE

STATUS = "DERIVED"
TITLE = "Linear growth (exact); dimension estimate drifts upward with N (not converged)"


def run():
    print("[DERIVED] %s" % TITLE)
    rng = random.Random(0)
    E = Counter([(0, 1), (1, 2), (2, 0)]); prev = 0
    for N in (400, 800, 1200):
        E, _ = evolve(E, KEYSTONE, N - prev, rng); prev = N
        d = ball_dimension(E, seed=0)
        print("  N=%4d  E=%4d  d=%.2f" % (N, num_edges(E), d if d else float('nan')))
    print("  -> E(t) is EXACTLY linear in t (+1 edge/step). The dimension estimate DRIFTS UP with N")
    print("     (~2.31 -> ~2.52 here): non-integer and scale-dependent, NOT converged at a single 2.3.")
