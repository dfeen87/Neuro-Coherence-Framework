# Neuro‑Coherence Framework for Bipolar I Disorder
### A Computational Systems Neuroscience Approach to Affective Stability

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/)
[![Documentation](https://img.shields.io/badge/docs-latest-brightgreen.svg)](docs/)
[![Research Status](https://img.shields.io/badge/status-private%20development-orange.svg)](#research-status)

---

## Overview

The **Neuro‑Coherence Framework** proposes that Bipolar I disorder is not simply a neurotransmitter imbalance, but a **systems‑level failure of adaptive oscillatory coherence** across neural, metabolic, and endocrine networks.

Rather than modeling mood episodes as isolated chemical fluctuations, this framework treats them as **emergent breakdowns in phase‑aligned information flow** across distributed brain systems.

At the center of the model is the **Neuro‑Coherence Function (Ψ)** — a mathematical formulation that quantifies systemic harmony across space, time, and biophysical energy domains.

This repository contains a **research‑grade computational framework** for exploring that hypothesis through simulation, multimodal biomarkers, and falsifiable predictions.

> **This is not a clinical tool.**  
> It is a theoretical and computational research framework.

---

## Conceptual Foundation  
### From Chemical Suppression → Systemic Restoration

Conventional treatments for Bipolar I disorder rely on broad neurochemical modulation. While effective for symptom stabilization, these approaches function primarily as **external regulators**, not internal restorers.

The Neuro‑Coherence Framework advances a different hypothesis:

> **Bipolar I disorder reflects a collapse in the brain’s ability to maintain coherent, phase‑aligned information flow across networks.**

The goal is not lifelong suppression, but **restoration of intrinsic coherence** — enabling the system to stabilize itself.

This reframes the central question:

**Not:** “What chemical is imbalanced?”  
**But:** “What physical law of coherence is failing in the Bipolar I brain's coherence?”

---

## The Neuro‑Coherence Function (Ψ)

```
Ψ = Φ · ∫∫∫ [ Θ(E) · Γ(t) · (1 − Δ_GR) · Λ(r,t) ] dE dr dt
```

| Symbol | Meaning | Interpretation |
|------|--------|----------------|
| **Φ** | Global modulation coefficient | System‑wide influence potential |
| **Θ** | Thermodynamic stability operator | Biochemical homeostasis |
| **Γ** | Adaptive gain function | Neuroplastic responsiveness |
| **Δ_GR** | Generalized regional differential | Synchronization variance |
| **Λ(r,t)** | Spatiotemporal coherence density | Phase alignment across regions & time |

**Interpretation:**  
Ψ represents the system’s capacity to maintain **resilient, coherent information flow**.  
When any operator destabilizes, the system enters **oscillatory divergence** — the computational signature of manic or depressive episodes.

---

## Biomarker Mapping

Each operator corresponds to measurable physiological quantities:

| Operator | Domain | Proxy Metric | Measurement |
|--------|--------|-------------|-------------|
| **Γ** | Neuroplasticity | PLV recovery after perturbation | High‑density EEG |
| **Θ** | Metabolic stability | Mitochondrial OCR, ATP production | Metabolomics, PET |
| **Δ_GR** | Network variance | DMN–SN–CEN connectivity variance | fMRI |
| **Λ(r,t)** | Phase coherence | Global phase‑lag index | EEG–fMRI fusion |

This enables **multimodal computation of Ψ** from empirical data.

---

## Neuro‑Coherence Restoration Cycle (NCRC)

A translational model describing how coherence could theoretically be restored:

### Phase 1 — Stabilization (Scaffolding)
- Suppression of incoherent oscillations  
- Reduction of Δ_GR  
- Acute increase in Λ  
- Restoration of Θ  

### Phase 2 — Resonant Integration
- Endogenous coherence loops emerge  
- Γ increases  
- System learns phase‑aligned regulation  

### Phase 3 — Adaptive Release
- External modulation tapers  
- Ψ remains elevated as influence approaches zero  
- System achieves **Systemic Independence**

> The NCRC is a **theoretical construct**, not a clinical protocol.

---

## Computational Modeling

The repository includes:
- neural mass models
- perturbation simulations
- recovery dynamics
- multimodal fusion pipelines
- validation and sensitivity analyses

### Example

```python
from simulations.core import NeuroCoherence, Operators

nc = NeuroCoherence()

gamma = Operators.adaptive_gain(plasticity=0.8)
theta = Operators.thermodynamic_stability(homeostasis=0.9)
delta = Operators.connectivity_variance(sync_variance=0.3)
lambda_op = Operators.spatiotemporal_coherence(phase_alignment=0.85)

psi = nc.calculate(gamma, theta, delta, lambda_op)
trajectory = nc.simulate_bipolar_episode(duration=1000, episode_type='manic')
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

## Key Predictions (Falsifiable)

The framework succeeds only if **all three** predictions hold:

1. **Impaired Recovery Dynamics**  
   Bipolar I patients show slower PLV recovery after perturbation.

2. **Coherence–Symptom Correlation**  
   Ψ inversely correlates with symptom severity.

3. **Multi‑Domain Integration**  
   No single operator predicts stability alone.

The framework fails if any of these conditions are not met.

---

## Theoretical Therapeutic Model (Conceptual Only)

The framework introduces a **theoretical Gen‑4 Integrated Modulator (MIG4)** — a conceptual scaffold used to explore adaptive coherence restoration.

- Not a drug
- Not under development
- Not a clinical recommendation

Its purpose is to test **computational predictions**, not propose treatment.

---

## Suggested Diagrams

- Operator interaction → Ψ  
- Coherence collapse vs restoration  
- Neuro‑Coherence Restoration Cycle  
- Multimodal biomarker integration  
- Simulation architecture  

(Diagrams live in `visualization/figures/`.)

---

## Research Status

**Current Phase:** Private Development & Validation

Completed:
- Theoretical framework
- Mathematical formalization
- Core operators
- Initial simulations

In Progress:
- Validation
- Sensitivity analysis
- Documentation refinement

Public release occurs **only when quality gates are met**.

---

## Disclaimers

- Not peer‑reviewed
- Not clinically validated
- Not medical advice

Consult qualified professionals for clinical care.

---

## Citation

```bibtex
@software{feeney2025neurocoherence,
  author = {Feeney, Don Michael Jr.},
  title = {Neuro‑Coherence Framework for Bipolar I Disorder},
  year = {2025},
  publisher = {GitHub},
  note = {Theoretical framework with computational validation}
}
```

---

## Closing

> *“Not to impose stability through suppression, but to teach the system to stabilize itself.”*

**Open Science • Reproducible Research • Responsible Development**
