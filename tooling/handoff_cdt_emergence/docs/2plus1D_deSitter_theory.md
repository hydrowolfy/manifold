# 2+1D CDT de Sitter — theory summary

## The de Sitter blob in 2+1D CDT
In the extended (physical) phase, the ensemble-averaged spatial volume profile
N(t) of a foliated 2+1D CDT quantum universe condenses into a single **de Sitter
blob**: a lobe of large spatial volume localized over ~N3^{1/3} time slices,
connected by a thin "stalk" of near-minimal slices around the periodic time ring.

- **Shape law:** N(t) ~ A * cos^2( (t - t0) / W ).
  The exponent is **n = 2 in 2+1D** (contrast: n = 3, cos^3, is the 3+1D law).
  The blob half-width scales as **W ~ N3^{1/3}** (the universe grows self-similarly).
- **Phase:** the blob lives in the **extended / strongly-coupled phase at
  k0 < k0_c** (below the phase transition). Above k0_c the geometry decouples
  into a degenerate/branched-polymer-like or decoupled-tube phase.
- **Order parameter:** tau = N22 / N3 = fraction of (2,2) tetrahedra (the
  timelike inter-slice "coupling" simplices). tau rises sharply on crossing into
  the extended phase; a well-coupled 2+1D geometry sits near tau ~ 0.33-0.4,
  whereas a decoupled tube is (2,2)-poor (tau ~ 0.09).
- **Bulk DOF / alpha:** the asymmetry parameter alpha (ratio of timelike to
  spacelike edge-length-squared) is absorbed into the bare couplings; the action
  S = -k0 N0 + k3 N3 (+ volume fixing) has **two bulk coupling DOF** (k0, k3),
  with alpha reabsorbed into their definitions.

## Measurement subtlety
The de Sitter lobe **wanders** (its center-of-volume diffuses around the periodic
time ring, tau_int ~ 35 sweeps). A naive time-average of the raw N(t) smears one
wandering lobe into a spurious multi-lobe "tube". Each snapshot must be
**center-of-volume (COV) aligned** before averaging; only then does the single
lobe appear.

## References
- Ambjorn, Jurkiewicz, Loll, "Nonperturbative 3d Lorentzian Quantum Gravity",
  hep-th/0011276.
- Kommu, "A Validation of Causal Dynamical Triangulations", arXiv:1110.6875.
