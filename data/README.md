# Data Directory

This directory contains synthetic datasets, literature-extracted values, and standard templates.

## Structure

```
data/
├── synthetic/          # Generated datasets
│   └── generate_data.py
├── literature/         # Extracted values from research
└── templates/          # Standard atlases and montages
```

## Synthetic Data Generation

### EEG Signals

Generate multi-channel EEG with realistic oscillations:

```python
from data.synthetic.generate_data import generate_eeg_signals

time, signals = generate_eeg_signals(
    n_channels=19,      # Standard 10-20 system
    duration=1000,      # Samples
    fs=250.0,          # Sampling frequency (Hz)
    noise_level=0.1,   # Noise level
    state="euthymic"   # "euthymic", "manic", or "depressive"
)
```

**Output**:
- `time`: Time array (samples / fs)
- `signals`: Array (n_channels × duration)

**Characteristics by state**:
- **Euthymic**: Balanced alpha/theta/beta, high coherence
- **Manic**: Elevated beta, reduced coherence
- **Depressive**: Reduced amplitudes, low coherence

### fMRI Timeseries

Generate multi-ROI fMRI BOLD signals:

```python
from data.synthetic.generate_data import generate_fmri_timeseries

time, timeseries = generate_fmri_timeseries(
    n_rois=90,         # AAL atlas ROIs
    duration=200,      # TRs
    tr=2.0,           # Repetition time (seconds)
    state="euthymic"
)
```

**Output**:
- `time`: Time array (TRs × tr)
- `timeseries`: Array (n_rois × duration)

**Network structure**:
- 3 simplified networks (DMN, SN, CEN)
- Within-network and between-network connectivity varies by state

### Bipolar Trajectories

Generate longitudinal Ψ trajectories with episodes:

```python
from data.synthetic.generate_data import generate_bipolar_trajectory

trajectory = generate_bipolar_trajectory(
    duration=1000,
    n_episodes=3,
    episode_duration=200,
    noise_level=0.05
)
```

**Output dictionary**:
- `time`: Time array
- `psi`: Ψ trajectory
- `state_labels`: Episode labels (0=euthymic, 1=manic, 2=depressive)
- `n_episodes`: Number of episodes

### Healthy Controls

Generate control group data:

```python
from data.synthetic.generate_data import generate_healthy_controls

controls = generate_healthy_controls(
    n_subjects=20,
    duration=500,
    variability=0.1
)
```

**Output dictionary**:
- `trajectories`: Array (n_subjects × duration)
- `n_subjects`: Number of subjects
- `mean_psi`: Mean Ψ across subjects
- `std_psi`: Standard deviation

## Saving and Loading

### Save Dataset

```python
from data.synthetic.generate_data import save_synthetic_dataset

save_synthetic_dataset(
    filename="my_dataset.npz",
    eeg_signals=signals,
    fmri_timeseries=timeseries,
    psi_trajectory=trajectory
)
```

### Load Dataset

```python
from data.synthetic.generate_data import load_synthetic_dataset

data = load_synthetic_dataset("my_dataset.npz")
signals = data["eeg_signals"]
```

## Data Format

All synthetic data uses NumPy arrays saved in compressed `.npz` format:
- Efficient storage
- Fast loading
- Platform-independent
- Easy integration with analysis tools

## Literature Data

The `literature/` directory would contain:
- Extracted biomarker values from published studies
- Meta-analysis results
- Normative ranges for operators

**Example structure** (not yet implemented):
```csv
study,population,gamma_mean,theta_mean,delta_mean,lambda_mean
Smith2020,Euthymic,0.85,0.90,0.25,0.80
Jones2021,Manic,1.15,0.65,0.55,0.45
```

## Templates

The `templates/` directory would contain:
- Standard EEG montages (10-20, 10-10)
- Brain atlases (AAL, Harvard-Oxford)
- Network definitions (DMN, SN, CEN ROIs)

**Example** (not yet implemented):
```json
{
  "name": "Standard_1020",
  "channels": ["Fp1", "Fp2", "F3", "F4", ...],
  "positions": [[x1, y1, z1], [x2, y2, z2], ...]
}
```

## Best Practices

1. **Reproducibility**: Set random seeds for reproducible generation
2. **Validation**: Check generated data statistics match expectations
3. **Documentation**: Document parameter choices in metadata
4. **Storage**: Use compressed formats for large datasets
5. **Naming**: Use descriptive filenames with dates/versions

## Example Workflow

```python
import numpy as np
from data.synthetic import generate_data

# Set seed for reproducibility
np.random.seed(42)

# Generate complete dataset
time_eeg, eeg_signals = generate_data.generate_eeg_signals(
    n_channels=19, duration=5000, state="euthymic"
)

time_fmri, fmri_timeseries = generate_data.generate_fmri_timeseries(
    n_rois=90, duration=300, state="euthymic"
)

trajectory = generate_data.generate_bipolar_trajectory(
    duration=2000, n_episodes=5
)

# Save
generate_data.save_synthetic_dataset(
    filename="dataset_euthymic_v1.npz",
    eeg_time=time_eeg,
    eeg_signals=eeg_signals,
    fmri_time=time_fmri,
    fmri_timeseries=fmri_timeseries,
    trajectory=trajectory["psi"],
    state_labels=trajectory["state_labels"]
)

print("Dataset generated and saved!")
```

## Notes

- Synthetic data is for **validation and demonstration only**
- Real data requires proper preprocessing and quality control
- See `analysis/` modules for processing real measurements
- Consult ethics guidelines for human data handling
