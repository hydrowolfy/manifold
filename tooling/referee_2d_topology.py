#!/usr/bin/env python3
"""referee_2d_topology.py -- deterministic 2-complex / manifold-topology audit for the
project's frame-free 2D candidate (the s1_22 `_sandwich` output).

This is a HOLDOUT layer. It does NOT reuse the project's short-cycle face-degree proxy as
the face set. Instead it constructs a canonical 2-complex from a planar embedding (each
BOUNDED face of the embedding is a 2-cell) and then measures the genuine topological
obligations of a 2-manifold-with-boundary:

  * edge -> face incidence   (interior edge in exactly 2 distinct 2-cells, boundary in 1)
  * vertex links             (interior link = cycle, boundary link = path/interval)
  * boundary graph           (should be a small number of simple cycles)
  * Euler characteristic     (V - E + F_bounded)
  * Betti numbers over GF(2) (b0, b1, b2 of the constructed complex)
  * orientability            (consistent orientation of the 2-cells)

plus graph-level defect densities (bridges, articulation points) that any 2-manifold must
have at zero density in the interior.

The project's fd-based proxy numbers are reported ALONGSIDE, clearly labelled `proxy_*`, so
the report can separate "optimized proxy" from "true holdout".

Run (from the emergence/ project root):
    PYTHONPATH=. python3 tooling/referee_2d_topology.py --sizes 100 150 200 --seeds 6 \
        --steps-per-n 120 --out tooling/artifacts/topology_<tag>.json

Pure-Python topology; networkx only for the planar embedding + a straight-line layout used
to identify the unbounded face.
"""
import argparse
import json
import math
import os
import statistics
import sys
import time
from collections import Counter, defaultdict

_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.dirname(_HERE)
if _ROOT not in sys.path:
    sys.path.insert(0, _ROOT)

import networkx as nx
from sec01_raw_wolfram_hypergraph_facts.s1_22_isotropy_sandwich import _sandwich, _lat2, _tri2
from sec01_raw_wolfram_hypergraph_facts.s1_19_deficit_selection import _face_degree_hist

# The referee's "feasible ceiling" regime (matches STRUCTURE.md round-62 and the report).
REGIME = dict(w_glue=1.0, w_def=3.0, w_iso=2.0, cceil=2.1, T_hi=2.0, T_lo=0.2)


# ----------------------------------------------------------------------------- generators
def candidate_adj(n, seed, steps_per_n=120, regime=REGIME):
    adj, *_ = _sandwich(n, regime["w_glue"], regime["w_def"], n * steps_per_n, seed=seed,
                        w_iso=regime["w_iso"], cceil=regime["cceil"],
                        T_hi=regime["T_hi"], T_lo=regime["T_lo"])
    return {u: set(adj[u]) for u in adj}


def _factor_near_square(n):
    a = int(round(math.sqrt(n)))
    for da in range(0, a):
        for cand in (a - da, a + da):
            if cand >= 1 and n % cand == 0:
                b = n // cand
                lo, hi = min(cand, b), max(cand, b)
                return lo, hi
    a = int(math.sqrt(n))
    return a, (n + a - 1) // a  # near-square fallback (size may exceed n slightly)


def rect_grid_adj(n):
    a, b = _factor_near_square(n)
    adj = defaultdict(set)
    for i in range(a):
        for j in range(b):
            u = i * b + j
            adj[u]
            if j + 1 < b:
                v = i * b + j + 1; adj[u].add(v); adj[v].add(u)
            if i + 1 < a:
                v = (i + 1) * b + j; adj[u].add(v); adj[v].add(u)
    return {u: set(adj[u]) for u in adj}, (a, b)


def rect_tri_grid_adj(n):
    (grid, (a, b)) = rect_grid_adj(n)
    adj = {u: set(grid[u]) for u in grid}
    for i in range(a - 1):
        for j in range(b - 1):
            u = i * b + j; v = (i + 1) * b + j + 1
            adj[u].add(v); adj[v].add(u)
    return adj, (a, b)


