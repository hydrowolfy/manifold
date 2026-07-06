# Build design: the frame-free causal graph-rewriter (Wolfram + Horava seats)

Charge at the build's doorstep: must causal ordering be ADDED, or is it intrinsic to the Wolfram
rewriting; and does an added/emergent ordering land on the Horava fixed point? The two permanent
domain seats (Fable) answered decisively and upgraded the build. Citations are the seats' (verified;
re-verify before formal use).

## Verdict 1 (Wolfram seat): causality is INTRINSIC but NOT free -- add it, and instrument the intrinsic graph as a cheap probe
- A Wolfram model's causal graph (update events + dependency edges) is native output and is a DAG, so
  it "has cones" by definition. But that is irrelevant as stated: the load-bearing property is
  MANIFOLD-LIKENESS of the causal order, which is measure-zero. The causal-set program proves the twin
  of our crumpling attractor: Kleitman-Rothschild -- almost all finite posets have height 3 (order
  diameter O(1)). A generic intrinsic causal graph crumples too.
- WPP's Einstein-equation derivation (Gorard, Complex Systems 29(2) 2020, arXiv:2004.14810) is
  CONDITIONAL on causal invariance + fixed finite dimension + weak ergodicity -- it assumes exactly
  what the program keeps failing to produce. Causal invariance is not generic; the multiway fix
  reintroduces branching. The sharp external critiques (Aaronson quant-ph/0206089; Becker/SciAm 2020)
  bite: "search rule space until physics appears" is fitting, not explanation. So intrinsic causality
  turns "tune a coupling" into "search a rule space with NO action to steer it" -- strictly worse than
  CDT, whose Regge action + causal constraint define a measure that PENALIZES crumpled orders.
- BUILD: causality is INPUT (Jordan-Loll local spacelike/timelike labels + Regge action -- the only
  demonstrated escape). But log the intrinsic event-dependency DAG for free and test it. Cheapest
  discriminator: LONGEST CHAIN (height) vs N via one topological sort. Extended order -> height ~ N^(1/4);
  crumpled/KR -> O(1)-O(log N). If the untuned rewriter's causal graph has polynomial height it earns
  Myrheim-Meyer dimension + cone-volume growth + maximal-antichain ~ N^(3/4); if O(log N), "intrinsic
  causality is free" is empirically dead for this substrate (one hook + one traversal settles it).

## Verdict 2 (Horava seat): Horava is the principled target, but the current gate CANNOT confirm it -- add the anisotropy exponent z
- The weaker thesis in the continuum IS Horava-Lifshitz: foliation-preserving diffeos + anisotropic
  scaling z (=D; z=2 in 2+1D, z=3 in 3+1D) [Horava PRD 79 084008 / arXiv:0901.3775]. 2D CDT = quantized
  2D projectable HL is theorem-level [Ambjorn-Glaser-Sato-Watabiki, PLB 722 (2013) 172, arXiv:1302.6359];
  higher-D is structural resemblance [Ambjorn et al. PLB 690 (2010) 413, arXiv:1002.3298], not proven.
- CRUCIAL: d_s: 4->2 is NECESSARY not sufficient -- it is universal across HL, asymptotic safety, etc.
  And the program's chosen escape (locally-causal CDT) is exactly where the Horava reading is WEAKEST:
  Jordan-Loll show the foliation is inessential, so the continuum could be ISOTROPIC GR (z=1), not
  Lifshitz. "Impose a foliation" does NOT generically land on Horava -- it can land on crumpled,
  branched, modulated, arbitrary z, or an untuned preferred-frame theory. Horava is a multicritical
  target you STEER to, not a basin you fall into.
- THE FINGERPRINT: the anisotropy exponent z, from independent spatial vs temporal correlation lengths
  (xi_t ~ xi_x^z) via anisotropic finite-size scaling. z~2 (2+1D) flowing to 1 in the IR = Horava.
  This is THE discriminator; d_H=3 and diameter~N^(1/3) alone cannot tell emergent GR from Horava from
  a junk preferred-frame theory -- three very different continuum fates.

## Cheap class-sorter (both seats): the DIRECTION of the spectral-dimension flow
- CDT / Horava: d_s DECREASES 4->2 toward the UV. Causal-set / isotropic-Lorentz-invariant: d_s
  INCREASES toward the UV [Eichhorn-Mizera, CQG 31 (2014) 125007, arXiv:1311.2530]. Measuring d_s(sigma)
  on whatever causal graph we produce cheaply sorts which universality class we are in.

## UPGRADED acceptance gate (supersedes the earlier gate)
d_H stable at 3 across factor-30 N + diameter ~ N^(1/3) + sublinear max-degree + certified 3-manifold,
PLUS: (a) the anisotropy exponent z measured (target ~2 in 2+1D flowing to 1 IR); (b) spectral-dimension
flow DIRECTION (4->2 = CDT/Horava; increasing = isotropic/causal-set); (c) a REFOLIATION test -- if key
observables (V(t) profile, lambda, d_s) are foliation-independent, the target may be GR (z=1), which is a
FINDING not a failure. Instrument the intrinsic Wolfram causal-graph height test in parallel.

## Pathology monitors from day one (Horava seat)
- Scalar graviton / strong coupling as lambda -> 1: track Var[V(t)]/<V> and the fitted DeWitt lambda vs
  lattice spacing [Blas-Pujolas-Sibiryakov arXiv:0906.3046].
- Projectable IR instability / signature change: monitor the SIGN and V-dependence of the transfer-matrix
  kinetic term <(V_{t+1}-V_t)^2 | V_t> -- a sign flip / bifurcating map is the CDT "bifurcation phase"
  alarm [Ambjorn et al. JHEP 1608:033, arXiv:1610.05245].
- Low-energy Lorentz violation: temporal/spatial correlation-length ratio must converge; isotropy of
  geodesic-ball growth (BFS in graph distance vs causal depth) at largest N.

## Three possible outcomes and their meaning
- Crumpled (d_H->inf / diameter frozen / z ill-defined): last route closed; strong AND weak theses done.
- Extended with z~2 (2+1D): the WEAKER (Horava) thesis CONFIRMED -- the program's defensible success.
- Extended with z->1, foliation-independent: emergent isotropic GR -- a STRONGER-than-Horava result
  (full diffeo symmetry restored), and the best possible outcome; report as such.
