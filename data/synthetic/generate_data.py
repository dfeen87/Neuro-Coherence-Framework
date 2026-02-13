"""Synthetic data generation for Neuro-Coherence Framework."""

from typing import Tuple, Optional
import numpy as np


def generate_eeg_signals(
    n_channels: int = 19,
    duration: int = 1000,
    fs: float = 250.0,
    noise_level: float = 0.1,
    state: str = "euthymic",
) -> Tuple[np.ndarray, np.ndarray]:
    """
    Generate synthetic EEG signals.

    Args:
        n_channels: Number of EEG channels
        duration: Duration in samples
        fs: Sampling frequency (Hz)
        noise_level: Noise level (0 to 1)
        state: Brain state ("euthymic", "manic", "depressive")

    Returns:
        Tuple of (time_array, signals_array)
    """
    time = np.arange(duration) / fs
    signals = np.zeros((n_channels, duration))

    # Define frequency bands and amplitudes based on state
    if state == "euthymic":
        # Balanced oscillations
        alpha_amp = 10.0
        theta_amp = 5.0
        beta_amp = 3.0
        coherence_factor = 0.8
    elif state == "manic":
        # Increased high-frequency, reduced coherence
        alpha_amp = 5.0
        theta_amp = 8.0
        beta_amp = 8.0
        coherence_factor = 0.4
    else:  # depressive
        # Reduced amplitude, low coherence
        alpha_amp = 3.0
        theta_amp = 4.0
        beta_amp = 2.0
        coherence_factor = 0.5

    # Generate base oscillations
    alpha_freq = 10.0  # Hz
    theta_freq = 6.0  # Hz
    beta_freq = 20.0  # Hz

    # Common signal component (for coherence)
    common_signal = (
        alpha_amp * np.sin(2 * np.pi * alpha_freq * time)
        + theta_amp * np.sin(2 * np.pi * theta_freq * time)
        + beta_amp * np.sin(2 * np.pi * beta_freq * time)
    )

    # Generate signals for each channel
    for i in range(n_channels):
        # Mix common signal with independent noise
        phase_shift = 2 * np.pi * i / n_channels

        independent_signal = (
            alpha_amp * np.sin(2 * np.pi * alpha_freq * time + phase_shift)
            + theta_amp * np.sin(2 * np.pi * theta_freq * time + phase_shift * 0.5)
            + beta_amp * np.sin(2 * np.pi * beta_freq * time + phase_shift * 1.5)
        )

        # Mix coherent and independent components
        signals[i] = (
            coherence_factor * common_signal
            + (1 - coherence_factor) * independent_signal
        )

        # Add noise
        signals[i] += noise_level * np.random.randn(duration)

    return time, signals


def generate_fmri_timeseries(
    n_rois: int = 90, duration: int = 200, tr: float = 2.0, state: str = "euthymic"
) -> Tuple[np.ndarray, np.ndarray]:
    """
    Generate synthetic fMRI timeseries.

    Args:
        n_rois: Number of ROIs
        duration: Duration in TRs
        tr: Repetition time (seconds)
        state: Brain state

    Returns:
        Tuple of (time_array, timeseries_array)
    """
    time = np.arange(duration) * tr
    timeseries = np.zeros((n_rois, duration))

    # Define network structure (simplified)
    n_networks = 3  # DMN, SN, CEN
    rois_per_network = n_rois // n_networks

    # Network connectivity parameters based on state
    if state == "euthymic":
        within_network_strength = 0.7
        between_network_strength = 0.3
    elif state == "manic":
        within_network_strength = 0.4
        between_network_strength = 0.6  # Increased cross-talk
    else:  # depressive
        within_network_strength = 0.5
        between_network_strength = 0.2

    # Generate network signals
    network_signals = np.zeros((n_networks, duration))
    for net in range(n_networks):
        # Low-frequency oscillation (typical fMRI)
        freq = 0.01 + 0.05 * net  # Hz
        network_signals[net] = np.sin(2 * np.pi * freq * time)

    # Generate ROI timeseries
    for roi in range(n_rois):
        network_id = roi // rois_per_network
        if network_id >= n_networks:
            network_id = n_networks - 1

        # Within-network component
        within_component = within_network_strength * network_signals[network_id]

        # Between-network components
        between_component = 0
        for other_net in range(n_networks):
            if other_net != network_id:
                between_component += (
                    between_network_strength * network_signals[other_net]
                )
        between_component /= n_networks - 1

        # Independent noise
        noise = 0.3 * np.random.randn(duration)

        timeseries[roi] = within_component + between_component + noise

    return time, timeseries


