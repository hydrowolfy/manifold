#!/usr/bin/env python3
"""cdt_experiment.py -- v0 of the CDT-direction experiment: can an action move the geometry of a
certified 3-manifold toward d_s=3 while KEEPING it a manifold?

Fixed vertex count N0. Metropolis chain of 2-3 / 3-2 Pachner flips (which change the tet count
N3 but not N0), weighted by a Regge-type term exp(-k3 * dN3): small k3 -> denser (crumpled),
large k3 -> thinner. Every accepted state is still a closed triangulated 3-manifold; we assert
it (link census bad==0) and sweep k3 to see where d_s is closest to 3. This is Euclidean DT at
fixed volume; full CDT additionally imposes a causal/foliated restriction (next version).

Run: PYTHONPATH=. python3 tooling/cdt_experiment.py --selftest
     PYTHONPATH=. python3 tooling/cdt_experiment.py --n0 80 --sweeps 4000
"""
import argparse, itertools, math, os, random, sys
from collections import defaultdict
_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, _ROOT); sys.path.insert(0, os.path.join(_ROOT, "tooling"))
from construct_3manifold import build, move_2_3
from referee_3d import link_census
from referee_2d_scaling import lazy_rw_sdim, ball_growth_dim, nx_to_adj
from referee_2d_topology import to_graph


def move_3_2(tets, rng):
    edge_to = defaultdict(list)
    for t in tets:
        for e in itertools.combinations(sorted(t), 2):
            edge_to[frozenset(e)].append(t)
    cands = [(e, ts) for e, ts in edge_to.items() if len(ts) == 3]
    rng.shuffle(cands)
    existing = tets
    for e, ts in cands:
        d, ee = tuple(e)
        apex = set()
        for t in ts:
            apex |= (t - {d, ee})
        if len(apex) != 3:
            continue
        a, b, c = tuple(apex)
        need = {frozenset((x, y, d, ee)) for x, y in itertools.combinations((a, b, c), 2)}
        if set(ts) != need:
            continue
        n1 = frozenset((a, b, c, d)); n2 = frozenset((a, b, c, ee))
        if n1 in existing or n2 in existing:
            continue
        # triangle abc must not already be a face elsewhere, else it would land in >2 tets
        if any(a in t and b in t and c in t for t in tets):
            continue
        for t in ts:
            tets.discard(t)
        tets.add(n1); tets.add(n2)
        return True
    return False


def adj_of(tets):
    a = defaultdict(set)
    for t in tets:
        for x, y in itertools.combinations(t, 2):
            a[x].add(y); a[y].add(x)
    return {v: set(a[v]) for v in a}


def run_chain(n0, k3, sweeps, seed=0):
    rng = random.Random(seed)
    tets, _ = build(n0, seed=seed)
    N3 = len(tets)
    for _ in range(sweeps):
        if rng.random() < 0.5:
            # propose 2-3 (dN3 = +1); weight exp(-k3*(+1))
            if rng.random() < math.exp(-k3):
                move_2_3(tets, rng)
        else:
            # propose 3-2 (dN3 = -1); weight exp(-k3*(-1)) = exp(+k3), cap at 1
            if rng.random() < min(1.0, math.exp(k3)):
                move_3_2(tets, rng)
    return tets, adj_of(tets)


def measure(tets, adj):
    c = link_census(tets)
    a = nx_to_adj(to_graph(adj))
    ds = lazy_rw_sdim(a).get("4-12")
    dH = ball_growth_dim(a).get("2-6")
    return c, ds, dH


def selftest():
    print("=== CDT v0: 3-2 inverse move + manifold-preserving chain ===")
    tets, adj = build(40, seed=0)
    c0 = link_census(tets)
    assert c0["bad"] == 0
    print("seed manifold: N=%d tets=%d links sphere=%d bad=%d" % (len(adj), len(tets), c0["sphere"], c0["bad"]))
    # round-trip: a 2-3 then a 3-2 keeps it a manifold
    r = random.Random(1)
    ok23 = move_2_3(tets, r); ok32 = move_3_2(tets, r)
    c1 = link_census(tets)
    print("after 2-3(%s)+3-2(%s): tets=%d links bad=%d" % (ok23, ok32, len(tets), c1["bad"]))
    assert c1["bad"] == 0, "3-2 move broke the manifold -- bug"
    # short chain must stay a manifold
    tets, adj = run_chain(40, k3=0.0, sweeps=300, seed=2)
    c2 = link_census(tets)
    print("after 300-sweep chain (k3=0): N=%d tets=%d links sphere=%d bad=%d" % (len(adj), len(tets), c2["sphere"], c2["bad"]))
    assert c2["bad"] == 0, "chain broke the manifold -- bug"
    print("PASS: 3-2 move + chain preserve the 3-manifold (0 bad links throughout).")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--n0", type=int, default=80)
    ap.add_argument("--sweeps", type=int, default=3000)
    ap.add_argument("--k3s", type=float, nargs="+", default=[-0.4, 0.0, 0.4, 0.8])
    a = ap.parse_args()
    if a.selftest:
        selftest(); return
    print("Euclidean DT at fixed N0=%d, %d sweeps. Sweep k3; report tets, d_s, d_H, manifold-ok." % (a.n0, a.sweeps))
    best = None
    for k3 in a.k3s:
        tets, adj = run_chain(a.n0, k3, a.sweeps, seed=0)
        c, ds, dH = measure(tets, adj)
        ok = c["bad"] == 0
        f = lambda x: ("%.2f" % x) if isinstance(x, (int, float)) else "n/a"
        print("  k3=%+.2f -> tets=%4d avgdeg=%.1f | manifold_ok=%s | d_s(4-12)=%s d_H(2-6)=%s"
              % (k3, len(tets), 2*sum(len(adj[v]) for v in adj)/len(adj)/2*2/1, ok, f(ds), f(dH)))
        if isinstance(ds, (int, float)) and (best is None or abs(ds-3) < best[1]):
            best = (k3, abs(ds-3), ds)
    if best:
        print("closest d_s to 3: k3=%+.2f (d_s=%.2f). Reminder: Euclidean DT; causal slicing is the next lever." % (best[0], best[2]))


if __name__ == "__main__":
    main()
