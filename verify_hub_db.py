import os, random, itertools
os.environ.setdefault("MANIFOLD_REPO", os.getcwd())
import cdt_frontier2_run as m
from collections import Counter

def true_deg(st):
    deg = Counter()
    for e, c in st.ecnt.items():
        if c > 0:
            a, b = tuple(e); deg[a] += 1; deg[b] += 1
    return deg

def full_pen(st, D0):
    deg = true_deg(st)
    return sum((d - D0) ** 2 for d in deg.values() if d > D0)

st = m.seed_state(10)
rng = random.Random(3)
D0 = 14.0
# grow + thermalize a bit so the degree sequence has real hubs
while st.N3 < 1500:
    st.sweep(rng, 2.0, -0.5, 0.002, 1500)
for _ in range(120):
    st.sweep(rng, 2.0, 0.8, 0.002, 1500, 0.0, 0.5, D0)

# instrument _degpen_delta to stash its last return
orig = m.Causal._degpen_delta
last = {}
def patched(self, rems, adds, D0):
    v = orig(self, rems, adds, D0)
    last["v"] = v
    return v
m.Causal._degpen_delta = patched

checked = 0; maxerr = 0.0; cache_ok = True
sigma = 0.5
for _ in range(6000):
    a0 = sum(st.accs.values())
    pen_before = full_pen(st, D0)
    last.clear()
    st.attempt(rng, 2.0, 0.8, 0.002, 1500, 0.0, sigma, D0)
    accepted = sum(st.accs.values()) > a0
    # degree cache must match truth every step
    if dict(st.deg) != dict(true_deg(st)):
        cache_ok = False
    if accepted and "v" in last:
        pen_after = full_pen(st, D0)
        err = abs(last["v"] - (pen_after - pen_before))
        maxerr = max(maxerr, err); checked += 1

print("accepted-move hub-delta checks: %d" % checked)
print("max |_degpen_delta - (pen_after-pen_before)| = %.3e" % maxerr)
print("degree cache == true degree every step: %s" % cache_ok)
print("HUB-TERM DETAILED-BALANCE DELTA VERIFIED" if (checked > 50 and maxerr < 1e-9 and cache_ok)
      else "HUB-TERM DELTA PROBLEM -- investigate")
