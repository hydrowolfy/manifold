#!/usr/bin/env python3
"""cdt_frontier2_run.py -- campaign-7 frontier: cdt_causal_run.py core VERBATIM plus a
measure/action term sigma*sum_v max(0,deg_v-D0)^2 that suppresses 1-skeleton HUB vertices at
fixed simplex counts (hence fixed f22, by the locked identity N22=N3-4N0+8T). Tests whether
reshaping connectivity (not counts) can lower d_s / lift d_H toward the seed-averaged T^3
benchmark at a STABLE uniform state. Detailed balance: the term is a state function; proposals
are unchanged, so Metropolis with exp(-dS_total) preserves DB. Original docstring follows.

cdt_causal.py -- v1: genuine causal CDT in 2+1 dimensions (3D bulk), following the v0
Euclidean result that d_s and d_H trade off and never reach 3 together (crumpling).

Ensemble: triangulations of S^2 x S^1 with a global integer time label on vertices,
T spatial slices (periodic time). Every tetrahedron spans two adjacent slices and is one of
  (3,1): 3 vertices at t, 1 at t+1     (its spatial base triangle lies in slice t)
  (2,2): 2 at t, 2 at t+1
  (1,3): 1 at t, 3 at t+1              (base in slice t+1)
Spatial slices are the subcomplexes of all-same-t triangles; they stay closed triangulated
2-spheres under all moves (checked, not assumed).

Moves (the standard 2+1D CDT set, cf. Ambjorn-Jurkiewicz-Loll):
  (2,3)/(3,2): Euclidean 2-3/3-2 Pachner flips RESTRICTED to configurations that respect the
               foliation: 2-3 acts on a (3,1)+(2,2) [or (1,3)+(2,2)] pair sharing a timelike
               triangle, creating a timelike edge; 3-2 is its inverse. Slice surfaces untouched.
  (2,6)/(6,2): insert/delete a vertex in a slice: a spatial triangle with its (3,1) above and
               (1,3) below is barycentrically split into 6 tets (inverse: remove a spatial
               order-3 vertex with unique up- and down-apex).
  (4,4):       flip a spatial edge (2D Pachner flip of the slice surface) together with the
               4 tets over/under it (requires unique up-apex and down-apex).
All moves check legality so the complex stays a genuine simplicial closed 3-manifold; the
link census (referee_3d) is asserted during selftests and at every measurement.

Action (Euclideanized, alpha=1 style): S = k3*N3 - k0*N0 + eps*(N3 - V)^2  (volume pinning).
k3 is auto-tuned toward the pseudo-critical value during a tuning phase, then frozen.
Metropolis acceptance includes the proposal-count ratios of the anchor sets (tets for
2-3/3-2, spatial triangles vs vertices for 2-6/6-2, spatial edges for 4-4), so detailed
balance holds at the level of these anchored proposals.

Measurements reuse the repo estimators VERBATIM for comparability with the Euclidean v0:
  d_s = lazy_rw_sdim (window 4-12), d_H = ball_growth_dim (window 2-6), link_census.

Run:  PYTHONPATH=$REPO:$REPO/tooling python3 cdt_causal.py --selftest
      ... --chunk --k0 2.0 --T 10 --V 700 --sweeps 3000 --budget-s 30 --log results.jsonl
Each --chunk call loads the pickled state if present, advances it within the wall-clock
budget, measures, appends one JSON line, and saves the state (safe under a 45 s cap).
"""
import argparse, itertools, json, math, os, pickle, random, sys, time as _time
from collections import Counter, defaultdict

REPO = os.environ.get("MANIFOLD_REPO", "/tmp/m")
sys.path[:0] = [REPO, os.path.join(REPO, "tooling")]
from referee_3d import link_census                      # noqa: E402
from referee_2d_scaling import lazy_rw_sdim, ball_growth_dim, nx_to_adj  # noqa: E402
from referee_2d_topology import to_graph                # noqa: E402

FS = frozenset
PROB = {"23": 0.25, "32": 0.25, "26": 0.15, "62": 0.15, "44": 0.20}


