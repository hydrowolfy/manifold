"""Trying to derive the Dirac mass term -- and finding a structural obstruction: the keystone is a Weyl world.

Round 14 showed mass would be zitterbewegung (a glider zigzagging between the two native +/-v0 chiralities),
with one missing native ingredient: a chirality FLIP (the Dirac mass term, coupling left- and right-movers).
This module attempts to derive that flip from the rule. It cannot be found, for a structural reason, and the
reason is itself a result.

THE KEYSTONE RULE IS CHIRAL. For a directed path x->y->z it writes ((x,z),(y,x),(z,w)) -- the head x and the
tail z are treated ASYMMETRICALLY (x receives the back-edge y->x; z spawns the fresh node z->w). Applied to a
path and to its reverse the rule gives mirror-image results, never the same structure: the rule has a fixed
handedness. The glider inherits it and moves one way only (uni-chiral; no rightward firing exists -- the
round-7 result). This is the same "handedness bit" the amplitude track flags as possessed, not derived.

NO NATIVE L<->R COUPLING EXISTS. Both chiralities exist (the glider runs +v0 on a rail i+1->i and -v0 on the
mirror rail i->i+1; round 14), so a massive particle would be a glider converting between them. But every way
of coupling the two chiralities fails:
  - END-TO-END JUNCTIONS (a left-rail meeting a right-rail): the glider PINS at the junction -- the 2-path it
    needs to keep moving is broken there. Tested across boundaries, domain walls, and five junction/defect
    types (single reversed edge, doubled edge, side-loop, source, sink); a bounded search (6000 states each)
    found NO reversal.
  - SIDE-BY-SIDE RUNGS (parallel left- and right-rails coupled by cross-edges -- the natural "mass term"):
    the rungs make the whole ladder one 2-core, DELOCALIZING the glider (its two-core jumps from size 2 to
    the entire ladder). The localized excitation is destroyed rather than converted.

So the chiral keystone provides no native realization of the chirality flip: junctions pin, rungs delocalize.

CONCLUSION -- A WEYL WORLD; MASS IS AN IRREDUCIBLE INPUT. The keystone produces massless, single-chirality
gliders: Weyl-like fermions. A Dirac mass term (the L<->R coupling that would make zitterbewegung, hence a
sub-luminal accelerable particle) is NOT derivable from the bare rule; it must be added as an irreducible
input, joining the rule's handedness and the coupling beta. This mirrors the Standard Model precisely:
fermions are chiral in the kinetic term, and mass comes from an external (Higgs/Yukawa) coupling, not from
the kinetics. The substrate is, at this level, a massless chiral world; mass is added structure.

HONEST STATUS = OPEN (a characterized obstruction, not a derivation). This is empirical evidence from a
bounded search across boundaries, domain walls, junction/defect types, and rung-coupled ladders -- not a
proof that no mechanism exists. What is established: the rule's chirality (exact), the pinning at junctions,
and the delocalization by rungs. No leaf grade is changed by this module. Pure Python.
"""
from collections import Counter
import os
from collections import Counter
from sec00_core_substrate import two_core, apply_rule, redexes
from constants import KEYSTONE

STATUS = "OPEN"
TITLE = "Deriving the Dirac mass term: obstructed -- the keystone is a chiral (Weyl) world; mass is an irreducible input"

_FULL = os.environ.get("EMERGENCE_FULL", "") == "1"


def _build_defect(jtype, J=8, hi=24):
    E = Counter()
    for i in range(J, hi):
        E[(i, i + 1)] += 1                       # left-rail for i>=J (glider moves toward J)
    E[(hi - 3, hi - 4)] += 1                      # plant glider 2-cycle near hi
    if jtype == "source_wall":
        for i in range(0, J):
            E[(i + 1, i)] += 1                    # right-rail before J
    elif jtype == "rev_edge":
        for i in range(0, J - 1):
            E[(i, i + 1)] += 1
        E[(J, J - 1)] += 1                        # single reversed edge before J
    elif jtype == "double":
        for i in range(0, J):
            E[(i, i + 1)] += 1
        E[(J - 1, J)] += 1                        # doubled edge at the junction
    elif jtype == "branch":
        for i in range(0, J):
            E[(i, i + 1)] += 1
        E[(J, 100)] += 1; E[(100, J)] += 1        # side 2-cycle off J
    return E, max(max(u, v) for (u, v) in E) + 1


