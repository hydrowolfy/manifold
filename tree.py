"""The canonical reconstruction hierarchy (document 0), encoded as data.

This is the single source of truth for the project's STRUCTURE and its honest SCOREBOARD at
leaf granularity. Each node carries a grade; each subsection optionally points to the library
module that implements it (`exp`, a dotted path under the v8.1 domain packages) and/or to the
monolith commands that back it (`mono`, runnable via emergence_monolith.py).

Grades (v8.1 vocabulary, post-referee):
  DEF        infrastructure / definitional (no physics claimed)
  DERIVED    fell out / computed, with proof or strong evidence
  PARTIAL    a real but incomplete result
  BORROWED   relies on an external theorem (Gorard; Osterwalder-Schrader; causal-set order)
  CONJECTURE proposed, untested
  OPEN       identified target, not started
  REFUTED    tested and failed
  EXT        external experimental proposal (not a substrate result)

The grades here are aligned to Reconstructing-the-Physics-Hierarchy_v8.1.md and REFEREE_REPORT_v1.md.
Notable referee corrections baked in: local confluence is PARTIAL (joinable, not yet a theorem);
the consistency-dimension ceiling is PARTIAL (empirical); curvature is sign-only; dimension is a
range; nothing is graded on a "3+1" assumption.
"""

GRADES = ["DEF", "DERIVED", "PARTIAL", "BORROWED", "CONJECTURE", "OPEN", "REFUTED", "EXT"]


def SUB(sid, name, status, leaves, exp=None, mono=()):
    return {"id": sid, "name": name, "status": status,
            "leaves": [{"name": n, "status": s} for (n, s) in leaves],
            "exp": exp, "mono": list(mono)}


# ----------------------------------------------------------------------------------------------
# 0 — CORE SUBSTRATE
SEC0 = ("0", "Core substrate", [
    SUB("0.1", "Hypergraph state", "DEF", [
        ("Nodes", "DEF"), ("Hyperedges", "DEF"), ("Incidence structure", "DEF"),
        ("Local neighborhoods", "DEF"), ("Graph/hypergraph distance", "DEF")],
        exp="sec00_core_substrate.hypergraph", mono=["keystone", "hypergraph"]),
    SUB("0.2", "Rewrite rule", "DEF", [
        ("Local replacement rule", "DEF"), ("Rule matching", "DEF"), ("Rule application", "DEF"),
        ("Update ordering", "DEF"), ("Rule invariants", "DERIVED")],
        exp="sec00_core_substrate.rule_invariants", mono=["keystone", "hypergraph"]),
    SUB("0.3", "Evolution history", "DERIVED", [
        ("Event sequence", "DERIVED"), ("Causal dependencies", "DERIVED"),
        ("Causal graph", "DERIVED"), ("Branching histories", "PARTIAL"),
        ("Coarse-grained histories", "OPEN")],
        exp="sec00_core_substrate.causal_graph", mono=["bridge", "overlap"]),
    SUB("0.4", "Observables", "DEF", [
        ("Node count", "DEF"), ("Edge count", "DEF"), ("Degree distribution", "OPEN"),
        ("Clustering", "PARTIAL"), ("Path length", "DEF"), ("Dimension estimators", "PARTIAL"),
        ("Entropy proxies", "PARTIAL"), ("Conservation candidates", "DERIVED")],
        exp="sec00_core_substrate.observables", mono=["midi"]),
])

