#!/usr/bin/env python3
"""referee_2d_scaling.py -- independent-holdout dimension estimators + null-model panel
for the project's frame-free 2D candidate (s1_22 `_sandwich`).

The point of this script is SEPARATION OF OPTIMIZATION FROM VALIDATION. The project's native
d_s/d_H estimators are reported for reference, but the load-bearing numbers here are two
estimators that are NOT part of the objective and are implemented independently of the
project's code:

  * ball-growth dimension: slope of log(cumulative ball volume) vs log(radius), fit over
    several explicit radius windows, averaged over BFS sources.
  * lazy random-walk spectral dimension: d_s = -2 d log P(t) / d log t for the lazy walk
    P = (I + D^-1 A)/2, with P(t) the mean return probability estimated by a Hutchinson
    trace probe, fit over several explicit time windows.

Every graph is compared at matched N against a null/control panel:
  grid, triangulated disk, degree-preserving rewire of the candidate, tree+loops, random
  regular, preferential attachment (Barabasi-Albert), random geometric graph.

Run (from the emergence/ project root):
    PYTHONPATH=. python3 tooling/referee_2d_scaling.py --sizes 100 150 200 256 --seeds 4 \
        --steps-per-n 120 --out tooling/artifacts/scaling_<tag>.json
"""
import argparse
import json
import math
import os
import random
import statistics
import sys
import time
from collections import Counter, defaultdict, deque

_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.dirname(_HERE)
if _ROOT not in sys.path:
    sys.path.insert(0, _ROOT)
if _HERE not in sys.path:           # allow sibling imports whether run as script or module
    sys.path.insert(0, _HERE)

import networkx as nx
from referee_2d_topology import (candidate_adj, rect_grid_adj, rect_tri_grid_adj, to_graph,
                                  REGIME)
from sec01_raw_wolfram_hypergraph_facts.s1_6_manifold_modification import _d_s, _d_H
from sec01_raw_wolfram_hypergraph_facts.s1_20_triple_objective import _E_glue_per_edge
from sec01_raw_wolfram_hypergraph_facts.s1_18_gauge_flux_sectors import _flux_deficit
from sec01_raw_wolfram_hypergraph_facts.s1_19_deficit_selection import _face_degree_hist
from sec01_raw_wolfram_hypergraph_facts.s1_21_annealing_dynamics import _closed_link_frac

BALL_WINDOWS = [(1, 4), (2, 6), (3, 8)]
LAZY_WINDOWS = [(4, 12), (8, 24), (12, 36)]


# ------------------------------------------------------------------- graph plumbing
def nx_to_adj(G):
    G = nx.convert_node_labels_to_integers(G)
    return {i: set(G.neighbors(i)) for i in G.nodes()}


def n_and_m(adj):
    n = len(adj)
    m = sum(len(adj[u]) for u in adj) // 2
    return n, m


def _bfs_dist(adj, s):
    dist = {s: 0}
    q = deque([s])
    while q:
        u = q.popleft()
        for v in adj[u]:
            if v not in dist:
                dist[v] = dist[u] + 1
                q.append(v)
    return dist


def _slope(xs, ys):
    n = len(xs)
    if n < 2:
        return float("nan")
    mx = sum(xs) / n
    my = sum(ys) / n
    den = sum((x - mx) ** 2 for x in xs)
    if den == 0:
        return float("nan")
    return sum((xs[i] - mx) * (ys[i] - my) for i in range(n)) / den


# ------------------------------------------------------------------- HOLDOUT estimators
def ball_growth_dim(adj, windows=BALL_WINDOWS, nsrc=14, seed=1):
    """Raw slope of log(cumulative ball size) vs log(radius), averaged over sources."""
    rng = random.Random(seed)
    nodes = list(adj.keys())
    accum = defaultdict(float)
    cnt = defaultdict(int)
    for _ in range(nsrc):
        s = rng.choice(nodes)
        dist = _bfs_dist(adj, s)
        shell = Counter(dist.values())
        rmax = max(dist.values())
        cum = 0
        for r in range(0, rmax + 1):
            cum += shell.get(r, 0)
            accum[r] += cum
            cnt[r] += 1
    res = {}
    for (lo, hi) in windows:
        xs, ys = [], []
        for r in range(lo, hi + 1):
            if cnt.get(r, 0) == 0:
                continue
            xs.append(math.log(r))
            ys.append(math.log(accum[r] / cnt[r]))
        res["%d-%d" % (lo, hi)] = round(_slope(xs, ys), 4) if len(xs) >= 2 else None
    return res


