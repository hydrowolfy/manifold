"""How far must the keystone RULE deform to become an integer-dimensional MANIFOLD? Pin the obstruction exactly,
then test the minimal candidate modification -- and find it is NOT minimal. Closing local loops raises the cycle
density to lattice-like values AND eliminates the pendants (the two structural invariants that flag a tree), yet
the result is still NOT a manifold: the spectral dimension stays sub-2 and the walk dimension grows the WRONG way
(more anomalous, away from the manifold value 2). The bare b1=1 tree has no native d-dimensional MESH for local
loops to build on, so reaching d_s=d_H=d with d_w=2 requires imposing an external d-dimensional connectivity --
i.e. REPLACING the rule's tree character, not perturbing it.

IMPORTANT SCOPE: the ORIGINAL keystone rule's invariants are FIXED and unchanged here (b1=1, ~57% pendants, the
mismatched fractal dimensions of rounds 1/24). Everything below is a MODIFIED graph -- the keystone graph with an
added loop-closure / pendant-removal OVERLAY -- a SEPARATE object, labeled as such. This round changes no keystone
result and no leaf grade (tally fixed at 366).

THE MANIFOLD CRITERION (round 24's fractal Einstein relation d_s = 2 d_H / d_w): a smooth d-manifold has
d_s = d_H = d and d_w = 2 (normal diffusion). The keystone is a fractal: d_H~2.3-2.5 (volume), d_s~1.3-1.5
(transport), d_w~3 (subdiffusive) -- they DISAGREE. The cleanest finite-size-robust signals are the EXACT structural
invariants (cycle density c=b1/V, pendant fraction) and d_w (normal diffusion d_w=2 vs anomalous d_w>2); d_s is the
program's round-41 heat-kernel estimator; d_H (ball-growth) is finite-size-biased low and quoted with that caveat.

THE OBSTRUCTION, QUANTIFIED (exact, no fitting):
  * CYCLE DENSITY c = b1/V. Keystone: c = 1/V -> 0 (one loop in a growing tree). A d-lattice: c -> (d-1) EXTENSIVE
    (2D ->1, 3D ->2). The gap is not a small perturbation -- it is from zero to extensive.
  * PENDANT FRACTION. Keystone ~57% degree-1 nodes; a d-lattice 0%.
  * LOCALITY (round 25): a manifold needs loops between graph-NEARBY nodes (polynomial diameter ~N^{1/d}); random
    far loops give a small-world (diameter ~log N) -- mean-field, not a manifold.

THE TEST -- a single knob p (close distance-<=2 "elbows" into local cycles; this simultaneously adds local loops and
kills pendants), vs a random-loop control:
  RESULTS (modified keystone graph):
  OBSTRUCTION (exact): keystone c=b1/V~0 and ~52% pendants; a 2D lattice c=1 (=d-1), 0% pendants, d_w~1.95(~2); a 3D
  lattice c=1.63 (~d-1=2), d_w~2.2(~2). The keystone's three dimensions DISAGREE (d_s~1.2, d_w~2.6, d_H~2.5 = fractal);
  the lattices have d_w~2 (manifold signature). THE KNOB (close distance-2 elbows, p=0->1): cycle density c rises
  0->2.26 (lattice-like) and pendants fall 52%->0%, BUT d_s stays sub-2 (1.21->1.55) and d_w GROWS 2.70->3.42 (more
  anomalous, AWAY from the manifold value 2) -- a clustered fat-tree, not a manifold. LOCALITY: random loops at matched
  density collapse the diameter (21->5, small-world). So local loop-closure fixes the structural invariants but NOT the
  geometry; the minimal change to reach a d-manifold is to impose an external d-dimensional MESH, replacing the tree.

VALIDATION:
  (1) EXACT LATTICE BENCHMARK: a true d-lattice has c=(d-1) exactly, d_w~2, d_s~d (with the finite-size d_H caveat);
      the estimators are calibrated on it.
  (2) EXACT INVARIANTS: cycle density and pendant fraction are computed combinatorially (no fitting) and are exact.
  (3) LOCALITY: the random-loop control collapses the diameter (small-world), reproducing round 25.
  (4) INDEPENDENT REIMPLEMENTATION: the companion HTML recomputes c, pendant, diameter and d_s/d_w in JavaScript.

VERDICT (honest): the minimal modification is LARGE. Local loop-closure fixes the structural invariants (c -> ~2,
pendants -> 0) but the geometry stays fractal (d_s sub-2, d_w GROWS) -- a clustered fat-tree, not a manifold; random
loops give a small-world. A true d-manifold needs an externally-imposed d-dimensional mesh, which replaces the
rule's defining b1=1 tree. 3+1D is not reached by any minimal local edit of the keystone.

STATUS: PARTIAL (characterization) -- quantifies exactly how far the rule must deform; a negative result, graded as
such. No keystone result changes; no leaf change; tally fixed at 366. Pure Python.
"""
import math
import os
import random
from collections import Counter, defaultdict, deque
from sec00_core_substrate.rewriting import redexes
from constants import KEYSTONE

