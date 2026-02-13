# Operators - Mathematical Definitions

## Overview

The four operators capture distinct biophysical dimensions that together determine systemic coherence.

---

## Γ - Adaptive Gain (Neuroplasticity)

### Mathematical Form

```
Γ(t) = γ₀ · (1 + α · tanh(β · R(t)))
```

Where:
- **γ₀**: Baseline gain coefficient (default: 1.0)
- **α**: Plasticity coefficient (0 to 2)
- **β**: Responsiveness rate (default: 1.0)
- **R(t)**: Responsiveness signal

### Physical Interpretation

Γ models the system's ability to modulate gain in response to perturbations. High plasticity allows rapid adaptation; low plasticity indicates rigidity.

### Biomarker Mapping

**Primary**: PLV recovery after perturbation
- Measure PLV before and after TMS/task
- Recovery rate → plasticity estimate

**Secondary**: Synaptic markers
- BDNF levels
- Glutamate/GABA balance

### Implementation

```python
from simulations.core import Operators

gamma = Operators.adaptive_gain(
    plasticity=0.8,      # Plasticity coefficient
    responsiveness=0.5,  # Responsiveness signal
    baseline_gain=1.0    # Baseline gain
)
```

### Valid Ranges

- **Input**: plasticity ≥ 0, responsiveness: any float
- **Output**: Γ ≥ 0 (typically 0.5 - 2.0)

---

## Θ - Thermodynamic Stability (Metabolic Homeostasis)

### Mathematical Form

```
Θ(E) = exp(-λ · |E - E₀|²)
```

Where:
- **E**: Current metabolic state
- **E₀**: Homeostatic setpoint (default: 1.0)
- **λ**: Stability decay coefficient (default: 1.0)

### Physical Interpretation

Θ quantifies metabolic stability. Deviations from homeostasis reduce stability exponentially, modeling energy crisis vulnerability.

### Biomarker Mapping

**Primary**: Mitochondrial function
- Oxygen consumption rate (OCR)
- ATP production rate
- Lactate levels

**Secondary**: PET imaging
- FDG-PET glucose metabolism
- Regional energy distribution

### Implementation

```python
theta = Operators.thermodynamic_stability(
    homeostasis=0.9,        # Homeostatic balance (0-1)
    atp_production=1.0,     # Optional ATP level
    ocr=1.0,                # Optional OCR
    setpoint=1.0,
    stability_coeff=1.0
)
```

### Valid Ranges

- **Input**: homeostasis ∈ [0, 1], ATP/OCR ≥ 0
- **Output**: Θ ∈ [0, 1]

---

## Δ_GR - Generalized Regional Differential (Network Variance)

### Mathematical Form

```
Δ_GR = σ²(C) / (1 + σ²(C))
```

Where:
- **σ²(C)**: Variance of connectivity across networks
- Sigmoid normalization ensures [0, 1] range

### Physical Interpretation

Δ represents the **penalty** for network desynchronization. High variance indicates fragmented network dynamics.

### Biomarker Mapping

**Primary**: fMRI connectivity
- Variance across DMN-SN-CEN
- Dynamic connectivity fluctuations

**Secondary**: Graph metrics
- Network modularity changes
- Hub disruption indices

### Implementation

```python
delta = Operators.connectivity_variance(
    sync_variance=0.3,           # Network synchronization variance
    network_metrics={             # Optional network-specific values
        "DMN": 0.7,
        "SN": 0.65,
        "CEN": 0.68
    },
    normalization="sigmoid"       # "sigmoid" or "linear"
)
```

### Valid Ranges

- **Input**: sync_variance ≥ 0
- **Output**: Δ ∈ [0, 1]

---

## Λ - Spatiotemporal Coherence Density

### Mathematical Form

```
Λ(r,t) = ⟨PLV(r,t)⟩ · (1 - σ²(GPLI))
```

Where:
- **PLV(r,t)**: Phase Locking Value across space and time
- **GPLI**: Generalized Phase Lag Index
- **σ²**: Variance operator

### Physical Interpretation

Λ quantifies phase-aligned information flow. High values indicate synchronized oscillations across brain regions.

### Biomarker Mapping

**Primary**: High-density EEG
- PLV across electrode pairs
- GPLI for directed connectivity
- Cross-frequency coupling

**Secondary**: MEG
- Phase coherence analysis
- Source-space connectivity

### Implementation

```python
lambda_op = Operators.spatiotemporal_coherence(
    phase_alignment=0.85,        # Phase alignment metric (0-1)
    plv=0.9,                     # Optional PLV array
    gpli=0.8,                    # Optional GPLI array
    coherence_threshold=0.1      # Minimum coherence threshold
)
```

### Valid Ranges

- **Input**: phase_alignment ∈ [0, 1], PLV ∈ [0, 1], GPLI ∈ [0, 1]
- **Output**: Λ ∈ [0, 1]

---

## Operator Interactions

### Multiplicative Coupling

The operators interact multiplicatively in Ψ:

```
Ψ ∝ Γ · Θ · (1 - Δ) · Λ
```

**Implications**:
1. **No compensation**: Low value in any operator drastically reduces Ψ
2. **Balanced optimization**: All domains must improve together
3. **Clinical relevance**: Multi-target interventions required

### Independence

While operators are mathematically independent, they may be **physiologically coupled**:

- **Θ ↔ Γ**: Energy availability affects plasticity
- **Δ ↔ Λ**: Network structure influences phase coherence
- **Γ ↔ Λ**: Plasticity may enhance coherence

These couplings are **emergent properties**, not assumptions of the model.

---

## Numerical Stability

All operators include safeguards:
- Input validation
- Range clipping
- Division protection
- Saturation limits

See `simulations/core/operators.py` for implementation details.
