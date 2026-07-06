#!/usr/bin/env python3
"""Tier-1 mining of gate_out/: (1) d_s-peak vs N3 across all replicas with seed errors +
asymptote extrapolation; (2) preregistered de Sitter blob verdict per volume via iterative
cross-correlation registration of raw .snap profiles + cos^2 fit + Poisson-null baseline;
(3) short-scale d_s sanity. gate_register.py referenced in NEXT_SESSION.md does not exist
in the repo; this implements the described method from CONSOLIDATED_REPORT.md section 4.2.
Validated on synthetic controls: recovers a planted wandering cos^2 blob (R2=0.9998,
W/A within 2%); a flat Poisson tube fails (R2=0.42) with registered peak/mean ~1.45.
Usage: gate_mine.py <gate_out_dir> [--snap-stride K]"""
import sys, os, json, glob, math
import numpy as np

def load_jsons(d):
    out = {}
    for fn in sorted(glob.glob(os.path.join(d, 'v*_s*.json'))):
        base = os.path.basename(fn)[:-5]
        v, s = base[1:].split('_s')
        try:
            j = json.load(open(fn))
        except Exception as e:
            print("  [skip] %s: %s" % (base, e)); continue
        out[(int(v), int(s))] = j
    return out

def ds_peak(j):
    ds = j.get('ds_running', {})
    if not ds: return None, None
    items = sorted(((int(k), v) for k, v in ds.items()))
    sig, val = max(items, key=lambda kv: kv[1])
    return val, sig

