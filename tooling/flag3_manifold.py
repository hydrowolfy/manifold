#!/usr/bin/env python3
"""flag3_manifold.py -- frame-free FLAG 3-manifold generator (Lutz-Nevo stellar moves).

The complex IS the clique complex of the graph G, so everything is graph-only (frame-free by
construction; the manifold lives in the graph, per the E5 consult). Certification: for every
vertex v, the induced neighborhood graph G[N(v)] must be K4-free and its clique complex a
triangulated 2-SPHERE (that is the flag-3-manifold link condition).

Move: Lutz-Nevo edge subdivision (stellar). Subdivide edge {u,v}: remove uv, add w adjacent to
u, v and every common neighbor of u,v. Inverse is the reverse. Moves that break certification
are rejected, so the object stays a certified flag 3-manifold throughout.

Seed: the 16-cell = K_{2,2,2,2}, the minimal flag 3-sphere.

Empty-square flag-no-square (fns) option: reject any move that creates an induced 4-cycle with
no diagonal (an "empty square"). fns is the maximal local-curvature condition and the proposed
route to decrumpling (see redteam/DIRECTION_DECISION.md).
"""
import argparse, itertools, os, random, sys
from collections import defaultdict
_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, _ROOT); sys.path.insert(0, os.path.join(_ROOT, "tooling"))


def cell16():
    part = lambda x: x // 2
    G = {i: set() for i in range(8)}
    for i in range(8):
        for j in range(8):
            if i != j and part(i) != part(j):
                G[i].add(j)
    return G


def _induced(G, S):
    Ss = set(S)
    return {x: (G[x] & Ss) for x in Ss}


def link_is_flag_2sphere(G, v):
    H = _induced(G, G[v])
    verts = list(H)
    if len(verts) < 3:
        return False
    elist = [(a, b) for a in verts for b in H[a] if a < b]
    Ec = len(elist)
    tris = []
    for (a, b) in elist:
        for c in (H[a] & H[b]):
            if c > b:
                tris.append((a, b, c))
    Fc = len(tris)
    # K4-free (link must be 2-dimensional: no 4-clique in the neighborhood)
    for (a, b, c) in tris:
        if H[a] & H[b] & H[c]:
            return False
    # every edge in exactly 2 triangles (closed surface)
    et = defaultdict(int)
    for (a, b, c) in tris:
        et[(a, b)] += 1; et[(a, c)] += 1; et[(b, c)] += 1
    if len(et) != Ec or any(cnt != 2 for cnt in et.values()):
        return False
    # connected
    adjL = defaultdict(set)
    for (a, b) in elist:
        adjL[a].add(b); adjL[b].add(a)
    seen = {verts[0]}; st = [verts[0]]
    while st:
        x = st.pop()
        for y in adjL[x]:
            if y not in seen:
                seen.add(y); st.append(y)
    if len(seen) != len(verts):
        return False
    return (len(verts) - Ec + Fc) == 2   # chi == 2  -> sphere


def certify(G, verts=None):
    return all(link_is_flag_2sphere(G, v) for v in (verts if verts else G))


def has_empty_square(G, focus=None):
    """True if some induced 4-cycle has no diagonal (empty square). If focus given, only check
    4-cycles through those vertices (fast incremental check)."""
    nodes = list(focus) if focus else list(G)
    for a in nodes:
        Na = G[a]
        for b in Na:
            for d in Na:
                if d <= b or d in G[b]:
                    continue  # need b,d non-adjacent (diagonal absent)
                common = (G[b] & G[d]) - {a}
                for c in common:
                    if a not in G[c] and c not in Na:  # a-c non-adjacent -> a,b,c,d induced 4-cycle, no diagonal
                        return True
    return False


def subdivide(G, u, v, nextw):
    common = G[u] & G[v]
    G[u].discard(v); G[v].discard(u)
    G[nextw] = {u, v} | set(common)
    G[u].add(nextw); G[v].add(nextw)
    for c in common:
        G[c].add(nextw)
    return {u, v, nextw} | common  # affected vertices (links changed)


def undo_subdivide(G, u, v, w, common):
    for x in G[w]:
        G[x].discard(w)
    del G[w]
    G[u].add(v); G[v].add(u)


def count_empty_squares(G):
    seen = set()
    for a in G:
        Ga = G[a]
        for b in Ga:
            for d in Ga:
                if d == b or d in G[b]:
                    continue
                for c in (G[b] & G[d]):
                    if c == a or c in Ga:
                        continue
                    if len({a, b, c, d}) == 4:
                        seen.add((min(a, c), max(a, c), min(b, d), max(b, d)))
    return len(seen)


def grow(target_n, seed=0, fns=False):
    rng = random.Random(seed)
    G = cell16(); nextw = 8
    cur_sq = count_empty_squares(G) if fns else 0
    tries = 0
    while len(G) < target_n and tries < target_n * 300:
        tries += 1
        u = rng.choice(list(G))
        if not G[u]:
            continue
        v = rng.choice(list(G[u]))
        common = G[u] & G[v]
        aff = subdivide(G, u, v, nextw)
        ok = certify(G, aff)
        if ok and fns:
            new_sq = count_empty_squares(G)   # energy: number of empty squares (fns == 0)
            if new_sq > cur_sq:               # accept only non-increasing-square moves
                ok = False
            else:
                cur_sq = new_sq
        if ok:
            nextw += 1
        else:
            undo_subdivide(G, u, v, nextw, common)
    return G, (cur_sq if fns else count_empty_squares(G))


def _dims(G):
    import sys as _s
    _s.path.insert(0, "tooling")
    from referee_2d_scaling import lazy_rw_sdim, ball_growth_dim, nx_to_adj
    from referee_2d_topology import to_graph
    adj = {x: set(G[x]) for x in G}
    a = nx_to_adj(to_graph(adj))
    f = lambda z: ("%.2f" % z) if isinstance(z, (int, float)) else "n/a"
    return f(lazy_rw_sdim(a).get("4-12")), f(ball_growth_dim(a).get("2-6"))


def selftest():
    G = cell16()
    print("16-cell: N=%d certifies=%s" % (len(G), certify(G)))
    assert certify(G), "seed did not certify"
    for tv in (40, 80):
        G2, sq = grow(tv, seed=1)
        assert certify(G2), "flag growth broke certification"
        ds, dH = _dims(G2)
        print("FLAG   N=%d M=%d certified emptySquares=%d | d_s=%s d_H=%s"
              % (len(G2), sum(len(G2[x]) for x in G2)//2, count_empty_squares(G2), ds, dH))
    for tv in (40, 80):
        G3, sq = grow(tv, seed=2, fns=True)
        assert certify(G3), "fns growth broke certification"
        ds, dH = _dims(G3)
        print("FNS?   N=%d M=%d certified emptySquares=%d (0=flag-no-square) | d_s=%s d_H=%s"
              % (len(G3), sum(len(G3[x]) for x in G3)//2, sq, ds, dH))
    print("Flag 3-manifold generator certified. Arm C reports how low the empty-square energy is driven and the geometry there.")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--n", type=int, default=60); ap.add_argument("--fns", action="store_true")
    ap.add_argument("--seed", type=int, default=0)
    a = ap.parse_args()
    if a.selftest:
        selftest()
    else:
        G, sq = grow(a.n, seed=a.seed, fns=a.fns)
        print("N=%d M=%d certified=%s emptySquares=%d" %
              (len(G), sum(len(G[x]) for x in G)//2, certify(G), count_empty_squares(G)))
