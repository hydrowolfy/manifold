import os, random
os.environ.setdefault("MANIFOLD_REPO", os.getcwd())
from cdt_causal_run import seed_state, validate

def counts(st):
    return dict(N0=st.N0, N3=st.N3, T=st.T, N31=st.nk[3], N22=st.nk[2], N13=st.nk[1])

def check(label, st):
    c = counts(st)
    pred_n31 = 2*c["N0"] - 4*c["T"]
    pred_n22 = c["N3"] - 4*c["N0"] + 8*c["T"]
    ok_n31 = (c["N31"] == pred_n31) and (c["N13"] == pred_n31)
    ok_n22 = (c["N22"] == pred_n22)
    ok_sum = (c["N31"] + c["N22"] + c["N13"] == c["N3"])
    print("  [%-24s] N0=%d N3=%d T=%d | N31=%d(pred %d) N13=%d N22=%d(pred %d) | 2N0-4T:%s N3-4N0+8T:%s sum:%s"
          % (label, c["N0"], c["N3"], c["T"], c["N31"], pred_n31, c["N13"], c["N22"], pred_n22, ok_n31, ok_n22, ok_sum))
    return ok_n31 and ok_n22 and ok_sum, c

all_ok = True
for k0 in (2.0, 5.0):
    print("=== k0=%.1f ===" % k0)
    T = 12; st = seed_state(T); rng = random.Random(7)
    ok, c0 = check("seed", st); all_ok &= ok
    target = 2400
    while st.N3 < target:
        st.sweep(rng, k0, -0.5, 0.002, target)
    validate(st, heavy=False)
    ok, cg = check("grown ~%d" % target, st); all_ok &= ok
    for _ in range(300):
        st.sweep(rng, k0, 0.8, 0.002, target, 0.0)
    validate(st, heavy=False)
    ok, ct = check("thermalized +300sw", st); all_ok &= ok
    for lbl, c in (("seed", c0), ("grown", cg), ("therm", ct)):
        resid = c["N22"] - (c["N3"] - 4*c["N0"] + 8*c["T"])
        assert resid == 0, "IDENTITY VIOLATED at %s k0=%.1f resid=%d" % (lbl, k0, resid)
    dN0 = ct["N0"] - cg["N0"]; dN3 = ct["N3"] - cg["N3"]; dN22 = ct["N22"] - cg["N22"]
    if dN0 != 0:
        slope = (dN22 - dN3) / dN0
        print("  grown->therm: dN0=%d dN3=%d dN22=%d -> (dN22-dN3)/dN0=%.4f (must be -4)" % (dN0, dN3, dN22, slope))
        assert abs(slope + 4.0) < 1e-9, "slope != -4"
    print()
print("IDENTITY VERIFIED EXACTLY (integer) on all states." if all_ok else "IDENTITY FAILED")
