#!/usr/bin/env python3
"""construct_3manifold.py -- a frame-free construction that DOES produce a certified discrete
3-manifold, via Pachner (bistellar) moves on an abstract simplicial 3-complex. No coordinates.

Start: boundary of the 4-simplex = a 5-vertex triangulated 3-sphere.
Moves (both manifold-preserving):
  1-4: subdivide a tetrahedron with a new vertex (grows vertex count, tree-like).
  2-3: two tets sharing a triangle -> three tets sharing a new edge (bulks, no new vertex).
Every intermediate complex is a genuine triangulated 3-sphere, so referee_3d's link census
must return ALL interior links = 2-spheres, 0 bad. That is the manifold certificate the
project's cubic-target route (s1_23) could never obtain.

Run: PYTHONPATH=. python3 tooling/construct_3manifold.py --selftest
"""
import argparse, itertools, os, random, sys
from collections import defaultdict
_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, _ROOT); sys.path.insert(0, os.path.join(_ROOT, "tooling"))
from referee_3d import link_census
from referee_2d_scaling import ball_growth_dim, lazy_rw_sdim, nx_to_adj
from referee_2d_topology import to_graph


def sphere_seed():
    return set(frozenset(c) for c in itertools.combinations(range(5), 4))  # 5 tets of dDelta^4


def edges_of(tets):
    E = set()
    for t in tets:
        for e in itertools.combinations(sorted(t), 2):
            E.add(frozenset(e))
    return E


def move_1_4(tets, next_v):
    t = random.choice(list(tets))
    a, b, c, d = tuple(t)
    tets.discard(t)
    for tri in itertools.combinations((a, b, c, d), 3):
        tets.add(frozenset(tri + (next_v,)))
    return next_v + 1


def move_2_3(tets, rng):
    tri_to = defaultdict(list)
    for t in tets:
        for tri in itertools.combinations(sorted(t), 3):
            tri_to[frozenset(tri)].append(t)
    E = edges_of(tets)
    cands = [(tri, ts) for tri, ts in tri_to.items() if len(ts) == 2]
    rng.shuffle(cands)
    for tri, (t1, t2) in cands:
        d = next(iter(t1 - tri)); e = next(iter(t2 - tri))
        if d == e or frozenset((d, e)) in E:
            continue
        a, b, c = tuple(tri)
        tets.discard(t1); tets.discard(t2)
        tets.add(frozenset((a, b, d, e)))
        tets.add(frozenset((a, c, d, e)))
        tets.add(frozenset((b, c, d, e)))
        return True
    return False


def build(target_v, seed=0, bulk_ratio=0.6):
    rng = random.Random(seed); random.seed(seed)
    tets = sphere_seed(); nv = 5
    while nv < target_v:
        if rng.random() < bulk_ratio:
            if not move_2_3(tets, rng):
                nv = move_1_4(tets, nv)
        else:
            nv = move_1_4(tets, nv)
    # a few extra bulking passes to reduce tree-likeness
    for _ in range(2 * target_v):
        move_2_3(tets, rng)
    adj = defaultdict(set)
    for t in tets:
        for a, b in itertools.combinations(t, 2):
            adj[a].add(b); adj[b].add(a)
    return tets, {v: set(adj[v]) for v in adj}


def selftest():
    print("=== construct a 3-manifold and CERTIFY it with the link census ===")
    for tv, sd in [(30, 0), (60, 1), (120, 2)]:
        tets, adj = build(tv, seed=sd)
        c = link_census(tets)
        N = len(adj); M = sum(len(adj[v]) for v in adj) // 2
        a = nx_to_adj(to_graph(adj))
        ds = lazy_rw_sdim(a).get("4-12"); dH = ball_growth_dim(a).get("2-6")
        fmt = lambda x: ("%.2f" % x) if isinstance(x, (int, float)) else "n/a"
        status = "3-MANIFOLD (all links spheres)" if c["bad"] == 0 and c["disk"] == 0 else "NOT CLEAN"
        print("  target=%d -> N=%d tets=%d M=%d | links: sphere=%d disk=%d bad=%d -> %s | d_H(2-6)=%s d_s(4-12)=%s"
              % (tv, N, len(tets), M, c["sphere"], c["disk"], c["bad"], status, fmt(dH), fmt(ds)))
        assert c["bad"] == 0, "a Pachner move broke the manifold property -- bug"
    print("ALL PASS: every construction is a certified closed triangulated 3-manifold (0 bad links).")
    print("NOTE: the MANIFOLD is achieved (0 bad links), but the GEOMETRY is degenerate -- random")
    print("Pachner triangulations sit in the crumpled/branched-polymer phase (tiny diameter; d_s and")
    print("d_H are not both ~3). Getting a manifold whose d_s=d_H=3 is the CDT problem: it needs an")
    print("Einstein-Hilbert-type action + a causal (foliated) restriction on the moves, not more moves.")


if __name__ == "__main__":
    ap = argparse.ArgumentParser(); ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--target", type=int, default=120); ap.add_argument("--seed", type=int, default=0)
    a = ap.parse_args()
    if a.selftest:
        selftest()
    else:
        tets, adj = build(a.target, seed=a.seed); print(link_census(tets))
