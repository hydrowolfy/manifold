# Literature cross-check: our 2+1D causal-CDT joint-(d_H,d_s) negative vs the published field

Focused survey answering: does published 2+1D CDT have an extended de Sitter phase, under what
criterion does the field call the geometry "3-dimensional / successful," and how does our specific
negative (no JOINT match of d_H AND d_s to a regular flat-3-torus benchmark, across six lever
families) sit against that. Method: WebSearch + arXiv. Every external claim is tagged with an arXiv
ID. Where a source could not be fetched directly, that is flagged; nothing is invented.

Sourcing note: arXiv's HTML abstract pages timed out repeatedly this session; one direct fetch
succeeded (1711.02685, quoted verbatim below). All other arXiv claims are corroborated through
WebSearch result summaries of the abstracts/journals, not a direct read of the PDF -- treat the
qualitative statements as solid and any *exact* number I did not personally read as flagged.

---

## 0. Our result, stated precisely (the thing being cross-checked)

Genuine 2+1D causal CDT on S^2 x S^1: typed (3,1)/(2,2)/(1,3) tetrahedra, five foliation-preserving
Pachner moves, Regge action, CDT asymmetry alpha=1 (k22=0 baseline), census bad=0 in every snapshot.
Benchmark = exact flat Kuhn T^3 (a *regular crystalline* flat 3-manifold, uniform vertex degree 14,
profile CV 0), size-matched by N0 and read with the SAME seed-averaged estimators. On those estimators:

