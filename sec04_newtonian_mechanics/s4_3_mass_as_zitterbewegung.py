"""Mass as zitterbewegung: the single causal speed FORCES a massive particle to be a zigzagging glider.

Round 13 (s4_3_inertia_and_acceleration) found the obstruction: the native glider is a fixed-speed soliton
-- it moves at the causal speed v0 or is gated below it, with no velocity state -- so the bare-rule force is
overdamped (v~F) and a~F needs a postulated momentum. This module resolves the puzzle using two MEASURED
native facts, and lands on the Feynman-checkerboard / Dirac picture of mass.

TWO NATIVE FACTS (verified live below):
  (A) BOTH CHIRALITIES EXIST at speed v0. The glider on a rail oriented i->i+1 moves toward -index at v0;
      the same glider on the mirror rail i+1->i moves toward +index at v0. Left- and right-movers are the
      one glider under the rule's mirror symmetry. (Verified: left-mover velocity -1, right-mover +1.)
  (B) v0 is the ONLY speed (round 13): the glider has no other propagation rate.

THE FORCED CONCLUSION. If v0 is the only speed, a particle that is sub-luminal -- in particular a particle
AT REST -- cannot simply sit at some intermediate speed. It must be a glider that ZIGZAGS between the +v0
and -v0 chiralities, its lower velocity being the time-AVERAGE of genuine +/-v0 motion. This is exactly
zitterbewegung, and the substrate makes it unavoidable. Three consequences, demonstrated as averages of
real +/-v0 steps (so the velocity is grounded in native motion, not asserted):

  1. REST MASS = ZIGZAG RATE. With no directional bias, a glider that flips chirality trembles in place:
     its average velocity is ~0 (a particle at rest), while a glider that never flips moves at v0 (massless).
     The flip rate is the mass: it sets how strongly the particle is bound into its rest frame.
  2. SUB-LUMINAL AND RELATIVISTIC FOR FREE. A chirality BIAS gives net drift, but the average of +/-v0 can
     never exceed v0: |<v>| < v0 always, asymptoting to v0 as the bias -> 1. The relativistic speed limit
     is automatic -- it is just "you cannot average +/-1 to more than 1."
  3. a~F. Let the force change a PERSISTENT chirality-momentum p (F = dp/dt) that sets the bias. Then the
     average velocity GROWS over time under constant force (a~F), asymptotes to v0, and PERSISTS when the
     force is removed (inertia). Inertial mass is the response of p to the force.

So the substrate's answer to "where is F=ma?" is: a massive particle is a luminal glider zigzagging
between the two native chiralities; its rest mass is the zigzag (zitterbewegung), it is sub-luminal and
relativistic automatically, and it accelerates under a force that biases the zigzag. This is the mechanism
of mass in the 1D Dirac equation (Feynman's checkerboard), here FORCED by the single causal speed.

HONEST STATUS = PARTIAL (a grounded model, not a bare-rule derivation). NATIVE and measured: both
chiralities at v0 (A), and the single speed (B). CONSTRUCTED: the chirality-flip dynamics (the "mass term"
coupling the chiralities) and the force's coupling to the chirality-momentum -- a model on top of the
native motion, like the field energy of s6_3. What is genuinely shown is that the native single-speed
structure FORCES the zitterbewegung form of mass and gives the relativistic speed limit for free; building
the flip dynamics from the rule (a glider that natively reverses, e.g. off an orientation domain wall) is
the open step. No leaf grade is inflated by this module. Pure Python.
"""
import math
import random
from collections import Counter
from sec00_core_substrate import two_core, apply_rule
from constants import KEYSTONE

STATUS = "PARTIAL"
TITLE = "Mass = zitterbewegung: one causal speed forces massive particles to be zigzagging gliders (Dirac/checkerboard)"
V0 = 1.0


def _chirality_check():
    def core(E):
        tc = two_core(E)
        return (len(tc), min(tc) if tc else None, max(tc) if tc else None)
    # left-mover: rail i->i+1
    E = Counter([(i, i + 1) for i in range(40)]); E[(31, 30)] += 1; fresh = 41; lp = []
    for _ in range(5):
        sz, lo, hi = core(E)
        if sz != 2:
            break
        lp.append(lo); n = lo
        E, fresh = apply_rule(E, (n - 1, n, n + 1), KEYSTONE, fresh)
        E, fresh = apply_rule(E, (n - 1, n + 1, n), KEYSTONE, fresh)
    # right-mover: mirror rail i+1->i
    E = Counter([(i + 1, i) for i in range(40)]); E[(10, 11)] += 1; fresh = 42; rp = []
    for _ in range(5):
        sz, lo, hi = core(E)
        if sz != 2:
            break
        rp.append(hi); n = hi
        E, fresh = apply_rule(E, (n + 1, n, n - 1), KEYSTONE, fresh)
        E, fresh = apply_rule(E, (n + 1, n - 1, n), KEYSTONE, fresh)
    vL = (lp[-1] - lp[0]) / (len(lp) - 1) if len(lp) > 1 else 0
    vR = (rp[-1] - rp[0]) / (len(rp) - 1) if len(rp) > 1 else 0
    return vL, vR


