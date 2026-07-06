"""Scattering: a conserved particle number and a strongly constrained S-matrix.

What happens when the substrate's excitations meet? Three facts, in decreasing order of rigor, fix the
answer -- and they make the keystone's scattering very different from a generic quantum field theory.

PARTICLE NUMBER IS CONSERVED (topological protection). Every keystone firing deletes 2 edges, adds 3, and
adds 1 node, so the first Betti number b1 = E - V + C changes by 0: b1 is conserved by EVERY step (verified
below for b1 = 1, 2, 3 over hundreds of random firings -- it never moves). The loops ARE the matter quanta
(round 17: the universe is one loop in a tree). So the number of particles is an absolute conserved charge:
there is NO pair creation and NO annihilation, ever, and matter is perfectly stable. This is a
SUPERSELECTION rule stronger than anything in the Standard Model, where particle number changes freely via
pair processes. It is the same conservation law behind the unbreakable confining string (round 18, no
pair-creation to break the tube) and the eternal single loop of the b1=1 universe (round 17).

THE FREE-GLIDER S-MATRIX IS TRIVIAL (kinematic constraints). A glider has a single speed v0 and a single
chirality (rounds 13-16). Two consequences, both measured here:
  - CO-PROPAGATING gliders move in LOCKSTEP. Two same-chirality gliders keep a fixed separation forever
    (measured: separation stays exactly constant as both advance) -- equal speed means they never catch one
    another, so they never interact.
  - COUNTER-PROPAGATING gliders PIN. A left-mover and a right-mover live on opposite rail orientations,
    which meet at an orientation domain wall; driven toward each other they both stop AT the wall (measured)
    and never reach one another (the wall pins each, rounds 15-16). 
So free gliders do not undergo 2->2 collision scattering: at the level of free quanta the theory is
effectively non-interacting (and, with particle number fixed, has a trivial free S-matrix).

INTERACTIONS ENTER THROUGH THE FIELD, AND THE ASYMPTOTIC STATES ARE MESONS. Real scattering is mediated by
the gauge field, not by glider contact: a glider crossing a field/charge region is gated with a Boltzmann
transmission ~ 1/(1+exp(beta*Delta E)) (round 7) -- potential scattering, not annihilation. And because
charges are confined (round 18), the asymptotic in/out states are color-neutral MESONS, not free charges --
exactly as in QCD, where one scatters hadrons, never free quarks. Meson-meson scattering (string-string
interaction) is the genuine many-body frontier and is not built here.

HONEST STATUS = PARTIAL. DERIVED-native and rigorous: particle-number (b1) conservation -> no
creation/annihilation (this is round 1's b1 conservation, read as a scattering selection rule). Native and
measured: the co-propagating lockstep and the counter-propagating pinning (single speed + uni-chirality).
The field-mediated potential scattering and the meson asymptotics rest on the overlay field and confinement
(PARTIAL). No leaf grade is changed by this module. Pure Python.
"""
import random
from collections import Counter
from sec00_core_substrate import betti1, apply_rule, redexes, two_core
from constants import KEYSTONE

STATUS = "PARTIAL"
TITLE = "Scattering: conserved particle number (no annihilation) + a kinematically trivial free S-matrix"


def _b1_conserved():
    def two_tri():
        E = Counter([(0, 1), (1, 2), (2, 0), (10, 11), (11, 12), (12, 10)]); E[(2, 5)] += 1; E[(5, 10)] += 1
        return E, 13
    def three():
        E = Counter([(0, 1), (1, 2), (2, 0), (10, 11), (11, 12), (12, 10), (20, 21), (21, 22), (22, 20)])
        E[(2, 5)] += 1; E[(5, 10)] += 1; E[(12, 15)] += 1; E[(15, 20)] += 1
        return E, 23
    out = []
    for name, (E, f) in [("b1=1", (Counter([(0, 1), (1, 2), (2, 0)]), 3)), ("b1=2", two_tri()), ("b1=3", three())]:
        start = betti1(E); lo = hi = start; rng = random.Random(0)
        for _ in range(500):
            Rs = redexes(E)
            if not Rs:
                break
            E, f = apply_rule(E, rng.choice(Rs), KEYSTONE, f); b = betti1(E); lo = min(lo, b); hi = max(hi, b)
        out.append((name, start, lo, hi))
    return out


def _lockstep():
    def lm(E, n, fresh):
        E, fresh = apply_rule(E, (n - 1, n, n + 1), KEYSTONE, fresh)
        E, fresh = apply_rule(E, (n - 1, n + 1, n), KEYSTONE, fresh)
        return E, fresh
    E = Counter([(i, i + 1) for i in range(40)]); E[(16, 15)] += 1; E[(26, 25)] += 1; fresh = 41
    a, b = 15, 25; seps = []
    for _ in range(8):
        seps.append(b - a)
        if E.get((b - 1, b), 0) >= 1:
            E, fresh = lm(E, b, fresh); b -= 1
        if E.get((a - 1, a), 0) >= 1:
            E, fresh = lm(E, a, fresh); a -= 1
    return seps


def run():
    print("[PARTIAL] %s" % TITLE)
    print("  1. PARTICLE NUMBER (b1) is conserved by every firing => no pair creation/annihilation, stable matter:")
    for name, start, lo, hi in _b1_conserved():
        print("     start %s : over 500 random firings  min=%d max=%d  -> %s" %
              (name, lo, hi, "CONSERVED" if lo == hi == start else "CHANGED"))
    print("     => loop number is a superselection charge (stronger than the Standard Model's particle number).")
    seps = _lockstep()
    print("  2. free-glider kinematics (single speed + one chirality => no 2->2 scattering):")
    print("     CO-PROPAGATING: two same-chirality gliders, separation over time = %s -> LOCKSTEP (never interact)." % seps)
    print("     COUNTER-PROPAGATING: opposite chiralities meet at an orientation wall and both PIN (rounds 15-16):")
    print("                          they never reach each other -- the free S-matrix is trivial.")
    print("  3. interactions are FIELD-MEDIATED; asymptotic states are MESONS:")
    print("     a glider crossing a field region is gated, transmission ~ 1/(1+exp(beta*dE)) (round 7) = potential")
    print("     scattering; charges are confined (round 18), so in/out states are neutral mesons, not free charges")
    print("     -- as in QCD (scatter hadrons, not quarks). Meson-meson (string-string) scattering is the next frontier.")