def lazy_rw_sdim(adj, windows=LAZY_WINDOWS, nz=6, tmax=40, seed=2):
    """Spectral dimension from lazy random-walk return probability P(t) = trace(P^t)/N,
    P = (I + D^-1 A)/2, estimated by Hutchinson trace probe. d_s = -2 dlogP/dlogt."""
    rng = random.Random(seed)
    nodes = list(adj.keys())
    idx = {u: i for i, u in enumerate(nodes)}
    N = len(nodes)
    nbr = [[idx[v] for v in adj[u]] for u in nodes]
    deg = [len(nbr[i]) for i in range(N)]
    P = {t: 0.0 for t in range(1, tmax + 1)}
    for _ in range(nz):
        z = [1.0 if rng.random() < 0.5 else -1.0 for _ in range(N)]
        w = z[:]
        for t in range(1, tmax + 1):
            nw = [0.0] * N
            for i in range(N):
                if deg[i] == 0:
                    nw[i] = w[i]
                    continue
                s = 0.0
                for j in nbr[i]:
                    s += w[j]
                nw[i] = 0.5 * (w[i] + s / deg[i])
            w = nw
            P[t] += sum(z[i] * w[i] for i in range(N)) / N
    for t in P:
        P[t] /= nz
    res = {}
    for (lo, hi) in windows:
        xs, ys = [], []
        for t in range(lo, hi + 1):
            if P.get(t, 0) > 0:
                xs.append(math.log(t))
                ys.append(math.log(P[t]))
        res["%d-%d" % (lo, hi)] = round(-2 * _slope(xs, ys), 4) if len(xs) >= 2 else None
    return res


# ------------------------------------------------------------------- null / control panel
def rewire(adj, seed=0):
    G = to_graph(adj)
    G = nx.convert_node_labels_to_integers(G)
    m = G.number_of_edges()
    try:
        nx.double_edge_swap(G, nswap=10 * m, max_tries=200 * m, seed=seed)
    except Exception:
        pass
    return {i: set(G.neighbors(i)) for i in G.nodes()}