def to_graph(adj):
    G = nx.Graph()
    G.add_nodes_from(adj.keys())
    for u in adj:
        for v in adj[u]:
            if u < v:
                G.add_edge(u, v)
    return G


# ----------------------------------------------------------------------------- gf(2) rank
def gf2_rank(vectors):
    pivots = {}
    rank = 0
    for v in vectors:
        x = v
        while x:
            hb = x.bit_length() - 1
            if hb in pivots:
                x ^= pivots[hb]
            else:
                pivots[hb] = x
                rank += 1
                break
    return rank


# --------------------------------------------------------------------- planar face layer
def planar_faces(G):
    """Return (is_planar, faces, he2face, outer_idx). faces: list of node-lists (closed
    walks). he2face: directed half-edge -> face index. outer_idx: index of unbounded face."""
    is_planar, emb = nx.check_planarity(G)
    if not is_planar:
        return False, None, None, None
    he2face = {}
    faces = []
    visited = set()
    for u, v in emb.edges():
        if (u, v) in visited:
            continue
        f = emb.traverse_face(u, v, mark_half_edges=visited)
        fid = len(faces)
        faces.append(f)
        L = len(f)
        for i in range(L):
            he2face[(f[i], f[(i + 1) % L])] = fid
    # Identify the unbounded face: largest |signed area| in a straight-line planar layout.
    outer = None
    try:
        pos = nx.combinatorial_embedding_to_pos(emb)
        best = -1.0
        for fid, f in enumerate(faces):
            s = 0.0
            for i in range(len(f)):
                x1, y1 = pos[f[i]]
                x2, y2 = pos[f[(i + 1) % len(f)]]
                s += x1 * y2 - x2 * y1
            if abs(s) > best:
                best = abs(s)
                outer = fid
    except Exception:
        outer = max(range(len(faces)), key=lambda i: len(faces[i]))
    return True, faces, he2face, outer


def edge_incidence(G, faces, he2face, outer):
    interior = boundary = zero_bounded = double_in_face = 0
    boundary_edges = []
    for u, v in G.edges():
        f1 = he2face.get((u, v))
        f2 = he2face.get((v, u))
        if f1 == f2:
            if f1 == outer:
                zero_bounded += 1
            else:
                double_in_face += 1
            continue
        b1 = f1 is not None and f1 != outer
        b2 = f2 is not None and f2 != outer
        if b1 and b2:
            interior += 1
        else:
            boundary += 1
            boundary_edges.append((u, v))
    E = G.number_of_edges()
    return dict(
        interior_edges=interior, boundary_edges=boundary,
        zero_bounded_edges=zero_bounded, double_in_face_edges=double_in_face,
        bad_incidence_edges=zero_bounded + double_in_face,
        bad_incidence_frac=(zero_bounded + double_in_face) / max(E, 1),
    ), boundary_edges


