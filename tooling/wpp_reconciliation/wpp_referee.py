#!/usr/bin/env python3
"""WPP reconciliation: evolve documented Wolfram-model rules with RANDOM sequential updating,
track the event DAG, and run this program's referee suite on the result.

Rules (exact, from the WPP registry, init {{1,1,1},{1,1,1}}):
  R1 wm7714: {{x,y,y},{z,x,w}} -> {{y,n,y},{y,z,n},{w,n,n}}   (n fresh)
  R2 wm8619: {{x,y,y},{x,z,w}} -> {{w,n,n},{n,z,y},{x,y,n}}   (n fresh)
  C1 tree  : {{x,y}} -> {{x,y},{y,z}}                          (z fresh)

Referee suite: d_H (ball growth), d_s (return probability peak), diameter vs N, p_max,
link census (skeleton-link single-cycle = closed-2-manifold certificate; path = boundary),
causal-DAG longest-chain height vs events.

Modes: selftest | R1 <seed> <ck...> | R2 <seed> <ck...> | C1 <seed> <ck...> | R1gen <ck...> | R2gen <ck...>
"""
import sys, math, random
from collections import deque, defaultdict


class WM23:
    """Random-sequential evolution for the two registry rules. Edge = (a,b,c) ternary.
    R1: A=(x,y,y), B=(z,x,w) share x=A[0]=B[1]; RHS=[(y,n,y),(y,z,n),(w,n,n)]
    R2: A=(x,y,y), B=(x,z,w) share x=A[0]=B[0]; RHS=[(w,n,n),(n,z,y),(x,y,n)]
    Event DAG: each edge carries the id of its creator event (0 = initial)."""

    def __init__(self, rule, seed=0):
        self.rule = rule
        self.rng = random.Random(seed)
        self.next_v = 2
        self.edges = {}
        self.next_e = 0
        self.next_ev = 1
        self.ev_depth = {0: 0}
        self.yy = set()
        self.by_elem = defaultdict(set)
        for t in [(1, 1, 1), (1, 1, 1)]:
            self._add(t, 0)

    def _add(self, t, ev):
        eid = self.next_e; self.next_e += 1
        self.edges[eid] = (t, ev)
        if t[1] == t[2]:
            self.yy.add(eid)
        for x in set(t):
            self.by_elem[x].add(eid)
        return eid

    def _rm(self, eid):
        t, _ = self.edges.pop(eid)
        self.yy.discard(eid)
        for x in set(t):
            s = self.by_elem[x]; s.discard(eid)
            if not s: del self.by_elem[x]

    def _apply(self, aid, bid):
        ta, eva = self.edges[aid]; tb, evb = self.edges[bid]
        x, y = ta[0], ta[1]
        n = self.next_v; self.next_v += 1
        ev = self.next_ev; self.next_ev += 1
        self.ev_depth[ev] = 1 + max(self.ev_depth[eva], self.ev_depth[evb])
        if self.rule == 'R1':
            z, w = tb[0], tb[2]
            rhs = [(y, n, y), (y, z, n), (w, n, n)]
        else:
            z, w = tb[1], tb[2]
            rhs = [(w, n, n), (n, z, y), (x, y, n)]
        self._rm(aid); self._rm(bid)
        for t in rhs: self._add(t, ev)

    def step(self):
        rng = self.rng
        for _ in range(64):
            if not self.yy: return False
            aid = rng.choice(tuple(self.yy))
            ta, _ = self.edges[aid]
            x = ta[0]
            cands = []
            for bid in self.by_elem.get(x, ()):
                if bid == aid: continue
                tb, _ = self.edges[bid]
                if (self.rule == 'R1' and tb[1] == x) or (self.rule == 'R2' and tb[0] == x):
                    cands.append(bid)
            if not cands: continue
            self._apply(aid, rng.choice(cands))
            return True
        return False

    def gen_sweep(self):
        """One GENERATION in Wolfram's default (standard) updating order: scan edges
        oldest-first, greedily apply non-overlapping matches within the generation
        snapshot (B = oldest compatible partner). Returns events applied."""
        applied = 0
        consumed = set()
        snapshot = sorted(self.edges.keys())
        snapset = set(snapshot)
        for aid in snapshot:
            if aid in consumed or aid not in self.edges: continue
            ta, _ = self.edges[aid]
            if ta[1] != ta[2]: continue
            x = ta[0]
            best = None
            for bid in sorted(self.by_elem.get(x, ())):
                if bid == aid or bid in consumed or bid not in snapset: continue
                tb2 = self.edges.get(bid)
                if tb2 is None: continue
                tb = tb2[0]
                if (self.rule == 'R1' and tb[1] == x) or (self.rule == 'R2' and tb[0] == x):
                    best = bid; break
            if best is None: continue
            consumed.add(aid); consumed.add(best)
            self._apply(aid, best)
            applied += 1
        return applied

    def n_vertices(self):
        return len(self.by_elem)

    def skeleton(self):
        adj = defaultdict(set)
        for t, _ in self.edges.values():
            a, b, c = t
            for u, v in ((a, b), (b, c), (a, c)):
                if u != v:
                    adj[u].add(v); adj[v].add(u)
        return adj

    def dag_height(self):
        return max(self.ev_depth.values())


