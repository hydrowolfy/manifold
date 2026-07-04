"""Maxwell equations / dynamical gauge field (the owed FORCE)

AXIOM/GOAL: Make the U(1) phase dynamical so that opposite charges attract and like charges repel.
APPROACH:   Weight rewriting amplitudes by a charge-responsive Wilson action; charges that can cancel holonomy lower the action. Not started -- this is the missing gauge dynamics.
STATUS:     OPEN
"""
STATUS = "OPEN"
TITLE = "Maxwell equations / dynamical gauge field (the owed FORCE)"
AXIOM = "Make the U(1) phase dynamical so that opposite charges attract and like charges repel."
APPROACH = "Weight rewriting amplitudes by a charge-responsive Wilson action; charges that can cancel holonomy lower the action. Not started -- this is the missing gauge dynamics."


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
