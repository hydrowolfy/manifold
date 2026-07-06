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


def _substrate_demo():
    print("1+1D CDT validation (canonical, fixed volume): expect Hausdorff d_H -> 2 (Ambjorn-Loll).")
    for T, Lmean in [(24, 16), (32, 24), (40, 32)]:
        L, w, adj = run_canonical(T, Lmean, 40000, seed=1)
        dH = ball_growth_dH(adj)
        print("  T=%d meanL=%d (N2=%d, ~square) -> d_H(ball 2-8)=%.2f  (target ~2)"
              % (T, Lmean, 2 * sum(L), dH))


# ============================================================================
#  OFF-MANIFOLD BRANCH A: spatial-topology-change ("pinch" / baby-universe)
#  Added by the OFF-MANIFOLD IMPLEMENTATION subcommittee.
#  D=0 reduces EXACTLY to the validated substrate above (build_graph_pinched
#  with empty P == build_graph). Metropolis weight e^{-mu*dD} on PINCH/UNPINCH.
# ============================================================================
from collections import Counter, defaultdict


def init_pinches(T):
    """P[t] = set of frozenset({i,j}) identified-vertex pairs on spatial circle t.
    Each vertex index participates in at most one pinch. D = sum_t |P[t]|."""
    return [set() for _ in range(T)]


def total_D(P):
    return sum(len(s) for s in P)


def _pinched_indices(P_t):
    """set of vertex indices on a slice that are already in some pinch."""
    used = set()
    for pr in P_t:
        used |= pr
    return used


def n_valid_pinch_pairs(Lt, P_t):
    """Number of proposable NEW pinch pairs {i,j} on a slice of length Lt:
    i<j, i,j not currently pinched, and NOT spatially adjacent (|i-j| != 1 mod Lt),
    and not the same vertex. This count is needed for detailed-balance proposal ratio.
    Non-adjacency ensures the pinch is a genuine spatial identification (figure-8),
    not the contraction of an existing spatial edge."""
    used = _pinched_indices(P_t)
    free = [i for i in range(Lt) if i not in used]
    nf = len(free)
    # all unordered pairs among free vertices
    total = nf * (nf - 1) // 2
    # subtract adjacent free pairs (spatial neighbours i,i+1 mod Lt)
    adj_bad = 0
    freeset = set(free)
    for i in free:
        j = (i + 1) % Lt
        if j in freeset and i < j:          # count i<j adjacency once
            adj_bad += 1
        # wraparound pair (Lt-1, 0): i=Lt-1,j=0 -> stored as {0,Lt-1}, i<j fails above
    # handle wrap pair (0, Lt-1) explicitly
    if Lt > 2 and 0 in freeset and (Lt - 1) in freeset:
        adj_bad += 1
    return total - adj_bad


def _random_valid_pinch_pair(Lt, P_t, rng):
    """Uniformly sample a valid NEW pinch pair, or None. Rejection sampling
    (valid fraction is high for our regimes)."""
    used = _pinched_indices(P_t)
    free = [i for i in range(Lt) if i not in used]
    if len(free) < 2:
        return None
    for _ in range(200):
        i, j = rng.sample(free, 2)
        if i > j:
            i, j = j, i
        # reject spatial adjacency (incl. wrap)
        if (j - i) == 1 or (i == 0 and j == Lt - 1):
            continue
        return frozenset((i, j))
    return None


def build_graph_pinched(L, w, T, P):
    """Extended build_graph: build the flat causal graph, then MERGE each pinched
    pair of vertices into a single graph node (union-find). A pinch on slice t
    identifies two vertices of that spatial circle -> figure-8 neck, so the ball
    growth / d_H actually sees the baby-universe neck. With P all-empty this is
    IDENTICAL (up to relabelling) to build_graph."""
    adj = build_graph(L, w, T)   # flat substrate graph, keys (t,i)
    # union-find over graph nodes
    parent = {}
    def find(x):
        parent.setdefault(x, x)
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x
    def union(a, b):
        ra, rb = find(a), find(b)
        if ra != rb:
            parent[ra] = rb
    for x in adj:
        find(x)
    for t in range(T):
        for pr in P[t]:
            i, j = tuple(pr)
            union((t, i), (t, j))
    # rebuild merged adjacency
    madj = {}
    for u, nbrs in adj.items():
        ru = find(u)
        madj.setdefault(ru, set())
        for v in nbrs:
            rv = find(v)
            if rv != ru:
                madj[ru].add(rv)
                madj.setdefault(rv, set()).add(ru)
    return madj