def tree_loops(n, seed=0, extra=None):
    rng = random.Random(seed)
    G = nx.random_labeled_tree(n, seed=seed)
    if extra is None:
        extra = max(1, n // 20)
    nodes = list(G.nodes())
    added = 0
    tries = 0
    while added < extra and tries < extra * 50:
        a, b = rng.choice(nodes), rng.choice(nodes)
        tries += 1
        if a != b and not G.has_edge(a, b):
            G.add_edge(a, b)
            added += 1
    return nx_to_adj(G)


def random_regular(n, seed=0, d=3):
    if (n * d) % 2 != 0:
        d = 4
    try:
        G = nx.random_regular_graph(d, n, seed=seed)
    except Exception:
        G = nx.random_regular_graph(4, n + (n % 2), seed=seed)
    return nx_to_adj(G)


def pref_attach(n, seed=0, m=2):
    G = nx.barabasi_albert_graph(n, m, seed=seed)
    return nx_to_adj(G)


def random_geometric(n, seed=0, target_deg=3.3):
    radius = math.sqrt(target_deg / (math.pi * n))
    G = nx.random_geometric_graph(n, radius, seed=seed)
    # keep largest connected component, then pad label space
    if not nx.is_connected(G):
        comp = max(nx.connected_components(G), key=len)
        G = G.subgraph(comp).copy()
    return nx_to_adj(G)


# ------------------------------------------------------------------- per-graph measurement
def measure(adj, seed=7, proxy=False):
    n, m = n_and_m(adj)
    G = to_graph(adj)
    connected = nx.is_connected(G)
    if not connected:
        comp = max(nx.connected_components(G), key=len)
        adj = {u: set(v for v in adj[u] if v in comp) for u in comp}
        adj = nx_to_adj(to_graph(adj))
        n, m = n_and_m(adj)
        G = to_graph(adj)
    out = dict(N=n, M=m, avg_degree=round(2.0 * m / max(n, 1), 3),
               connected=connected,
               d_s_native=round(_d_s(adj), 4), d_H_native=round(_d_H(adj), 4),
               ball=ball_growth_dim(adj, seed=seed),
               lazy=lazy_rw_sdim(adj, seed=seed),
               bridges=len(list(nx.bridges(G))),
               articulation_points=len(list(nx.articulation_points(G))))
    out["bridge_frac"] = round(out["bridges"] / max(m, 1), 4)
    out["articulation_frac"] = round(out["articulation_points"] / max(n, 1), 4)
    if proxy:
        eg, ne = _E_glue_per_edge(adj)
        _, _, _, deficit = _flux_deficit(adj, maxlen=4)
        fd = _face_degree_hist(adj)
        out["proxy_Eglue_per_edge"] = round(eg, 4)
        out["proxy_deficit"] = deficit
        out["proxy_fd2_pct"] = round(fd[2], 3)
        out["proxy_closed_link"] = round(_closed_link_frac(adj), 4)
    return out


# ------------------------------------------------------------------- aggregation
def _agg_window(rows, key):
    out = {}
    wins = rows[0][key].keys()
    for w in wins:
        vals = [r[key][w] for r in rows if r[key].get(w) is not None]
        if vals:
            out[w] = dict(mean=round(statistics.mean(vals), 4),
                          min=round(min(vals), 4), max=round(max(vals), 4))
    return out


def aggregate(rows):
    agg = {}
    scalar_keys = [k for k in rows[0] if isinstance(rows[0][k], (int, float))]
    for k in scalar_keys:
        vals = [r[k] for r in rows if isinstance(r.get(k), (int, float))]
        agg[k] = dict(mean=round(statistics.mean(vals), 4), min=round(min(vals), 4),
                      max=round(max(vals), 4),
                      stdev=round(statistics.pstdev(vals), 4) if len(vals) > 1 else 0.0)
    agg["ball"] = _agg_window(rows, "ball")
    agg["lazy"] = _agg_window(rows, "lazy")
    agg["n_seeds"] = len(rows)
    return agg


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--sizes", type=int, nargs="+", default=[100, 150, 200])
    ap.add_argument("--seeds", type=int, default=4)
    ap.add_argument("--seed-start", type=int, default=0)
    ap.add_argument("--steps-per-n", type=int, default=120)
    ap.add_argument("--out", type=str, default=None)
    ap.add_argument("--nulls", action="store_true", help="include full null panel (1 instance/size)")
    args = ap.parse_args()

    t0 = time.time()
    result = dict(meta=dict(kind="scaling", regime=REGIME, sizes=args.sizes, seeds=args.seeds,
                            seed_start=args.seed_start, steps_per_n=args.steps_per_n,
                            ball_windows=BALL_WINDOWS, lazy_windows=LAZY_WINDOWS,
                            timestamp=time.strftime("%Y-%m-%dT%H:%M:%S"),
                            networkx=nx.__version__),
                  candidate={}, controls={})
    null_builders = dict(grid=lambda n, s: rect_grid_adj(n)[0],
                         tri_disk=lambda n, s: rect_tri_grid_adj(n)[0])
    if args.nulls:
        null_builders.update(
            rewire=lambda n, s: rewire(candidate_adj(n, s, args.steps_per_n), seed=s),
            tree_loops=lambda n, s: tree_loops(n, s),
            random_regular=lambda n, s: random_regular(n, s),
            pref_attach=lambda n, s: pref_attach(n, s),
            random_geometric=lambda n, s: random_geometric(n, s))

    def flush():
        if args.out:
            result["meta"]["elapsed_sec"] = round(time.time() - t0, 1)
            os.makedirs(os.path.dirname(args.out), exist_ok=True)
            with open(args.out, "w") as fh:
                json.dump(result, fh, indent=2)

    for n in args.sizes:
        for name, build in null_builders.items():
            crows = []
            nseed = args.seeds if name in ("grid", "tri_disk") else 1
            for s in range(nseed):
                cadj = build(n, s)
                cr = measure(cadj, seed=100 + s, proxy=(name in ("grid", "tri_disk")))
                cr["seed"] = s
                crows.append(cr)
            result["controls"].setdefault(name, {})["N=%d" % n] = dict(
                per_seed=crows, agg=aggregate(crows))
            flush()
            print("  [ctrl %-16s N=%d] dS_nat=%.3f ball(3-8)=%s lazy(8-24)=%s brg=%s"
                  % (name, n, crows[0]["d_s_native"], crows[0]["ball"].get("3-8"),
                     crows[0]["lazy"].get("8-24"), crows[0]["bridges"]), flush=True)
        rows = []
        for s in range(args.seed_start, args.seed_start + args.seeds):
            adj = candidate_adj(n, s, args.steps_per_n)
            r = measure(adj, seed=100 + s, proxy=True)
            r["seed"] = s
            rows.append(r)
            result["candidate"]["N=%d" % n] = dict(per_seed=rows, agg=aggregate(rows))
            flush()
            print("[cand N=%d s=%d] dS_nat=%.3f dH_nat=%.3f ball(3-8)=%s lazy(8-24)=%s "
                  "brg=%d art=%d t=%.1fs"
                  % (n, s, r["d_s_native"], r["d_H_native"], r["ball"].get("3-8"),
                     r["lazy"].get("8-24"), r["bridges"], r["articulation_points"],
                     time.time() - t0), flush=True)

    result["meta"]["elapsed_sec"] = round(time.time() - t0, 1)
    if args.out:
        flush()
        print("wrote", args.out)
    else:
        print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
