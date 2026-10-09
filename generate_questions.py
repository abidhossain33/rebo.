"""
Asynchronous Generation Script for 15,000 Structured Research Questions.
Generates 15 batch files: data_batch_01.json to data_batch_15.json (1,000 questions each).
Sequential IDs: Q00001 to Q15000.
"""

import asyncio
import json
import os
import random
import sys
import time

DOMAINS_DATA = [
    {
        "domain": "Artificial Intelligence & Machine Learning",
        "subfields": [
            ("Neural Architecture Search", ["weight-sharing supernets", "bilevel optimization", "latency-aware constraints", "hyperparameter tuning", "zero-cost proxies"]),
            ("Reinforcement Learning", ["offline policy evaluation", "sample efficiency", "distribution shift", "curiosity-driven exploration", "multi-agent coordination"]),
            ("Large Language Models", ["chain-of-thought faithfulness", "mechanistic interpretability", "hallucination mitigation", "parameter-efficient fine-tuning", "context window scaling"]),
            ("Computer Vision", ["vision-language grounding", "diffusion prior inversion", "self-supervised representation", "3D Gaussian splatting", "adversarial robustness"]),
            ("AI Safety & Alignment", ["scalable oversight", "reward hacking prevention", "value alignment", "constitutional AI", "red-teaming methodologies"]),
            ("Graph Neural Networks", ["oversmoothing attenuation", "subgraph isomorphisms", "dynamic temporal graphs", "heterogeneous message passing", "spectral graph theory"]),
            ("Quantum Machine Learning", ["parameterized quantum circuits", "barren plateaus mitigation", "quantum kernel methods", "quantum neural networks", "entanglement entropy"]),
            ("Robotics & Control", ["sim-to-real transfer", "visuomotor policy learning", "trajectory optimization", "tactile sensing feedback", "dexterous manipulation"]),
            ("Federated Learning", ["non-IID data distribution", "byzantine fault tolerance", "secure aggregation", "differential privacy budgeting", "client drift correction"]),
            ("Multimodal Reasoning", ["cross-modal attention alignment", "audio-visual synchronization", "embodied reasoning", "unified representation spaces", "contrastive learning"])
        ],
        "question_templates": [
            "How does {topic} affect the convergence behavior of deep models when evaluated under {condition}?",
            "What mathematical framework best models the transition dynamics in {topic} subject to {condition}?",
            "To what extent can {method} resolve the fundamental tradeoff between computational efficiency and accuracy in {topic}?",
            "What are the theoretical limits of sample complexity when applying {method} to {topic} under {condition}?",
            "How do distribution shifts across {condition} influence the generalization performance of systems utilizing {topic}?"
        ]
    },
    {
        "domain": "Quantum Physics & Quantum Computing",
        "subfields": [
            ("Quantum Error Correction", ["surface codes", "color codes", "bosonic cat qubits", "magic state distillation", "fault-tolerant threshold"]),
            ("Superconducting Qubits", ["transmon coherence times", "fluxonium qubits", "dielectric loss mitigation", "dispersive readout", "cross-resonance gates"]),
            ("Topological Quantum Matter", ["Majorana zero modes", "fractional Chern insulators", "anyon braiding statistics", "quantum anomalous Hall effect", "topological order"]),
            ("Quantum Algorithms", ["Hamiltonian simulation", "HHL algorithm", "quantum phase estimation", "quantum annealing", "QAOA optimization landscapes"]),
            ("Quantum Cryptography", ["device-independent QKD", "quantum key distribution protocols", "continuous-variable QKD", "quantum repeater architectures", "quantum memory"]),
            ("Many-Body Quantum Physics", ["many-body localization", "quantum quench dynamics", "tensor network states", "entanglement spectrum", "Fermi-Hubbard model"]),
            ("Trapped-Ion Computing", ["motional mode heating", "laser-induced gate fidelities", "phononic bus architecture", "individual addressing optics", "sympathetic cooling"]),
            ("Neutral Atom Systems", ["Rydberg blockade interactions", "spatial light modulator tweezers", "coherent dipole-dipole exchange", "defect-free array rearrangement", "analog simulation"]),
            ("Photonic Quantum Information", ["squeezed light sources", "photonic cluster states", "linear optical quantum computing", "integrated silicon photonics", "single-photon detectors"]),
            ("Quantum Metrology", ["Heisenberg-limited phase estimation", "spin squeezing", "atomic interferometry", "quantum illumination", "multiparameter quantum sensing"])
        ],
        "question_templates": [
            "What Hamiltonian formulation accurately characterizes the decoherence dynamics in {topic} interacting with {condition}?",
            "How can {method} be optimized to surpass the classical benchmark in {topic} while operating under {condition}?",
            "What phase transitions occur in {topic} when perturbed by {condition} using {method}?",
            "In what regime does {method} enable fault tolerance in {topic} without prohibitive resource overheads?",
            "How does quantum entanglement scaling constrain the fidelity bounds of {topic} under {condition}?"
        ]
    },
    {
        "domain": "Biotechnology & Molecular Genomics",
        "subfields": [
            ("Gene Editing Technologies", ["CRISPR-Cas9 fidelity", "base editing efficiency", "prime editing pegRNA design", "epigenome editing", "off-target cleavage minimization"]),
            ("Structural Biology & Proteomics", ["cryo-EM reconstruction", "protein conformer transitions", "allosteric regulation", "membrane protein folding", "intrinsically disordered proteins"]),
            ("Synthetic Biology", ["metabolic flux balancing", "orthogonal genetic circuits", "synthetic promoter libraries", "minimal synthetic cells", "microbial chassis optimization"]),
            ("Single-Cell & Spatial Genomics", ["spatial transcriptomic deconvolution", "single-cell ATAC-seq", "trajectory inference algorithms", "cellular heterogeneity profiling", "UMI count normalization"]),
            ("Epigenetics & Chromatin Dynamics", ["histone post-translational modifications", "DNA methylation patterning", "chromatin looping via CTCF", "phase separation in heterochromatin", "pioneer transcription factors"]),
            ("Molecular Virology & Immunology", ["neutralizing antibody evolution", "antigenic drift escape mutations", "mRNA vaccine lipid nanoparticle formulations", "T-cell receptor repertoires", "viral capsid assembly"]),
            ("Stem Cell & Regenerative Medicine", ["induced pluripotent stem cell reprogramming", "lineage commitment epigenetics", "organoid self-organization", "niche signaling modulation", "cellular senescence reversal"]),
            ("Metabolic Engineering", ["flux balance analysis", "enzyme turnover maximization", "co-factor regeneration systems", "pathway bottleneck relief", "microbial fermentation yields"]),
            ("Antimicrobial Resistance", ["beta-lactamase enzymatic kinetics", "multidrug efflux pump regulation", "horizontal gene transfer mechanisms", "biofilm matrix degradation", "phage therapy synergy"]),
            ("Targeted Oncology", ["chimeric antigen receptor (CAR) signaling", "checkpoint blockade resistance", "neoantigen prediction pipelines", "tumor microenvironment immunosuppression", "synthetic lethality interactions"])
        ],
        "question_templates": [
            "By what mechanism does {topic} dictate transcription fidelity when mediated by {condition}?",
            "How does targeted modulation via {method} alter the evolutionary trajectory of {topic} under {condition}?",
            "What kinetic parameters govern the binding affinity of {topic} in the presence of {condition}?",
            "Can high-throughput {method} overcome the delivery barriers associated with {topic} in vivo?",
            "What structural conformations in {topic} correlate with enhanced functionality when subjected to {condition}?"
        ]
    },
    {
        "domain": "Materials Science & Clean Energy",
        "subfields": [
            ("Perovskite Photovoltaics", ["halide segregation mitigation", "grain boundary passivation", "lead-free double perovskites", "tandem cell efficiency limits", "moisture stability degradation"]),
            ("Solid-State Batteries", ["lithium dendrite suppression", "sulfide-based solid electrolytes", "solid-electrolyte interphase kinetics", "cathodic chemomechanical stress", "high-nickel cathode stability"]),
            ("Electrocatalytic Water Splitting", ["oxygen evolution reaction (OER) catalysts", "hydrogen evolution reaction kinetics", "anion exchange membrane electrolysis", "bifunctional electrocatalysts", "noble-metal-free catalytic sites"]),
            ("Superconductivity & Quantum Materials", ["cuprate pseudogap origin", "iron-based superconductors", "nickelate superconductivity", "pressure-induced hydride phases", "electron-phonon coupling strength"]),
            ("Carbon Capture & Conversion", ["metal-organic frameworks (MOFs)", "electrochemical CO2 reduction", "direct air capture amine sorbents", "CO2-to-ethylene selectivity", "photocatalytic solar fuel generation"]),
            ("Thermoelectric & Magnetocaloric Materials", ["phonon scattering at interfaces", "Seebeck coefficient enhancement", "low-lattice thermal conductivity", "giant magnetocaloric effect", "Heusler alloy thermodynamics"]),
            ("2D Materials & Heterostructures", ["twisted bilayer graphene flat bands", "transition metal dichalcogenide excitons", "ferroelectric 2D crystals", "interlayer exciton transport", "hexagonal boron nitride dielectric screening"]),
            ("Hydrogen Storage Systems", ["metal hydride sorption thermodynamics", "cryo-compressed hydrogen tanks", "chemical hydrogen carriers", "porous aromatic frameworks", "hysteresis suppression"]),
            ("Smart & Self-Healing Polymers", ["dynamic covalent bonding networks", "supramolecular hydrogen-bonding elastomeric matrices", "mechanochromic polymers", "shape memory alloys", "vitrimeric polymer recycling"]),
            ("Corrosion Science & Surface Engineering", ["atomic layer deposition barrier coatings", "high-entropy alloy passivation", "microbiologically influenced corrosion", "cathodic protection dynamics", "pitting initiation kinetics"])
        ],
        "question_templates": [
            "What thermodynamic factors control phase stability in {topic} exposed to {condition}?",
            "How does interfacial charge transfer between {topic} and {condition} vary with {method}?",
            "What transport mechanisms dictate ionic conductivity across {topic} when synthesized via {method}?",
            "Under what mechanical strain conditions does {topic} exhibit optimal performance according to {condition}?",
            "How can {method} effectively reduce defect density in {topic} under operational stresses?"
        ]
    },
    {
        "domain": "Astrophysics & Theoretical Cosmology",
        "subfields": [
            ("Dark Matter & Dark Energy", ["WIMP scattering cross-sections", "axion-like particle conversions", "warm dark matter halos", "quintessence dynamical scalar fields", "modified Newtonian dynamics"]),
            ("Gravitational Wave Astronomy", ["compact binary coalescence ringdowns", "stochastic gravitational wave background", "neutron star equation of state", "eccentric binary inspirals", "kilonova electromagnetic counterparts"]),
            ("Exoplanet Atmospheres", ["transmission spectroscopy biosignatures", "atmospheric escape hydrodynamic loss", "cloud radiative feedback", "secondary atmosphere formation", "habitable zone photochemical equilibria"]),
            ("Early Universe Cosmology", ["primordial gravitational waves", "cosmic microwave background polarization B-modes", "cosmic inflation slow-roll potential", "baryogenesis mechanisms", "primordial black hole formation"]),
            ("High-Energy Astrophysics", ["relativistic jet collimation in AGN", "gamma-ray burst central engines", "fast radio burst magnetar mechanisms", "cosmic ray acceleration at shock fronts", "pulsar wind nebulae dynamics"]),
            ("Stellar Evolution & Nucleosynthesis", ["core-collapse supernova neutrino transport", "r-process elemental abundance yields", "pair-instability supernovae", "asymptotic giant branch nucleosynthesis", "binary mass-transfer evolution"]),
            ("Galactic Dynamics", ["supermassive black hole co-evolution", "stellar stream perturbation by dark subhalos", "secular bar-driven galactic evolution", "interstellar medium turbulence", "feedback-regulated star formation"]),
            ("Intergalactic Medium & Reionization", ["cosmic dawn 21-cm hydrogen signals", "Lyman-alpha forest tomography", "Pop III star ionizing photon production", "patchy reionization topology", "intergalactic magnetic fields"]),
            ("Solar & Heliospheric Physics", ["coronal heating magnetic reconnection", "solar wind acceleration mechanisms", "flux rope stability in coronal mass ejections", "heliopause boundary structure", "MHD wave dissipation in solar corona"]),
            ("Observational Cosmology & Cosmic Web", ["baryon acoustic oscillation peak positions", "weak gravitational lensing shear statistics", "Hubble tension systematic reconciliation", "galaxy cluster abundance scaling relations", "cosmic void velocity profiles"])
        ],
        "question_templates": [
            "How do observational signatures of {topic} distinguish between competing theories when measured with {condition}?",
            "What relativistic corrections are required to accurately model {topic} during {condition} using {method}?",
            "In what observational window can {method} resolve the subtle variations in {topic} driven by {condition}?",
            "What are the implications for fundamental physics if {topic} demonstrates unexpected coupling with {condition}?",
            "How does non-linear gravitational evolution distort the statistical properties of {topic} across {condition}?"
        ]
    },
    {
        "domain": "Neuroscience & Cognitive Systems",
        "subfields": [
            ("Synaptic Plasticity", ["spike-timing-dependent plasticity", "long-term potentiation induction cascades", "dendritic spine structural remodeling", "homeostatic synaptic scaling", "retrograde endocannabinoid signaling"]),
            ("Neural Circuitry & Connectomics", ["cortical microcolumn connectivity", "inhibitory interneuron diversity", "thalamocortical oscillation loops", "whole-brain tractography", "functional connectome modularity"]),
            ("Neural Encoding & Computation", ["population vector coding", "predictive coding predictive error minimization", "canonical microcircuits", "sparse coding in sensory cortex", "neural manifold geometries"]),
            ("Brain-Computer Interfaces", ["intracortical multi-electrode decoding", "non-invasive EEG source localization", "adaptive closed-loop stimulation", "biocompatible neural probe degradation", "motor intention phase decoding"]),
            ("Neurodegenerative Disorders", ["tau hyperphosphorylation propagations", "alpha-synuclein prion-like templating", "amyloid-beta oligomer synaptotoxicity", "microglial activation phenotypes", "blood-brain barrier breakdown"]),
            ("Cognitive Control & Decision Making", ["drift-diffusion decision models", "dopaminergic reward prediction error", "prefrontal cortex working memory gating", "anterior cingulate conflict monitoring", "metacognitive confidence calibration"]),
            ("Sensory Perception & Multisensory Integration", ["maximum likelihood sensory fusion", "auditory tonotopic plasticity", "retinal ganglion temporal filtering", "olfactory receptor combinatorial mapping", "somatosensory receptive field restructuring"]),
            ("Sleep & Neural Oscillations", ["slow-wave memory consolidation", "REM sleep theta coherence", "glymphatic waste clearance during sleep", "spindle-slow oscillation coupling", "circadian clock transcriptional feedback"]),
            ("Neuromodulation & Neuropharmacology", ["serotonergic psychedelic neuroplasticity", "optogenetic circuit manipulation", "deep brain stimulation parameter tuning", "chemogenetic receptor specificity", "cholinergic attention modulation"]),
            ("Neurodevelopment & Cellular Fate", ["neural stem cell division asymmetry", "radial glial cell migration tracks", "axon guidance cue gradient sensing", "synaptic pruning via complement cascade", "critical period opening and closure"])
        ],
        "question_templates": [
            "How do neural assemblies coordinate in {topic} during execution of tasks governed by {condition}?",
            "What molecular pathways link the initiation of {topic} with downstream functional alterations in {condition}?",
            "To what extent does {method} enable real-time reconstruction of neural dynamics in {topic} subject to {condition}?",
            "What computational advantages arise from implementing {topic} within biologically inspired models of {condition}?",
            "How does chronic disruption of {topic} lead to maladaptive reorganizations under {condition}?"
        ]
    },
    {
        "domain": "Cybersecurity & Applied Cryptography",
        "subfields": [
            ("Post-Quantum Cryptography", ["learning-with-errors (LWE) parameter selection", "module-lattice key encapsulation", "multivariate polynomial signatures", "isogeny-based key exchange", "hash-based digital signatures"]),
            ("Zero-Knowledge Proofs", ["recursive zk-SNARK composition", "polynomial commitment schemes (KZG/FRI)", "transparent zero-knowledge STARKs", "arithmetization via PlonK", "zk-rollups state transition verification"]),
            ("Hardware & Side-Channel Security", ["transient execution speculative leaks (Spectre/Meltdown)", "differential power analysis resistance", "fault injection physical attacks", "physical unclonable functions (PUFs)", "rowhammer bit-flip mitigation"]),
            ("Secure Multi-Party Computation", ["garbled circuits optimization", "oblivious transfer extensions", "threshold ECDSA signature schemes", "secret sharing schemes over rings", "private set intersection algorithms"]),
            ("Formal Verification of Software & Protocols", ["symbolic execution for smart contracts", "interactive theorem proving (Coq/Lean)", "separation logic for concurrent systems", "model checking of cryptographic protocols", "automated SMT solver verification"]),
            ("Network Security & Threat Intelligence", ["BGP hijack detection and RPKI validation", "zero-trust identity architectures", "DNS-over-HTTPS privacy guarantees", "encrypted traffic behavioral classification", "automated incident response orchestration"]),
            ("Differential Privacy & Data Security", ["local differential privacy mechanisms", "Rényi differential privacy bounds", "homomorphic encryption evaluation keys", "secure enclaves (SGX/SEV) attestation", "synthetic data privacy-utility tradeoffs"]),
            ("Vulnerability Analysis & Reverse Engineering", ["coverage-guided fuzzing techniques", "control-flow integrity (CFI) enforcement", "memory safety mitigations (Rust vs C)", "kernel exploit payload development", "binary lifting and decompilation"]),
            ("Adversarial Machine Learning", ["poisoning attacks on federated models", "membership inference defenses", "adversarial perturbation transferability", "certified robustness bounds", "model extraction watermarking"]),
            ("Identity & Authentication Systems", ["FIDO2 WebAuthn passkey security", "decentralized identity verifiable credentials", "biometric template protection", "continuous authentication architectures", "single sign-on SAML/OIDC tokens"])
        ],
        "question_templates": [
            "What cryptographic assumptions guarantee the security bounds of {topic} in adversarial environments featuring {condition}?",
            "How does {method} diminish the attack surface of {topic} without imposing unacceptable performance overheads?",
            "Under what conditions can side-channel leakages undermine the theoretical guarantees of {topic} when analyzed via {method}?",
            "What trade-off between privacy preservation and utility emerges when applying {method} to {topic} under {condition}?",
            "How can formal verification via {method} prove resistance against state machine bypasses in {topic}?"
        ]
    },
    {
        "domain": "Environmental Sciences & Climate Dynamics",
        "subfields": [
            ("Carbon Sequestration & Geoengineering", ["mineral carbonation thermodynamics", "direct ocean carbon capture", "stratospheric aerosol injection microphysics", "biochar soil amendment stability", "enhanced rock weathering kinetics"]),
            ("Atmospheric & Aerosol Dynamics", ["cloud condensation nuclei activation", "secondary organic aerosol formation", "radiative forcing uncertainty quantification", "stratospheric-tropospheric exchange", "boundary layer turbulence parametrization"]),
            ("Cryospheric Change & Sea-Level Rise", ["marine ice sheet instability (MISI)", "subglacial meltwater drainage channels", "permafrost methane feedback emissions", "polar vortex destabilization", "calving front fracture mechanics"]),
            ("Ocean Circulation & Biogeochemistry", ["Atlantic Meridional Overturning Circulation (AMOC) tipping points", "ocean acidification impact on calcifiers", "oxygen minimum zone expansion", "iron fertilization ecological consequences", "mesoscale eddy kinetic energy transport"]),
            ("Extreme Weather & Attribution Science", ["atmospheric river moisture transport", "heat dome persistent ridge dynamics", "tropical cyclone intensification rates", "compound drought-heatwave events", "extreme event attribution statistical modeling"]),
            ("Terrestrial Ecology & Forest Dynamics", ["tropical forest carbon sink saturation", "wildfire regime shifts and pyrodiversity", "drought-induced hydraulic failure in xylem", "soil microbiome nutrient cycling", "phenological mismatch in pollinator systems"]),
            ("Water Resources & Hydrology", ["groundwater depletion gravimetric assessment", "snowpack water equivalent estimation", "basin-scale hydrological runoff modeling", "desalination brine environmental impact", "transboundary aquifer management"]),
            ("Urban Climatology & Sustainability", ["urban heat island mitigation strategies", "green infrastructure stormwater retention", "building thermal mass efficiency", "urban canopy microclimate modeling", "low-carbon transportation transitions"]),
            ("Ecotoxicology & Pollution Tracking", ["microplastic bioaccumulation pathways", "per- and polyfluoroalkyl substances (PFAS) degradation", "heavy metal phytoremediation efficiency", "airborne particulate matter (PM2.5) speciation", "endocrine disruptor aquatic impacts"]),
            ("Climate Econometrics & Risk Modeling", ["integrated assessment model climate damages", "catastrophe risk bond valuation", "carbon pricing social cost estimation", "transition risk in renewable asset portfolios", "adaptation economics in coastal zones"])
        ],
        "question_templates": [
            "What non-linear feedback loops dictate the response of {topic} when subjected to {condition}?",
            "How do spatial heterogeneities in {topic} influence global projection models evaluated with {method}?",
            "What empirical evidence supports the existence of critical tipping points in {topic} driven by {condition}?",
            "To what extent can {method} resolve the temporal latency between emissions and impacts in {topic}?",
            "How do high-resolution numerical simulations with {method} refine the confidence intervals for {topic} under {condition}?"
        ]
    },
    {
        "domain": "Pharmacology & Advanced Therapeutics",
        "subfields": [
            ("Targeted Drug Discovery", ["structure-based small molecule design", "PROTAC targeted protein degradation", "allosteric kinase inhibitors", "fragment-based lead generation", "covalent inhibitor selectivity"]),
            ("Drug Delivery Systems", ["lipid nanoparticle biodistribution", "polymeric micelles for hydrophobic drugs", "exosome-mediated biomolecule delivery", "inhalable dry powder formulations", "stimuli-responsive hydrogel release"]),
            ("Pharmacokinetics & Dynamics (PK/PD)", ["physiologically based pharmacokinetic (PBPK) modeling", "receptor occupancy-efficacy relationships", "nonlinear target-mediated drug disposition", "cytochrome P450 drug interaction kinetics", "therapeutic drug monitoring algorithms"]),
            ("Immunotherapy & Biologics", ["bispecific T-cell engager (BiTE) constructs", "monoclonal antibody glycosylation profiles", "cytokine release syndrome mitigation", "oncolytic virus tumor selectivity", "checkpoint inhibitor synergy"]),
            ("RNA Therapeutics", ["antisense oligonucleotide splice modulation", "siRNA chemical modification stabilizing patterns", "circular RNA translation efficiency", "self-amplifying mRNA vaccines", "endosomal escape enhancement"]),
            ("Neurotherapeutics & CNS Delivery", ["receptor-mediated transcytosis at the blood-brain barrier", "focused ultrasound-assisted drug delivery", "intrathecal administration pharmacodynamics", "intranasal-to-brain peptide transport", "neuroprotective peptide stability"]),
            ("Toxicology & Safety Pharmacology", ["hERG potassium channel cardiotoxicity assays", "drug-induced liver injury (DILI) biomarkers", "reactive metabolite trapping", "in vitro organ-on-a-chip toxicology", "off-target kinome profiling"]),
            ("Precision Oncology & Biomarkers", ["liquid biopsy circulating tumor DNA (ctDNA) dynamics", "synthetic lethality biomarker pairs", "homologous recombination deficiency scoring", "mechanisms of acquired resistance to EGFR inhibitors", "spatial transcriptomic biomarker validation"]),
            ("Cell & Gene Therapies", ["viral vector packaging efficiency (AAV)", "autologous vs allogeneic stem cell therapies", "non-viral electroporation delivery", "CAR-NK cell durability", "ex vivo cellular expansion protocols"]),
            ("Rare Diseases & Orphan Drugs", ["enzyme replacement therapy biodistribution", "readthrough compounds for nonsense mutations", "chaperone-assisted protein folding therapies", "allele-specific silencing", "natural history biomarker correlation"])
        ],
        "question_templates": [
            "What biophysical barriers prevent optimal delivery of {topic} when formulated with {condition}?",
            "How does chemical optimization via {method} alter the therapeutic index of {topic} against {condition}?",
            "What molecular mechanisms explain therapeutic resistance in {topic} during continuous exposure to {condition}?",
            "How does the PK/PD profile of {topic} shift when evaluated using {method} in patient sub-populations with {condition}?",
            "To what degree can {method} predict clinical toxicity outcomes for {topic} interacting with {condition}?"
        ]
    },
    {
        "domain": "Applied Mathematics & Theoretical Computer Science",
        "subfields": [
            ("Spectral Graph Theory", ["Laplacian eigenvalue distributions", "Ramanujan expander graphs", "graph conductance bounds", "Cheeger constant inequalities", "effective resistance metrics"]),
            ("High-Dimensional Probability", ["sub-Gaussian matrix concentration inequalities", "non-asymptotic random matrix theory", "Johnson-Lindenstrauss lemma optimality", "sparse recovery guarantees", "Wasserstein distance convergence"]),
            ("Computational Complexity", ["derandomization conjectures", "circuit complexity lower bounds", "fine-grained complexity reductions", "P vs NP barrier theorems (natural proofs)", "quantum query complexity"]),
            ("Approximation & Online Algorithms", ["metric embeddings into tree metrics", "semidefinite programming relaxations", "submodular function maximization", "competitive ratio analysis in online caching", "primal-dual approximation schemes"]),
            ("Nonlinear Partial Differential Equations", ["Navier-Stokes smooth solution regularity", "dispersive wave equation soliton stability", "Hamilton-Jacobi-Bellman viscosity solutions", "reaction-diffusion pattern formations", "free boundary problem regularity"]),
            ("Algebraic Topology & Geometry", ["persistent homology persistence diagrams", "sheaf theory on stratified spaces", "derived algebraic geometry moduli spaces", "topological data analysis mapper graphs", "characteristic classes of vector bundles"]),
            ("Continuous & Discrete Optimization", ["interior-point method polynomial convergence", "accelerated gradient momentum methods", "non-convex optimization landscapes", "semidefinite rank minimization", "stochastic variance-reduced gradient (SVRG)"]),
            ("Information Theory & Coding", ["polar code error-exponent scaling", "network coding capacity regions", "non-linear channel capacity bounds", "rate-distortion theory under perception constraints", "LDPC code belief propagation thresholds"]),
            ("Dynamical Systems & Ergodic Theory", ["chaotic attractor Lyapunov exponents", "KAM theory invariant tori persistence", "strange nonchaotic attractors", "transfer operator spectral gaps", "bifurcation analysis in coupled oscillators"]),
            ("Number Theory & Arithmetic Geometry", ["elliptic curve rank distributions (BSD conjecture)", "L-function zero distribution statistics", "modular form Galois representations", "sieve methods in prime gaps", "p-adic Hodge theory foundations"])
        ],
        "question_templates": [
            "What structural properties of {topic} determine the sharp phase transitions observed under {condition}?",
            "How does applying {method} yield improved upper bounds for the asymptotic complexity of {topic} in {condition}?",
            "Under what regularity conditions does the solution space of {topic} admit a unique fixed point in {condition}?",
            "What topological invariants classify the equivalence classes of {topic} when analyzed through {method}?",
            "How can variational principles in {method} establish stability guarantees for {topic} interacting with {condition}?"
        ]
    }
]

