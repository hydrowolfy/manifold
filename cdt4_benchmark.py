#!/usr/bin/env python3
"""
Exact flat 4-torus benchmark (calibrant) for STAGE 3 (3+1D).
Coxeter-Freudenthal-Kuhn triangulation of T^4 = (Z/m)^4:
each unit 4-cube -> 24 four-simplices (one per permutation of the 4 axes,
the 'staircase' simplices). Tiles periodically -> closed 4-manifold.

Validates: (a) it is a valid closed simplicial 4-pseudomanifold (every
tetrahedron in exactly 2 four-simplices), chi(T^4)=0; (b) the repo referee
estimators read d_H ~ 4 and d_s ~ 4 on its 1-skeleton -- i.e. the joint
(d_H AND d_s) 4-manifold is what we are scoring against.
"""
import itertools, sys, math, statistics
from collections import Counter, defaultdict
sys.path.insert(0, "tooling")
from referee_2d_scaling import ball_growth_dim, lazy_rw_sdim

def kuhn_T4(m):
    """return (simplices, adjacency) for the Kuhn triangulation of (Z/m)^4."""
    E = [(1,0,0,0),(0,1,0,0),(0,0,1,0),(0,0,0,1)]
    def add(a,b): return tuple((a[i]+b[i]) % m for i in range(4))
    simplices = []
    for base in itertools.product(range(m), repeat=4):
        for perm in itertools.permutations(range(4)):
            v = base
            verts = [v]
            for ax in perm:
                v = add(v, E[ax])
                verts.append(v)
            fs = frozenset(verts)
            assert len(fs) == 5, "degenerate simplex (m too small): %r" % (verts,)
            simplices.append(fs)
    # 1-skeleton adjacency
    adj = defaultdict(set)
    for s in simplices:
        for a,b in itertools.combinations(s,2):
            adj[a].add(b); adj[b].add(a)
    return simplices, {k:set(v) for k,v in adj.items()}

def census_4mfld(simplices):
    """closed 4-pseudomanifold: every tetrahedron (3-face) in exactly 2 four-simplices.
       also report full f-vector + Euler characteristic."""
    ridge = Counter()   # 3-faces (tetrahedra)
    faces = [set() for _ in range(5)]
    for s in simplices:
        s = tuple(sorted(s))
        for k in range(5):
            for c in itertools.combinations(s, k+1):
                faces[k].add(c)
        for c in itertools.combinations(s, 4):
            ridge[c] += 1
    fvec = [len(f) for f in faces]
    bad = sum(1 for v in ridge.values() if v != 2)
    chi = sum(((-1)**k)*n for k,n in enumerate(fvec))
    return dict(fvec=fvec, bad=bad, chi=chi, n_ridge=len(ridge),
                ridge_hist=dict(Counter(ridge.values())))

def measure(adj, seeds=6):
    dH_w = [(2,6),(3,8),(2,8)]
    dS_w = [(8,24),(6,18),(10,30)]
    dHs = defaultdict(list); dSs = defaultdict(list)
    for s in range(seeds):
        h = ball_growth_dim(adj, windows=dH_w, nsrc=14, seed=1+s)
        d = lazy_rw_sdim(adj, windows=dS_w, nz=6, tmax=40, seed=2+s)
        for k,val in h.items():
            if val is not None: dHs[k].append(val)
        for k,val in d.items():
            if val is not None: dSs[k].append(val)
    def ms(d):
        return {k:(round(statistics.mean(v),3),
                   round(statistics.pstdev(v),3)) for k,v in d.items()}
    return ms(dHs), ms(dSs)

if __name__ == "__main__":
    print("="*70)
    print("FLAT T^4 KUHN BENCHMARK -- validity + estimator calibration")
    print("="*70)
    for m in (3,4,5):
        simplices, adj = kuhn_T4(m)
        c = census_4mfld(simplices)
        N4 = len(simplices)
        print(f"\n m={m}: N0={c['fvec'][0]} N1={c['fvec'][1]} N2={c['fvec'][2]} "
              f"N3={c['fvec'][3]} N4={c['fvec'][4]}  (24*m^4={24*m**4})")
        print(f"    census bad(tets not in exactly 2 pentachora)={c['bad']}  "
              f"ridge_hist={c['ridge_hist']}  chi={c['chi']} (T^4 expects 0)")
        # DS sanity: N3=5N4/2, N1=3N0+N4/2-3chi, N2=2N0+2N4-2chi
        N0,N1,N2,N3,N4c = c['fvec']
        ds_ok = (N3==5*N4c//2 and N1==3*N0+N4c//2-3*c['chi'] and N2==2*N0+2*N4c-2*c['chi'])
        print(f"    Dehn-Sommerville relations hold: {ds_ok}")
        degs = [len(v) for v in adj.values()]
        print(f"    mean vertex degree={statistics.mean(degs):.2f} "
              f"(uniform={len(set(degs))==1}, deg={degs[0] if len(set(degs))==1 else '...'})")
        if m >= 4:
            dH, dS = measure(adj, seeds=6)
            print(f"    d_H: {dH}")
            print(f"    d_s: {dS}")
