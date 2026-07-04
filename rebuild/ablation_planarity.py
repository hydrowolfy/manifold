#!/usr/bin/env python3
"""Minimal-reconstruction ablation for a 2D discrete manifold.

Thesis: the minimum construction step that reaches a 2D-manifold-grade object is the
frame-free GLOBAL PLANARITY CONSTRAINT (s1_14 `_mcmc_planar`). The later arc
(s1_16..s1_22: growth cap, deficit selection, triple objective, isotropy sandwich) is
ablatable — it does not improve, and in fact regresses, the manifold holdouts.

This script runs three constructions through the same calibrated validation harness and
reports the holdouts that decide manifoldness (bridges, articulation, boundary, spectral
dimension vs a matched grid):
  - PLANAR (step present)   : s1_14 _mcmc_planar         -> expect manifold-grade
  - EULER-GATE (step altered): s1_14 _mcmc_euler_gate    -> over-connects, breaks planarity
  - SANDWICH (arc added)    : s1_22 _sandwich            -> regresses (persistent defects)

Run: PYTHONPATH=. python3 rebuild/ablation_planarity.py --n 140 --seeds 3
"""
import argparse, json, os, statistics, sys
_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, _ROOT); sys.path.insert(0, os.path.join(_ROOT, "tooling"))
import referee_2d_topology as TP
import referee_2d_scaling as SC
from sec01_raw_wolfram_hypergraph_facts.s1_14_global_action import _mcmc_planar, _mcmc_euler_gate
from sec01_raw_wolfram_hypergraph_facts.s1_22_isotropy_sandwich import _sandwich

def sandwich_adj(n, seed, steps):
    a, *_ = _sandwich(n, 1.0, 3.0, steps, seed=seed, w_iso=2.0, cceil=2.1, T_hi=2.0, T_lo=0.2)
    return {u: set(a[u]) for u in a}

CONSTRUCTIONS = {
    "PLANAR (s1_14, step present)":      lambda n, s, st: {u:set(v) for u,v in _mcmc_planar(n, st, seed=s).items()},
    "EULER-GATE (s1_14, step altered)":  lambda n, s, st: {u:set(v) for u,v in _mcmc_euler_gate(n, st, seed=s).items()},
    "SANDWICH (s1_22, arc added)":       lambda n, s, st: sandwich_adj(n, s, st),
}

def measure(adj):
    r = TP.analyze(adj, "x")
    lazy = SC.lazy_rw_sdim(SC.nx_to_adj(TP.to_graph(adj))).get("8-24")
    return r, lazy

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=140)
    ap.add_argument("--seeds", type=int, default=3)
    ap.add_argument("--steps-per-n", type=int, default=60)
    ap.add_argument("--out", default="rebuild/ablation_results.json")
    a = ap.parse_args()
    seeds = [11, 1, 2, 3, 4][:a.seeds]
    g, _ = TP.rect_grid_adj(a.n); gr, gl = measure(g)
    print("grid@%d: bridges=%d artic=%d badlink=%d simpleBdy=%s lazyDs=%.2f"
          % (a.n, gr["bridges"], gr["articulation_points"], gr["bad_links"],
             gr["single_simple_boundary_cycle"], gl))
    out = {"meta": {"n": a.n, "seeds": seeds, "steps_per_n": a.steps_per_n},
           "grid": {"bridges": gr["bridges"], "lazy_ds": gl}, "constructions": {}}
    for name, gen in CONSTRUCTIONS.items():
        rows = []
        for s in seeds:
            adj = gen(a.n, s, a.n * a.steps_per_n)
            r, lazy = measure(adj)
            rows.append(dict(seed=s, planar=r.get("planar"), E=r["E"],
                             bridge_frac=round(r["bridges"]/r["E"], 4) if r.get("bridges") is not None else None,
                             artic_frac=round(r["articulation_points"]/r["V"], 4) if r.get("articulation_points") is not None else None,
                             bad_link_frac=r.get("bad_link_frac"),
                             simple_boundary=r.get("single_simple_boundary_cycle"),
                             lazy_ds=lazy))
        def mean(k):
            vals = [x[k] for x in rows if isinstance(x.get(k), (int, float))]
            return round(statistics.mean(vals), 4) if vals else None
        agg = dict(planar_rate=sum(1 for x in rows if x["planar"])/len(rows),
                   bridge_frac=mean("bridge_frac"), artic_frac=mean("artic_frac"),
                   bad_link_frac=mean("bad_link_frac"),
                   simple_boundary_rate=sum(1 for x in rows if x["simple_boundary"])/len(rows),
                   lazy_ds=mean("lazy_ds"))
        out["constructions"][name] = dict(per_seed=rows, agg=agg)
        print("%-34s planar=%.0f%% brgFrac=%s articFrac=%s badlinkFrac=%s simpleBdy=%.0f%% lazyDs=%s"
              % (name, 100*agg["planar_rate"], agg["bridge_frac"], agg["artic_frac"],
                 agg["bad_link_frac"], 100*agg["simple_boundary_rate"], agg["lazy_ds"]))
    os.makedirs(os.path.dirname(a.out), exist_ok=True)
    json.dump(out, open(a.out, "w"), indent=2)
    print("wrote", a.out)

if __name__ == "__main__":
    main()