class TreeRule:
    """C1: {{x,y}} -> {{x,y},{y,z}}, random sequential; edge=(a,b)."""
    def __init__(self, seed=0):
        self.rng = random.Random(seed)
        self.edges = [(1, 2)]
        self.next_v = 3
        self.depth = [0]

    def step(self):
        i = self.rng.randrange(len(self.edges))
        a, b = self.edges[i]
        z = self.next_v; self.next_v += 1
        d = self.depth[i] + 1
        self.edges.append((b, z)); self.depth.append(d)
        return True

    def n_vertices(self): return self.next_v - 1

    def skeleton(self):
        adj = defaultdict(set)
        for a, b in self.edges:
            if a != b: adj[a].add(b); adj[b].add(a)
        return adj

    def dag_height(self): return max(self.depth)

    @property
    def next_ev(self): return len(self.edges)


def bfs_dists(adj, src, cap=None):
    dist = {src: 0}; q = deque([src])
    while q:
        u = q.popleft()
        if cap is not None and dist[u] >= cap: continue
        for v in adj[u]:
            if v not in dist:
                dist[v] = dist[u] + 1; q.append(v)
    return dist

def ball_dH(adj, nsrc=24, rlo=2, rhi=8, seed=3):
    rng = random.Random(seed); nodes = list(adj)
    acc = defaultdict(float); cnt = defaultdict(int)
    for _ in range(nsrc):
        dist = bfs_dists(adj, rng.choice(nodes), cap=rhi + 2)
        sh = defaultdict(int)
        for d in dist.values(): sh[d] += 1
        cum = 0; rmax = max(dist.values())
        for r in range(min(rmax, rhi + 2) + 1):
            cum += sh.get(r, 0); acc[r] += cum; cnt[r] += 1
    xs, ys = [], []
    for r in range(rlo, rhi + 1):
        if cnt.get(r) and acc[r] > 0:
            xs.append(math.log(r)); ys.append(math.log(acc[r] / cnt[r]))
    if len(xs) < 3: return float('nan')
    n = len(xs); mx = sum(xs)/n; my = sum(ys)/n
    return sum((xs[i]-mx)*(ys[i]-my) for i in range(n)) / sum((x-mx)**2 for x in xs)

def spectral_ds(adj, nsrc=20, smax=40, seed=5):
    rng = random.Random(seed); nodes = list(adj)
    P = [0.0]*(smax+1)
    for _ in range(nsrc):
        src = rng.choice(nodes)
        p = {src: 1.0}
        for s in range(1, smax+1):
            np_ = defaultdict(float)
            for u, pu in p.items():
                if pu < 1e-12: continue
                deg = len(adj[u])
                np_[u] += 0.5*pu
                w = 0.5*pu/deg
                for v in adj[u]: np_[v] += w
            p = np_
            P[s] += p.get(src, 0.0)
    ds = {}
    for s in range(2, smax):
        p1, p2 = P[s-1]/nsrc, P[s+1]/nsrc
        if p1 > 0 and p2 > 0:
            ds[s] = -2.0*(math.log(p2)-math.log(p1))/(math.log(s+1)-math.log(s-1))
    if not ds: return float('nan'), {}
    return max(ds.values()), ds

def diameter_est(adj, nsweep=4, seed=7):
    rng = random.Random(seed); nodes = list(adj)
    best = 0
    for _ in range(nsweep):
        d1 = bfs_dists(adj, rng.choice(nodes))
        far = max(d1, key=d1.get)
        d2 = bfs_dists(adj, far)
        best = max(best, max(d2.values()))
    return best