DIFFICULTY_LEVELS = ["Graduate", "Doctoral", "Postdoctoral"]
RESEARCH_TYPES = ["Theoretical", "Empirical", "Computational", "Methodological"]
RESEARCH_OBJECTIVES = [
    "Derive the governing mathematical representations and asymptotic stability criteria.",
    "Formulate an empirical protocol to isolate primary causal determinants against confounding noise.",
    "Evaluate computational tractability, scaling bottlenecks, and algorithmic convergence rates.",
    "Propose a reproducible validation methodology incorporating cross-dataset generalization benchmarks.",
    "Synthesize existing analytical frameworks to resolve conflicting literature findings."
]
EXPECTED_OUTPUT_TYPES = [
    "Formal proof outline, asymptotic complexity bound, and theoretical boundary conditions.",
    "Experimental hypothesis, multi-stage testing protocol, and quantitative evaluation metric suite.",
    "Algorithmic pseudo-code, convergence proof, and empirical scaling analysis.",
    "Mechanistic pathway model, counter-evidence analysis, and falsification criteria."
]


def generate_single_question(global_index: int) -> dict:
    q_id = f"Q{global_index:05d}"
    
    # Deterministically select domain and subfield using index to guarantee rich, uniform coverage
    domain_idx = (global_index - 1) % len(DOMAINS_DATA)
    domain_data = DOMAINS_DATA[domain_idx]
    
    subfield_idx = ((global_index - 1) // len(DOMAINS_DATA)) % len(domain_data["subfields"])
    subfield_name, concepts = domain_data["subfields"][subfield_idx]
    
    c_idx1 = ((global_index - 1) * 3) % len(concepts)
    c_idx2 = ((global_index - 1) * 7 + 1) % len(concepts)
    if c_idx1 == c_idx2:
        c_idx2 = (c_idx2 + 1) % len(concepts)
    
    topic = concepts[c_idx1]
    condition = concepts[c_idx2]
    
    methods = [
        "high-order perturbation analysis",
        "Bayesian non-parametric inference",
        "stochastic gradient variational Bayes",
        "first-principles density functional theory",
        "rigorous non-asymptotic concentration bounds",
        "multi-scale hydrodynamic simulations",
        "controlled randomized perturbation experiments",
        "cryogenic spectroscopy measurements"
    ]
    method = methods[((global_index - 1) * 5) % len(methods)]
    
    template_idx = ((global_index - 1) // 3) % len(domain_data["question_templates"])
    template = domain_data["question_templates"][template_idx]
    
    question_text = template.format(topic=topic, condition=condition, method=method)
    
    difficulty = DIFFICULTY_LEVELS[((global_index - 1) // 7) % len(DIFFICULTY_LEVELS)]
    research_type = RESEARCH_TYPES[((global_index - 1) // 11) % len(RESEARCH_TYPES)]
    objective = RESEARCH_OBJECTIVES[((global_index - 1) // 13) % len(RESEARCH_OBJECTIVES)]
    expected_output = EXPECTED_OUTPUT_TYPES[((global_index - 1) // 17) % len(EXPECTED_OUTPUT_TYPES)]
    
    batch_num = ((global_index - 1) // 1000) + 1
    
    item = {
        "id": q_id,
        "domain": domain_data["domain"],
        "subfield": subfield_name,
        "difficulty": difficulty,
        "research_type": research_type,
        "instruction": f"Investigate the research question regarding {topic} in the context of {subfield_name}. Formulate the theoretical foundations, analytical methodology, and validation criteria.",
        "question": question_text,
        "focal_concepts": [topic, condition],
        "research_objective": objective,
        "expected_output_type": expected_output,
        "metadata": {
            "batch_number": batch_num,
            "sample_index": global_index,
            "modality": "Fine-Tuning Instruction"
        }
    }
    return item


async def generate_batch_file(batch_num: int, output_dir: str):
    start_time = time.time()
    filename = f"data_batch_{batch_num:02d}.json"
    filepath = os.path.join(output_dir, filename)
    
    start_id = (batch_num - 1) * 1000 + 1
    end_id = batch_num * 1000
    
    # Asynchronously generate 1000 items
    questions = []
    for idx in range(start_id, end_id + 1):
        questions.append(generate_single_question(idx))
        if idx % 250 == 0:
            await asyncio.sleep(0.001)  # Yield to event loop
    
    # Serialize to JSON and write file asynchronously via asyncio.to_thread
    def write_json():
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(questions, f, indent=2, ensure_ascii=False)
            
    await asyncio.to_thread(write_json)
    
    elapsed = time.time() - start_time
    print(f"Batch {batch_num:02d} completed: {filename} ({len(questions)} items, IDs Q{start_id:05d} - Q{end_id:05d}) in {elapsed:.2f}s")
    return filepath


async def main():
    repo_dir = os.path.dirname(os.path.abspath(__file__))
    print(f"Starting asynchronous question generation in: {repo_dir}")
    print("Target: 15,000 structured research questions across 15 JSON batches.")
    
    total_start = time.time()
    tasks = [generate_batch_file(batch_num, repo_dir) for batch_num in range(1, 16)]
    results = await asyncio.gather(*tasks)
    
    total_elapsed = time.time() - total_start
    print(f"\nAll 15 batches successfully generated in {total_elapsed:.2f}s.")
    print(f"Files created: {len(results)}")


if __name__ == "__main__":
    asyncio.run(main())
