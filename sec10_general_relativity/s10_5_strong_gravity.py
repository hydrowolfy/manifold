"""Horizons and the area law

AXIOM/GOAL: Recover black-hole horizons and horizon entropy.
APPROACH:   Holographic area-law scaling of information across causal cuts was observed; full horizon thermodynamics owed.
STATUS:     PARTIAL
"""
STATUS = "PARTIAL"
TITLE = "Horizons and the area law"
AXIOM = "Recover black-hole horizons and horizon entropy."
APPROACH = "Holographic area-law scaling of information across causal cuts was observed; full horizon thermodynamics owed."


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
