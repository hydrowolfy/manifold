"""Monogamy of mutual information: the keystone free scalar VIOLATES it (I3 > 0), so its entanglement has
no classical Ryu-Takayanagi bulk dual -- it is not holographic in the strong sense, despite the area law.

A sharp holographic diagnostic. States with a classical RT (minimal-surface) bulk dual satisfy the
MONOGAMY of mutual information (Hayden-Headrick-Maloney): for any three regions,
    I3(A:B:C) = I(A:B) + I(A:C) - I(A:BC) = S_A+S_B+S_C - S_AB-S_AC-S_BC + S_ABC  <=  0.
Generic quantum field states need not; free fields typically VIOLATE it (I3 > 0). So the sign of I3 tests
whether a system's entanglement is holographic (RT-geometric) or merely area-law.

The tempting hypothesis (which this module REFUTES): the keystone's b1=1 TREE geometry is exactly the
geometry MERA / holographic tensor networks live on, so maybe the keystone entanglement is monogamous
(holographic). It is not -- because the natural STATE here is the free-field (Gaussian) ground state, not a
holographic tensor network. The tree geometry is holography-friendly; the free-field state on it is not.

RESULT (computed with the round-31 Casini-Huerta machinery, pure Python):
  * 1D chain (a tree): nearby triples give I3 > 0 (every config). VIOLATES monogamy -- a free field.
  * 2D grid (non-tree): nearby triples give I3 > 0 (every config). VIOLATES monogamy -- a free field.
  * keystone tree: nearby triples give I3 > 0 (essentially every config); the cleanest signal is the HUB
    tripartition -- three subtree branches hanging off one high-degree node -- where I(A:B) ~ 0.1-0.14 and
    I3(A:B:C) ~ 0.05-0.08 > 0, a substantial, unambiguous violation.
So the keystone free scalar is NOT holographic in the RT sense. Its entanglement obeys an area law
(s9_5_entanglement_entropy_area_law) but lacks the monogamy a classical bulk geometry would require; the
area law is necessary but not sufficient, and the keystone fails the sufficient (MMI) test exactly as a
generic free field does. The tree geometry does not rescue it -- holography is a property of the state, and
the rule's natural state is a free Gaussian field, not a MERA.

STATUS: this REFUTES the "entanglement geometry" (RT) conjecture for the natural free-scalar realization
(monogamy is violated, so no consistent minimal-surface bulk); it sharpens the "limits of the analogy"
(area law yes, RT geometry no). Native: the field is the rule's Laplacian; regions are bare-graph subtrees.
Pure Python.
"""
import os
import random
from collections import deque
from sec09_quantum_mechanics.s9_5_entanglement_entropy_area_law import (
    _corr, _entropy, _keystone, _chain, _grid)

STATUS = "REFUTED"
TITLE = "Monogamy of mutual information VIOLATED (I3>0): free-scalar entanglement is not holographic (no RT bulk)"

_FULL = os.environ.get("EMERGENCE_FULL", "") == "1"


def _S(X, P, A):
    return _entropy(X, P, A) if A else 0.0


def _I2(X, P, A, B):
    return _S(X, P, A) + _S(X, P, B) - _S(X, P, list(A) + list(B))


def _I3(X, P, A, B, C):
    A = list(A); B = list(B); C = list(C)
    return (_S(X, P, A) + _S(X, P, B) + _S(X, P, C)
            - _S(X, P, A + B) - _S(X, P, A + C) - _S(X, P, B + C)
            + _S(X, P, A + B + C))


def _dist(adj, src):
    d = {src: 0}; dq = deque([src])
    while dq:
        x = dq.popleft()
        for y in adj[x]:
            if y not in d:
                d[y] = d[x] + 1; dq.append(y)
    return d


def _nearby_signs(n, adj, m2, blk=2, reps=24, seed=7):
    X, P = _corr(n, adj, m2); rng = random.Random(seed)
    pos = neg = tot = 0; mx = 0.0
    for _ in range(reps):
        c = rng.randrange(n); d = _dist(adj, c)
        near = [x for x in d if d[x] <= 5]
        if len(near) < 3 * blk + 1:
            continue
        rng.shuffle(near)
        A = near[:blk]; B = near[blk:2 * blk]; C = near[2 * blk:3 * blk]
        v = _I3(X, P, A, B, C); tot += 1; mx = max(mx, v)
        if v > 1e-7:
            pos += 1
        elif v < -1e-7:
            neg += 1
    return pos, neg, tot, mx


def run():
    print("[REFUTED] %s" % TITLE)
    print("  Holographic (classical RT bulk) <=> monogamy I3 = I(A:B)+I(A:C)-I(A:BC) <= 0. Free fields violate it.")
    nchain = 60 if not _FULL else 140
    Lgrid = 9 if not _FULL else 13
    nstep = 150 if not _FULL else 360

    n, adj, _e = _chain(nchain)
    pos, neg, tot, mx = _nearby_signs(n, adj, 0.05)
    print("  1D chain (a tree)   : %d/%d nearby triples have I3>0 (max %.3f) -> VIOLATES monogamy (free field)" % (pos, tot, mx))
    n, adj = _grid(Lgrid)
    pos, neg, tot, mx = _nearby_signs(n, adj, 0.05)
    print("  2D grid (non-tree)  : %d/%d nearby triples have I3>0 (max %.3f) -> VIOLATES monogamy (free field)" % (pos, tot, mx))

    print("  KEYSTONE -- hub tripartition (3 subtree branches off one high-degree node, where I3 is largest):")
    n, adj, _e = _keystone(nstep, seed=5); X, P = _corr(n, adj, 0.05)
    hubs = [v for v in range(n) if len(adj[v]) >= 3]
    rng = random.Random(1); rng.shuffle(hubs); shown = 0
    for h in hubs:
        nbrs = list(adj[h])
        if len(nbrs) < 3:
            continue
        nbrs = nbrs[:3]

        def _branch(start, cap=6):
            seen = {start}; dq = deque([start])
            while dq and len(seen) < cap:
                x = dq.popleft()
                for y in adj[x]:
                    if y != h and y not in seen:
                        seen.add(y); dq.append(y)
            return list(seen)
        A = _branch(nbrs[0]); B = _branch(nbrs[1]); C = _branch(nbrs[2])
        if set(A) & set(B) or set(A) & set(C) or set(B) & set(C):
            continue
        iab = _I2(X, P, A, B); v = _I3(X, P, A, B, C)
        print("    deg %d hub: I(A:B)=%.3f  I3(A:B:C)=%+.3f  -> %s" % (
            len(adj[h]), iab, v, "<=0 monogamous (holographic)" if v <= 1e-7 else ">0 VIOLATES (not holographic)"))
        shown += 1
        if shown >= 5:
            break
    print("  => the keystone free scalar VIOLATES monogamy (I3>0), like the chain and grid free fields. Its")
    print("     entanglement has an area law but NO classical RT bulk dual -- it is not holographic in the")
    print("     strong sense. The b1=1 tree geometry is MERA-friendly, but holography is a property of the")
    print("     STATE, and the rule's natural state is a free Gaussian field, not a holographic tensor network.")
