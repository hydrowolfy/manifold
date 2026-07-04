#!/usr/bin/env python3
"""referee_3d.py -- independent re-adjudication of the project's 3D manifold claim.

Two things are new relative to the 2D tooling:
 1. A genuine 3-manifold LOCAL criterion: the link of an interior vertex must be a
    triangulated 2-SPHERE (boundary vertex -> 2-disk). Calibrated on a Freudenthal (Kuhn)
    triangulation of a grid, whose interior links are provably 2-spheres. Note the cubic
    lattice itself FAILS the flag version of this test (an interior vertex's 6 neighbors have
    no edges among them), which is exactly the minor-universality obstruction (s1_15): there
    is no planarity-style graph criterion for d=3, so a "cubic-grade" graph cannot be certified
    a 3-manifold by links -- the cube can't be either.
 2. Because of (1), the cubic-target candidate is judged by SCALING and INTERIOR-FILL holdouts
    (dimension-agnostic), matched to the cube's own finite-size line, not to the ideal value 3.

Run: PYTHONPATH=. python3 tooling/referee_3d.py --selftest
     PYTHONPATH=. python3 tooling/referee_3d.py --sizes 64 125 216 --steps-per-n 40
"""
import argparse, itertools, os, sys, statistics
from collections import Counter, defaultdict, deque
_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, _ROOT); sys.path.insert(0, os.path.join(_ROOT, "tooling"))
import networkx as nx
from referee_2d_scaling import ball_growth_dim, lazy_rw_sdim, nx_to_adj
from referee_2d_topology import to_graph
from sec01_raw_wolfram_hypergraph_facts.s1_23_dim3_sandwich import _sandwich_k, _lat3


# ---------------------------------------------------------------- triangulated-3mfld control
def freudenthal(m):
    tets = []
    for i in range(m - 1):
        for j in range(m - 1):
            for k in range(m - 1):
                base = (i, j, k)
                for perm in itertools.permutations(range(3)):
                    cur = list(base); path = [base]
                    for ax in perm:
                        cur = list(cur); cur[ax] += 1; path.append(tuple(cur))
                    tets.append(frozenset(path))
    adj = defaultdict(set)
    for t in tets:
        for a, b in itertools.combinations(t, 2):
            adj[a].add(b); adj[b].add(a)
    return tets, {v: set(adj[v]) for v in adj}


def link_type(v, tets_with_v):
    tris = [frozenset(t - {v}) for t in tets_with_v]
    edge_ct = Counter(); lverts = set()
    for tri in tris:
        lverts.update(tri)
        for e in itertools.combinations(sorted(tri), 2):
            edge_ct[frozenset(e)] += 1
    F, E, V = len(tris), len(edge_ct), len(lverts)
    chi = V - E + F
    closed = all(c == 2 for c in edge_ct.values())
    disk = all(c in (1, 2) for c in edge_ct.values()) and any(c == 1 for c in edge_ct.values())
    g = defaultdict(set)
    for e in edge_ct:
        a, b = tuple(e); g[a].add(b); g[b].add(a)
    conn = False
    if lverts:
        s = next(iter(lverts)); seen = {s}; st = [s]
        while st:
            x = st.pop()
            for y in g[x]:
                if y not in seen:
                    seen.add(y); st.append(y)
        conn = len(seen) == V
    if conn and closed and chi == 2:
        return "sphere"
    if conn and disk and chi == 1:
        return "disk"
    return "bad"


def link_census(tets):
    by_v = defaultdict(list)
    for t in tets:
        for v in t:
            by_v[v].append(t)
    c = Counter(link_type(v, by_v[v]) for v in by_v)
    n = sum(c.values())
    return dict(sphere=c.get("sphere", 0), disk=c.get("disk", 0), bad=c.get("bad", 0),
               n=n, good_frac=round((c.get("sphere", 0) + c.get("disk", 0)) / max(n, 1), 4))


# ---------------------------------------------------------------- graph measures
def flag_link_fails(adj, sample=40, seed=0):
    """fraction of sampled high-degree vertices whose neighbours induce a NON-2-sphere flag
    link (few/no edges among neighbours). ~1.0 means 'not a flag 3-manifold' (like the cube)."""
    import random
    rng = random.Random(seed)
    verts = [v for v in adj if len(adj[v]) >= 4]
    if not verts:
        return None
    rng.shuffle(verts); verts = verts[:sample]
    bad = 0
    for v in verts:
        nb = list(adj[v]); m = len(nb)
        e = sum(1 for i in range(m) for j in range(i + 1, m) if nb[j] in adj[nb[i]])
        # a triangulated 2-sphere on m verts has 3m-6 edges; require at least a closed surface's worth
        if e < 3 * m - 6:
            bad += 1
    return round(bad / len(verts), 3)


