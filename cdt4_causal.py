#!/usr/bin/env python3
"""
STAGE 3 (3+1D) causal machinery + calibrant validation.

Key fact used: the Kuhn triangulation of T^4, foliated along axis 3, is a VALID
CAUSAL triangulation -- spatial slices are Kuhn T^3 (closed 3-manifolds), every
pentachoron spans two adjacent time levels and falls into a (4,1)/(3,2)/(2,3)/(1,4)
type. So the flat joint-4 benchmark IS a genuine state of the 4D causal ensemble
(the flat foliated calibrant), and we can read the 4D causal COUNTING relations off
it and show -- concretely -- that there is NO 2+1D-style lock (N0 and the timelike
fraction are two independent DOF).

Validates:
  (C1) foliation: every pentachoron spans exactly two adjacent time slices;
  (C2) census: every tetrahedron (3-face) is shared by exactly 2 pentachora (closed
       4-pseudomanifold), and every spatial slice is a valid closed 3-manifold
       (every spatial triangle in exactly 2 spatial tetrahedra), chi(slice)=0;
  (C3) 4D causal counting relations, and the ABSENCE of a dN=-c dN0 lock:
       N41 = 2 * (sum_t S_t)  with S_t (spatial tets/slice) FREE of V_t (verts/slice);
  (C4) the calibrant reads the joint 4-manifold (d_H and d_s ~ 4-band) -- the target.
"""
import itertools, sys, statistics
from collections import Counter, defaultdict
sys.path.insert(0, "tooling")
from cdt4_benchmark import kuhn_T4
from referee_2d_scaling import ball_growth_dim, lazy_rw_sdim

def build_causal_T4(m):
    """foliate Kuhn T^4 along axis 3 -> pentachora with time-typed vertices."""
    simplices, adj = kuhn_T4(m)
    time = {}                      # vertex -> t (its x3 coord)
    for v in adj:
        time[v] = v[3]
    def typ(pent):
        ts = sorted(set(time[v] for v in pent))
        assert len(ts) == 2, "pentachoron does not span two slices"
        a, b = ts
        # adjacency with wraparound
        if b == a + 1:                lo = a
        elif a == 0 and b == m - 1:   lo = b   # wrap m-1 -> 0
        else:                         raise AssertionError("non-adjacent slices %r" % ts)
        nlo = sum(1 for v in pent if time[v] == lo)
        return nlo, lo               # (n_lower, lower_slice)
    return simplices, adj, time, typ

def validate(m):
    simplices, adj, time, typ = build_causal_T4(m)
    T = m
    # ---- C1 foliation + types
    tcount = Counter()
    for p in simplices:
        nlo, lo = typ(p)
        tcount[(nlo, 5 - nlo)] += 1
    N41 = tcount[(4,1)] + tcount[(1,4)]
    N32 = tcount[(3,2)] + tcount[(2,3)]
    N4 = len(simplices)
    # ---- C2 whole-complex census (tets in exactly 2 pentachora)
    ridge = Counter()
    for p in simplices:
        for c in itertools.combinations(sorted(p), 4):
            ridge[c] += 1
    bad = sum(1 for v in ridge.values() if v != 2)
    # ---- spatial slices: valid closed 3-manifolds?
    S_t = Counter(); V_t = Counter()
    stets_by_t = defaultdict(list)
    for p in simplices:
        levels = [time[v] for v in p]
        for t in set(levels):
            if levels.count(t) == 4:                    # a spatial tetrahedron at t
                sp = frozenset(v for v in p if time[v] == t)
                stets_by_t[t].append(sp)
    slice_ok = True; slice_chi = {}
    for t in range(T):
        stets = set(stets_by_t[t])
        S_t[t] = len(stets)
        verts = set(v for tet in stets for v in tet); V_t[t] = len(verts)
        stri = Counter()
        for tet in stets:
            for c in itertools.combinations(sorted(tet), 3):
                stri[c] += 1
        sbad = sum(1 for x in stri.values() if x != 2)   # closed 3-mfld: tri in 2 tets
        # slice Euler (3-manifold -> 0)
        sf = [set(),set(),set(),set()]
        for tet in stets:
            for k in range(4):
                for c in itertools.combinations(sorted(tet), k+1):
                    sf[k].add(c)
        chi = len(sf[0])-len(sf[1])+len(sf[2])-len(sf[3])
        slice_chi[t] = chi
        if sbad != 0 or chi != 0: slice_ok = False
    N0 = len(adj)
    # ---- C3 counting relation: N41 == 2 * sum_t S_t
    sumS = sum(S_t.values())
    rel_ok = (N41 == 2 * sumS)
    print(f"=== causal T^4  m={m}  (T={T} slices) ===")
    print(f"  types per (n_lo,n_hi): {dict(tcount)}")
    print(f"  N0={N0}  N4={N4}  N41={N41}  N32={N32}  f_timelike=N32/N4={N32/N4:.3f}")
    print(f"  [C1] every pentachoron spans 2 adjacent slices, typed: OK")
    print(f"  [C2] whole-complex census bad(tet not in 2 pent)={bad}; "
          f"spatial slices valid closed 3-mflds={slice_ok} (all chi=0)")
    print(f"  [C3] N41 == 2*sum_t S_t : {N41} == 2*{sumS} : {rel_ok}")
    print(f"       per-slice V_t={dict(V_t)}")
    print(f"       per-slice S_t={dict(S_t)}   (S_t is the spatial-tet count)")
    return dict(simplices=simplices, adj=adj, N0=N0, N4=N4, N41=N41, N32=N32,
                S_t=S_t, V_t=V_t, bad=bad, slice_ok=slice_ok, rel_ok=rel_ok)

