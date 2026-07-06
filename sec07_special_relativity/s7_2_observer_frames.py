"""Special relativity assembly (Lorentz BORROWED; completeness PARTIAL)

AXIOM/GOAL: Assemble special relativity from causal invariance, light cones and velocity structure.
APPROACH:   The Lorentz bridge is BORROWED (Gorard: causal invariance => local Lorentz, in WHATEVER
            emergent dimension the rule produces -- the argument is dimension-agnostic). Light cones
            and a matter velocity are PARTIAL. Completeness checks are incomplete.
STATUS:     PARTIAL
NOTE (corrected v8.1): earlier wording ("complete in 3+1", "the keystone 3+1") was inconsistent with
this program's OWN dimension result. The keystone's measured spatial dimension is non-integer (~2.3-
2.5), NOT 3, and the program's headline finding is precisely that 3+1 is NOT selected (dimension is a
free, generically-fractional input). There is nothing "3+1" about the keystone or about the Lorentz
bridge, which holds in whatever dimension emerges. The "3+1" framing is removed.
"""
STATUS = "PARTIAL"
TITLE = "Special relativity assembly (Lorentz borrowed; completeness partial; NOT tied to 3+1)"
AXIOM = "Assemble special relativity from causal invariance, light cones and velocity structure."
APPROACH = "Lorentz bridge BORROWED (Gorard, dimension-agnostic); light cones + matter velocity PARTIAL; completeness incomplete. The keystone dimension is ~2.3-2.5, not 3+1."


def run():
    print("[%s] %s" % (STATUS, TITLE))
    print("  goal:     " + AXIOM)
    print("  approach: " + APPROACH)
    _note = {
        "OPEN": ">> Not yet derived. Target and approach recorded; no result is claimed.",
        "BORROWED": ">> Relies on an external theorem; not re-derived inside this program.",
        "CONJECTURE": ">> Proposed but untested. No numerical support yet.",
        "PARTIAL": ">> A partial result exists; the full derivation is incomplete (see whitepaper).",
    }.get(STATUS)
    if _note:
        print("  " + _note)
