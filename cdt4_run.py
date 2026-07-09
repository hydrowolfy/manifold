#!/usr/bin/env python3
"""
Minimal 3+1D causal CDT core: pentachora, foliation, census/manifold checks, and a
foliation-preserving Metropolis move pair (the 4D (2,4)/(4,2) Pachner flips on a
shared tetrahedron).  Pachner's theorem guarantees these preserve the PL-manifold
type; we ADD the CDT foliation legality (new pentachora must span exactly two adjacent
time slices) and verify detailed balance (exact round-trips, reverse delta = -forward)
+ manifold preservation (census bad=0) by brute force in --selftest, exactly as the
validated 2+1D runner does.

This is the validated FOUNDATION for the de Sitter production sweep.  It is NOT the
full ergodic AJL move set ((2,4)/(4,2)+(3,3)+... needed to explore the whole phase
diagram); scope + honesty are documented in REPORT_CDT_4D.md.
"""
import itertools, sys, math, statistics
from collections import Counter, defaultdict
sys.path.insert(0, "tooling")

def FS(x): return frozenset(x)

class Causal4:
    def __init__(self, T):
        self.T = T
        self.time = {}                     # vertex -> slice
        self.pents = set()                 # frozenset(5)
        self.tet2pent = defaultdict(set)   # frozenset(4) -> pentachora (<=2)
        self.edges = Counter()             # frozenset(2) -> multiplicity (present iff >0)

    # ---- incremental maintenance
    def add_pent(self, p):
        assert len(p) == 5
        self.pents.add(p)
        for c in itertools.combinations(sorted(p), 4):
            self.tet2pent[FS(c)].add(p)
            assert len(self.tet2pent[FS(c)]) <= 2, "tet in >2 pentachora (illegal)"
        for c in itertools.combinations(sorted(p), 2):
            self.edges[FS(c)] += 1
    def rem_pent(self, p):
        self.pents.discard(p)
        for c in itertools.combinations(sorted(p), 4):
            s = self.tet2pent[FS(c)]; s.discard(p)
            if not s: del self.tet2pent[FS(c)]
        for c in itertools.combinations(sorted(p), 2):
            f = FS(c); self.edges[f] -= 1
            if self.edges[f] == 0: del self.edges[f]

    @property
    def N4(self): return len(self.pents)
    @property
    def N0(self): return len({v for p in self.pents for v in p})

    def ptype(self, p):
        ts = sorted(set(self.time[v] for v in p))
        assert len(ts) == 2
        a, b = ts
        if b == a + 1:                  lo = a
        elif a == 0 and b == self.T-1:  lo = b
        else: return None               # spans non-adjacent slices -> not foliated
        return sum(1 for v in p if self.time[v] == lo)

    def is_foliated_pent(self, verts):
        """verts (5) span exactly two ADJACENT slices?"""
        ts = set(self.time[v] for v in verts)
        if len(ts) != 2: return False
        a, b = sorted(ts)
        return (b == a+1) or (a == 0 and b == self.T-1)

    # ---- census / manifold check
    def census(self):
        bad = sum(1 for s in self.tet2pent.values() if len(s) != 2)
        untyped = sum(1 for p in self.pents if self.ptype(p) is None)
        return bad, untyped

    # ---- (2,4): split tetrahedron tau (2 pentachora) -> 4 pentachora + edge{a,b}
    def prop_24(self, tau):
        ps = self.tet2pent.get(tau)
        if ps is None or len(ps) != 2: return None
        p1, p2 = tuple(ps)
        a = next(iter(p1 - tau)); b = next(iter(p2 - tau))
        if a == b: return None
        if FS((a, b)) in self.edges: return None          # Pachner legality: edge absent
        new = [FS({a, b} | set(tri)) for tri in itertools.combinations(sorted(tau), 3)]
        for q in new:
            if len(q) != 5: return None
            if q in self.pents: return None
            if not self.is_foliated_pent(q): return None   # CDT foliation legality
        return ([p1, p2], new)

    # ---- (4,2): inverse. edge {a,b} in exactly 4 pentachora forming the (2,4) pattern
    def prop_42(self, edge):
        a, b = tuple(edge)
        around = [p for p in self.pents if a in p and b in p]
        if len(around) != 4: return None
        # the "other 3" vertices of each must be the 4 triangles of a common tetrahedron
        tris = [frozenset(p - {a, b}) for p in around]
        if any(len(t) != 3 for t in tris): return None
        tau = frozenset().union(*tris)
        if len(tau) != 4: return None
        need = {frozenset(c) for c in itertools.combinations(sorted(tau), 3)}
        if set(tris) != need: return None
        if tau in self.tet2pent: return None               # tetrahedron must be re-addable
        p1 = FS(tau | {a}); p2 = FS(tau | {b})
        if p1 in self.pents or p2 in self.pents: return None
        if not (self.is_foliated_pent(p1) and self.is_foliated_pent(p2)): return None
        return (around, [p1, p2])

    def apply(self, rems, adds):
        for p in rems: self.rem_pent(p)
        for p in adds: self.add_pent(p)


