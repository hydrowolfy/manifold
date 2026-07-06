"""Attacking beta -- the one residual of the round-8 derivation -- and the honest answer: within the
present construction it is an independent parameter, not fixed by the bare rule or the field-energy overlay.

Round 8 derived the field coupling from the keystone rule down to a SINGLE constant beta (the field
operator, the charge rho=in-out, and the Boltzmann form are all the rule's own). The natural hope was
that the amplitude track (`The-Price-of-an-Amplitude`, which already weights rewriting histories and buys
the quantum `i` from reversibility) might also induce beta, closing the derivation completely.

It does not -- and this module shows WHY, with three independent arguments and a demonstration. The result
is a clean NEGATIVE, in the spirit of the round-5 refutation: beta is independent within this
constant -- the price of the electromagnetic force -- which must be POSSESSED, not derived.

THE DEMONSTRATION: a charged glider's drift under the Glauber coupling P(hop)=1/(1+exp(beta*dE)). At
beta=0 the bias is 1/2 -- no force at all; the entire force is the deviation of beta from 0. So the
question "why is there a force" is exactly "why is beta != 0".

THREE INDEPENDENT REASONS beta is not fixed by the rule OR the current construction (this is NOT a proof
that no deeper principle -- a finer rule, a branchial/amplitude consistency condition, a continuum or RG
fixed point, unitarity, anomaly cancellation -- could ever fix it; that question is OPEN):
  (1) beta IS AN INVERSE TEMPERATURE. The keystone is *defined* by UNIFORM redex selection -- that is the
      beta=0, infinite-temperature state: maximum entropy, no energy bias, provably no force. A finite
      beta is a finite temperature, which the bare rule does not specify. (Consistent with round 3: at
      infinite T the equilibrium is pi~degree with no energy tilt; finite beta would tilt it.)
  (2) beta IS A TWO-BODY COUPLING. It multiplies the field energy, which carries the cross/interference
      term 2<E1,E2> between charges. The rule's one-body generator (the Laplacian, round 3) has no
      two-body term; one-body kinematics makes fields superpose, so there is no force at ANY temperature
      unless beta is added by hand. beta is orthogonal to everything the generator fixes.
  (3) THE FORCE IS CLASSICAL. It is a static field energy plus a real Glauber drift -- no `i`. The
      amplitude track buys the quantum `i` (e^{-iHt} propagation vs e^{-Ht} diffusion), which is about
      KINEMATICS, not interaction. A Coulomb/confining force survives the classical limit, so the `i`
      cannot supply beta. The amplitude buys the `i`; it does not buy the coupling.

This MIRRORS the program's own amplitude-track conclusion: there, the chiral handedness "must be
possessed, not derived." The analogy is suggestive but NOT a theorem of impossibility: it says beta is
unconstrained by what is currently built, not that it is unconstrainable in principle
a measured input in real physics. (An additional honesty note surfaced: the round-6/7 force uses the
*instantaneous* global field energy, i.e. the electrostatic limit, which is non-local; a strictly local
rule permits at most a RETARDED, mediated force -- radiation/magnetism, the still-OPEN §6.4/§6.6.)

STATUS = PARTIAL: the derivation is complete up to beta, and beta is shown to be independent within the
present construction (not fixed by the bare rule or the overlay) -- whether a deeper principle fixes it is OPEN,
not a gap to be closed -- the honest terminus. Pure Python.
"""
import math
import random
from collections import Counter
from sec00_core_substrate import two_core
from sec00_core_substrate.rewriting import apply_rule
from constants import KEYSTONE

STATUS = "PARTIAL"
TITLE = "The coupling beta is independent within the present construction (3 reasons; deeper fixing is OPEN)"


def _drift(q, Q, beta, x0=34, Qpos=2, ticks=40, seed=0):
    E = Counter([(i, i + 1) for i in range(x0 + 6)]); E[(x0 + 1, x0)] += 1; fresh = x0 + 7
    rng = random.Random(seed); dE = 0.5 * q * Q
    for _ in range(ticks):
        x = two_core(E)
        if len(x) != 2:
            break
        n = min(x)
        if n - 1 <= Qpos:
            break
        if rng.random() < 1.0 / (1.0 + math.exp(beta * dE)):
            E, fresh = apply_rule(E, (n - 1, n, n + 1), KEYSTONE, fresh)
            E, fresh = apply_rule(E, (n - 1, n + 1, n), KEYSTONE, fresh)
    x = two_core(E)
    return min(x) if len(x) == 2 else None


def run():
    print("[PARTIAL] %s" % TITLE)
    print("  the whole force is the deviation of beta from 0 (= deviation of temperature from infinity):")
    for beta in (0.0, 1.0, 2.0, 4.0):
        o = [p for p in (_drift(+1, -1, beta, seed=s) for s in range(40)) if p]
        print("    beta=%.1f : opposite glider final pos = %.1f%s"
              % (beta, sum(o) / len(o), "   (beta=0: P(hop)=1/2, NO force)" if beta == 0 else ""))
    print("  beta is independent within the present construction -- three reasons (deeper fixing remains OPEN):")
    print("    (1) beta is an INVERSE TEMPERATURE; the keystone's uniform firing IS beta=0 (infinite T),")
    print("        provably forceless. A finite beta = a temperature the bare rule does not specify.")
    print("    (2) beta is a TWO-BODY coupling (it multiplies the field energy's cross term); the rule's")
    print("        one-body generator (Laplacian, round 3) has none -> fields superpose, no force.")
    print("    (3) the force is CLASSICAL (static energy + real Glauber drift, no `i`); the amplitude")
    print("        track buys the quantum `i` (kinematics), which cannot supply a classical coupling.")
    print("  => beta is unconstrained by what is currently built (NOT proven unconstrainable in principle) --")
    print("     amplitude track's own handedness verdict and alpha in physics. The derivation closes here.")
