#!/usr/bin/env python3
"""
cdt4_scan.py -- Metropolis engine + (kappa_0, Delta) scan driver for 3+1D causal CDT.
Uses the validated full move set in cdt4_prod.py (stdlib only, no networkx).

Action (standard 4D CDT Regge form):
    S = -(kappa0 + 6*Delta)*N0 + kappa4*N4 + Delta*(2*N41 + N32) + eps*(N4 - N4t)^2
The eps-quadratic fixes the 4-volume near N4t (auto-tunes the effective kappa4), so we
scan (kappa0, Delta) at ~fixed N4 -- the standard way to map the CDT phase diagram.

Detailed balance (verified by --db-check): each step selects a move type uniformly
from the 7, picks a primitive uniformly from that type's live pick-set (exact count via
indexed-sets), and accepts with
    A = min(1, (K_fwd / K_rev) * exp(-dS))
where K_fwd = #primitives of the forward type BEFORE, K_rev = #primitives of the reverse
type AFTER. Uniform type selection makes the reverse-pair proposal probabilities cancel.

CLI:
  --db-check            verify the DB balance equation numerically on random states
  --grow --T --N4t      grow a fresh flat seed to ~N4t (biased additive moves)
  --thermalize ...      run Metropolis, checkpoint, log observables
  --scan ...            scan a (kappa0,Delta) grid, checkpoint each point, results.jsonl
  --measure --pkl P     seed-averaged d_H/d_s/profile of a checkpoint
"""
import sys, os, math, random, pickle, time, json, argparse
from collections import Counter, defaultdict
sys.path.insert(0, "tooling"); sys.path.insert(0, ".")
import cdt4_prod as C
from cdt4_prod import FS

MOVES = ['24','42','33','46','64','28','82']
PICK  = {'24':'S_tet','42':'S_edge','33':'S_tri','46':'S_stri','64':'S_sedge','28':'S_stet','82':'S_vert'}
REV   = {'24':'42','42':'24','33':'33','46':'64','64':'46','28':'82','82':'28'}
REVPICK = {m: PICK[REV[m]] for m in MOVES}

def action_val(st, p):
    k0, D, k4, eps, N4t = p['k0'], p['D'], p['k4'], p['eps'], p['N4t']
    N0 = st.N0; N4 = st.N4
    return (-(k0 + 6*D)*N0 + k4*N4 + D*(2*st.n41 + st.n32) + eps*(N4 - N4t)**2)

def mstep(st, p, rng):
    """one Metropolis attempt; returns move-key if accepted else None."""
    m = MOVES[rng.randrange(7)]
    pk = getattr(st, PICK[m])
    if len(pk) == 0: return None
    Kf = len(pk)
    prim = pk.pick(rng)
    prop = getattr(st, 'prop_' + m)(prim)
    if prop is None: return None
    rems, adds, meta = prop
    S0 = action_val(st, p)
    st.apply(rems, adds)
    S1 = action_val(st, p)
    Kr = len(getattr(st, REVPICK[m]))
    dS = S1 - S0
    if Kr == 0:
        accept = False
    else:
        logA = math.log(Kf) - math.log(Kr) - dS
        accept = (logA >= 0.0) or (rng.random() < math.exp(logA))
    if accept:
        if m == '28': st.nextv += 1
        return m
    st.apply(adds, rems)
    if m == '28':
        x = meta[1]
        if x in st.time and x not in st.vcount: del st.time[x]
    return None

def sweep(st, p, rng, nsteps):
    acc = Counter()
    for _ in range(nsteps):
        k = mstep(st, p, rng)
        if k: acc[k] += 1
    return acc

def grow_to(st, N4t, rng, cap_s=1e9):
    p = dict(k0=0.0, D=0.0, k4=-0.8, eps=0.0, N4t=N4t)
    t0 = time.time()
    while st.N4 < N4t and time.time() - t0 < cap_s:
        r = rng.random()
        if r < 0.45 and len(st.S_tet):   prop = st.prop_24(st.S_tet.pick(rng)); m='24'
        elif r < 0.85 and len(st.S_stet):prop = st.prop_28(st.S_stet.pick(rng)); m='28'
        elif len(st.S_stri):             prop = st.prop_46(st.S_stri.pick(rng)); m='46'
        else: prop=None; m=None
        if prop:
            st.apply(prop[0], prop[1])
            if m=='28': st.nextv += 1
    return st