- Benchmark flat T^3:  d_s(8-24) = 3.10-3.15,  d_s(16-48) ~ 3.0,  d_H(2-6) = 2.47-2.58.
- Causal baseline (k0=2, k22=0, V6000 T12, the field's *extended* phase -- see Sec 1):
  d_s(8-24) ~ 3.2-3.5 (at/above benchmark),  d_H(2-6) ~ 1.68-1.82 (ratio 0.68-0.73, well below),
  heavy-tailed hubs deg_max 79-84 (vs the flat 14).

The joint gate (G1 census clean, G2 d_H ratio >= 0.90, G3 |d_s(8-24) - 3.13| <= 0.20, G4 no
condensation, G5 equilibrium) is never met simultaneously. Six independent lever families each move
BOTH dimensions but only ALONG one anticorrelated tradeoff line, crossing the two benchmark
conditions far apart:

1. aspect / slice size s=N3/T: d_s=bench at s~385, d_H=bench at s~1940 (~5x apart), V-independent;
2. the whole k0 x k22 plane: lowering f22 fixes d_s but decouples slices and condenses -> d_H drops;
3. a local hub-cap measure term sigma: d_s crosses at sigma~0.007, d_H at sigma~0.08 (~10x apart);
4. spatial topology (S^2 -> T^2): identical failing corner reappears;
5. a non-local profile-uniformity term (NL-P): orthogonal to the wall;
6. a non-local symmetric degree counter-term (NL-D): d_H saturates ~0.85 while d_s collapses.

When the levers are pushed hard enough to lift d_H onto/above the flat benchmark, d_s collapses to
~2.0-2.2. Structural root (proven, exact): the per-slice Euler identity forces
N22 = N3 - 4 N0 + 4*chi*T, whose differential dN22 = -4 dN0 is topology-independent -- spatial-vertex
density and the (2,2) "stitching" are ONE locked DOF, so no foliation-preserving move can regularize
the 1-skeleton toward the flat crystal at fixed volume. The flat joint 3-manifold *exists* in the
ensemble (it is literally the benchmark's geometry) but is entropically unselected: the typical
causal geometry is hub-rich and walk-confining.

---

## 1. Does 2+1D CDT have an extended, de Sitter-like phase? YES -- established.

**Where in the phase diagram.** The 3D CDT phase space is (k0, k3) with the bare cosmological
constant k3 fine-tuned to criticality, leaving a one-parameter line in k0 (bare inverse Newton
constant). For a *range of k0* the path integral is dominated by non-degenerate, extended,
three-dimensional geometries -- a dynamically generated ground state of extended geometry. As k0
increases there is a (first-order) transition to a *degenerate* phase in which neighbouring spatial
slices decouple (Ambjorn-Jurkiewicz-Loll, **hep-th/0011276**, Phys. Rev. D 64, 044011, 2001;
corroborated and framed this way in later work below).

**Evidence the field cites for "extended / de Sitter."**
- Spatial-volume profile. Monitoring N_spatial(t) (the "volume profile" / global scale factor), the
  extended phase's averaged profile matches the Euclidean de Sitter solution -- for spherical slices,
  the round three-sphere shape (**hep-th/0011276**; reviews **2401.09399**, **1905.08669**).
- Independent replication. Kommu gave a fully independent verification of the emergent Euclidean
  de Sitter solution in 2+1 (and 3+1) dimensions (**1110.6875**, 2011).
- Foliation-independence. Jordan-Loll reproduced the extended de Sitter universe in 2+1D even in
  CDT *without* a preferred proper-time foliation (**1305.4582**, Phys. Lett. B 724, 2013;
  **1307.5469**, Phys. Rev. D 88, 044055, 2013) -- so the extended phase is not an artifact of the
  slicing that our construction happens to use.
- Effective action / minisuperspace. The quantum dynamics of the scale factor is matched to a
  semiclassical minisuperspace reduction (**1905.08669**). Important 2+1D subtlety: the naive
  *general-relativistic* minisuperspace reduction FAILS to reproduce the measured 2+1D condensation,
  whereas a **Horava-Lifshitz** minisuperspace model succeeds (**1410.0845**, "Spacetime condensation
  in (2+1)-dimensional CDT from a Horava-Lifshitz minisuperspace model"; H-L<->CDT link in
  **1111.6634**, Phys. Rev. D 85, 044027, 2012).

**Crucial for us -- the field's "degenerate phase" IS our condensation.** In the degenerate phase the
spatial volume "oscillates wildly" and "spacetime disintegrates into a sequence of uncorrelated
two-dimensional geometries"; neighbouring-slice volumes are correlated in the de Sitter phase and
uncorrelated in the degenerate phase (**1410.0845**; genus/effective-action study **2208.13084**,
JHEP 09(2022)212). This is *exactly* our campaign-6 mechanism: raising k0 (or k22) lowers f22, the
(2,2) "stitching" vanishes, slices decouple, the profile condenses (CV rises, min slice collapses),
and d_H falls. The 2+1D de Sitter universe is itself a *condensate* whose time extent is strictly
smaller than the full time axis -- i.e. a blob-with-stalk (**1410.0845**). Our "alpha/k22 near-miss
is a blob+stalk collapse" observation is the *known* shape of the 2+1D universe, not a novel pathology.

---

## 2. The field's success criterion, and the spectral-dimension behaviour.

**What "extended / genuinely 3D / successful" means in the literature.** The primary, load-bearing
criterion is the SEMICLASSICAL one: the coarse-grained volume profile / scale factor reproduces the
de Sitter (minisuperspace) solution, with the correct fluctuation spectrum around it. The Hausdorff
dimension d_H ~ topological dimension at *large* scale is supporting evidence; the spectral dimension
d_s is reported as a *scale-dependent* diagnostic and its short-scale reduction is celebrated, not
penalized (**1905.08669**; **2401.09399**).

**Do they ever demand a strict joint d_s = d_H = 3?** No. The clearest evidence is 4D, stated
plainly in Loll's review: the emergent universe is "compatible with ... de Sitter space," with
"a spectral dimension near 2, replacing the classical value of 4" on short scales, while the
Hausdorff dimension in the de Sitter phase was measured at **d_H = 4.01 +/- 0.05** (AJL 2005, volumes
to N4 = 180,000) (**1905.08669**). The field thus reports d_H ~ D (large scale) and d_s -> ~2 (UV)
*simultaneously, as twin successes* -- they are deliberately different numbers at different scales.
A single-scale demand that d_s equal d_H equal the topological dimension appears nowhere; it would
contradict the celebrated result (dynamical dimensional reduction).

**Accepted 2+1D spectral-dimension flow.** Directly quoted from the one abstract that fetched
cleanly, Cooperman's 3D-CDT scaling analysis (**1711.02685**, 2017):

> "the spectral dimension exhibits novel scale-dependent dynamics: reducing towards a value near 2
> on sufficiently small scales, matching closely the topological dimension on intermediate scales,
> and decaying in the presence of positive curvature on sufficiently large scales. ... the spectral
> dimension is completely finite in the infinite volume limit, and ... its maximal value is exactly
> consistent with the topological dimension of 3 in this limit. ... the spectral dimension reduces
> further towards a value near 2 as this case's bare coupling approaches its phase transition ...
> [tentative explanation:] branched polymeric quantum geometry on sufficiently small scales."

So the accepted picture in 2+1D: d_s FLOWS -- ~2 (UV / small scale), ~3 (intermediate), decaying
again at large scale (finite-size/curvature). The de Sitter ground state and this reduction were
first established by Benedetti-Henson (**0911.0401**, Phys. Rev. D 80, 124036, 2009). The continuum
rationale is Horava-Lifshitz anisotropic scaling d_s = 1 + D/z: in 2+1D (D=2), z=2 gives d_s = 2 in
the UV and z=1 gives d_s = 3 in the IR (**1111.6634**, **1410.0845**). The spatial slices themselves
are measured to be *fractal* (**2208.12718**, Phys. Rev. D 107, 026011, 2023).

---

## 3. How our negative sits against that.

**(a) Our criterion is strictly stronger than, and different in kind from, the field's.** The field
asks: does the coarse-grained scale factor match de Sitter, with d_H ~ D at large scale and d_s
flowing 2->D? We ask: can the *microscopic* causal geometry be made as regular as a flat crystalline
lattice -- matching a flat T^3's d_s AND d_H JOINTLY at accessible finite scales, on a uniform
profile, with a flat degree distribution? Those are different targets. The field's reference geometry
is the de Sitter *blob* (a peaked, curved, fluctuating S^3-like universe); ours is a *flat, uniform,
zero-curvature crystal*. The field never claims the quantum geometry should look like a flat lattice
-- on the contrary, its short-scale irregularity (hubs, fractality, d_s reduction) is the physics.
So "the causal ensemble is not a flat crystal" is expected from the field's standpoint, and several
of our gate clauses (G2's flat-lattice d_H target, G4's no-condensation/uniform-profile demand) are
*stricter than* what the field uses to certify an extended de Sitter universe -- indeed G4 penalizes
the very condensation that the field identifies AS the de Sitter phase (**1410.0845**).

**(b) Our d_s ~ 2 is consistent with the known dynamical reduction -- NOT an anomaly.** The value we
hit (2.0-2.2) when we force the geometry toward flat-lattice regularity coincides with the
established 2+1D short-scale / near-transition value d_s ~ 2 (**1711.02685**: "reduces further
towards a value near 2 as ... the bare coupling approaches its phase transition"; **0911.0401**;
continuum d_s = 1 + D/z -> 2 in 2+1D). Our route to it (hub suppression / low f22 -> a walk-confining
1-skeleton) is the same *family* of mechanism the field invokes -- "branched polymeric quantum
geometry" / decoupled slices confine the diffusing walker (**1711.02685**, **1410.0845**). Nothing in
our d_s ~ 2 is in tension with the literature; it is a rediscovery of dimensional reduction under a
different driver.

Honest nuance (our inference, worth stating): in our *accessible* diffusion windows (8-24, 16-48 ...)
at N0 ~ 1000-4000, the baseline d_s(8-24) is ~3.2-3.5 -- i.e. at/above topological, then DECAYING at
the longer 16-48 window (2.3-2.9). That matches the "intermediate ~3, decaying at large scale" part
of the flow (**1711.02685**), not the deep-UV rise to 2. We do not cleanly resolve the UV 2->3 climb
(our lattices are coarse); our "d_s -> 2" is produced dynamically by forcing regularity, not by
probing the deep UV. So it is consistent with the known reduction *in value and mechanism-family*,
but it is not a clean one-to-one measurement of the UV fixed value -- flagged as such.

**(c) Our condensation / slice-decoupling is the field's degenerate-phase physics.** The k0-up /
f22-down decoupling and profile condensation we characterize is the documented extended->degenerate
transition (**hep-th/0011276**, **1410.0845**, **2208.13084**). We did not find a new phase; we
re-derived the known one and added an exact combinatorial reason for the decoupling: the locked
identity dN22 = -4 dN0 (Sec 0), which -- as far as this survey found -- is a sharper, more explicit
statement than the standard f22/(coupling) descriptions in the cited papers. That specific algebraic
lock is our genuine new content, not a literature restatement (flagged: I did not find it stated in
this exact differential form in the surveyed papers; a deeper reference dive could still turn one up).

**Is our "wall" in real tension with the extended-phase results? No.** Our own runs put the field's
extended de Sitter phase at k0=2 (uniform-ish profile, CV ~0.16; d_s(8-24) ~ topological). We do not
claim the extended phase is absent -- we confirm it. The wall is not "2+1D CDT has no 3D phase"; it
is "the entropically-typical causal geometry cannot be *regularized into a flat crystal* jointly in
d_s and d_H at these volumes." Those are different claims, and only the latter is ours.

---

## 4. Bottom line -- how to honestly frame our negative.

It is **a stricter-criterion refinement plus a partial rediscovery -- NOT a genuine tension** with
the published extended-phase / de Sitter results.

- NOT a tension. Every extended-phase claim in the field (de Sitter volume profile at low-range k0;
  d_H ~ D at large scale; d_s flowing 2->3; degenerate phase at high k0) is reproduced or untouched
  by our work. Our k0=2 baseline sits IN that extended phase.
- A stricter-criterion refinement. Our JOINT test against a *regular flat-lattice* benchmark, on a
  uniform profile with a matched degree distribution, at accessible finite scales, is a stronger and
  more microscopic demand than the field's semiclassical de Sitter criterion. Under that stricter
  bar we find, and prove the algebraic root of, a real, volume-stable, topology-independent
  obstruction (dN22 = -4 dN0; the entropic dominance of hub-rich walk-confining geometries). That is
  a legitimate, novel *characterization* -- of how far the typical 2+1D causal geometry is from a
  flat crystal, and why -- not a contradiction of anyone's positive result.
- Partly a rediscovery under a benchmark that over-demands d_s at short scales. Our benchmark reads
  d_s ~ 3.1 at *every* window because a flat crystal does not dimensionally reduce. Real 2+1D CDT
  does reduce -- d_s -> ~2 at short/near-transition scales is the established physics
  (**1711.02685**, **0911.0401**). So demanding d_s ~ 3 at the scales where our levers drive it to
  ~2 is asking the causal ensemble to be *less* dimensionally-reduced than genuine 2+1D CDT is known
  to be. To that extent our d_s ~ 2 "failure" is the field's celebrated success (dimensional
  reduction) re-labelled by a flat-lattice yardstick.

Recommended framing for the writeup / handoff: present the wall as **"the flat joint 3-manifold is
entropically unselected in 2+1D causal CDT -- a stricter, microscopic-regularity probe that
recovers, and gives an exact combinatorial mechanism for, the field's known dimensional reduction
and extended->degenerate condensation, rather than contradicting the established extended de Sitter
phase."** Keep the honest caveat front and centre: the part of the negative that is d_s ~ 2 vs a
flat-lattice 3.1 is over-determined by the benchmark, whereas the part that is genuinely new is the
locked-DOF obstruction to *crystalline regularity* (and its dimensional escape in 3+1D, where
dN22 = -4 dN0 has no analogue). This is consistent with the program's own STAGE-3 finding that the
escape is dimensional.

---

## What is established (literature) vs our inference vs unresolved

Established in the published field (cited above):
- 2+1D CDT has an extended, de Sitter-like phase over a range of k0; transition to a degenerate
  (decoupled-slice) phase as k0 grows. [hep-th/0011276, 1110.6875, 1307.5469, 1410.0845, 2208.13084]
- Success criterion = semiclassical de Sitter volume profile / effective action (H-L minisuperspace
  in 2+1D), with d_H ~ D at large scale and a scale-dependent d_s. No joint d_s = d_H = D demand.
  [1905.08669, 2401.09399, 1410.0845, 1111.6634]
- 2+1D d_s flows: ~2 (small/near-transition), ~3 (intermediate), decaying at large scale; finite in
  the infinite-volume limit with max = 3. [1711.02685, 0911.0401]

Our inference (reasoned from the above + our data, flagged as such):
- Our G4 (no-condensation / uniform profile) is stricter than the field's de Sitter-blob criterion.
- Our d_s ~ 2 under hard regularization is the same value & mechanism-family as the field's known
  reduction, but reached by a different driver; not a clean deep-UV measurement.
- The exact differential lock dN22 = -4 dN0 as the combinatorial root of slice-decoupling appears to
  be a sharper statement than the surveyed papers give (not found stated this way; not exhaustively
  checked).

Unresolved / could not source this session:
- A directly-read, precise *2+1D* Hausdorff-dimension number for the extended phase (the d_H = 4.01
  +/- 0.05 I could source is 4D, AJL 2005 via 1905.08669). 2+1D d_H is reported as "compatible with
  3 at large scale" qualitatively; I did not pin a primary numeric value.
- Exact Benedetti-Henson short-scale d_s value in 3D (I have "near 2" qualitatively from 0911.0401
  summaries + 1711.02685, not a direct read of 0911.0401).
- arXiv HTML/API fetch was unreliable this session; only 1711.02685 was read verbatim. All other IDs
  are corroborated via WebSearch summaries of the abstract/journal record, which is sufficient for
  the qualitative claims but not for digit-level numbers I did not personally read.

---

## Sources (arXiv IDs)

- hep-th/0011276 -- Ambjorn, Jurkiewicz, Loll, "Non-perturbative 3d Lorentzian Quantum Gravity,"
  Phys. Rev. D 64, 044011 (2001). Extended-geometry phase, range of k0, round-S^3 volume profile.
- 0911.0401 -- Benedetti, Henson, "Spectral geometry as a probe of quantum spacetime,"
  Phys. Rev. D 80, 124036 (2009). 3D CDT ground state = de Sitter; dynamical dimensional reduction.
- 1110.6875 -- Kommu, "A Validation of Causal Dynamical Triangulations" (2011). Independent
  verification of de Sitter emergence in 2+1 and 3+1.
- 1110.6880 -- "Testing Lattice Quantum Gravity in 2+1 Dimensions" (Anderson, Carlip, Cooperman,
  Horava, Kommu, Mukund). d_H / d_s measured in 2+1D. (Cited for existence; no specific number used.)
- 1111.6634 -- Anderson, Carlip, Cooperman, Horava, Kommu, Mukund, "Quantizing Horava-Lifshitz
  Gravity via CDT," Phys. Rev. D 85, 044027 (2012). H-L <-> CDT; d_s = 1 + D/z.
- 1305.4582 -- Jordan, Loll, "Causal Dynamical Triangulations without Preferred Foliation,"
  Phys. Lett. B 724 (2013). 2+1D.
- 1307.5469 -- Jordan, Loll, "De Sitter Universe from CDT without Preferred Foliation,"
  Phys. Rev. D 88, 044055 (2013). 2+1D de Sitter without foliation.
- 1305.4702 -- "Exploring Torus Universes in Causal Dynamical Triangulations." (Torus-slice context.)
- 1410.0845 -- "Spacetime condensation in (2+1)-dimensional CDT from a Horava-Lifshitz minisuperspace
  model" (2014). Condensate < total time (blob+stalk); GR minisuperspace fails, H-L succeeds;
  degenerate phase = decoupled slices.
- 1711.02685 -- Cooperman, "Scaling analyses of the spectral dimension in 3-dimensional CDT" (2017).
  [Fetched verbatim.] d_s ~2 small / ~3 intermediate / decays large; finite, max = 3; ->2 near
  transition; branched-polymer explanation.
- 1802.10434 -- "The phase structure of CDT with toroidal spatial topology." (Topology context.)
- 2208.12718 -- "On the Nature of Spatial Universes in 3D Lorentzian Quantum Gravity,"
  Phys. Rev. D 107, 026011 (2023). Fractal spatial slices.
- 2208.13084 -- "The phase structure and effective action of 3D CDT at higher spatial genus,"
  JHEP 09(2022)212. Extended vs degenerate phase; effective action; genus.
- 1705.05417 -- Carlip, "Dimension and Dimensional Reduction in Quantum Gravity" (2017). Universal
  UV d_s -> 2 across approaches (framing of our d_s ~ 2 as expected, not anomalous).
- 1905.08669 -- Loll, "Quantum Gravity from Causal Dynamical Triangulations: A Review,"
  Class. Quantum Grav. 37, 013002 (2020). Criterion; d_s -> 2 (UV) with d_H = 4.01 +/- 0.05 (4D)
  reported as twin successes -- no joint d_s = d_H demand.
- 2401.09399 -- "Causal Dynamical Triangulations: Gateway to Nonperturbative Quantum Gravity" (2024
  review). de Sitter emergence, volume profiles.

_Compiled for branch causal-cdt-scaling. Ground-truth for our result: HANDOFF.md,
REPORT_CDT_FRONTIER.md / _K0 / _HUB / _ACTION / _TOPOLOGY.md._
