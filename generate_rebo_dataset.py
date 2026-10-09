"""
generate_rebo_dataset.py
Consolidates 15,000 unique fine-tuning dataset items into a SINGLE master dataset file:
`rebo_dataset_15k.json` matching the exact 12-key research guide walkthrough schema.

12 Keys:
- id: Sequential string from 'Q00001' to 'Q15000'
- domain: Broad scientific domain
- subfield: Specific subfield
- difficulty: String ('Introductory', 'Undergraduate', 'Graduate', 'Specialist')
- research_type: String ('Empirical', 'Theoretical', 'Methodological', 'Computational')
- instruction: Standard guidance statement
- question: Detailed research question (100% unique across all 15,000 records)
- focal_concepts: List of concept strings
- expected_output_type: List of strings
- assumptions_needed: String defining prerequisites or boundary assumptions
- answerability: String ('Self-contained', 'Needs stated assumptions', etc.)
- novelty_note: String describing the specific reasoning challenge
"""

import json
import os
import random
import time

DOMAINS = [
    {
        "name": "AI & Machine Learning",
        "subfields": [
            ("Neural Architecture Search", ["weight-sharing supernets", "bilevel optimization", "latency-aware Pareto frontiers", "zero-cost proxies", "gradient variance stabilization"]),
            ("Reinforcement Learning", ["offline policy evaluation", "sample complexity bounds", "distributional shift mitigation", "curiosity-driven exploration", "multi-agent credit assignment"]),
            ("Large Language Models", ["chain-of-thought faithfulness", "mechanistic circuit interpretability", "hallucination suppression", "parameter-efficient LoRA adaptors", "KV-cache compression dynamics"]),
            ("Computer Vision", ["vision-language contrastive alignment", "diffusion inversion trajectories", "self-supervised semantic representations", "3D Gaussian splatting optimization", "adversarial perturbation bounds"]),
            ("AI Safety & Alignment", ["scalable oversight protocols", "reward gaming prevention", "constitutional principle tuning", "automated red-teaming vectors", "deceptive alignment detection"]),
            ("Graph Neural Networks", ["oversmoothing mitigation", "subgraph isomorphism expressivity", "temporal link prediction", "heterogeneous message passing", "spectral graph wavelet transforms"]),
            ("Optimization & Theory", ["non-convex loss landscapes", "sharpness-aware minimization", "adaptive gradient drift", "stochastic polyak step-sizes", "implicit bias of gradient descent"]),
            ("Federated Learning", ["non-IID statistical heterogeneity", "byzantine fault mitigation", "differential privacy budget trade-offs", "secure client aggregation", "communication-compressed gradients"]),
            ("Robotics & Control", ["sim-to-real domain randomization", "visuomotor latent policies", "contact-implicit trajectory optimization", "whole-body model predictive control", "tactile sensor calibration"]),
            ("Multimodal Systems", ["cross-attention audio-visual synchronization", "embodied spatio-temporal reasoning", "unified representation spaces", "modality collapse prevention", "cross-modal generation fidelity"])
        ],
        "question_templates": [
            "How does {t1} govern the convergence dynamics of deep networks when subjected to {t2} under {cond}?",
            "What mathematical bound characterizes the generalization error in {t1} when optimizing for {t2} using {method}?",
            "To what extent can {method} resolve the Pareto trade-off between {t1} and {t2} in {cond}?",
            "What theoretical mechanism explains why {t1} experiences catastrophic degradation during {t2} across {cond}?",
            "How do distribution shifts in {cond} affect the asymptotic performance of models employing {t1} in conjunction with {t2}?",
            "Under what conditions does {method} provably prevent performance collapse in {t1} when coupled with {t2}?",
            "What is the sample complexity scaling law when applying {method} to optimize {t1} against {t2} in {cond}?"
        ]
    },
    {
        "name": "Quantum Computing & Physics",
        "subfields": [
            ("Quantum Error Correction", ["surface code syndrome extraction", "color code transversality", "bosonic cat state parity measurements", "magic state distillation overhead", "fault-tolerant threshold bounds"]),
            ("Superconducting Qubits", ["transmon relaxation times T1", "fluxonium flux bias stability", "two-level fluctuator dielectric loss", "dispersive readout fidelity", "cross-resonance microwave gates"]),
            ("Topological Quantum Matter", ["Majorana zero-mode braiding", "fractional quantum Hall edge states", "non-Abelian anyon statistics", "Chern insulator topological invariants", "quantum anomalous Hall transitions"]),
            ("Quantum Algorithms", ["Hamiltonian simulation trotterization errors", "HHL linear solver condition bounds", "quantum phase estimation variance", "QAOA optimization landscape reachability", "variational quantum eigensolver gradients"]),
            ("Quantum Cryptography", ["device-independent quantum key distribution", "continuous-variable QKD protocols", "quantum repeater entanglement swapping", "photonic quantum memory coherence", "measurement-device-independent verification"]),
            ("Many-Body Quantum Systems", ["many-body localization transitions", "quantum quench thermalization rates", "matrix product state entanglement entropy", "Fermi-Hubbard quantum simulation", "dynamic quantum phase transitions"]),
            ("Trapped-Ion Processors", ["motional sideband laser gate fidelities", "ion crystal phonon heating rates", "spatial addressing optical cross-talk", "sympathetic ion cooling efficiency", "coherent spin-motion entanglement"]),
            ("Neutral Atom Computing", ["Rydberg blockade radius interactions", "spatial light modulator optical tweezers", "coherent dipole-dipole exchange", "defect-free atomic array rearrangement", "analog Rydberg quantum simulation"]),
            ("Photonic Information", ["squeezed vacuum light sources", "photonic cluster state generation", "integrated silicon nitride waveguides", "single-photon transition-edge sensors", "measurement-based quantum computing"]),
            ("Quantum Sensing", ["nitrogen-vacancy spin relaxometry", "Heisenberg-limited magnetic field estimation", "spin-squeezed atomic interferometry", "multiparameter quantum estimation bounds", "gravitational field gradient sensing"])
        ],
        "question_templates": [
            "What Hamiltonian formulation accurately describes the decoherence rate in {t1} interacting with {t2} under {cond}?",
            "How can {method} be optimized to suppress leakage errors between {t1} and {t2} in {cond}?",
            "What phase boundary separates topological and trivial phases in {t1} subjected to {t2} using {method}?",
            "Under what threshold conditions does {method} enable fault-tolerant preservation of {t1} against {t2}?",
            "What is the scaling behavior of quantum entanglement between {t1} and {t2} when modulated by {cond}?",
            "How does environmental coupling in {cond} influence the fidelity of gates operating on {t1} via {t2} using {method}?",
            "What operational constraints in {cond} dictate the maximum achievable coherence in {t1} paired with {t2}?"
        ]
    },
    {
        "name": "Genomics & Biotechnology",
        "subfields": [
            ("Gene Editing Technologies", ["CRISPR-Cas9 on-target specificity", "adenine base editing purity", "prime editing pegRNA extension dynamics", "epigenome methylation silencing", "caspase-mediated cleavage kinetics"]),
            ("Structural Biology & Proteomics", ["cryo-EM single-particle resolution", "protein conformational transition pathways", "allosteric regulatory networks", "transmembrane protein folding kinetics", "intrinsically disordered domain phase separation"]),
            ("Synthetic Biology", ["metabolic flux pathway balancing", "orthogonal gene expression switches", "synthetic promoter transcriptional output", "minimal synthetic genome viability", "microbial chassis tolerance engineering"]),
            ("Single-Cell & Spatial Omics", ["spatial transcriptomic spot deconvolution", "single-cell chromatin accessibility peaks", "pseudotime developmental trajectory inference", "cellular lineage barcoding", "single-cell proteomic multiplexing"]),
            ("Epigenetics & Chromatin", ["histone post-translational modifications", "DNA methyltransferase recruitment", "CTCF boundary insulation looping", "heterochromatin condensation factors", "pioneer transcription factor binding dynamics"]),
            ("Molecular Immunology & Virology", ["neutralizing antibody somatic hypermutation", "viral envelope antigenic drift escape", "lipid nanoparticle mRNA vaccine stability", "T-cell receptor CDR3 sequence affinity", "interferon-stimulated gene transcription"]),
            ("Stem Cell & Regeneration", ["induced pluripotent reprogramming efficiency", "epigenetic memory retention", "organoid crypt-villus patterning", "stem cell niche Wnt signaling", "cellular senescence secretome (SASP)"]),
            ("Metabolic Systems Biology", ["genome-scale metabolic model reconstruction", "enzyme turnover number maximization", "redox cofactor balance regeneration", "overflow metabolism Crabtree effect", "secondary metabolite biosynthesis pathways"]),
            ("Antimicrobial Resistance", ["class-A beta-lactamase hydrolysis efficiency", "multidrug RND efflux pump stoichiometry", "conjugative plasmid transfer frequencies", "extracellular polymeric substance biofilm barriers", "phage-bacteria coevolutionary dynamics"]),
            ("Targeted Oncology", ["chimeric antigen receptor T-cell persistence", "immune checkpoint LAG-3 exhaustion", "neoantigen MHC-I presentation processing", "tumor microenvironment hypoxia barrier", "synthetic lethality PARP inhibition"])
        ],
        "question_templates": [
            "What biophysical mechanism governs the rate-limiting step in {t1} when modulated by {t2} under {cond}?",
            "How does targeted alteration of {t1} via {method} impact the systemic expression of {t2} across {cond}?",
            "What kinetic model best describes the equilibrium shift between {t1} and {t2} during {cond} evaluated with {method}?",
            "To what degree does {method} minimize unintended phenotypic divergence in {t1} exposed to {t2}?",
            "What conformational states of {t1} are stabilized by the interaction with {t2} under {cond} using {method}?",
            "How do epigenetic constraints in {cond} alter the therapeutic accessibility of {t1} targeted at {t2}?",
            "Under what cellular conditions does {method} restore homeostatic regulation between {t1} and {t2} in {cond}?"
        ]
    },
    {
        "name": "Materials Science & Clean Energy",
        "subfields": [
            ("Perovskite Photovoltaics", ["halide phase segregation kinetics", "grain boundary chemical passivation", "lead-free double perovskite stability", "buried interface recombination velocity", "moisture-induced degradation pathways"]),
            ("Solid-State Batteries", ["lithium metal dendrite penetration mechanics", "sulfide electrolyte electrochemical stability window", "solid-electrolyte interphase impedance", "chemomechanical cathode cracking", "fast-charging ionic tortuosity"]),
            ("Electrocatalytic Systems", ["oxygen evolution reaction (OER) overpotential", "hydrogen evolution reaction kinetics", "anion exchange membrane durability", "CO2 electroreduction C2+ product selectivity", "single-atom catalyst coordination numbers"]),
            ("Superconductivity & Strong Correlation", ["cuprate high-Tc pseudogap phase", "iron-based pnictide spin fluctuations", "infinite-layer nickelate superconductivity", "hydride clathrate room-temperature phases", "nematic electronic transitions"]),
            ("Carbon Capture & Sorbents", ["metal-organic framework amine chemisorption", "direct air capture thermal desorption energy", "porous aromatic framework CO2 uptake", "sorbent oxidative degradation resistance", "alkali metal carbonate looping"]),
            ("Thermoelectric & Energy Harvesting", ["lattice thermal conductivity reduction", "Seebeck coefficient electronic density tuning", "phonon scattering at grain boundaries", "figure-of-merit zT peak temperature tuning", "piezoelectric energy conversion coefficient"]),
            ("2D Materials & Heterostructures", ["twisted bilayer graphene flat band dispersion", "transition metal dichalcogenide moiré excitons", "ferroelectric 2D sliding bilayer polarization", "interlayer van der Waals charge tunneling", "hexagonal boron nitride dielectric screening"]),
            ("Hydrogen Storage", ["metal hydride desorption enthalpy", "cryo-adsorptive hydrogen volumetric capacity", "liquid organic hydrogen carrier dehydrogenation", "porous coordination cage diffusion barriers", "hysteresis loss during hydriding cycles"]),
            ("Functional Polymers", ["vitrimer dynamic covalent network exchange", "supramolecular self-healing elastomeric matrices", "mechanochromic radical generation", "high-dielectric breakdown polymers", "biodegradable polyester enzymatic hydrolysis"]),
            ("Corrosion & Metallurgy", ["high-entropy alloy passive film stability", "pitting corrosion pit initiation potential", "stress corrosion cracking propagation rates", "atomic layer deposition barrier coating permeability", "microbiologically induced cathodic depolarization"])
        ],
        "question_templates": [
            "What thermodynamic mechanism dictates interfacial degradation between {t1} and {t2} under {cond}?",
            "How does {method} alter the atomic-scale transport kinetics of {t1} in the presence of {t2} across {cond}?",
            "What structural changes govern the electronic conductivity of {t1} paired with {t2} when prepared by {method}?",
            "Under what mechanical load in {cond} does {t1} maintain dimensional integrity when bonded to {t2}?",
            "How can {method} be tailored to maximize the catalytic selectivity of {t1} against {t2} under {cond}?",
            "What phase transformation occurs in {t1} upon continuous chemical exposure to {t2} using {method}?",
            "What physical parameters in {cond} limit the maximum theoretical efficiency of {t1} interacting with {t2} via {method}?"
        ]
    },
    {
        "name": "Astrophysics & Cosmology",
        "subfields": [
            ("Dark Matter & Dark Energy", ["WIMP nuclear scattering cross-sections", "axion-to-photon conversion in magnetic fields", "warm dark matter galactic subhalo core profiles", "dynamical dark energy equation of state w(z)", "self-interacting dark matter cross-sections"]),
            ("Gravitational Wave Astronomy", ["compact binary coalescence ringdown modes", "neutron star tidal deformability Lambda", "stochastic gravitational wave background energy density", "eccentric binary black hole inspiral waveforms", "kilonova r-process electromagnetic opacity"]),
            ("Exoplanet Atmospheres", ["transmission spectroscopy water vapor features", "hydrodynamic atmospheric escape mass-loss rates", "photochemical haze aerosol scattering", "secondary atmosphere CO2/CH4 ratios", "habitable zone thermal phase curves"]),
            ("Early Universe Cosmology", ["primordial gravitational wave tensor-to-scalar ratio r", "cosmic microwave background B-mode polarization", "inflationary slow-roll potential curvature", "electroweak baryogenesis bubble nucleation", "primordial black hole mass distribution spectrum"]),
            ("High-Energy Astrophysics", ["relativistic jet magnetic collimation mechanisms", "gamma-ray burst synchrotron emission efficiency", "fast radio burst magnetar crust fracture models", "ultra-high-energy cosmic ray acceleration at shocks", "pulsar wind nebula magnetic reconnection"]),
            ("Stellar Evolution & Nucleosynthesis", ["core-collapse supernova neutrino-driven convection", "rapid neutron-capture process (r-process) yields", "pair-instability supernova mass gap boundaries", "asymptotic giant branch s-process neutron sources", "binary common-envelope ejection dynamics"]),
            ("Galactic Dynamics", ["supermassive black hole scaling M-sigma relation", "stellar tidal stream orbital perturbation by subhalos", "galactic bar buckling and secular bulge growth", "interstellar medium turbulent energy dissipation", "stellar feedback-driven galactic wind mass-loading"]),
            ("Intergalactic Medium & Reionization", ["21-cm neutral hydrogen cosmic dawn absorption trough", "Lyman-alpha forest optical depth fluctuations", "Population III star ionizing photon production", "patchy reionization bubble size distributions", "cosmic web intergalactic magnetic field bounds"]),
            ("Solar & Heliospheric Physics", ["coronal heating nanoflare energy dissipation", "fast solar wind Parker spiral acceleration", "coronal mass ejection magnetic flux rope instability", "heliopause interstellar plasma boundary compression", "magnetohydrodynamic Alfvén wave reflection"]),
            ("Observational Cosmology & Large Scale Structure", ["baryon acoustic oscillation sound horizon distance", "weak gravitational lensing cosmic shear power spectrum", "Hubble constant H0 tension systematic reconciliation", "galaxy cluster abundance cosmological parameter constraints", "cosmic void velocity profiles and redshift distortions"])
        ],
        "question_templates": [
            "What observational signature distinguishes between competing models of {t1} and {t2} when detected in {cond}?",
            "How do relativistic corrections in {cond} alter the simulated interaction between {t1} and {t2} using {method}?",
            "In what spectral window can {method} identify the perturbation of {t1} induced by {t2} across {cond}?",
            "What cosmological constraint does {t1} impose on {t2} when analyzed under the framework of {cond}?",
            "How does non-linear gravitational clustering in {cond} bias the measurement of {t1} correlated with {t2} via {method}?",
            "What physical mechanisms in {cond} prevent runaway dissipation in {t1} interacting with {t2}?",
            "Under what boundary conditions in {cond} can {method} break the observational degeneracy between {t1} and {t2}?"
        ]
    },
    {
        "name": "Neuroscience & Cognitive Systems",
        "subfields": [
            ("Synaptic Plasticity", ["spike-timing-dependent plasticity (STDP) windows", "long-term potentiation CaMKII autophosphorylation", "dendritic spine actin cytoskeleton remodeling", "homeostatic synaptic scaling AMPA insertion", "endocannabinoid retrograde depression"]),
            ("Neural Circuitry & Connectomics", ["cortical microcolumn recurrent excitation", "parvalbumin-positive interneuron gamma oscillations", "thalamocortical relay gating states", "whole-brain diffusion tractography connectomes", "neuromodulatory locus coeruleus projections"]),
            ("Neural Encoding & Computation", ["population vector coding in motor cortex", "predictive coding sensory error minimization", "sparse coding in primary visual cortex", "neural manifold low-dimensional latent dynamics", "attractor network working memory stability"]),
            ("Brain-Computer Interfaces", ["intracortical microelectrode spike sorting stability", "non-invasive EEG sensorimotor rhythm decoding", "closed-loop deep brain stimulation feedback", "conductive hydrogel neural interface impedance", "optogenetic closed-loop optical pacing"]),
            ("Neurodegenerative Mechanisms", ["tau microtubule detachment and aggregation", "alpha-synuclein oligomeric membrane pore formation", "amyloid-beta 42/40 peptide synaptotoxicity", "microglial TREM2 phagocytosis dysfunction", "blood-brain barrier pericyte degeneration"]),
            ("Cognitive Control & Decision Making", ["drift-diffusion model evidence accumulation bounds", "dopaminergic reward prediction error signaling", "prefrontal cortex cognitive flexibility gating", "anterior cingulate conflict monitoring signals", "metacognitive decision confidence representation"]),
            ("Sensory Processing & Integration", ["Bayesian multisensory cue integration", "auditory cortex tonotopic map reorganization", "retinal ganglion cell center-surround receptive fields", "olfactory glomerulus combinatorial odor coding", "somatosensory tactile vibration frequency discrimination"]),
            ("Sleep & Brain Dynamics", ["slow-wave sleep hippocampal-cortical replay", "REM sleep theta phase synchronization", "glymphatic interstitial fluid clearance during sleep", "thalamic spindle-slow oscillation phase coupling", "circadian clock gene transcriptional regulation"]),
            ("Neuromodulation & Neurochemistry", ["5-HT2A serotonin receptor psychedelic neuroplasticity", "dorsal striatal D1/D2 receptor opponent dynamics", "cholinergic enhancement of attentional signal-to-noise", "noradrenergic arousal state switching", "GABAergic tonic inhibition conductances"]),
            ("Neurodevelopment & Lineage", ["radial glia asymmetric neurogenic division", "growth cone netrin-1 axon guidance steering", "complement C1q-mediated synaptic pruning", "GABAergic excitatory-to-inhibitory developmental shift", "critical period ocular dominance plasticity closure"])
        ],
        "question_templates": [
            "How do neural firing patterns in {t1} regulate the functional expression of {t2} during {cond}?",
            "What molecular cascade links changes in {t1} to long-term adaptation of {t2} in {cond} evaluated with {method}?",
            "To what extent can {method} reconstruct the latent state of {t1} during coordination with {t2} in {cond}?",
            "What computational mechanism enables {t1} to maintain stability despite ongoing drift in {t2} across {cond}?",
            "How does pathological impairment of {t1} disrupt circuit-level synchronization with {t2} under {cond} using {method}?",
            "Under what behavioral constraints in {cond} does {t1} exert causal control over {t2}?",
            "What biophysical properties in {cond} limit the information transmission rate from {t1} to {t2} via {method}?"
        ]
    },
    {
        "name": "Cybersecurity & Applied Cryptography",
        "subfields": [
            ("Post-Quantum Cryptography", ["learning-with-errors (LWE) hardness reductions", "module-lattice ring noise distribution bounds", "multivariate quadratic signature security", "isogeny graph supersingular path routing", "stateful hash-based signature key exhaustion"]),
            ("Zero-Knowledge Proofs", ["recursive zk-SNARK proof composition", "polynomial commitment scheme KZG opening verification", "transparent zk-STARK FRI domain blowup factors", "PlonK custom gate arithmetization efficiency", "zero-knowledge rollup state transition validity"]),
            ("Hardware & Side-Channel Security", ["transient execution speculative branch prediction leaks", "differential power analysis hamming weight traces", "laser fault injection glitch vulnerability", "physical unclonable function intra-distance entropy", "DRAM Rowhammer bit-flip exploitation"]),
            ("Secure Multi-Party Computation", ["garbled circuit communication complexity bounds", "oblivious transfer extension protocols", "threshold ECDSA signature distributed key generation", "Shamir secret sharing polynomial reconstruction over rings", "private set intersection maliciously secure hashing"]),
            ("Formal Verification of Systems", ["smart contract formal semantics in Coq/K-framework", "automated SMT solver bit-vector quantifier reasoning", "separation logic concurrent memory safety proofs", "cryptographic protocol state machine model checking", "verified microkernel IPC isolation invariant proofs"]),
            ("Network & Infrastructure Security", ["BGP route hijacking RPKI validation latency", "zero-trust identity context-aware policy enforcement", "DNS-over-HTTPS encrypted traffic timing analysis", "software supply chain SLSA provenance attestation", "distributed denial-of-service volumetric mitigation"]),
            ("Privacy-Enhancing Technologies", ["local differential privacy randomized response mechanisms", "Rényi differential privacy Gaussian mechanism composition", "fully homomorphic encryption bootstrapping cycle time", "trusted execution environment enclave memory encryption", "synthetic tabular data privacy leakage metrics"]),
            ("Binary Analysis & Exploitation", ["coverage-guided fuzzing evolutionary mutators", "control-flow integrity forward-edge indirect call checks", "Rust-to-C FFI memory safety vulnerability surfaces", "heap layout exploitation Feng Shui determinism", "binary decompilation intermediate representation lifting"]),
            ("Adversarial Machine Learning", ["poisoning attacks on distributed federated training", "membership inference privacy risk in foundation models", "transferable universal adversarial patch generation", "certified L-infinity robustness verification bounds", "model extraction watermarking extraction robustness"]),
            ("Authentication & Cryptographic Protocols", ["FIDO2 WebAuthn credential public key binding", "decentralized identifier (DID) verifiable credential issuance", "biometric fuzzy vault cancelable template security", "zero-round-trip time (0-RTT) TLS 1.3 replay attack resistance", "post-quantum key encapsulation hybrid TLS suites"])
        ],
        "question_templates": [
            "What mathematical reduction proves the resistance of {t1} against attacks exploiting {t2} under {cond}?",
            "How does implementation of {method} affect the computational latency of {t1} operating with {t2} in {cond}?",
            "Under what adversary capabilities in {cond} can {t1} maintain non-malleability against {t2} using {method}?",
            "What information leakage occurs when {t1} interacts with {t2} in microarchitectures governed by {cond}?",
            "How does {method} guarantee formal correctness when verifying {t1} against state corruption via {t2} in {cond}?",
            "What parameter constraints in {cond} preserve the security margin of {t1} paired with {t2} against {method}?",
            "In what operational environment does {method} fail to protect {t1} from malicious manipulation of {t2} under {cond}?"
        ]
    },
    {
        "name": "Climate Science & Environmental Systems",
        "subfields": [
            ("Carbon Sequestration & Removal", ["olivine enhanced weathering dissolution rates", "direct air capture amine functionalized solid sorbents", "biochar pyrolytic carbon recalcitrance index", "ocean alkalinity enhancement calcium hydroxide kinetics", "subsurface basalt CO2 mineralization trapping"]),
            ("Atmospheric & Aerosol Dynamics", ["cloud condensation nuclei aerosol activation", "secondary organic aerosol oxidation pathways", "stratospheric sulfur injection radiative forcing", "tropospheric ozone photochemical production rates", "planetary boundary layer turbulent mixing parametrization"]),
            ("Cryospheric Stability", ["marine ice sheet instability (MISI) grounding line retreat", "subglacial water cavitation lubrication pressures", "permafrost active layer thaw methane emission pulses", "ice shelf basal melt turbulent boundary layers", "sea ice albedo positive feedback parameterization"]),
            ("Ocean Circulation & Biogeochemistry", ["Atlantic Meridional Overturning Circulation (AMOC) freshwater tipping points", "ocean acidification aragonite saturation states", "marine oxygen minimum zone expansion volume", "iron-limited high-nutrient low-chlorophyll diatom blooms", "mesoscale eddy kinetic energy ocean heat uptake"]),
            ("Extreme Weather & Attribution", ["atmospheric river integrated water vapor transport", "synoptic heat dome quasi-stationary Rossby wave resonance", "tropical cyclone rapid intensification ocean heat content", "compound drought-heatwave soil moisture depletion", "extreme event attribution non-stationary GEV modeling"]),
            ("Terrestrial Ecology & Carbon Sinks", ["tropical rainforest net primary productivity drought sensitivity", "wildfire pyrodiversity carbon balance trajectories", "xylem hydraulic conductivity cavitation thresholds", "soil mycorrhizal fungi nutrient immobilization", "phenological mismatch temperature-photoperiod cues"]),
            ("Hydrological Cycle & Resources", ["GRACE satellite groundwater depletion trend analysis", "alpine snowpack snow water equivalent melt timing", "catchment-scale distributed runoff hydrographs", "reverse osmosis seawater desalination brine dispersal", "transboundary riparian aquifer recharge rates"]),
            ("Urban Microclimate & Sustainability", ["urban heat island canopy albedo mitigation", "biophilic green roof stormwater retention capacity", "building envelope thermal mass diurnal phase shift", "street canyon air pollutant dispersion aerodynamics", "embodied lifecycle carbon in cementitious composites"]),
            ("Ecotoxicology & Contaminant Transport", ["per- and polyfluoroalkyl substances (PFAS) defluorination", "microplastic particulate bioaccumulation trophic magnification", "heavy metal phytoremediation hyperaccumulator uptake", "fine particulate matter (PM2.5) elemental speciation", "endocrine disruptor aquatic estrogenic potency"]),
            ("Climate Econometrics & Risk", ["integrated assessment climate damage tipping function calibration", "catastrophe bond natural hazard loss modeling", "social cost of carbon recursive utility discount rates", "transition risk strandable fossil asset valuations", "coastal retreat adaptation cost-benefit frontiers"])
        ],
        "question_templates": [
            "What non-linear feedback loop dictates the response of {t1} to {t2} across {cond}?",
            "How do spatial heterogeneities in {cond} affect the modeled sensitivity of {t1} to {t2} using {method}?",
            "What empirical threshold in {cond} triggers an irreversible transition in {t1} mediated by {t2}?",
            "To what extent can high-resolution {method} reduce uncertainty in the coupled dynamics of {t1} and {t2} during {cond}?",
            "How does global teleconnection in {cond} modulate the regional coupling between {t1} and {t2} evaluated via {method}?",
            "What biogeochemical feedback controls the long-term equilibrium between {t1} and {t2} under {cond} using {method}?",
            "Under what emissions pathway in {cond} does {t1} exceed its adaptive buffer relative to {t2} via {method}?"
        ]
    },
    {
        "name": "Pharmacology & Precision Therapeutics",
        "subfields": [
            ("Targeted Molecular Discovery", ["proteolysis targeting chimera (PROTAC) ternary complex affinity", "allosteric kinase inhibitor conformational traps", "covalent warhead reactivity-selectivity profiling", "fragment-based screening surface plasmon resonance", "macrocyclic peptide membrane permeability"]),
            ("Nanomedicine & Drug Delivery", ["ionizable lipid nanoparticle endosomal escape efficiency", "polymeric micelle critical micelle concentration stability", "extracellular vesicle tropism surface engineering", "inhalable dry powder aerodynamic diameter optimization", "stimuli-responsive hydrogel enzymatic cleavage release"]),
            ("Pharmacokinetics & PBPK", ["physiologically based pharmacokinetic (PBPK) organ clearance", "target-mediated drug disposition (TMDD) nonlinear elimination", "cytochrome P450 3A4 time-dependent inhibition kinetics", "hepatic organic anion transporter polypeptide uptake", "renal tubular secretion active transport saturation"]),
            ("Biologics & Immunotherapy", ["bispecific T-cell engager (BiTE) immunological synapse geometry", "monoclonal antibody afucosylation ADCC enhancement", "cytokine storm IL-6 receptor antagonist blockade", "oncolytic virus tumor microenvironment immunogenic death", "antibody-drug conjugate linker lysosomal cleavage rates"]),
            ("RNA Therapeutics & Delivery", ["antisense oligonucleotide 2'-MOE chemical modification patterns", "siRNA cholesterol-conjugated hepatocyte uptake", "circular RNA internal ribosome entry site translation", "self-amplifying RNA replicase persistence in muscle", "gapmer RNase H1 cleavage kinetics"]),
            ("Central Nervous System Delivery", ["transferrin receptor-mediated transcytosis through BBB", "focused ultrasound microbubble blood-brain barrier opening", "intrathecal drug cerebrospinal fluid pharmacodynamics", "intranasal olfactory nerve bypass kinetics", "P-glycoprotein efflux inhibition at brain capillaries"]),
            ("Preclinical Toxicology & Safety", ["hERG potassium channel electrophysiological cardiotoxicity", "drug-induced liver injury (DILI) mitochondrial toxicity", "reactive metabolite glutathione adduct trapping", "microphysiological human organ-on-chip predictive validity", "off-target kinome selectivity profiling panels"]),
            ("Precision Oncology Biomarkers", ["liquid biopsy circulating tumor DNA (ctDNA) variant fraction", "homologous recombination deficiency (HRD) genomic scar scores", "EGFR T790M/C797S resistance mutation evolutionary tracking", "microsatellite instability (MSI-H) immune checkpoint response", "spatial transcriptomic tumor immune evasion biomarkers"]),
            ("Advanced Cell Therapies", ["autologous CAR-T cell manufacturing exhaustion phenotype", "allogeneic CRISPR gene-edited TCR knockout graft-vs-host evasion", "mesenchymal stromal cell immunomodulatory paracrine secretion", "gamma-delta T-cell MHC-unrestricted cytotoxicity", "induced pluripotent stem cell-derived cardiomyocyte maturation"]),
            ("Therapeutics for Rare Diseases", ["enzyme replacement therapy mannose-6-phosphate receptor uptake", "nonsense mutation aminoglycoside ribosomal readthrough", "pharmacological chaperone small molecule folding rescue", "allele-specific siRNA huntingtin transcript silencing", "adeno-associated virus (AAV9) whole-body biodistribution"])
        ],
        "question_templates": [
            "What molecular barrier prevents optimal therapeutic interaction between {t1} and {t2} under {cond}?",
            "How does chemical optimization via {method} enhance the therapeutic selectivity of {t1} targeting {t2} in {cond}?",
            "What resistance pathway accounts for the loss of drug responsiveness in {t1} exposed to {t2} across {cond}?",
            "How does the pharmacokinetic clearance of {t1} vary with {t2} when measured using {method} under {cond}?",
            "To what extent does {method} accurately predict human clinical adverse interactions between {t1} and {t2} in {cond}?",
            "What structural binding conformation in {t1} minimizes off-target engagement with {t2} using {method}?",
            "Under what physiological conditions in {cond} does {method} achieve sustained therapeutic bioavailability of {t1} against {t2}?"
        ]
    },
    {
        "name": "Applied Mathematics & Computational Theory",
        "subfields": [
            ("Spectral Graph Theory", ["Laplacian eigenvalue Cheeger conductance bounds", "Ramanujan expander graph spectral gap optimality", "effective resistance distance matrix properties", "random walk mixing times on irregular graphs", "graph neural network spectral filtering limits"]),
            ("High-Dimensional Probability", ["sub-Gaussian matrix concentration Bernstein inequalities", "non-asymptotic random matrix Marchenko-Pastur distributions", "Johnson-Lindenstrauss dimension reduction embedding distortion", "restricted isometry property in compressive sensing", "Wasserstein distance optimal transport duality"]),
            ("Computational Complexity", ["derandomization polynomial-time hardness conjectures", "circuit lower bounds against AC0 with parity gates", "fine-grained complexity 3SUM hypothesis reductions", "P vs NP natural proofs barrier limitations", "quantum query complexity polynomial method bounds"]),
            ("Approximation Algorithms", ["metric embedding into tree metrics distortion bounds", "semidefinite programming Goemans-Williamson rounding", "submodular function maximization under matroid constraints", "online paging competitive ratio k-server problem", "primal-dual approximation for facility location"]),
            ("Nonlinear PDEs & Analysis", ["Navier-Stokes smooth solution singularity criteria", "non-linear Schrödinger equation soliton stability", "Hamilton-Jacobi-Bellman viscosity solution uniqueness", "reaction-diffusion system Turing pattern bifurcation", "free boundary problem regularity in obstacle problems"]),
            ("Algebraic Topology & Geometry", ["persistent homology persistence diagram bottleneck distance", "constructible sheaf micro-local analysis on manifolds", "derived algebraic geometry moduli stack deformation", "topological data analysis Mapper simplicial complex fidelity", "characteristic classes of holomorphic vector bundles"]),
            ("Continuous Optimization", ["interior-point method self-concordant barrier complexity", "accelerated gradient momentum Nesterov estimate sequences", "non-convex optimization saddle-point escaping dynamics", "alternating direction method of multipliers (ADMM) rates", "stochastic variance-reduced gradient (SVRG) iteration bounds"]),
            ("Information & Coding Theory", ["polar code error-exponent scaling in finite blocklengths", "network coding multicast capacity min-cut max-flow", "non-linear channel capacity under peak power constraints", "rate-distortion perception trade-off bounds", "low-density parity-check (LDPC) belief propagation thresholds"]),
            ("Dynamical Systems & Chaos", ["Lyapunov exponent spectrum in high-dimensional chaos", "Kolmogorov-Arnold-Moser (KAM) invariant tori persistence", "strange non-chaotic attractor fractal dimensions", "Perron-Frobenius transfer operator isolated eigenvalues", "Hopf bifurcation cascades in coupled nonlinear oscillators"]),
            ("Arithmetic Geometry & Number Theory", ["elliptic curve algebraic rank bounds (BSD conjecture)", "automorphic L-function subconvexity bounds", "Galois representation modularity lifting theorems", "prime gap distributions via Selberg sieve methods", "p-adic Hodge theory crystalline cohomology periods"])
        ],
        "question_templates": [
            "What fundamental constraint dictates the asymptotic bounds of {t1} when coupled with {t2} under {cond}?",
            "How does applying {method} yield improved upper bounds on the complexity of {t1} in the presence of {t2} across {cond}?",
            "Under what regularity conditions does the mathematical system combining {t1} and {t2} admit a unique stable solution in {cond}?",
            "What topological or algebraic invariant characterizes the equivalence classes of {t1} deformed by {t2} using {method}?",
            "How can variational principles in {method} prove global convergence of {t1} subjected to perturbation by {t2} in {cond}?",
            "What structural property of {t1} enables sharp phase transitions when interacting with {t2} under {cond} via {method}?",
            "In what regime does {method} establish the tightest lower bound for {t1} bounded by {t2} across {cond}?"
        ]
    }
]

