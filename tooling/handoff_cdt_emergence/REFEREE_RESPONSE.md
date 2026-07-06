# Referee Response and Corrections (Round 2)

An adversarial deep-research referee treated the handoff. Its central empirical hit was
independently verified and several claims are corrected below. Where it landed, we concede.

## Verified hit: 1+1D d_H "validation" was overclaimed (conceded), then rescued at larger volume

The referee showed the repo's ball-growth estimator gives d_H ~= 1.76 on the trivial,
un-equilibrated triangular torus at every size, so the small equilibrated runs do not
separate from that null. Independently reproduced: (24,16) equilibrates to ~1.60 (below the
null), (32,24) to ~1.80 (on the null); only larger sizes separate. The original "1.54, 1.90,
2.06 -> d_H=2" sequence overclaimed: two of three points do not beat the null.

New finite-size series (8, 8, 6 seeds; null under the identical r-window):

| (T,Lmean) | N2    | null d_H | equilibrated d_H | separation |
|-----------|-------|----------|------------------|------------|
| (48,32)   | 3072  | 1.761    | 2.03 +/- 0.075   | ~10 SEM    |
| (64,48)   | 6144  | 1.761    | 2.16 +/- 0.089   | ~13 SEM    |
| (96,64)   | 12288 | 1.761    | 2.28 +/- 0.068   | ~19 SEM    |

**Verdict: rescued at N2 >~ 3000.** The equilibrated substrate separates decisively from the
trivial-torus null and sits in the smooth (CDT-like) phase, not the null and not Liouville
d_H=4. It overshoots 2 at larger N (a known ball-growth fit-window effect), so the honest
statement is "separates cleanly from the null and is consistent with the smooth d_H~=2 phase
at larger volume," and the smallest sizes are NOT independent evidence.

## Corrections adopted

- **Off-manifold / ALWZ (conceded).** A measured slope ~1.76 does not discriminate 3/2 from
  2. Downgrade "reproduces ALWZ" to "consistent with the Euclidean/Liouville direction and
  inconsistent with the 1/2 proxy." A clean claim needs an >=8-volume fit of mu_c = a + b ln N
  with locked model comparison b=1/2 vs 3/2 vs 2 (AIC/Bayes factor), plus raw d_s diffusion
  curves with a pre-registered plateau window.
- **Nonequilibrium (partial).** z ~= 2 IS the WASEP/Edwards-Wilkinson prediction at these sizes
  (crossover length l* ~= 340 >> L=48), so it is the expected diffusive regime, not a
  wrong-model artifact. But "irrelevant" overclaims what a crossover measurement can conclude,
  and "5.5 sigma off KPZ" oversells a formal error bar against systematics. Downgrade to
  "in the diffusive/EW regime at accessible sizes; KPZ presumably asymptotic for any E>0;
  confirmation needs a nested-window z-drift test as L increases."
- **2D refutation (packaging).** The vertex-link test is correct in principle, but the handoff
  did not expose raw audit tables / failure-rate-vs-size. Add them before claiming assent.

## de Sitter gate: adopted, and found to be thermalization-bound (HPC)

Adopted the referee's pre-registered fail-fast gate: N3 = 4k, 8k, 16k, 32k; SUCCESS = profile
broadens ~N3^{1/3} and fits cos^2 materially better than a flat/noise null; FAILURE = still flat
at 32k -> ensemble defect likely (not "needs more compute").

Finding at N3=4000 (coupled phase, frac22=0.51): the registered profile is flat (peak/mean
1.11; cos^2 R^2=0.32) and sits on the uniform-tube + Poisson-noise null (null cos^2 R^2 p95=0.23,
peak/mean p95=1.77) -- no blob. BUT this run did only ~11 moves per tetrahedron: drastically
under-thermalized, hence inconclusive. At the serial sampler's ~1-3k moves/sec, properly
thermalizing 8k-32k (~10^7-10^8 moves) is hours-to-days -- beyond the 40s-chunk sandbox.

So the gate is thermalization-bound, not merely volume-bound: the sandbox reaches the volumes
but cannot equilibrate them. This reinforces the referee's core point -- "compute-scale limit"
vs "wrong ensemble" is genuinely undecided at any properly-thermalized accessible scale -- and
confirms the gate belongs on HPC, run with the pre-registered fail-fast criterion above.

## Updated verdict table

| Claim | Prior | Updated after referee round |
|---|---|---|
| 2D "manifold emergence" refuted | asserted | overclaimed on packaging; add raw vertex-link audit |
| 1+1D d_H -> 2 validated | asserted | RESCUED at N2 >~ 3000 (clean null separation); small sizes retracted |
| Off-manifold reproduces ALWZ (3/2) | asserted | downgraded: consistent with, not "reproduces"; needs 8-volume model test |
| Nonequilibrium drive irrelevant | asserted | downgraded: diffusive WASEP regime at accessible sizes; needs drift test |
| 2+1D faithful rebuild, exact DB | asserted | supported (local kernel); strengthen via tiny-volume full enumeration |
| Missing de Sitter blob = compute-scale, not a bug | asserted | UNDECIDED; HPC gate with fail-fast criterion required; also thermalization-bound |

## Go-forward (referee-driven)

1. **Tiny-volume full-enumeration detailed-balance check** (sandbox-feasible): build the full
   transition matrix independent of the MC driver and verify the sampler's stationary
   histogram matches the intended Gibbs measure (with correct triangulation symmetry factors).
   This is the sandbox way to defeat the common-mode-bookkeeping-bug objection.
2. **HPC de Sitter fail-fast gate** (4k-32k) with the pre-registered success/failure criteria.
3. **8-volume ALWZ slope model comparison** and **nested-window nonequilibrium z-drift test**
   when compute allows.

Nothing here is laundered: "wrong" is kept separate from "unproven at this scale," per the
referee's standard.
