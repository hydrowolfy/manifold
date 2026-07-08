#!/usr/bin/env python3
"""Euclidean DT control at matched vertex count, v0 moves/params UNCHANGED, chunked."""
import argparse, itertools, json, math, os, pickle, random, sys, time as _time

sys.path[:0] = ["/tmp/m", "/tmp/m/tooling"]
from construct_3manifold import sphere_seed, move_1_4, move_2_3
from cdt_experiment import move_3_2, adj_of, measure

ap = argparse.ArgumentParser()
ap.add_argument("--n0", type=int, default=500)
ap.add_argument("--k3", type=float, default=-0.2)
ap.add_argument("--sweeps", type=int, default=3000)
ap.add_argument("--seed", type=int, default=0)
ap.add_argument("--budget-s", type=float, default=30.0, dest="budget_s")
ap.add_argument("--scratch", default="/tmp/m/scratch")
ap.add_argument("--log", default=None)
a = ap.parse_args()

os.makedirs(a.scratch, exist_ok=True)
sf = os.path.join(a.scratch, "euclid_n%d_k3%+.2f_s%d.pkl" % (a.n0, a.k3, a.seed))
t0 = _time.time()
if os.path.exists(sf):
    with open(sf, "rb") as fh:
        blob = pickle.load(fh)
    tets, nv, phase, done, rng = blob["tets"], blob["nv"], blob["phase"], blob["done"], blob["rng"]
    random.setstate(blob["rstate"])
else:
    rng = random.Random(a.seed); random.seed(a.seed)
    tets = sphere_seed(); nv = 5; phase = "build"; done = 0

if phase == "build":
    while nv < a.n0 and _time.time() - t0 < a.budget_s:
        if rng.random() < 0.6:
            if not move_2_3(tets, rng):
                nv = move_1_4(tets, nv)
        else:
            nv = move_1_4(tets, nv)
    if nv >= a.n0:
        phase = "bulk"
if phase == "bulk":
    while done < 2 * a.n0 and _time.time() - t0 < a.budget_s:
        move_2_3(tets, rng); done += 1
    if done >= 2 * a.n0:
        phase = "chain"; done = 0
if phase == "chain":
    while done < a.sweeps and _time.time() - t0 < a.budget_s:
        if rng.random() < 0.5:
            if rng.random() < math.exp(-a.k3):
                move_2_3(tets, rng)
        else:
            if rng.random() < min(1.0, math.exp(a.k3)):
                move_3_2(tets, rng)
        done += 1

with open(sf, "wb") as fh:
    pickle.dump(dict(tets=tets, nv=nv, phase=phase, done=done, rng=rng, rstate=random.getstate()), fh)

if phase == "chain" and done >= a.sweeps:
    c, ds, dH = measure(tets, adj_of(tets))
    rec = dict(kind="euclid_control", n0=a.n0, k3=a.k3, sweeps=done, seed=a.seed,
               tets=len(tets), bad=c["bad"], ds=ds, dh=dH)
    if a.log:
        with open(a.log, "a") as fh:
            fh.write(json.dumps(rec) + "\n")
    print("EUCLID control n0=%d k3=%+.2f sweeps=%d DONE: tets=%d bad=%d d_s(4-12)=%s d_H(2-6)=%s"
          % (a.n0, a.k3, done, len(tets), c["bad"], ds, dH))
else:
    print("EUCLID control n0=%d: phase=%s nv=%d done=%d tets=%d (checkpointed, rerun to continue)"
          % (a.n0, phase, nv, done, len(tets)))
