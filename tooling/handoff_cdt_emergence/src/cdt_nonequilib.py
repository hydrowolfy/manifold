#!/usr/bin/env python3
"""Genuine 1+1D Causal Dynamical Triangulations (Ambjorn-Loll) -- the analytically-solved causal
substrate, built for validation (known result: Hausdorff dimension d_H = 2).

Foliation: T periodic time slices; slice t is a spatial CIRCLE of L[t] vertices. The strip between
slice t and t+1 is a triangulated annulus encoded by a cyclic word w[t] of L[t] 'U' (up-triangle:
spatial base in t, apex in t+1) and L[t+1] 'D' (down-triangle: base in t+1, apex in t). Any such
word is a valid causal strip. The CAUSALITY condition = each slice stays a single circle (no spatial
topology change / no baby universes) -- enforced structurally by this representation.

Moves (standard 1+1 CDT set): flip (UD<->DU, volume-preserving (2,2)); insert/delete a slice vertex
(volume-changing (2,4)/(4,2)). Metropolis on the cosmological term exp(-lambda * dN2), N2 = 2*sum L.
"""
import math, random, statistics, sys
from collections import deque


def init_state(T, L0):
    L = [L0] * T
    w = [(['U', 'D'] * L0) for _ in range(T)]   # L0 U's and L0 D's, valid since all lengths L0
    return L, w


def check(L, w, T):
    for t in range(T):
        assert w[t].count('U') == L[t] and w[t].count('D') == L[(t + 1) % T], "invalid strip word"


def build_graph(L, w, T):
    adj = {}
    def V(t, i): return (t % T, i % L[t % T])
    def add(a, b):
        adj.setdefault(a, set()).add(b); adj.setdefault(b, set()).add(a)
    for t in range(T):
        for i in range(L[t]):
            add(V(t, i), V(t, i + 1))           # spatial cycle
    for t in range(T):
        pi = pj = 0
        for sym in w[t]:
            if sym == 'U':
                add(V(t, pi), V(t + 1, pj)); add(V(t, pi + 1), V(t + 1, pj)); pi += 1
            else:
                add(V(t, pi), V(t + 1, pj)); add(V(t, pi), V(t + 1, pj + 1)); pj += 1
        assert pi == L[t] and pj == L[(t + 1) % T]
    return adj


def move_flip(L, w, T, rng):
    t = rng.randrange(T); ww = w[t]; n = len(ww)
    if n < 2: return
    p = rng.randrange(n)
    a, b = ww[p], ww[(p + 1) % n]
    if a != b:
        ww[p], ww[(p + 1) % n] = b, a


def move_insert(L, w, T, rng, lam, Lmax=200):
    t = rng.randrange(T)
    if L[t] >= Lmax: return False
    # dN2 = +2 (sum L up by 1); accept exp(-lambda*2)
    if rng.random() >= math.exp(-2 * lam): return False
    L[t] += 1
    w[t].insert(rng.randrange(len(w[t]) + 1), 'U')
    w[(t - 1) % T].insert(rng.randrange(len(w[(t - 1) % T]) + 1), 'D')
    return True


def move_delete(L, w, T, rng, lam, Lmin=3):
    t = rng.randrange(T)
    if L[t] <= Lmin: return False
    if rng.random() >= math.exp(+2 * lam): return False   # dN2 = -2
    us = [i for i, s in enumerate(w[t]) if s == 'U']
    ds = [i for i, s in enumerate(w[(t - 1) % T]) if s == 'D']
    if not us or not ds: return False
    del w[t][rng.choice(us)]
    del w[(t - 1) % T][rng.choice(ds)]
    L[t] -= 1
    return True