# 1 — RAW WOLFRAM / HYPERGRAPH FACTS
SEC1 = ("1", "Raw Wolfram / hypergraph facts", [
    SUB("1.1", "Causal structure", "DERIVED", [
        ("Partial order of events", "DERIVED"), ("Causal cones", "DERIVED"),
        ("Event horizons", "PARTIAL"), ("Causal invariance tests", "PARTIAL")],
        exp=["sec01_raw_wolfram_hypergraph_facts.s1_1_causal_structure", "sec07_special_relativity.s7_1_invariant_speed"],
        mono=["confluence", "bridge", "overlap"]),
    SUB("1.2", "Locality", "PARTIAL", [
        ("Neighborhood preservation", "DERIVED"), ("Propagation bounds", "PARTIAL"),
        ("Effective signal speed", "PARTIAL"), ("Nonlocal artifact detection", "OPEN")],
        mono=["channel", "rapidity"]),
    SUB("1.3", "Dimensionality", "DERIVED", [
        ("Hausdorff dimension", "PARTIAL"), ("Spectral dimension", "DERIVED"),
        ("Box-counting dimension", "DERIVED"), ("Scaling windows", "DERIVED"),
        ("Non-integer dimension behavior", "DERIVED")],
        exp=["sec01_raw_wolfram_hypergraph_facts.s1_3_dimensionality", "sec01_raw_wolfram_hypergraph_facts.s1_3_dimensionality_spectral"],
        mono=["specdim", "family", "dimension", "tension", "knob", "depth"]),
    SUB("1.4", "Symmetry", "BORROWED", [
        ("Translation-like invariance", "PARTIAL"), ("Rotation-like invariance", "PARTIAL"),
        ("Boost-like invariance", "BORROWED"), ("Isotropy tests", "PARTIAL"),
        ("Anisotropy diagnostics", "PARTIAL")],
        mono=["twoplus", "threeplus", "closure", "cone"]),
    SUB("1.5", "Statistics", "DERIVED", [
        ("Growth statistics", "DERIVED"), ("Degree statistics", "DERIVED"),
        ("Fluctuation statistics", "PARTIAL"), ("Correlation functions", "OPEN"),
        ("Noise spectra", "PARTIAL"), ("Boost-Fano diagnostics", "PARTIAL")],
        exp=["sec01_raw_wolfram_hypergraph_facts.s1_5_statistics", "sec01_raw_wolfram_hypergraph_facts.s1_5_statistics_degree"],
        mono=["grid", "source", "hunt", "branch", "grain", "round", "dynamic", "fulldist"]),
    SUB("1.6", "Coarse-graining", "OPEN", [
        ("Microstate grouping", "PARTIAL"), ("Effective macrovariables", "PARTIAL"),
        ("Renormalization-like flow", "OPEN"), ("Continuum limits", "DERIVED"),
        ("Scale-dependent behavior", "PARTIAL")],
        exp=["sec01_raw_wolfram_hypergraph_facts.s1_6_continuum_fractal_tree",
             "sec01_raw_wolfram_hypergraph_facts.s1_6_manifold_phase_transition",
             "sec01_raw_wolfram_hypergraph_facts.s1_6_history_enriched_geometry",
             "sec01_raw_wolfram_hypergraph_facts.s1_6_manifold_modification",
             "sec01_raw_wolfram_hypergraph_facts.s1_7_coherent_mesh",
             "sec01_raw_wolfram_hypergraph_facts.s1_8_manifold_d3",
             "sec01_raw_wolfram_hypergraph_facts.s1_9_causal_foliation",
             "sec01_raw_wolfram_hypergraph_facts.s1_10_frame_free_dimension",
             "sec01_raw_wolfram_hypergraph_facts.s1_11_genus_obstruction",
             "sec01_raw_wolfram_hypergraph_facts.s1_12_connection_reduction",
             "sec01_raw_wolfram_hypergraph_facts.s1_13_condensation_route",
             "sec01_raw_wolfram_hypergraph_facts.s1_14_global_action",
             "sec01_raw_wolfram_hypergraph_facts.s1_15_minor_universality_d3",
             "sec01_raw_wolfram_hypergraph_facts.s1_16_growth_cap_dial",
             "sec01_raw_wolfram_hypergraph_facts.s1_17_matter_viability",
             "sec01_raw_wolfram_hypergraph_facts.s1_18_gauge_flux_sectors",
             "sec01_raw_wolfram_hypergraph_facts.s1_19_deficit_selection",
             "sec01_raw_wolfram_hypergraph_facts.s1_20_triple_objective",
             "sec01_raw_wolfram_hypergraph_facts.s1_21_annealing_dynamics",
             "sec01_raw_wolfram_hypergraph_facts.s1_22_isotropy_sandwich",
             "sec01_raw_wolfram_hypergraph_facts.s1_23_dim3_sandwich",
             "sec01_raw_wolfram_hypergraph_facts.s1_24_dim3_scaling_gate"], mono=["sprinkle"]),
])

# 2 — PRE-NEWTONIAN KINEMATICS
SEC2 = ("2", "Pre-Newtonian kinematics", [
    SUB("2.1", "Space proxies", "PARTIAL", [
        ("Distance", "DERIVED"), ("Direction", "PARTIAL"), ("Neighborhoods", "DERIVED"),
        ("Effective coordinates", "PARTIAL"), ("Spatial slices", "PARTIAL")]),
    SUB("2.2", "Time proxies", "PARTIAL", [
        ("Rewrite step time", "DERIVED"), ("Causal time", "DERIVED"),
        ("Clock construction", "PARTIAL"), ("Proper-time candidates", "PARTIAL"),
        ("Foliation dependence", "PARTIAL")],
        mono=["lrule", "relaxer"]),
    SUB("2.3", "Motion", "DERIVED", [
        ("Persistent structures", "DERIVED"), ("Excitation tracking", "DERIVED"),
        ("Trajectories", "DERIVED"), ("Velocity proxies", "DERIVED"),
        ("Acceleration proxies", "OPEN")],
        exp="sec04_newtonian_mechanics.s4_1_inertial_motion", mono=["particle", "glider"]),
    SUB("2.4", "Measurement", "PARTIAL", [
        ("Internal observers", "PARTIAL"), ("Rulers", "PARTIAL"), ("Clocks", "PARTIAL"),
        ("Operational definitions", "PARTIAL"), ("Observer-independent quantities", "PARTIAL")],
        mono=["rapidity", "sprinkle"]),
])