class IndexedSet:
    """set with O(1) uniform random choice."""
    __slots__ = ("items", "pos")

    def __init__(self):
        self.items = []; self.pos = {}

    def add(self, x):
        if x not in self.pos:
            self.pos[x] = len(self.items); self.items.append(x)

    def discard(self, x):
        i = self.pos.pop(x, None)
        if i is None:
            return
        last = self.items.pop()
        if i < len(self.items):
            self.items[i] = last; self.pos[last] = i

    def choice(self, rng):
        return self.items[rng.randrange(len(self.items))]

    def __len__(self):
        return len(self.items)

    def __contains__(self, x):
        return x in self.pos

    def __iter__(self):
        return iter(self.items)


class Causal:
    def __init__(self, T):
        assert T >= 3, "need T>=3 so a sandwich (t,t+1) is unambiguous"
        self.T = T
        self.time = {}            # vertex -> slice index
        self.next_id = 0
        self.tets = IndexedSet()  # frozenset(4)
        self.tkind = {}           # tet -> (n_lower, lo_slice)
        self.v2tets = {}          # vertex -> set(tets)
        self.valive = IndexedSet()
        self.tri2 = {}            # frozenset(3) -> set(tets), size <= 2
        self.ecnt = {}            # frozenset(2) -> #tets containing it
        self.stris = IndexedSet() # spatial triangles (all 3 verts same t)
        self.sedges = IndexedSet()# spatial edges
        self.nk = Counter()       # kind -> count, kind in {3:'(3,1)',2:'(2,2)',1:'(1,3)'}
        self.tries = Counter(); self.accs = Counter()
        self.deg = Counter()      # vertex -> current graph degree (edges with ecnt>0); maintained incrementally

    # -------------------------------------------------- typing
    def kind_of(self, tet):
        ts = [self.time[v] for v in tet]
        vals = set(ts)
        assert len(vals) == 2, "tet does not span exactly two slices"
        a, b = vals
        if b == (a + 1) % self.T:
            lo = a
        elif a == (b + 1) % self.T:
            lo = b
        else:
            raise AssertionError("tet spans non-adjacent slices")
        return ts.count(lo), lo

    def split_lo_hi(self, tet):
        k, lo = self.tkind[tet]
        lo_v = [v for v in tet if self.time[v] == lo]
        hi_v = [v for v in tet if self.time[v] != lo]
        return lo_v, hi_v, lo

    # -------------------------------------------------- incremental add/remove
    def add_tet(self, tet):
        self.tets.add(tet)
        self.tkind[tet] = self.kind_of(tet)
        self.nk[self.tkind[tet][0]] += 1
        for v in tet:
            s = self.v2tets.get(v)
            if s is None:
                s = set(); self.v2tets[v] = s
            if not s:
                self.valive.add(v)
            s.add(tet)
        for e in itertools.combinations(tet, 2):
            f = FS(e)
            c = self.ecnt.get(f, 0) + 1
            self.ecnt[f] = c
            if c == 1:
                self.deg[e[0]] += 1; self.deg[e[1]] += 1
                if self.time[e[0]] == self.time[e[1]]:
                    self.sedges.add(f)
        for tri in itertools.combinations(tet, 3):
            f = FS(tri)
            s = self.tri2.get(f)
            if s is None:
                s = set(); self.tri2[f] = s
            s.add(tet)
            assert len(s) <= 2, "face in >2 tets: move legality bug"
            if len(s) == 1 and len({self.time[v] for v in tri}) == 1:
                self.stris.add(f)

    def rem_tet(self, tet):
        self.tets.discard(tet)
        self.nk[self.tkind.pop(tet)[0]] -= 1
        for tri in itertools.combinations(tet, 3):
            f = FS(tri)
            s = self.tri2[f]
            s.discard(tet)
            if not s:
                del self.tri2[f]
                self.stris.discard(f)
        for e in itertools.combinations(tet, 2):
            f = FS(e)
            c = self.ecnt[f] - 1
            if c == 0:
                del self.ecnt[f]
                self.sedges.discard(f)
                a1, a2 = tuple(f)
                self.deg[a1] -= 1; self.deg[a2] -= 1
                if self.deg[a1] == 0: del self.deg[a1]
                if self.deg[a2] == 0: del self.deg[a2]
            else:
                self.ecnt[f] = c
        for v in tet:
            s = self.v2tets[v]
            s.discard(tet)
            if not s:
                del self.v2tets[v]
                self.valive.discard(v)

    @property
    def N3(self):
        return len(self.tets)

    @property
    def N0(self):
        return len(self.valive)

    # -------------------------------------------------- proposals
    # each returns None (illegal) or (dN3, dN0, prop_ratio, rem_list, add_list)
    def prop_23(self, rng):
        t0 = self.tets.choice(rng)
        k, _ = self.tkind[t0]
        if k == 2:
            return None
        lo_v, hi_v, lo = self.split_lo_hi(t0)
        if k == 3:      # (3,1): timelike faces are the 3 through the upper apex
            apex = hi_v[0]; base = lo_v
        else:           # (1,3)
            apex = lo_v[0]; base = hi_v
        i = rng.randrange(3)
        pair = [base[j] for j in range(3) if j != i]
        w = base[i]                       # opposite vertex of t0
        f = FS((apex, pair[0], pair[1]))
        nbrs = self.tri2[f]
        other = next(t for t in nbrs if t != t0) if len(nbrs) == 2 else None
        if other is None or self.tkind[other][0] != 2:
            return None
        x = next(iter(other - f))         # opposite vertex of the (2,2)
        piv = FS((w, x))
        if piv in self.ecnt:
            return None
        adds = [FS((w, x, pair[0], pair[1])), FS((w, x, pair[0], apex)), FS((w, x, pair[1], apex))]
        ratio = (PROB["32"] / PROB["23"]) * (self.N3 / (self.N3 + 1.0))
        return (1, 0, ratio, [t0, other], adds)

    def prop_32(self, rng):
        t0 = self.tets.choice(rng)
        k, _ = self.tkind[t0]
        if k == 2:
            return None
        lo_v, hi_v, lo = self.split_lo_hi(t0)
        if k == 3:
            apex = hi_v[0]; base = lo_v
        else:
            apex = lo_v[0]; base = hi_v
        a = base[rng.randrange(3)]        # pivot edge (a, apex): timelike
        around = [t for t in self.v2tets[a] if apex in t]
        if len(around) != 3:
            return None
        apx = set()
        for t in around:
            apx |= (t - {a, apex})
        if len(apx) != 3:
            return None
        need = {FS((a, apex) + p) for p in itertools.combinations(tuple(apx), 2)}
        if set(around) != need:
            return None
        # foliation: apexes must be 2 lower + 1 upper (anchor (3,1)) or 1 + 2 (anchor (1,3))
        nl = sum(1 for v in apx if self.time[v] == self.time[a])
        if (k == 3 and nl != 2) or (k == 1 and nl != 2):
            # for k==3 anchor, a is lower: want 2 apexes at time[a]; for k==1 anchor,
            # a is upper: want 2 apexes at time[a] as well (1 lower + 2 upper).  Same test.
            return None
        newtri = FS(apx)
        if newtri in self.tri2:
            return None
        n1 = FS(apx | {a}); n2 = FS(apx | {apex})
        if n1 in self.tets or n2 in self.tets:
            return None
        ratio = (PROB["23"] / PROB["32"]) * (self.N3 / (self.N3 - 1.0))
        return (-1, 0, ratio, list(around), [n1, n2])

    def prop_26(self, rng):
        f = self.stris.choice(rng)
        above, below = tuple(self.tri2[f])
        u, v, w = tuple(f)
        t = self.time[u]
        c = self.next_id  # new vertex (id assigned on apply)
        pa = next(iter(above - f)); pb = next(iter(below - f))
        adds, rems = [], [above, below]
        for x, y in ((u, v), (v, w), (u, w)):
            adds.append(FS((x, y, c, pa))); adds.append(FS((x, y, c, pb)))
        ratio = (PROB["62"] / PROB["26"]) * (len(self.stris) / (self.N0 + 1.0))
        return (4, 1, ratio, rems, adds, ("newv", c, t))

    def prop_62(self, rng):
        c = self.valive.choice(rng)
        tc = self.v2tets[c]
        if len(tc) != 6:
            return None
        t = self.time[c]
        sp, up, dn = set(), set(), set()
        for tet in tc:
            for v in tet:
                if v == c:
                    continue
                tv = self.time[v]
                if tv == t:
                    sp.add(v)
                elif tv == (t + 1) % self.T:
                    up.add(v)
                else:
                    dn.add(v)
        if len(sp) != 3 or len(up) != 1 or len(dn) != 1:
            return None
        u, v, w = tuple(sp); p = next(iter(up)); q = next(iter(dn))
        expect = set()
        for x, y in itertools.combinations((u, v, w), 2):
            expect.add(FS((x, y, c, p))); expect.add(FS((x, y, c, q)))
        if tc != expect:
            return None
        newtri = FS((u, v, w))
        if newtri in self.tri2:
            return None
        adds = [FS((u, v, w, p)), FS((u, v, w, q))]
        ratio = (PROB["26"] / PROB["62"]) * (self.N0 / (len(self.stris) - 2.0))
        return (-4, -1, ratio, list(tc), adds)

    def prop_44(self, rng):
        e = self.sedges.choice(rng)
        u, v = tuple(e)
        around = [t for t in self.v2tets[u] if v in t]
        if len(around) != 4:
            return None
        t = self.time[u]
        sp, up, dn = Counter(), Counter(), Counter()
        for tet in around:
            for z in tet:
                if z == u or z == v:
                    continue
                tz = self.time[z]
                if tz == t:
                    sp[z] += 1
                elif tz == (t + 1) % self.T:
                    up[z] += 1
                else:
                    dn[z] += 1
        if len(sp) != 2 or len(up) != 1 or len(dn) != 1:
            return None
        (w, cw), (x, cx) = sp.most_common()
        p = next(iter(up)); q = next(iter(dn))
        if cw != 2 or cx != 2 or up[p] != 2 or dn[q] != 2:
            return None
        if FS((w, x)) in self.ecnt:
            return None
        adds = [FS((z, w, x, p)) for z in (u, v)] + [FS((z, w, x, q)) for z in (u, v)]
        return (0, 0, 1.0, list(around), adds)

    def _degpen_delta(self, rems, adds, D0):
        # net change in sum_v pen(deg_v), pen(d)=max(0,d-D0)**2, if we apply rems->adds.
        # Uses current self.ecnt/self.deg (call BEFORE mutating). New vertices default deg 0.
        cnt = Counter()
        for t in rems:
            for e in itertools.combinations(t, 2):
                cnt[FS(e)] -= 1
        for t in adds:
            for e in itertools.combinations(t, 2):
                cnt[FS(e)] += 1
        dchg = Counter()
        for f, dc in cnt.items():
            if dc == 0:
                continue
            before = self.ecnt.get(f, 0)
            after = before + dc
            be = 1 if before > 0 else 0
            af = 1 if after > 0 else 0
            if af != be:
                a1, a2 = tuple(f)
                dchg[a1] += (af - be); dchg[a2] += (af - be)
        if not dchg:
            return 0.0
        s = 0.0
        for v, d in dchg.items():
            old = self.deg.get(v, 0)
            xo = old - D0; xn = old + d - D0
            po = xo * xo if xo > 0 else 0.0
            pn = xn * xn if xn > 0 else 0.0
            s += pn - po
        return s

    # -------------------------------------------------- Metropolis
    def attempt(self, rng, k0, k3, eps, V, k22=0.0, sigma=0.0, D0=18.0):
        r = rng.random(); acc_key = None
        for key in ("23", "32", "26", "62", "44"):
            r -= PROB[key]
            if r < 0:
                acc_key = key
                break
        self.tries[acc_key] += 1
        prop = getattr(self, "prop_" + acc_key)(rng)
        if prop is None:
            return False
        dN3, dN0, ratio, rems, adds = prop[0], prop[1], prop[2], prop[3], prop[4]
        dN22 = 1 if acc_key == "23" else (-1 if acc_key == "32" else 0)
        dS = (k3 * dN3 - k0 * dN0 + k22 * dN22
              + eps * ((self.N3 + dN3 - V) ** 2 - (self.N3 - V) ** 2))
        if sigma != 0.0:
            dS += sigma * self._degpen_delta(rems, adds, D0)
        if rng.random() >= min(1.0, ratio * math.exp(-dS)):
            return False
        if len(prop) == 6 and prop[5][0] == "newv":
            _, c, t = prop[5]
            self.time[c] = t
            self.next_id += 1
        for tet in rems:
            self.rem_tet(tet)
        for tet in adds:
            self.add_tet(tet)
        self.accs[acc_key] += 1
        return True

    def sweep(self, rng, k0, k3, eps, V, k22=0.0, sigma=0.0, D0=18.0):
        for _ in range(max(1, self.N3)):
            self.attempt(rng, k0, k3, eps, V, k22, sigma, D0)


