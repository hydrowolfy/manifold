"""Newton's second law on the substrate: why the native force is overdamped (v~F), and what a~F needs.

The force-on-matter mechanism (s4_2_force_coupling) moves the glider charge-dependently but in an
OVERDAMPED regime: velocity ~ force (Aristotelian drift), not acceleration ~ force (Newtonian). This
module finds the STRUCTURAL reason and the path forward, and it ties the answer to the causal speed.

THE NATIVE GLIDER IS A FIXED-SPEED SOLITON. The minimal 2-cycle glider (s4_1) advances exactly one
rail-node per 2-move -- a single propagation speed v0 (the causal speed, 1 node/tick here). The field
coupling can only GATE that motion: each tick the glider hops with probability P(F)=1/(1+exp(beta*dE)),
so its time-averaged velocity is P(F)*v0 -- set INSTANTANEOUSLY by the force, with no memory. Three
measured consequences:

  1. CONSTANT FORCE -> CONSTANT VELOCITY (overdamped v~F). Under a constant field bias the glider holds a
     constant average velocity; it does NOT accelerate. Velocity tracks the force, not its time-integral.
  2. FIXED-SPEED CEILING = THE CAUSAL SPEED. However strong the force, the velocity saturates at v0=1
     node/tick and never exceeds it (P -> 1). The glider is "massless-like": it moves at the substrate's
     one speed, or is gated below it. v0 is a universal speed limit, consistent with the causal cones (s1).
  3. NO VELOCITY MEMORY. Drive the glider hard, then switch the force off: the velocity drops instantly to
     the unbiased baseline (~v0/2). There is no persistent velocity to coast on -- no inertia in SPEED.

So the native force-on-matter is OHMIC/overdamped because the minimal glider has no velocity state to
accumulate; the force gates a fixed-speed motion. This is a precise obstruction to inertial F=ma for this
excitation -- a negative result in the spirit of the round-5 refutation.

WHAT a~F REQUIRES (and the relativistic bonus). Genuine Newtonian inertia needs a velocity-CARRYING
("massive") excitation: an internal momentum p that the force CHANGES (F = dp/dt = alpha*F per tick) and
that PERSISTS on its own. Mapping momentum to velocity by the relativistic relation v = p/sqrt(1+p^2)
(which saturates at the causal speed v0=1) and gating the glider's hop by v, one gets exactly Newtonian
behaviour: under constant force the velocity GROWS over time (a~F) and asymptotes to v0; when the force is
removed the velocity PERSISTS (inertia). The inertial mass is m = 1/alpha.

HONEST STATUS = PARTIAL. The NATIVE finding is the obstruction (1-3 above): the minimal glider is
fixed-speed, so the bare-rule force is overdamped and capped at the causal speed. The a~F demonstration
uses a POSTULATED momentum variable -- an overlay (like the field energy of s6_3), not derived from the
rule. What is genuinely shown: (i) WHY the native dynamics is overdamped (no velocity state), (ii) that
the causal speed is a universal ceiling for any excitation, and (iii) that a~F with finite inertial mass
is recovered by a velocity-carrying excitation, which then asymptotes to v0 -- i.e. a massive particle is
relativistic for free. Building such a "massive" excitation natively (a structured glider with a persistent
sub-luminal speed the force can advance) is the open frontier of the mechanics sector. Pure Python.
"""
import math
import random
from collections import Counter
from sec00_core_substrate import two_core, apply_rule
from constants import KEYSTONE

STATUS = "PARTIAL"
TITLE = "Newton II: native glider is fixed-speed (overdamped v~F, capped at causal speed); a~F needs a massive excitation"


def _core(E):
    tc = two_core(E)
    return min(tc) if len(tc) == 2 else None


def _hop_left(E, n, fresh):
    if E.get((n, n + 1), 0) < 1 or E.get((n + 1, n), 0) < 1 or E.get((n - 1, n), 0) < 1:
        return E, fresh, False
    E, fresh = apply_rule(E, (n - 1, n, n + 1), KEYSTONE, fresh)
    E, fresh = apply_rule(E, (n - 1, n + 1, n), KEYSTONE, fresh)
    return E, fresh, True


