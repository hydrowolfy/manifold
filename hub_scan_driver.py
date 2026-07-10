#!/usr/bin/env python3
"""Resumable staged driver for the PREREG_CDT_HUB sigma scan (campaign 7).
Imports VERIFIED physics from cdt_frontier2_run + tooling estimators (same seeding
as remeasure.py). Each invocation self-limits to --budget-s wall, checkpoints, exits.
Re-invoke until it prints 'SCAN COMPLETE'. Config frozen from PREREG_CDT_HUB Sec 4."""
import argparse, json, os, pickle, random, statistics, sys, time
from collections import Counter, defaultdict
os.environ.setdefault("MANIFOLD_REPO", os.getcwd())
sys.path[:0] = [os.getcwd(), os.path.join(os.getcwd(), "tooling")]
import cdt_frontier2_run as F
from referee_2d_scaling import lazy_rw_sdim, ball_growth_dim, nx_to_adj
from referee_2d_topology import to_graph
from referee_3d import link_census

def adj_from_state(st):
    adj = defaultdict(set)
    for e in st.ecnt:
        a, b = tuple(e); adj[a].add(b); adj[b].add(a)
    return dict(adj)

def profile_cv(st):
    pf = Counter()
    for f in st.stris:
        pf[st.time[next(iter(f))]] += 1
    prof = [pf.get(t, 0) for t in range(st.T)]
    mean = sum(prof)/max(1, len(prof))
    cv = (statistics.pstdev(prof)/mean) if mean else 0.0
    return prof, round(cv, 3)

def f22_of(st):
    return round(st.nk[2]/max(1, st.N3), 4)

def load(path):
    with open(path, "rb") as fh: return pickle.load(fh)
def save(path, blob):
    tmp = path + ".tmp"
    with open(tmp, "wb") as fh: pickle.dump(blob, fh)
    os.replace(tmp, path)

