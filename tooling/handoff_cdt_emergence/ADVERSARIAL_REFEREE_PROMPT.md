# Adversarial Referee Prompt (for a deep-research pass)

Paste the block below into a deep-research tool. It points the referee at this repo as
ground truth and forces independent re-derivation of the physics rather than trusting the
report's prose.

---

You are an adversarial but scrupulously fair referee for a computational-physics
manuscript on emergent geometry via Causal Dynamical Triangulations (CDT). Your job
is to try to break it. Assume the authors are competent and honest but may have fooled
themselves. Default to skepticism; give credit only where a claim survives attack.

TARGET (treat the repo as the only ground truth; treat the prose as advocacy).
Public at github.com/hydrowolfy/manifold, branch `cdt-emergence-handoff`, folder
`tooling/handoff_cdt_emergence/`. Start from CONSOLIDATED_REPORT.md, then use docs/
(technical records) and src/ (the actual Monte Carlo code, including cdt_2plus1_faithful.c).
Read the code, not just the report.

CLAIMS TO ADJUDICATE — attack each independently:
1. 2D "manifold emergence" is refuted by vertex-link + scaling tests.
2. 1+1D CDT substrate validated: ball-growth Hausdorff d_H -> 2 (Ambjorn-Loll).
3. Off-manifold (baby-universe) branch reproduces ALWZ: per-baby mu_c slope ~ 3/2
   (vs a proxy's 1/2) and Liouville spectral dimension d_s ~ 2 (not bottleneck <1,
   not branched-polymer 4/3); detailed balance ~1e-16.
4. Nonequilibrium winding-current branch: Kolmogorov cycle violated (e^{LE} != 1) =
   genuinely non-integrable; measured z ~ 2 (Edwards-Wilkinson), 5.5 sigma off KPZ 3/2,
   drive "irrelevant" at weak E; a strong-drive positive control recovers KPZ.
5. 2+1D faithful rebuild: three named defects (missing Metropolis-Hastings proposal
   factors; too-weak chi=2 manifold gate; mis-targeted (2,3) move) fixed -> exact
   detailed balance (~1e-16) and a volume-flat order parameter tau = N22/N3.
6. The de Sitter blob does NOT condense, and this is a COMPUTE-SCALE limit (needs
   N3 ~ 1e4-1e5, 1e5-1e6 sweeps), NOT a code/ensemble bug.

FOR EACH CLAIM, DELIVER:
- Independent literature verification. Re-derive or re-check the load-bearing numbers:
  d_H=2 and d_H=4, gamma/d_s for Liouville vs branched polymer, ASEP z=3/2, the 2+1D
  de Sitter cos^2 profile and k0_c, the ALWZ (3/2)ln N and critical 2/(3 sqrt 3).
  Confirm or correct EVERY citation. The report self-flags some as unverified (the cos^2
  width prefactor, the exact decoupled-phase tau, and that arXiv:1108.3932/1205.1229 are
  3+1D not 2+1D papers) — check those and hunt for more.
- The strongest attack you can mount. Specifically probe: is the ALWZ "reproduction"
  real or curve-fitting to a known answer on too few volumes; is a measured 1.76 actually
  "3/2" or equally consistent with 2; is the nonequilibrium null genuine irrelevance or an
  artifact of measuring an observable orthogonal to the drive (they claim to have checked
  this in the "current sector" — verify or debunk); is the strong-drive positive control
  cherry-picked; is "exact detailed balance" actually proven or just small residuals on a
  tiny system; and is "compute-scale, not a bug" falsifiable — state exactly what result at
  ACCESSIBLE volume would instead indicate a real ensemble defect, and whether the authors
  could reach it.
- Statistical rigor: separate results resting on ~2 sigma from >=5 sigma; check whether
  error bars account for autocorrelation and seed variance; flag any conclusion drawn from
  under-thermalized runs (the report admits earlier ones were).
- Reproducibility: can the posted code be compiled and run to reproduce the headline
  numbers? Note anything blocking independent replication.

ADVERSARIAL CONTROLS (perform them, don't just request them): for at least the 1+1D d_H
claim and the detailed-balance claim, state the foregone-conclusion / null result and
whether the work distinguishes signal from it. Name any place a null model reproduces the
reported "signal."

OUTPUT:
- A per-claim verdict table: SUPPORTED / OVERCLAIMED / UNSUPPORTED / REFUTED, each with
  its single most damaging specific objection.
- The one critique most likely to sink the whole program if correct.
- A falsification plan: the cheapest experiment that would decide each contested claim.
- A ruling on the HPC handoff: is the proposed N3 ~ 1e5, 1e6-sweep de Sitter run worth the
  compute, and is its success/failure criterion pre-registered tightly enough to be honest,
  or could either outcome be rationalized post hoc?
- Explicitly keep "wrong" separate from "unproven at this scale." Do NOT let finite-size
  honesty launder into credit.

Cite every source you rely on. Where you cannot verify something, say so rather than guess.
Accept no number at face value.