# 3 — CONSERVATION LAWS
SEC3 = ("3", "Conservation laws", [
    SUB("3.1", "Counting invariants", "DERIVED", [
        ("Node conservation candidates", "DERIVED"), ("Edge conservation candidates", "DERIVED"),
        ("Degree-sum constraints", "DERIVED"), ("Boundary terms", "OPEN"),
        ("Defect accounting", "DERIVED")],
        exp="sec03_conservation_laws.s3_1_counting_invariants", mono=["matter", "nodecreate", "branch"]),
    SUB("3.2", "Flow invariants", "OPEN", [
        ("Conserved currents", "OPEN"), ("Flux through surfaces", "OPEN"),
        ("Continuity equations", "OPEN"), ("Source/sink terms", "OPEN"),
        ("Local balance laws", "OPEN")]),
    SUB("3.3", "Momentum-like quantities", "DERIVED", [
        ("Translation symmetry link", "OPEN"), ("Persistent drift", "DERIVED"),
        ("Collision bookkeeping", "DERIVED"), ("Center-of-mass proxies", "OPEN"),
        ("Momentum conservation tests", "DERIVED")],
        exp="sec03_conservation_laws.s3_3_momentum_like_quantities", mono=["collide"]),
    SUB("3.4", "Energy-like quantities", "OPEN", [
        ("Rewrite activity", "PARTIAL"), ("Curvature/activity density", "OPEN"),
        ("Local update rate", "PARTIAL"), ("Hamiltonian candidates", "PARTIAL"),
        ("Energy conservation tests", "OPEN")],
        mono=["heisenberg"]),
    SUB("3.5", "Angular momentum-like quantities", "OPEN", [
        ("Rotation symmetry link", "OPEN"), ("Circulation", "OPEN"),
        ("Orbital motion proxies", "OPEN"), ("Spin-like defects", "OPEN"),
        ("Angular momentum conservation tests", "OPEN")]),
])

# 4 — NEWTONIAN MECHANICS
SEC4 = ("4", "Newtonian mechanics", [
    SUB("4.1", "Inertial motion", "DERIVED", [
        ("Free-particle candidates", "DERIVED"), ("Straight-line motion", "DERIVED"),
        ("Constant-velocity motion", "DERIVED"), ("Galilean frames", "PARTIAL"),
        ("Inertial frame tests", "PARTIAL")],
        exp="sec04_newtonian_mechanics.s4_1_inertial_motion", mono=["glider"]),
    SUB("4.2", "Force", "PARTIAL", [
        ("Acceleration from graph gradients", "PARTIAL"), ("Interaction neighborhoods", "PARTIAL"),
        ("Effective force laws", "PARTIAL"), ("Action-reaction tests", "OPEN"),
        ("Force superposition tests", "OPEN"),
        ("Charge-responsive dynamics (holonomy-mismatch bias)", "REFUTED"),
        ("Force on matter (field-energy coupling)", "PARTIAL")],
        exp=["sec04_newtonian_mechanics.s4_2_force",
             "sec04_newtonian_mechanics.s4_2_force_coupling"]),
    SUB("4.3", "Mass", "PARTIAL", [
        ("Inertial mass proxy", "PARTIAL"), ("Gravitational mass proxy", "OPEN"),
        ("Resistance to acceleration", "PARTIAL"), ("Defect/activity mass", "PARTIAL"),
        ("Equivalence tests", "OPEN")],
        exp=["sec04_newtonian_mechanics.s4_3_inertia_and_acceleration",
             "sec04_newtonian_mechanics.s4_3_mass_as_zitterbewegung",
             "sec04_newtonian_mechanics.s4_3_dirac_mass_obstruction"]),
    SUB("4.4", "Potentials", "PARTIAL", [
        ("Scalar potential candidates", "OPEN"), ("Gradient flow", "OPEN"),
        ("Effective potential wells", "OPEN"), ("Bound states", "PARTIAL"),
        ("Stability criteria", "PARTIAL")],
        exp="sec04_newtonian_mechanics.s4_4_potentials"),
    SUB("4.5", "Central forces", "PARTIAL", [
        ("Inverse-square behavior", "REFUTED"), ("Radial symmetry", "OPEN"),
        ("Orbital trajectories", "PARTIAL"), ("Kepler-like laws", "REFUTED"), ("Virial checks", "PARTIAL")],
        exp="sec04_newtonian_mechanics.s4_5_mesons_confined_bound_states"),
    SUB("4.6", "Many-body mechanics", "PARTIAL", [
        ("Pairwise interactions", "PARTIAL"), ("Collective motion", "OPEN"),
        ("Scattering", "PARTIAL"), ("Relaxation", "PARTIAL"),
        ("Emergent continuum mechanics", "OPEN")],
        exp=["sec04_newtonian_mechanics.s4_4_potentials",
             "sec04_newtonian_mechanics.s4_6_scattering",
             "sec04_newtonian_mechanics.s4_6_meson_meson",
             "sec04_newtonian_mechanics.s4_6_tetraquark_binding"], mono=["collide"]),
])

