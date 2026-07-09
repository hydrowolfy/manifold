#!/usr/bin/env python3
"""
STAGE 3 PART A -- the cheap on-paper gate, computationally backed.

Question: does 3+1D causal CDT have an analogue of the 2+1D locking identity
dN22 = -4 dN0 (spatial-vertex density and the timelike-simplex fraction being
ONE locked DOF), or are they TWO INDEPENDENT DOF (path open)?

This script proves the algebra rather than asserting it:
  [1] recount the 2+1D locking identity on the ACTUAL runner seed (N31=2N0-2chi T,
      N22=N3-4N0+8T on the S^2 slices) -- reproduces the campaign-7 result.
  [2] derive+verify the closed-4-manifold Dehn-Sommerville relations on explicit
      triangulations with known f-vectors (dDelta5=S^4, cross-polytope S^4, CP^2_9),
      spanning chi in {2,3}; and on many random f-vectors from REAL 1->5 stellar
      subdivisions of an S^4 complex (recounted from scratch each time).
  [3] the decisive structural contrast: a closed 3-manifold slice's f-vector has
      TWO free parameters (V and #tetrahedra), vs ONE for a closed 2-manifold slice
      (F = 2V - 2chi). Demonstrated concretely with REAL Pachner moves: a 2-3 move
      changes #tetrahedra at FIXED vertex count on an S^3 (impossible on a surface).

No dependency beyond the repo's stdlib core (imports Causal for step 1 only).
"""
import itertools, sys, random
from collections import Counter

def FS(x): return frozenset(x)

# ----------------------------------------------------------------------------
# generic face-recounter for an abstract simplicial complex given by its
# maximal simplices (top-dim d). Non-circular: counts every k-face from scratch.
# ----------------------------------------------------------------------------
def fvector(tops, d):
    faces = [set() for _ in range(d+1)]
    for s in tops:
        s = tuple(sorted(s))
        for k in range(d+1):
            for c in itertools.combinations(s, k+1):
                faces[k].add(c)
    return [len(f) for f in faces]  # [N0, N1, ..., Nd]

def is_closed_pseudomanifold(tops, d):
    """every (d-1)-face is in exactly 2 top simplices."""
    ridge = Counter()
    for s in tops:
        s = tuple(sorted(s))
        for c in itertools.combinations(s, d):
            ridge[c] += 1
    return all(v == 2 for v in ridge.values()), ridge

def euler(fvec):
    return sum(((-1)**k) * n for k, n in enumerate(fvec))

# ----------------------------------------------------------------------------
# [1] 2+1D locking identity on the real runner seed
# ----------------------------------------------------------------------------
def check_2p1_identity():
    print("="*74)
    print("[1] 2+1D LOCKING IDENTITY on the real cdt_causal_run seed (S^2 slices, chi=2)")
    print("    predicted: N31=N13=2N0-2chiT ,  N22=N3-4N0+4chiT  (chi=2 -> +8T)")
    print("="*74)
    from cdt_causal_run import Causal, seed_state
    ok = True
    for T in (3, 4, 6, 8):
        st = seed_state(T)
        N0, N3 = st.N0, st.N3
        N31 = st.nk[3]; N22 = st.nk[2]; N13 = st.nk[1]
        chi = 2
        pred31 = 2*N0 - chi*T             # per-whole-complex, = 2N0 - 2*chi*T? see below
        # careful: identity is N31 = 2N0 - 2 chi T. compute directly:
        pred31 = 2*N0 - 2*chi*T
        pred22 = N3 - 4*N0 + 2*chi*T      # = N3 - 4N0 + 4 chi T? recheck: +4 chi T; chi=2 -> +8T
        pred22 = N3 - 4*N0 + 4*chi*T
        good = (N31 == pred31 == N13) and (N22 == pred22) and (N31+N22+N13 == N3)
        ok &= good
        f22 = N22 / N3
        print(f"  T={T:2d}: N0={N0:3d} N3={N3:3d} | N31={N31:3d}(pred {pred31:3d}) "
              f"N13={N13:3d} N22={N22:3d}(pred {pred22:3d}) f22={f22:.3f}  "
              f"{'OK' if good else 'MISMATCH'}")
    # the differential lock: at fixed (N3,T,chi), dN22 = -4 dN0
    print("  => at fixed (N3,T,chi): dN31=+2 dN0, dN22=-4 dN0  (ONE locked DOF: N0)")
    print(f"  identity exact on all seeds: {ok}")
    return ok