def measure_seedavg(st, seeds, seedbase, tmax, ds_wins):
    adj = adj_from_state(st)
    g = nx_to_adj(to_graph(adj))
    dh_wins = [(2,6),(3,8),(4,10)]
    ds_runs = {("%d-%d"%w): [] for w in ds_wins}
    dh_runs = {("%d-%d"%w): [] for w in dh_wins}
    for k in range(seeds):
        ds = lazy_rw_sdim(g, windows=ds_wins, tmax=tmax, seed=seedbase+k)
        dh = ball_growth_dim(g, windows=dh_wins, seed=seedbase+500+k)
        for key in ds_runs: ds_runs[key].append(ds.get(key))
        for key in dh_runs: dh_runs[key].append(dh.get(key))
    def summ(vs):
        vs = [v for v in vs if v is not None]
        if not vs: return None
        return [round(statistics.mean(vs),4), round(statistics.stdev(vs) if len(vs)>1 else 0.0,4), len(vs)]
    deg = [len(v) for v in adj.values()]
    return dict(ds={k:summ(v) for k,v in ds_runs.items()},
                dh={k:summ(v) for k,v in dh_runs.items()},
                deg_mean=round(sum(deg)/len(deg),2), deg_sd=round(statistics.pstdev(deg),2),
                deg_max=max(deg))

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dir", required=True)
    ap.add_argument("--V", type=int, default=6000)
    ap.add_argument("--T", type=int, default=12)
    ap.add_argument("--k0", type=float, default=2.0)
    ap.add_argument("--D0", type=float, default=14.0)
    ap.add_argument("--sigmas", default="0.0,0.02,0.05,0.10,0.20")
    ap.add_argument("--budget-s", type=float, default=40.0, dest="budget_s")
    ap.add_argument("--seeds", type=int, default=8)
    ap.add_argument("--seedbase", type=int, default=200)
    ap.add_argument("--tmax", type=int, default=100)
    ap.add_argument("--eps", type=float, default=0.002)
    ap.add_argument("--ref-target", type=int, default=900, dest="ref_target")  # min sweeps for ref
    ap.add_argument("--equil-target", type=int, default=600, dest="equil_target")
    ap.add_argument("--tune", type=int, default=600)
    a = ap.parse_args()
    t0 = time.time()
    os.makedirs(a.dir, exist_ok=True)
    statef = os.path.join(a.dir, "scan_state.json")
    resultf = os.path.join(a.dir, "results.jsonl")
    sigmas = [float(x) for x in a.sigmas.split(",")]
    ds_wins = [(8,24),(16,48)]
    if os.path.exists(statef):
        with open(statef) as fh: S = json.load(fh)
    else:
        S = dict(stage="ref", ref_sweeps=0, ref_ready=False,
                 sigmas={("%.3f"%s): dict(sweeps=0, equil=False, measured=False, f22_hist=[], cv_hist=[]) for s in sigmas})
    def flush():
        with open(statef, "w") as fh: json.dump(S, fh, indent=0)

    # ---- helper: run sweeps on a blob until wall, with gentle k3 volume control ----
    def advance(blob, sigma, add_sweeps_key, wall):
        st, k3, done, rng = blob["st"], blob["k3"], blob["done"], blob["rng"]
        n=0
        while time.time()-t0 < wall:
            st.sweep(rng, a.k0, k3, a.eps, a.V, 0.0, sigma, a.D0)
            k3 += min(max((st.N3 - a.V)*2e-5, -2e-3), 2e-3)  # always hold volume near V
            done += 1; n += 1
            if n % 25 == 0 and time.time()-t0 >= wall: break
        F.validate(st, heavy=False)
        blob["st"], blob["k3"], blob["done"], blob["rng"] = st, k3, done, rng
        return n

    # ============ STAGE: reference (sigma=0) grow+thermalize ============
    refpath = os.path.join(a.dir, "ref.pkl")
    if not S["ref_ready"]:
        if os.path.exists(refpath):
            blob = load(refpath)
        else:
            st = F.seed_state(a.T); rng = random.Random(0)
            while st.N3 < a.V:
                st.sweep(rng, a.k0, -0.5, a.eps, a.V)
            blob = dict(st=st, k3=0.8, done=0, rng=rng)
        n = advance(blob, 0.0, "ref", a.budget_s)
        st = blob["st"]; S["ref_sweeps"] = blob["done"]
        prof, cv = profile_cv(st); f22 = f22_of(st)
        c = link_census(list(st.tets))
        S["sigmas"]["0.000"]["f22_hist"].append(f22)
        S["sigmas"]["0.000"]["cv_hist"].append(cv)
        S["sigmas"]["0.000"]["sweeps"] = blob["done"]
        save(refpath, blob)
        # ready when enough sweeps AND f22 plateau (last two within 0.01)
        h = S["sigmas"]["0.000"]["f22_hist"]
        plateau = len(h) >= 2 and abs(h[-1]-h[-2]) < 0.01
        if S["ref_sweeps"] >= a.ref_target and (plateau or S["ref_sweeps"] >= 1400):
            S["ref_ready"] = True; S["sigmas"]["0.000"]["equil"] = True
            # seed the sigma=0 pickle = ref
            save(os.path.join(a.dir, "sig_0.000.pkl"), blob)
        flush()
        print("REF sweeps=%d f22=%.3f cv=%.3f bad=%d N0=%d N3=%d ready=%s (+%d sw, %.1fs)" %
              (S["ref_sweeps"], f22, cv, c["bad"], st.N0, st.N3, S["ref_ready"], n, time.time()-t0))
        return

    # ============ STAGE: equilibrate each sigma>0 ============
    for s in sigmas:
        key = "%.3f"%s
        if s == 0.0:
            continue
        rec = S["sigmas"][key]
        if rec["equil"]:
            continue
        sp = os.path.join(a.dir, "sig_%s.pkl"%key)
        if not os.path.exists(sp):
            import shutil; shutil.copy(os.path.join(a.dir,"sig_0.000.pkl"), sp)  # warm-start from ref
            rec["sweeps"]=0
        blob = load(sp)
        n = advance(blob, s, key, a.budget_s)
        st = blob["st"]; rec["sweeps"] = blob["done"] if "done" in blob else rec["sweeps"]+n
        prof, cv = profile_cv(st); f22 = f22_of(st)
        c = link_census(list(st.tets))
        rec["f22_hist"].append(f22); rec["cv_hist"].append(cv)
        save(sp, blob)
        h = rec["f22_hist"]
        plateau = len(h) >= 2 and abs(h[-1]-h[-2]) < 0.01
        # require a floor of accumulated sweeps at this sigma
        rec["_acc"] = rec.get("_acc",0)+n
        if rec["_acc"] >= a.equil_target and (plateau or rec["_acc"] >= a.equil_target*3):
            rec["equil"]=True
        flush()
        print("SIG %s acc_sw=%d f22=%.3f cv=%.3f bad=%d N0=%d equil=%s (+%d sw, %.1fs)" %
              (key, rec["_acc"], f22, cv, c["bad"], st.N0, rec["equil"], n, time.time()-t0))
        return

    # ============ STAGE: measure each sigma (seed-averaged) ============
    for s in sigmas:
        key = "%.3f"%s
        rec = S["sigmas"][key]
        if rec["measured"]:
            continue
        sp = os.path.join(a.dir, "sig_%s.pkl"%key)
        blob = load(sp); st = blob["st"]
        prof, cv = profile_cv(st); f22 = f22_of(st)
        c = link_census(list(st.tets))
        mm = measure_seedavg(st, a.seeds, a.seedbase, a.tmax, ds_wins)
        out = dict(kind="hub_result", sigma=s, D0=a.D0, k0=a.k0, V=a.V, T=a.T,
                   N0=st.N0, N3=st.N3, f22=f22, prof_cv=cv, prof_min=min(prof), prof_max=max(prof),
                   census_bad=c["bad"], acc_sweeps=rec.get("_acc",0), **mm)
        with open(resultf, "a") as fh: fh.write(json.dumps(out)+"\n")
        rec["measured"]=True; flush()
        dss = mm["ds"].get("8-24"); dhh = mm["dh"].get("2-6")
        print("MEASURED sigma=%s: d_s(8-24)=%.3f+-%.3f d_H(2-6)=%.3f+-%.3f f22=%.3f cv=%.3f degmax=%d bad=%d (%.1fs)" %
              (key, dss[0], dss[1], dhh[0], dhh[1], f22, cv, mm["deg_max"], c["bad"], time.time()-t0))
        return

    print("SCAN COMPLETE")

if __name__ == "__main__":
    main()
