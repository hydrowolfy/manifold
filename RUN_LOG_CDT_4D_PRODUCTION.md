# RUN LOG: the launched 3+1D de Sitter (kappa_0, Delta) scan (actual data)

Companion to REPORT_CDT_4D_PRODUCTION.md. Records the ACTUAL uncapped run executed on Kirk's
WSL box (cdt4run/, T=5, N4t~24000, eps=0.004, grown-above-seed base), and the two run-tuning
lessons learned live. Honest landing unchanged: machinery complete + validated; a CERTIFIED de
Sitter gate-pass is compute-bound beyond this session (finite-size N0 saturation + slow machine).

## Run-tuning lessons (learned on the live box)

1. THE DENSE REGULAR KUHN SEED FREEZES THE METROPOLIS. Starting the dynamics from seed_flat(T)
   (the maximally-regular Coxeter-Freudenthal-Kuhn T^4, N4=24 T^4) with a tight volume term
   (eps=0.02) gives ~0.06% acceptance: the regular seed has almost no legal (4,2)/(8,2)/(6,4)
   sites and every additive move is volume-penalized, so the chain sits BYTE-FROZEN at the seed
   (N0, f_tl, CV all pinned at seed values over 147 sweeps). Not a bug -- a near-absorbing start.
2. GROW ABOVE THE SEED VOLUME to escape it. Setting N4t > seed N4 forces the grow phase (biased
   additive moves, 40% of them the vertex-adding (2,8)) to run: it IRREGULARIZES the complex
   (CV 0 -> ~0.06) AND grows N0 into the un-saturated regime (T=5: 625 -> ~1750). Acceptance
   jumps to ~14% and the chain thermalizes. This is the 4D analogue of the 2+1D `grow` phase.
3. WATCH heartbeat.txt, NOT run.log OR the console. The mounted Downloads caches file MTIMES
   (stale) but serves small-file CONTENT fresh; `tee`-to-run.log block-buffers when piped; the
   console only prints per COMPLETED point (~10+ min each). The per-sweep heartbeat.txt (single
   overwritten line: ALIVE <ts> | point | sweep N | N0 N4 f_tl cv | acc census) is the truth.

## Actual result -- (kappa0, Delta) = (2.2, 0.6), the de Sitter candidate

Thermalization from the grown-irregular base (T=5, N4~24000), census bad=0 at every sweep:

    sweep    N0     N4     f_tl    CV
      1     1804   24028   0.372  0.060   (grown-irregular start)
     26     1239   24048   0.508  0.031
     51     1026   24058   0.560  0.013
    120      859   24064   0.600  0.015
    292      772   24052   0.625  0.024   (plateauing)

Relaxes to a PLATEAU: N0 ~ 760 (N0/N4 ~ 0.032), f_tl ~ 0.62, and an EXTENDED / non-collapsed
volume profile (CV ~ 0.02, low and stable -- NOT a stalk/spike). The ergodic Metropolis thus
thermalizes to a STABLE, EXTENDED, census-clean 4-geometry at the literature de Sitter coupling.

## What this does and does NOT establish (honest)

ESTABLISHES: the full apparatus runs a real, ergodic, detailed-balance-correct 4D causal CDT
Monte Carlo that thermalizes to a stable extended census-clean 4-geometry at (2.2,0.6). The state
is EXTENDED (CV ~ 0.02), i.e. NOT the branched-polymer collapse (phase B) and NOT a degenerate
stalk -- CONSISTENT with the extended (de Sitter, phase C) side of the diagram.

DOES NOT ESTABLISH (compute-bound, per PREREG_CDT_4D_PRODUCTION Sec 5 rule 2): the CERTIFIED de
Sitter gate-pass. At N4~24000 the equilibrium N0 ~ 760 is BELOW the ~1300 threshold where d_H/d_s
stop saturating (LESSONS 43), so the QUANTITATIVE signatures (d_H -> 4, d_s ~4 IR -> ~2 UV) cannot
be certified at this volume; and the localized cos^3 de Sitter blob requires spontaneous time-
translation symmetry breaking that emerges only at larger 4-volume. No de Sitter CLAIM is made
from saturated/under-thermalized data -- that is the program's standing discipline (LESSONS 40).

## The path to the certified verdict (handed off, resumable)

Run at N4 large enough that equilibrium N0 clears ~1300 -- with N0/N4 ~ 0.032 that means
N4 >~ 40000 (T=6 grown to ~40k; the run is resumable, re-run run_cdt4_scan.bat to extend), on an
UNCONTENDED box (the loaded gaming machine crawled at ~11 s/sweep). Then thermalize each
(kappa0,Delta) to an N0/f_tl/CV plateau, measure d_H/d_s (8 seeds) + the N3^SL(t) profile, and
score vs the frozen gate G1-G5. The direct B-vs-C test is whether the low-Delta control (2.2,0.0)
COLLAPSES (CV spikes, stalk) while (2.2,0.6) stays extended -- the machinery is built to deliver it.
