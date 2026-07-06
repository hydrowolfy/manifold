"""Hypergraph rewriting.

A rule is a right-hand side: three directed edges among the symbols x, y, z, w. The left-hand
side is always the directed 2-path x->y->z. A match (redex) is any directed 2-path a->b->c in
the host; applying it destroys one copy each of (a,b) and (b,c) and adds the RHS with x,y,z
bound to a,b,c and w bound to a freshly-minted node.
"""
from collections import Counter
from sec00_core_substrate.hypergraph import nodes


def redexes(E):
    """All directed 2-paths a->b->c (a,b,c distinct) currently present."""
    out = {}
    for (a, b), m in E.items():
        if m > 0:
            out.setdefault(a, set()).add(b)
    R = []
    for (a, b), m in E.items():
        if m <= 0:
            continue
        for c in out.get(b, ()):
            if c != a and c != b and a != b and E[(b, c)] > 0:
                R.append((a, b, c))
    return R


def apply_rule(E, redex, rhs, fresh):
    """Apply `rhs` at `redex`; `fresh` is the next free node id. Returns (newE, next_fresh)."""
    a, b, c = redex
    sub = {'x': a, 'y': b, 'z': c, 'w': fresh}
    F = Counter(E)
    F[(a, b)] -= 1
    F[(b, c)] -= 1
    if F[(a, b)] <= 0:
        del F[(a, b)]
    if F[(b, c)] <= 0:
        del F[(b, c)]
    for (s, t) in rhs:
        F[(sub[s], sub[t])] += 1
    return F, fresh + 1


def evolve(E, rhs, steps, rng, fresh=None):
    """Random sequential rewriting for `steps` steps (or until no redex)."""
    if fresh is None:
        fresh = (max(nodes(E)) + 1) if nodes(E) else 0
    for _ in range(steps):
        R = redexes(E)
        if not R:
            break
        E, fresh = apply_rule(E, rng.choice(R), rhs, fresh)
    return E, fresh
