#!/usr/bin/env python3
"""Scaling-campaign aggregate: causal d_H(V) slope vs exact-T^3 benchmark slope."""
import json, math, statistics, sys
from collections import defaultdict

path = "/sessions/zealous-nifty-heisenberg/mnt/outputs/cdt_causal_results.jsonl"
causal, bench, euclid, longm = defaultdict(list), {}, [], []
for line in open(path):
    r = json.loads(line)
    k = r.get("kind")
    if k == "torus_benchmark":
        bench[r["m"]] = r
    elif k == "euclid_control":
        euclid.append(r)
    elif k == "long_measure":
        longm.append(r)
    elif r.get("tuned"):
        causal[(r["k0"], r["V"])].append(r)

bpts = sorted((r["N0"], r["dh"]["2-6"], r["ds"]["4-12"]) for r in bench.values())
def bench_at(n0, idx):
    xs = [math.log(p[0]) for p in bpts]; ys = [p[idx] for p in bpts]
    x = math.log(n0)
    if x <= xs[0]: return ys[0]
    if x >= xs[-1]: return ys[-1]
    for i in range(len(xs) - 1):
        if xs[i] <= x <= xs[i + 1]:
            f = (x - xs[i]) / (xs[i + 1] - xs[i])
            return ys[i] + f * (ys[i + 1] - ys[i])

print("== benchmark line (exact T^3) ==")
for n0, dh, ds in bpts:
    print("  N0=%4d  d_s(4-12)=%.2f  d_H(2-6)=%.2f" % (n0, ds, dh))

print("== causal groups (pooled tuned snapshots, both seeds) ==")
rows = []
for (k0, V), rs in sorted(causal.items(), key=lambda x: (x[0][1], x[0][0])):
    if V == 1500 and any(r["T"] == 8 for r in rs):
        rs = [r for r in rs if r["T"] != 8]
    ds = [r["ds"]["4-12"] for r in rs]; dh = [r["dh"]["2-6"] for r in rs]
    n0 = statistics.mean([r["N0"] for r in rs])
    seeds = sorted({r["seed"] for r in rs})
    bad = sum(r["census"]["bad"] for r in rs)
    bdh = bench_at(n0, 1); bds = bench_at(n0, 2)
    dhm = statistics.mean(dh); dsm = statistics.mean(ds)
    sd_dh = statistics.stdev(dh) if len(dh) > 1 else 0.0
    sd_ds = statistics.stdev(ds) if len(ds) > 1 else 0.0
    rows.append((k0, V, n0, dhm, sd_dh, dsm, sd_ds, bdh, bds, len(rs)))
    print("  k0=%.0f V=%4d N0~%4.0f seeds=%s snaps=%d bad=%d | d_H=%.2f+/-%.2f (bench %.2f, ratio %.2f) | d_s=%.2f+/-%.2f (bench %.2f, diff %+.2f)"
          % (k0, V, n0, seeds, len(rs), bad, dhm, sd_dh, bdh, dhm / bdh, dsm, sd_ds, bds, dsm - bds))

print("== d_H slope per ln(N0): causal vs benchmark ==")
for k0 in (1.0, 2.0):
    sel = sorted([r for r in rows if r[0] == k0], key=lambda r: r[2])
    for a, b in zip(sel, sel[1:]):
        dln = math.log(b[2] / a[2])
        sc = (b[3] - a[3]) / dln
        sb = (bench_at(b[2], 1) - bench_at(a[2], 1)) / dln
        print("  k0=%.0f V %4d->%4d: causal slope %.2f | bench slope %.2f" % (k0, a[1], b[1], sc, sb))
    lo, hi = sel[0], sel[-1]
    dln = math.log(hi[2] / lo[2])
    print("  k0=%.0f OVERALL: causal %.3f/ln N0 | bench %.3f/ln N0 | offset at V=6000: %.2f"
          % (k0, (hi[3] - lo[3]) / dln, (bench_at(hi[2], 1) - bench_at(lo[2], 1)) / dln, bench_at(hi[2], 1) - hi[3]))

print("== Euclidean controls (k3=-0.2, v0 moves; depth caveat at n0>=500) ==")
for r in sorted(euclid, key=lambda r: r["n0"]):
    att = r["sweeps"] / r["tets"]
    print("  N0=%4d d_s=%.2f (bench %.2f) d_H=%.2f (bench %.2f, ratio %.2f) [%.1f att/tet]"
          % (r["n0"], r["ds"], bench_at(r["n0"], 2), r["dh"], bench_at(r["n0"], 1), r["dh"] / bench_at(r["n0"], 1), att))

print("== long-window d_s (8-24 = longest clean window) ==")
for r in sorted(longm, key=lambda r: (r["V"], r["k0"])):
    print("  causal k0=%.0f V=%4d N0=%d: d_s(8-24)=%.2f d_H(3-8)=%.2f" % (r["k0"], r["V"], r["N0"], r["ds_long"]["8-24"], r["dh_long"]["3-8"]))
for m in sorted(bench):
    r = bench[m]
    if "8-24" in r["ds"]:
        print("  torus  m=%d N0=%d: d_s(8-24)=%.2f d_H(3-8)=%s" % (m, r["N0"], r["ds"]["8-24"], r["dh"].get("3-8")))