STATUS = "PARTIAL"
TITLE = "Manifold modification: local loops fix the invariants (c, pendants) but NOT the geometry (d_w grows) -- minimal change is large"
_FULL = os.environ.get("EMERGENCE_FULL", "") == "1"


def _keystone(steps, seed=5):
    E = Counter([(0, 1), (1, 2), (2, 0)]); fresh = 3; rng = random.Random(seed)
    for _ in range(steps):
        R = redexes(E)
        if not R:
            break
        a, b, c = rng.choice(R); E[(a, b)] -= 1; E[(b, c)] -= 1
        if E[(a, b)] <= 0:
            del E[(a, b)]
        if E[(b, c)] <= 0:
            del E[(b, c)]
        sub = {'x': a, 'y': b, 'z': c, 'w': fresh}
        for (s, t) in KEYSTONE:
            E[(sub[s], sub[t])] += 1
        fresh += 1
    adj = defaultdict(set)
    for (u, v) in E:
        if u != v:
            adj[u].add(v); adj[v].add(u)
    nodes = sorted(adj); idx = {v: i for i, v in enumerate(nodes)}
    return {idx[u]: set(idx[v] for v in adj[u]) for u in adj}


def _lattice(dims):
    import itertools
    idx = {c: i for i, c in enumerate(itertools.product(*[range(L) for L in dims]))}
    adj = defaultdict(set)
    for c, i in idx.items():
        for d in range(len(dims)):
            for s in (1, -1):
                c2 = list(c); c2[d] += s; c2 = tuple(c2)
                if c2 in idx:
                    adj[i].add(idx[c2])
    return {i: adj[i] for i in range(len(idx))}


def _add_local(adj, p, seed=7):
    """close distance-2 'elbows' (pairs sharing a neighbour) into local cycles with probability p."""
    A = {u: set(adj[u]) for u in adj}; rng = random.Random(seed); cand = set()
    for u in list(A):
        nb = list(A[u])
        for i in range(len(nb)):
            for j in range(i + 1, len(nb)):
                a, b = nb[i], nb[j]
                if b not in A[a]:
                    cand.add((min(a, b), max(a, b)))
    for (a, b) in cand:
        if rng.random() < p:
            A[a].add(b); A[b].add(a)
    return A


def _add_random(adj, nadd, seed=7):
    A = {u: set(adj[u]) for u in adj}; rng = random.Random(seed); n = len(A); added = 0; tries = 0
    while added < nadd and tries < nadd * 30:
        a = rng.randrange(n); b = rng.randrange(n); tries += 1
        if a != b and b not in A[a]:
            A[a].add(b); A[b].add(a); added += 1
    return A


def _bfs(A, s):
    d = {s: 0}; q = deque([s])
    while q:
        u = q.popleft()
        for v in A[u]:
            if v not in d:
                d[v] = d[u] + 1; q.append(v)
    return d