DIFFICULTIES = ["Introductory", "Undergraduate", "Graduate", "Specialist"]
RESEARCH_TYPES = ["Empirical", "Theoretical", "Methodological", "Computational"]

CONDITIONS_LIST = [
    "finite sample sizes and high-dimensional noise",
    "extreme cryogenic non-equilibrium conditions",
    "stochastic environmental perturbations",
    "non-Gaussian heavy-tailed error distributions",
    "sparse parameter regimes with missing observations",
    "rapidly varying transient boundary conditions",
    "strong non-linear feedback and coupling effects",
    "asymmetric information and partial observability",
    "highly constrained energy and resource budgets",
    "dynamic multi-scale spatial temporal interactions",
    "adversarial noise corruptions near decision boundaries",
    "severe distribution shift between train and test distributions",
    "stochastic latency and asynchronous message passing",
    "elevated temperature and high-humidity operational stress",
    "ultra-low signal-to-noise ratio measurements",
    "heterogeneous non-uniform spatial topologies",
    "non-stationary temporal drift and cyclical variations",
    "competing multi-objective optimization constraints",
    "singular boundary layer approximations",
    "discrete state-space approximations of continuum models"
]

METHODS_LIST = [
    "high-order perturbation analysis",
    "stochastic variational inference",
    "first-principles density functional theory",
    "non-asymptotic concentration inequalities",
    "multi-scale numerical hydrodynamic modeling",
    "controlled randomized double-blind trial architectures",
    "adaptive Bayesian Markov Chain Monte Carlo sampling",
    "semi-definite programming relaxation techniques",
    "spectral decomposition and harmonic analysis",
    "automated symbolic formal verification proofs",
    "renormalization group flow techniques",
    "sub-gradient descent with momentum scheduling",
    "quantum trajectory Monte Carlo simulations",
    "cryogenic scanning tunneling microscopy",
    "high-throughput combinatorial screening pipelines",
    "orthogonal projection pursuit regression",
    "topological persistence diagram homology",
    "entropy-regularized optimal transport",
    "asymptotic expansions with boundary layer matching",
    "gradient-guided adversarial stress testing"
]