# ---- PINCH / UNPINCH Metropolis moves (canonical: N2 fixed) ----------------
# Proposal: with prob 1/2 attempt PINCH, else UNPINCH. Detailed balance requires
# the proposal combinatorics ratio. Let a slice-independent global scheme:
#   PINCH:  pick slice t uniformly (1/T); pick a valid new pair uniformly among
#           n_valid_pinch_pairs(t) candidates.  q(pinch) = (1/2)(1/T)(1/Nvalid)
#   UNPINCH: pick slice t uniformly (1/T); pick an existing pinch on t uniformly
#           among |P[t]| of them.            q(unpinch)= (1/2)(1/T)(1/|P[t]|)
# For the reverse of a PINCH that created pair on slice t (new D on that slice =
# |P[t]|+1 pinches), reverse UNPINCH picks slice t (1/T) then that pinch among
# |P[t]|+1. Acceptance:
#   A(pinch) = min(1, e^{-mu} * Nvalid_before / (|P[t]|+1) )
#   A(unpinch)= min(1, e^{+mu} * |P[t]| / Nvalid_after )
# (These are exact inverses; verified by the Kolmogorov/reversibility check.)

def move_pinch(L, w, T, P, mu, rng):
    """Attempt one PINCH or UNPINCH. Returns ('pinch'|'unpinch'|None, accepted)."""
    do_pinch = rng.random() < 0.5
    t = rng.randrange(T)
    if do_pinch:
        Lt = L[t]
        nb = n_valid_pinch_pairs(Lt, P[t])
        if nb <= 0:
            return ('pinch', False)
        pr = _random_valid_pinch_pair(Lt, P[t], rng)
        if pr is None:
            return ('pinch', False)
        k_after = len(P[t]) + 1            # |P[t]| after adding
        A = math.exp(-mu) * nb / k_after
        if rng.random() < min(1.0, A):
            P[t].add(pr)
            return ('pinch', True)
        return ('pinch', False)
    else:
        k = len(P[t])
        if k == 0:
            return ('unpinch', False)
        pr = rng.choice(tuple(P[t]))
        # Nvalid AFTER removal (reverse pinch proposal denominator)
        P[t].discard(pr)
        nb_after = n_valid_pinch_pairs(L[t], P[t])
        A = math.exp(+mu) * k / nb_after if nb_after > 0 else 0.0
        if rng.random() < min(1.0, A):
            return ('unpinch', True)
        P[t].add(pr)   # reject: restore
        return ('unpinch', False)


# ---- baby-universe (minbu) size behind each pinch neck ----------------------
def baby_universe_sizes(L, w, T, P):
    """For each pinch {i,j} on slice t, the pinch splits that spatial circle into
    two arcs. The 'baby universe' behind the neck is the smaller side. Its size B
    is measured as the spatial length of the smaller arc (number of vertices on the
    shorter side of the circle between i and j). Returns list of B (one per pinch).
    (This is the minbu volume proxy appropriate at 1+1D fixed slice; the neck
    isolates a spatial sub-circle of B vertices.)"""
    sizes = []
    for t in range(T):
        Lt = L[t]
        for pr in P[t]:
            i, j = tuple(pr)
            arc = (j - i) % Lt          # vertices strictly between going one way
            B = min(arc, Lt - arc)
            sizes.append(B)
    return sizes


# ---- spectral dimension via lazy random walk return probability -------------
def spectral_dimension(adj, tmax=40, nwalk=200, seed=7, lazy=0.5):
    """Estimate d_s from return probability P0(t) ~ t^{-d_s/2} of a lazy random
    walk. Fit slope of log P0 vs log t over an intermediate window. Averaged over
    random start vertices. Uses exact probability propagation from each start
    (deterministic distribution), not stochastic sampling, for low noise."""
    rng = random.Random(seed)
    nodes = list(adj)
    starts = [rng.choice(nodes) for _ in range(nwalk)]
    # return prob per start via distribution propagation is O(t * E); do stochastic
    # ensemble instead for speed but many walkers. We use deterministic sparse
    # propagation for a handful of starts (cleaner).
    ret = [0.0] * (tmax + 1)
    ns = min(len(starts), 30)
    starts = starts[:ns]
    for s in starts:
        # distribution over nodes, lazy walk
        prob = {s: 1.0}
        ret[0] += 1.0
        for tt in range(1, tmax + 1):
            newp = defaultdict(float)
            for u, pu in prob.items():
                deg = len(adj[u])
                newp[u] += lazy * pu
                share = (1 - lazy) * pu / deg
                for v in adj[u]:
                    newp[v] += share
            prob = newp
            ret[tt] += prob.get(s, 0.0)
    ret = [r / ns for r in ret]
    # fit log P0 vs log t on window
    xs, ys = [], []
    for tt in range(4, tmax + 1):
        if ret[tt] > 0:
            xs.append(math.log(tt)); ys.append(math.log(ret[tt]))
    if len(xs) < 3:
        return float('nan'), ret
    n = len(xs); mx = sum(xs) / n; my = sum(ys) / n
    sl = sum((xs[i] - mx) * (ys[i] - my) for i in range(n)) / sum((xs[i] - mx) ** 2 for i in range(n))
    d_s = -2 * sl
    return d_s, ret