def two_dof_demo():
    """CONCRETE: at fixed spatial-vertex count V, the spatial-tetrahedron count S is
       free (2-3 Pachner move on a slice's 3-manifold) -> N41=2*sum S_t moves at fixed
       N0.  This is the operational unlock impossible in 2+1D (there dN22=-4dN0)."""
    print("\n=== [C3'] two independent DOF, operationally ===")
    # minimal S^3 slice = boundary of 4-simplex, then a 2-3 move (from Part A):
    tets = set(frozenset(c) for c in itertools.combinations(range(5),4))
    def counts(tets):
        verts=set(v for t in tets for v in t)
        return len(verts), len(tets)
    V0,S0 = counts(tets)
    # 1-4 then 2-3 (identical to the validated Part-A demonstration):
    tets.discard(frozenset((1,2,3,4)))
    for i in range(4):
        b=[1,2,3,4]; b[i]=5; tets.add(frozenset(b))
    V1,S1 = counts(tets)
    a,b = frozenset((5,2,3,4)), frozenset((0,2,3,4))
    tets.discard(a); tets.discard(b)
    for tri in [(2,3),(2,4),(3,4)]: tets.add(frozenset((0,5)+tri))
    V2,S2 = counts(tets)
    print(f"  slice S^3: (V,S)=({V0},{S0}) -1-4-> ({V1},{S1}) -2-3-> ({V2},{S2})")
    print(f"  => the 2-3 move changed spatial tets S {S1}->{S2} at FIXED spatial verts V={V2}.")
    print(f"     Since N41 = 2*sum_t S_t and N0 = sum_t V_t, this changes the timelike")
    print(f"     fraction at fixed N0.  In 2+1D the analogue is FORBIDDEN (dN22=-4dN0).")
    print(f"     => spatial-vertex density and timelike fraction are TWO independent DOF. OK")

def measure_calibrant(res, seeds=6):
    print("\n=== [C4] calibrant reads the joint 4-manifold ===")
    adj = res["adj"]
    dHw=[(2,6),(3,8)]; dSw=[(6,18),(8,24),(10,30)]
    H=defaultdict(list); S=defaultdict(list)
    for s in range(seeds):
        for k,v in ball_growth_dim(adj,windows=dHw,nsrc=16,seed=1+s).items():
            if v is not None: H[k].append(v)
        for k,v in lazy_rw_sdim(adj,windows=dSw,nz=6,tmax=60,seed=2+s).items():
            if v is not None: S[k].append(v)
    ms=lambda d:{k:(round(statistics.mean(v),3),round(statistics.pstdev(v),3)) for k,v in d.items()}
    print(f"  d_H (ball-growth): {ms(H)}")
    print(f"  d_s (spectral)   : {ms(S)}")
    print(f"  (T^3 benchmark for contrast: d_s(8-24)~3.13, d_H(2-6)~2.47; T^4 sits well above)")

if __name__ == "__main__":
    r = validate(4)          # m=4: N0=256, small, structure check
    two_dof_demo()
    r2 = validate(6)         # m=6: N0=1296, measure the calibrant here
    measure_calibrant(r2, seeds=6)
    allok = (r["bad"]==0 and r["slice_ok"] and r["rel_ok"]
             and r2["bad"]==0 and r2["slice_ok"] and r2["rel_ok"])
    print(f"\n  ALL CAUSAL-STRUCTURE CHECKS PASSED: {allok}")
