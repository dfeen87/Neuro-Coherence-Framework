# Copyright (c) 2026 Don Michael Feeney Jr.
# MIT License - see LICENSE for details.

"""
EEG-in-MRI preprocessing and artifact correction module.

Provides Average Artifact Subtraction (AAS) and Optimal Basis Set (OBS/PCA)
for gradient and ballistocardiogram (BCG) artifact removal, as well as
motion detection and noise filtering.
"""

from typing import Dict, Optional, Any
import numpy as np
from scipy.signal import butter, filtfilt, find_peaks


def detect_ecg_rpeaks(ecg_signal: np.ndarray, fs: float) -> np.ndarray:
    """
    Detect R-peaks in ECG signal using peak detection.

    Args:
        ecg_signal: 1D ECG signal array.
        fs: Sampling frequency in Hz.

    Returns:
        Array of sample indices corresponding to R-peaks.
    """
    min_distance = int(0.4 * fs)  # Minimum 400ms between R-peaks (max 150 bpm)
    threshold = np.mean(ecg_signal) + 1.0 * np.std(ecg_signal)
    peaks, _ = find_peaks(ecg_signal, height=threshold, distance=min_distance)
    return peaks


def remove_gradient_artifacts(
    eeg_signals: np.ndarray,
    fs: float,
    tr: float,
    tr_trigger_indices: Optional[np.ndarray] = None,
    n_pca_components: int = 3,
) -> Dict[str, Any]:
    """
    Remove MRI Gradient Artifacts (GA) using Average Artifact Subtraction (AAS)
    augmented with Optimal Basis Sets (OBS/PCA).

    Args:
        eeg_signals: EEG signals array of shape (n_channels, n_samples).
        fs: EEG sampling rate in Hz.
        tr: Repetition time (TR) in seconds.
        tr_trigger_indices: Optional indices of TR slice/volume triggers.
        n_pca_components: Number of PCA components for residual OBS removal.

    Returns:
        Dictionary containing cleaned EEG signals, estimated artifact, and metrics.
    """
    n_channels, n_samples = eeg_signals.shape
    window_len = int(np.round(tr * fs))

    if tr_trigger_indices is None or len(tr_trigger_indices) == 0:
        tr_trigger_indices = np.arange(0, n_samples - window_len + 1, window_len)

    n_triggers = len(tr_trigger_indices)
    cleaned_signals = eeg_signals.copy()
    estimated_artifact = np.zeros_like(eeg_signals)

    if n_triggers < 2:
        return {
            "cleaned_signals": cleaned_signals,
            "estimated_artifact": estimated_artifact,
            "n_triggers": n_triggers,
        }

    # 1. Average Artifact Subtraction (AAS)
    for ch in range(n_channels):
        epochs = []
        valid_trigs = []
        for trig in tr_trigger_indices:
            if trig + window_len <= n_samples:
                epochs.append(eeg_signals[ch, trig : trig + window_len])
                valid_trigs.append(trig)

        if not epochs:
            continue

        epochs_arr = np.array(epochs)  # (n_triggers, window_len)
        mean_template = np.mean(epochs_arr, axis=0)  # (window_len,)

        # Subtract AAS template
        for trig in valid_trigs:
            cleaned_signals[ch, trig : trig + window_len] -= mean_template
            estimated_artifact[ch, trig : trig + window_len] += mean_template

        # 2. Optimal Basis Set (OBS / PCA residual removal)
        if n_pca_components > 0 and len(epochs_arr) >= n_pca_components:
            residuals = epochs_arr - mean_template
            # SVD on residual matrix
            U, S, Vt = np.linalg.svd(residuals, full_matrices=False)
            obs_basis = Vt[:n_pca_components, :]  # (n_components, window_len)

            for i, trig in enumerate(valid_trigs):
                res_epoch = residuals[i]
                weights = np.dot(obs_basis, res_epoch)
                obs_fit = np.dot(weights, obs_basis)

                cleaned_signals[ch, trig : trig + window_len] -= obs_fit
                estimated_artifact[ch, trig : trig + window_len] += obs_fit

    return {
        "cleaned_signals": cleaned_signals,
        "estimated_artifact": estimated_artifact,
        "n_triggers": n_triggers,
    }


