#!/usr/bin/env python3
"""d_H(3-8) and d_H(2-6) vs sweep time per chain -- the thermalization tracker."""
import json, sys
from collections import defaultdict

series = defaultdict(list)
for line in open("/sessions/zealous-nifty-heisenberg/mnt/outputs/cdt_causal_results.jsonl"):
    r = json.loads(line)
    if r.get("kind") is None and "sweeps" in r:
        key = (r["k0"], r["V"], r["T"], r["seed"], r.get("k22", 0.0))
        series[key].append((r["sweeps"], r["dh"].get("3-8"), r["dh"]["2-6"], r["ds"].get("8-24"), r["census"]["bad"]))
sel = sys.argv[1:] if len(sys.argv) > 1 else None
for key in sorted(series):
    k0, V, T, seed, k22 = key
    tag = "k0=%.0f V=%d T=%d s%d" % (k0, V, T, seed) + (" k22=%+.1f" % k22 if k22 else "")
    if sel and not any(s in tag for s in sel):
        continue
    pts = sorted(series[key])
    line_ = " ".join("%d:%s/%.2f" % (sw, ("%.2f" % dh38 if dh38 else "--"), dh26) for sw, dh38, dh26, _, _ in pts)
    badtot = sum(p[4] for p in pts)
    print("%s bad=%d | sweeps:dH(3-8)/dH(2-6) -> %s" % (tag, badtot, line_))
