"""Regression tests for the program's headline claims (referee request #14).

Guards the results most likely to break silently across refactors and the ledger most likely to drift
out of sync with the prose. Run: `python tooling/regression_test.py` (or `python main.py mono` wires it).
Each check prints PASS/FAIL; the script exits non-zero if any check fails. All checks are bare-rule or
cheap recomputations -- no heavy experiments -- so the suite runs in a couple of seconds.

The six headline invariants:
  1. LEDGER SNAPSHOT  -- the tree leaf tally matches the published counts (keeps the whitepaper honest).
  2. b1 CONSERVATION  -- the keystone preserves the first Betti number exactly (the matter charge).
  3. CHARGE CONTINUITY -- rho=in-out is conserved LOCALLY by the bare rule (the native half of continuity).
  4. REDEXES OBSTRUCTION -- redexes(E) is a function of the edge multiset alone (why holonomy force was doomed).
  5. H-THEOREM -- the lazy random walk's KL to the degree-stationary distribution decreases monotonically.
  6. RAMIFIED GEOMETRY -- the pendant fraction is ~57% (the mechanism behind the dimension split + curvature).
"""
import os
import sys
import math
import random
from collections import Counter

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from sec00_core_substrate import evolve, betti1, nodes, redexes, apply_rule
from constants import KEYSTONE
import tree as T

EXPECTED_TALLY = {"DEF": 12, "DERIVED": 78, "PARTIAL": 125, "BORROWED": 15,
                  "CONJECTURE": 27, "OPEN": 99, "REFUTED": 5, "EXT": 5}
TRI = Counter([(0, 1), (1, 2), (2, 0)])
results = []


def check(name, ok, detail=""):
    results.append(ok)
    print("  [%s] %s%s" % ("PASS" if ok else "FAIL", name, ("  -- " + detail) if detail else ""))


def test_ledger():
    # Count leaves directly from the tree structure (the source of truth).
    tally = {g: v for g, v in T.leaf_tally().items() if v}
    expected = {g: v for g, v in EXPECTED_TALLY.items() if v}
    ok = tally == expected
    check("ledger snapshot matches published counts", ok,
          "" if ok else "got %s" % tally)


def test_b1():
    rng = random.Random(0); E = TRI; series = [betti1(E)]
    for _ in range(60):
        R = redexes(E)
        if not R:
            break
        E, _ = apply_rule(E, rng.choice(R), KEYSTONE, max(nodes(E)) + 1)
        series.append(betti1(E))
    ok = len(set(series)) == 1
    check("b1 conserved by the keystone (60 steps)", ok, "values %s" % sorted(set(series)))


def test_charge_continuity():
    def div(E):
        ind = Counter(); outd = Counter()
        for (u, v), m in E.items():
            outd[u] += m; ind[v] += m
        return ind, outd
    rng = random.Random(0); worst_sum = worst_nl = 0
    for t in range(20):
        E, _ = evolve(TRI, KEYSTONE, 150 + t, random.Random(t))
        R = redexes(E)
        if not R:
            continue
        r = rng.choice(R); a, b, c = r; fresh = max(nodes(E)) + 1
        i0, o0 = div(E); E2, _ = apply_rule(E, r, KEYSTONE, fresh); i1, o1 = div(E2)
        alln = set(i0) | set(o0) | set(i1) | set(o1) | set(nodes(E2))
        ch = {n: (i1.get(n, 0) - o1.get(n, 0)) - (i0.get(n, 0) - o0.get(n, 0)) for n in alln}
        ch = {n: v for n, v in ch.items() if v}
        worst_sum = max(worst_sum, abs(sum(ch.values())))
        worst_nl = max(worst_nl, len([n for n in ch if n not in {a, b, c, fresh}]))
    ok = worst_sum == 0 and worst_nl == 0
    check("charge rho=in-out locally conserved (continuity)", ok,
          "worst|sum|=%d worst_nonlocal=%d" % (worst_sum, worst_nl))


def test_redexes_obstruction():
    E, _ = evolve(TRI, KEYSTONE, 200, random.Random(3))
    r1 = sorted(redexes(E))
    Erl = Counter({(u + 1000, v + 1000): m for (u, v), m in E.items()})
    r2 = sorted((a - 1000, b - 1000, c - 1000) for (a, b, c) in redexes(Erl))
    ok = r1 == r2
    check("redexes is a function of the edge multiset alone", ok)


def test_h_theorem():
    E, _ = evolve(TRI, KEYSTONE, 150, random.Random(0))
    adj = {}
    for (u, v), m in E.items():
        adj.setdefault(u, {}); adj.setdefault(v, {})
        adj[u][v] = adj[u].get(v, 0) + m; adj[v][u] = adj[v].get(u, 0) + m
    N = sorted(adj); idx = {nn: i for i, nn in enumerate(N)}; n = len(N)
    deg = [sum(adj[u].values()) for u in N]; tot = sum(deg); pi = [d / tot for d in deg]
    p = [0.0] * n; p[0] = 1.0

    def stp(p):
        q = [0.0] * n
        for u in N:
            i = idx[u]
            if p[i] == 0:
                continue
            q[i] += 0.5 * p[i]
            for v, w in adj[u].items():
                q[idx[v]] += 0.5 * p[i] * w / deg[i]
        return q

    def kl(p):
        return sum(pp * math.log(pp / pii) for pp, pii in zip(p, pi) if pp > 1e-15)
    kls = [kl(p)]
    for _ in range(40):
        p = stp(p); kls.append(kl(p))
    ok = all(kls[i + 1] <= kls[i] + 1e-12 for i in range(len(kls) - 1))
    check("H-theorem: lazy-walk KL monotonically decreasing", ok,
          "%.3f -> %.4f" % (kls[0], kls[-1]))


def test_ramified():
    E, _ = evolve(TRI, KEYSTONE, 1200, random.Random(0))
    deg = Counter()
    for (u, v), m in E.items():
        deg[u] += m; deg[v] += m
    pend = sum(1 for nn in deg if deg[nn] == 1) / len(deg)
    ok = 0.45 <= pend <= 0.65
    check("ramified geometry: pendant fraction ~57%", ok, "measured %.1f%%" % (100 * pend))


def main():
    print("REGRESSION TESTS -- headline claims")
    test_ledger()
    test_b1()
    test_charge_continuity()
    test_redexes_obstruction()
    test_h_theorem()
    test_ramified()
    npass = sum(results); ntot = len(results)
    print("  ---- %d/%d passed ----" % (npass, ntot))
    sys.exit(0 if npass == ntot else 1)


if __name__ == "__main__":
    main()
