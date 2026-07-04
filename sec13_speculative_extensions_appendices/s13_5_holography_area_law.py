"""Holographic area law on the bare keystone graph -- and the static/dynamic dimension split.

AXIOM/GOAL: does an area law (boundary sub-extensive relative to bulk volume) hold for the ACTUAL
keystone graph -- not only for the continuum causal-set sprinkling the monolith measured?
RESULT (PARTIAL, honestly): YES qualitatively -- the edge boundary of a region is SUB-EXTENSIVE. The
ratio |dR|/|R| falls steadily as regions grow (e.g. ~1.25 at |R|~8 down to ~0.51 at |R|~98), so the
bare graph is NOT a pure expander ("all surface, no bulk"); a bulk/boundary separation exists. But the
area-law EXPONENT is only loosely pinned: |dR| ~ |R|^beta with beta ~ 0.65-0.75 and a noisy fit
(R^2 ~ 0.6), because the ramified graph is locally irregular (pendant clusters vs the 2-core). The
implied area dimension d = 1/(1-beta) ~ 2.5-3.5 is broadly on the STATIC/volume side, distinctly above
the transport dimension ~1.3.

SYNTHESIS (the real payoff): the substrate's effective dimension splits cleanly into two families,
measured five ways:
  STATIC / counting   -- volume ball-growth ~2.3-2.5 (s1_3), area-law boundary ~2.5-3.5 (here)
  DYNAMIC / transport -- spectral ~1.3-1.5 (s1_3_spectral), causal-cone ~1.3 (s7_1), entropy-rate
                         d_s/2 ~1.6 (s5_2)
Static probes (how much stuff, how much boundary) see a higher dimension than dynamic probes (how a
walker or signal actually spreads). That gap is the quantitative content of the ramified geometry.

STATUS: PARTIAL -- sub-extensivity is robust; the sharp area-law exponent and a true entanglement
entropy (Gaussian-field / Casini-Huerta, which needs spectral linear algebra) are not done on the bare
graph. The full holographic entropy area law remains the continuum-sprinkling result. Pure Python.
"""
import math
import random
from collections import deque, Counter
from sec00_core_substrate import evolve
from constants import KEYSTONE

STATUS = "PARTIAL"
TITLE = "Area law qualitatively holds (boundary sub-extensive); area dim ~2.5-3.5 (static side)"


def _adj(E):
    a = {}
    for (u, v), m in E.items():
        a.setdefault(u, {}); a.setdefault(v, {})
        a[u][v] = a[u].get(v, 0) + m; a[v][u] = a[v].get(u, 0) + m
    return a


def _ball(adj, c, r):
    seen = {c: 0}; dq = deque([c])
    while dq:
        u = dq.popleft()
        if seen[u] >= r:
            continue
        for w in adj[u]:
            if w not in seen:
                seen[w] = seen[u] + 1; dq.append(w)
    return set(seen)


def _boundary(adj, R):
    return sum(m for u in R for w, m in adj[u].items() if w not in R)


def measure(E, sample=150, seed=1):
    adj = _adj(E); V = [u for u in adj if adj[u]]
    rng = random.Random(seed); pts = []; ratios = {}
    for c in rng.sample(V, min(sample, len(V))):
        for r in (2, 3, 4, 5, 6):
            R = _ball(adj, c, r)
            if 6 <= len(R) < 0.5 * len(V):
                b = _boundary(adj, R)
                if b > 0:
                    pts.append((math.log(len(R)), math.log(b)))
                    ratios.setdefault(r, []).append(b / len(R))
    n = len(pts); sx = sum(x for x, _ in pts); sy = sum(y for _, y in pts)
    sxx = sum(x * x for x, _ in pts); sxy = sum(x * y for x, y in pts); syy = sum(y * y for _, y in pts)
    beta = (n * sxy - sx * sy) / (n * sxx - sx * sx)
    den = math.sqrt((n * sxx - sx * sx) * (n * syy - sy * sy))
    r2 = ((n * sxy - sx * sy) / den) ** 2
    return beta, r2, ratios


def run():
    print("[PARTIAL] %s" % TITLE)
    rng = random.Random(0)
    E, _ = evolve(Counter([(0, 1), (1, 2), (2, 0)]), KEYSTONE, 3000, rng)
    beta, r2, ratios = measure(E)
    print("  boundary/volume ratio falls as regions grow (sub-extensive => an area law holds):")
    print("    " + "  ".join("r=%d:%.2f" % (r, sum(v) / len(v)) for r, v in sorted(ratios.items())))
    print("  |dR| ~ |R|^%.2f  (R^2=%.2f, noisy) -> area dimension d ~ %.1f (STATIC/volume side)"
          % (beta, r2, 1 / (1 - beta)))
    print("  SYNTHESIS - dimension splits in two: STATIC (volume ~2.4, area ~2.5-3.5) vs")
    print("              DYNAMIC (spectral ~1.3, causal-cone ~1.3, entropy-rate ~1.6).")
    print("  -> static probes see more dimension than transport probes: the ramified-geometry gap.")
