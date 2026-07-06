#!/usr/bin/env python3
"""Ring-bootstrap power-law fit of Var_c[dQ](t) over a lag window.
Precomputes per-ring variances once; each bootstrap replicate resamples rings with
replacement and refits the WLS log-log slope -> slope distribution robust to
lag-lag correlation from overlapping windows."""
import sys, math
import numpy as np
from analyze_q import load

def perring_var(Q, dt, lags):
    """Per-ring connected variance of increments for each lag. Returns (t[], V[nlag, nr])."""
    nsamp = Q.shape[0]
    out_t, rows = [], []
    for lag_sw in lags:
        lag = int(round(lag_sw / dt))
        if lag < 1 or lag >= nsamp - 8:
            continue
        d = Q[lag:, :] - Q[:-lag, :]
        out_t.append(lag * dt)
        rows.append(d.var(axis=0, ddof=1))
    return np.array(out_t), np.vstack(rows)

def slope_ll(t, v):
    x = np.log(t); y = np.log(v)
    A = np.vstack([x, np.ones_like(x)]).T
    m, c = np.linalg.lstsq(A, y, rcond=None)[0]
    return m

def main(fn, tmin, tmax, nboot=2000, seed=5):
    sweeps, Q, dt = load(fn)
    nr = Q.shape[1]
    lags = np.unique(np.round(np.geomspace(tmin, tmax, 10) / dt).astype(int)) * dt
    t, V = perring_var(Q, dt, lags)   # V: (nlag, nr)
    m0 = slope_ll(t, V.mean(axis=1))
    rng = np.random.default_rng(seed)
    ms = []
    for _ in range(nboot):
        idx = rng.integers(0, nr, nr)
        ms.append(slope_ll(t, V[:, idx].mean(axis=1)))
    ms = np.array(ms)
    lo, hi = np.percentile(ms, [16, 84])
    err = 0.5 * (hi - lo)
    print("%s  window [%g, %g]:  slope = %.3f +- %.3f   (boot 68%% CI [%.3f, %.3f], %d rings)"
          % (fn, tmin, tmax, m0, err, lo, hi, nr))
    print("   sigma from EW 1/2: %+.1f    sigma from KPZ 2/3: %+.1f"
          % ((m0 - 0.5) / err, (m0 - 2/3) / err))
    return m0, err

if __name__ == "__main__":
    main(sys.argv[1], float(sys.argv[2]), float(sys.argv[3]))