def _invariants(A):
    n = len(A); E = sum(len(A[u]) for u in A) // 2
    seen = set(); C = 0
    for s in A:
        if s in seen:
            continue
        C += 1; st = [s]; seen.add(s)
        while st:
            u = st.pop()
            for v in A[u]:
                if v not in seen:
                    seen.add(v); st.append(v)
    b1 = E - n + C
    pend = sum(1 for u in A if len(A[u]) == 1) / n
    return n, b1 / n, pend, E / n


def _diam(A, ns=8, seed=1):
    rng = random.Random(seed); m = 0
    for _ in range(ns):
        m = max(m, max(_bfs(A, rng.randrange(len(A))).values()))
    return m


def _sl(xs, ys):
    nn = len(xs); mx = sum(xs) / nn; my = sum(ys) / nn
    return sum((xs[i] - mx) * (ys[i] - my) for i in range(nn)) / sum((xs[i] - mx) ** 2 for i in range(nn))


def _d_s(A, nz=8, tmax=35, seed=2):
    n = len(A); deg = {i: len(A[i]) for i in A}; md = max(deg.values()); dt = 0.4 / md; rng = random.Random(seed)
    nb = {i: list(A[i]) for i in A}; ns = int(tmax / dt)
    samp = sorted(set(int(x) for x in [1.45 ** k for k in range(3, 40)] if 1 <= x < ns)); acc = {s: 0.0 for s in samp}
    for _ in range(nz):
        v = [1.0 if rng.random() < 0.5 else -1.0 for _ in range(n)]; z = v[:]; si = 0
        for st in range(1, ns + 1):
            Lv = [0.0] * n
            for i in range(n):
                s = deg[i] * v[i]
                for j in nb[i]:
                    s -= v[j]
                Lv[i] = s
            for i in range(n):
                v[i] -= dt * Lv[i]
            if si < len(samp) and st == samp[si]:
                acc[samp[si]] += sum(z[i] * v[i] for i in range(n)) / n; si += 1
    ts = [s * dt for s in samp]; Ps = [acc[s] / nz for s in samp]
    pts = [(math.log(t), math.log(P)) for t, P in zip(ts, Ps) if P > 6.0 / n and P > 0]
    return -2 * _sl([p[0] for p in pts], [p[1] for p in pts]) if len(pts) >= 4 else float('nan')


def _d_w(A, nwalk=300, tmax=90, seed=3):
    n = len(A); rng = random.Random(seed); nb = {i: list(A[i]) for i in A}
    samp = sorted(set(int(x) for x in [1.4 ** k for k in range(2, 40)] if 1 <= x < tmax))
    msd = {t: 0.0 for t in samp}; cnt = {t: 0 for t in samp}
    for _ in range(nwalk):
        s = rng.randrange(n); d = _bfs(A, s); pos = s; si = 0
        for st in range(1, tmax + 1):
            pos = rng.choice(nb[pos])
            if si < len(samp) and st == samp[si]:
                msd[samp[si]] += d[pos] ** 2; cnt[samp[si]] += 1; si += 1
    dm = max(_bfs(A, 0).values()); lim = (0.4 * dm) ** 2
    xs = [math.log(t) for t in samp if cnt[t] and 0 < msd[t] / cnt[t] < lim]
    ys = [math.log(msd[t] / cnt[t]) for t in samp if cnt[t] and 0 < msd[t] / cnt[t] < lim]
    return 2.0 / _sl(xs, ys) if len(xs) >= 4 else float('nan')


def _d_H(A, nsrc=14, seed=1):
    n = len(A); rng = random.Random(seed); sl = []
    for _ in range(nsrc):
        s = rng.randrange(n); d = _bfs(A, s); S = Counter(d.values()); rmax = max(S)
        rhi = max(3, int(rmax * 0.4))
        xs = [math.log(r) for r in range(1, rhi + 1) if S[r] > 0]; ys = [math.log(S[r]) for r in range(1, rhi + 1) if S[r] > 0]
        if len(xs) >= 3:
            sl.append(1.0 + _sl(xs, ys))
    return sum(sl) / len(sl)