# ------------------------------------------------------ seed: T octahedral slices, prisms
OCTA_TRIS = [(0, 2, 4), (0, 2, 5), (0, 3, 4), (0, 3, 5), (1, 2, 4), (1, 2, 5), (1, 3, 4), (1, 3, 5)]


def seed_state(T):
    st = Causal(T)
    for t in range(T):
        for i in range(6):
            st.time[t * 6 + i] = t
    st.next_id = 6 * T
    for t in range(T):
        t2 = (t + 1) % T
        for tri in OCTA_TRIS:
            a, b, c = sorted(tri)
            A, B, C = (t * 6 + a, t * 6 + b, t * 6 + c)
            A2, B2, C2 = (t2 * 6 + a, t2 * 6 + b, t2 * 6 + c)
            st.add_tet(FS((A, B, C, C2)))       # (3,1)
            st.add_tet(FS((A, B, B2, C2)))      # (2,2)
            st.add_tet(FS((A, A2, B2, C2)))     # (1,3)
    return st


# ------------------------------------------------------ validation (full rebuild, no trust)
def validate(st, heavy=False):
    ec, tc = Counter(), Counter()
    for tet in st.tets:
        st.kind_of(tet)  # raises if a tet does not span adjacent slices
        for e in itertools.combinations(tet, 2):
            ec[FS(e)] += 1
        for tr in itertools.combinations(tet, 3):
            tc[FS(tr)] += 1
    assert all(c == 2 for c in tc.values()), "complex not closed: face not in exactly 2 tets"
    assert set(ec) == set(st.ecnt) and all(st.ecnt[e] == ec[e] for e in ec), "edge cache drift"
    stris = {f for f in tc if len({st.time[v] for v in f}) == 1}
    assert stris == set(st.stris.pos), "spatial-triangle cache drift"
    sedges = {e for e in ec if len({st.time[v] for v in e}) == 1}
    assert sedges == set(st.sedges.pos), "spatial-edge cache drift"
    verts = set()
    for tet in st.tets:
        verts |= tet
    assert verts == set(st.valive.pos), "vertex cache drift"
    degc = Counter()
    for e in st.ecnt:
        aa, bb = tuple(e); degc[aa] += 1; degc[bb] += 1
    assert dict(st.deg) == dict(degc), "degree cache drift"
    # every spatial slice must be a closed connected 2-sphere
    by_t = defaultdict(list)
    for f in stris:
        by_t[st.time[next(iter(f))]].append(f)
    assert set(by_t) == set(range(st.T)), "a slice lost all its spatial triangles"
    for t, fs in by_t.items():
        ec2 = Counter()
        vs = set()
        for f in fs:
            vs |= f
            for e in itertools.combinations(sorted(f), 2):
                ec2[FS(e)] += 1
        assert all(c == 2 for c in ec2.values()), "slice %d not a closed surface" % t
        chi = len(vs) - len(ec2) + len(fs)
        assert chi == 2, "slice %d has chi=%d, not a 2-sphere" % (t, chi)
        g = defaultdict(set)
        for e in ec2:
            a, b = tuple(e); g[a].add(b); g[b].add(a)
        seen = {next(iter(vs))}; stk = [next(iter(vs))]
        while stk:
            xx = stk.pop()
            for y in g[xx]:
                if y not in seen:
                    seen.add(y); stk.append(y)
        assert len(seen) == len(vs), "slice %d disconnected" % t
    if heavy:
        c = link_census(list(st.tets))
        assert c["bad"] == 0 and c["disk"] == 0, "link census not clean: %s" % c
    return True


