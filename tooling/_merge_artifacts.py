#!/usr/bin/env python3
"""Merge per-batch referee JSON artifacts (produced by chunked runs) into one sweep file."""
import glob
import json
import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.dirname(_HERE)
if _ROOT not in sys.path:
    sys.path.insert(0, _ROOT)


def merge(kind, inglob, out):
    if kind == "topology":
        import referee_2d_topology as M
    else:
        import referee_2d_scaling as M
    files = sorted(glob.glob(inglob))
    base = None
    cand = {}          # N -> {seed -> row}
    controls = {}      # name -> N -> node (dict or {per_seed,agg})
    for fpath in files:
        d = json.load(open(fpath))
        if base is None:
            base = d
        for nk, node in d.get("candidate", {}).items():
            cand.setdefault(nk, {})
            for r in node["per_seed"]:
                cand[nk][r.get("seed")] = r
        for name, byN in d.get("controls", {}).items():
            controls.setdefault(name, {})
            for nk, node in byN.items():
                if nk not in controls[name]:
                    controls[name][nk] = node
                else:
                    old = controls[name][nk]
                    if isinstance(node, dict) and "per_seed" in node and "per_seed" in old:
                        seen = {r.get("seed"): r for r in old["per_seed"]}
                        for r in node["per_seed"]:
                            seen[r.get("seed")] = r
                        rows = [seen[k] for k in sorted(seen)]
                        controls[name][nk] = dict(per_seed=rows, agg=M.aggregate(rows))
    out_candidate = {}
    for nk, seedmap in cand.items():
        rows = [seedmap[k] for k in sorted(seedmap)]
        out_candidate[nk] = dict(per_seed=rows, agg=M.aggregate(rows))
    result = dict(meta=base["meta"], candidate=out_candidate, controls=controls)
    result["meta"]["merged_from"] = [os.path.basename(f) for f in files]
    result["meta"]["sizes"] = sorted(int(k.split("=")[1]) for k in out_candidate)
    json.dump(result, open(out, "w"), indent=2)
    ns = {k: len(v["per_seed"]) for k, v in out_candidate.items()}
    print("merged %d files -> %s ; candidate seeds/N: %s" % (len(files), out, ns))


if __name__ == "__main__":
    merge(sys.argv[1], sys.argv[2], sys.argv[3])
