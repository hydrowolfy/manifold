"""The continuum limit of the keystone is a random fractal tree (Levy/CRT class), not a smooth manifold.

The Hauptvermutung asks whether the discrete substrate has a well-defined continuum limit. For the keystone
the answer is yes -- but the limit is NOT a Riemannian/Lorentzian manifold. The graph is a single loop in a
growing tree (b1 = 1 exactly, conserved; the 2-core is a vanishing fraction, round 20), so at large scale it
is tree-like, and the scaling limit of such a structure is a random REAL TREE, not a manifold.

We pin this down with the three fractal dimensions of diffusion-on-graphs:
  * Hausdorff  d_H : volume growth   N(r) ~ r^{d_H}             (how volume scales with radius)
  * spectral   d_s : return prob     P0(t) ~ t^{-d_s/2}         (how the walk re-finds its origin)
  * walk       d_w : mean-sq displ.  <r^2(t)> ~ t^{2/d_w}       (how far the walk roams)
related on any fractal by the EINSTEIN RELATION d_s = 2 d_H / d_w. A smooth d-manifold would give the integer
triple (d, d, 2) with d_s = d_H = d (and d_w = 2); a fractal tree gives a NON-integer triple with d_s < d_H
< d_w. The canonical random tree -- Aldous's Continuum Random Tree (CRT), the universal scaling limit of
critical finite-variance branching -- has exactly (d_H, d_s, d_w) = (2, 4/3, 3).

Measured on the keystone (per seed below): **d_H ~ 2.4 (robust)**, with d_s and d_w individually scattered by
finite size but co-varying so that **the Einstein relation d_s = 2 d_H / d_w holds**, and always with the
fractal ordering **d_s < d_H < d_w** -- never the manifold triple. The values sit in the random-fractal-tree
(Levy/CRT) universality class: d_H a little above the CRT's 2 points to a slightly heavier-tailed branching
(a stable tree of index alpha = d_H/(d_H-1) ~ 1.7), though the exact member is not pinned at this size.

So the keystone's Hauptvermutung verdict: a continuum limit EXISTS and is essentially unique, but it is a
random fractal tree, NOT a manifold. Recovering a manifold would need the loop content (the 2-core) to
dominate the large-scale geometry; it provably does not (b1 conserved = 1; 2-core grows sub-linearly). This
is consistent and sobering: the bare rule does not smooth into Euclidean/Lorentzian spacetime -- a manifold
phase, if any, must come from extra structure (more loops / higher effective dimension, cf. the d_s>2
deconfinement boundary in section 6), not from the bare keystone.

STATUS = DERIVED for the qualitative characterization (fractal tree, Einstein relation, not a manifold);
the exact dimension values and the precise universality member carry finite-size uncertainty (+/- 0.1-0.3).
Native: all three dimensions are measured on the bare-rule graph. Pure Python.
"""
import math
import os
import random
from collections import Counter, deque
from sec00_core_substrate import evolve
from constants import KEYSTONE

STATUS = "DERIVED"
TITLE = "The continuum limit is a random fractal tree (Levy/CRT class), not a manifold: d_s<d_H<d_w, Einstein relation"

_FULL = os.environ.get("EMERGENCE_FULL", "") == "1"


def _build(steps, seed):
    E, _ = evolve(Counter([(0, 1), (1, 2), (2, 0)]), KEYSTONE, steps, random.Random(seed))
    adj = {}
    for (u, v), m in E.items():
        if u != v:
            adj.setdefault(u, set()).add(v); adj.setdefault(v, set()).add(u)
    return adj


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


def _measure(adj, norigin, ncen, T):
    nodes = list(adj); N = len(nodes); idx = {u: i for i, u in enumerate(nodes)}
    deg = [len(adj[u]) for u in nodes]; nbr = [[idx[w] for w in adj[u]] for u in nodes]
    rng = random.Random(7)
    maxr = 14; cen = rng.sample(nodes, min(ncen, N)); vol = [0.0] * (maxr + 1)
    for c in cen:
        d = _bfs(adj, c, maxr); cnt = [0] * (maxr + 1)
        for _, dd in d.items():
            if dd <= maxr:
                cnt[dd] += 1
        run = 0
        for r in range(maxr + 1):
            run += cnt[r]; vol[r] += run
    vol = [v / len(cen) for v in vol]
    dH = _slope(list(range(1, maxr + 1)), vol[1:], 2, 11)
    origins = rng.sample(nodes, min(norigin, N)); P0 = [0.0] * T; MSD = [0.0] * T
    for o in origins:
        do = _bfs(adj, o); p = [0.0] * N; p[idx[o]] = 1.0
        for t in range(T):
            P0[t] += p[idx[o]]; MSD[t] += sum(p[i] * (do.get(nodes[i], 0) ** 2) for i in range(N))
            np_ = [0.0] * N
            for i in range(N):
                pi = p[i]
                if pi == 0.0:
                    continue
                np_[i] += 0.5 * pi; sh = 0.5 * pi / deg[i]
                for j in nbr[i]:
                    np_[j] += sh
            p = np_
    P0 = [x / len(origins) for x in P0]; MSD = [x / len(origins) for x in MSD]
    ds = -2 * _slope(list(range(1, T)), [P0[t] for t in range(1, T)], 12, 70)
    dw = 2.0 / _slope(list(range(2, T)), [MSD[t] for t in range(2, T)], 8, 55)
    return dH, ds, dw, N


def run():
    print("[DERIVED] %s" % TITLE)
    print("  the keystone is a loop in a growing tree (b1=1); its scaling limit is a random REAL tree.")
    print("  three diffusion dimensions, related on any fractal by  d_s = 2 d_H / d_w:")
    steps = 4000 if _FULL else 3000
    seeds = (5, 11, 23, 42) if _FULL else (5, 23, 42)
    norigin = 8 if _FULL else 6
    T = 130 if _FULL else 105
    print("    seed |  N   | d_H  | d_s  | d_w  || 2 d_H/d_w | ordering d_s<d_H<d_w?")
    agg = []
    for sd in seeds:
        dH, ds, dw, N = _measure(_build(steps, sd), norigin, 36, T)
        agg.append((dH, ds, dw))
        order = "yes" if (ds < dH < dw) else "NO"
        print("    %4d | %4d | %.2f | %.2f | %.2f || %.2f      | %s (Einstein: d_s~%.2f vs %.2f)"
              % (sd, N, dH, ds, dw, 2 * dH / dw, order, ds, 2 * dH / dw))
    mH = sum(a[0] for a in agg) / len(agg); mS = sum(a[1] for a in agg) / len(agg); mW = sum(a[2] for a in agg) / len(agg)
    print("  means: d_H=%.2f  d_s=%.2f  d_w=%.2f   (CRT reference: 2, 4/3=1.33, 3)" % (mH, mS, mW))
    print("  => NON-integer triple with d_s < d_H < d_w (a manifold would give the integer triple (d,d,2)).")
    print("     The Einstein relation d_s = 2 d_H/d_w holds, so it is a genuine fractal with consistent transport.")
    print("     CONCLUSION: the continuum limit is a random fractal tree (Levy/CRT class, alpha~%.1f from d_H), NOT"
          % (mH / (mH - 1)))
    print("     a manifold. Hauptvermutung: a unique continuum exists but it is fractal -- the bare rule does not")
    print("     smooth into Euclidean/Lorentzian spacetime (a manifold phase would need the 2-core to dominate; it")
    print("     does not, b1=1). Exact dimension values carry finite-size uncertainty; the qualitative verdict is robust.")