def seed_flat(m):
    """flat foliated causal T^4 (Kuhn sliced along axis 3) as a Causal4 state."""
    from cdt4_benchmark import kuhn_T4
    simplices, _ = kuhn_T4(m)
    st = Causal4(T=m)
    for v in {v for s in simplices for v in s}:
        st.time[v] = v[3]
    for s in simplices:
        st.add_pent(s)
    return st


def selftest():
    print("=== 3+1D causal CDT selftest: foliation, census, (2,4)/(4,2) DB + manifold ===")
    import random
    ok = True
    for m in (4, 5):
        st = seed_flat(m)
        bad, untyped = st.census()
        typ = Counter(st.ptype(p) for p in st.pents)
        print(f"  seed m={m}: N0={st.N0} N4={st.N4} types(n_lo)={dict(typ)} "
              f"census bad={bad} untyped={untyped}")
        ok &= (bad == 0 and untyped == 0)

    # (2,4)/(4,2) round-trip: exact, census clean at both steps
    st = seed_flat(4)
    rng = random.Random(0)
    n_rt = 0; n_moves = 0
    tets = list(st.tet2pent.keys())
    for tau in tets:
        prop = st.prop_24(tau)
        if prop is None: continue
        rems, adds = prop
        before = set(st.pents)
        N4_0, N0_0 = st.N4, st.N0
        st.apply(rems, adds)
        b1, u1 = st.census()
        # reverse via (4,2) on the new edge {a,b}
        a = next(iter(rems[0] - tau)); b = next(iter(rems[1] - tau))
        inv = st.prop_42(FS((a, b)))
        assert inv is not None, "inverse (4,2) not found -> DB broken"
        # dN4 forward = +2, reverse = -2 (antisymmetric); dN0 = 0 both
        assert (st.N4 - N4_0 == 2) and (st.N0 - N0_0 == 0), "forward deltas wrong"
        st.apply(inv[0], inv[1])
        b2, u2 = st.census()
        assert set(st.pents) == before, "round-trip not exact -> DB broken"
        assert b1 == 0 == b2 and u1 == 0 == u2, "census dirty during move"
        n_rt += 1; n_moves += 1
        if n_rt >= 200: break
    print(f"  (2,4)/(4,2) exact round-trips verified: {n_rt} (census clean, reverse=-forward)")
    ok &= (n_rt > 0)

    # a random walk of accepted (2,4)/(4,2) moves keeps the census clean + foliated
    st = seed_flat(4); acc = Counter(); rng = random.Random(1)
    for _ in range(4000):
        if rng.random() < 0.5 and st.tet2pent:
            tau = rng.choice(list(st.tet2pent.keys())); pr = st.prop_24(tau)
            if pr: st.apply(*pr); acc['24'] += 1
        elif st.edges:
            e = rng.choice(list(st.edges.keys())); pr = st.prop_42(e)
            if pr: st.apply(*pr); acc['42'] += 1
    bad, untyped = st.census()
    print(f"  4000-attempt move chain: accepted {dict(acc)}  final N4={st.N4} "
          f"census bad={bad} untyped={untyped}")
    ok &= (bad == 0 and untyped == 0 and sum(acc.values()) > 0)

    print("ALL 3+1D CAUSAL SELF-TESTS PASSED" if ok else "SELFTEST FAILED")
    return ok


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        sys.exit(0 if selftest() else 1)
    else:
        print("usage: python3 cdt4_run.py --selftest")
