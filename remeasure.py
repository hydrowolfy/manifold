#!/usr/bin/env python3
"""Re-measure d_s / d_H on a saved causal-CDT state pickle OR an exact Kuhn T^3, with
error bars over K estimator seeds. Read-only w.r.t. states."""
import argparse, itertools, json, math, os, pickle, statistics, sys, time
from collections import defaultdict

os.environ.setdefault("MANIFOLD_REPO", os.getcwd())
sys.path[:0] = [os.getcwd(), os.path.join(os.getcwd(), "tooling")]
import cdt_causal_run as C  # noqa: E402
import __main__  # noqa: E402
__main__.Causal = C.Causal
__main__.IndexedSet = C.IndexedSet
from referee_2d_scaling import lazy_rw_sdim, ball_growth_dim, nx_to_adj  # noqa: E402
from referee_2d_topology import to_graph  # noqa: E402
from referee_3d import link_census  # noqa: E402

DH_WIN = [(2, 6), (3, 8), (4, 10)]


def adj_from_state(st):
    adj = defaultdict(set)
    for e in st.ecnt:
        a, b = tuple(e)
        adj[a].add(b); adj[b].add(a)
    return dict(adj)


def adj_from_torus(m):
    tets = set()
    for base in itertools.product(range(m), repeat=3):
        for perm in itertools.permutations(range(3)):
            cur = list(base); path = [tuple(cur)]
            for ax in perm:
                cur = list(cur); cur[ax] = (cur[ax] + 1) % m
                path.append(tuple(cur))
            tets.add(frozenset(path))
    adj = defaultdict(set)
    for t in tets:
        for x, y in itertools.combinations(t, 2):
            adj[x].add(y); adj[y].add(x)
    return dict(adj), tets


def summarize(vals):
    vals = [v for v in vals if v is not None]
    if not vals:
        return None
    m = statistics.mean(vals)
    s = statistics.stdev(vals) if len(vals) > 1 else 0.0
    return [round(m, 4), round(s, 4), len(vals)]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pkl")
    ap.add_argument("--torus", type=int)
    ap.add_argument("--seeds", type=int, default=6)
    ap.add_argument("--tmax", type=int, default=50)
    ap.add_argument("--dswin", default="4-12,8-24,16-48")
    ap.add_argument("--tag", default="")
    ap.add_argument("--log", default=None)
    ap.add_argument("--census", action="store_true")
    ap.add_argument("--seedbase", type=int, default=100)
    a = ap.parse_args()
    t0 = time.time()
    ds_win = [tuple(int(x) for x in w.split("-")) for w in a.dswin.split(",")]
    meta = {}; census_tets = None
    if a.pkl:
        with open(a.pkl, "rb") as fh:
            blob = pickle.load(fh)
        st = blob["st"]
        adj = adj_from_state(st)
        from collections import Counter as _C
        _pf = _C()
        for _f in st.stris:
            _pf[st.time[next(iter(_f))]] += 1
        _prof = [_pf.get(_t, 0) for _t in range(st.T)]
        _mean = sum(_prof)/max(1,len(_prof))
        _cv = (statistics.pstdev(_prof)/_mean) if _mean else 0.0
        meta = dict(N0=st.N0, N3=st.N3, T=st.T, f22=round(st.nk[2] / max(1, st.N3), 4),
                    k3=round(blob.get("k3", float("nan")), 4), done=blob.get("done"),
                    prof_min=min(_prof), prof_max=max(_prof), prof_cv=round(_cv,3))
        if a.census:
            census_tets = list(st.tets)
    elif a.torus is not None:
        adj, tets = adj_from_torus(a.torus)
        meta = dict(N0=len(adj), N3=len(tets), m=a.torus)
        if a.census:
            census_tets = list(tets)
    else:
        raise SystemExit("need --pkl or --torus")
    g = nx_to_adj(to_graph(adj))
    _deg = [len(v) for v in adj.values()]
    if _deg:
        meta['deg_mean'] = round(sum(_deg)/len(_deg), 2)
        meta['deg_max'] = max(_deg)
    ds_runs = {("%d-%d" % w): [] for w in ds_win}
    dh_runs = {("%d-%d" % w): [] for w in DH_WIN}
    for k in range(a.seeds):
        ds = lazy_rw_sdim(g, windows=ds_win, tmax=a.tmax, seed=a.seedbase + k)
        dh = ball_growth_dim(g, windows=DH_WIN, seed=a.seedbase + 500 + k)
        for key in ds_runs:
            ds_runs[key].append(ds.get(key))
        for key in dh_runs:
            dh_runs[key].append(dh.get(key))
    rec = dict(kind="remeasure", tag=a.tag, seeds=a.seeds, tmax=a.tmax,
               wall=round(time.time() - t0, 1),
               ds={k: summarize(v) for k, v in ds_runs.items()},
               dh={k: summarize(v) for k, v in dh_runs.items()}, **meta)
    if census_tets is not None:
        c = link_census(census_tets)
        rec["census_bad"] = c["bad"]; rec["census_n"] = c["n"]
    if a.log:
        with open(a.log, "a") as fh:
            fh.write(json.dumps(rec) + "\n")
    ds_s = " ".join("%s=%.3f+-%.3f" % (k, v[0], v[1]) for k, v in rec["ds"].items() if v)
    dh_s = " ".join("%s=%.3f+-%.3f" % (k, v[0], v[1]) for k, v in rec["dh"].items() if v)
    print("[%s] N0=%s N3=%s f22=%s | d_s %s | d_H %s | %.1fs" %
          (a.tag, meta.get("N0"), meta.get("N3"), meta.get("f22"), ds_s, dh_s, rec["wall"]))


if __name__ == "__main__":
    main()