def vertex_links(G, faces, outer):
    corners = defaultdict(list)
    for fid, f in enumerate(faces):
        if fid == outer:
            continue
        L = len(f)
        for i in range(L):
            p = f[(i - 1) % L]; v = f[i]; s = f[(i + 1) % L]
            corners[v].append((p, s))
    interior_good = boundary_good = bad = isolated = 0
    bad_ids = []
    for v in G.nodes():
        cs = corners.get(v, [])
        if not cs:
            isolated += 1
            bad += 1
            bad_ids.append(v)
            continue
        ladj = defaultdict(int)
        spur = False
        seen_pairs = Counter()
        for (p, s) in cs:
            if p == s:            # self-loop arc: degenerate spur -> non-manifold pinch
                spur = True
                continue
            key = (min(p, s), max(p, s))
            seen_pairs[key] += 1  # NOTE parallel arcs are legitimate: a degree-2 interior
            ladj[p] += 1          # vertex has a 2-gon link, a valid circle. Only self-loops,
            ladj[s] += 1          # disconnection, or wrong degrees make a link non-manifold.
        verts = list(ladj.keys())
        if not verts:
            bad += 1
            bad_ids.append(v)
            continue
        # connectivity of the link graph
        nbr = defaultdict(set)
        for (p, s) in seen_pairs:
            nbr[p].add(s); nbr[s].add(p)
        start = verts[0]
        stack = [start]; comp = {start}
        while stack:
            x = stack.pop()
            for y in nbr[x]:
                if y not in comp:
                    comp.add(y); stack.append(y)
        connected = len(comp) == len(verts)
        degs = list(ladj.values())
        ones = sum(1 for d in degs if d == 1)
        all2 = all(d == 2 for d in degs)
        if spur or not connected:
            bad += 1
            bad_ids.append(v)
        elif all2 and ones == 0:
            interior_good += 1          # link is a single cycle
        elif ones == 2 and all(d in (1, 2) for d in degs):
            boundary_good += 1          # link is a single path (interval)
        else:
            bad += 1
            bad_ids.append(v)
    V = G.number_of_nodes()
    return dict(
        interior_good_links=interior_good, boundary_good_links=boundary_good,
        bad_links=bad, isolated_links=isolated,
        good_link_frac=(interior_good + boundary_good) / max(V, 1),
        bad_link_frac=bad / max(V, 1),
        _bad_ids=bad_ids,
    )


def boundary_analysis(boundary_edges):
    badj = defaultdict(set)
    for u, v in boundary_edges:
        badj[u].add(v); badj[v].add(u)
    if not badj:
        return dict(boundary_components=0, single_simple_boundary_cycle=False,
                    non_simple_boundary=True, boundary_all_simple_cycles=False,
                    max_boundary_vertex_degree=0)
    seen = set()
    comps = 0
    all_cycles = True
    maxdeg = max(len(badj[x]) for x in badj)
    for s in badj:
        if s in seen:
            continue
        comps += 1
        stack = [s]; seen.add(s); nodes = [s]
        while stack:
            x = stack.pop()
            for y in badj[x]:
                if y not in seen:
                    seen.add(y); stack.append(y); nodes.append(y)
        if not all(len(badj[x]) == 2 for x in nodes):
            all_cycles = False
    return dict(
        boundary_components=comps,
        boundary_all_simple_cycles=all_cycles,
        single_simple_boundary_cycle=(comps == 1 and all_cycles),
        non_simple_boundary=(maxdeg != 2 or comps != 1),
        max_boundary_vertex_degree=maxdeg,
    )


def betti_and_orientability(G, faces, outer):
    edges = list(G.edges())
    eidx = {frozenset(e): i for i, e in enumerate(edges)}
    E = len(edges)
    c0 = nx.number_connected_components(G)
    rank_d1 = G.number_of_nodes() - c0
    cols = []
    edge_faces = defaultdict(list)
    n_cells = 0
    for fid, f in enumerate(faces):
        if fid == outer:
            continue
        n_cells += 1
        cnt = defaultdict(int)
        L = len(f)
        for i in range(L):
            a = f[i]; b = f[(i + 1) % L]
            e = frozenset((a, b))
            if e in eidx:
                cnt[eidx[e]] += 1
                edge_faces[e].append((fid, (a, b)))
        vec = 0
        for ei, c in cnt.items():
            if c % 2 == 1:
                vec |= (1 << ei)
        if vec:
            cols.append(vec)
    rank_d2 = gf2_rank(cols)
    b0 = c0
    b1 = (E - rank_d1) - rank_d2
    b2 = n_cells - rank_d2
    euler = G.number_of_nodes() - E + n_cells

    # orientability over the "clean" part (interior edges shared by exactly 2 distinct faces)
    parent = {}
    parity = {}

    def find(x):
        px = x
        acc = 0
        while parent.get(px, px) != px:
            acc ^= parity.get(px, 0)
            px = parent.get(px, px)
        return px, acc

    manifold_edges_ok = True
    orientable = True
    for fid in range(len(faces)):
        if fid != outer:
            parent[fid] = fid; parity[fid] = 0
    for e, lst in edge_faces.items():
        if len(lst) != 2:
            if len(lst) > 2:
                manifold_edges_ok = False
            continue
        (f1, d1), (f2, d2) = lst
        if f1 == f2:
            manifold_edges_ok = False
            continue
        want = 0 if d1 != d2 else 1   # planar traversal: opposite dirs -> same sign
        r1, p1 = find(f1)
        r2, p2 = find(f2)
        if r1 == r2:
            if (p1 ^ p2) != want:
                orientable = False
        else:
            parent[r1] = r2
            parity[r1] = p1 ^ p2 ^ want
    return dict(b0=b0, b1=b1, b2=b2, rank_d2=rank_d2, n_2cells=n_cells,
                euler_char=euler, orientable=bool(orientable and manifold_edges_ok),
                manifold_edges_ok=manifold_edges_ok)


