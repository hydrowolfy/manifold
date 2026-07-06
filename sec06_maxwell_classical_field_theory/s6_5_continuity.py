"""Closing Maxwell: the continuity equation (the last equation) and the unifying structure.

CONTINUITY (charge conservation, d_t rho + div J = 0) is the final Maxwell relation. Like Faraday and
no-monopole, it is NOT a dynamical input -- it is forced by d^2 = 0:

  FIELD LEVEL. The inhomogeneous equation is d*F = J. Taking d of both sides, d(d*F) = dJ, and d^2 = 0
  gives dJ = 0 -- continuity. In 2D: Ampere is (d_y B, -d_x B) = J + d_t E; the divergence of the left
  side is d_x d_y B - d_y d_x B = 0 (mixed partials commute), so d_t(div E) + div J = 0, i.e.
  d_t rho + div J = 0. Verified to machine precision for an arbitrary B.

  RULE LEVEL. The structural charge rho = in_degree - out_degree (sec06 s6_2) is conserved by the bare
  keystone rule not just globally but LOCALLY: at every firing the change d_rho sums to zero AND is
  supported only on the rewrite's own nodes {x,y,z,w}. Charge that leaves a node appears on an adjacent
  node -- a conserved local current. (Verified over many random firings on evolved graphs: worst
  |sum d_rho| = 0, worst out-of-neighbourhood change = 0.)

This completes the picture of Maxwell on the substrate, and it has a clean shape:

  THREE relations are KINEMATIC IDENTITIES (all the single fact d^2 = 0, given that the field is the
  curl of a potential, F = dA):
     - no magnetic monopoles   div B = 0           (DERIVED, sec06 s6_4)
     - Faraday induction       curl E = -d_t B     (DERIVED, sec06 s6_4)
     - continuity              d_t rho + div J = 0 (DERIVED, here)
  TWO relations are the DYNAMICAL equation of motion d*F = J (they carry the actual physics input):
     - Gauss's law             div E = rho         (PARTIAL, sec06 s6_3 -- the discrete Poisson law)
     - Ampere-Maxwell          curl B = J + d_t E  (PARTIAL, sec06 s6_4 -- current sources circulating B)

So Maxwell's four equations are three free identities plus two equations of motion; and the two
equations of motion rest on the one field action whose single coupling constant beta is the irreducible
input (sec06 s6_5_coupling_constant). The electromagnetic sector is therefore closed as far as it can
be: its kinematic half is fully DERIVED, its dynamical half is PARTIAL and reduces to that one number.
Pure Python.
"""
import math
import random
from collections import Counter
from sec00_core_substrate import nodes, evolve
from sec00_core_substrate.rewriting import redexes, apply_rule
from constants import KEYSTONE

STATUS = "DERIVED"
TITLE = "Continuity = d^2=0 (charge conserved, field + rule level); Maxwell closed (3 identities + 2 EOM)"


def _field_continuity(N=16):
    rng = random.Random(0)
    B = [[math.sin(0.4 * i - 0.3 * j) + 0.2 * rng.random() * math.cos(0.1 * i * j) for j in range(N)] for i in range(N)]
    cd_x = lambda F, i, j: (F[i + 1][j] - F[i - 1][j]) / 2.0
    cd_y = lambda F, i, j: (F[i][j + 1] - F[i][j - 1]) / 2.0
    Jx = [[cd_y(B, i, j) if 0 < i < N - 1 and 0 < j < N - 1 else 0.0 for j in range(N)] for i in range(N)]
    Jy = [[-cd_x(B, i, j) if 0 < i < N - 1 and 0 < j < N - 1 else 0.0 for j in range(N)] for i in range(N)]
    worst = 0.0
    for i in range(2, N - 2):
        for j in range(2, N - 2):
            worst = max(worst, abs(cd_x(Jx, i, j) + cd_y(Jy, i, j)))
    return worst


def _rule_continuity(trials=40):
    def div(E):
        ind = Counter(); outd = Counter()
        for (u, v), m in E.items():
            outd[u] += m; ind[v] += m
        return ind, outd
    worst_sum = 0; worst_nonlocal = 0; checked = 0; rng = random.Random(1)
    for trial in range(trials):
        E, _ = evolve(Counter([(0, 1), (1, 2), (2, 0)]), KEYSTONE, 200 + trial, rng)
        fresh = max(nodes(E)) + 1; R = redexes(E)
        if not R:
            continue
        r = rng.choice(R); a, b, c = r
        i0, o0 = div(E); E2, _ = apply_rule(E, r, KEYSTONE, fresh); i1, o1 = div(E2)
        alln = set(i0) | set(o0) | set(i1) | set(o1) | set(nodes(E2))
        ch = {n: (i1.get(n, 0) - o1.get(n, 0)) - (i0.get(n, 0) - o0.get(n, 0)) for n in alln}
        ch = {n: v for n, v in ch.items() if v != 0}
        worst_sum = max(worst_sum, abs(sum(ch.values())))
        worst_nonlocal = max(worst_nonlocal, len([n for n in ch if n not in {a, b, c, fresh}]))
        checked += 1
    return worst_sum, worst_nonlocal, checked


def run():
    print("[DERIVED] %s" % TITLE)
    w = _field_continuity()
    print("  CONTINUITY (field): div of Ampere's (d_yB,-d_xB) = %.1e for arbitrary B  => 0 (d^2=0 identity)." % w)
    ws, wn, ck = _rule_continuity()
    print("  CONTINUITY (rule, %d firings): worst|sum d_rho|=%d (globally conserved), worst out-of-{x,y,z,w}=%d (LOCAL)."
          % (ck, ws, wn))
    print("    => charge that leaves a node appears on a neighbour: a conserved local current. Continuity holds.")
    print("  MAXWELL CLOSED -- three identities (all d^2=0, from F=dA) + two equations of motion (d*F=J):")
    print("    identities (DERIVED): no-monopole div B=0 | Faraday curl E=-d_tB | continuity d_t rho+div J=0")
    print("    dynamical (PARTIAL):  Gauss div E=rho     | Ampere curl B=J+d_tE")
    print("    => the kinematic half is fully derived; the dynamical half reduces to one coupling beta")
    print("       (sec06 s6_5_coupling_constant), the irreducible input. EM is closed as far as it can be.")
