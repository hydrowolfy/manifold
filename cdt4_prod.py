#!/usr/bin/env python3
"""
cdt4_prod.py -- SELF-CONTAINED (stdlib-only, no networkx) 3+1D causal CDT production
core for the de Sitter (kappa_0, Delta) scan. Bundles verbatim: the validated Causal4
core (cdt4_run.py) extended with the FULL ergodic AJL move set, the exact Kuhn T^4 seed
(cdt4_benchmark.py), and the referee d_H/d_s estimators (tooling/referee_2d_scaling.py).

Move set (all foliation-preserving; each DB-verified by exact round-trip + reverse
delta = -forward, manifold-verified by census bad=0; see cdt4_prod_selftest.py):
  (2,4)/(4,2)  dN0=0    dN4=+/-2   timelike-tet flip
  (3,3)        dN0=0    dN4=0      triangle flip (self-inverse)
  (4,6)/(6,4)  dN0=0    dN4=+/-2   spatial (2,3) flip thru both sandwiches
  (2,8)/(8,2)  dN0=+/-1 dN4=+/-6   spatial-tet vertex insert/remove  [the N0 DOF]

Simplex containers are indexed-sets (O(1) uniform pick + exact live count for the
detailed-balance move-count factors); v2p/tri2tet/edge2tet give O(local) legality.
"""
import itertools, sys, math, random, pickle, os, time, json
from collections import Counter, defaultdict, deque

def FS(x): return frozenset(x)

class IdxSet:
    __slots__ = ("items", "pos")
    def __init__(self): self.items = []; self.pos = {}
    def add(self, x):
        if x in self.pos: return
        self.pos[x] = len(self.items); self.items.append(x)
    def discard(self, x):
        i = self.pos.pop(x, None)
        if i is None: return
        last = self.items.pop()
        if i < len(self.items): self.items[i] = last; self.pos[last] = i
    def __len__(self): return len(self.items)
    def __contains__(self, x): return x in self.pos
    def pick(self, rng): return self.items[rng.randrange(len(self.items))]