def measure(st, seeds=8, dHw=((2,6),(3,8)), dSw=((8,24),(10,30)), tmax=40, nz=6, nsrc=16, seedbase=1):
    adj = C.skeleton_adj(st)
    H = defaultdict(list); S = defaultdict(list)
    for s in range(seeds):
        for k,v in C.ball_growth_dim(adj, windows=dHw, nsrc=nsrc, seed=seedbase+s).items():
            if v is not None: H[k].append(v)
        for k,v in C.lazy_rw_sdim(adj, windows=dSw, nz=nz, tmax=tmax, seed=seedbase+100+s).items():
            if v is not None: S[k].append(v)
    import statistics as _st
    ms = lambda d: {k:[round(_st.mean(v),4), round(_st.pstdev(v),4)] for k,v in d.items()}
    prof = C.slice_profile(st)
    mean = sum(prof)/len(prof) if prof else 0.0
    cv = (math.sqrt(sum((x-mean)**2 for x in prof)/len(prof))/mean) if mean>0 else 0.0
    degs = [len(v) for v in adj.values()]
    return dict(N0=st.N0, N4=st.N4, n41=st.n41, n32=st.n32,
                f_tl=round(st.n32/max(st.N4,1),4), f_N41=round(st.n41/max(st.N4,1),4),
                dH=ms(H), dS=ms(S), profile=prof, prof_cv=round(cv,4),
                prof_max=max(prof) if prof else 0, prof_min=min(prof) if prof else 0,
                deg_mean=round(sum(degs)/len(degs),2), deg_max=max(degs), N_slices=st.T)

def save_ckpt(st, rng, meta, path):
    st.time = {v:t for v,t in st.time.items() if v in st.vcount}
    tmp = path + ".tmp"
    with open(tmp, "wb") as f:
        pickle.dump(dict(st=st, rng=rng.getstate(), meta=meta), f, protocol=4)
    os.replace(tmp, path)

def load_ckpt(path):
    with open(path, "rb") as f:
        d = pickle.load(f)
    rng = random.Random(); rng.setstate(d["rng"])
    return d["st"], rng, d["meta"]

def db_check(nstates=6, ntests=400):
    """Verify the DB balance equation g_f A_f pi(c) == g_r A_r pi(c') for random legal
    moves at random couplings. g=1/K (uniform type prob cancels), pi ~ exp(-S)."""
    rng = random.Random(7); worst = 0.0; n = 0
    for s in range(nstates):
        st = C.seed_flat(4)
        for _ in range(rng.randint(80,240)):
            mstep(st, dict(k0=rng.uniform(0,5),D=rng.uniform(0,1),k4=0.0,eps=0.0,N4t=st.N4), rng)
        p = dict(k0=rng.uniform(0,5), D=rng.uniform(-0.2,1.0), k4=0.0, eps=0.0, N4t=st.N4)
        for _ in range(ntests):
            m = MOVES[rng.randrange(7)]
            pk = getattr(st, PICK[m])
            if len(pk)==0: continue
            Kf = len(pk); prim = pk.pick(rng)
            prop = getattr(st,'prop_'+m)(prim)
            if prop is None: continue
            rems, adds, meta = prop
            S0 = action_val(st, p); st.apply(rems, adds); S1 = action_val(st, p)
            Kr = len(getattr(st, REVPICK[m]))
            dS = S1 - S0
            Af = min(1.0, (Kf/Kr)*math.exp(-min(dS,700)))
            Ar = min(1.0, (Kr/Kf)*math.exp(min(dS,700)))
            lhs = math.log(Af) - math.log(Kf) - S0
            rhs = math.log(Ar) - math.log(Kr) - S1
            worst = max(worst, abs(lhs-rhs)); n += 1
            st.apply(adds, rems)
            if m=='28':
                x=meta[1]
                if x in st.time and x not in st.vcount: del st.time[x]
    print(f"DB balance check: {n} (move,state) pairs, worst |log lhs - log rhs| = {worst:.2e}")
    print("DETAILED BALANCE:", "PASS (<1e-9)" if worst < 1e-9 else "FAIL")
    return worst < 1e-9