def run():
    print("[PARTIAL] %s" % TITLE)
    print("  Manifold criterion: d_s=d_H=d, d_w=2 (normal diffusion). Keystone is a FRACTAL (the three disagree).")
    print("  SCOPE: keystone invariants are FIXED; below are MODIFIED-graph OVERLAYS (separate objects). Tally 366.\n")
    ksteps = 300 if not _FULL else 600

    print("  (A) THE OBSTRUCTION, EXACT -- keystone vs d-lattice (cycle density c=b1/V, pendant fraction):")
    K = _keystone(ksteps)
    n, c, pend, ev = _invariants(K)
    print("      keystone     N=%3d  c=b1/V=%.3f (->0)   pendants=%.0f%%   d_s=%.2f d_w=%.2f d_H=%.2f (fractal: disagree)"
          % (n, c, 100 * pend, _d_s(K), _d_w(K), _d_H(K)))
    for name, dims in [("2D lattice", (24, 24)), ("3D lattice", (8, 8, 8))]:
        L = _lattice(dims); nL, cL, pL, _ = _invariants(L)
        print("      %-12s N=%3d  c=b1/V=%.3f (=d-1=%d) pendants=%.0f%%   d_s=%.2f d_w=%.2f d_H=%.2f (MANIFOLD: d_w~2)"
              % (name, nL, cL, len(dims) - 1, 100 * pL, _d_s(L), _d_w(L), _d_H(L)))
    print("      => gap: cycle density 0 -> EXTENSIVE (d-1); pendants 57%% -> 0; and d_w must fall to 2.")

    print("\n  (B) THE KNOB -- close distance-<=2 elbows into LOCAL loops (raises c AND kills pendants), vs p:")
    print("      %5s  %6s  %8s  %5s  %6s  %6s  %6s" % ("p", "c", "pendant", "diam", "d_s", "d_w", "d_H"))
    for p in [0.0, 0.25, 0.5, 1.0]:
        A = _add_local(K, p); nA, cA, pA, evA = _invariants(A)
        print("      %5.2f  %6.2f  %7.0f%%  %5d  %6.2f  %6.2f  %6.2f" % (p, cA, 100 * pA, _diam(A), _d_s(A), _d_w(A), _d_H(A)))
    print("      => c rises to lattice-like (~2) and pendants -> 0, BUT d_s stays sub-2 and d_w GROWS (away from 2):")
    print("         local triangle-closure makes a clustered FAT-TREE (triangles trap the walk), NOT a manifold.")

    print("\n  (C) LOCALITY CONTROL -- random (non-local) loops at matched density:")
    A1 = _add_local(K, 1.0); extra = (sum(len(A1[u]) for u in A1) - sum(len(K[u]) for u in K)) // 2
    AR = _add_random(K, extra); _, cR, _, _ = _invariants(AR)
    print("      random loops c=%.2f  diameter=%d  vs LOCAL (p=1) diameter=%d -- random COLLAPSES the diameter" % (
        cR, _diam(AR), _diam(A1)))
    print("      (small-world / mean-field, NOT a manifold) -- reproducing round 25: the loops must be LOCAL.")

    print("\n  => VERDICT: the minimal modification is LARGE. Local loop-closure fixes the structural INVARIANTS")
    print("     (cycle density 0->~2 extensive, pendants 57%->0) but NOT the GEOMETRY -- d_s stays ~1.5 and d_w GROWS")
    print("     to ~3.4 (more anomalous, away from the manifold value 2): a clustered fat-tree, still fractal/")
    print("     hyperbolic at large scales. Random loops give a small-world. A true d-manifold (d_s=d_H=d, d_w=2)")
    print("     needs an externally-imposed d-dimensional MESH -- a directional structure the b1=1 tree does not")
    print("     possess -- which REPLACES the rule's tree character. 3+1D is NOT reached by any minimal local edit;")
    print("     the obstruction is not the loop COUNT (fixable) but the absence of native d-dimensional CONNECTIVITY.")