class Prod4:
    def __init__(self, T):
        self.T = T
        self.time = {}
        self.pents = set()
        self.tet2pent = defaultdict(set)
        self.edges = Counter(); self.tris = Counter(); self.vcount = Counter()
        self.v2p = defaultdict(set)
        self.tri2tet = defaultdict(set)
        self.edge2tet = defaultdict(set)
        self.S_tet = IdxSet(); self.S_edge = IdxSet(); self.S_tri = IdxSet()
        self.S_stet = IdxSet(); self.S_sedge = IdxSet(); self.S_stri = IdxSet()
        self.S_vert = IdxSet()
        self.n41 = 0; self.n32 = 0
        self.nextv = 0

    def _sp(self, simplex):
        it = iter(simplex); t0 = self.time[next(it)]
        return all(self.time[v] == t0 for v in it)

    def _ptype_raw(self, p):
        ts = sorted(set(self.time[v] for v in p))
        if len(ts) != 2: return None
        a, b = ts
        if b == a + 1: lo = a
        elif a == 0 and b == self.T - 1: lo = b
        else: return None
        return sum(1 for v in p if self.time[v] == lo)
    def ptype(self, p): return self._ptype_raw(p)

    def is_foliated_pent(self, verts):
        ts = set(self.time[v] for v in verts)
        if len(ts) != 2: return False
        a, b = sorted(ts)
        return (b == a + 1) or (a == 0 and b == self.T - 1)

    def add_pent(self, p):
        self.pents.add(p)
        for c in itertools.combinations(sorted(p), 2):
            f = FS(c); m = self.edges[f]; self.edges[f] = m + 1
            if m == 0:
                self.S_edge.add(f)
                if self._sp(f): self.S_sedge.add(f)
        for c in itertools.combinations(sorted(p), 3):
            f = FS(c); m = self.tris[f]; self.tris[f] = m + 1
            if m == 0:
                self.S_tri.add(f)
                if self._sp(f): self.S_stri.add(f)
        for c in itertools.combinations(sorted(p), 4):
            f = FS(c); s = self.tet2pent[f]
            if not s:
                self.S_tet.add(f)
                if self._sp(f): self.S_stet.add(f)
                for tr in itertools.combinations(sorted(f), 3): self.tri2tet[FS(tr)].add(f)
                for ed in itertools.combinations(sorted(f), 2): self.edge2tet[FS(ed)].add(f)
            s.add(p)
            assert len(s) <= 2, "tet in >2 pentachora"
        for v in p:
            self.vcount[v] += 1; self.v2p[v].add(p)
            if self.vcount[v] == 1: self.S_vert.add(v)
        nlo = self._ptype_raw(p)
        if nlo in (1, 4): self.n41 += 1
        elif nlo in (2, 3): self.n32 += 1

    def rem_pent(self, p):
        self.pents.discard(p)
        nlo = self._ptype_raw(p)
        if nlo in (1, 4): self.n41 -= 1
        elif nlo in (2, 3): self.n32 -= 1
        for c in itertools.combinations(sorted(p), 2):
            f = FS(c); self.edges[f] -= 1
            if self.edges[f] == 0:
                del self.edges[f]; self.S_edge.discard(f); self.S_sedge.discard(f)
        for c in itertools.combinations(sorted(p), 3):
            f = FS(c); self.tris[f] -= 1
            if self.tris[f] == 0:
                del self.tris[f]; self.S_tri.discard(f); self.S_stri.discard(f)
        for c in itertools.combinations(sorted(p), 4):
            f = FS(c); s = self.tet2pent[f]; s.discard(p)
            if not s:
                del self.tet2pent[f]; self.S_tet.discard(f); self.S_stet.discard(f)
                for tr in itertools.combinations(sorted(f), 3): self.tri2tet[FS(tr)].discard(f)
                for ed in itertools.combinations(sorted(f), 2): self.edge2tet[FS(ed)].discard(f)
        for v in p:
            self.vcount[v] -= 1; self.v2p[v].discard(p)
            if self.vcount[v] == 0:
                del self.vcount[v]; self.S_vert.discard(v)

    def apply(self, rems, adds):
        for p in rems: self.rem_pent(p)
        for p in adds: self.add_pent(p)

    @property
    def N4(self): return len(self.pents)
    @property
    def N0(self): return len(self.S_vert)

    def census(self):
        bad = sum(1 for s in self.tet2pent.values() if len(s) != 2)
        untyped = sum(1 for p in self.pents if self._ptype_raw(p) is None)
        return bad, untyped

    def recount(self):
        edges = Counter(); tris = Counter(); tets = defaultdict(set); vc = Counter()
        n41 = n32 = 0
        for p in self.pents:
            for c in itertools.combinations(sorted(p), 2): edges[FS(c)] += 1
            for c in itertools.combinations(sorted(p), 3): tris[FS(c)] += 1
            for c in itertools.combinations(sorted(p), 4): tets[FS(c)].add(p)
            for v in p: vc[v] += 1
            nlo = self._ptype_raw(p)
            if nlo in (1, 4): n41 += 1
            elif nlo in (2, 3): n32 += 1
        nsp = lambda ks: sum(1 for f in ks if self._sp(f))
        return dict(n0=len(vc), n1=len(edges), n2=len(tris), n3=len(tets),
                    n1s=nsp(edges), n2s=nsp(tris), n3s=nsp(tets), n41=n41, n32=n32)

    def counters_ok(self):
        r = self.recount()
        cur = dict(n0=len(self.S_vert), n1=len(self.S_edge), n2=len(self.S_tri),
                   n3=len(self.S_tet), n1s=len(self.S_sedge), n2s=len(self.S_stri),
                   n3s=len(self.S_stet), n41=self.n41, n32=self.n32)
        return cur == r, cur, r

    def prop_24(self, tau):
        ps = self.tet2pent.get(tau)
        if ps is None or len(ps) != 2: return None
        p1, p2 = tuple(ps)
        a = next(iter(p1 - tau)); b = next(iter(p2 - tau))
        if a == b or FS((a, b)) in self.edges: return None
        new = [FS({a, b} | set(tri)) for tri in itertools.combinations(sorted(tau), 3)]
        for q in new:
            if len(q) != 5 or q in self.pents or not self.is_foliated_pent(q): return None
        return ([p1, p2], new, ('24', FS((a, b))))

    def prop_42(self, edge):
        a, b = tuple(edge)
        around = list(self.v2p[a] & self.v2p[b])
        if len(around) != 4: return None
        tris = [frozenset(p - {a, b}) for p in around]
        if any(len(t) != 3 for t in tris): return None
        tau = frozenset().union(*tris)
        if len(tau) != 4: return None
        if set(tris) != {frozenset(c) for c in itertools.combinations(sorted(tau), 3)}: return None
        if tau in self.tet2pent: return None
        p1 = FS(tau | {a}); p2 = FS(tau | {b})
        if p1 in self.pents or p2 in self.pents: return None
        if not (self.is_foliated_pent(p1) and self.is_foliated_pent(p2)): return None
        return (around, [p1, p2], ('42', tau))

    def prop_33(self, tri):
        a, b, c = tuple(tri)
        ps = list(self.v2p[a] & self.v2p[b] & self.v2p[c])
        if len(ps) != 3: return None
        extras = [p - tri for p in ps]
        if any(len(e) != 2 for e in extras): return None
        opp = frozenset().union(*extras)
        if len(opp) != 3: return None
        if set(extras) != {FS(cc) for cc in itertools.combinations(sorted(opp), 2)}: return None
        if opp in self.tris: return None
        new = [FS(opp | e) for e in (FS(cc) for cc in itertools.combinations(sorted(tri), 2))]
        for q in new:
            if len(q) != 5 or q in self.pents or not self.is_foliated_pent(q): return None
        return (list(ps), new, ('33', opp))

    def _stet_apex(self, stet):
        ps = self.tet2pent.get(stet)
        if not ps or len(ps) != 2: return None
        t = next(iter(self.time[v] for v in stet)); up = dn = None
        for p in ps:
            ap = next(iter(p - stet)); ta = self.time[ap]
            if ta == (t + 1) % self.T: up = ap
            elif ta == (t - 1) % self.T: dn = ap
        if up is None or dn is None: return None
        return (up, dn, t)

    def prop_46(self, tri):
        if len(tri) != 3: return None
        cofaces = [t for t in self.tri2tet.get(tri, ()) if self._sp(t)]
        if len(cofaces) != 2: return None
        s1, s2 = cofaces
        a1 = self._stet_apex(s1); a2 = self._stet_apex(s2)
        if a1 is None or a2 is None or a1[0] != a2[0] or a1[1] != a2[1]: return None
        w, u = a1[0], a1[1]
        if w == u: return None
        d = next(iter(s1 - tri)); e = next(iter(s2 - tri))
        if d == e or FS((d, e)) in self.edges: return None
        others = [FS(c) for c in itertools.combinations(sorted(tri), 2)]
        rems = [FS(s1 | {w}), FS(s2 | {w}), FS(s1 | {u}), FS(s2 | {u})]
        for p in rems:
            if p not in self.pents: return None
        adds = []
        for o in others:
            ns = FS(o | {d, e}); adds += [FS(ns | {w}), FS(ns | {u})]
        for q in adds:
            if len(q) != 5 or q in self.pents or not self.is_foliated_pent(q): return None
        return (rems, adds, ('46', FS((d, e))))

    def prop_64(self, edge):
        if len(edge) != 2: return None
        d, e = tuple(edge)
        stets = [t for t in self.edge2tet.get(edge, ()) if self._sp(t)]
        if len(stets) != 3: return None
        opp = frozenset().union(*[s - edge for s in stets])
        if len(opp) != 3: return None
        if {frozenset(s - edge) for s in stets} != {FS(c) for c in itertools.combinations(sorted(opp), 2)}:
            return None
        tri = opp
        if tri in self.tris: return None
        apex = [self._stet_apex(s) for s in stets]
        if any(a is None for a in apex): return None
        if len({a[0] for a in apex}) != 1 or len({a[1] for a in apex}) != 1: return None
        w = apex[0][0]; u = apex[0][1]
        if w == u: return None
        rems = []
        for s in stets: rems += [FS(s | {w}), FS(s | {u})]
        ns1 = FS(tri | {d}); ns2 = FS(tri | {e})
        if ns1 in self.tet2pent or ns2 in self.tet2pent: return None
        adds = [FS(ns1 | {w}), FS(ns2 | {w}), FS(ns1 | {u}), FS(ns2 | {u})]
        for q in adds:
            if len(q) != 5 or q in self.pents or not self.is_foliated_pent(q): return None
        return (rems, adds, ('64', tri))

    def prop_28(self, stet):
        ps = self.tet2pent.get(stet)
        if ps is None or len(ps) != 2 or not self._sp(stet): return None
        t = next(iter(self.time[v] for v in stet)); up = dn = None
        for p in ps:
            ap = next(iter(p - stet)); ta = self.time[ap]
            if ta == (t + 1) % self.T: up = (p, ap)
            elif ta == (t - 1) % self.T: dn = (p, ap)
        if up is None or dn is None or up[1] == dn[1]: return None
        w, u = up[1], dn[1]; x = self.nextv
        self.time[x] = t
        subs = [FS({x} | (stet - {v})) for v in stet]
        adds = []
        for s4 in subs: adds += [FS(s4 | {w}), FS(s4 | {u})]
        for q in adds:
            if len(q) != 5 or q in self.pents or not self.is_foliated_pent(q):
                del self.time[x]; return None
        return ([up[0], dn[0]], adds, ('28', x))

    def _match_82(self, x, ps):
        nbrs = set()
        for p in ps: nbrs |= (p - {x})
        if len(nbrs) != 6: return None
        tx = self.time[x]
        same = [v for v in nbrs if self.time[v] == tx]
        up = [v for v in nbrs if self.time[v] == (tx + 1) % self.T]
        dn = [v for v in nbrs if self.time[v] == (tx - 1) % self.T]
        if len(same) != 4 or len(up) != 1 or len(dn) != 1: return None
        w = up[0]; u = dn[0]; stet = FS(same)
        subs = [FS({x} | (stet - {v})) for v in stet]
        want = set()
        for s4 in subs: want |= {FS(s4 | {w}), FS(s4 | {u})}
        if set(ps) != want: return None
        if stet in self.tet2pent: return None
        p_up = FS(stet | {w}); p_dn = FS(stet | {u})
        if p_up in self.pents or p_dn in self.pents: return None
        return (stet, w, u, p_up, p_dn)

    def prop_82(self, x):
        ps = list(self.v2p.get(x, ()))
        if len(ps) != 8: return None
        info = self._match_82(x, ps)
        if info is None: return None
        return (ps, [info[3], info[4]], ('82', x))

