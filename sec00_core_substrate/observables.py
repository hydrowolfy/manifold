"""Observables read off the substrate."""
import math
import random
from collections import deque, Counter
from sec00_core_substrate.hypergraph import nodes, num_edges, components


def betti1(E):
    """First Betti number = independent loops = the conserved topological charge."""
    return num_edges(E) - len(nodes(E)) + components(E)


def two_core(E):
    """Iteratively peel nodes of degree < 2; survivors are the loop/defect support."""
    alive = set(nodes(E))
    while True:
        deg = Counter()
        for (a, b), m in E.items():
            if a in alive and b in alive:
                deg[a] += m; deg[b] += m
        rem = [v for v in alive if deg.get(v, 0) < 2]
        if not rem:
            break
        for v in rem:
            alive.discard(v)
    return alive


def ball_dimension(E, centers=45, R=8, lo=2, hi=6, seed=1):
    """Spatial dimension from |B(r)| ~ r^d: fit log<|B(r)|> vs log r. None if too small."""
    adj = {}
    for (a, b), m in E.items():
        adj.setdefault(a, set()).add(b)
        adj.setdefault(b, set()).add(a)
    V = list(adj)
    rng = random.Random(seed)
    if len(V) < 60:
        return None
    avg = {r: 0.0 for r in range(R + 1)}
    nc = min(centers, len(V))
    for s in rng.sample(V, nc):
        seen = {s: 0}; dq = deque([s]); cnt = {0: 1}
        while dq:
            u = dq.popleft(); d = seen[u]
            if d >= R:
                continue
            for v in adj.get(u, ()):
                if v not in seen:
                    seen[v] = d + 1; cnt[d + 1] = cnt.get(d + 1, 0) + 1; dq.append(v)
        cum = 0
        for r in range(R + 1):
            cum += cnt.get(r, 0); avg[r] += cum
    for r in avg:
        avg[r] /= nc
    xs = [math.log(r) for r in range(lo, hi + 1)]
    ys = [math.log(avg[r]) for r in range(lo, hi + 1) if avg[r] > 0]
    if len(ys) < len(xs):
        return None
    n = len(xs); sx = sum(xs); sy = sum(ys)
    sxx = sum(x * x for x in xs); sxy = sum(x * y for x, y in zip(xs, ys))
    return (n * sxy - sx * sy) / (n * sxx - sx * sx)


def degree_sequence(E):
    deg = Counter()
    for (a, b), m in E.items():
        deg[a] += m; deg[b] += m
    return sorted(deg.values(), reverse=True)


# --- §0.4 Observables: demonstrate the exact read-outs (counts, charge b1, 2-core localization) ---
def run():
    import random
    from collections import Counter
    from sec00_core_substrate.rewriting import evolve
    from constants import KEYSTONE
    print("[DEF] 0.4 Observables -- exact read-outs on the substrate")
    rng = random.Random(0)
    E, _ = evolve(Counter([(0, 1), (1, 2), (2, 0), (2, 3), (3, 4), (4, 2)]), KEYSTONE, 40, rng)
    print("  after 40 steps: b1 (loops) = %d, 2-core size = %d, max degree = %d, %d nodes"
          % (betti1(E), len(two_core(E)), max(degree_sequence(E)), len(nodes(E))))
    print("  b1 is the exactly-conserved topological charge; the 2-core is the loop's support (localization).")
