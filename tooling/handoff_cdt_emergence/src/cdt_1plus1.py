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