# ------------------------------------------------------ measurement (repo estimators verbatim)
def measure(st):
    adj = defaultdict(set)
    for e in st.ecnt:
        a, b = tuple(e)
        adj[a].add(b); adj[b].add(a)
    census = link_census(list(st.tets))
    a = nx_to_adj(to_graph(dict(adj)))
    ds = lazy_rw_sdim(a)
    dh = ball_growth_dim(a)
    prof = Counter()
    for f in st.stris:
        prof[st.time[next(iter(f))]] += 1
    profile = [prof.get(t, 0) for t in range(st.T)]
    degs = list(st.deg.values())
    import statistics as _st
    dmean = _st.mean(degs) if degs else 0.0
    dsd = _st.pstdev(degs) if len(degs) > 1 else 0.0
    return dict(census=census, ds=ds, dh=dh, profile=profile,
                N0=st.N0, N3=st.N3,
                n31=st.nk[3], n22=st.nk[2], n13=st.nk[1],
                deg_mean=round(dmean, 3), deg_sd=round(dsd, 3), deg_max=max(degs) if degs else 0,
                f22=round(st.nk[2] / max(1, st.N3), 4))


# ------------------------------------------------------ selftest
def selftest():
    print("=== causal CDT selftest: seed, typed moves, foliation + manifold invariants ===")
    for T in (3, 4, 8):
        st = seed_state(T)
        validate(st, heavy=True)
        chi = st.N0 - len(st.ecnt) + len(st.tri2) - st.N3
        assert chi == 0, "chi=%d, closed 3-manifold needs 0" % chi
        print("  seed T=%d: N0=%d N3=%d (31/22/13=%d/%d/%d) chi=0 census clean, slices are 2-spheres"
              % (T, st.N0, st.N3, st.nk[3], st.nk[2], st.nk[1]))
    rng = random.Random(0)
    st = seed_state(4)
    base = set(st.tets)

    def force(key, tries=4000):
        for _ in range(tries):
            p = getattr(st, "prop_" + key)(rng)
            if p is not None:
                if len(p) == 6 and p[5][0] == "newv":
                    st.time[p[5][1]] = p[5][2]; st.next_id += 1
                for tet in p[3]:
                    st.rem_tet(tet)
                for tet in p[4]:
                    st.add_tet(tet)
                return True
        return False

    # 2-3 then 3-2 must round-trip exactly
    assert force("23"); validate(st, heavy=True)
    assert force("32"); validate(st, heavy=True)
    assert set(st.tets) == base, "2-3 then 3-2 did not round-trip"
    print("  2-3 / 3-2 round-trip: exact, census clean at both steps")
    # 2-6 then 6-2 must round-trip exactly
    assert force("26"); validate(st, heavy=True)
    assert force("62"); validate(st, heavy=True)
    assert set(st.tets) == base, "2-6 then 6-2 did not round-trip"
    print("  2-6 / 6-2 round-trip: exact, census clean at both steps")
    # 4-4 twice on the same diamond restores the slice
    assert force("44"); validate(st, heavy=True)
    assert force("44"); validate(st, heavy=True)
    print("  4-4: applied twice, census clean throughout")
    # random chain at small volume: manifold + foliation must hold throughout
    st = seed_state(4)
    rng = random.Random(2)
    k3 = 0.6
    for s in range(200):
        st.sweep(rng, k0=1.0, k3=k3, eps=0.02, V=150)
        k3 += min(max((st.N3 - 150) * 2e-5, -2e-3), 2e-3)
        if (s + 1) % 50 == 0:
            validate(st, heavy=True)
    print("  200-sweep chain (T=4, V~150): N0=%d N3=%d f22=%.2f, census clean every 50 sweeps"
          % (st.N0, st.N3, st.nk[2] / st.N3))
    used = [k for k in PROB if st.accs[k] > 0]
    print("  accepted move mix:", {k: st.accs[k] for k in ("23", "32", "26", "62", "44")})
    assert len(used) == 5, "some move type never accepted: not exploring"
    m = measure(st)
    assert m["census"]["bad"] == 0
    print("  estimator smoke: d_s(4-12)=%s d_H(2-6)=%s profile=%s" % (m["ds"].get("4-12"), m["dh"].get("2-6"), m["profile"]))
    print("ALL CAUSAL SELF-TESTS PASSED")


