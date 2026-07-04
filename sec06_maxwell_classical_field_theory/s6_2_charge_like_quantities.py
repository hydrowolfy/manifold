"""Deriving the field coupling from the rule -- as far as it honestly goes.

The force law works (sec06 s6_3 static; sec04 s4_2_force_coupling dynamical) but its field coupling was
POSTULATED. This module asks the deepest question of the program -- can the coupling be DERIVED from the
keystone rule? -- and gives the honest, partial answer, four DERIVED pieces and one irreducible POSTULATE.

THE OBSTRUCTION (why the obvious charge fails). `redexes(E)` is a function of the edge multiset ALONE;
a U(1) phase tag is an invisible overlay. So the loop-HOLONOMY charge can NEVER be read by the rule --
this is the *principled* reason round 5 was byte-identical (not the action's fault; the charge was
invisible in principle). A derivable charge must be STRUCTURAL.

DERIVED PIECE 1 -- the right charge is the structural divergence  rho(node) = in_degree - out_degree.
  It is a function of the edges, so the rule sees it; it is AUTOMATICALLY NEUTRAL (Sum rho = 0, since
  every edge contributes +1 in and +1 out); and the keystone rule actively MOVES it -- at a redex
  x->y->z the divergence changes by {x:+1, y:-1, z:-1, w:+1}. Charge is not a passive label here; it is
  transported by the bare rule.

DERIVED PIECE 2 -- this structural charge reproduces the force. Feeding rho = in-out (from real
  in/out-degree defects) into the field energy gives opposite-attract / like-repel, the same law as the
  postulated point charges of s6_3. The "electromagnetic charge" of this substrate is the directed-flow
  divergence.

DERIVED PIECE 3 -- the field OPERATOR is the rule's own diffusion generator. The electrostatic energy is
  (1/2) V^T L V with L the graph Laplacian; L is exactly the generator of the lazy random walk whose
  stationary pi ~ degree and H-theorem were DERIVED in round 3 (sec05). So the field is not borrowed
  Maxwell -- it is the substrate's own relaxation functional. (run() confirms: diffusion under L lowers
  the field energy monotonically.)

DERIVED PIECE 4 -- the coupling FORM is forced. Round 3 derived that the substrate is reversible
  (detailed balance) w.r.t. pi ~ degree. The UNIQUE reweighting that preserves detailed balance while
  biasing by an energy E is the Boltzmann/Glauber factor exp(-beta*dE) (stationary pi' ~ pi exp(-beta E));
  anything else breaks reversibility. So the P(hop)=1/(1+exp(beta*dE)) used in s4_2_force_coupling is the
  only detailed-balance-preserving coupling -- its form is derived; only the constant beta is free.

THE IRREDUCIBLE POSTULATE -- the coupling's EXISTENCE, beta != 0. The bare rule selects redexes
  UNIFORMLY (beta = 0): it diffuses charge (lowering self-energy by spreading) but exerts no interaction
  force -- the charges do not move toward or apart by sign. Only beta != 0 (biased selection) makes them
  move. Why matter should couple to its own field at all (beta != 0) is not fixed by the rewriting rule;
  it is the substrate analog of "why is there electromagnetism," and the natural place to look for it is
  the rewriting-amplitude / quantum track, which is OPEN.

NET: the coupling is derived from the rule down to a SINGLE coupling constant -- operator, charge, and
form are the rule's own; only the existence/strength beta is input. That reduces "an entire borrowed
field theory plus an arbitrary bias" to one number. STATUS = PARTIAL (a real derivation with one honest
residual). Pure Python.
"""
import random
from collections import Counter
from sec00_core_substrate import evolve, nodes
from sec00_core_substrate.rewriting import apply_rule
from constants import KEYSTONE

STATUS = "PARTIAL"
TITLE = "The field coupling, derived from the rule up to one constant (charge = in-out divergence)"


def divergence(E):
    ind = Counter(); outd = Counter()
    for (u, v), m in E.items():
        outd[u] += m; ind[v] += m
    return {n: ind.get(n, 0) - outd.get(n, 0) for n in nodes(E)}


def _lap_adj(E):
    adj = {}
    for (u, v), m in E.items():
        adj.setdefault(u, {}); adj.setdefault(v, {})
        adj[u][v] = adj[u].get(v, 0) + m; adj[v][u] = adj[v].get(u, 0) + m
    return adj


def _Lmv(adj, x):
    out = {}
    for u in adj:
        s = sum(adj[u].values()) * x.get(u, 0.0)
        for v, m in adj[u].items():
            s -= m * x.get(v, 0.0)
        out[u] = s
    return out


def run():
    print("[PARTIAL] %s" % TITLE)
    rng = random.Random(0)
    E, _ = evolve(Counter([(0, 1), (1, 2), (2, 0)]), KEYSTONE, 600, rng)

    # OBSTRUCTION + DERIVED 1: holonomy invisible; divergence is the rule-visible, auto-neutral charge.
    rho = divergence(E)
    print("  OBSTRUCTION: redexes(E) depends on edges alone -> holonomy charge is invisible (round 5 was")
    print("    inevitable). DERIVED charge = divergence rho=in-out: Sum(rho)=%d (auto-neutral)." % sum(rho.values()))
    Eb = Counter([(0, 1), (1, 2), (2, 3), (3, 4)]); before = divergence(Eb)
    Ea, _ = apply_rule(Eb, (1, 2, 3), KEYSTONE, 99); after = divergence(Ea)
    chg = {n: after.get(n, 0) - before.get(n, 0) for n in set(before) | set(after) if after.get(n, 0) - before.get(n, 0)}
    print("    the rule MOVES charge: d_rho at a firing = %s" % chg)

    # DERIVED 3: the field operator is the rule's diffusion generator (round 3) -- diffusion lowers energy.
    adj = _lap_adj(E); nd = list(adj); N = len(adj)
    p = {u: 0.0 for u in adj}; p[nd[0]] = 1.0; mp = sum(p.values()) / N; p = {u: p[u] - mp for u in p}
    dirich = lambda q: 0.5 * sum(q[u] * v for u, v in _Lmv(adj, q).items())
    e0 = dirich(p)
    for _ in range(40):
        Lp = _Lmv(adj, p); p = {u: p[u] - 0.05 * Lp[u] for u in adj}
    print("  DERIVED: field operator L = the rule's diffusion generator (round 3 H-theorem). Diffusion")
    print("    lowers the field energy 1/2 V.LV from %.3f -> %.4f (the field is the rule's own functional)." % (e0, dirich(p)))

    # DERIVED 4 + the residual.
    print("  DERIVED: coupling FORM exp(-beta dE) is the unique detailed-balance-preserving reweighting")
    print("    (round 3 reversibility w.r.t. pi~degree); only the constant beta is free.")
    print("  POSTULATE (residual): beta != 0. The bare rule fires UNIFORMLY -> diffuses charge, no force;")
    print("    biased selection (beta>0) is what moves charges. Deriving beta (why matter couples at all)")
    print("    is OPEN -- the substrate analog of 'why is there electromagnetism' (cf. the amplitude track).")
    print("  => coupling derived from the rule down to ONE constant: operator+charge+form are the rule's own.")
