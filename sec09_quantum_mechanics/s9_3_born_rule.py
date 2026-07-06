"""The Born rule

AXIOM/GOAL: Recover probabilities equal to amplitude modulus squared.
APPROACH:   OS reconstruction supplies the Hilbert inner product and Born weights; relied upon, not independently derived.
STATUS:     BORROWED
"""
STATUS = "BORROWED"
TITLE = "The Born rule"
AXIOM = "Recover probabilities equal to amplitude modulus squared."
APPROACH = "OS reconstruction supplies the Hilbert inner product and Born weights; relied upon, not independently derived."


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