# ----------------------------------------------------------------------------
# [2] closed-4-manifold Dehn-Sommerville relations
#     derived: N1 = 3N0 + N4/2 - 3chi ; N2 = 2N0 + 2N4 - 2chi ; N3 = 5N4/2
# ----------------------------------------------------------------------------
def ds4_predict(N0, N4, chi):
    return (3*N0 + N4//2 - 3*chi,      # N1  (N4 even for closed 4-mfld: 2N3=5N4)
            2*N0 + 2*N4 - 2*chi,       # N2
            (5*N4)//2)                 # N3

def boundary_of_simplex(n):
    """boundary complex of the n-simplex = S^(n-1), tops = all n-subsets of n+1 verts."""
    V = list(range(n+1))
    return [FS(c) for c in itertools.combinations(V, n)]  # each omits one vertex

def cross_polytope_boundary(d):
    """boundary of the d-dim cross-polytope = triangulated S^(d-1).
       vertices +-e_i (2d of them); tops = choose one of each antipodal pair."""
    pairs = [(2*i, 2*i+1) for i in range(d)]
    tops = []
    for choice in itertools.product(*pairs):
        tops.append(FS(choice))
    return tops  # 2^d top (d-1)-simplices

def check_4d_ds():
    print("\n" + "="*74)
    print("[2] CLOSED 4-MANIFOLD DEHN-SOMMERVILLE (2 DS relations + Euler)")
    print("    derived: N1=3N0+N4/2-3chi ,  N2=2N0+2N4-2chi ,  N3=5N4/2")
    print("="*74)
    cases = []
    # explicit complexes, recount f-vector from scratch:
    s4a = boundary_of_simplex(5)                 # dDelta^5 = S^4, 6 verts
    cases.append(("dDelta^5 (S^4)", fvector(s4a, 4), 2))
    s4b = cross_polytope_boundary(5)             # 5-cross-polytope bdry = S^4, 10 verts
    cases.append(("cross-poly bdry (S^4)", fvector(s4b, 4), 2))
    # analytic-only f-vectors (well-known), to span chi:
    cases.append(("CP^2_9 (analytic f)", [9,36,84,90,36], 3))
    ok = True
    for name, fv, chi in cases:
        N0,N1,N2,N3,N4 = fv
        chk_euler = (euler(fv) == chi)
        p1,p2,p3 = ds4_predict(N0, N4, chi)
        good = (N1==p1 and N2==p2 and N3==p3 and chk_euler)
        ok &= good
        print(f"  {name:24s} f=({N0},{N1},{N2},{N3},{N4}) chi={euler(fv):+d} "
              f"| pred N1,N2,N3=({p1},{p2},{p3}) {'OK' if good else 'MISMATCH'}")
    return ok

def check_4d_random_stellar():
    print("\n  random REAL 1->5 stellar subdivisions of S^4 (recount from scratch):")
    tops = set(boundary_of_simplex(5))   # S^4
    nextv = 6
    rng = random.Random(12345)
    ok = True
    for step in range(12):
        # pick a facet, 1->5 stellar subdivide (adds 1 vertex, +4 facets)
        s = rng.choice(list(tops)); s = tuple(sorted(s))
        tops.discard(FS(s))
        x = nextv; nextv += 1
        for i in range(5):
            newf = FS(s[:i] + (x,) + s[i+1:])
            tops.add(newf)
        fv = fvector(tops, 4)
        closed,_ = is_closed_pseudomanifold(tops, 4)
        N0,N1,N2,N3,N4 = fv
        p1,p2,p3 = ds4_predict(N0, N4, 2)   # stays S^4, chi=2
        good = (N1==p1 and N2==p2 and N3==p3 and euler(fv)==2 and closed)
        ok &= good
        if step % 3 == 0 or not good:
            print(f"    step {step:2d}: f=({N0},{N1},{N2},{N3},{N4}) chi={euler(fv):+d} "
                  f"closed={closed} DS={'OK' if good else 'MISMATCH'}")
    print(f"  all random stellar steps satisfy DS + closed: {ok}")
    return ok

# ----------------------------------------------------------------------------
# [3] THE DECISIVE CONTRAST: slice f-vector free parameters, 2D vs 3D
# ----------------------------------------------------------------------------
def slice_dof_counting():
    print("\n" + "="*74)
    print("[3] SPATIAL-SLICE f-vector DOF  (the algebraic root of the (un)lock)")
    print("="*74)
    print("  closed 2-manifold slice (V,E,F):  2E=3F  and  V-E+F=chi")
    print("     => F = 2V - 2chi ,  E = 3V - 3chi     ONE free param (V).")
    print("     top-simplex count F is LOCKED to V.  --> 2+1D: N31=2N0-2chiT locked.")
    print("  closed 3-manifold slice (V,E,F,S):  2F=4S(=>F=2S)  and  V-E+F-S=0")
    print("     => F = 2S ,  E = V + S               TWO free params (V and S).")
    print("     top-simplex count S is FREE of V.   --> 3+1D: N41=2*sum S_t NOT locked to N0.")

def real_pachner_3manifold():
    print("\n  concrete proof: REAL Pachner moves on S^3 change #tetrahedra at FIXED N0")
    # S^3 = boundary of the 4-simplex: 5 vertices, 5 tetrahedra (each omits one vertex)
    tets = set(FS(c) for c in itertools.combinations(range(5), 4))
    def report(tag, tets):
        fv = fvector(tets, 3)
        closed, ridge = is_closed_pseudomanifold(tets, 3)
        print(f"    {tag:26s} N0={fv[0]} N1={fv[1]} N2={fv[2]} N3={fv[3]} "
              f"chi={euler(fv):+d} closed={closed}")
        return fv
    fv0 = report("dDelta^4 (S^3, minimal)", tets)

    # 1->4 stellar (bistellar) move on tet {1,2,3,4}: add vertex 5.  N0:5->6, N3:5->8
    tets.discard(FS((1,2,3,4)))
    for i in range(4):
        base=[1,2,3,4]; base[i]=5; tets.add(FS(base))
    fvA = report("after 1-4 move (N0->6)", tets)

    # 2->3 move: tets {5,2,3,4} & {0,2,3,4} share triangle {2,3,4}; opposite verts 5,0;
    # edge {0,5} absent (5 only in the 4 new tets) -> move is valid. N0 FIXED at 6, N3:8->9.
    a, b = FS((5,2,3,4)), FS((0,2,3,4))
    assert a in tets and b in tets, "precondition"
    assert FS((0,5)) not in set(e for t in tets for e in map(FS, itertools.combinations(t,2))), \
        "edge {0,5} must be absent for a valid 2-3 move"
    tets.discard(a); tets.discard(b)
    for tri in [(2,3),(2,4),(3,4)]:
        tets.add(FS((0,5)+tri))
    fvB = report("after 2-3 move (N0 FIXED)", tets)

    same_N0 = (fvA[0] == fvB[0] == 6)
    diff_N3 = (fvA[3] != fvB[3])
    print(f"    => N0 fixed at 6 across the 2-3 move: {same_N0};  "
          f"N3 changed {fvA[3]}->{fvB[3]}: {diff_N3}")
    print("    (a surface has NO fixed-V move that changes F: bistellar moves are")
    print("     1-3 [V+1,F+2], 2-2 flip [V,F unchanged], 3-1 [V-1,F-2] -- exhaustive.)")
    return same_N0 and diff_N3

# ----------------------------------------------------------------------------
if __name__ == "__main__":
    r1 = check_2p1_identity()
    r2 = check_4d_ds()
    r3 = check_4d_random_stellar()
    slice_dof_counting()
    r4 = real_pachner_3manifold()
    print("\n" + "="*74)
    print("VERDICT INPUTS:")
    print(f"  [1] 2+1D identity exact (one locked DOF)        : {r1}")
    print(f"  [2] 4D Dehn-Sommerville relations verified      : {r2}")
    print(f"  [3] 4D DS holds across random stellar f-vectors : {r3}")
    print(f"  [4] 3-manifold slice: N3 free at fixed N0       : {r4}")
    allok = r1 and r2 and r3 and r4
    print(f"\n  ALL CHECKS PASSED: {allok}")
    print("  CONCLUSION: 3+1D has NO analogue of dN22=-4dN0. Spatial-vertex density")
    print("  (N0) and the timelike-simplex fraction (N32/N4) are TWO INDEPENDENT DOF.")
    print("  Root: a 3-manifold slice's tetrahedron count is FREE of its vertex count")
    print("  (no 3D analogue of F=2V-2chi). PATH OPEN -> Part B warranted.")
    sys.exit(0 if allok else 1)