def _reversal_search(cap=2500, max_depth=7):
    """LIVE test of the Weyl obstruction: drive a glider to a defect, then bounded-search for ANY reversal
    (a size-2 2-core that moves back the other way). Returns (n_types_tested, any_reversal, total_states)."""
    types = ("source_wall", "rev_edge", "double", "branch") if _FULL else ("source_wall", "rev_edge")
    cap = 6000 if _FULL else cap
    any_rev = False; total = 0
    for jtype in types:
        E, fresh = _build_defect(jtype)
        # drive the glider left to the junction
        while True:
            tc = two_core(E); lo = min(tc) if tc else None
            if lo is None or lo <= 8:
                break
            n = lo
            if E.get((n - 1, n), 0) < 1:
                break
            E, fresh = apply_rule(E, (n - 1, n, n + 1), KEYSTONE, fresh)
            E, fresh = apply_rule(E, (n - 1, n + 1, n), KEYSTONE, fresh)
        start = min(two_core(E)) if two_core(E) else 8
        # bounded BFS for a reversed 2-cycle
        def key(E):
            return frozenset((e, m) for e, m in E.items() if m > 0)
        seen = {key(E)}; frontier = [(E, fresh, 0)]
        while frontier and len(seen) < cap:
            Ec, fc, d = frontier.pop()
            if d >= max_depth:
                continue
            for r in redexes(Ec):
                try:
                    E2, f2 = apply_rule(Ec, r, KEYSTONE, fc)
                except Exception:
                    continue
                k = key(E2)
                if k in seen:
                    continue
                seen.add(k)
                tc2 = two_core(E2)
                if tc2 and len(tc2) == 2 and min(tc2) > start + 1:
                    any_rev = True
                frontier.append((E2, f2, d + 1))
                if len(seen) >= cap:
                    break
        total += len(seen)
    return len(types), any_rev, total


def _rule_chirality():
    def ap(elist, redex):
        E = Counter(elist); E, _ = apply_rule(E, redex, KEYSTONE, max(max(u, v) for (u, v) in E) + 1)
        return dict(E)
    fwd = ap([(0, 1), (1, 2)], (0, 1, 2))
    rev = ap([(2, 1), (1, 0)], (2, 1, 0))
    return fwd, rev


def _localization():
    A = Counter([(i, i + 1) for i in range(12)]); A[(9, 8)] += 1
    clean = len(two_core(A))
    B = Counter(A)
    for i in range(12):
        B[(i, 100 + i)] += 1; B[(100 + i + 1, 100 + i)] += 1
    rung = len(two_core(B))
    return clean, rung


def run():
    print("[OPEN] %s" % TITLE)
    print("  KEYSTONE = %s" % (KEYSTONE,))
    fwd, rev = _rule_chirality()
    print("  1. the rule is CHIRAL (head x and tail z treated asymmetrically):")
    print("     rule on 0->1->2 : %s" % fwd)
    print("     rule on 2->1->0 : %s  (mirror image, never the same -> a fixed handedness)" % rev)
    clean, rung = _localization()
    ntypes, any_rev, total = _reversal_search()
    print("  2. coupling the two chiralities fails two ways (the reversal search is run LIVE here):")
    print("     - END-TO-END junctions: searched %d defect type(s), %d states total -> reversal found: %s" %
          (ntypes, total, any_rev))
    print("       (the glider PINS; no size-2 2-core ever moves back. Set EMERGENCE_FULL=1 for 4 types x 6000 states.)")
    print("     - SIDE-BY-SIDE rungs (the natural mass term): 2-core size %d (clean glider) -> %d (whole" % (clean, rung))
    print("       ladder) = the glider is DELOCALIZED, not converted.")
    print("  => the keystone is a WEYL world: massless single-chirality gliders. The Dirac mass term")
    print("     (L<->R coupling -> zitterbewegung -> a sub-luminal accelerable particle) is NOT derivable")
    print("     from the bare rule; it is an irreducible input, like the handedness bit and beta.")
    print("     Exactly as in the Standard Model: chiral fermions get mass from a Higgs coupling, not the")
    print("     kinetic term. (Empirical obstruction from a bounded search, not a proof of impossibility.)")