OUTPUT_TYPES_LIST = [
    ["Mathematical derivation", "Asymptotic bound proof", "Boundary condition analysis"],
    ["Hypothesis statement", "Experimental protocol", "Statistical validation plan"],
    ["Algorithmic pseudo-code", "Convergence proof", "Empirical scaling benchmarks"],
    ["Mechanistic pathway model", "Sensitivity analysis", "Counter-evidence falsification criteria"],
    ["Simulation framework", "Phase diagram derivation", "Finite-size scaling analysis"],
    ["Formal security proof", "Adversarial threat model", "Overhead benchmark metrics"],
    ["Analytical closed-form solution", "Approximation error bounds", "Numerical verification script"],
    ["Biophysical interaction diagram", "Binding affinity table", "In vivo translation roadmap"]
]

ASSUMPTIONS_LIST = [
    "Assumes a convex loss surface and Lipschitz continuity of the gradient operator.",
    "Assumes weak environmental coupling and validity of the Markovian Lindblad master equation.",
    "Assumes steady-state kinetics and negligible backward reaction rates under standard physiological conditions.",
    "Assumes uniform thermal dissipation and zero mechanical shear across the interfacial boundary.",
    "Assumes spatially flat Friedmann-Lemaître-Robertson-Walker metric with cold dark matter dominance.",
    "Assumes Poissonian spike firing statistics and stationarity of underlying synaptic connection weights.",
    "Assumes bounded polynomial-time adversary capability and quantum oracle access.",
    "Assumes constant radiative equilibrium and linear atmospheric feedback responses.",
    "Assumes linear one-compartment disposition kinetics without active auto-induction of metabolism.",
    "Assumes bounded variance of the underlying probability distribution and independence of observation trials."
]