# 5 — STATISTICAL MECHANICS AND THERMODYNAMICS
SEC5 = ("5", "Statistical mechanics and thermodynamics", [
    SUB("5.1", "Microstates and macrostates", "PARTIAL", [
        ("Microstate enumeration", "PARTIAL"), ("Macrostate variables", "OPEN"),
        ("Coarse-graining maps", "PARTIAL"), ("State degeneracy", "OPEN"), ("Typicality", "OPEN")]),
    SUB("5.2", "Entropy", "DERIVED", [
        ("Graph entropy", "DERIVED"), ("Causal entropy", "PARTIAL"), ("Branch entropy", "PARTIAL"),
        ("Entropy growth", "DERIVED"), ("Entropy bounds", "OPEN")],
        exp="sec05_statistical_mechanics_and_thermodynamics.s5_2_entropy"),
    SUB("5.3", "Equilibrium", "DERIVED", [
        ("Equilibration tests", "DERIVED"), ("Detailed balance", "DERIVED"),
        ("Stationary distributions", "DERIVED"), ("Thermalization", "PARTIAL"),
        ("Fluctuation behavior", "PARTIAL")],
        exp=["sec05_statistical_mechanics_and_thermodynamics.s5_3_equilibrium",
             "sec05_statistical_mechanics_and_thermodynamics.s5_3_quench_localization",
             "sec05_statistical_mechanics_and_thermodynamics.s5_3_level_spacing_statistics",
             "sec05_statistical_mechanics_and_thermodynamics.s5_3_otoc_scrambling",
             "sec05_statistical_mechanics_and_thermodynamics.s5_3_krylov_complexity",
             "sec05_statistical_mechanics_and_thermodynamics.s5_3_localization_transition",
             "sec05_statistical_mechanics_and_thermodynamics.s5_3_critical_dynamics",
             "sec05_statistical_mechanics_and_thermodynamics.s5_3_spectral_dimension",
             "sec05_statistical_mechanics_and_thermodynamics.s5_3_mbl",
             "sec05_statistical_mechanics_and_thermodynamics.s5_3_mbl_dynamics"]),
    SUB("5.4", "Temperature", "OPEN", [
        ("Activity-temperature proxy", "OPEN"), ("Fluctuation-temperature relation", "OPEN"),
        ("Equipartition-like tests", "OPEN"), ("Heat capacity proxy", "OPEN"),
        ("Thermal gradients", "OPEN")]),
    SUB("5.5", "Irreversibility", "DERIVED", [
        ("Arrow of time", "DERIVED"), ("Entropy production", "DERIVED"),
        ("Loschmidt-style reversibility checks", "PARTIAL"),
        ("Coarse-graining irreversibility", "DERIVED"), ("Information loss", "PARTIAL")],
        exp="sec05_statistical_mechanics_and_thermodynamics.s5_5_irreversibility"),
])

