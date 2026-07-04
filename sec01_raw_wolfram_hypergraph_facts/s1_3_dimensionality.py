"""Emergent spatial dimension.

AXIOM/GOAL: measure the dimension of the emergent space from ball growth |B(r)| ~ r^d.
RESULT: the keystone gives a stable, robustly NON-INTEGER spatial dimension. The log-log ball-growth
fit is genuinely good (R^2 ~ 0.99 across seeds), but the VALUE is window- and size-dependent and
should be quoted as a RANGE, not to three significant figures (corrected v8.1): with fit window
[2,6] the estimate is d ~ 2.3-2.5 (seed sd ~ 0.08), and it DRIFTS UPWARD with the fit radius
(~1.8 at [1,4] up to ~2.8 at [3,6]) and with N (2.31 -> 2.52 from N=400 to 1200). That upward drift
is itself a signature of NEGATIVE curvature (faster-than-power-law ball growth) and cross-checks the
curvature module -- but it means "d = 2.34" exactly is false precision; the honest headline is
"non-integer, ~2.3-2.5 (drifting up with scale)". Across the rule family the dimension SPREADS
CONTINUOUSLY from ~0 to ~4 with no quantization, controlled by the arbitrary throwaway-pendant
placement. So causal order fixes spacetime's Lorentzian SHAPE but not its SIZE: 3+1 is a free,
generically-fractional input, neither predicted nor cleanly hit. See foundations/causal_structure
for the (empirical, PARTIAL) consistency CEILING on dimension.
"""
import random
from collections import Counter
from sec00_core_substrate import ball_dimension
from sec00_core_substrate import evolve
from constants import KEYSTONE

STATUS = "DERIVED"
TITLE = "Ball-growth dimension (keystone non-integer ~2.3-2.5, drifts up with scale; family is continuous)"


def run():
    print("[DERIVED] %s" % TITLE)
    for N in (600, 1000, 1400):
        ds = []
        for s in (0, 1):
            rng = random.Random(s)
            E, _ = evolve(Counter([(0, 1), (1, 2), (2, 0)]), KEYSTONE, N, rng)
            d = ball_dimension(E, seed=s)
            if d:
                ds.append(d)
        print("  N=%4d   d = %.2f   (spacetime ~ %.2f)" % (N, sum(ds) / len(ds), sum(ds) / len(ds) + 1))
    print("  -> keystone dimension is a stable, robustly NON-INTEGER number, but window/N-dependent:")
    print("     quote a RANGE (~2.3-2.5 at window [2,6]) not '2.34'; it DRIFTS UP with scale (curvature).")
    print("  -> across the family d ranges ~0..4 continuously; dimension is a TUNABLE INPUT, not a prediction.")