def face_spectrum(faces, outer):
    lens = [len(f) for i, f in enumerate(faces) if i != outer]
    c = Counter(lens)
    return dict(
        n_2cells=len(lens),
        n_triangles=c.get(3, 0),
        n_quads=c.get(4, 0),
        n_pentagon_plus=sum(v for k, v in c.items() if k >= 5),
        largest_face=max(lens) if lens else 0,
        tri_frac=c.get(3, 0) / max(len(lens), 1),
        quad_frac=c.get(4, 0) / max(len(lens), 1),
    )


def analyze(adj, label):
    G = to_graph(adj)
    V = G.number_of_nodes(); E = G.number_of_edges()
    connected = nx.is_connected(G)
    fd = _face_degree_hist(adj)  # PROXY: percent of edges bordering k short faces
    out = dict(label=label, V=V, E=E, connected=connected,
               proxy_fd0_pct=round(fd[0], 3), proxy_fd2_pct=round(fd[2], 3),
               proxy_fd3_pct=round(fd[3], 3))
    # graph-level defects (any 2-manifold: zero bridges, zero interior articulation)
    artic = set(nx.articulation_points(G)) if connected else set()
    if connected:
        out["bridges"] = len(list(nx.bridges(G)))
        out["articulation_points"] = len(artic)
    else:
        out["bridges"] = None
        out["articulation_points"] = None
    out["bridge_frac"] = (out["bridges"] / max(E, 1)) if out["bridges"] is not None else None
    out["articulation_frac"] = (out["articulation_points"] / max(V, 1)) if out["articulation_points"] is not None else None

    is_planar, faces, he2face, outer = planar_faces(G)
    out["planar"] = is_planar
    if not is_planar:
        out["note"] = "non-planar: no canonical 2-cell set; face-based diagnostics skipped"
        return out
    inc, bedges = edge_incidence(G, faces, he2face, outer)
    out.update(inc)
    vl = vertex_links(G, faces, outer)
    bad_ids = set(vl.pop("_bad_ids"))
    pend = {v for v in G.nodes() if G.degree(v) <= 1}
    vl["bad_links_noncut"] = len(bad_ids - artic - pend)
    vl["bad_links_noncut_frac"] = round(len(bad_ids - artic - pend) / max(V, 1), 4)
    out.update(vl)
    out.update(boundary_analysis(bedges))
    out.update(betti_and_orientability(G, faces, outer))
    out.update(face_spectrum(faces, outer))
    return out