# ------------------------------------------------------ chunked runner
def run_chunk(a):
    os.makedirs(a.scratch, exist_ok=True)
    tag = "k0%+.2f_T%d_V%d_s%d" % (a.k0, a.T, a.V, a.seed)
    sf = os.path.join(a.scratch, "causal_%s.pkl" % tag)
    if os.path.exists(sf):
        with open(sf, "rb") as fh:
            blob = pickle.load(fh)
        st, k3, done, rng = blob["st"], blob["k3"], blob["done"], blob["rng"]
        if not getattr(st, "deg", None):   # resume old pickle lacking the degree cache: rebuild from edges
            st.deg = Counter()
            for _e in st.ecnt:
                _x, _y = tuple(_e); st.deg[_x] += 1; st.deg[_y] += 1
    else:
        st = seed_state(a.T); k3 = a.k3_init; done = 0; rng = random.Random(a.seed)
        # grow to target volume quickly before tuning
        while st.N3 < a.V:
            st.sweep(rng, a.k0, -0.5, a.eps, a.V)
    if a.measure_long:
        adj = defaultdict(set)
        for e in st.ecnt:
            x, y = tuple(e)
            adj[x].add(y); adj[y].add(x)
        g = nx_to_adj(to_graph(dict(adj)))
        dsl = lazy_rw_sdim(g, windows=[(4, 12), (8, 24), (16, 48), (30, 90)], tmax=100)
        dhl = ball_growth_dim(g, windows=[(2, 6), (3, 8), (4, 10)])
        rec = dict(kind="long_measure", k0=a.k0, T=a.T, V=a.V, seed=a.seed, sweeps=done,
                   N0=st.N0, N3=st.N3, ds_long=dsl, dh_long=dhl)
        if a.log:
            with open(a.log, "a") as fh:
                fh.write(json.dumps(rec) + "\n")
        print("LONG k0=%+.2f V=%d T=%d s%d: d_s 4-12=%s 8-24=%s 16-48=%s 30-90=%s | d_H 2-6=%s 3-8=%s 4-10=%s"
              % (a.k0, a.V, a.T, a.seed, dsl.get("4-12"), dsl.get("8-24"), dsl.get("16-48"),
                 dsl.get("30-90"), dhl.get("2-6"), dhl.get("3-8"), dhl.get("4-10")))
        return
    t0 = _time.time()
    while done < a.sweeps and _time.time() - t0 < a.budget_s:
        st.sweep(rng, a.k0, k3, a.eps, a.V, a.k22, a.sigma, a.D0)
        if done < a.tune:
            k3 += min(max((st.N3 - a.V) * 2e-5, -2e-3), 2e-3)
        done += 1
    validate(st, heavy=False)
    m = measure(st)
    rec = dict(k0=a.k0, T=a.T, V=a.V, eps=a.eps, seed=a.seed, k3=round(k3, 4), sweeps=done,
               tuned=done >= a.tune, k22=a.k22, sigma=a.sigma, D0=a.D0, wall=round(_time.time() - t0, 1),
               acc={k: round(st.accs[k] / max(1, st.tries[k]), 3) for k in PROB}, **m)
    with open(sf, "wb") as fh:
        pickle.dump(dict(st=st, k3=k3, done=done, rng=rng), fh)
    if a.log:
        with open(a.log, "a") as fh:
            fh.write(json.dumps(rec) + "\n")
    c = m["census"]
    print("k0=%+.2f sweeps=%d/%d k3=%.3f | N0=%d N3=%d f22=%.2f | bad=%d | d_s(4-12)=%s d_H(2-6)=%s | prof min/max=%d/%d"
          % (a.k0, done, a.sweeps, k3, m["N0"], m["N3"], m["f22"], c["bad"],
             m["ds"].get("4-12"), m["dh"].get("2-6"), min(m["profile"]), max(m["profile"])))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--chunk", action="store_true")
    ap.add_argument("--k0", type=float, default=1.0)
    ap.add_argument("--k3-init", type=float, default=0.8, dest="k3_init")
    ap.add_argument("--T", type=int, default=10)
    ap.add_argument("--V", type=int, default=700)
    ap.add_argument("--eps", type=float, default=0.002)
    ap.add_argument("--k22", type=float, default=0.0)
    ap.add_argument("--sigma", type=float, default=0.0, help="hub-penalty coupling on sum_v max(0,deg-D0)^2")
    ap.add_argument("--D0", type=float, default=18.0, help="degree threshold above which hubs are penalized")
    ap.add_argument("--measure-long", action="store_true", dest="measure_long")
    ap.add_argument("--sweeps", type=int, default=3000)
    ap.add_argument("--tune", type=int, default=1000)
    ap.add_argument("--budget-s", type=float, default=30.0, dest="budget_s")
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--scratch", default="/tmp/m/scratch")
    ap.add_argument("--log", default=None)
    a = ap.parse_args()
    if a.selftest:
        selftest()
    elif a.chunk:
        run_chunk(a)
    else:
        ap.print_help()


if __name__ == "__main__":
    main()