def _const_force(dE, ticks=22, seed=0, L=60, release_at=None):
    E = Counter([(i, i + 1) for i in range(L)]); E[(L - 3, L - 4)] += 1; fresh = L + 1
    rng = random.Random(seed); pos = []
    for t in range(ticks):
        x = _core(E)
        if x is None:
            break
        pos.append(x)
        d = 0.0 if (release_at is not None and t >= release_at) else dE
        if rng.random() < 1.0 / (1.0 + math.exp(d)):
            E, fresh, _ = _hop_left(E, x, fresh)
    return pos


def _massive(F, alpha=0.06, ticks=34, seed=0, L=110, release_at=None):
    E = Counter([(i, i + 1) for i in range(L)]); E[(L - 3, L - 4)] += 1; fresh = L + 1
    rng = random.Random(seed); p = 0.0; pos = []
    for t in range(ticks):
        x = _core(E)
        if x is None:
            break
        pos.append(x)
        Ft = 0.0 if (release_at is not None and t >= release_at) else F
        p += alpha * Ft                       # F = dp/dt : force changes a PERSISTENT momentum
        v = p / math.sqrt(1.0 + p * p)        # relativistic map: saturates at the causal speed v0=1
        if rng.random() < max(0.0, min(1.0, v)):
            E, fresh, _ = _hop_left(E, x, fresh)
    return pos


def _avgvel(runs, t0, t1):
    T = min(len(r) for r in runs)
    if T <= t1:
        return None
    a0 = sum(r[t0] for r in runs) / len(runs); a1 = sum(r[t1] for r in runs) / len(runs)
    return (a0 - a1) / (t1 - t0)


def run():
    print("[PARTIAL] %s" % TITLE)
    S = 24
    print("  1. NATIVE glider, constant force -> velocity vs time (overdamped if constant):")
    for dE, label in [(-0.5, "favorable"), (0.0, "no force"), (+1.0, "opposing")]:
        runs = [_const_force(dE, seed=s) for s in range(S)]
        ve = _avgvel(runs, 0, 10); vl = _avgvel(runs, 10, 20)
        if ve is not None and vl is not None:
            tag = "CONSTANT v (overdamped v~F)" if abs(ve - vl) < 0.04 else "accelerating"
            print("     %-9s (dE=%+.1f): v_early=%.3f v_late=%.3f -> %s" % (label, dE, ve, vl, tag))
    print("  2. FIXED-SPEED CEILING = causal speed v0=1 (force cannot push the glider past it):")
    for dE in (-1.0, -4.0, -20.0):
        runs = [_const_force(dE, seed=s) for s in range(S)]
        v = _avgvel(runs, 0, 10)
        print("     dE=%+6.1f (P_hop=%.3f): mean v=%.3f node/tick" % (dE, 1 / (1 + math.exp(dE)), v))
    print("  3. NO velocity MEMORY (drive hard t<10, force OFF t>=10):")
    runs = [_const_force(-4.0, ticks=22, seed=s, release_at=10) for s in range(S)]
    vd = _avgvel(runs, 2, 8); va = _avgvel(runs, 12, 18)
    if vd is not None and va is not None:
        print("     v driven=%.3f  v after release=%.3f -> %s" % (vd, va,
              "DROPS to baseline: no inertia in speed (overdamped)" if va < 0.65 else "persists"))
    print("  => native force-on-matter is OVERDAMPED: a fixed-speed glider with no velocity state.")
    print("  4. a~F WITH a velocity-carrying ('massive') excitation [overlay: postulated momentum, F=dp/dt]:")
    runs = [_massive(1.0, seed=s) for s in range(S)]
    for w in (0, 1, 2):
        v = _avgvel(runs, w * 10, w * 10 + 10)
        if v is not None:
            print("     ticks %2d-%2d: velocity=%.3f" % (w * 10, w * 10 + 10, v))
    runs2 = [_massive(1.0, seed=s, release_at=15) for s in range(S)]
    vb = _avgvel(runs2, 10, 15); vaf = _avgvel(runs2, 25, 30)
    if vb is not None and vaf is not None:
        print("     persistence (force off at t=15): v before=%.3f v after=%.3f -> %s" % (vb, vaf,
              "PERSISTS = inertia (a~F)" if vaf > 0.4 else "decays"))
    print("  => a~F is recovered by a massive excitation (inertial mass m=1/alpha), asymptoting to v0:")
    print("     a massive particle is relativistic for free. Native such an excitation = open frontier.")
