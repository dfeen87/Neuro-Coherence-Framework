# Neuro‑Coherence Framework for Bipolar I Disorder
### A Computational Systems Neuroscience Approach to Affective Stability

[![CI](https://github.com/dfeen87/Neuro-Coherence-Framework/actions/workflows/ci.yml/badge.svg)](https://github.com/dfeen87/Neuro-Coherence-Framework/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/)
[![Documentation](https://img.shields.io/badge/docs-latest-brightgreen.svg)](docs/)
[![Tests](https://img.shields.io/badge/tests-65%20passing-brightgreen.svg)](#testing)

---

## Overview

The **Neuro‑Coherence Framework** proposes that Bipolar I disorder is not simply a neurotransmitter imbalance, but a **systems‑level failure of adaptive oscillatory coherence** across neural, metabolic, and endocrine networks.

Rather than modeling mood episodes as isolated chemical fluctuations, this framework treats them as **emergent breakdowns in phase‑aligned information flow** across distributed brain systems.

At the center of the model is the **Neuro‑Coherence Function (Ψ)** — a mathematical formulation that quantifies systemic harmony across space, time, and biophysical energy domains.

This repository contains a **research‑grade computational framework** for exploring that hypothesis through simulation, multimodal biomarkers, and falsifiable predictions.

> **Note: This is not a clinical tool.**
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
**But:** “What physical law governing coherence is failing in Bipolar I?”

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

### Concurrent EEG–fMRI Integration & Clinical Stratification (v2.0.0)

The **v2.0.0** release establishes concurrent EEG–fMRI (simultaneous EEG–fMRI) processing as a first-class integration unit within the Neuro-Coherence Framework. Located in `analysis/eeg_fmri/` and orchestrated via `ConcurrentEEGFMRIProcessor`, this architecture aligns high-temporal-resolution EEG phase dynamics with spatial BOLD network connectivity to quantify systemic coherence ($\Psi$) in bipolar disorder workflows.

#### Core Capabilities

1. **EEG-in-MRI Preprocessing & Artifact Correction (`analysis/eeg_fmri/preprocessing.py`)**:
   - **Gradient Artifact (GA) Removal**: Average Artifact Subtraction (AAS) with volume trigger alignment, augmented with Optimal Basis Sets (OBS/PCA) for residual pulse suppression.
   - **Ballistocardiogram (BCG) Removal**: ECG R-peak alignment paired with OBS/PCA cardiac artifact decomposition.
   - **Motion & Scanner Noise Filtering**: Bandpass filtering, z-score motion detection, and signal despeckling.
   - **Quantitative Benchmark Metrics**: Calculates Artifact Reduction Ratio (ARR in dB), Signal-to-Artifact Ratio improvement ($\Delta\text{SAR}$ in dB), and ground-truth correlation.

2. **Cross-Modal Spatiotemporal Synchronization (`analysis/eeg_fmri/synchronization.py`)**:
   - **Temporal Alignment**: HRF convolution of band-limited EEG envelope and downsampling to fMRI TR resolution.
   - **Joint Coherence ($\Lambda$)**: Combines sliding-window Phase Locking Value (PLV), EEG envelope ↔ BOLD cross-correlation, and Canonical Correlation Analysis / singular correlation (CCA).
   - **Network Connectivity Instability ($\Delta_{GR}$)**: Measures sliding-window functional connectivity variance across fronto-limbic and triple-network nodes (DMN, Salience, CEN).

3. **Bipolar Disorder Regime Stratification**:
   - **Euthymic**: High joint coherence ($\Lambda \ge 0.50$) and stable network regulation ($\Delta_{GR} \le 0.35$).
   - **Manic**: Elevated network connectivity variance ($\Delta_{GR} \ge 0.40$) driven by phase instability and cross-network dysregulation.
   - **Depressive**: Low joint coherence ($\Lambda \le 0.35$) and hypo-connected network regulation ($\Delta_{GR} \le 0.35$).

4. **Synthetic Concurrent Dataset Generation (`data/synthetic/generate_data.py`)**:
   - `generate_concurrent_eeg_fmri_data()` simulates uncorrupted/corrupted concurrent EEG and BOLD signals with controllable bipolar coupling and realistic scanner artifacts for benchmarking.

---

### Target Identification & Sensitivity Analysis

The **v1.2.0** update introduces the `analysis/sensitivity.py` module, transitioning the framework from a theoretical model to a functional **Target Identification** tool for drug development and clinical research.

#### The Sensitivity Gradient (∇Ψ)

To move beyond chemical suppression toward **Systemic Restoration**, we must identify which biological operators provide the most leverage for stabilization. The framework now calculates the partial derivatives of the Neuro-Coherence Function:

**∂Ψ/∂Γ, ∂Ψ/∂Θ, ∂Ψ/∂Δ, ∂Ψ/∂Λ**

This allows researchers to quantify exactly how a change in **Thermodynamic Stability (Θ)** or **Adaptive Gain (Γ)** impacts the global coherence of the system. By mapping the magnitude of the gradient **||∇Ψ||**, we can pinpoint the "Leverage Points" of the architecture.

#### Key Capabilities

* **Global Parameter Sweeps**: Execute Grid or Monte Carlo sampling to map the "Topography of Stability."
* **Tipping Point Mapping**: Automatically detect the "Cliff’s Edge"—the specific parameter coordinates where **Ψ ≈ 0** and the system enters oscillatory divergence (Manic/Depressive onset).
* **Therapeutic Leverage Points**: Identify regions where the sensitivity magnitude is maximized, indicating the most effective targets for metabolic or neuroplastic intervention.



#### Practical Application: Metabolic vs. Plasticity Targets

If the sensitivity heatmap shows high density along the **Θ axis**, it mathematically suggests that **metabolic/mitochondrial restoration** is the priority for that specific systemic profile. Conversely, if **Γ** is the primary driver of variance, **neuroplastic-restorative** agents take precedence.

---

## Installation

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Quick Install

```bash
# Clone repository
git clone https://github.com/dfeen87/Neuro-Coherence-Framework.git
cd Neuro-Coherence-Framework

# Install package
pip install -e .

# Run quick start example
python examples/quickstart.py
```

### Development Install

```bash
# Install with development dependencies
pip install -e ".[dev]"

# Run tests
pytest tests/
```

### Optional Dependencies

For full functionality (EEG/fMRI analysis, interactive visualizations):

```bash
pip install -e ".[full]"
```

---

## Quick Start

### Basic Usage

```python
from simulations.core import NeuroCoherence, Operators

# Initialize calculator
nc = NeuroCoherence()

# Calculate operators
gamma = Operators.adaptive_gain(plasticity=0.8)
theta = Operators.thermodynamic_stability(homeostasis=0.9)
delta = Operators.connectivity_variance(sync_variance=0.3)
lambda_op = Operators.spatiotemporal_coherence(phase_alignment=0.85)

# Compute Ψ
psi = nc.calculate(gamma, theta, delta, lambda_op)
print(f"Ψ = {psi.psi:.4f}")

# Simulate bipolar episode
trajectory = nc.simulate_bipolar_episode(
    duration=1000,
    episode_type='manic'
)
```

### Multimodal Analysis

```python
from analysis.integration import MultimodalPsiCalculator
from data.synthetic.generate_data import generate_eeg_signals
from analysis.eeg import calculate_plv_matrix

# Generate synthetic EEG
time, signals = generate_eeg_signals(state="euthymic")

# Calculate PLV
plv_matrix = calculate_plv_matrix(signals)

# Calculate Ψ from multimodal data
calc = MultimodalPsiCalculator()
result = calc.calculate_psi_multimodal(
    eeg_data={"plv_matrix": plv_matrix}
)
print(f"Multimodal Ψ = {result['psi']:.4f}")

# Concurrent EEG-fMRI Analysis (v2.0.0)
from data.synthetic.generate_data import generate_concurrent_eeg_fmri_data

concurrent_data = generate_concurrent_eeg_fmri_data(state="euthymic")
eeg_fmri_result = calc.calculate_from_concurrent_eeg_fmri(concurrent_data)
print(f"Concurrent EEG-fMRI Ψ = {eeg_fmri_result['psi']:.4f}")
print(f"Regime: {eeg_fmri_result['bipolar_regime']['regime']}")
```

### Global Sensitivity Analysis (v1.2.0)

```python
from analysis.sensitivity import (
    perform_parameter_sweep,
    identify_tipping_points,
    generate_sensitivity_heatmap,
)

# Run GSA parameter sweep across operators
theta_vals, gamma_vals, psi_grid, d_theta, d_gamma, d_delta, d_lambda = (
    perform_parameter_sweep(resolution=20, n_mc_samples=50)
)

# Identify tipping points where Psi approaches 0
tipping_points = identify_tipping_points(psi_grid, threshold=0.05)

# Generate sensitivity heatmap visualization
sensitivity_grid = (d_theta**2 + d_gamma**2 + d_delta**2 + d_lambda**2) ** 0.5
generate_sensitivity_heatmap(
    theta_vals=theta_vals,
    gamma_vals=gamma_vals,
    sensitivity_grid=sensitivity_grid,
    tipping_points=tipping_points,
    output_path="docs/figures/sensitivity_heatmap.png",
)
```

### Examples

See `examples/` directory for complete workflows:
- `quickstart.py` - 5-minute introduction
- `custom_simulation.py` - Advanced simulations
- `full_analysis.py` - Multimodal integration
- `eeg_fmri_analysis.py` - Concurrent EEG-fMRI preprocessing, synchronization, and regime stratification

---

## Testing

The framework includes comprehensive tests:

```bash
# Run all tests
pytest tests/

# Run with coverage
pytest tests/ --cov=simulations --cov=analysis

# Run specific test file
pytest tests/test_operators.py -v
```

**Current Status**: 65 tests passing
- 27 operator tests
- 19 simulation tests
- 19 concurrent EEG-fMRI & multimodal integration tests

---

## Computational Modeling

The repository includes:
- Core Ψ function implementation
- Four mathematical operators (Γ, Θ, Δ, Λ)
- Bipolar episode simulations
- Perturbation and recovery models
- Multimodal biomarker integration (EEG, fMRI)
- Synthetic data generation
- Visualization tools
- Validation and sensitivity analyses

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
├── setup.py                           # Package setup
├── setup.cfg                          # Setup configuration
├── pyproject.toml                     # Modern Python project config
├── requirements.txt                   # Core dependencies
│
├── docs/                              # Documentation
│   ├── CI.md                          # CI/CD documentation
│   ├── CI_SETUP_COMPLETE.md           # CI configuration notes
│   │
│   ├── theoretical-framework/         # Theory & mathematical foundations
│   │   ├── 02-neuro-coherence-function.md
│   │   └── 03-operators.md
│   │   └── SNCM.md
│   │   └── LAYMANS_EXPLANATION.md
│   │ 
│   ├── summaries/                     # Analysis & summary documents
│   │   ├── AI_PERSPECTIVE_ANALYSIS.md # AI analysis of framework
│   │   ├── FINDINGS_SUMMARY.md        # Repository findings
│   │   ├── IMPLEMENTATION_SUMMARY.md  # Implementation status
│   │   ├── READING_GUIDE.md           # Guide to understanding the repo
│   │   └── WORKFLOW_SUMMARY.md        # Workflow documentation
│   │
│   └── figures/                       # Generated visualizations
│       ├── eeg_fmri_integration.png
│       ├── longitudinal_analysis.png
│       ├── multimodal_comparison.png
│       ├── operator_correlations.png
│       ├── parameter_sensitivity.png
│       ├── perturbation_experiment.png
│       ├── quickstart_results.png
│       ├── recovery_comparison.png
│       └── sensitivity_heatmap.png
│
├── simulations/                       # Computational Models
│   └── core/                          # Core implementations
│       ├── __init__.py
│       ├── neuro_coherence.py        # Ψ function
│       ├── operators.py              # Γ, Θ, Δ, Λ operators
│       └── utils.py                  # Utility functions
│
├── analysis/                          # Data Analysis Tools
│   ├── __init__.py
│   │
│   ├── eeg/                           # EEG analysis
│   │   ├── __init__.py
│   │   ├── phase_locking.py          # PLV calculations
│   │   ├── coherence_metrics.py
│   │   ├── oscillatory_analysis.py
│   │   └── preprocessing.py
│   │
│   ├── fmri/                          # fMRI analysis
│   │   ├── __init__.py
│   │   ├── connectivity.py
│   │   └── network_metrics.py
│   │
│   ├── eeg_fmri/                      # Concurrent EEG-fMRI integration (v2.0.0)
│   │   ├── __init__.py
│   │   ├── processor.py              # ConcurrentEEGFMRIProcessor
│   │   ├── preprocessing.py          # AAS & OBS/PCA GA/BCG artifact removal
│   │   └── synchronization.py        # Spatiotemporal Lambda, Delta_GR, & regime classification
│   │
│   ├── integration/                   # Multimodal integration
│   │   ├── __init__.py
│   │   └── multimodal_fusion.py      # Multimodal data fusion
│   │
│   └── sensitivity.py                 # Global sensitivity analysis (v1.2.0)
│
├── data/                              # Data Resources
│   ├── README.md
│   └── synthetic/                     # Generated datasets
│       └── generate_data.py          # Data generation scripts
│
├── tests/                             # Testing Suite
│   ├── __init__.py
│   ├── test_operators.py             # Operator tests
│   ├── test_simulations.py           # Simulation tests
│   └── test_eeg_fmri.py              # Concurrent EEG-fMRI tests
│
├── examples/                          # Usage Examples
│   ├── README.md
│   ├── quickstart.py                 # 5-minute demo
│   ├── full_analysis.py              # Complete workflow
│   ├── custom_simulation.py          # Customization guide
│   └── eeg_fmri_analysis.py          # Concurrent EEG-fMRI workflow
│
└── .github/                           # GitHub automation
    └── workflows/
        └── ci.yml                    # Continuous integration
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

(Generated diagrams are stored in `docs/figures/`.)

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

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## Closing

> *“Not to impose stability through suppression, but to teach the system to stabilize itself.”*

**Open Science • Reproducible Research • Responsible Development**
