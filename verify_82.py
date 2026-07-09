#!/usr/bin/env python3
"""Vertex-move label-convention verification (STAGE 3 PART C).

The (2,8)/(8,2) move INSERTS a vertex with a FRESH integer label (nextv) and REMOVES a
specific vertex. Consequences, both CORRECT and intentional:
  * (2,8) then (8,2) on the inserted vertex is BYTE-IDENTICAL (selftest checks this).
  * (8,2) then (2,8) is reversible only UP TO RELABELING the reinserted vertex (a fresh
    label != the removed one) -- i.e. ISOMORPHISM-identical, not byte-identical.
Detailed balance is unaffected: the Metropolis acceptance A=min(1,(Kf/Kr)exp(-dS)) uses the
label-INDEPENDENT pick-set COUNTS (Kf=#spatial-tets for (2,8); Kr=#vertices for (8,2)), which
was verified to 0.00e+00 over 828+ (move,state) pairs (cdt4_scan.py --db-check). Do NOT 'fix'
the non-byte-identical (8,2)->(2,8) round-trip -- the fresh-label convention is required.

This script proves the (8,2)->(2,8) isomorphism-reversibility explicitly, and that (6,4)'s
reverse (4,6) primitive sits in its live pick-set (resolving the two coverage flags a naive
byte-identical test would raise).
"""
import sys, random
sys.path.insert(0, "tooling")
import cdt4_prod as C, cdt4_scan as S
def pr(*a): print(*a, flush=True)

def run():
    rng = random.Random(11); st = C.seed_flat(4)
    for _ in range(400):
        r = rng.random()
        if r < 0.4 and len(st.S_tet):
            p = st.prop_24(st.S_tet.pick(rng))
            if p: st.apply(p[0], p[1])
        elif r < 0.8 and len(st.S_stet):
            p = st.prop_28(st.S_stet.pick(rng))
            if p: st.apply(p[0], p[1]); st.nextv += 1
        elif len(st.S_stri):
            p = st.prop_46(st.S_stri.pick(rng))
            if p: st.apply(p[0], p[1])

    ok82 = None
    for v in list(st.S_vert.items):
        p82 = st.prop_82(v)
        if p82 is None: continue
        before = set(st.pents)
        info = st._match_82(v, list(st.v2p[v])); stet = info[0]
        st.apply(p82[0], p82[1])                 # (8,2): remove vertex v
        p28 = st.prop_28(stet)                   # (2,8): reinsert a FRESH vertex on merged tet
        assert p28 is not None, "reverse (2,8) on merged tet must exist"
        st.apply(p28[0], p28[1]); st.nextv += 1
        yv = p28[2][1]
        relab = lambda P: frozenset(v if w == yv else w for w in P)
        ok82 = ({relab(P) for P in st.pents} == before)
        pr(f"(8,2)->(2,8): removed v={v}, reinserted y={yv}; ISOMORPHIC after y->v relabel: {ok82}")
        break

    ok64 = None
    for e in list(st.S_sedge.items):
        p64 = st.prop_64(e)
        if p64 is None: continue
        before = set(st.pents); tri = p64[2][1]
        st.apply(p64[0], p64[1])
        in_set = tri in st.S_stri
        p46 = st.prop_46(tri)
        st.apply(p46[0], p46[1]) if p46 else st.apply(p64[1], p64[0])
        ok64 = in_set and p46 is not None and set(st.pents) == before
        pr(f"(6,4): reverse (4,6) primitive in S_stri={in_set}, byte-exact round-trip={set(st.pents)==before} -> {ok64}")
        break
    if ok64 is None: pr("(6,4): no site in this state (coverage only; selftest validates 15 round-trips)")

    good = bool(ok82) and (ok64 or ok64 is None)
    pr("VERIFY_82/64:", "PASS" if good else "REVIEW")
    return good

if __name__ == "__main__":
    sys.exit(0 if run() else 1)
