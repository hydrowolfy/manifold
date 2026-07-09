#!/usr/bin/env python3
"""Empirical ergodicity probe for the 4D CDT move set: show that N4 AND N0 (the two
independent DOF that unlock de Sitter) are each drivable UP and DOWN, the timelike
fraction f_tl=N32/N4 is tunable, and the walk returns from far-from-seed states.
(Formal ergodicity of this move set is the standard AJL 4D CDT result; this shows the
configuration space is practically connected on the implementation.)"""
import sys, random, time
from collections import Counter
sys.path.insert(0, "tooling")
import cdt4_prod as C
def pr(*a): print(*a, flush=True)

ADD = {'24':0.25,'28':0.30,'46':0.25,'33':0.20}
SUB = {'42':0.30,'82':0.30,'64':0.20,'33':0.20}

def step(st, weights, rng):
    r = rng.random(); c = 0.0
    for k, w in weights.items():
        c += w
        if r <= c: kind = k; break
    else: kind = '33'
    if kind == '24' and len(st.S_tet):   p = st.prop_24(st.S_tet.pick(rng))
    elif kind == '42' and len(st.S_edge): p = st.prop_42(st.S_edge.pick(rng))
    elif kind == '33' and len(st.S_tri):  p = st.prop_33(st.S_tri.pick(rng))
    elif kind == '46' and len(st.S_stri): p = st.prop_46(st.S_stri.pick(rng))
    elif kind == '64' and len(st.S_sedge):p = st.prop_64(st.S_sedge.pick(rng))
    elif kind == '28' and len(st.S_stet): p = st.prop_28(st.S_stet.pick(rng))
    elif kind == '82' and len(st.S_vert): p = st.prop_82(st.S_vert.pick(rng))
    else: p = None
    if p:
        st.apply(p[0], p[1])
        if kind == '28': st.nextv += 1
        return kind
    return None

def ftl(st): return st.n32 / max(st.N4, 1)

def run():
    rng = random.Random(0); t0 = time.time()
    st = C.seed_flat(4)
    N0s, N4s = st.N0, st.N4
    pr(f"seed: N0={N0s} N4={N4s} f_tl={ftl(st):.3f}")
    for i in range(4000): step(st, ADD, rng)
    N0g, N4g, fg = st.N0, st.N4, ftl(st)
    b,u = st.census()
    pr(f"after 4000 grow-biased: N0={N0g} N4={N4g} f_tl={fg:.3f} census=({b},{u})")
    for i in range(6000): step(st, SUB, rng)
    N0h, N4h, fh = st.N0, st.N4, ftl(st)
    b2,u2 = st.census()
    pr(f"after 6000 shrink-biased: N0={N0h} N4={N4h} f_tl={fh:.3f} census=({b2},{u2})")
    grew   = (N4g > 1.4*N4s and N0g > 1.2*N0s)
    shrank = (N4h < 0.75*N4g and N0h < 0.9*N0g)
    pr(f"  N4 up-and-down: {N4s} -> {N4g} -> {N4h}   (grew={grew}, shrank={shrank})")
    pr(f"  N0 up-and-down: {N0s} -> {N0g} -> {N0h}")
    st2 = C.seed_flat(4)
    for i in range(2500): step(st2, {'24':0.4,'42':0.4,'33':0.2}, rng)
    fA = ftl(st2)
    for i in range(2500): step(st2, {'33':0.6,'46':0.2,'64':0.2}, rng)
    fB = ftl(st2)
    pr(f"  timelike fraction tunable: f_tl {fg:.3f}(grow) vs {fA:.3f} vs {fB:.3f} "
       f"(range={max(fg,fA,fB)-min(fg,fA,fB):.3f})")
    spread = []
    for s in range(3):
        r = random.Random(100+s); q = C.seed_flat(4)
        for i in range(3000): step(q, {'24':0.22,'28':0.22,'46':0.18,'33':0.16,'42':0.08,'82':0.08,'64':0.06}, r)
        spread.append((q.N0, q.N4, round(ftl(q),3), q.census()))
    pr(f"  3 independent walks (N0,N4,f_tl,census): {spread}")
    all_clean = all(c==(0,0) for *_,c in spread) and b==0==u and b2==0==u2
    ok = grew and shrank and all_clean and (max(fg,fA,fB)-min(fg,fA,fB) > 0.05)
    pr(f"ERGODICITY PROBE [{time.time()-t0:.1f}s]:", "PASS (N4&N0 bidirectional, f_tl tunable, census-clean)" if ok else "REVIEW")
    return ok

if __name__ == "__main__":
    sys.exit(0 if run() else 1)