# ---------- blob machinery ----------
def register_profiles(P, iters=6):
    """P: (nsnap, T) raw slice-volume profiles on a periodic time circle.
    Iterative template registration via circular cross-correlation to a running template."""
    n, T = P.shape
    A = np.empty_like(P)
    for i in range(n):
        shift = T//2 - int(np.argmax(P[i]))
        A[i] = np.roll(P[i], shift)
    templ = A.mean(axis=0)
    for _ in range(iters):
        Fa = np.fft.rfft(P, axis=1)
        Ft = np.conj(np.fft.rfft(templ))
        xc = np.fft.irfft(Fa * Ft[None, :], n=T, axis=1)   # circular cross-correlation
        shifts = (T//2 - np.argmax(xc, axis=1)) % T
        idx = (np.arange(T)[None, :] - shifts[:, None]) % T
        A = P[np.arange(n)[:, None], idx]
        newt = A.mean(axis=0)
        if np.allclose(newt, templ, rtol=1e-6): break
        templ = newt
    return templ, A

def fit_cos2(prof, free_n=False):
    """Fit A*cos(x)^(2p) + stalk B, x=(t-t0)/W, |x|<pi/2; grid search W (and p if free_n).
    Returns dict with A,B,W,p,R2,single_lobe."""
    T = len(prof); t = np.arange(T); c = T/2.0
    best = None
    ns = np.linspace(0.15, 4.0, 40) if free_n else [1.0]
    for p in ns:
        for W in np.linspace(2, T/2.0, 60):
            x = (t - c)/W
            core = np.where(np.abs(x) < math.pi/2, np.cos(np.clip(x, -math.pi/2, math.pi/2))**(2*p), 0.0)
            M = np.vstack([core, np.ones(T)]).T
            coef, *_ = np.linalg.lstsq(M, prof, rcond=None)
            A, B = coef
            pred = M @ coef
            ss = ((prof-pred)**2).sum(); tt = ((prof-prof.mean())**2).sum()
            r2 = 1-ss/tt if tt > 0 else 0
            if best is None or r2 > best['R2']:
                best = {'A': A, 'B': B, 'W': W, 'p': p, 'R2': r2}
    sm = np.convolve(prof, np.ones(3)/3, mode='same')
    thr = sm.min() + 0.5*(sm.max()-sm.min())
    above = sm > thr
    runs = 0
    for i in range(T):
        if above[i] and not above[i-1]: runs += 1
    best['single_lobe'] = (runs == 1)
    return best

def poisson_null_peakmean(prof_mean_level, T, nsnap, rng):
    """peak/mean of a registered average of nsnap uniform-tube Poisson profiles (the
    noise-artifact baseline)."""
    P = rng.poisson(prof_mean_level, size=(nsnap, T)).astype(float)
    templ, A = register_profiles(P, iters=3)
    return templ.max()/templ.mean()

def main():
    d = sys.argv[1]
    stride = 1
    if '--snap-stride' in sys.argv:
        stride = int(sys.argv[sys.argv.index('--snap-stride')+1])
    js = load_jsons(d)
    vols = sorted(set(v for v, s in js))
    print("=== 1. d_s peak vs N3 (all replicas) ===")
    ds_by_vol = {}
    for v in vols:
        vals = []
        for (vv, s), j in sorted(js.items()):
            if vv != v: continue
            pk, sig = ds_peak(j)
            tau = j.get('frac22', float('nan'))
            dh = j.get('dH_fit', float('nan'))
            print("  N3=%5d s%d: ds_peak=%.3f @sigma=%s  dH=%.3f  frac22=%.3f  therm=%d meas=%d"
                  % (v, s, pk, sig, dh, tau, j.get('done_therm', -1), j.get('meas_samples', -1)))
            vals.append(pk)
        ds_by_vol[v] = np.array(vals)
        print("  N3=%5d: ds_peak = %.4f +- %.4f (n=%d seeds)" % (v, np.mean(vals), np.std(vals, ddof=1) if len(vals) > 1 else float('nan'), len(vals)))
    print("\n=== 2. extrapolation: ds_peak(N3) = dinf - c*N3^-a ===")
    x = np.array(vols, float)
    y = np.array([ds_by_vol[v].mean() for v in vols])
    e = np.array([ds_by_vol[v].std(ddof=1)/math.sqrt(len(ds_by_vol[v])) for v in vols])
    best = None
    for a in np.linspace(0.05, 1.5, 300):
        M = np.vstack([np.ones(len(x)), -x**(-a)]).T
        coef, *_ = np.linalg.lstsq(M/e[:, None], y/e, rcond=None)
        dinf, cc = coef
        pred = M @ coef
        chi2 = (((y-pred)/e)**2).sum()
        if best is None or chi2 < best[0]: best = (chi2, a, dinf, cc)
    chi2, a, dinf, cc = best
    print("  free asymptote: d_inf=%.3f, a=%.3f, c=%.2f (chi2=%.2g)" % (dinf, a, cc, chi2))
    best3 = None
    for a in np.linspace(0.05, 1.5, 300):
        num = ((3-y)*x**(-a)/e**2).sum(); den = (x**(-2*a)/e**2).sum()
        ccc = num/den
        chi2 = (((y-(3-ccc*x**(-a)))/e)**2).sum()
        if best3 is None or chi2 < best3[0]: best3 = (chi2, a, ccc)
    chi23, a3, c3 = best3
    print("  fixed d_inf=3 : a=%.3f, c=%.2f, chi2=%.2f -> %s"
          % (a3, c3, chi23, "consistent with ds->3" if chi23 < 4 else "TENSION with ds->3"))
    print("\n=== 3. short-scale d_s (sigma=2-4) per volume ===")
    for v in vols:
        arr = []
        for (vv, s), j in sorted(js.items()):
            if vv != v: continue
            ds = {int(k): val for k, val in j.get('ds_running', {}).items()}
            arr.append([ds.get(2, np.nan), ds.get(3, np.nan), ds.get(4, np.nan)])
        m = np.nanmean(arr, axis=0)
        print("  N3=%5d: ds(2)=%.2f ds(3)=%.2f ds(4)=%.2f  (canonical CDT short-scale ~2)" % (v, *m))
    print("\n=== 4. preregistered blob: registration + cos^2 fit per replica ===")
    rng = np.random.default_rng(11)
    for v in vols:
        r2s, ws, lobes, pms, pnulls, ps = [], [], [], [], [], []
        for (vv, s), j in sorted(js.items()):
            if vv != v: continue
            snapfn = os.path.join(d, 'v%d_s%d.snap' % (v, s))
            if not os.path.exists(snapfn): continue
            try:
                P = np.loadtxt(snapfn, delimiter=',')[::stride]
            except Exception as ex:
                print("  [snap skip] %s: %s" % (snapfn, ex)); continue
            if P.ndim != 2 or len(P) < 50: continue
            templ, _ = register_profiles(P)
            f2 = fit_cos2(templ, free_n=False)
            ff = fit_cos2(templ, free_n=True)
            pm = templ.max()/templ.mean()
            pnull = poisson_null_peakmean(P.mean(), P.shape[1], len(P), rng)
            print("  N3=%5d s%d: cos2 R2=%.3f W=%.1f | free-n R2=%.3f p=%.2f | single_lobe=%s peak/mean=%.2f (Poisson null %.2f)"
                  % (v, s, f2['R2'], f2['W'], ff['R2'], ff['p'], f2['single_lobe'], pm, pnull))
            r2s.append(f2['R2']); ws.append(f2['W']); lobes.append(f2['single_lobe']); pms.append(pm); pnulls.append(pnull); ps.append(ff['p'])
        if r2s:
            print("  N3=%5d SUMMARY: cos2 R2=%.3f+-%.3f  W=%.1f+-%.1f (N3^(1/3)=%.1f)  single-lobe %d/%d  peak/mean %.2f vs null %.2f  free-p=%.2f"
                  % (v, np.mean(r2s), np.std(r2s), np.mean(ws), np.std(ws), v**(1/3),
                     sum(lobes), len(lobes), np.mean(pms), np.mean(pnulls), np.mean(ps)))

if __name__ == "__main__":
    main()