def generate_bipolar_trajectory(
    duration: int = 1000,
    n_episodes: int = 3,
    episode_duration: int = 200,
    noise_level: float = 0.05,
) -> dict:
    """
    Generate synthetic bipolar disorder trajectory.

    Args:
        duration: Total duration
        n_episodes: Number of mood episodes
        episode_duration: Duration of each episode
        noise_level: Noise level

    Returns:
        Dictionary with trajectory data
    """
    from simulations.core import NeuroCoherence

    time = np.arange(duration)
    psi_trajectory = np.zeros(duration)
    state_labels = np.zeros(duration, dtype=int)  # 0=euthymic, 1=manic, 2=depressive

    nc = NeuroCoherence()

    # Default euthymic state
    euthymic_baseline = nc.simulate_bipolar_episode(
        duration=duration, episode_type="euthymic"
    )
    psi_trajectory = euthymic_baseline["psi"]

    # Insert episodes
    episode_types = ["manic", "depressive"]
    for i in range(n_episodes):
        # Random start time
        start = np.random.randint(0, duration - episode_duration)
        episode_type = episode_types[i % len(episode_types)]

        # Generate episode
        episode = nc.simulate_bipolar_episode(
            duration=episode_duration, episode_type=episode_type
        )

        # Insert into trajectory
        psi_trajectory[start : start + episode_duration] = episode["psi"]

        # Label
        label = 1 if episode_type == "manic" else 2
        state_labels[start : start + episode_duration] = label

    # Add noise
    psi_trajectory += noise_level * np.random.randn(duration)
    psi_trajectory = np.clip(psi_trajectory, 0, 2)

    return {
        "time": time,
        "psi": psi_trajectory,
        "state_labels": state_labels,
        "n_episodes": n_episodes,
    }


def generate_healthy_controls(
    n_subjects: int = 20, duration: int = 500, variability: float = 0.1
) -> dict:
    """
    Generate synthetic healthy control data.

    Args:
        n_subjects: Number of subjects
        duration: Duration per subject
        variability: Inter-subject variability

    Returns:
        Dictionary with control data
    """
    from simulations.core import NeuroCoherence

    nc = NeuroCoherence()

    trajectories = []
    for subject in range(n_subjects):
        # Vary parameters slightly
        plasticity = 0.8 + variability * np.random.randn()
        homeostasis = 0.9 + variability * np.random.randn()

        # Clip to valid ranges
        plasticity = np.clip(plasticity, 0.5, 1.0)
        homeostasis = np.clip(homeostasis, 0.7, 1.0)

        # Generate trajectory
        trajectory = nc.simulate_bipolar_episode(
            duration=duration, episode_type="euthymic"
        )

        trajectories.append(trajectory["psi"])

    return {
        "trajectories": np.array(trajectories),
        "n_subjects": n_subjects,
        "mean_psi": np.mean(trajectories),
        "std_psi": np.std(trajectories),
    }


def save_synthetic_dataset(filename: str, **data_dict) -> None:
    """
    Save synthetic dataset to file.

    Args:
        filename: Output filename (.npz)
        **data_dict: Data to save
    """
    np.savez_compressed(filename, **data_dict)
    print(f"Saved synthetic dataset to: {filename}")


def load_synthetic_dataset(filename: str) -> dict:
    """
    Load synthetic dataset from file.

    Args:
        filename: Input filename (.npz)

    Returns:
        Dictionary with loaded data
    """
    data = np.load(filename, allow_pickle=True)
    return {key: data[key] for key in data.files}