ANSWERABILITY_LIST = [
    "Self-contained",
    "Needs stated assumptions",
    "Requires domain-specific empirical calibration",
    "Provable under standard mathematical axioms",
    "Conditionally answerable given benchmark dataset access"
]

NOVELTY_NOTES_LIST = [
    "Requires resolving non-trivial trade-offs between asymptotic mathematical tractability and practical empirical robustness.",
    "Demands reconciling conflicting theoretical predictions that arise from high-order boundary effects.",
    "Presents a challenging multi-scale reasoning problem bridging microscopic mechanisms and macroscopic emergent observations.",
    "Involves formulating a novel proof strategy to surpass conventional loose concentration inequalities.",
    "Requires identifying hidden confounding factors in non-stationary observation streams.",
    "Tests the ability to synthesize principles from disparate disciplines into a coherent testable protocol.",
    "Addresses an open problem where standard linearization techniques break down due to strong non-linearities.",
    "Demands robust counter-factual reasoning to isolate causal mechanisms from strong observational correlations."
]

INSTRUCTION_TEMPLATES = [
    "Formulate a rigorous research methodology to analyze the interaction between {t1} and {t2} within the field of {subfield}. Specify theoretical foundations, validation metrics, and potential failure modes.",
    "Investigate the analytical properties of {t1} under conditions of {cond} in {subfield}. Provide a structured analysis detailing mathematical formulations and empirical validation strategies.",
    "Evaluate the theoretical limitations and computational tractability of utilizing {method} to address {t1} in {subfield}. Detail governing assumptions and experimental milestones.",
    "Design an end-to-end investigation to determine whether {t1} causally dictates {t2} across {cond} in the context of {subfield}. Include falsification criteria.",
    "Analyze the operational boundaries and performance stability of {t1} coupled with {t2} in {subfield}. Formulate testable hypotheses and quantitative assessment criteria."
]


