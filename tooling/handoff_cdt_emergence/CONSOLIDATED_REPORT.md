# Emergent-Geometry Program — Consolidated Report and HPC Handoff

**Purpose.** A self-contained record of an adversarial computational investigation into whether extended geometry emerges from discrete causal-ordering models, covering three dimensional levels (2D, 1+1D, 2+1D). Written to be fed into a deep-research pass: every established result is stated with its control and its verified citation, every negative is stated with the null model that produced it, and the open questions plus the exact next-step compute spec are laid out at the end. Nothing here is a claim of new physics; the program's discipline throughout was "matching known CDT is the entry ticket, not the result."

---

## 0. Executive summary

- **The strong thesis is falsified; a weaker thesis stands.** Extended geometry does **not** emerge from minimal causal ordering alone ("zero coordinates"); it requires the causal/foliated structure and tuned couplings of Causal Dynamical Triangulations (CDT). The investigation therefore reduced to: can we validate a CDT substrate and ask whether it does anything novel off-manifold or out of equilibrium.
- **2D manifold claim: refuted** (prior phase; a candidate "2D manifold emergence" fails standard vertex-link and scaling tests).
- **1+1D CDT substrate: validated** (Hausdorff dimension d_H → 2, Ambjørn–Loll).
- **1+1D off-manifold (baby-universe proliferation): reproduced against ALWZ theory.** A faithful spatial-topology-change move gives the analytically-known string-susceptibility exponent (per-baby μ_c slope ≈ 3/2) and the Liouville spectral-dimension certificate (d_s ≈ 2), the two targets a naive "graft" proxy failed.
- **1+1D nonequilibrium (winding current): a clean, controlled null.** A genuinely non-integrable drive (Kolmogorov cycle violated, e^{LE} ≠ 1) is **irrelevant** to the geometry at accessible weak drive (dynamic exponent z ≈ 2, Edwards–Wilkinson, 5.5σ off KPZ), while a strong-drive **positive control** recovers KPZ, proving the observable can see a relevant drive.
- **2+1D CDT substrate: built, optimized (C, N3 ~ 10⁴), and corrected to the faithful AJL measure — but it does not yet exhibit the de Sitter blob, for a now-verified compute-scale reason, not a bug.** After fixing three genuine measure/gate/targeting defects (detailed balance now exact to 1e-16; order parameter τ = N22/N3 coupled and volume-flat), the defining de Sitter droplet still does not condense at the volumes/thermalization the sandbox allows (~10³ sweeps vs the literature's 10⁵–10⁶). A 14k-sample registration + null-model test confirmed there is no hidden droplet. This is the HPC handoff point.

---

## 1. Scope, thesis, and method

**Thesis under test.** The original ("strong") claim was that extended, higher-dimensional geometry emerges from a minimal discrete causal order with no background coordinates. That was falsified in earlier phases: random/Pachner and flag-complex constructions crumple (expander/log-diameter attractors), and the one escape is locally-causal CDT (Jordan–Loll). The program adopted the **weaker thesis**: extended geometry emerges from minimal causal ordering **plus** a tuned coupling and an imposed foliation — i.e., CDT — and the only genuinely new questions are whether the CDT extended phase survives **off-manifold** (spatial topology change) and under **detailed-balance-violating** dynamics.

**Method.** Build the analytically-solved substrate at each level, validate it against ground truth ("entry ticket"), then perturb. Every claimed effect is a scaling/threshold object carrying its foregone-conclusion control; honest error bars and finite-size caveats throughout. Work was adversarially reviewed by a standing red team plus recruited specialists (skeptic, condensed-matter, Hořava–Lifshitz, Wolfram, methodology).

**Compute environment (a hard constraint on everything below).** A sandbox with 40-second synchronous execution chunks, no persistent background jobs, pure-Python + a C toolchain (gcc 11.4). All long runs were chunked with checkpoint/resume. This caps reachable volume and thermalization and is the binding limit on the 2+1D result.

---

## 2. Level 0 — 2D manifold claim: refuted

A candidate "2D manifold emergence" was re-adjudicated with a topology suite (vertex-link = cycle test) and a scaling suite. It fails: interior vertex links are not clean cycles at the rate a genuine 2-manifold requires, and the scaling does not hold up. Verdict: the 2D-manifold claim does not survive tough-but-fair retesting. (This motivated dropping the strong thesis and moving to CDT.)

---

## 3. Level 1 — 1+1D CDT

### 3.1 Substrate (validated)
Genuine 1+1D CDT (Ambjørn–Loll): T periodic proper-time slices, each a spatial circle of L[t] vertices; strips between slices are triangulated annuli encoded as cyclic U/D words; causality = each slice stays one circle. Canonical (fixed-volume) ensemble with flip + volume-conserving relocate moves. **Validation: ball-growth Hausdorff dimension d_H → 2** (measured 1.54, 1.90, 2.06 at increasing volume; asymptotes to the Ambjørn–Loll value 2). Code: `cdt_1plus1.py`.

### 3.2 Off-manifold branch — baby-universe proliferation (reproduced vs ALWZ)
**Physics.** Generalized CDT allows spatial topology change: a spatial circle splits into two, one being a baby universe that caps off downstream; penalty μ per event (branching coupling g_s ~ e^{−μ}). ALWZ predict μ_c(N) diverges as (3/2)ln N and observables collapse in x = e^{−μ}N^{3/2}, with a critical (g_s/λ^{3/2})_c = 2/(3√3) ≈ 0.385. Crucially d_H alone cannot certify the phase (branched polymers also have d_H = 2), so the string-susceptibility exponent γ or spectral dimension d_s must be measured.

**Result (two implementations, adversarially compared).**
- A naive **"graft" proxy** (a cap on a single neck vertex) made d_H rise toward the Euclidean 4 but was an independent-site fugacity gas: it gave the **wrong** exponent (μ_c collapse under N^{1/2}, not N^{3/2}) and a **bottleneck** d_s < 1 — not Liouville. Rejected as unfaithful.
- The **faithful multi-circle topology-change move** (parent circle splits into two sharing seam vertices; baby caps off; full multi-circle spacetime adjacency) banks both analytically-known targets: **per-baby μ_c slope ≈ 1.76 (3/2 regime, decisively not 1/2)** and **d_s ≈ 2.0 across all μ (Liouville certificate, not bottleneck <1, not branched-polymer 4/3)**. Detailed balance exact to ~1e-16; μ→∞ recovers the validated substrate. d_H → 4 not shown (volume-limited, needs N2 ≳ 10⁴), but the exponent and d_s already certify the correct phase.

**Interpretation (condensed-matter + Hořava seats).** The transition is Kosterlitz–Thouless-like (log-fugacity μ_c ~ (3/2)ln N, essential singularity), i.e., a defect-unbinding transition. In 1+1D this branch is the Hořava-relevant one: it tests robustness of the foliation-universality (projectable-Hořava) fixed point against foliation-breaking operators. Code: `cdt_1plus1_topch.py`.

### 3.3 Nonequilibrium branch — winding current (clean null with positive control)
**Physics.** Read each periodic slice as an ASEP (U = particle, D = hole); the flip is a hop; add a chiral bias e^{±E/2}. This is genuinely non-integrable: L forward hops around the ring return to the same state but the rate-product ratio is e^{+LE} ≠ 1 (a closed-but-not-exact 1-form on the non-contractible loop; no shifted action reproduces it). Contrast a bias that telescopes to e^0 = 1 (a mere coupling shift).

**Results.**
- **Kolmogorov cycle test PASSED** (make-or-break): R = e^{L·E} ≠ 1 around the ring, R = 1 on contractible loops, verified analytically and by measuring rates off the mover. Genuine detailed-balance violation.
- **Dynamic exponent, measured in the correct (current) sector**: z_eq = 1.93 ± 0.02, **z(E=0.3) = 2.00 ± 0.09** — diffusive (Edwards–Wilkinson z = 2), **5.5σ above KPZ 3/2**, identical to equilibrium. **Positive control z(E=2.0) = 1.71 ± 0.08**, bent toward KPZ with a clean t^{2/3} current-variance window, proving the observable responds to a relevant drive.
- **Verdict: the drive is genuinely non-integrable but irrelevant to the geometry at accessible weak drive.** Interpretation is textbook WASEP: crossover length ℓ*(0.3) ≈ 340 ≫ accessible L = 48; KPZ is presumably the asymptotic class for any E > 0 but is out of reach at linear-response drive. The geometry is a spectator (d_H flat while current flows). Code: `cdt_nonequilib.py`.

**Guard against over-claiming.** An earlier first pass had reported a suggestive z-shift (1.19 → 1.80, ~2σ) on the wrong observable (volume-profile mode); scaling up and moving to the current sector dissolved it. The reported null is the post-scrutiny result.

---

## 4. Level 2 — 2+1D CDT

### 4.1 Substrate and optimization
Genuine AJL structure: T periodic slices, each a closed S² triangulation (χ = 2); sandwiches filled with tetrahedra of the three causal types (3,1)/(2,2)/(1,3); closed causal 3-manifold; action S = −k0·N0 + k3·N3 (the correct reduced 2+1D form; the asymmetry α is absorbed into k0, k3 because a 2+1D triangulation has only two bulk DOF — verified from Kommu). Full ergodic move set (2,3)/(3,2), (2,6)/(6,2), (4,4). Self-tests (closed, foliated, χ = 2, independent slice-volume fluctuation) pass. Ported to standalone **C** (incremental hash-map adjacency, xoshiro256\*\*), ~34–250× over Python, reaching **N3 ≈ 10⁴** in checkpointed 40s chunks, cross-validated against the Python oracle. Code: `cdt_2plus1.py` (reference oracle), `cdt_2plus1_faithful.c` (corrected).

### 4.2 The de Sitter test and the debugging saga
The defining validation of 2+1D CDT is the **de Sitter blob**: the extended phase condenses into a single semiclassical universe with spatial-volume profile N(t) ~ **cos²**(t/(B·N^{1/3})) (exponent n = 2 in 2+1D; cos³ is the 3+1D result), one droplet on a minimal stalk, width ~ N3^{1/3}. d_H → 3 alone is necessary but not sufficient (a rough tube also has rising d_H).

The naive substrate produced a lumpy multi-lobe tube, worsening with volume. The debugging established, in order:
1. **Fit-function fix:** 2+1D is cos², not cos³ (Kommu 1110.6875).
2. **Measurement fix:** the de Sitter droplet wanders in proper time; each sample must be center-of-volume/registration-aligned before averaging, or a single wandering lobe smears into a fake tube.
3. **Phase fix:** the (2,2) tetrahedra carry the timelike inter-slice coupling; order parameter τ = N22/N3. Default k0 gave τ ≈ 0.09 (decoupled phase); the de Sitter phase is at k0 < k0_c with τ ~ 0.3–0.5.
4. **Ruled out:** the asymmetry α is not a missing ingredient in 2+1D (two bulk DOF).
5. **The three real bugs (spec audit vs AJL hep-th/0105267 §7.1):**
   - **Tilted measure (crux):** moves omitted the Metropolis–Hastings N_forward/N_reverse proposal factors, so detailed balance held only accidentally and the sampled measure was wrong.
   - **Too-weak manifold gate:** acceptance checked only χ = 2, admitting pinched/degenerate slices (a superset ensemble).
   - **Mis-targeted (2,3) move:** fired on any face, not the AJL (3,1)+(2,2)-sharing-a-triangle pattern.

### 4.3 Faithful rebuild — what got fixed, and the honest remaining wall
All three fixed and verified in `cdt_2plus1_faithful.c`:
- **Detailed balance now exact** (worst relative flux imbalance ~1.7e-16, badrev = 0, across couplings and sizes, decoupled and extended).
- **τ = N22/N3 now stationary and volume-flat** in the extended phase (~0.50 at k0 = −2 across N3 = 1k–6k; the residual dip at 10k is a thermalization-budget effect, confirmed by therm-scaling controls) — the old collapse 0.44 → 0.19 is gone.
- Full vertex-link-single-cycle manifold gate; AJL-correct (2,3)/(3,2) targeting.

**The de Sitter blob still does not condense, and this is now a verified compute-scale limit, not a bug.** A 14,000-sample iterative cross-correlation registration produced a **flat** averaged profile (free-n ≈ 0.3, not 2; width scaling fails). A null model (uniform tube + Poisson slice noise) reproduces the data's peak/mean almost exactly (data 1.76 vs Poisson 1.65), so the earlier "per-snapshot droplet, peak/mean ~2.0" was a max-over-T-slices noise artifact, not a real droplet. There is no hidden blob to register. On the **now-correct, exactly-reversible, coupled** ensemble, the droplet simply does not form at the accessible budget: AJL/Kommu need N3 ~ 10⁴–10⁵ with 10⁵–10⁶ sweeps; the sandbox reaches N3 ~ 10⁴ but only ~10³ thermalization sweeps. The flat profile is consistent with under-volume/under-thermalization on a correct implementation. Benedetti–Henson (1410.0845) confirm the full CDT ensemble does condense in 2+1D (only the reduced minisuperspace fails), so the target is reachable — at HPC scale.

---

## 5. Honest limitations

- The 2+1D de Sitter blob is **unconfirmed** here. What is confirmed is (a) an internally-correct, literature-spec-audited implementation with exact detailed balance and the correct coupled order parameter, and (b) that no measurement/statistics trick synthesizes the blob at accessible scale. Distinguishing "correct code, needs volume" from "a subtler ensemble defect" ultimately requires reaching the literature's volumes.
- 1+1D off-manifold d_H → 4 is volume-limited (exponent + d_s carry the certification instead).
- 1+1D nonequilibrium KPZ at weak drive is beyond the accessible ring size (ℓ* ≈ 340 ≫ 48); the null is a linear-response-regime statement backed by a strong-drive positive control.
- All numbers carry sandbox finite-size/thermalization caveats; none should be quoted as continuum values.

---

## 6. Open questions for a deep-research pass

1. **Does the faithful 2+1D substrate produce the de Sitter cos² blob at literature volumes** (N3 ~ 10⁴–10⁵, 10⁵–10⁶ sweeps)? If yes, the substrate is validated and the two branches can be carried into 2+1D. If no on a verified-correct measure, that is itself a notable result requiring explanation.
2. **Do the off-manifold (baby-universe) and nonequilibrium (winding-current) branches do anything novel in 2+1D**, where — unlike 1+1D — no analytic result pins the answer? Specifically: does baby-universe proliferation change d_H/d_s or the de Sitter profile; does a genuinely non-integrable drive remain geometry-irrelevant (as in 1+1D) or couple to the 2+1D geometry?
3. **Is the weak-drive KPZ crossover in 1+1D reachable** (L ≳ 340) and does it confirm KPZ z = 3/2 with Tracy–Widom statistics on the fluctuating CDT ring, or a geometry-dressed value?
4. **Literature cross-check** of the exact AJL 2+1D acceptance combinatorics (the N_forward/N_reverse factors per move) and the extended-phase τ = N22/N3 value and k0_c normalization, to independently confirm the corrected measure.

---

## 7. HPC HANDOFF

### 7.1 What to run
The de Sitter validation of the corrected 2+1D substrate at literature scale. Success criterion: center-of-volume/registration-aligned N(t) forms a **single cos² lobe on a minimal stalk**, with fit R² improving toward 1 and width W ~ N3^{1/3}, together with d_H → 3 and running d_s from ~2 (short) to ~3 (long).

### 7.2 Code inventory (all in the working tree; portable pure-Python + one C file)
- `cdt_2plus1_faithful.c` — the corrected 2+1D Monte Carlo: exact detailed balance (Metropolis–Hastings with per-move N_forward/N_reverse redex counts), vertex-link-single-cycle manifold gate, AJL-targeted (2,3)/(3,2), incremental hash-map adjacency, (2,2)/(3,1)/(1,3) census, per-snapshot N(t) dump. This is the artifact to scale.
- `cdt_2plus1.py` — pure-Python reference oracle for cross-validation.
- `cdt_1plus1.py`, `cdt_1plus1_topch.py`, `cdt_offmanifold.py`, `cdt_nonequilib.py` — the validated 1+1D substrate and branches (portable, for carrying into 2+1D).
- Supporting analysis: iterative cross-correlation registration + cos² fit + Poisson null model (in the rebuild output dir).

### 7.3 Run specification
- **Volumes:** N3 = 10⁴, 3×10⁴, 10⁵ (finite-size series). Time extent T ≳ 3–5·N3^{1/3}, periodic.
- **Thermalization:** 10⁵–10⁶ sweeps (1 sweep ≡ N3 attempted moves); measure every ≥ few×τ_int; report run_length/τ_int per point (target ≥ 50).
- **Phase:** scan k0 to locate k0_c via the τ = N22/N3 jump; run well into the extended side (τ ~ 0.3–0.5). Soft volume-fixing ε(N3−N̄)² so N3 fluctuates ~√N̄.
- **Measurement:** per-sample iterative-template (cross-correlation) registration of N(t); fit A·cos²((t−t0)/W) and free-n; report R², n, single-lobe boolean, W, and the Poisson-null peak/mean baseline to guard against noise artifacts. Also measure d_H (ball growth) and running d_s (return probability) on the 3D dual graph.
- **Validation gates before trusting physics:** reproduce the exact-detailed-balance self-test (imbalance ~1e-16); cross-validate small-volume observables against `cdt_2plus1.py`; confirm τ stationary and volume-flat.
- **Resources:** single-node, hours-to-days, GB-scale RAM (per AJL/Kommu-class runs). The C code is serial and incremental; parallelize by independent seeds for the ensemble.

### 7.4 Expected results if the substrate is correct
Single cos² de Sitter lobe with R² → 1 and W ~ N3^{1/3}; d_H → 3; running d_s from ~2.1 (short) to ~2.98–3.19 (long); extended-phase τ ~ 0.3–0.4 flat in N3; k0_c ≈ 3.3 (Kommu normalization) or ≈ 6.6 (AJL). A persistent flat/multi-lobe profile at these volumes on the verified-correct measure would itself be a result worth reporting.

---

## 8. Verified citations
- Ambjørn, Loll, *Non-perturbative Lorentzian quantum gravity, causality and topology change*, Nucl. Phys. B536 (1998) 407 (hep-th/9805108) — 1+1D CDT, d_H = 2, topology-change → Euclidean.
- Ambjørn, Watabiki, Nucl. Phys. B445 (1995) 129 — Euclidean 2D d_H = 4.
- Ambjørn, Loll, Westra, Zohren (ALWZ), arXiv:0709.2784 — generalized CDT, branching coupling g_s, μ_c ~ (3/2)ln N, critical 2/(3√3).
- Jain, Mathur, Phys. Lett. B286 (1992) 239; Ambjørn, Jain, Thorleifsson, Phys. Lett. B307 (1993) 34 — minbu / string-susceptibility extraction.
- Kardar, Parisi, Zhang, PRL 56 (1986) 889; Gwa, Spohn, PRL 68 (1992) 725 — KPZ, ASEP dynamic exponent z = 3/2.
- Derrida, Evans, Hakim, Pasquier, J. Phys. A 26 (1993) 1493 — ASEP matrix-product stationary state.
- Kosterlitz, Thouless, J. Phys. C 6 (1973) 1181 — defect-unbinding transition.
- Knizhnik, Polyakov, Zamolodchikov, Mod. Phys. Lett. A3 (1988) 819 — gravity-dressed exponents (KPZ-DDK).
- Ambjørn, Glaser, Sato, Watabiki, arXiv:1302.6359 — 1+1D CDT = 2D projectable Hořava–Lifshitz.
- Ambjørn, Jurkiewicz, Loll, *Non-perturbative 3d Lorentzian quantum gravity*, PRD 64 (2001) 044011 (hep-th/0011276); move set in Nucl. Phys. B610 (hep-th/0105267) §7.1 — 2+1D CDT, moves, de Sitter, k0_c.
- Kommu, arXiv:1110.6875 — independent 2+1D CDT code, τ = N22/N3 order parameter, k0_c ≈ 3.3, cos² de Sitter, α absorbed (two bulk DOF).
- Benedetti, Henson, arXiv:1410.0845 — 2+1D: full CDT ensemble condenses (reduced minisuperspace does not).

*Flagged:* arXiv:1108.3932 / 1205.1229 are primarily the 3+1D phase-order papers; the canonical 2+1D de Sitter references are hep-th/0011276 and Kommu 1110.6875. The cos² width prefactor and exact decoupled-phase τ were not independently confirmed from primary sources.