# 6 — MAXWELL / CLASSICAL FIELD THEORY
SEC6 = ("6", "Maxwell / classical field theory", [
    SUB("6.1", "Field variables", "DERIVED", [
        ("Scalar fields", "OPEN"), ("Vector fields", "OPEN"), ("Tensor fields", "OPEN"),
        ("Field values on nodes", "PARTIAL"), ("Field values on edges", "DERIVED"),
        ("Field values on hyperedges", "OPEN")],
        exp="sec06_maxwell_classical_field_theory.s6_1_field_variables"),
    SUB("6.2", "Charge-like quantities", "DERIVED", [
        ("Source defects", "DERIVED"), ("Sink defects", "DERIVED"),
        ("Conserved charge", "DERIVED"), ("Charge neutrality", "DERIVED"),
        ("Charge-current continuity", "DERIVED")],
        exp="sec06_maxwell_classical_field_theory.s6_2_charge_like_quantities",
        mono=["matter", "charge"]),
    SUB("6.3", "Electric-field analogues", "PARTIAL", [
        ("Gradient fields", "DERIVED"), ("Divergence", "DERIVED"), ("Gauss-law candidates", "PARTIAL"),
        ("Coulomb-like behavior", "PARTIAL"), ("Electric potential", "DERIVED")],
        exp=["sec06_maxwell_classical_field_theory.s6_3_electric_field_analogues",
             "sec06_maxwell_classical_field_theory.s6_3_confinement_flux_tube",
             "sec06_maxwell_classical_field_theory.s6_3_deconfinement_dimension"]),
    SUB("6.4", "Magnetic-field analogues", "PARTIAL", [
        ("Circulation", "DERIVED"), ("Curl-like operators", "DERIVED"), ("Loop defects", "DERIVED"),
        ("No-monopole constraint", "DERIVED"), ("Magnetic flux", "PARTIAL")],
        exp="sec06_maxwell_classical_field_theory.s6_4_magnetic_and_induction"),
    SUB("6.5", "Maxwell equations", "PARTIAL", [
        ("Gauss law", "PARTIAL"), ("No magnetic monopoles", "DERIVED"),
        ("Faraday induction", "DERIVED"), ("Ampere-Maxwell law", "PARTIAL"),
        ("Continuity equation", "DERIVED")],
        exp=["sec06_maxwell_classical_field_theory.s6_5_maxwell_equations",
             "sec06_maxwell_classical_field_theory.s6_5_coupling_constant",
             "sec06_maxwell_classical_field_theory.s6_5_retarded_field",
             "sec06_maxwell_classical_field_theory.s6_5_continuity"]),
    SUB("6.6", "Gauge structure", "DERIVED", [
        ("Gauge redundancy", "DERIVED"), ("Gauge transformations", "DERIVED"),
        ("Potentials versus fields", "DERIVED"), ("Local phase-like freedom", "DERIVED"),
        ("Gauge-invariant observables", "DERIVED")],
        exp="sec06_maxwell_classical_field_theory.s6_6_gauge_structure", mono=["charge"]),
    SUB("6.7", "Radiation and waves", "PARTIAL", [
        ("Wave equation", "PARTIAL"), ("Propagation speed", "PARTIAL"), ("Polarization", "OPEN"),
        ("Dispersion", "OPEN"), ("Radiation from accelerating charges", "PARTIAL"),
        ("Energy flux / Poynting-like vector", "PARTIAL")],
        exp="sec06_maxwell_classical_field_theory.s6_7_photon_and_radiation"),
])

# 7 — SPECIAL RELATIVITY
SEC7 = ("7", "Special relativity", [
    SUB("7.1", "Invariant speed", "PARTIAL", [
        ("Maximum signal speed", "PARTIAL"), ("Light-cone structure", "DERIVED"),
        ("Maxwell-to-Lorentz bridge", "OPEN"), ("Speed-of-light normalization", "BORROWED"),
        ("Signal-speed isotropy", "PARTIAL")],
        exp="sec07_special_relativity.s7_1_invariant_speed", mono=["fronts", "cone", "lightcone", "channel"]),
    SUB("7.2", "Observer frames", "PARTIAL", [
        ("Internal observers", "PARTIAL"), ("Moving observers", "PARTIAL"),
        ("Frame transformations", "BORROWED"), ("Boost operations", "PARTIAL"),
        ("Frame equivalence tests", "PARTIAL")]),
    SUB("7.3", "Lorentz behavior", "BORROWED", [
        ("Time dilation", "PARTIAL"), ("Length contraction", "BORROWED"),
        ("Relativity of simultaneity", "BORROWED"), ("Velocity composition", "PARTIAL"),
        ("Lorentz invariance hierarchy tests", "PARTIAL")],
        exp=["sec07_special_relativity.s7_3_lorentz_behavior",
             "sec07_special_relativity.s7_4_zitterbewegung_dispersion"], mono=["rapidity"]),
    SUB("7.4", "Minkowski structure", "BORROWED", [
        ("Invariant interval", "BORROWED"), ("Proper time", "BORROWED"),
        ("Four-velocity", "BORROWED"), ("Four-momentum", "BORROWED"),
        ("Mass-energy relation", "DERIVED")],
        exp=["sec07_special_relativity.s7_4_minkowski_structure",
             "sec07_special_relativity.s7_4_zitterbewegung_dispersion"], mono=["lightcone"]),
    SUB("7.5", "Symmetry restoration", "CONJECTURE", [
        ("Preferred microscopic foliation", "CONJECTURE"), ("Low-energy Lorentz emergence", "CONJECTURE"),
        ("UV Lorentz violation checks", "PARTIAL"), ("IR symmetry restoration", "CONJECTURE"),
        ("CMB-frame-style detectability tests", "PARTIAL")],
        mono=["doors", "closure", "z"]),
])

