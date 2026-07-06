#!/usr/bin/env python3
"""Connected variance of bond-current increments vs lag, with local log-slopes.
Var_c[Q(t0+t)-Q(t0)] pooled over start times (stationary) per ring; ring-to-ring
scatter gives the error bar. Slope 1/2 = EW, 2/3 = KPZ, 1 = finite-size diffusive."""
import sys, math
import numpy as np

def load(fn):
    dat = np.loadtxt(fn, comments='#')
    sweeps = dat[:, 0]
    Q = dat[:, 1:]              # (nsamp, n_rings)
    dt = sweeps[1] - sweeps[0]
    return sweeps, Q, dt

def var_curve(Q, dt, lags_sw):
    """lags_sw: lags in sweeps. Returns list of (t, var_mean, var_sem_over_rings, count)."""
    nsamp, nr = Q.shape
    out = []
    for lag_sw in lags_sw:
        lag = int(round(lag_sw / dt))
        if lag < 1 or lag >= nsamp // 2:
            continue
        d = Q[lag:, :] - Q[:-lag, :]          # all start times
        v = d.var(axis=0, ddof=1)             # connected: per-ring mean (drift) subtracted
        vm = v.mean()
        sem = v.std(ddof=1) / math.sqrt(nr) if nr > 1 else float('nan')
        out.append((lag * dt, vm, sem, d.shape[0]))
    return out

def local_slopes(curve):
    sl = []
    for i in range(len(curve) - 1):
        t1, v1, e1, _ = curve[i]
        t2, v2, e2, _ = curve[i + 1]
        if v1 > 0 and v2 > 0:
            s = (math.log(v2) - math.log(v1)) / (math.log(t2) - math.log(t1))
            err = math.sqrt((e1 / v1) ** 2 + (e2 / v2) ** 2) / (math.log(t2) - math.log(t1))
            sl.append((math.sqrt(t1 * t2), s, err))
    return sl

if __name__ == "__main__":
    fn = sys.argv[1]
    tmin = float(sys.argv[2]) if len(sys.argv) > 2 else None
    tmax = float(sys.argv[3]) if len(sys.argv) > 3 else None
    sweeps, Q, dt = load(fn)
    T = sweeps[-1] - sweeps[0]
    if tmin is None: tmin = 2 * dt
    if tmax is None: tmax = T / 4
    lags = np.unique(np.round(np.geomspace(tmin, tmax, 18) / dt).astype(int)) * dt
    curve = var_curve(Q, dt, lags)
    print("# t  Var_c  sem  nstart   (file %s, %d rings, %d samples, dt=%g)"
          % (fn, Q.shape[1], Q.shape[0], dt))
    for t, v, e, c in curve:
        print("%10.1f  %12.4f  %10.4f  %d" % (t, v, e, c))
    print("# local slopes (t_geo, slope, err):")
    for t, s, e in local_slopes(curve):
        print("  t=%9.1f  slope=%.3f +- %.3f" % (t, s, e))
"""NOTE: np.loadtxt is slow on the large raw files; for production analysis load with
pandas.read_csv(fn, sep=' ', comment='#', header=None) and adapt load()."""