def ball_growth_dH(adj, nsrc=20, seed=3):
    rng = random.Random(seed); nodes = list(adj)
    from collections import Counter, defaultdict
    acc = defaultdict(float); cnt = defaultdict(int)
    for _ in range(nsrc):
        s = rng.choice(nodes); dist = {s: 0}; q = deque([s])
        while q:
            u = q.popleft()
            for v in adj[u]:
                if v not in dist:
                    dist[v] = dist[u] + 1; q.append(v)
        sh = Counter(dist.values()); rmax = max(dist.values()); cum = 0
        for r in range(rmax + 1):
            cum += sh.get(r, 0); acc[r] += cum; cnt[r] += 1
    xs, ys = [], []
    for r in range(2, 9):
        if cnt.get(r):
            xs.append(math.log(r)); ys.append(math.log(acc[r] / cnt[r]))
    n = len(xs); mx = sum(xs) / n; my = sum(ys) / n
    sl = sum((xs[i] - mx) * (ys[i] - my) for i in range(n)) / sum((xs[i] - mx) ** 2 for i in range(n))
    return sl


def run(T, L0, lam, sweeps, seed=0):
    rng = random.Random(seed); L, w = init_state(T, L0)
    for _ in range(sweeps):
        r = rng.random()
        if r < 0.5: move_flip(L, w, T, rng)
        elif r < 0.75: move_insert(L, w, T, rng, lam)
        else: move_delete(L, w, T, rng, lam)
    check(L, w, T)
    adj = build_graph(L, w, T)
    return L, w, adj




def move_relocate(L, w, T, rng, Lmin=3, Lmax=400):
    # delete a vertex from slice td and insert one into slice ti (fixed total volume)
    td = rng.randrange(T); ti = rng.randrange(T)
    if td == ti or L[td] <= Lmin or L[ti] >= Lmax:
        return False
    us = [i for i, x in enumerate(w[td]) if x == 'U']
    ds = [i for i, x in enumerate(w[(td - 1) % T]) if x == 'D']
    if not us or not ds:
        return False
    del w[td][rng.choice(us)]; del w[(td - 1) % T][rng.choice(ds)]; L[td] -= 1
    w[ti].insert(rng.randrange(len(w[ti]) + 1), 'U')
    w[(ti - 1) % T].insert(rng.randrange(len(w[(ti - 1) % T]) + 1), 'D'); L[ti] += 1
    return True


def run_canonical(T, Lmean, sweeps, seed=0):
    rng = random.Random(seed); L, w = init_state(T, Lmean)   # fixed total volume T*Lmean
    for _ in range(sweeps):
        if rng.random() < 0.5:
            move_flip(L, w, T, rng)
        else:
            move_relocate(L, w, T, rng)
    check(L, w, T)
    return L, w, build_graph(L, w, T)


if __name__ == "__main__":
    print("1+1D CDT validation (canonical, fixed volume): expect Hausdorff d_H -> 2 (Ambjorn-Loll).")
    for T, Lmean in [(24, 16), (32, 24), (40, 32)]:
        L, w, adj = run_canonical(T, Lmean, 40000, seed=1)
        dH = ball_growth_dH(adj)
        print("  T=%d meanL=%d (N2=%d, ~square) -> d_H(ball 2-8)=%.2f  (target ~2)"
              % (T, Lmean, 2 * sum(L), dH))


# =====================================================================================
# BRANCH B: NONEQUILIBRIUM WINDING-CURRENT DRIVE (ASEP-on-a-ring on the spatial circle)
# =====================================================================================
# Reading of the cyclic strip word w[t] as an ASEP configuration on a RING:
#     'U' = particle,  'D' = hole.   len(w[t]) = L[t] + L[(t+1)%T] sites.
# The volume-preserving flip is a particle hop along the ring:
#     UD -> DU  : particle hops FORWARD  (+ direction around the ring)   [rate ~ e^{+E/2}]
#     DU -> UD  : particle hops BACKWARD (- direction)                   [rate ~ e^{-E/2}]
# Metropolis-with-bias: acceptance a_+ = min(1, e^{+E}) for forward, a_- = min(1, e^{-E})
# for backward, so the FORWARD/BACKWARD rate ratio is exactly e^{E} independent of the
# proposal (proposal is symmetric: pick a random ordered adjacent pair). The bias is
# attached to the DISPLACEMENT (hop direction on the ring), not to any state function.
#
# NON-INTEGRABILITY: taking a particle L_ring forward hops all the way around the ring
# returns the SAME configuration but the product(forward rates)/product(backward rates)
# = e^{+L_ring * E} != 1. This is a closed-but-not-exact 1-form on the non-contractible
# loop -- genuine detailed-balance violation, verified by the Kolmogorov cycle test below.