# 8 — EARLY QUANTUM / PRE-QM LAYER
SEC8 = ("8", "Early quantum / pre-QM layer", [
    SUB("8.1", "Discreteness", "DERIVED", [
        ("Quantized events", "DERIVED"), ("Quantized action candidates", "PARTIAL"),
        ("Minimum update units", "DERIVED"), ("Spectral discreteness", "PARTIAL"),
        ("Energy packet behavior", "PARTIAL")]),
    SUB("8.2", "Wave-particle behavior", "PARTIAL", [
        ("Persistent localized excitations", "DERIVED"), ("Wave propagation", "OPEN"),
        ("Interference-like effects", "OPEN"), ("Diffraction-like behavior", "OPEN"),
        ("De Broglie-style relations", "OPEN")]),
    SUB("8.3", "Atomic / bound-state analogues", "PARTIAL", [
        ("Stable bound structures", "PARTIAL"), ("Discrete spectra", "OPEN"),
        ("Transition rules", "OPEN"), ("Emission/absorption analogues", "OPEN"),
        ("Selection-rule candidates", "OPEN")]),
    SUB("8.4", "Uncertainty-like behavior", "OPEN", [
        ("Position/momentum proxy tradeoff", "OPEN"), ("Sampling limits", "OPEN"),
        ("Coarse-graining uncertainty", "OPEN"), ("Measurement disturbance", "OPEN"),
        ("Fourier-like uncertainty", "OPEN")],
        exp="sec08_early_quantum_pre_qm_layer.s8_4_uncertainty_like_behavior"),
])

# 9 — QUANTUM MECHANICS
SEC9 = ("9", "Quantum mechanics", [
    SUB("9.1", "Multiway evolution", "PARTIAL", [
        ("Branching histories", "PARTIAL"), ("Branchial graph", "PARTIAL"), ("Path sums", "PARTIAL"),
        ("Interference between branches", "PARTIAL"), ("Rule-ordering superposition", "PARTIAL")],
        exp="sec09_quantum_mechanics.s9_1_multiway_evolution", mono=["branchial", "weld", "action"]),
    SUB("9.2", "Amplitudes", "BORROWED", [
        ("Amplitude reconstruction", "BORROWED"), ("Complex phase candidates", "BORROWED"),
        ("Probability weights", "BORROWED"), ("Norm preservation", "BORROWED"),
        ("Unitarity tests", "PARTIAL")],
        exp="sec09_quantum_mechanics.s9_2_amplitudes", mono=["rp", "heisenberg", "weld", "action"]),
    SUB("9.3", "Born rule", "BORROWED", [
        ("Branch counting", "PARTIAL"), ("Measure problem", "CONJECTURE"),
        ("Squared-amplitude behavior", "BORROWED"), ("Typicality arguments", "CONJECTURE"),
        ("Statistical tests", "PARTIAL")],
        exp="sec09_quantum_mechanics.s9_3_born_rule"),
    SUB("9.4", "Measurement", "CONJECTURE", [
        ("Observer-system split", "OPEN"), ("Decoherence", "CONJECTURE"),
        ("Record formation", "OPEN"), ("Apparent collapse", "OPEN"),
        ("Information loss accounting", "CONJECTURE")],
        exp="sec09_quantum_mechanics.s9_4_measurement"),
    SUB("9.5", "Entanglement", "OPEN", [
        ("Branchial adjacency", "PARTIAL"), ("Correlation structure", "PARTIAL"),
        ("Bell-test analogues", "OPEN"), ("No-signaling checks", "OPEN"),
        ("Entanglement entropy", "PARTIAL")],
        exp=["sec09_quantum_mechanics.s9_5_entanglement",
             "sec09_quantum_mechanics.s9_5_entanglement_entropy_area_law",
             "sec09_quantum_mechanics.s9_5_entanglement_negativity"]),
])

