"""A dark-matter analogue

AXIOM/GOAL: Seek a gravitating but non-interacting residue.
APPROACH:   Conjecture: pruned measurement branches leave charge/structure that still curves the causal graph but does not interact. Speculative.
STATUS:     CONJECTURE
"""
STATUS = "CONJECTURE"
TITLE = "A dark-matter analogue"
AXIOM = "Seek a gravitating but non-interacting residue."
APPROACH = "Conjecture: pruned measurement branches leave charge/structure that still curves the causal graph but does not interact. Speculative."


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