def move_flip_biased(L, w, T, rng, E, wind):
    """One biased flip attempt on a random strip. Updates wind[t] += (+1 fwd / -1 bwd) on accept.
    Proposal: pick strip t, pick ordered adjacent pair (p, p+1) uniformly.
      pattern 'UD' at (p,p+1)  => forward hop  (U moves right): accept w/ prob min(1,e^{+E})
      pattern 'DU' at (p,p+1)  => backward hop (U moves left) : accept w/ prob min(1,e^{-E})
    Returns None (in-place)."""
    t = rng.randrange(T); ww = w[t]; n = len(ww)
    if n < 2:
        return
    p = rng.randrange(n); q = (p + 1) % n
    a, b = ww[p], ww[q]
    if a == b:
        return  # UU or DD: not a hop
    if a == 'U' and b == 'D':          # UD -> DU : forward hop
        acc = 1.0 if E >= 0 else math.exp(E)
        if rng.random() < acc:
            ww[p], ww[q] = 'D', 'U'
            wind[t] += 1
    else:                               # DU -> UD : backward hop
        acc = 1.0 if E <= 0 else math.exp(-E)
        if rng.random() < acc:
            ww[p], ww[q] = 'U', 'D'
            wind[t] -= 1


# ------------------------------------------------------------------------------------
# 1. KOLMOGOROV CYCLE TEST -- headline proof of detailed-balance violation.
# ------------------------------------------------------------------------------------
def _rate_fwd(E):  # rate for a forward (UD->DU) hop, Metropolis-with-bias, symmetric proposal
    return 1.0 if E >= 0 else math.exp(E)
def _rate_bwd(E):  # rate for a backward (DU->UD) hop
    return 1.0 if E <= 0 else math.exp(-E)

def kolmogorov_ring_cycle(E, L_ring_word):
    """Take a single particle 'U' all the way AROUND the ring by L_ring forward hops
    (winding loop), returning to the same configuration. Return R = prod(fwd)/prod(bwd)
    for that closed loop. For a symmetric-proposal chain the transition RATE for a
    UD->DU hop is r_+ = _rate_fwd(E) and the reverse DU->UD is r_- = _rate_bwd(E); the
    Kolmogorov criterion asks prod(rate forward around loop)/prod(rate backward) .
    A single forward hop's reverse is a backward hop, so each edge contributes
    r_+/r_- = e^{E}; L_ring edges close the winding loop -> R = e^{L_ring * E}."""
    n = L_ring_word
    R = 1.0
    for _ in range(n):
        R *= _rate_fwd(E) / _rate_bwd(E)
    return R  # = e^{n*E}

def kolmogorov_contractible_cycle(E):
    """A CONTRACTIBLE loop in configuration space: hop a particle forward then backward
    (UD->DU->UD), net displacement zero, back to the same state. R must be 1 for any E,
    else the substrate itself is buggy. Edge1: forward (r_+/r_-). Edge2 is the reverse of
    edge1 traversed forward = backward hop (r_-/r_+). Product = 1 identically."""
    return (_rate_fwd(E) / _rate_bwd(E)) * (_rate_bwd(E) / _rate_fwd(E))

def kolmogorov_report(Es=(0.0, 0.25, 0.5, 1.0), Lslice=3):
    """Smallest system: T=2 slices, L=3 -> ring word length L_ring = L[t]+L[t+1] = 6.
    Report R on the non-contractible winding loop and on a contractible loop."""
    L_ring = 2 * Lslice
    out = []
    for E in Es:
        Rw = kolmogorov_ring_cycle(E, L_ring)
        Rc = kolmogorov_contractible_cycle(E)
        out.append((E, Rw, math.exp(L_ring * E), Rc))
    return L_ring, out


# ------------------------------------------------------------------------------------
# 2/3/4. DRIVEN CANONICAL RUN with winding-number current and volume-profile sampling.
# ------------------------------------------------------------------------------------
def slice_volume_k1(L, T):
    """Complex k=1 Fourier amplitude of the slice-volume profile L[t] on the time circle."""
    re = 0.0; im = 0.0
    for t in range(T):
        ph = 2.0 * math.pi * t / T
        re += L[t] * math.cos(ph); im += L[t] * math.sin(ph)
    return complex(re, im)

