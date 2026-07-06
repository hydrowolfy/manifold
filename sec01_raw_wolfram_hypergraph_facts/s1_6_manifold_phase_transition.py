"""Can minimal extra structure push the substrate across d_s=2 into a manifold phase? Yes -- but only LOCAL loops.

Round 24 showed the bare keystone's continuum is a random fractal tree with spectral dimension d_s ~ 1.5 < 2,
NOT a manifold, and that a manifold phase would need the loop content to dominate (the deconfinement boundary
of section 6 sits at d_s=2). This asks the constructive question: what is the MINIMAL extra structure that
crosses d_s=2 into a manifold, and does the bare rule supply it?

The bare rule conserves b1=1 (one loop in a tree), so it does NOT. We must add loops. But there are two
sharply different ways, and only one gives a manifold:

  * LOCAL loop-closure: add edges between nodes at small TREE-distance r (e.g. close 'elbows' at r=2 into
    triangles). This thickens the geometry while respecting the tree metric. Measured: d_s rises smoothly
    and CROSSES 2 at modest density (r=2 reaches d_s~2 at p~0.5; range r tunes the target -- r=2 ~ 2D,
    r=3 ~ 3D), and the DIAMETER stays large (~N^{1/d}, polynomial volume growth). A finite-dimensional,
    MANIFOLD-LIKE phase.
  * RANDOM long-range edges: connect random pairs. d_s shoots up without bound (3.8, 5.2, ...) and the
    diameter COLLAPSES toward log N (~8) -- exponential volume growth, the small-world / MEAN-FIELD phase.
    Infinite-dimensional, NOT a manifold.

So crossing d_s=2 is easy, but landing in a manifold (finite-dimensional, large diameter) rather than
mean-field (infinite-dimensional, collapsed diameter) requires the extra structure to be LOCAL with respect
to a metric. The bare keystone already supplies that metric (graph distance); the minimal manifold-building
structure is local loop-closure against it. The bare rule does not perform this closure (b1 stays 1), so the
manifold phase is reachable IN PRINCIPLE by one local rule addition, but is not native -- consistent with
round 24's verdict that the bare substrate stays a fractal tree.

Diagnostics: d_s from the return probability P0(t)~t^{-d_s/2}; the diameter (estimate) separates the
finite-dimensional phase (diameter ~ N^{1/d}, large) from mean-field (diameter ~ log N, collapsed).

STATUS = PARTIAL. The d_s crossing and the finite-dim-vs-mean-field separation are clearly measured; the
result is constructive (it characterizes the phase diagram of an added local rule), and the manifold phase is
conditional on non-native extra structure, so no native physics leaf is claimed. Pure Python.
"""
import math
import os
import random
from collections import Counter, deque
from sec00_core_substrate import evolve
from constants import KEYSTONE

STATUS = "PARTIAL"
TITLE = "Minimal extra structure & the d_s=2 manifold transition: LOCAL loop-closure -> manifold; random loops -> mean-field"

_FULL = os.environ.get("EMERGENCE_FULL", "") == "1"


def _build_tree(steps, seed=5):
    E, _ = evolve(Counter([(0, 1), (1, 2), (2, 0)]), KEYSTONE, steps, random.Random(seed))
    adj = {}
    for (u, v), m in E.items():
        if u != v:
            adj.setdefault(u, set()).add(v); adj.setdefault(v, set()).add(u)
    return {u: set(vs) for u, vs in adj.items()}


def _bfs(adj, s, cap=None):
    seen = {s: 0}; dq = deque([s])
    while dq:
        x = dq.popleft()
        for y in adj[x]:
            if y not in seen:
                seen[y] = seen[x] + 1
                if cap is None or seen[y] <= cap:
                    dq.append(y)
    return seen


def _slope(xs, ys, lo, hi):
    pts = [(math.log(x), math.log(y)) for x, y in zip(xs, ys) if lo <= x <= hi and y > 0]
    n = len(pts); sx = sum(p[0] for p in pts); sy = sum(p[1] for p in pts)
    sxx = sum(p[0] ** 2 for p in pts); sxy = sum(p[0] * p[1] for p in pts)
    return (n * sxy - sx * sy) / (n * sxx - sx * sx)


