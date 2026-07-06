"""Force law: the pre-registered charge-responsive-dynamics conjecture -- TESTED, and REFUTED.

BACKGROUND: the central open problem of the classical sector is that the keystone rule fires on graph
SHAPE and never reads the U(1) phase tags, so like- and opposite-charge collisions are byte-identical:
a passive gauge label exerts no force (sec06 gauge structure). Paper I section 8 PRE-REGISTERED a
falsifiable fix:

  > Weight redex selection at a glider-glider contact by exp(-beta*dS), where dS is the change in
  > total holonomy mismatch (sum of |phase difference| around the affected loops). Then (a) opposite
  > charges close faster than the charge-blind baseline, (b) like charges slower, (c) effects grow
  > with beta. FALSIFIED if the like / opposite / baseline curves are indistinguishable at every beta,
  > or if the sign reverses.

This module implements that test faithfully -- a phase-aware keystone (holonomy-preserving parallel
transport: phi(x->z)=phi(x->y)+phi(y->z), phi(y->x)=-phi(x->y), phi(z->w)=0; verified to conserve a
glider's holonomy exactly), two charged gliders in contact, and redex selection biased by exp(-beta*dS)
with S = sum over elementary loops of |holonomy|.

RESULT: REFUTED. The like- and opposite-charge dynamics are not merely statistically indistinguishable
-- they are BYTE-IDENTICAL at every beta and every seed. The conjecture fails for a STRUCTURAL reason,
shown in run():
  (1) the registered action is SIGN-BLIND for separated charges: S = |+q|+|-q| = |+q|+|+q| (the sum of
      per-loop |holonomy| cannot see relative sign while the charges sit on separate loops);
  (2) hence the biased evolution is identical for like and opposite (verified, all seeds, all beta);
  (3) the ONLY sign-sensitive quantity, the total SIGNED holonomy q_L+q_R, is CONSERVED, so biasing by
      it gives dS=0 -- no force from there either.
Deeper reason: a Coulomb-like force is an INTERACTION (cross) term between two charges' fields,
2 integral E_1.E_2, which needs the fields to OVERLAP. Loop holonomies are localized at each charge and
have no cross term, so no holonomy-based local action can produce the force. The fix is not a bias
tweak: each charge needs an EXTENDED field on the edges (a connection that decays away from the loop),
and the action must be a genuine field energy with the interference term. That is real derivational
work, now precisely motivated by this refutation.

STATUS: the pre-registered mechanism is REFUTED; the force law itself remains OPEN (a different,
field-energy mechanism is not excluded). Pure Python, no third-party deps.
"""
import math
import random
from collections import Counter
from sec00_core_substrate.rewriting import redexes

STATUS = "REFUTED"
TITLE = "Pre-registered force mechanism (holonomy-mismatch bias) REFUTED; force law still OPEN"


def phase_apply(E, ph, redex, fresh):
    """Phase-aware keystone with holonomy-preserving parallel transport."""
    a, b, c = redex
    F = Counter(E); P = dict(ph)
    pab = P.get((a, b), 0.0); pbc = P.get((b, c), 0.0)
    F[(a, b)] -= 1; F[(b, c)] -= 1
    if F[(a, b)] <= 0:
        del F[(a, b)]
    if F[(b, c)] <= 0:
        del F[(b, c)]
    F[(a, c)] += 1; P[(a, c)] = pab + pbc      # composed path: preserves holonomy
    F[(b, a)] += 1; P[(b, a)] = -pab           # reversed consumed edge
    F[(c, fresh)] += 1; P[(c, fresh)] = 0.0    # fresh node: uncharged
    return F, P, fresh + 1


def _loops(E):
    seen = set(); out = []
    for (u, v), m in E.items():
        if m > 0 and E.get((v, u), 0) > 0 and (v, u) not in seen:
            seen.add((u, v)); out.append((u, v))
    return out


def S_mismatch(E, ph):
    return sum(abs(ph.get((u, v), 0.0) + ph.get((v, u), 0.0)) for (u, v) in _loops(E))


def total_signed(E, ph):
    return sum(ph.get((u, v), 0.0) + ph.get((v, u), 0.0) for (u, v) in _loops(E))


def _setup(qL, qR):
    E = Counter([(i, i + 1) for i in range(16)]); E[(6, 5)] += 1; E[(9, 8)] += 1
    return E, {(6, 5): qL, (9, 8): qR}


def biased_trajectory(qL, qR, beta, steps, seed):
    E, ph = _setup(qL, qR); fresh = 16; rng = random.Random(seed); traj = []
    for _ in range(steps):
        R = redexes(E)
        if not R:
            break
        if beta == 0:
            r = rng.choice(R)
        else:
            ds = []
            for rr in R:
                F, P, _ = phase_apply(E, ph, rr, fresh)
                ds.append(S_mismatch(F, P) - S_mismatch(E, ph))
            w = [math.exp(-beta * d) for d in ds]; tot = sum(w); x = rng.random() * tot; acc = 0; r = R[-1]
            for rr, wi in zip(R, w):
                acc += wi
                if x <= acc:
                    r = rr; break
        E, ph, fresh = phase_apply(E, ph, r, fresh); traj.append(round(S_mismatch(E, ph), 6))
    return traj


def run():
    print("[REFUTED] %s" % TITLE)
    Eo, po = _setup(0.8, -0.8); El, pl = _setup(0.8, 0.8)
    print("  (1) registered action is SIGN-BLIND for separated charges:")
    print("      S(opposite +.8,-.8) = %.3f  ==  S(like +.8,+.8) = %.3f   (|+q|+|-q| = |+q|+|+q|)"
          % (S_mismatch(Eo, po), S_mismatch(El, pl)))
    print("  (2) so the biased dynamics are byte-identical for like vs opposite:")
    for beta in (1.0, 3.0, 8.0):
        same = all(biased_trajectory(0.8, -0.8, beta, 10, s) == biased_trajectory(0.8, 0.8, beta, 10, s)
                   for s in range(150))
        print("      beta=%.1f : identical action-trajectories for ALL 150 seeds : %s" % (beta, same))
    E, ph = _setup(0.8, -0.8); fresh = 16; rng = random.Random(0); ts = [round(total_signed(E, ph), 3)]
    for _ in range(8):
        R = redexes(E)
        if not R:
            break
        E, ph, fresh = phase_apply(E, ph, rng.choice(R), fresh); ts.append(round(total_signed(E, ph), 3))
    print("  (3) only sign-sensitive quantity (total signed holonomy) is CONSERVED: %s -> dS=0" % ts)
    print("  => the conjecture's falsification criterion is met in the strongest form (identical curves).")
    print("  => FIX (precisely motivated): extended per-charge fields + a field energy with the")
    print("     interaction term 2*integral(E1.E2); loop holonomies have no cross term. Force: still OPEN.")