def kuhn_T4(m):
    E = [(1,0,0,0),(0,1,0,0),(0,0,1,0),(0,0,0,1)]
    def add(a, b): return tuple((a[i]+b[i]) % m for i in range(4))
    simplices = []
    for base in itertools.product(range(m), repeat=4):
        for perm in itertools.permutations(range(4)):
            v = base; verts = [v]
            for ax in perm:
                v = add(v, E[ax]); verts.append(v)
            fs = frozenset(verts); assert len(fs) == 5
            simplices.append(fs)
    return simplices

def seed_flat(m):
    simplices = kuhn_T4(m)
    verts = sorted({v for s in simplices for v in s})
    relab = {v: i for i, v in enumerate(verts)}
    st = Prod4(T=m); st.nextv = len(verts)
    for v, i in relab.items(): st.time[i] = v[3]
    for s in simplices: st.add_pent(FS(relab[v] for v in s))
    return st

def slice_profile(st):
    prof = Counter()
    for tet in st.S_stet.items:
        prof[next(iter(st.time[v] for v in tet))] += 1
    return [prof.get(t, 0) for t in range(st.T)]

def _bfs_dist(adj, s):
    dist = {s: 0}; q = deque([s])
    while q:
        u = q.popleft()
        for v in adj[u]:
            if v not in dist: dist[v] = dist[u] + 1; q.append(v)
    return dist