# 10 — GENERAL RELATIVITY
SEC10 = ("10", "General relativity", [
    SUB("10.1", "Metric emergence", "PARTIAL", [
        ("Distance metric", "PARTIAL"), ("Time metric", "PARTIAL"),
        ("Effective spacetime metric", "PARTIAL"), ("Signature", "BORROWED"),
        ("Continuum approximation", "PARTIAL")],
        exp=["sec07_special_relativity.s7_4_minkowski_structure",
             "sec10_general_relativity.s10_1_causal_set_dimension"],
        mono=["grow", "genesis", "climb", "foliation"]),
    SUB("10.2", "Curvature", "DERIVED", [
        ("Graph curvature", "DERIVED"), ("Ricci-like curvature", "DERIVED"),
        ("Scalar curvature", "PARTIAL"), ("Curvature from update density", "PARTIAL"),
        ("Curvature-flow relation", "OPEN")],
        exp=["sec10_general_relativity.s10_2_curvature", "sec10_general_relativity.s10_2_emergent_curvature", "sec10_general_relativity.s10_2_hyperbolicity"], mono=["curvature", "desitter", "ricci"]),
    SUB("10.3", "Geodesics", "OPEN", [
        ("Shortest-path motion", "PARTIAL"), ("Extremal-action motion", "OPEN"),
        ("Free-fall trajectories", "OPEN"), ("Geodesic deviation", "OPEN"),
        ("Equivalence principle tests", "OPEN")],
        exp="sec10_general_relativity.s10_3_geodesics"),
    SUB("10.4", "Einstein limit", "PARTIAL", [
        ("Stress-energy analogue", "OPEN"), ("Einstein-equation approximation", "PARTIAL"),
        ("Newtonian gravity limit", "OPEN"), ("Gravitational waves", "OPEN"),
        ("Constraint equations", "PARTIAL")],
        exp="sec10_general_relativity.s10_4_einstein_limit", mono=["einstein"]),
    SUB("10.5", "Strong gravity", "PARTIAL", [
        ("Horizons", "PARTIAL"), ("Black-hole analogues", "PARTIAL"), ("Singularities", "OPEN"),
        ("Information paradox analogues", "PARTIAL"), ("Hawking-like behavior", "OPEN")],
        exp=["sec10_general_relativity.s10_5_strong_gravity",
             "sec10_general_relativity.s10_5_page_curve"],
        mono=["horizon", "scaling", "coefficient"]),
])

# 11 — QUANTUM FIELD THEORY
SEC11 = ("11", "Quantum field theory", [
    SUB("11.1", "Fields as excitations", "PARTIAL", [
        ("Local field modes", "PARTIAL"), ("Particle excitations", "DERIVED"),
        ("Creation/annihilation analogues", "REFUTED"), ("Vacuum state", "DERIVED"),
        ("Correlation functions", "PARTIAL")],
        exp="sec11_quantum_field_theory.s11_1_loop_defects_and_vacuum"),
    SUB("11.2", "Propagators", "PARTIAL", [
        ("Green-function analogues", "DERIVED"), ("Path-integral behavior", "PARTIAL"),
        ("Scattering amplitudes", "OPEN"), ("Feynman-diagram analogues", "OPEN"),
        ("Causality constraints", "PARTIAL")],
        exp=["sec11_quantum_field_theory.s11_2_propagator_and_spectral_density"], mono=["pathintegral"]),
    SUB("11.3", "Gauge theories", "DERIVED", [
        ("U(1)-like electromagnetism", "DERIVED"), ("Non-Abelian analogues", "OPEN"),
        ("Yang-Mills-like structure", "OPEN"), ("Charge conservation", "DERIVED"),
        ("Gauge boson candidates", "OPEN")],
        exp="sec06_maxwell_classical_field_theory.s6_6_gauge_structure", mono=["charge", "matter"]),
    SUB("11.4", "Renormalization", "PARTIAL", [
        ("Coarse-graining flow", "OPEN"), ("Scale dependence", "DERIVED"), ("Fixed points", "PARTIAL"),
        ("Relevant/irrelevant operators", "OPEN"), ("Continuum effective theory", "OPEN")],
        exp=["sec11_quantum_field_theory.s11_4_running_spectral_dimension"]),
    SUB("11.5", "Standard Model bridge", "CONJECTURE", [
        ("Fermion candidates", "CONJECTURE"), ("Boson candidates", "OPEN"),
        ("Chirality", "CONJECTURE"), ("Symmetry breaking", "CONJECTURE"),
        ("Coupling constants", "OPEN")],
        mono=["jw", "bott", "dome", "edge", "op7"]),
])

# 12 — COSMOLOGY
SEC12 = ("12", "Cosmology", [
    SUB("12.1", "Expansion", "PARTIAL", [
        ("Graph growth", "DERIVED"), ("Scale factor proxy", "PARTIAL"),
        ("Hubble-like relation", "PARTIAL"), ("Redshift analogue", "OPEN"),
        ("Expansion history", "PARTIAL")],
        exp="sec12_cosmology.s12_1_expansion", mono=["cosmos", "desitter"]),
    SUB("12.2", "Early universe", "OPEN", [
        ("Initial conditions", "PARTIAL"), ("Inflation-like behavior", "OPEN"),
        ("Horizon problem", "OPEN"), ("Flatness problem", "OPEN"),
        ("Primordial fluctuations", "OPEN")]),
    SUB("12.3", "Structure formation", "OPEN", [
        ("Density perturbations", "OPEN"), ("Clustering", "OPEN"), ("Power spectrum", "OPEN"),
        ("Galaxy-scale analogues", "OPEN"), ("Large-scale structure", "OPEN")]),
    SUB("12.4", "CMB analogues", "PARTIAL", [
        ("Preferred frame diagnostics", "PARTIAL"), ("Thermal background", "OPEN"),
        ("Anisotropy spectrum", "OPEN"), ("Acoustic-peak analogues", "OPEN"),
        ("Observer motion corrections", "PARTIAL")],
        mono=["cosmos", "grid"]),
    SUB("12.5", "Dark sector", "CONJECTURE", [
        ("Dark-matter candidates", "CONJECTURE"), ("Dark-energy candidates", "CONJECTURE"),
        ("Vacuum energy", "OPEN"), ("Measurement-information-loss model", "CONJECTURE"),
        ("Effective cosmological constant", "CONJECTURE")],
        exp="sec12_cosmology.s12_5_dark_sector"),
])