def remove_bcg_artifacts(
    eeg_signals: np.ndarray,
    fs: float,
    r_peak_indices: Optional[np.ndarray] = None,
    ecg_signal: Optional[np.ndarray] = None,
    n_pca_components: int = 3,
) -> Dict[str, Any]:
    """
    Remove Ballistocardiogram (BCG) artifacts using R-peak alignment and
    Optimal Basis Set (OBS/PCA) decomposition.

    Args:
        eeg_signals: EEG signals array of shape (n_channels, n_samples).
        fs: Sampling rate in Hz.
        r_peak_indices: Optional pre-detected R-peak sample indices.
        ecg_signal: Optional 1D ECG array if r_peak_indices not given.
        n_pca_components: Number of PCA components for BCG template.

    Returns:
        Dictionary containing cleaned signals, estimated BCG artifact, and R-peaks.
    """
    n_channels, n_samples = eeg_signals.shape

    if r_peak_indices is None:
        if ecg_signal is not None:
            r_peak_indices = detect_ecg_rpeaks(ecg_signal, fs)
        else:
            # Fallback: estimate from global mean EEG signal
            mean_eeg = np.mean(eeg_signals, axis=0)
            r_peak_indices = detect_ecg_rpeaks(mean_eeg, fs)

    cleaned_signals = eeg_signals.copy()
    estimated_artifact = np.zeros_like(eeg_signals)

    bcg_window_len = int(0.5 * fs)  # 500ms post R-peak window
    valid_peaks = [p for p in r_peak_indices if p + bcg_window_len <= n_samples]

    if len(valid_peaks) < 3:
        return {
            "cleaned_signals": cleaned_signals,
            "estimated_artifact": estimated_artifact,
            "r_peak_indices": r_peak_indices,
        }

    for ch in range(n_channels):
        epochs = [eeg_signals[ch, p : p + bcg_window_len] for p in valid_peaks]
        epochs_arr = np.array(epochs)  # (n_peaks, bcg_window_len)

        # OBS / PCA
        U, S, Vt = np.linalg.svd(epochs_arr, full_matrices=False)
        k = min(n_pca_components, len(S))
        bcg_basis = Vt[:k, :]

        for i, p in enumerate(valid_peaks):
            epoch = epochs_arr[i]
            weights = np.dot(bcg_basis, epoch)
            bcg_fit = np.dot(weights, bcg_basis)

            cleaned_signals[ch, p : p + bcg_window_len] -= bcg_fit
            estimated_artifact[ch, p : p + bcg_window_len] += bcg_fit

    return {
        "cleaned_signals": cleaned_signals,
        "estimated_artifact": estimated_artifact,
        "r_peak_indices": np.array(valid_peaks),
    }


def remove_motion_and_scanner_noise(
    eeg_signals: np.ndarray,
    fs: float,
    motion_threshold: float = 3.5,
    lowcut: float = 0.5,
    highcut: float = 40.0,
) -> Dict[str, Any]:
    """
    Remove motion artifacts and residual scanner high/low frequency noise.

    Args:
        eeg_signals: EEG signals of shape (n_channels, n_samples).
        fs: Sampling rate in Hz.
        motion_threshold: Z-score threshold for motion artifact detection.
        lowcut: Low cutoff frequency for bandpass filter.
        highcut: High cutoff frequency for bandpass filter.

    Returns:
        Dictionary with cleaned signals and motion artifact mask.
    """
    n_channels, n_samples = eeg_signals.shape
    cleaned_signals = eeg_signals.copy()

    # 1. Bandpass filter
    nyq = 0.5 * fs
    b, a = butter(2, [lowcut / nyq, highcut / nyq], btype="band")
    for ch in range(n_channels):
        cleaned_signals[ch] = filtfilt(b, a, cleaned_signals[ch])

    # 2. Motion artifact detection and linear interpolation / despeckling
    motion_mask = np.zeros((n_channels, n_samples), dtype=bool)

    for ch in range(n_channels):
        sig = cleaned_signals[ch]
        z_scores = np.abs((sig - np.mean(sig)) / (np.std(sig) + 1e-8))
        artifacts = z_scores > motion_threshold
        motion_mask[ch] = artifacts

        art_idx = np.where(artifacts)[0]
        good_idx = np.where(~artifacts)[0]

        if 0 < len(art_idx) < n_samples - 2 and len(good_idx) >= 2:
            cleaned_signals[ch, art_idx] = np.interp(art_idx, good_idx, sig[good_idx])

    return {
        "cleaned_signals": cleaned_signals,
        "motion_mask": motion_mask,
    }


def compute_artifact_metrics(
    corrupted_signal: np.ndarray,
    cleaned_signal: np.ndarray,
    clean_ground_truth: Optional[np.ndarray] = None,
) -> Dict[str, float]:
    """
    Compute quantitative artifact reduction metrics.

    Args:
        corrupted_signal: Corrupted signal array.
        cleaned_signal: Cleaned signal array after preprocessing.
        clean_ground_truth: Optional uncorrupted ground-truth signal array.

    Returns:
        Dictionary of metrics including ARR (dB), SAR improvement (dB), and correlation.
    """
    var_corrupted = np.var(corrupted_signal) + 1e-12
    var_cleaned = np.var(cleaned_signal) + 1e-12

    # Artifact Reduction Ratio (ARR)
    arr_db = 10.0 * np.log10(var_corrupted / var_cleaned)

    metrics = {
        "artifact_reduction_ratio_db": float(arr_db),
    }

    if clean_ground_truth is not None:
        err_before = corrupted_signal - clean_ground_truth
        err_after = cleaned_signal - clean_ground_truth

        var_gt = np.var(clean_ground_truth) + 1e-12
        var_err_before = np.var(err_before) + 1e-12
        var_err_after = np.var(err_after) + 1e-12

        sar_before_db = 10.0 * np.log10(var_gt / var_err_before)
        sar_after_db = 10.0 * np.log10(var_gt / var_err_after)
        sar_improvement_db = sar_after_db - sar_before_db

        # Pearson correlation to ground truth
        flat_gt = clean_ground_truth.flatten()
        flat_clean = cleaned_signal.flatten()
        r_corr = np.corrcoef(flat_gt, flat_clean)[0, 1]

        metrics["sar_before_db"] = float(sar_before_db)
        metrics["sar_after_db"] = float(sar_after_db)
        metrics["sar_improvement_db"] = float(sar_improvement_db)
        metrics["ground_truth_correlation"] = float(r_corr)

    return metrics
