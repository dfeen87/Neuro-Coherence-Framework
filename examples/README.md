# Examples

This directory contains usage examples for the Neuro-Coherence Framework.

## Quick Start (`quickstart.py`)

**Duration**: ~5 minutes  
**Prerequisites**: Basic Python knowledge

Demonstrates:
- Calculating individual operators (Γ, Θ, Δ, Λ)
- Computing Ψ from operators
- Simulating bipolar episodes (manic, depressive, euthymic)
- Recovery dynamics
- Basic visualization

**Run:**
```bash
python quickstart.py
```

**Output:**
- Console output with Ψ values
- Figure: `quickstart_results.png`

---

## Custom Simulation (`custom_simulation.py`)

**Duration**: ~10 minutes  
**Prerequisites**: Understanding of operators

Demonstrates:
- Parameter customization
- Time-series analysis
- Perturbation experiments
- Parameter sensitivity sweeps
- Advanced visualization

**Run:**
```bash
python custom_simulation.py
```

---

## Full Analysis (`full_analysis.py`)

**Duration**: ~15 minutes  
**Prerequisites**: Multimodal data concepts

Demonstrates:
- Synthetic EEG data generation
- Synthetic fMRI data generation
- Multimodal Ψ calculation
- Integration workflow
- Publication-quality figures

**Run:**
```bash
python full_analysis.py
```

---

## Usage Patterns

### 1. Single Ψ Calculation

```python
from simulations.core import NeuroCoherence, Operators

nc = NeuroCoherence()

gamma = Operators.adaptive_gain(plasticity=0.8)
theta = Operators.thermodynamic_stability(homeostasis=0.9)
delta = Operators.connectivity_variance(sync_variance=0.3)
lambda_op = Operators.spatiotemporal_coherence(phase_alignment=0.85)

psi = nc.calculate(gamma, theta, delta, lambda_op)
print(f"Ψ = {psi.psi:.4f}")
```

### 2. Time Series Simulation

```python
trajectory = nc.simulate_bipolar_episode(
    duration=1000,
    episode_type="manic",
    dt=0.1
)

import matplotlib.pyplot as plt
plt.plot(trajectory["time"], trajectory["psi"])
plt.xlabel("Time")
plt.ylabel("Ψ")
plt.show()
```

### 3. Multimodal Analysis

```python
from analysis.integration import MultimodalPsiCalculator
from data.synthetic import generate_data

# Generate synthetic data
time, eeg_signals = generate_data.generate_eeg_signals(state="euthymic")

# Calculate PLV
from analysis.eeg import calculate_plv_matrix
plv_matrix = calculate_plv_matrix(eeg_signals)

# Calculate Ψ
calc = MultimodalPsiCalculator()
result = calc.calculate_psi_multimodal(
    eeg_data={"plv_matrix": plv_matrix}
)

print(f"Multimodal Ψ = {result['psi']:.4f}")
```

### 4. Parameter Sweep

```python
import numpy as np

param_range = np.linspace(0.2, 1.0, 20)
results = nc.run_parameter_sweep(
    param_name="plasticity",
    param_range=param_range,
    fixed_params={
        "responsiveness": 0.5,
        "homeostasis": 0.9,
        "sync_variance": 0.3,
        "phase_alignment": 0.85
    }
)

plt.plot(results["param_values"], results["psi_values"])
plt.xlabel("Plasticity")
plt.ylabel("Ψ")
plt.show()
```

---

## Data Files

Examples may generate output files:
- `*.png`: Figures
- `*.npz`: Saved simulation results
- `*.csv`: Tabular data exports

These are excluded from version control via `.gitignore`.

---

## Customization

All examples can be modified to:
- Change parameter values
- Adjust simulation duration
- Modify visualization styles
- Export different data formats

See inline comments in each script for customization points.

---

## Troubleshooting

### Import Errors

If you see `ModuleNotFoundError`, ensure the package is installed:
```bash
pip install -e .
```

### Missing Dependencies

Install optional visualization dependencies:
```bash
pip install matplotlib plotly
```

### Figure Display

On headless systems, figures won't display interactively but will still save to files.

---

## Next Steps

After running examples:
1. Review `docs/` for theoretical background
2. Explore `tests/` for validation examples
3. Check `simulations/notebooks/` for interactive tutorials (if available)
4. Read source code in `simulations/core/` for implementation details
