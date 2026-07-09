"""cdt_k0_driver.py -- the campaign-6 scan DRIVER (seed-averaged measurement + uncapped
k0xk22 grid + resumable checkpoints). The full runnable cdt_k0_local.py = ast-extracted
verbatim core (Causal + moves from cdt_causal_run.py; lazy_rw_sdim/ball_growth_dim/link_census
from tooling/) PREPENDED to this driver. Rebuild recipe: LESSONS_CDT.md lesson 17. No networkx."""

# =========================== measurement (seed-averaged, direct adjacency) ===========================
DS_WINDOWS = [(4, 12), (8, 24), (16, 48)]
DH_WINDOWS = [(2, 6), (3, 8), (4, 10)]


def state_adj(st):
    adj = defaultdict(set)
    for e in st.ecnt:
        a, b = tuple(e)
        adj[a].add(b); adj[b].add(a)
    return dict(adj)


def profile_of(st):
    pf = Counter()
    for f in st.stris:
        pf[st.time[next(iter(f))]] += 1
    return [pf.get(t, 0) for t in range(st.T)]


def _summ(vals):
    vals = [v for v in vals if v is not None]
    if not vals:
        return None
    return [round(statistics.mean(vals), 4), round(statistics.pstdev(vals), 4)]


def measure_state(st, seeds=8, tmax=50, seedbase=100):
    adj = state_adj(st)
    ds_runs = {("%d-%d" % w): [] for w in DS_WINDOWS}
    dh_runs = {("%d-%d" % w): [] for w in DH_WINDOWS}
    for k in range(seeds):
        ds = lazy_rw_sdim(adj, windows=DS_WINDOWS, tmax=tmax, seed=seedbase + k)
        dh = ball_growth_dim(adj, windows=DH_WINDOWS, seed=seedbase + 500 + k)
        for key in ds_runs:
            ds_runs[key].append(ds.get(key))
        for key in dh_runs:
            dh_runs[key].append(dh.get(key))
    prof = profile_of(st); mean = sum(prof) / max(1, len(prof))
    cv = statistics.pstdev(prof) / mean if mean else 0.0
    cen = link_census(list(st.tets))
    return dict(N0=st.N0, N3=st.N3, f22=round(st.nk[2] / max(1, st.N3), 4),
                ds={k: _summ(v) for k, v in ds_runs.items()},
                dh={k: _summ(v) for k, v in dh_runs.items()},
                prof_cv=round(cv, 4), prof_max=max(prof), prof_mean=round(mean, 1),
                bad=cen["bad"], census_n=cen["n"], profile=prof)


# =========================== exact T^3 benchmark (verify) ===========================
def kuhn_torus_tets(m):
    tets = set()
    for base in itertools.product(range(m), repeat=3):
        for perm in itertools.permutations(range(3)):
            cur = list(base); path = [tuple(cur)]
            for ax in perm:
                cur = list(cur); cur[ax] = (cur[ax] + 1) % m
                path.append(tuple(cur))
            tets.add(frozenset(path))
    return tets


def measure_torus(m, seeds=8, tmax=50):
    tets = kuhn_torus_tets(m)
    adj = defaultdict(set)
    for t in tets:
        for x, y in itertools.combinations(t, 2):
            adj[x].add(y); adj[y].add(x)
    adj = dict(adj)
    ds_runs = {("%d-%d" % w): [] for w in DS_WINDOWS}
    dh_runs = {("%d-%d" % w): [] for w in DH_WINDOWS}
    for k in range(seeds):
        ds = lazy_rw_sdim(adj, windows=DS_WINDOWS, tmax=tmax, seed=100 + k)
        dh = ball_growth_dim(adj, windows=DH_WINDOWS, seed=600 + k)
        for key in ds_runs:
            ds_runs[key].append(ds.get(key))
        for key in dh_runs:
            dh_runs[key].append(dh.get(key))
    return dict(m=m, N0=len(adj), N3=len(tets), ds={k: _summ(v) for k, v in ds_runs.items()},
                dh={k: _summ(v) for k, v in dh_runs.items()}, bad=link_census(list(tets))["bad"])


# =========================== chain helpers ===========================
def grow(st, rng, k0, V, eps=0.002):
    while st.N3 < V:
        st.sweep(rng, k0, -0.5, eps, V)


def run_sweeps(st, rng, k0, k22, V, n, k3, eps=0.002, tune=True):
    for _ in range(n):
        st.sweep(rng, k0, k3, eps, V, k22)
        if tune:
            k3 += min(max((st.N3 - V) * 2e-5, -2e-3), 2e-3)
    return k3


# =========================== scan driver (uncapped, resumable) ===========================
def log_progress(outdir, msg):
    line = "%s  %s" % (time.strftime("%H:%M:%S"), msg)
    with open(os.path.join(outdir, "progress.txt"), "a") as fh:
        fh.write(line + "\n")
    print(line, flush=True)