# 13 — SPECULATIVE EXTENSIONS / APPENDICES
SEC13 = ("13", "Speculative extensions / appendices", [
    SUB("13.1", "Boost-Fano statistics", "PARTIAL", [
        ("Definition", "DERIVED"), ("Motivation", "DERIVED"), ("Lorentz-noise diagnostic", "PARTIAL"),
        ("Emergence diagnostic", "PARTIAL"), ("Experimental interpretation", "PARTIAL")],
        mono=["grid", "hunt", "branch", "grain", "round", "dynamic", "fulldist", "source"]),
    SUB("13.2", "Horava-like interpretation", "CONJECTURE", [
        ("Preferred foliation", "CONJECTURE"), ("UV Lorentz violation", "PARTIAL"),
        ("IR Lorentz restoration", "CONJECTURE"), ("Scale-dependent symmetry", "CONJECTURE"),
        ("Difference from Horava-Lifshitz gravity", "PARTIAL")],
        mono=["z", "doors", "closure"]),
    SUB("13.3", "Measurement-information-loss cosmology", "CONJECTURE", [
        ("Measurement as coarse-graining", "CONJECTURE"), ("Lost information budget", "CONJECTURE"),
        ("Vacuum-pressure analogy", "CONJECTURE"), ("Dark-energy comparison", "CONJECTURE"),
        ("Observational constraints", "CONJECTURE")],
        exp="sec13_speculative_extensions_appendices.s13_3_measurement_information_loss_cosmology"),
    SUB("13.4", "Multiverse / branch coupling", "CONJECTURE", [
        ("Branchial neighborhoods", "PARTIAL"), ("Inter-branch leakage", "CONJECTURE"),
        ("Dark-matter analogy", "CONJECTURE"), ("Level-II / Level-III analogy", "CONJECTURE"),
        ("Testability concerns", "CONJECTURE")],
        exp="sec13_speculative_extensions_appendices.s13_4_multiverse_branch_coupling"),
    SUB("13.5", "Holography / AdS-CFT analogues", "PARTIAL", [
        ("Boundary encoding", "PARTIAL"), ("Bulk reconstruction", "CONJECTURE"),
        ("Entanglement geometry", "REFUTED"), ("Area-law behavior", "PARTIAL"),
        ("Limits of the analogy", "PARTIAL")],
        exp=["sec13_speculative_extensions_appendices.s13_5_holography_area_law",
             "sec09_quantum_mechanics.s9_5_entanglement_entropy_area_law",
             "sec13_speculative_extensions_appendices.s13_5_monogamy_mutual_information"],
        mono=["horizon", "scaling", "coefficient"]),
    SUB("13.6", "Experimental proposals", "EXT", [
        ("SRF cavity tests", "EXT"), ("Chiral superconducting material tests", "EXT"),
        ("Lorentz hierarchy tests", "EXT"), ("Noise anisotropy tests", "EXT"),
        ("Measurement-independence tests", "EXT")]),
])

SECTIONS = [SEC0, SEC1, SEC2, SEC3, SEC4, SEC5, SEC6, SEC7, SEC8, SEC9, SEC10, SEC11, SEC12, SEC13]


# ---- helpers -------------------------------------------------------------------------------
def explist(sub):
    """Normalize a subsection's `exp` (str | list | None) to a list of dotted module paths."""
    e = sub.get("exp")
    if not e:
        return []
    return [e] if isinstance(e, str) else list(e)


def all_subsections():
    for num, name, subs in SECTIONS:
        for s in subs:
            yield num, name, s


def leaf_tally():
    t = {g: 0 for g in GRADES}
    for _, _, s in all_subsections():
        for lf in s["leaves"]:
            t[lf["status"]] = t.get(lf["status"], 0) + 1
    return t


def find(sub_id):
    for _, _, s in all_subsections():
        if s["id"] == sub_id:
            return s
    return None