# ------------------------------------------------------------------------------ aggregate
def aggregate(rows):
    keys_num = [k for k in rows[0] if isinstance(rows[0][k], (int, float)) and rows[0][k] is not None
                and k not in ("V",)]
    agg = {}
    for k in keys_num:
        vals = [r[k] for r in rows if isinstance(r.get(k), (int, float))]
        if not vals:
            continue
        agg[k] = dict(mean=round(statistics.mean(vals), 4),
                      min=round(min(vals), 4), max=round(max(vals), 4),
                      stdev=round(statistics.pstdev(vals), 4) if len(vals) > 1 else 0.0)
    # discrete pass rates
    agg["single_simple_boundary_cycle_rate"] = round(
        sum(1 for r in rows if r.get("single_simple_boundary_cycle")) / len(rows), 4)
    agg["planar_rate"] = round(sum(1 for r in rows if r.get("planar")) / len(rows), 4)
    agg["orientable_rate"] = round(sum(1 for r in rows if r.get("orientable")) / len(rows), 4)
    agg["n_seeds"] = len(rows)
    return agg


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--sizes", type=int, nargs="+", default=[100, 150, 200])
    ap.add_argument("--seeds", type=int, default=6)
    ap.add_argument("--seed-start", type=int, default=0)
    ap.add_argument("--steps-per-n", type=int, default=120)
    ap.add_argument("--out", type=str, default=None)
    ap.add_argument("--controls", action="store_true", help="also audit same-N grid + tri-disk")
    args = ap.parse_args()

    t0 = time.time()
    result = dict(meta=dict(kind="topology", regime=REGIME, sizes=args.sizes,
                            seeds=args.seeds, seed_start=args.seed_start,
                            steps_per_n=args.steps_per_n,
                            timestamp=time.strftime("%Y-%m-%dT%H:%M:%S"),
                            networkx=nx.__version__),
                  candidate={}, controls={})
    def flush():
        if args.out:
            result["meta"]["elapsed_sec"] = round(time.time() - t0, 1)
            os.makedirs(os.path.dirname(args.out), exist_ok=True)
            with open(args.out, "w") as fh:
                json.dump(result, fh, indent=2)

    for n in args.sizes:
        if args.controls:
            g_adj, (ga, gb) = rect_grid_adj(n)
            t_adj, (ta, tb) = rect_tri_grid_adj(n)
            gr = analyze(g_adj, "grid %dx%d" % (ga, gb))
            tr = analyze(t_adj, "tri_disk %dx%d" % (ta, tb))
            result["controls"].setdefault("grid", {})["N=%d" % n] = gr
            result["controls"].setdefault("tri_disk", {})["N=%d" % n] = tr
            flush()
            print("[ctrl N=%d] grid %dx%d chi=%s bridges=%s badlink=%s | tri %dx%d chi=%s badlink=%s"
                  % (n, ga, gb, gr.get("euler_char"), gr.get("bridges"), gr.get("bad_links"),
                     ta, tb, tr.get("euler_char"), tr.get("bad_links")), flush=True)
        rows = []
        for s in range(args.seed_start, args.seed_start + args.seeds):
            adj = candidate_adj(n, s, args.steps_per_n)
            r = analyze(adj, "candidate N=%d seed=%d" % (n, s))
            r["seed"] = s
            rows.append(r)
            result["candidate"]["N=%d" % n] = dict(per_seed=rows, agg=aggregate(rows))
            flush()
            print("[cand N=%d s=%d] planar=%s V=%d E=%d bridges=%s artic=%s badlink=%s "
                  "chi=%s b1=%s tri=%s quad=%s simpleBdy=%s t=%.1fs"
                  % (n, s, r.get("planar"), r["V"], r["E"], r.get("bridges"),
                     r.get("articulation_points"), r.get("bad_links"), r.get("euler_char"),
                     r.get("b1"), r.get("n_triangles"), r.get("n_quads"),
                     r.get("single_simple_boundary_cycle"), time.time() - t0), flush=True)

    result["meta"]["elapsed_sec"] = round(time.time() - t0, 1)
    if args.out:
        flush()
        print("wrote", args.out)
    else:
        print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
