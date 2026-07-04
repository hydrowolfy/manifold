"""Complex amplitudes / path sum

AXIOM/GOAL: Assign complex amplitudes by summing over rewriting paths.
APPROACH:   Reversibility implies reflection positivity, then Osterwalder-Schrader reconstruction yields the quantum i. Relied upon.
STATUS:     BORROWED
"""
STATUS = "BORROWED"
TITLE = "Complex amplitudes / path sum"
AXIOM = "Assign complex amplitudes by summing over rewriting paths."
APPROACH = "Reversibility implies reflection positivity, then Osterwalder-Schrader reconstruction yields the quantum i. Relied upon."


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