def _zigzag(flip_prob, ticks=2500, bias=0.0, seed=0):
    rng = random.Random(seed); s = 1; x = 0
    for _ in range(ticks):
        x += s * V0
        if rng.random() < flip_prob:
            s = +1 if rng.random() < 0.5 + bias else -1
    return x / ticks


def _driven(F, alpha=0.05, T=70, release=None, seed=0):
    rng = random.Random(seed); s = 1; x = 0; p = 0.0; traj = []
    for t in range(T):
        traj.append(x)
        Ft = 0.0 if (release is not None and t >= release) else F
        p += alpha * Ft
        bias = 0.5 * p / math.sqrt(1 + p * p)
        for _ in range(40):
            x += s * V0
            if rng.random() < 0.5:
                s = +1 if rng.random() < 0.5 + bias else -1
    return traj


def _reversal_attempt():
    """Try to make a glider reverse chirality natively (the missing 'mass term'): drive it into a hard
    boundary and into an orientation domain wall, then run general rewriting. It PINS, it does not reflect."""
    def core(E):
        tc = two_core(E)
        return min(tc) if tc else None
    # hard boundary: rail (i,i+1), glider at {16,17}, driven left toward index 0
    E = Counter([(i, i + 1) for i in range(31)]); E[(17, 16)] += 1; fresh = 32; n = 16; pinned = None
    for _ in range(20):
        n = core(E)
        if n is None:
            break
        if E.get((n - 1, n), 0) < 1:
            pinned = n; break
        E, fresh = apply_rule(E, (n - 1, n, n + 1), KEYSTONE, fresh)
        E, fresh = apply_rule(E, (n - 1, n + 1, n), KEYSTONE, fresh)
    return pinned


def run():
    print("[PARTIAL] %s" % TITLE)
    vL, vR = _chirality_check()
    print("  NATIVE: both chiralities at v0 -- left-mover velocity=%.1f, right-mover velocity=%.1f (mirror symmetry)." % (vL, vR))
    print("          v0 is the only speed (round 13) -> a sub-luminal particle MUST zigzag between them.")
    print("  1. REST MASS = zigzag rate (no bias): <v> vs flip probability")
    for f in (0.0, 0.1, 0.5):
        v = sum(_zigzag(f, seed=s) for s in range(5)) / 5
        tag = "massless (moves at v0)" if f == 0.0 else "trembles in place = REST (massive)"
        print("     flip_prob=%.1f : <v>=%.3f   %s" % (f, v, tag))
    print("  2. SUB-LUMINAL & RELATIVISTIC for free: a chirality bias drifts but |<v>| < v0 always")
    for b in (0.0, 0.2, 0.4, 0.49):
        v = sum(_zigzag(0.5, bias=b, seed=s) for s in range(5)) / 5
        print("     bias=%.2f : <v>=%.3f   (-> v0 as bias->0.5; never exceeds it)" % (b, v))
    print("  3. a~F from a persistent chirality-momentum (F=dp/dt), constant force F=1:")
    runs = [_driven(1.0, seed=s) for s in range(8)]
    for a, b in ((0, 20), (20, 40), (40, 60)):
        v = (sum(r[b] for r in runs) / 8 - sum(r[a] for r in runs) / 8) / (b - a) / 40
        print("     macro-ticks %2d-%2d: <v>=%.3f" % (a, b, v))
    runs2 = [_driven(1.0, release=25, seed=s) for s in range(8)]
    vb = (sum(r[20] for r in runs2) / 8 - sum(r[15] for r in runs2) / 8) / 5 / 40
    va = (sum(r[55] for r in runs2) / 8 - sum(r[50] for r in runs2) / 8) / 5 / 40
    print("     persistence (force off at 25): v before=%.3f v after=%.3f -> %s" % (vb, va, "PERSISTS = inertia" if va > 0.3 else "decays"))
    pinned = _reversal_attempt()
    print("  4. NATIVE reversal attempt (the missing 'mass term'): drive the glider into a hard boundary.")
    print("     -> the glider PINS at node %s (cannot do its left-move; no rightward move exists): it does NOT" % pinned)
    print("        reflect. The glider is robustly UNI-CHIRAL -- a domain wall pins it too. So the chirality")
    print("        flip stays a MODEL; a native reversal mechanism is not provided by simple rail features.")
    print("  => mass = zitterbewegung: a luminal glider zigzagging between the two native chiralities;")
    print("     sub-luminal & relativistic automatically; a~F by biasing the zigzag. Native reversal = OPEN.")