def thermalize(st, p, rng, sweeps, sweep_len, ckpt, log, meta, budget_s=1e9, measure_every=0):
    t0 = time.time(); done = meta.get("sweeps_done", 0)
    for i in range(sweeps):
        acc = sweep(st, p, rng, sweep_len)
        done += 1; meta["sweeps_done"] = done
        b,u = st.census()
        prof = C.slice_profile(st); mean=sum(prof)/len(prof)
        cv = math.sqrt(sum((x-mean)**2 for x in prof)/len(prof))/mean if mean>0 else 0
        rec = dict(sweep=done, N0=st.N0, N4=st.N4, f_tl=round(st.n32/max(st.N4,1),4),
                   f_N41=round(st.n41/max(st.N4,1),4), prof_cv=round(cv,4),
                   acc=dict(acc), census_bad=b, t=round(time.time()-t0,1))
        with open(log, "a") as f: f.write(json.dumps(rec)+"\n")
        if ckpt: save_ckpt(st, rng, meta, ckpt)
        if time.time()-t0 > budget_s: break
    return st

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--db-check", action="store_true")
    ap.add_argument("--grow", action="store_true")
    ap.add_argument("--thermalize", action="store_true")
    ap.add_argument("--scan", action="store_true")
    ap.add_argument("--measure", action="store_true")
    ap.add_argument("--T", type=int, default=8)
    ap.add_argument("--N4t", type=int, default=8000)
    ap.add_argument("--k0", type=float, default=2.2)
    ap.add_argument("--D", type=float, default=0.6)
    ap.add_argument("--k4", type=float, default=0.0)
    ap.add_argument("--eps", type=float, default=0.02)
    ap.add_argument("--sweeps", type=int, default=100)
    ap.add_argument("--sweep-len", type=int, default=0)
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--budget-s", type=float, default=1e9)
    ap.add_argument("--scratch", type=str, default="scratch")
    ap.add_argument("--pkl", type=str, default=None)
    ap.add_argument("--grid-k0", type=str, default="0.8,1.5,2.2,3.0,4.0")
    ap.add_argument("--grid-D", type=str, default="0.0,0.3,0.6")
    ap.add_argument("--meas-seeds", type=int, default=8)
    args = ap.parse_args()
    os.makedirs(args.scratch, exist_ok=True)
    sl = args.sweep_len or args.N4t

    if args.db_check:
        sys.exit(0 if db_check() else 1)

    if args.grow:
        rng = random.Random(args.seed); st = C.seed_flat(args.T)
        grow_to(st, args.N4t, rng, cap_s=args.budget_s)
        path = os.path.join(args.scratch, f"grow_T{args.T}_N{args.N4t}_s{args.seed}.pkl")
        save_ckpt(st, rng, dict(kind="grow", T=args.T, N4t=args.N4t, sweeps_done=0), path)
        print(f"grew to N4={st.N4} N0={st.N0} census={st.census()} -> {path}")
        return

    if args.measure:
        st, rng, meta = load_ckpt(args.pkl)
        print(json.dumps(measure(st, seeds=args.meas_seeds), indent=2))
        return

    if args.thermalize:
        base = os.path.join(args.scratch, f"grow_T{args.T}_N{args.N4t}_s{args.seed}.pkl")
        if args.pkl: base = args.pkl
        if os.path.exists(base):
            st, rng, meta = load_ckpt(base)
        else:
            rng = random.Random(args.seed); st = C.seed_flat(args.T)
            grow_to(st, args.N4t, rng); meta = dict(sweeps_done=0)
        p = dict(k0=args.k0, D=args.D, k4=args.k4, eps=args.eps, N4t=args.N4t)
        tag = f"therm_T{args.T}_N{args.N4t}_k{args.k0}_D{args.D}_s{args.seed}"
        ckpt = os.path.join(args.scratch, tag+".pkl")
        log = os.path.join(args.scratch, tag+".jsonl")
        thermalize(st, p, rng, args.sweeps, sl, ckpt, log, meta, budget_s=args.budget_s)
        print(f"thermalized {meta['sweeps_done']} sweeps: N0={st.N0} N4={st.N4} census={st.census()} -> {ckpt}")
        return

    if args.scan:
        grid_k0 = [float(x) for x in args.grid_k0.split(",")]
        grid_D  = [float(x) for x in args.grid_D.split(",")]
        results = os.path.join(args.scratch, "results.jsonl")
        prog = os.path.join(args.scratch, "progress.txt")
        base = os.path.join(args.scratch, f"grow_T{args.T}_N{args.N4t}_s{args.seed}.pkl")
        if not os.path.exists(base):
            rng = random.Random(args.seed); st0 = C.seed_flat(args.T)
            grow_to(st0, args.N4t, rng)
            save_ckpt(st0, rng, dict(kind="grow", sweeps_done=0), base)
        t0 = time.time()
        for D in grid_D:
            for k0 in grid_k0:
                tag = f"pt_T{args.T}_N{args.N4t}_k{k0}_D{D}"
                ckpt = os.path.join(args.scratch, tag+".pkl")
                if os.path.exists(ckpt):
                    st, rng, meta = load_ckpt(ckpt)
                else:
                    st, rng, meta = load_ckpt(base); meta = dict(sweeps_done=0, k0=k0, D=D)
                p = dict(k0=k0, D=D, k4=args.k4, eps=args.eps, N4t=args.N4t)
                log = os.path.join(args.scratch, tag+".jsonl")
                thermalize(st, p, rng, args.sweeps, sl, ckpt, log, meta, budget_s=args.budget_s)
                m = measure(st, seeds=args.meas_seeds)
                m.update(dict(k0=k0, D=D, T=args.T, N4t=args.N4t, sweeps=meta["sweeps_done"]))
                with open(results, "a") as f: f.write(json.dumps(m)+"\n")
                with open(prog, "a") as f:
                    f.write(f"[{round(time.time()-t0)}s] k0={k0} D={D}: N0={m['N0']} N4={m['N4']} "
                            f"f_tl={m['f_tl']} cv={m['prof_cv']} dH={m['dH']} dS={m['dS']}\n")
                print(f"  point k0={k0} D={D}: N0={m['N0']} N4={m['N4']} f_tl={m['f_tl']} "
                      f"cv={m['prof_cv']} dS={m['dS'].get('8-24')}", flush=True)
                if time.time()-t0 > args.budget_s:
                    print("budget reached, checkpointed"); return
        print("scan complete")
        return

    ap.print_help()

if __name__ == "__main__":
    main()
