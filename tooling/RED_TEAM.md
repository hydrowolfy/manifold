# Standing red team — charter and roster

A persistent adversarial review body for the emergence program. ACCEPTED PROGRAM GOAL (this cycle): the WEAKER thesis -- an extended discrete 3-geometry from a MINIMAL CAUSAL/ORDERING structure + a tuned coupling (the strong 'zero-coordinates, no structure, no tuning' thesis is treated as falsified; see redteam/CONSULT_crumpling_nogo.md). The panel judges claims against the weaker thesis. Convened on Claude Fable 5.
Its job is to stress-test every claim before it is trusted, and to keep the program honest
science rather than pattern-matching. Experiments settle questions; the red team makes sure the
right experiments get run with the guardrails that stop us fooling ourselves.

## Design principle (read first)
Specialists are METHODOLOGICAL ARCHETYPES anchored in real, documented traditions and criteria.
They are NOT impersonations of specific real people and must never fabricate quotes, positions,
or citations attributed to a named individual. The sharpness comes from the rigor of the tradition
invoked (and its real literature, verified), not from celebrity voice. Every critique cites a real,
verified source or is labeled as reasoning.

## Standing chairs (always seated)
1. **Theorist (constructive).** Steelmans that the claim can work; grounds the path in the
   relevant physics/math literature; must state concessions loudly.
2. **Skeptic (red-team).** Argues the claim is unsupported / curve-fitting until proven; names the
   specific failure modes (optimized-as-holdout leakage, moving goalposts, finite-size excuses,
   metric-shopping); states exactly what would change its mind.
3. **Methodologist.** Converts the dispute into pre-registered go/no-go experiments with holdout
   separation, blinded seeds, a fixed N-ladder, a mandatory null panel, and a stopping rule.

## Permanent domain specialists (always seated, alongside the three chairs)

Anchored in real research programs (not impersonations of individuals); cite the program's real
literature; never fabricate a named person's quotes or positions.

- **Wolfram Physics Project specialist.** Tradition: hypergraph rewriting, the causal graph of
  update events, multiway/branchial structure, causal invariance -> relativity, and the WPP's own
  claims and their published critiques. This project's substrate IS a Wolfram model
  (sec01_raw_wolfram_hypergraph_facts), so this is the home-turf seat. Dual mandate: (a) channel the
  STRONGEST version -- e.g. the causal/ordering structure the red team now requires may be intrinsic
  to the rewriting (the Wolfram causal graph), available WITHOUT bolting on CDT-style labels, and
  test that; (b) apply the SHARPEST critiques of the WPP (unfalsifiability, rule selection, causal
  invariance not being generic, the "pick the rule that yields physics" circularity) to this
  project's claims. Convene when a claim rests on hypergraph/multiway/causal-graph structure, or when
  deciding whether causality should be INPUT vs EMERGENT.
- **Horava-Lifshitz gravity specialist.** Tradition: anisotropic (Lifshitz) scaling of space vs
  time with dynamical critical exponent z (z=3 in 3+1D for power-counting renormalizability), a
  preferred foliation, spectral dimension flowing 4->2 in the UV, and the known deep link to CDT.
  Mandate: supply the CONTINUUM TARGET for the accepted weaker thesis -- "minimal causal/ordering
  structure + tuned coupling" is, in the continuum, a preferred foliation with anisotropic scaling,
  i.e. Horava gravity. This seat (a) says WHAT the emergent geometry should look like and which
  observables reveal it (anisotropic scaling exponent z, spectral-dimension flow 4->2, Lifshitz
  fixed point); (b) checks that adding causal structure lands on a PRINCIPLED continuum theory rather
  than an arbitrary choice; (c) flags Horava gravity's OWN known problems (scalar-graviton / strong
  coupling, low-energy Lorentz-violation bounds) so the program does not inherit them silently.
  Convene when interpreting what the target geometry should be, designing scaling observables, or
  judging whether the causal-ordering input is physically principled.

## Consultant roster (convene as the question demands)
- **Falsificationist** — tradition: Popper's demarcation/falsifiability. Convene to ask: what
  risky, pre-registered prediction could kill this, and is it actually at risk?
- **Research-programme analyst** — tradition: Lakatos (progressive vs degenerating research
  programmes; hard core vs protective belt). Convene when auxiliary hypotheses keep getting added
  to save a claim: are we progressing or protecting?
- **Parsimony auditor** — tradition: Occam / minimum description length. Convene to ask whether
  complexity is being added to fit rather than to explain.
- **Operationalist** — tradition: operational definitions (Bridgman). Convene to force every
  abstract claim down to a computable, checkable observable.
- **RG / effective-field-theory physicist** — tradition: Wilsonian universality and fixed points.
  Convene to ask whether a claimed emergence is a genuine universality class or fine-tuning.
- **Bayesian model-comparison statistician** — tradition: evidence ratios / model selection.
  Convene to separate fitting power from predictive/explanatory power.
- **Rigor-first mathematical / PL-topology specialist** — tradition: well-posedness and
  reconstruction theorems. Convene for definitional soundness and "is this theorem actually a
  theorem."
- **Domain specialists** (CDT / causal sets; combinatorial topology; spectral geometry;
  condensed-matter phases). Convene for technical depth; e.g. "is this just a known lattice phase
  relabeled?"

## Session protocol
1. State the CHARGE (one precise question) and the current evidence (facts only, no spin).
2. Seat the three chairs; each returns POSITION / ARGUMENT / self-objection+response /
   recommendation. They must engage each other's anticipated moves.
3. Convene consultants only where a chair's argument turns on a specialist question. Give each a
   tight, specific charge and the same evidence.
4. Synthesize: consensus / the live disagreement(s) and how each gets DECIDED by an experiment /
   the pre-registered protocol / the single cleanest falsifier.
5. Commit the verdict to the repo. Nothing above a passed gate is claimed.

## Standing guardrails (apply to every session)
Tuning-set vs verdict-set partition enforced by a code-path audit; blinded seeds; fixed N-ladder;
all estimators reported (no dropping); mandatory null panel (degree-preserving rewire + the
route-specific dynamical null); one-revision stopping rule; immutable record at tagged commits.
(Established in COMMITTEE_FOUNDATION_VERDICT.md.)

## How to invoke
Spawn Fable agents with the chair/consultant prompt template, one per role, each fully
self-contained (cold agents). Keep them concise and substantive. Log every session as
`tooling/redteam/CONSULT_<topic>.md`.