def ball2_bulk_fraction(adj, target):
    """fraction of vertices whose 2-ball volume >= target (the cube's interior |B2|=25)."""
    n = len(adj); hit = 0
    for s in adj:
        seen = {s}; q = deque([(s, 0)])
        while q:
            u, d = q.popleft()
            if d == 2:
                continue
            for w in adj[u]:
                if w not in seen:
                    seen.add(w); q.append((w, d + 1))
        if len(seen) >= target:
            hit += 1
    return round(hit / max(n, 1), 4)


def graph_defects(adj):
    G = to_graph(adj)
    n, m = G.number_of_nodes(), G.number_of_edges()
    conn = nx.is_connected(G)
    br = len(list(nx.bridges(G))) if conn else None
    ar = len(list(nx.articulation_points(G))) if conn else None
    return dict(N=n, M=m, avg_deg=round(2*m/n, 2),
                bridge_frac=round(br/m, 4) if br is not None else None,
                artic_frac=round(ar/n, 4) if ar is not None else None)


def candidate(n, seed=11, steps_per_n=40):
    a, *_ = _sandwich_k(n, 3.0, 4, 1.0, 3.0, n*steps_per_n, seed=seed,
                        T_hi=2.0, T_lo=0.2, w_iso=2.0, cceil=2.8)
    return {u: set(a[u]) for u in a}


def scaling(adj, seed=7):
    a = nx_to_adj(to_graph(adj))
    return dict(ball=ball_growth_dim(a, seed=seed), lazy=lazy_rw_sdim(a, seed=seed))


def selftest():
    print("=== 3D self-test: calibrate the vertex-link 2-sphere criterion ===")
    tets, adj = freudenthal(4)
    c = link_census(tets)
    print("Freudenthal 4^3:", c, "(interior links must be spheres, boundary disks, bad=0)")
    assert c["bad"] == 0 and c["sphere"] > 0, "link criterion miscalibrated"
    tets5, _ = freudenthal(5)
    c5 = link_census(tets5)
    print("Freudenthal 5^3:", c5)
    assert c5["bad"] == 0
    cube = _lat3(5)
    print("cube 5^3 flag-link fail fraction:", flag_link_fails(cube),
          "(≈1.0 expected: cube is NOT a flag 3-manifold — minor-universality)")
    print("ALL 3D SELF-TESTS PASSED")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--sizes", type=int, nargs="+", default=[64, 125, 216])
    ap.add_argument("--seeds", type=int, default=2)
    ap.add_argument("--steps-per-n", type=int, default=40)
    a = ap.parse_args()
    if a.selftest:
        selftest(); return
    print("N is matched to cube sizes k^3. Candidate = _sandwich_k(alpha=3,k=4). Independent holdouts.")
    print("%-10s %-26s %-26s" % ("N (k^3)", "CANDIDATE", "CUBE _lat3"))
    for N in a.sizes:
        k = round(N ** (1/3));  cube = _lat3(k); Ncube = len(cube)
        cd = graph_defects(cube); cs = scaling(cube); cbulk = ball2_bulk_fraction(cube, 25)
        # candidate, multi-seed means on the key holdouts
        rows = []
        for s in range(11, 11 + a.seeds):
            adj = candidate(N, seed=s, steps_per_n=a.steps_per_n)
            d = graph_defects(adj); sc = scaling(adj)
            rows.append((d, sc, ball2_bulk_fraction(adj, 25)))
        def cm(f): return round(statistics.mean([f(r) for r in rows]), 4)
        print("N=%-8d cand: dH(3-8)=%s dS(8-24)=%s brgF=%.3f artF=%.3f bulk=%.2f | cube: dH=%s dS=%s brgF=%.3f artF=%.3f bulk=%.2f"
              % (N,
                 cm(lambda r: r[1]["ball"].get("3-8")), cm(lambda r: r[1]["lazy"].get("8-24")),
                 cm(lambda r: r[0]["bridge_frac"]), cm(lambda r: r[0]["artic_frac"]), cm(lambda r: r[2]),
                 cs["ball"].get("3-8"), cs["lazy"].get("8-24"),
                 cd["bridge_frac"], cd["artic_frac"], cbulk))


if __name__ == "__main__":
    main()