def link_census(adj, sample=2000, seed=9):
    rng = random.Random(seed); nodes = list(adj)
    if len(nodes) > sample: nodes = rng.sample(nodes, sample)
    cyc = pth = oth = 0
    for v in nodes:
        nb = adj[v]
        if len(nb) < 2: oth += 1; continue
        deg = {u: len(adj[u] & nb) for u in nb}
        d1 = sum(1 for k in deg.values() if k == 1)
        d2 = sum(1 for k in deg.values() if k == 2)
        if d1 + d2 != len(deg):
            oth += 1; continue
        start = next(iter(nb)); seen = {start}; q = deque([start])
        while q:
            u = q.popleft()
            for w in adj[u] & nb:
                if w not in seen: seen.add(w); q.append(w)
        if len(seen) != len(nb): oth += 1; continue
        if d1 == 0: cyc += 1
        elif d1 == 2: pth += 1
        else: oth += 1
    n = len(nodes)
    return cyc/n, pth/n, oth/n

def pmax(adj):
    return max(len(s) for s in adj.values())

def suite(adj, label, events=None, height=None):
    dH = ball_dH(adj)
    ds_pk, _ = spectral_ds(adj)
    diam = diameter_est(adj)
    fc, fp, fo = link_census(adj)
    N = len(adj)
    out = ("%s: N=%d  d_H=%.2f  ds_peak=%.2f  diam=%d  p_max=%d  link[cycle=%.3f path=%.3f other=%.3f]"
           % (label, N, dH, ds_pk, diam, pmax(adj), fc, fp, fo))
    if events is not None and events > 1:
        out += "  events=%d chain_height=%d (h/E^(1/2)=%.2f, h/logE=%.1f)" % (
            events, height, height/math.sqrt(events), height/math.log(events))
    print(out); sys.stdout.flush()
    return dict(N=N, dH=dH, ds=ds_pk, diam=diam, pmax=pmax(adj), link=(fc, fp, fo))


def torus_grid(L):
    adj = defaultdict(set)
    for i in range(L):
        for j in range(L):
            v = (i, j)
            for di, dj in ((1, 0), (0, 1), (1, 1)):
                u = ((i+di) % L, (j+dj) % L)
                adj[v].add(u); adj[u].add(v)
    return adj

def binary_tree(depth):
    adj = defaultdict(set)
    for v in range(1, 2**depth):
        if 2*v < 2**(depth+1)-1:
            adj[v].add(2*v); adj[2*v].add(v)
            adj[v].add(2*v+1); adj[2*v+1].add(v)
    return adj

def random_cubic(n, seed=1):
    rng = random.Random(seed)
    stubs = list(range(n))*3
    while True:
        rng.shuffle(stubs)
        adj = defaultdict(set); ok = True
        for i in range(0, len(stubs), 2):
            a, b = stubs[i], stubs[i+1]
            if a == b or b in adj[a]: ok = False; break
            adj[a].add(b); adj[b].add(a)
        if ok: return adj

def selftest():
    print("== selftests ==")
    r = suite(torus_grid(40), "torus_grid_40  (expect dH~2 ds~2 diam~L links all cycle)")
    assert 1.6 < r['dH'] < 2.4 and 1.6 < r['ds'] < 2.4 and r['link'][0] > 0.99, "torus selftest FAIL"
    r = suite(binary_tree(12), "binary_tree_12 (expect links other)")
    assert r['link'][0] < 0.01, "tree selftest FAIL"
    r = suite(random_cubic(3000), "random_cubic_3k (expander: log diam, links other)")
    assert r['diam'] < 20 and r['link'][0] < 0.05, "expander selftest FAIL"
    print("selftests PASS")


def run_rule(rule, seed, checkpoints):
    m = WM23(rule, seed=seed) if rule in ('R1', 'R2') else TreeRule(seed=seed)
    for ck in checkpoints:
        while m.n_vertices() < ck:
            if not m.step():
                print("  [%s s%d] STUCK at N=%d" % (rule, seed, m.n_vertices())); break
        suite(m.skeleton(), "%s s%d" % (rule, seed), events=m.next_ev - 1, height=m.dag_height())

if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else 'selftest'
    if mode == 'selftest':
        selftest()
    elif mode.endswith('gen'):
        rule = mode[:2]
        cks = [int(x) for x in sys.argv[2:]] or [1000, 2000, 4000]
        m = WM23(rule, seed=0)
        for ck in cks:
            while m.n_vertices() < ck:
                if m.gen_sweep() == 0:
                    print("  [%sgen] no matches; stopped at N=%d" % (rule, m.n_vertices())); break
            suite(m.skeleton(), "%s GEN" % rule, events=m.next_ev - 1, height=m.dag_height())
    else:
        rule = mode
        seed = int(sys.argv[2]) if len(sys.argv) > 2 else 1
        cks = [int(x) for x in sys.argv[3:]] or [1000, 2000, 4000, 8000, 16000]
        run_rule(rule, seed, cks)