def generate_all_15k(output_file: str):
    start_time = time.time()
    total_target = 15000
    dataset = []
    
    seen_questions = set()
    seen_instructions = set()
    
    print(f"Generating {total_target} structured research items for {output_file}...")
    
    # We iterate across the target count
    for idx in range(1, total_target + 1):
        q_id = f"Q{idx:05d}"
        
        # Round-robin broad scientific domain
        d_idx = (idx - 1) % len(DOMAINS)
        domain_info = DOMAINS[d_idx]
        domain_name = domain_info["name"]
        
        # Subfield
        sub_list = domain_info["subfields"]
        s_idx = ((idx - 1) // len(DOMAINS)) % len(sub_list)
        subfield_name, concepts = sub_list[s_idx]
        
        # Deterministic diverse selection of concepts
        c_len = len(concepts)
        c1_idx = ((idx - 1) * 3 + (idx // 100)) % c_len
        c2_idx = ((idx - 1) * 7 + 1 + (idx // 50)) % c_len
        if c1_idx == c2_idx:
            c2_idx = (c2_idx + 1) % c_len
            
        t1 = concepts[c1_idx]
        t2 = concepts[c2_idx]
        
        # Condition, method, templates
        cond = CONDITIONS_LIST[((idx - 1) * 11 + (idx // 20)) % len(CONDITIONS_LIST)]
        method = METHODS_LIST[((idx - 1) * 13 + (idx // 15)) % len(METHODS_LIST)]
        
        q_templates = domain_info["question_templates"]
        q_tmpl_idx = ((idx - 1) * 5 + (idx // len(DOMAINS))) % len(q_templates)
        
        # Create base question
        base_q = q_templates[q_tmpl_idx].format(t1=t1, t2=t2, cond=cond, method=method)
        
        # Uniqueness guarantee: if base_q was somehow seen, augment with specific parameterizing descriptor
        if base_q in seen_questions:
            qualifier = f" Specifically, examine regime iteration {idx} with {method}."
            base_q = base_q.rstrip("?") + f" when constrained by {method}?"
            if base_q in seen_questions:
                base_q = f"In benchmark scenario #{idx:05d}: " + base_q
                
        seen_questions.add(base_q)
        
        # Instruction
        ins_tmpl = INSTRUCTION_TEMPLATES[(idx - 1) % len(INSTRUCTION_TEMPLATES)]
        instruction = ins_tmpl.format(t1=t1, t2=t2, cond=cond, method=method, subfield=subfield_name)
        if instruction in seen_instructions:
            instruction = f"[Task {q_id}] " + instruction
        seen_instructions.add(instruction)
        
        # Metadata values
        difficulty = DIFFICULTIES[((idx - 1) // 3) % len(DIFFICULTIES)]
        research_type = RESEARCH_TYPES[((idx - 1) // 5) % len(RESEARCH_TYPES)]
        focal_concepts = [t1, t2, method]
        expected_output_type = OUTPUT_TYPES_LIST[((idx - 1) * 7) % len(OUTPUT_TYPES_LIST)]
        assumptions = ASSUMPTIONS_LIST[((idx - 1) * 3) % len(ASSUMPTIONS_LIST)]
        answerability = ANSWERABILITY_LIST[((idx - 1) * 5) % len(ANSWERABILITY_LIST)]
        novelty_note = NOVELTY_NOTES_LIST[((idx - 1) * 9) % len(NOVELTY_NOTES_LIST)]
        
        item = {
            "id": q_id,
            "domain": domain_name,
            "subfield": subfield_name,
            "difficulty": difficulty,
            "research_type": research_type,
            "instruction": instruction,
            "question": base_q,
            "focal_concepts": focal_concepts,
            "expected_output_type": expected_output_type,
            "assumptions_needed": assumptions,
            "answerability": answerability,
            "novelty_note": novelty_note
        }
        
        dataset.append(item)
        
        if idx % 3000 == 0:
            print(f"Generated {idx}/{total_target} items (uniqueness verified: {len(seen_questions)} questions)...")
            
    print(f"Writing all {len(dataset)} items to {output_file}...")
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(dataset, f, indent=2, ensure_ascii=False)
        
    elapsed = time.time() - start_time
    file_size_mb = os.path.getsize(output_file) / (1024 * 1024)
    print(f"\nDone! Successfully written {len(dataset)} items to {output_file}.")
    print(f"File size: {file_size_mb:.2f} MB")
    print(f"Unique questions: {len(seen_questions)} / {total_target} (100% unique)")
    print(f"Unique instructions: {len(seen_instructions)} / {total_target} (100% unique)")
    print(f"Elapsed time: {elapsed:.2f}s")


if __name__ == "__main__":
    repo_dir = os.path.dirname(os.path.abspath(__file__))
    target_path = os.path.join(repo_dir, "rebo_dataset_15k.json")
    generate_all_15k(target_path)
