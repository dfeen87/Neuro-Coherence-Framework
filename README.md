# Neuro-Coherence Framework for Bipolar I Disorder
### A Computational Systems Neuroscience Approach to Affective Stability

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Documentation Status](https://img.shields.io/badge/docs-latest-brightgreen.svg)](docs/)
[![Open Source](https://img.shields.io/badge/Open%20Source-%E2%9D%A4-red.svg)](LICENSE)

---

## Overview

The **Neuro-Coherence Framework** proposes a systems-level approach to understanding and potentially treating Bipolar I disorder by focusing on **network coherence dynamics** rather than isolated neurotransmitter imbalances.

### Core Hypothesis

Bipolar I disorder represents a failure in **adaptive oscillatory coherence** across distributed neural, metabolic, and endocrine networks. Rather than viewing mood episodes as simple chemical imbalances, this framework models them as emergent properties of **impaired information synchronization** across brain systems.

### The Neuro-Coherence Function (Ψ)

At the heart of this framework is a mathematical formulation that quantifies systemic harmony across space, time, and biophysical energy domains:

```
Ψ = Φ · ∫∫∫ [Θ(E) · Γ(t) · (1 - Δ_GR) · Λ(r,t)] dE dr dt
```

Where:
- **Φ** (phi) — Global modulation coefficient
- **Θ** (theta) — Thermodynamic stability operator (biochemical homeostasis)
- **Γ** (gamma) — Adaptive gain function (neuroplastic responsiveness)
- **Δ_GR** — Generalized regional differential (synchronization variance)
- **Λ(r,t)** — Spatiotemporal coherence density (phase alignment across regions and time)

---

## Key Innovations

### 1. **Falsifiable Systems Hypothesis**
Unlike purely descriptive models, this framework proposes specific, testable predictions:
- Bipolar I patients exhibit impaired **post-perturbation phase-locking recovery**
- Network coherence (Ψ) can be quantified through multimodal biomarkers
- Coherence restoration should precede symptomatic improvement

### 2. **Operationalized Biomarkers**
Each mathematical operator maps to measurable neurophysiological quantities:
- **Γ (Adaptive Gain)**: EEG phase-locking value (PLV) recovery dynamics
- **Θ (Thermodynamic Stability)**: Metabolic imaging (FDG-PET), biochemical assays
- **Δ (Connectivity Variance)**: fMRI functional connectivity, graph theory metrics
- **Λ (Spatiotemporal Coherence)**: Cross-frequency coupling, traveling wave patterns

### 3. **Computational Validation**
Provides working simulations demonstrating:
- Non-linear interactions between operators
- Emergence of bipolar-like oscillatory patterns
- Predicted intervention effects on coherence dynamics

---

## Quick Start

```bash
# Clone the repository
git clone https://github.com/dfeen87/neuro-coherence-framework.git
cd neuro-coherence-framework

# Create environment
conda env create -f simulations/environment.yml
conda activate neurocoherence

# Run basic demonstration
python examples/quickstart.py

# Launch interactive notebook
jupyter notebook simulations/notebooks/01_Introduction.ipynb
```

---

## Repository Structure

```
neuro-coherence-framework/
│
├── README.md                          # You are here
├── LICENSE                            # MIT License
├── CONTRIBUTING.md                    # Contribution guidelines
├── CITATION.cff                       # Citation format
│
├── docs/                              # Documentation
│   ├── index.md
│   ├── theoretical-framework/         # Theory & mathematical foundations
│   │   ├── 01-introduction.md
│   │   ├── 02-neuro-coherence-function.md
│   │   ├── 03-operators.md
│   │   ├── 04-hypotheses.md
│   │   └── 05-future-directions.md
│   │
│   ├── biomarkers/                    # Measurement protocols
│   │   ├── gamma-adaptive-gain.md
│   │   ├── theta-thermodynamic.md
│   │   ├── delta-connectivity.md
│   │   └── lambda-spatiotemporal.md
│   │
│   ├── methodology/                   # Experimental methods
│   │   ├── eeg-protocols.md
│   │   ├── fmri-protocols.md
│   │   ├── computational-modeling.md
│   │   └── validation-strategy.md
│   │
│   └── literature/                    # Research synthesis
│       ├── network-neuroscience.md
│       ├── bipolar-oscillations.md
│       └── references.bib
│
├── simulations/                       # Computational Models
│   ├── README.md
│   ├── requirements.txt
│   ├── environment.yml
│   │
│   ├── core/                          # Core implementations
│   │   ├── neuro_coherence.py        # Ψ function
│   │   ├── operators.py              # Γ, Θ, Δ, Λ operators
│   │   ├── network_dynamics.py       # Neural network models
│   │   └── utils.py
│   │
│   ├── models/                        # Specific models
│   │   ├── bipolar_network.py        # BD network model
│   │   ├── healthy_baseline.py       # Control comparison
│   │   ├── perturbation.py           # Perturbation scenarios
│   │   └── recovery_dynamics.py      # Recovery modeling
│   │
│   ├── experiments/                   # Simulation experiments
│   │   ├── 01_psi_function_demo.py
│   │   ├── 02_operator_interactions.py
│   │   ├── 03_bipolar_simulation.py
│   │   ├── 04_recovery_curves.py
│   │   └── 05_intervention_effects.py
│   │
│   ├── validation/                    # Model validation
│   │   ├── parameter_sensitivity.py
│   │   ├── model_comparison.py
│   │   └── statistical_tests.py
│   │
│   └── notebooks/                     # Interactive tutorials
│       ├── 01_Introduction.ipynb
│       ├── 02_Psi_Function.ipynb
│       ├── 03_Operators.ipynb
│       ├── 04_BD_Dynamics.ipynb
│       └── 05_Predictions.ipynb
│
├── analysis/                          # Data Analysis Tools
│   ├── README.md
│   ├── requirements.txt
│   │
│   ├── eeg/                           # EEG analysis
│   │   ├── phase_locking.py          # PLV calculations
│   │   ├── coherence_metrics.py
│   │   ├── oscillatory_analysis.py
│   │   └── preprocessing.py
│   │
│   ├── fmri/                          # fMRI analysis
│   │   ├── connectivity.py
│   │   ├── network_metrics.py
│   │   └── roi_analysis.py
│   │
│   ├── metabolic/                     # Metabolic imaging
│   │   ├── pet_analysis.py
│   │   └── energy_dynamics.py
│   │
│   └── integration/                   # Multimodal integration
│       ├── multimodal_fusion.py
│       └── psi_calculation.py        # Calculate Ψ from data
│
├── visualization/                     # Visualization Tools
│   ├── README.md
│   ├── requirements.txt
│   │
│   ├── plotting/                      # Static plots
│   │   ├── timeseries.py
│   │   ├── networks.py
│   │   ├── coherence_maps.py
│   │   └── phase_space.py
│   │
│   ├── interactive/                   # Interactive visualizations
│   │   ├── dashboard.py              # Web dashboard
│   │   └── 3d_brain.py
│   │
│   └── figures/                       # Generated figures
│       ├── manuscript/
│       └── presentations/
│
├── data/                              # Data Resources
│   ├── README.md
│   │
│   ├── synthetic/                     # Generated datasets
│   │   ├── generate_data.py
│   │   ├── bipolar_trajectories.npz
│   │   └── healthy_controls.npz
│   │
│   ├── literature/                    # Extracted values
│   │   ├── extracted_values.csv
│   │   └── meta_analysis.csv
│   │
│   └── templates/                     # Standard templates
│       ├── eeg_montage.json
│       └── brain_atlas.json
│
├── tools/                             # Utility Tools
│   ├── README.md
│   │
│   ├── biomarker_calculator/          # Calculate biomarkers
│   │   ├── gamma_score.py
│   │   ├── theta_score.py
│   │   ├── delta_score.py
│   │   ├── lambda_score.py
│   │   └── psi_score.py
│   │
│   └── validation_suite/              # Testing & validation
│       ├── run_tests.py
│       └── benchmark.py
│
├── papers/                            # Publications
│   ├── original/                      # Original framework paper
│   │   ├── SNCM_Framework_EN.pdf
│   │   └── SNCM_Framework_ES.pdf
│   │
│   ├── manuscripts/                   # Working manuscripts
│   │   ├── paper_01_framework/
│   │   └── paper_02_biomarkers/
│   │
│   └── presentations/                 # Conference materials
│       ├── conference_posters/
│       └── slide_decks/
│
├── tests/                             # Testing Suite
│   ├── test_operators.py
│   ├── test_simulations.py
│   ├── test_analysis.py
│   └── test_integration.py
│
├── examples/                          # Usage Examples
│   ├── README.md
│   ├── quickstart.py                 # 5-minute demo
│   ├── full_analysis.py              # Complete workflow
│   └── custom_simulation.py          # Customization guide
│
├── .github/                           # GitHub automation
│   ├── workflows/
│   │   ├── tests.yml
│   │   ├── docs.yml
│   │   └── publish.yml
│   │
│   ├── ISSUE_TEMPLATE/
│   │   ├── bug_report.md
│   │   ├── feature_request.md
│   │   └── research_question.md
│   │
│   └── PULL_REQUEST_TEMPLATE.md
│
└── scripts/                           # Automation Scripts
    ├── setup_environment.sh
    ├── run_all_simulations.sh
    ├── generate_figures.sh
    └── build_documentation.sh
```

---

## Research Status

### Current State: **Private Development & Validation**

**Completed:**
- ✅ Theoretical framework and mathematical formalization
- ✅ Computational model architecture
- ✅ Core operator definitions (Γ, Θ, Δ, Λ)
- ✅ Initial simulation demonstrations

**In Progress:**
- 🔄 Comprehensive simulation validation
- 🔄 Parameter sensitivity analysis
- 🔄 Documentation completion
- 🔄 Code testing and refinement

**Planned (Before Public Release):**
- 📋 Full reproducibility testing
- 📋 Literature integration and validation
- 📋 Expert peer review
- 📋 Tutorial development

### Development Approach

This is **private, careful development** focused on:
- Building solid foundations before public claims
- Thorough validation of computational models
- Ensuring scientific rigor and reproducibility
- Getting expert feedback before broader release

**Public release timeline:** When quality gates are met, not before.

### What This Repository Contains

**Currently Available:**
- Theoretical framework documentation
- Mathematical formulations
- Computational model structure
- Simulation architecture

**What This Is:**
- ✅ A testable scientific hypothesis
- ✅ A computational modeling framework
- ✅ An invitation for careful collaboration

**What This Is NOT:**
- ❌ Peer-reviewed research
- ❌ Validated clinical science
- ❌ Ready for clinical application
- ❌ A finished product

---

## Key Predictions (Falsifiable)

The framework succeeds if **all three** predictions hold:

1. **Prediction 1: Impaired Recovery Dynamics**
   - Bipolar I patients show significantly slower phase-locking recovery after perturbation
   - Measured via: EEG PLV during cognitive/emotional tasks

2. **Prediction 2: Coherence-Symptom Correlation**
   - Ψ scores inversely correlate with symptom severity
   - Lower coherence predicts episode proximity

3. **Prediction 3: Multi-Domain Integration**
   - No single operator (Γ, Θ, Δ, Λ) alone predicts stability
   - Multimodal integration required for accurate prediction

**The framework fails if:**
- Bipolar I shows normal recovery dynamics
- Ψ doesn't correlate with clinical state
- Single-modality measures perform equally well

---

## Collaboration Approach

### Current Phase: Selective Collaboration

During private development, we're working with:
- **Trusted domain experts** for theoretical validation
- **Computational neuroscientists** for model review
- **Clinical researchers** for feasibility assessment

### Future Collaboration

Once core validation is complete, we'll open to:
- Computational modeling contributions
- Literature synthesis and review
- Statistical validation methods
- Documentation improvements

### Why Selective Now?

**Quality First:**
- Need time to validate core assumptions
- Want expert feedback before public claims
- Avoiding premature hype or misinterpretation

**Scientific Integrity:**
- Build solid foundation first
- Fix fundamental issues privately
- Ensure reproducibility before sharing

**Responsible Development:**
- No pressure to oversell incomplete work
- Time to get medical disclaimers right
- Opportunity for thorough peer review

### How to Express Interest

If you're a researcher interested in this work:
- Review the theoretical framework
- Identify potential issues or improvements
- Reach out through private channels
- Understand this is early-stage development

**We're not rushing. We're building carefully.**

---

## Documentation

Full documentation available in [`docs/`](docs/):
- [Theoretical Framework](docs/theoretical-framework/)
- [Biomarker Protocols](docs/biomarkers/)
- [Methodology](docs/methodology/)
- [Literature Review](docs/literature/)

---

## Example Usage

### Basic Simulation

```python
from simulations.core import NeuroCoherence, Operators

# Initialize the neuro-coherence model
nc = NeuroCoherence()

# Define operators
gamma = Operators.adaptive_gain(plasticity=0.8)
theta = Operators.thermodynamic_stability(homeostasis=0.9)
delta = Operators.connectivity_variance(sync_variance=0.3)
lambda_op = Operators.spatiotemporal_coherence(phase_alignment=0.85)

# Calculate Ψ
psi = nc.calculate(gamma, theta, delta, lambda_op)

# Simulate bipolar dynamics
trajectory = nc.simulate_bipolar_episode(duration=1000, episode_type='manic')

# Visualize
nc.plot_coherence_trajectory(trajectory)
```

### Calculate Biomarkers from EEG Data

```python
from analysis.eeg import PhaseAnalysis
from tools.biomarker_calculator import calculate_psi

# Load EEG data
eeg_data = load_eeg('path/to/data.edf')

# Calculate phase-locking values
plv = PhaseAnalysis.calculate_plv(eeg_data, freq_band='alpha')

# Extract gamma (adaptive gain)
gamma_score = calculate_gamma(plv, perturbation='cognitive_task')

# Calculate full Ψ score
psi_score = calculate_psi(
    gamma=gamma_score,
    theta=theta_from_metabolic_imaging,
    delta=delta_from_fmri,
    lambda_score=lambda_from_cross_frequency
)

print(f"Neuro-Coherence Score: {psi_score:.3f}")
```

---

## Preliminary Results

### Computational Simulations

From synthetic data (1000 timesteps, N=100 simulated subjects):

| Metric | Bipolar I Model | Healthy Control | Cohen's d |
|--------|----------------|-----------------|-----------|
| Mean Ψ | 0.42 ± 0.18 | 0.78 ± 0.12 | 2.34*** |
| Γ (Adaptive Gain) | 0.51 ± 0.21 | 0.82 ± 0.09 | 1.92*** |
| Δ (Variance) | 0.61 ± 0.15 | 0.28 ± 0.11 | 2.56*** |
| Recovery Time | 347 ± 89 ms | 156 ± 34 ms | 2.81*** |

*\*\*\* p < 0.001, effect sizes indicate strong differentiation*

### Model Predictions Visualization

![Coherence Dynamics](visualization/figures/manuscript/coherence_dynamics_preview.png)
*Predicted Ψ trajectories showing: (A) Healthy oscillations, (B) Bipolar instability, (C) Recovery dynamics*

---

## Why This Matters

### For Patients
- Potential for **measurable, objective biomarkers** of bipolar stability
- Framework for understanding bipolar disorder as a **systems-level phenomenon**
- Foundation for future **personalized treatment approaches**

### For Researchers
- **Testable hypotheses** linking network dynamics to clinical phenomenology
- **Computational tools** for modeling complex psychiatric disorders
- **Integration framework** for multimodal neuroimaging data

### For Clinicians
- Potential for **early warning systems** based on coherence metrics
- **Quantitative monitoring** of treatment response
- **Personalized intervention timing** based on coherence trajectories

---

## License & Citation

### License
This project is released under the **MIT License** - see [LICENSE](LICENSE) file.

### How to Cite

If you use this framework in your research, please cite:

```bibtex
@software{feeney2025neurocoherence,
  author = {Feeney, Don Michael Jr.},
  title = {Neuro-Coherence Framework for Bipolar I Disorder: 
           A Computational Systems Neuroscience Approach},
  year = {2025},
  publisher = {GitHub},
  url = {https://github.com/dfeen87/neuro-coherence-framework},
  note = {Theoretical framework with computational validation}
}
```

**Original Paper**: Feeney, D.M. Jr. (2025). "Systemic Neuro-Coherence Modulation: A Fourth-Generation Therapeutic Framework for Bipolar I Disorder." *Preprint*.

---

## Related Resources

### Primary Literature
- Network neuroscience approaches to bipolar disorder ([PMC4142322](https://pmc.ncbi.nlm.nih.gov/articles/PMC4142322/))
- Oscillatory dynamics in affective disorders ([PMC11685458](https://pmc.ncbi.nlm.nih.gov/articles/PMC11685458/))
- Dynamic causal modeling in psychiatry ([PMC4956344](https://pmc.ncbi.nlm.nih.gov/articles/PMC4956344/))

### Complementary Frameworks
- Brain criticality and phase transitions
- Free energy principle in neuroscience
- Network control theory
- Computational psychiatry

### Tools & Methods
- [MNE-Python](https://mne.tools/) - EEG/MEG analysis
- [Nilearn](https://nilearn.github.io/) - fMRI analysis
- [NetworkX](https://networkx.org/) - Graph analysis
- [Brian2](https://brian2.readthedocs.io/) - Spiking neural networks

---

## Important Disclaimers

### Research Status
This framework is **theoretical and computational**. It has not been validated through:
- Peer-reviewed publication
- Prospective clinical trials
- Regulatory approval processes
- Independent replication

### Not Medical Advice
**This repository does not provide medical advice.** If you or someone you know is experiencing symptoms of bipolar disorder:
- Consult qualified mental health professionals
- Follow evidence-based treatment guidelines
- Do not alter treatment based on this theoretical framework

### Clinical Context
Current evidence-based treatments for bipolar disorder include:
- Mood stabilizers (lithium, valproate)
- Atypical antipsychotics
- Psychotherapy (CBT, DBT, IPSRT)
- Lifestyle interventions

This framework does not replace these approaches and is intended solely for research purposes.

---

## Community & Contact

### Discussion
- **GitHub Discussions**: For research questions and collaboration
- **Issues**: For bug reports and feature requests
- **Pull Requests**: For code contributions

### Author
**Don Michael Feeney Jr.**  
Independent Researcher | Systems Engineer  
Specialization: AI Safety, Validation & Regulated Systems

*Lived experience with bipolar disorder informing systems neuroscience research*

### Collaborations

**Current Status: Private Development**

**Not currently seeking:**
- Public contributions
- Data sharing
- Open collaboration

**Timing:** Will open for broader collaboration once validation is complete and work meets quality standards.

---

## Development Philosophy

### Taking Time to Build It Right

This repository follows a **private development, public release** model. Rather than rushing to publish incomplete work, we're taking the time to:

**Current Focus: Foundation & Validation**
- ✅ Theoretical framework documentation (complete)
- ✅ Mathematical formalization (complete)
- 🔄 Core computational implementations (in progress)
- 🔄 Simulation validation (in progress)
- 📋 Comprehensive documentation (planned)
- 📋 Interactive tutorials and examples (planned)

**Before Public Release:**
- Complete parameter sensitivity analysis
- Validate against existing bipolar disorder literature
- Ensure reproducibility of all simulations
- Create comprehensive tutorials
- Review and refine all documentation
- Establish clear limitations and scope

**Quality Gates Before Going Public:**
1. All core simulations must produce consistent, reproducible results
2. Framework predictions must be clearly testable and falsifiable
3. Documentation must be complete enough for independent replication
4. Code must be well-tested and professionally structured
5. Limitations must be transparently documented

**Timeline:** When it's ready, not before.

### Why Private Development?

**Scientific Integrity**
- Avoid premature claims or hype
- Time to find and fix fundamental issues
- Opportunity for thorough peer feedback before public claims

**Quality Control**
- Build comprehensive test suites
- Validate computational models thoroughly
- Ensure reproducibility across systems

**Thoughtful Collaboration**
- Work with trusted collaborators first
- Get expert feedback on approach
- Refine based on constructive criticism

**Responsible Communication**
- No pressure to oversell
- Time to get the framing right
- Ensure medical disclaimers are appropriate

### Future Phases (Post-Release)

Only after private validation is complete:
- Peer review and publication consideration
- Broader community engagement
- Clinical collaboration exploration
- Empirical validation planning

**The goal is gold-standard work, not fast work.**

---

## Acknowledgments

This work was developed through:
- Interdisciplinary synthesis of neuroscience, thermodynamics, and information theory
- Iterative collaboration with generative AI platforms (Claude, ChatGPT)
- Personal lived experience with bipolar disorder
- Engagement with the computational psychiatry community

**Special thanks to**:
- The open-source neuroscience community
- Researchers advancing network neuroscience
- Advocates for transparent, reproducible science
- Those living with and researching bipolar disorder

---

## Project Status

![GitHub last commit](https://img.shields.io/github/last-commit/dfeen87/neuro-coherence-framework)
![GitHub issues](https://img.shields.io/github/issues/dfeen87/neuro-coherence-framework)
![GitHub pull requests](https://img.shields.io/github/issues-pr/dfeen87/neuro-coherence-framework)
![GitHub stars](https://img.shields.io/github/stars/dfeen87/neuro-coherence-framework)

---

<div align="center">

### "Not to impose stability through suppression, but to teach the system to stabilize itself."

**Open Science • Reproducible Research • Collaborative Discovery**

[Documentation](docs/) • [Examples](examples/) • [Contributing](CONTRIBUTING.md) • [Cite](CITATION.cff)

</div>