def _slope(xs, ys):
    n = len(xs)
    if n < 2: return float("nan")
    mx = sum(xs)/n; my = sum(ys)/n
    den = sum((x-mx)**2 for x in xs)
    if den == 0: return float("nan")
    return sum((xs[i]-mx)*(ys[i]-my) for i in range(n))/den

def ball_growth_dim(adj, windows=((2,6),(3,8)), nsrc=14, seed=1):
    rng = random.Random(seed); nodes = list(adj.keys())
    accum = defaultdict(float); cnt = defaultdict(int)
    for _ in range(nsrc):
        s = rng.choice(nodes); dist = _bfs_dist(adj, s)
        shell = Counter(dist.values()); rmax = max(dist.values()); cum = 0
        for r in range(0, rmax+1):
            cum += shell.get(r, 0); accum[r] += cum; cnt[r] += 1
    res = {}
    for (lo, hi) in windows:
        xs, ys = [], []
        for r in range(lo, hi+1):
            if cnt.get(r, 0) == 0: continue
            xs.append(math.log(r)); ys.append(math.log(accum[r]/cnt[r]))
        res["%d-%d" % (lo, hi)] = round(_slope(xs, ys), 4) if len(xs) >= 2 else None
    return res

def lazy_rw_sdim(adj, windows=((8,24),(10,30)), nz=6, tmax=40, seed=2):
    rng = random.Random(seed); nodes = list(adj.keys())
    idx = {u: i for i, u in enumerate(nodes)}; N = len(nodes)
    nbr = [[idx[v] for v in adj[u]] for u in nodes]
    deg = [len(nbr[i]) for i in range(N)]
    P = {t: 0.0 for t in range(1, tmax+1)}
    for _ in range(nz):
        z = [1.0 if rng.random() < 0.5 else -1.0 for _ in range(N)]; w = z[:]
        for t in range(1, tmax+1):
            nw = [0.0]*N
            for i in range(N):
                if deg[i] == 0: nw[i] = w[i]; continue
                s = 0.0
                for j in nbr[i]: s += w[j]
                nw[i] = 0.5*(w[i] + s/deg[i])
            w = nw
            P[t] += sum(z[i]*w[i] for i in range(N))/N
    for t in P: P[t] /= nz
    res = {}
    for (lo, hi) in windows:
        xs, ys = [], []
        for t in range(lo, hi+1):
            if P.get(t, 0) > 0: xs.append(math.log(t)); ys.append(math.log(P[t]))
        res["%d-%d" % (lo, hi)] = round(-2*_slope(xs, ys), 4) if len(xs) >= 2 else None
    return res

def skeleton_adj(st):
    adj = defaultdict(set)
    for e in st.edges:
        a, b = tuple(e); adj[a].add(b); adj[b].add(a)
    return {k: set(v) for k, v in adj.items()}

if __name__ == "__main__":
    print("cdt4_prod.py core loaded (metropolis CLI in cdt4_scan.py).")