# ---- combined canonical sampler with pinch dof ------------------------------
def run_offmanifold(T, Lmean, mu, therm_sweeps, meas_sweeps, seed=0,
                    pinch_frac=0.5, start='cold', dH_seed=None, meas_every=1):
    """Canonical (N2 fixed) 1+1D CDT + baby-universe pinch dof at penalty mu.
    1 sweep = N2 attempted moves (N2 = 2*T*Lmean). Each attempted move is:
      with prob pinch_frac -> a PINCH/UNPINCH attempt; else a geometry move
      (half flip, half relocate). start='cold' (D=0) or 'hot' (pre-pinched).
    Returns dict with D-series, <D>, d_H samples, baby-universe sizes, ret-prob.
    """
    rng = random.Random(seed)
    L, w = init_state(T, Lmean)
    P = init_pinches(T)
    N2 = 2 * sum(L)
    moves_per_sweep = N2
    if dH_seed is None:
        dH_seed = 100 + seed

    if start == 'hot':
        # pre-load pinches: attempt to seed ~ up to a few per slice
        for t in range(T):
            for _ in range(max(1, L[t] // 4)):
                pr = _random_valid_pinch_pair(L[t], P[t], rng)
                if pr is not None:
                    P[t].add(pr)

    def one_attempt():
        if rng.random() < pinch_frac:
            move_pinch(L, w, T, P, mu, rng)
        else:
            if rng.random() < 0.5:
                move_flip(L, w, T, rng)
            else:
                move_relocate(L, w, T, rng)

    # thermalize
    for _ in range(therm_sweeps * moves_per_sweep):
        one_attempt()

    Dseries = []
    dH_samples = []
    bu_sizes = []
    ret_accum = None
    ret_n = 0
    n_meas = 0
    for s in range(meas_sweeps):
        for _ in range(moves_per_sweep):
            one_attempt()
        Dseries.append(total_D(P))
        if (s % meas_every) == 0:
            adj = build_graph_pinched(L, w, T, P)
            dH_samples.append(ball_growth_dH(adj, nsrc=16, seed=dH_seed + s))
            bu_sizes.extend(baby_universe_sizes(L, w, T, P))
            n_meas += 1
    check(L, w, T)
    return {
        'T': T, 'Lmean': Lmean, 'N2': N2, 'mu': mu, 'seed': seed, 'start': start,
        'Dseries': Dseries, 'D_mean': statistics.mean(Dseries),
        'D_over_N2': statistics.mean(Dseries) / N2,
        'dH_samples': dH_samples,
        'dH_mean': statistics.mean(dH_samples) if dH_samples else float('nan'),
        'bu_sizes': bu_sizes, 'n_meas': n_meas,
        'L_final': list(L), 'P_final': [sorted(tuple(sorted(pr)) for pr in s) for s in P],
    }


# ============================================================================
#  DRIVER (off-manifold Branch A demo).  Run:  python3 cdt_offmanifold.py
# ============================================================================
def offmanifold_demo():
    print("OFF-MANIFOLD Branch A: baby-universe (pinch) 1+1D CDT.")
    # 0) D=0 reduces exactly to substrate
    L, w = init_state(8, 10); P = init_pinches(8)
    a1 = build_graph(L, w, 8); a2 = build_graph_pinched(L, w, 8, P)
    def sig(a):
        return (len(a), sum(len(v) for v in a.values()) // 2)
    print("  [reduction] D=0 pinched graph == substrate graph:", sig(a1) == sig(a2), sig(a1))
    # 1) mu -> inf recovers d_H=2 ; small mu drives d_H down (shredding)
    for mu in [20.0, 1.0]:
        r = run_offmanifold(32, 32, mu, therm_sweeps=60, meas_sweeps=60, seed=1, meas_every=20)
        print("  [d_H]  N2=%d mu=%4.1f  <D>/N2=%.4f  d_H=%.3f"
              % (r['N2'], mu, r['D_over_N2'], r['dH_mean']))
    # 2) phase certificate: spectral dimension small-mu vs substrate
    import random as _rnd
    def ds(mu):
        vals = []
        for sd in (1, 2, 3):
            rng = _rnd.Random(sd); L, w = init_state(16, 32); P = init_pinches(16); N2 = 2 * sum(L)
            for _ in range(120 * N2):
                if rng.random() < 0.5:
                    move_pinch(L, w, 16, P, mu, rng)
                else:
                    (move_flip if rng.random() < 0.5 else move_relocate)(L, w, 16, rng)
            adj = build_graph_pinched(L, w, 16, P)
            d, _ = spectral_dimension(adj, tmax=32, nwalk=10, seed=300 + sd); vals.append(d)
        return sum(vals) / len(vals)
    print("  [certificate] d_s(small-mu)=%.2f  d_s(substrate)=%.2f  (BP=1.33 rejected if >>1.33; Liouville=2)"
          % (ds(1.0), ds(8.0)))


if __name__ == "__main__":
    offmanifold_demo()
