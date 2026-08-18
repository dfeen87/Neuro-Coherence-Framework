"""Synthetic data generation for Neuro-Coherence Framework."""

from typing import Tuple
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


def _canonical_hrf(
    t: np.ndarray, delay: float = 6.0, undershoot: float = 16.0
) -> np.ndarray:
    """Standard double-gamma hemodynamic response function (HRF)."""
    from scipy.stats import gamma

    peak = gamma.pdf(t, delay)
    undershoot_peak = gamma.pdf(t, undershoot)
    hrf = peak - 0.16 * undershoot_peak
    norm = np.max(hrf)
    return hrf / norm if norm > 0 else hrf


def generate_concurrent_eeg_fmri_data(
    n_eeg_channels: int = 19,
    n_rois: int = 12,
    duration_sec: float = 120.0,
    fs_eeg: float = 250.0,
    tr_fmri: float = 2.0,
    state: str = "euthymic",
    add_gradient_artifact: bool = True,
    add_bcg_artifact: bool = True,
    add_motion_artifact: bool = True,
    random_seed: int = 42,
) -> dict:
    """
    Generate synthetic concurrent EEG-fMRI dataset with realistic scanner artifacts
    and neural coupling configured for bipolar disorder states.

    Args:
        n_eeg_channels: Number of EEG channels.
        n_rois: Number of fMRI ROIs.
        duration_sec: Total duration of recording in seconds.
        fs_eeg: EEG sampling rate in Hz.
        tr_fmri: fMRI repetition time (TR) in seconds.
        state: Clinical state ("euthymic", "manic", or "depressive").
        add_gradient_artifact: Whether to add MRI gradient switching artifacts.
        add_bcg_artifact: Whether to add Ballistocardiogram (BCG) artifacts.
        add_motion_artifact: Whether to add motion-related transient artifacts.
        random_seed: Random seed for reproducibility.

    Returns:
        Dictionary containing clean and corrupted EEG/fMRI data, ECG, triggers, and ground truth.
    """
    rng = np.random.RandomState(random_seed)

    n_eeg_samples = int(np.round(duration_sec * fs_eeg))
    n_tr = int(np.round(duration_sec / tr_fmri))

    time_eeg = np.arange(n_eeg_samples) / fs_eeg
    time_fmri = np.arange(n_tr) * tr_fmri

    # 1. State-dependent parameters
    if state == "euthymic":
        coupling_strength = 0.8
        eeg_coherence = 0.85
        expected_lambda = 0.82
        expected_delta_gr = 0.20
    elif state == "manic":
        coupling_strength = 0.4
        eeg_coherence = 0.45
        expected_lambda = 0.42
        expected_delta_gr = 0.68
    else:  # depressive
        coupling_strength = 0.25
        eeg_coherence = 0.35
        expected_lambda = 0.25
        expected_delta_gr = 0.55

    # 2. Low-frequency neural driver (0.01 - 0.1 Hz) for network synchronization
    t_hrf = np.linspace(0, 30, int(30 * fs_eeg))
    hrf = _canonical_hrf(t_hrf)

    # Global low-frequency driver
    global_driver = np.sin(2 * np.pi * 0.03 * time_eeg)

    # 3 Networks: DMN (0..n_rois//3), SN (n_rois//3..2*n_rois//3), CEN (2*n_rois//3..n_rois)
    n_networks = 3
    rois_per_network = max(1, n_rois // n_networks)

    net_drivers_eeg = np.zeros((n_networks, n_eeg_samples))
    for net_idx in range(n_networks):
        freq = 0.03
        base_driver = np.sin(2 * np.pi * freq * time_eeg + net_idx * np.pi / 6)
        if state == "euthymic":
            net_drivers_eeg[net_idx] = global_driver
        elif state == "manic":
            mod = 1.0 + 1.5 * np.sin(2 * np.pi * 0.1 * time_eeg + net_idx)
            net_drivers_eeg[net_idx] = base_driver * mod
        else:  # depressive
            net_drivers_eeg[net_idx] = 0.3 * base_driver

    # 3. Clean fMRI construction
    fmri_clean = np.zeros((n_rois, n_tr))

    for roi_idx in range(n_rois):
        net_idx = min(roi_idx // rois_per_network, n_networks - 1)
        driver_eeg = net_drivers_eeg[net_idx]

        # Convolve EEG driver with HRF and downsample to TRs
        bold_conv = np.convolve(driver_eeg, hrf, mode="full")[:n_eeg_samples]
        bold_tr_indices = np.clip(
            np.round(time_fmri * fs_eeg).astype(int), 0, n_eeg_samples - 1
        )
        bold_signal = bold_conv[bold_tr_indices]

        # Add ROI-specific variance and state-dependent temporal instability
        if state == "manic":
            cross_mod = 1.5 * np.sin(2.0 * np.pi * 0.03 * time_fmri + roi_idx * np.pi / 3.0)
            fmri_clean[roi_idx] = (
                bold_signal + cross_mod * bold_signal + 0.02 * rng.randn(n_tr)
            )
        elif state == "depressive":
            fmri_clean[roi_idx] = (
                0.3 * bold_signal + 0.02 * rng.randn(n_tr)
            )
        else:  # euthymic
            fmri_clean[roi_idx] = bold_signal + 0.05 * rng.randn(n_tr)

    # 4. Clean EEG construction
    alpha_freq = 10.0  # Hz
    theta_freq = 6.0  # Hz
    eeg_clean = np.zeros((n_eeg_channels, n_eeg_samples))

    common_signal = np.sin(2 * np.pi * alpha_freq * time_eeg) + 0.5 * np.sin(
        2 * np.pi * theta_freq * time_eeg
    )

    for ch in range(n_eeg_channels):
        net_idx = ch % n_networks
        modulating_driver = net_drivers_eeg[net_idx]

        if state == "euthymic":
            p_noise = 0.05 * rng.randn(n_eeg_samples)
            carrier_alpha = np.sin(2 * np.pi * alpha_freq * time_eeg + p_noise)
            carrier_theta = np.sin(2 * np.pi * theta_freq * time_eeg + p_noise)
            indep_signal = carrier_alpha + 0.5 * carrier_theta
            ch_signal = 0.85 * common_signal + 0.15 * indep_signal
        elif state == "manic":
            p_noise = 0.4 * np.sin(2 * np.pi * 0.1 * time_eeg + ch)
            carrier_alpha = np.sin(2 * np.pi * alpha_freq * time_eeg + p_noise)
            carrier_theta = np.sin(2 * np.pi * theta_freq * time_eeg + p_noise)
            indep_signal = carrier_alpha + 0.5 * carrier_theta
            envelope = 1.0 + coupling_strength * modulating_driver
            ch_signal = 0.50 * common_signal + 0.50 * (indep_signal * envelope)
        else:  # depressive
            p_noise = rng.uniform(-np.pi, np.pi, n_eeg_samples)
            carrier_alpha = np.sin(2 * np.pi * alpha_freq * time_eeg + p_noise)
            carrier_theta = np.sin(2 * np.pi * theta_freq * time_eeg + p_noise)
            indep_signal = carrier_alpha + 0.5 * carrier_theta
            ch_signal = 0.10 * common_signal + 0.90 * indep_signal

        eeg_clean[ch] = ch_signal + 0.02 * rng.randn(n_eeg_samples)

    # 5. Generate Triggers and ECG Signal
    # TR Triggers every tr_fmri seconds
    tr_trigger_indices = np.round(np.arange(0, duration_sec, tr_fmri) * fs_eeg).astype(
        int
    )
    tr_trigger_indices = tr_trigger_indices[tr_trigger_indices < n_eeg_samples]

    # ECG generation (R-peaks every ~0.8s = 75 bpm)
    heart_rate_bpm = 75.0
    rr_interval_sec = 60.0 / heart_rate_bpm
    r_peak_times = np.arange(0.2, duration_sec, rr_interval_sec)
    r_peak_indices = np.round(r_peak_times * fs_eeg).astype(int)
    r_peak_indices = r_peak_indices[r_peak_indices < n_eeg_samples]

    ecg_signal = np.zeros(n_eeg_samples)
    for idx in r_peak_indices:
        # Standard synthetic QRS complex
        qrs_window = np.arange(-int(0.05 * fs_eeg), int(0.05 * fs_eeg) + 1)
        valid_mask = (idx + qrs_window >= 0) & (idx + qrs_window < n_eeg_samples)
        valid_win = qrs_window[valid_mask]
        ecg_signal[idx + valid_win] += 2.0 * np.exp(
            -0.5 * (valid_win / (0.01 * fs_eeg)) ** 2
        )
    ecg_signal += 0.05 * rng.randn(n_eeg_samples)

    # 6. Artifact Syntheses
    eeg_corrupted = eeg_clean.copy()
    fmri_corrupted = fmri_clean.copy()

    ga_artifact = np.zeros((n_eeg_channels, n_eeg_samples))
    bcg_artifact = np.zeros((n_eeg_channels, n_eeg_samples))
    motion_artifact = np.zeros((n_eeg_channels, n_eeg_samples))

    # Gradient Artifact (GA)
    if add_gradient_artifact:
        # Repeating high-frequency slice/volume gradient pulse
        slice_period_samples = int(0.05 * fs_eeg)  # Slice every 50ms
        pulse_shape = np.sin(
            2 * np.pi * 50.0 * np.arange(slice_period_samples) / fs_eeg
        )
        for trig in tr_trigger_indices:
            for s in range(0, int(tr_fmri * fs_eeg), slice_period_samples):
                start = trig + s
                end = min(start + slice_period_samples, n_eeg_samples)
                if start < n_eeg_samples:
                    pulse_len = end - start
                    ga_pulse = 15.0 * pulse_shape[:pulse_len]
                    for ch in range(n_eeg_channels):
                        chan_weight = 1.0 + 0.2 * np.sin(ch)
                        ga_artifact[ch, start:end] += chan_weight * ga_pulse

    # BCG Artifact
    if add_bcg_artifact:
        bcg_template_len = int(0.4 * fs_eeg)
        t_bcg = np.linspace(0, 1, bcg_template_len)
        bcg_shape = np.sin(2 * np.pi * 3 * t_bcg) * np.exp(-3 * t_bcg)
        for r_idx in r_peak_indices:
            start = r_idx + int(0.1 * fs_eeg)  # BCG delay ~100ms after R-peak
            end = min(start + bcg_template_len, n_eeg_samples)
            if start < n_eeg_samples:
                bcg_len = end - start
                for ch in range(n_eeg_channels):
                    chan_weight = 3.0 * np.cos(ch * np.pi / n_eeg_channels)
                    bcg_artifact[ch, start:end] += chan_weight * bcg_shape[:bcg_len]

    # Motion Artifact
    if add_motion_artifact:
        n_motion_events = int(duration_sec / 30.0) + 1
        for _ in range(n_motion_events):
            m_time = rng.uniform(5.0, duration_sec - 5.0)
            m_idx = int(m_time * fs_eeg)
            m_duration = int(rng.uniform(0.5, 1.5) * fs_eeg)
            m_end = min(m_idx + m_duration, n_eeg_samples)
            m_shape = 10.0 * np.sin(np.pi * np.linspace(0, 1, m_end - m_idx))
            for ch in range(n_eeg_channels):
                motion_artifact[ch, m_idx:m_end] += rng.uniform(-1, 1) * m_shape

            # Add corresponding motion artifact to fMRI
            m_tr_idx = int(m_time / tr_fmri)
            if m_tr_idx < n_tr:
                fmri_corrupted[:, m_tr_idx : min(m_tr_idx + 2, n_tr)] += rng.uniform(
                    1.5, 3.0
                )

    eeg_corrupted += ga_artifact + bcg_artifact + motion_artifact

    return {
        "eeg_clean": eeg_clean,
        "eeg_corrupted": eeg_corrupted,
        "time_eeg": time_eeg,
        "fs_eeg": fs_eeg,
        "fmri_clean": fmri_clean,
        "fmri_corrupted": fmri_corrupted,
        "time_fmri": time_fmri,
        "tr_fmri": tr_fmri,
        "ecg_signal": ecg_signal,
        "r_peak_indices": r_peak_indices,
        "tr_trigger_indices": tr_trigger_indices,
        "ground_truth": {
            "state": state,
            "expected_lambda": expected_lambda,
            "expected_delta_gr": expected_delta_gr,
            "ga_artifact": ga_artifact,
            "bcg_artifact": bcg_artifact,
            "motion_artifact": motion_artifact,
        },
    }
