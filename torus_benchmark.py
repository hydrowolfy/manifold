#!/usr/bin/env python3
"""Exact benchmark: periodic Kuhn triangulation of the flat 3-torus T^3, measured with the
same estimators/windows as all other runs. The finite-size line 'success' must be scored on."""
import argparse, itertools, json, sys
from collections import defaultdict

sys.path[:0] = ["/tmp/m", "/tmp/m/tooling"]
from referee_3d import link_census
from referee_2d_scaling import lazy_rw_sdim, ball_growth_dim, nx_to_adj
from referee_2d_topology import to_graph


def kuhn_torus(m):
    tets = set()
    for base in itertools.product(range(m), repeat=3):
        for perm in itertools.permutations(range(3)):
            cur = list(base); path = [tuple(cur)]
            for ax in perm:
                cur = list(cur); cur[ax] = (cur[ax] + 1) % m
                path.append(tuple(cur))
            assert len(set(path)) == 4
            tets.add(frozenset(path))
    return tets


ap = argparse.ArgumentParser()
ap.add_argument("--ms", type=int, nargs="+", default=[5, 6, 8])
ap.add_argument("--long", action="store_true", dest="long_win")
ap.add_argument("--log", default=None)
a = ap.parse_args()
for m in a.ms:
    tets = kuhn_torus(m)
    c = link_census(list(tets))
    adj = defaultdict(set)
    for t in tets:
        for x, y in itertools.combinations(t, 2):
            adj[x].add(y); adj[y].add(x)
    g = nx_to_adj(to_graph(dict(adj)))
    if a.long_win:
        ds = lazy_rw_sdim(g, windows=[(4, 12), (8, 24), (16, 48), (30, 90)], tmax=100)
        dh = ball_growth_dim(g, windows=[(2, 6), (3, 8), (4, 10)])
    else:
        ds = lazy_rw_sdim(g); dh = ball_growth_dim(g)
    n0, n3 = len(adj), len(tets)
    E = set(); F = set()
    for t in tets:
        for e in itertools.combinations(sorted(t), 2):
            E.add(frozenset(e))
        for f in itertools.combinations(sorted(t), 3):
            F.add(frozenset(f))
    chi = n0 - len(E) + len(F) - n3
    rec = dict(kind="torus_benchmark", m=m, N0=n0, N3=n3, chi=chi, bad=c["bad"],
               sphere=c["sphere"], long=a.long_win, ds=ds, dh=dh)
    if a.log:
        with open(a.log, "a") as fh:
            fh.write(json.dumps(rec) + "\n")
    print("T^3 Kuhn m=%d: N0=%d N3=%d chi=%d bad=%d | d_s=%s | d_H=%s"
          % (m, n0, n3, chi, c["bad"], ds, dh))
