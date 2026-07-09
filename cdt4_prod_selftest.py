#!/usr/bin/env python3
"""Validate assembled Prod4: every move DB round-trip + census bad=0 + counters
consistent with recount (checked once/family) + long mixed chain. Lean + flushed."""
import sys, random, itertools, time
from collections import Counter
sys.path.insert(0, "tooling")
import cdt4_prod as C
from cdt4_prod import FS
def pr(*a): print(*a, flush=True)

def warmup(st, n, seed=0):
    rng = random.Random(seed)
    for _ in range(n):
        if rng.random() < 0.5 and len(st.S_tet):
            p = st.prop_24(st.S_tet.pick(rng))
            if p: st.apply(p[0], p[1])
        elif len(st.S_stet):
            p = st.prop_28(st.S_stet.pick(rng))
            if p: st.apply(p[0], p[1]); st.nextv += 1

def run():
    ok = True; rng = random.Random(0); t0 = time.time()

    st = C.seed_flat(4); before = set(st.pents); tested = 0
    for tau in list(st.tet2pent):
        p = st.prop_24(tau)
        if p is None: continue
        rems, adds, meta = p; N0_0, N4_0 = st.N0, st.N4
        st.apply(rems, adds); b1, u1 = st.census()
        inv = st.prop_42(meta[1]); assert inv is not None
        assert st.N4 - N4_0 == 2 and st.N0 - N0_0 == 0
        st.apply(inv[0], inv[1]); b2, u2 = st.census()
        assert set(st.pents) == before and b1==0==b2 and u1==0==u2
        tested += 1
        if tested >= 20: break
    assert st.counters_ok()[0]
    pr(f"  (2,4)/(4,2): {tested} exact round-trips, census+counters clean [{time.time()-t0:.1f}s]"); ok &= tested>0

    st = C.seed_flat(4); before = set(st.pents); tested = 0
    for stet in list(st.S_stet.items):
        p = st.prop_28(stet)
        if p is None: continue
        rems, adds, meta = p; x = meta[1]; N0_0, N4_0 = st.N0, st.N4
        st.apply(rems, adds); st.nextv += 1; b1, u1 = st.census()
        assert st.N0 - N0_0 == 1 and st.N4 - N4_0 == 6
        inv = st.prop_82(x); assert inv is not None
        st.apply(inv[0], inv[1]); b2, u2 = st.census()
        assert set(st.pents) == before and b1==0==b2 and u1==0==u2
        tested += 1
        if tested >= 15: break
    assert st.counters_ok()[0]
    pr(f"  (2,8)/(8,2): {tested} exact round-trips (dN0=+1,dN4=+6), census+counters clean [{time.time()-t0:.1f}s]"); ok &= tested>0

    st = C.seed_flat(4); warmup(st, 200, 1); assert st.census()==(0,0)
    before = set(st.pents); cand = [t for t,n in st.tris.items() if n==3]; tested = 0
    for tri in cand:
        p = st.prop_33(tri)
        if p is None: continue
        rems, adds, meta = p; N0_0, N4_0 = st.N0, st.N4
        st.apply(rems, adds); b1, u1 = st.census()
        p2 = st.prop_33(meta[1])
        if p2 is None: st.apply(adds, rems); continue
        assert st.N4==N4_0 and st.N0==N0_0
        st.apply(p2[0], p2[1]); b2, u2 = st.census()
        assert set(st.pents)==before and b1==0==b2 and u1==0==u2
        tested += 1
        if tested >= 15: break
    assert st.counters_ok()[0]
    pr(f"  (3,3): {tested} exact self-inverse round-trips, census+counters clean [{time.time()-t0:.1f}s]"); ok &= tested>0

    st = C.seed_flat(4); warmup(st, 200, 2); assert st.census()==(0,0)
    before = set(st.pents); tested = 0
    for tri in list(st.S_stri.items):
        p = st.prop_46(tri)
        if p is None: continue
        rems, adds, meta = p; N0_0, N4_0 = st.N0, st.N4
        st.apply(rems, adds); b1, u1 = st.census()
        assert st.N4 - N4_0 == 2 and st.N0 == N0_0
        p2 = st.prop_64(meta[1])
        if p2 is None: st.apply(adds, rems); continue
        st.apply(p2[0], p2[1]); b2, u2 = st.census()
        assert set(st.pents)==before and b1==0==b2 and u1==0==u2
        tested += 1
        if tested >= 15: break
    assert st.counters_ok()[0]
    pr(f"  (4,6)/(6,4): {tested} exact round-trips (dN4=+2,dN0=0), census+counters clean [{time.time()-t0:.1f}s]"); ok &= tested>0

    st = C.seed_flat(4); acc = Counter()
    for i in range(1500):
        r = rng.random()
        if r < 0.30 and len(st.S_tet):   p = st.prop_24(st.S_tet.pick(rng));  k='24'
        elif r < 0.50 and len(st.S_edge):p = st.prop_42(st.S_edge.pick(rng)); k='42'
        elif r < 0.62 and len(st.S_tri): p = st.prop_33(st.S_tri.pick(rng));  k='33'
        elif r < 0.72 and len(st.S_stri):p = st.prop_46(st.S_stri.pick(rng)); k='46'
        elif r < 0.80 and len(st.S_sedge):p = st.prop_64(st.S_sedge.pick(rng));k='64'
        elif r < 0.90 and len(st.S_stet):p = st.prop_28(st.S_stet.pick(rng)); k='28'
        elif len(st.S_vert):             p = st.prop_82(st.S_vert.pick(rng)); k='82'
        else: p=None; k=None
        if p:
            st.apply(p[0], p[1]); acc[k]+=1
            if k=='28': st.nextv += 1
    bad, unt = st.census(); cok = st.counters_ok()[0]
    pr(f"  mixed chain 1500: accepted {dict(acc)}")
    pr(f"    final N0={st.N0} N4={st.N4} census bad={bad} untyped={unt} counters_ok={cok} [{time.time()-t0:.1f}s]")
    ok &= (bad==0 and unt==0 and cok and all(acc[m]>0 for m in ('24','42','33','46','64','28','82')))
    pr("MOVE-SET SELFTEST:", "ALL PASSED" if ok else "FAILED")
    return ok

if __name__ == "__main__":
    sys.exit(0 if run() else 1)