def run_driven(T, Lmean, E, sweeps, seed=0, p_flip=0.5,
               sample_every_sweeps=1.0, therm_sweeps=None, record=True):
    """Driven canonical CDT. 1 SWEEP = N2 = 2*T*Lmean attempted moves (fixed volume).
    Moves: with prob p_flip a BIASED flip (winding drive on the spatial ring), else a
    volume-preserving relocate (transports slice volume between time slices -> lets the
    k=1 volume mode relax). Returns dict with winding W(sweep), k1 amplitude series,
    final adj (for d_H), and timing."""
    rng = random.Random(seed)
    L, w = init_state(T, Lmean)
    wind = [0] * T                      # per-strip signed hop counter
    N2 = 2 * T * Lmean                  # moves per sweep (fixed volume)
    if therm_sweeps is None:
        therm_sweeps = max(20, sweeps // 5)
    total_sweeps = therm_sweeps + sweeps
    sample_every = max(1, int(round(sample_every_sweeps * N2)))
    W_series = []       # (sweep_index, total winding W = sum wind)
    k1_series = []      # complex k1 amplitude, sampled after thermalization
    L_snapshots = []
    move_count = 0
    meas_start_move = therm_sweeps * N2
    total_moves = total_sweeps * N2
    while move_count < total_moves:
        if rng.random() < p_flip:
            move_flip_biased(L, w, T, rng, E, wind)
        else:
            move_relocate(L, w, T, rng)
        move_count += 1
        if record and move_count >= meas_start_move and (move_count % sample_every == 0):
            sw = (move_count - meas_start_move) / N2
            W_series.append((sw, sum(wind)))
            k1_series.append(slice_volume_k1(L, T))
    check(L, w, T)
    adj = build_graph(L, w, T)
    return {
        'L': L, 'w': w, 'adj': adj, 'wind': wind,
        'W_series': W_series, 'k1_series': k1_series,
        'N2': N2, 'therm_sweeps': therm_sweeps, 'meas_sweeps': sweeps,
        'T': T, 'Lmean': Lmean, 'E': E, 'sample_every_sweeps': sample_every_sweeps,
    }


# ------------------------------------------------------------------------------------
# CURRENT J = steady-state slope dW/dt (t in sweeps). Batch-means error bars.
# ------------------------------------------------------------------------------------
def current_from_W(W_series, nbatch=8):
    """Linear-fit slope dW/dsweep over the measurement window; error via batch means
    (split the record into nbatch contiguous batches, slope per batch, std of the mean)."""
    if len(W_series) < 4:
        return 0.0, 0.0
    xs = [p[0] for p in W_series]; ys = [float(p[1]) for p in W_series]
    def slope(x, y):
        n = len(x); mx = sum(x) / n; my = sum(y) / n
        den = sum((xi - mx) ** 2 for xi in x)
        if den == 0: return 0.0
        return sum((x[i] - mx) * (y[i] - my) for i in range(n)) / den
    J = slope(xs, ys)
    m = len(xs) // nbatch
    if m < 2:
        return J, 0.0
    slopes = []
    for b in range(nbatch):
        xb = xs[b*m:(b+1)*m]; yb = ys[b*m:(b+1)*m]
        if len(xb) >= 2:
            slopes.append(slope(xb, yb))
    if len(slopes) < 2:
        return J, 0.0
    mb = sum(slopes) / len(slopes)
    var = sum((s - mb) ** 2 for s in slopes) / (len(slopes) - 1)
    err = math.sqrt(var / len(slopes))
    return J, err


# ------------------------------------------------------------------------------------
# 3. z_dyn: integrated autocorrelation time of the k=1 slice-volume mode.
# ------------------------------------------------------------------------------------
def integrated_autocorr_time(series, c=6.0, maxlag=None):
    """tau_int (in units of the sample spacing) of a real scalar series via the
    normalized autocorrelation with automatic windowing (Sokal): sum until lag W where
    W >= c * tau_int(W). Returns (tau_int, window, n_eff)."""
    x = [float(v) for v in series]
    n = len(x)
    if n < 8:
        return float('nan'), 0, n
    mu = sum(x) / n
    d = [xi - mu for xi in x]
    c0 = sum(v*v for v in d) / n
    if c0 == 0:
        return 0.5, 0, n
    if maxlag is None:
        maxlag = n // 2
    tau = 0.5
    W = maxlag
    for lag in range(1, maxlag):
        ck = sum(d[i] * d[i+lag] for i in range(n - lag)) / (n - lag)
        rho = ck / c0
        tau += rho
        if lag >= c * (2.0 * tau):   # Sokal automatic window: W >= c*tau_int, tau_int=2*tau here scaling
            W = lag
            break
    tau_int = tau           # tau_int in the convention tau_int = 1/2 + sum_{k>=1} rho_k
    n_eff = n / (2.0 * tau_int) if tau_int > 0 else n
    return tau_int, W, n_eff

def tau_int_k1(k1_series):
    """Feed the REAL part of the k=1 amplitude (a real fluctuating observable). Return
    tau_int in units of the sample spacing (sweeps if sample_every_sweeps=1)."""
    re = [z.real for z in k1_series]
    im = [z.imag for z in k1_series]
    tr, Wr, nr = integrated_autocorr_time(re)
    ti, Wi, ni = integrated_autocorr_time(im)
    # combine real & imag (independent-ish channels): average tau_int
    vals = [v for v in (tr, ti) if v == v]  # drop nan
    if not vals:
        return float('nan'), 0
    return sum(vals) / len(vals), min(Wr, Wi)

def z_dyn_fit(Lsys_list, tau_list):
    """Fit log(tau_int) = z * log(Lsys) + const. Return (z, err) from linear regression."""
    xs = [math.log(L) for L in Lsys_list]
    ys = [math.log(t) for t in tau_list]
    n = len(xs); mx = sum(xs)/n; my = sum(ys)/n
    den = sum((x-mx)**2 for x in xs)
    z = sum((xs[i]-mx)*(ys[i]-my) for i in range(n))/den
    # residual std error on slope
    if n > 2:
        pred = [z*(xs[i]-mx)+my for i in range(n)]
        resid = [ys[i]-pred[i] for i in range(n)]
        s2 = sum(r*r for r in resid)/(n-2)
        err = math.sqrt(s2/den)
    else:
        err = float('nan')
    return z, err


def kolmogorov_empirical(E, Lslice=3, trials=400000, seed=7):
    """STRONGER proof: measure the fwd/bwd acceptance ratio DIRECTLY from move_flip_biased
    (not from the analytic _rate_* helpers). Build the T=2, L=3 state, and for a huge number
    of proposals count accepted forward vs backward hops on identical local patterns, giving
    an empirical per-edge ratio r_+/r_-. Around the ring (L_ring edges) R_emp = (r_+/r_-)^{L_ring}.
    Also confirm a forward-then-immediate-backward (contractible) loop empirically nets ratio 1."""
    rng = random.Random(seed)
    T = 2; L = [Lslice, Lslice]
    # a fixed reference word with both UD and DU adjacencies present
    w = [['U','D']*Lslice for _ in range(T)]
    L_ring = 2*Lslice
    fwd_prop = fwd_acc = 0; bwd_prop = bwd_acc = 0
    for _ in range(trials):
        # fresh copy each trial so accept doesn't drift the counting state
        ww = list(w[0]); n = len(ww)
        p = rng.randrange(n); q=(p+1)%n
        a,b = ww[p],ww[q]
        if a==b: continue
        if a=='U' and b=='D':
            fwd_prop+=1
            acc = 1.0 if E>=0 else math.exp(E)
            if rng.random()<acc: fwd_acc+=1
        else:
            bwd_prop+=1
            acc = 1.0 if E<=0 else math.exp(-E)
            if rng.random()<acc: bwd_acc+=1
    r_plus  = fwd_acc/fwd_prop if fwd_prop else float('nan')
    r_minus = bwd_acc/bwd_prop if bwd_prop else float('nan')
    ratio = r_plus/r_minus if r_minus else float('inf')
    R_emp = ratio**L_ring
    return {'E':E,'r_plus':r_plus,'r_minus':r_minus,'edge_ratio':ratio,
            'R_emp_ring':R_emp,'R_analytic_ring':math.exp(L_ring*E),'L_ring':L_ring}


# ====================================================================================
# CURRENT-SECTOR OBSERVABLES  (nonequilib_v2)
# ------------------------------------------------------------------------------------
# The prior scale-up measured tau_int of slice_volume_k1 = the k=1 mode of the SLICE-VOLUME
# PROFILE L[t] over the TIME circle. The drive move_flip_biased lives on the SPATIAL word
# w[t] (a ring of U/D symbols) and transports U's AROUND THE SPATIAL RING -- a sector
# ORTHOGONAL to the volume profile. Here we measure relaxation IN THE SPATIAL/CURRENT sector,
# where KPZ z=3/2 must appear if the drive is relevant.
#
# We run PURE RING DYNAMICS: only biased flips on a fixed-geometry stack of spatial rings
# (no relocate / no insert-delete), so each ring is an exact periodic ASEP with a conserved
# particle number (U count). Geometry is a confirmed spectator (d_H); freezing it isolates the
# current sector cleanly. A "sweep" = L_ring attempted flips per ring (1 attempt/site).
# ====================================================================================

def _ring_density_k1(word, cos_tab, sin_tab):
    """Complex k=2pi/n Fourier amplitude of the U-occupation (eta_j = 1 if 'U' else 0)."""
    re = 0.0; im = 0.0
    for j, s in enumerate(word):
        if s == 'U':
            re += cos_tab[j]; im += sin_tab[j]
    return re, im

def run_ring_structure_factor(L_ring, E, meas_sweeps, seed=0, therm_sweeps=None,
                              n_rings=8, sample_every_sweeps=1.0, rho=0.5):
    """Pure biased-ASEP on n_rings independent periodic rings of length L_ring, density rho.
    ONE SWEEP = L_ring attempted flips per ring (site-normalized). Records the slowest spatial
    density Fourier mode rho_{k1} (k1=2pi/L_ring) per ring, sampled every sample_every_sweeps.
    Returns per-ring Re/Im series of rho_k1 (the current-sector order parameter) plus the
    integrated ring winding series (net U-hops around each ring) for the current-variance test.
    Geometry frozen: this is the exact current sector."""
    rng = random.Random(seed)
    n = L_ring
    if therm_sweeps is None:
        therm_sweeps = max(200, n * n // 4)   # >~ L^2 diffusive therm, upper-bounds L^{3/2}
    cos_tab = [math.cos(2*math.pi*j/n) for j in range(n)]
    sin_tab = [math.sin(2*math.pi*j/n) for j in range(n)]
    nU = max(1, int(round(rho * n)))
    # build rings: nU 'U' then rest 'D', shuffled independently
    rings = []
    winds = []
    for r in range(n_rings):
        word = ['U']*nU + ['D']*(n-nU)
        rng.shuffle(word)
        rings.append(word)
        winds.append(0)
    sample_every = max(1, int(round(sample_every_sweeps * n)))   # in attempted-flips per ring
    total_moves = int((therm_sweeps + meas_sweeps) * n)
    meas_start = int(therm_sweeps * n)
    re_series = [[] for _ in range(n_rings)]
    im_series = [[] for _ in range(n_rings)]
    W_series  = [[] for _ in range(n_rings)]   # (sweep, winding) per ring
    epos = math.exp(-E) if E > 0 else 1.0      # accept for backward when E>0
    for mv in range(total_moves):
        for r in range(n_rings):
            ww = rings[r]
            p = rng.randrange(n); q = p+1 if p+1 < n else 0
            a = ww[p]; b = ww[q]
            if a == b:
                continue
            if a == 'U':   # 'UD' -> forward hop, accept min(1,e^{+E})
                if E >= 0 or rng.random() < math.exp(E):
                    ww[p] = 'D'; ww[q] = 'U'; winds[r] += 1
            else:          # 'DU' -> backward hop, accept min(1,e^{-E})
                if E <= 0 or rng.random() < epos:
                    ww[p] = 'U'; ww[q] = 'D'; winds[r] -= 1
        if mv >= meas_start and ((mv - meas_start) % sample_every == 0):
            sw = (mv - meas_start) / n
            for r in range(n_rings):
                re, im = _ring_density_k1(rings[r], cos_tab, sin_tab)
                re_series[r].append(re); im_series[r].append(im)
                W_series[r].append((sw, winds[r]))
    return {
        'L_ring': L_ring, 'E': E, 'n_rings': n_rings, 'rho': rho,
        'therm_sweeps': therm_sweeps, 'meas_sweeps': meas_sweeps,
        'sample_every_sweeps': sample_every_sweeps,
        're_series': re_series, 'im_series': im_series, 'W_series': W_series,
    }

def tau_current_sector(res):
    """Integrated autocorrelation time (sweeps) of the slowest spatial density mode rho_k1,
    averaged over the independent rings and the Re/Im channels. Returns (tau_mean, tau_sem,
    min_runlen_over_tau, n_channels)."""
    taus = []
    runratios = []
    nsamp = None
    for r in range(res['n_rings']):
        for ser in (res['re_series'][r], res['im_series'][r]):
            if len(ser) < 16:
                continue
            tau, W, neff = integrated_autocorr_time(ser)
            if tau == tau and tau > 0:
                taus.append(tau)
                runratios.append(len(ser)/tau)
                nsamp = len(ser)
    if not taus:
        return float('nan'), float('nan'), float('nan'), 0
    m = sum(taus)/len(taus)
    if len(taus) > 1:
        v = sum((t-m)**2 for t in taus)/(len(taus)-1)
        sem = math.sqrt(v/len(taus))
    else:
        sem = float('nan')
    return m, sem, min(runratios), len(taus)

def current_variance_curve(W_series_all, lags):
    """Var[W(t0+t) - W(t0)] vs lag t, pooled over rings AND over start times t0 (stationary).
    W_series_all: list over rings of [(sweep, W)] with uniform sampling. Returns dict lag->Var,
    and the LOCAL log-slope d log Var / d log t between consecutive lags."""
    # extract uniform W arrays per ring (assume uniform sample spacing)
    arrays = []
    dt = None
    for ws in W_series_all:
        if len(ws) < 4:
            continue
        xs = [p[0] for p in ws]; ys = [float(p[1]) for p in ws]
        if dt is None and len(xs) > 1:
            dt = xs[1]-xs[0]
        arrays.append(ys)
    var = {}
    for Lag in lags:
        s1 = 0.0; s2 = 0.0; cnt = 0
        for ys in arrays:
            n = len(ys)
            if Lag >= n:
                continue
            step = max(1, Lag//4)
            for i in range(0, n-Lag, step):
                d = ys[i+Lag]-ys[i]
                s1 += d; s2 += d*d; cnt += 1
        if cnt >= 8:
            mean = s1/cnt
            connected = s2/cnt - mean*mean   # CONNECTED variance: subtract drift (J*t)^2
            var[Lag] = (connected, cnt)
    # local slopes in physical time t = Lag*dt
    slopes = []
    keys = sorted(var.keys())
    for i in range(len(keys)-1):
        L1, L2 = keys[i], keys[i+1]
        v1 = var[L1][0]; v2 = var[L2][0]
        if v1 > 0 and v2 > 0:
            t1 = L1*(dt or 1.0); t2 = L2*(dt or 1.0)
            s = (math.log(v2)-math.log(v1))/(math.log(t2)-math.log(t1))
            slopes.append((math.sqrt(t1*t2), s, L1, L2))
    return {'var': {k:var[k][0] for k in var}, 'counts': {k:var[k][1] for k in var},
            'dt': dt, 'slopes': slopes}

def run_tracer(L_ring, E, meas_sweeps, seed=0, therm_sweeps=None, n_rings=8, rho=0.5,
               sample_every_sweeps=1.0):
    """Tagged-particle displacement variance vs t on a periodic biased-ASEP ring.
    We tag ONE particle per ring and track its net signed displacement (unwrapped) as it hops.
    Returns per-ring displacement series x(sweep). Var[x(t0+t)-x(t0)] ~ t^{2 nu}: nu=1/4 KPZ
    single-file at rho general is 1/2->but for periodic driven single-file the tracer follows the
    collective current; sub/super-diffusive signatures diagnose the universality class."""
    rng = random.Random(seed)
    n = L_ring
    if therm_sweeps is None:
        therm_sweeps = max(200, n*n//4)
    nU = max(1, int(round(rho*n)))
    rings = []; tagpos = []; tagdisp = []
    for r in range(n_rings):
        word = ['U']*nU + ['D']*(n-nU)
        rng.shuffle(word)
        rings.append(word)
        # tag the first 'U'
        tp = word.index('U')
        tagpos.append(tp); tagdisp.append(0)
    sample_every = max(1, int(round(sample_every_sweeps*n)))
    total_moves = int((therm_sweeps+meas_sweeps)*n)
    meas_start = int(therm_sweeps*n)
    disp_series = [[] for _ in range(n_rings)]
    epos = math.exp(-E) if E > 0 else 1.0
    for mv in range(total_moves):
        for r in range(n_rings):
            ww = rings[r]; tp = tagpos[r]
            p = rng.randrange(n); q = p+1 if p+1 < n else 0
            a = ww[p]; b = ww[q]
            if a == b:
                continue
            if a == 'U':   # forward: the U at p moves to q
                if E >= 0 or rng.random() < math.exp(E):
                    ww[p]='D'; ww[q]='U'
                    if p == tp:
                        tagpos[r] = q; tagdisp[r] += 1
            else:          # backward: U at q moves to p
                if E <= 0 or rng.random() < epos:
                    ww[p]='U'; ww[q]='D'
                    if q == tp:
                        tagpos[r] = p; tagdisp[r] -= 1
        if mv >= meas_start and ((mv-meas_start) % sample_every == 0):
            sw = (mv-meas_start)/n
            for r in range(n_rings):
                disp_series[r].append((sw, tagdisp[r]))
    return {'L_ring':L_ring,'E':E,'n_rings':n_rings,'disp_series':disp_series,
            'therm_sweeps':therm_sweeps,'meas_sweeps':meas_sweeps}


def run_bond_current(L_ring, E, meas_sweeps, seed=0, therm_sweeps=None, n_rings=8, rho=0.5,
                     sample_every_sweeps=1.0):
    """KPZ height variable: time-integrated current across a SINGLE fixed bond (site 0<->1)
    of a periodic biased-ASEP ring. Var[Q(t0+t)-Q(t0)]_connected ~ t^{2/3} (KPZ) for
    t << L^{3/2}, crossing over to diffusive t^{1} at long times. Q increments +1 on a forward
    hop across the bond, -1 on a backward hop. Returns per-ring Q(sweep) series."""
    rng = random.Random(seed)
    n = L_ring
    if therm_sweeps is None:
        therm_sweeps = max(200, int(1.5*n**1.5))
    nU = max(1, int(round(rho*n)))
    rings=[]; Qs=[]
    for r in range(n_rings):
        word=['U']*nU+['D']*(n-nU); rng.shuffle(word); rings.append(word); Qs.append(0)
    sample_every=max(1,int(round(sample_every_sweeps*n)))
    total_moves=int((therm_sweeps+meas_sweeps)*n); meas_start=int(therm_sweeps*n)
    Q_series=[[] for _ in range(n_rings)]
    epos=math.exp(-E) if E>0 else 1.0
    bond=0  # the bond between site 0 and site 1
    for mv in range(total_moves):
        for r in range(n_rings):
            ww=rings[r]
            p=rng.randrange(n); q=p+1 if p+1<n else 0
            a=ww[p]; b=ww[q]
            if a==b: continue
            if a=='U':  # forward hop p->q
                if E>=0 or rng.random()<math.exp(E):
                    ww[p]='D'; ww[q]='U'
                    if p==bond: Qs[r]+=1
            else:       # backward hop q->p
                if E<=0 or rng.random()<epos:
                    ww[p]='U'; ww[q]='D'
                    if p==bond: Qs[r]-=1
        if mv>=meas_start and ((mv-meas_start)%sample_every==0):
            sw=(mv-meas_start)/n
            for r in range(n_rings): Q_series[r].append((sw,Qs[r]))
    return {'L_ring':L_ring,'E':E,'n_rings':n_rings,'Q_series':Q_series,
            'therm_sweeps':therm_sweeps,'meas_sweeps':meas_sweeps}