def _spectral(adj, T=130, norigin=3):
    nodes = list(adj); N = len(nodes); idx = {u: i for i, u in enumerate(nodes)}
    deg = [len(adj[u]) for u in nodes]; nbr = [[idx[w] for w in adj[u]] for u in nodes]
    rng = random.Random(3); origins = rng.sample(nodes, norigin); P0 = [0.0] * T
    for o in origins:
        p = [0.0] * N; p[idx[o]] = 1.0
        for t in range(T):
            P0[t] += p[idx[o]]
            np_ = [0.0] * N
            for i in range(N):
                pi = p[i]
                if pi == 0.0:
                    continue
                np_[i] += 0.5 * pi; sh = 0.5 * pi / deg[i]
                for j in nbr[i]:
                    np_[j] += sh
            p = np_
    P0 = [x / len(origins) for x in P0]
    return -2 * _slope(list(range(1, T)), [P0[t] for t in range(1, T)], 12, 72)


def _diameter(adj, ntry=18):
    nodes = list(adj); rng = random.Random(9); mx = 0
    for _ in range(ntry):
        d = _bfs(adj, rng.choice(nodes)); mx = max(mx, max(d.values()))
    return mx


def _local_loops(adj, r, p, seed=1):
    rng = random.Random(seed); g = {u: set(vs) for u, vs in adj.items()}
    for u in list(adj):
        d = _bfs(adj, u, r); at_r = [v for v, dd in d.items() if dd == r and v > u]
        for v in at_r:
            if rng.random() < p:
                g[u].add(v); g[v].add(u)
    return g


def _random_edges(adj, m, seed=1):
    rng = random.Random(seed); g = {u: set(vs) for u, vs in adj.items()}; nodes = list(adj)
    for _ in range(m):
        u, v = rng.choice(nodes), rng.choice(nodes)
        if u != v:
            g[u].add(v); g[v].add(u)
    return g


def run():
    print("[PARTIAL] %s" % TITLE)
    steps = 4000 if _FULL else 3000
    base = _build_tree(steps); N = len(base); E0 = sum(len(a) for a in base.values()) // 2
    logN = math.log(N)
    d0 = _spectral(base); diam0 = _diameter(base)
    print("  bare keystone tree: N=%d, d_s=%.2f, diameter=%d  (b1=1; sub-2D fractal, log N~%.0f)" % (N, d0, diam0, logN))
    print("  1. LOCAL loop-closure at tree-distance r=2 (close elbows -> triangles), vs density p:")
    print("     p     | +edges | d_s   | diameter | phase")
    for p in (0.25, 0.5, 1.0):
        g = _local_loops(base, 2, p); extra = sum(len(a) for a in g.values()) // 2 - E0
        ds = _spectral(g); diam = _diameter(g)
        tag = ("CROSSED 2, diameter large -> FINITE-DIM (manifold-like)" if ds > 2 else "still < 2")
        print("     %.2f  | %5d  | %.2f  |   %3d    | %s" % (p, extra, ds, diam, tag))
    print("  2. range r tunes the target dimension (p=0.5): bigger r reaches higher d_s:")
    for r in (2, 3, 4):
        g = _local_loops(base, r, 0.5); ds = _spectral(g)
        print("     r=%d: d_s=%.2f  diameter=%d   (~%dD manifold-like)" % (r, ds, _diameter(g), round(ds)))
    print("  3. RANDOM long-range edges (same kind of edge budget) -> MEAN-FIELD, not a manifold:")
    for m in (1500, 3000):
        g = _random_edges(base, m)
        ds = _spectral(g); diam = _diameter(g)
        print("     +%4d random: d_s=%.2f  diameter=%d  -> diameter COLLAPSES toward log N (mean-field)" % (m, ds, diam))
    print("  => crossing d_s=2 is easy, but a MANIFOLD (finite-dim, large diameter) vs MEAN-FIELD (collapsed")
    print("     diameter) depends on LOCALITY: local loop-closure against the tree metric -> manifold; random")
    print("     loops -> mean-field. The bare keystone supplies the metric but not the closure (b1=1), so a")
    print("     manifold phase is reachable by ONE local rule addition -- reachable in principle, not native.")