def done_configs(results_path):
    done = set()
    if os.path.exists(results_path):
        for l in open(results_path):
            try:
                r = json.loads(l)
                if r.get("kind") == "config_done":
                    done.add((r["k0"], r["k22"], r["V"], r["T"], r["seed"]))
            except Exception:
                pass
    return done


def run_config(k0, k22, V, T, seed, outdir, equil, nsnap, snapgap, seeds, tmax):
    rng = random.Random(seed)
    st = seed_state(T); k3 = 0.8
    grow(st, rng, k0, V)
    # tune + equilibrate (uncapped)
    k3 = run_sweeps(st, rng, k0, k22, V, equil, k3)
    swept = equil
    results = os.path.join(outdir, "results.jsonl")
    for snap in range(nsnap):
        k3 = run_sweeps(st, rng, k0, k22, V, snapgap, k3)
        swept += snapgap
        validate(st, heavy=False)
        m = measure_state(st, seeds=seeds, tmax=tmax)
        rec = dict(kind="snap", k0=k0, k22=k22, V=V, T=T, seed=seed, snap=snap, swept=swept,
                   k3=round(k3, 4), **m)
        with open(results, "a") as fh:
            fh.write(json.dumps(rec) + "\n")
        with open(os.path.join(outdir, "ckpt_k0%.1f_a%.1f_V%d_T%d_s%d.pkl" % (k0, k22, V, T, seed)), "wb") as fh:
            pickle.dump(dict(st=st, k3=k3, rng=rng, swept=swept), fh)
        log_progress(outdir, "k0=%.1f a=%.1f V=%d s%d snap%d/%d sw=%d | N0=%d f22=%.3f cv=%.3f max/mean=%.2f | dH2-6=%s dS8-24=%s bad=%d"
                     % (k0, k22, V, seed, snap + 1, nsnap, swept, m["N0"], m["f22"], m["prof_cv"],
                        m["prof_max"] / max(1, m["prof_mean"]), m["dh"]["2-6"], m["ds"]["8-24"], m["bad"]))
    with open(results, "a") as fh:
        fh.write(json.dumps(dict(kind="config_done", k0=k0, k22=k22, V=V, T=T, seed=seed)) + "\n")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--scan", action="store_true")
    ap.add_argument("--verify-torus", type=int, default=0)
    ap.add_argument("--verify-pkl", default=None)
    ap.add_argument("--V", type=int, default=12000)
    ap.add_argument("--T", type=int, default=15)
    ap.add_argument("--outdir", default="./out")
    ap.add_argument("--equil", type=int, default=2200)
    ap.add_argument("--nsnap", type=int, default=6)
    ap.add_argument("--snapgap", type=int, default=250)
    ap.add_argument("--seeds", type=int, default=8)
    ap.add_argument("--tmax", type=int, default=50)
    ap.add_argument("--k0grid", default="2,3,4,1,5")
    ap.add_argument("--k22grid", default="0,1.0,1.5")
    ap.add_argument("--mcseeds", default="0")
    a = ap.parse_args()
    if a.verify_torus:
        print(json.dumps(measure_torus(a.verify_torus, seeds=a.seeds, tmax=a.tmax)))
        return
    if a.verify_pkl:
        import __main__ as M
        M.Causal = Causal; M.IndexedSet = IndexedSet
        blob = pickle.load(open(a.verify_pkl, "rb")); st = blob["st"]
        print(json.dumps(measure_state(st, seeds=a.seeds, tmax=a.tmax)))
        return
    if a.scan:
        os.makedirs(a.outdir, exist_ok=True)
        results = os.path.join(a.outdir, "results.jsonl")
        done = done_configs(results)
        k0s = [float(x) for x in a.k0grid.split(",")]
        k22s = [float(x) for x in a.k22grid.split(",")]
        mcs = [int(x) for x in a.mcseeds.split(",")]
        t0 = time.time()
        log_progress(a.outdir, "SCAN start V=%d T=%d k0=%s k22=%s equil=%d nsnap=%d gap=%d done=%d"
                     % (a.V, a.T, k0s, k22s, a.equil, a.nsnap, a.snapgap, len(done)))
        for k0 in k0s:
            for k22 in k22s:
                for seed in mcs:
                    key = (k0, k22, a.V, a.T, seed)
                    if key in done:
                        log_progress(a.outdir, "skip (done) %s" % (key,))
                        continue
                    try:
                        run_config(k0, k22, a.V, a.T, seed, a.outdir, a.equil, a.nsnap, a.snapgap, a.seeds, a.tmax)
                    except Exception as e:
                        log_progress(a.outdir, "ERROR %s: %r" % (key, e))
        with open(os.path.join(a.outdir, "DONE"), "w") as fh:
            fh.write("scan complete in %.0f s\n" % (time.time() - t0))
        log_progress(a.outdir, "SCAN DONE in %.0f s" % (time.time() - t0))


if __name__ == "__main__":
    main()
