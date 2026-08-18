# Copyright (c) 2026 Don Michael Feeney Jr.
# MIT License - see LICENSE for details.

"""
Cross-modal spatiotemporal synchronization and coupling module.

Provides temporal alignment (HRF convolution, downsampling), sliding-window PLV,
Canonical Correlation Analysis (CCA), network variance calculation (Delta_GR),
joint spatiotemporal coherence (Lambda), and bipolar disorder regime stratification.
"""

from typing import Dict, Tuple, Any
import numpy as np
from scipy.signal import butter, filtfilt, hilbert


def _canonical_hrf(
    t: np.ndarray, delay: float = 6.0, undershoot: float = 16.0
) -> np.ndarray:
    """Canonical double-gamma hemodynamic response function (HRF)."""
    from scipy.stats import gamma

    peak = gamma.pdf(t, delay)
    undershoot_peak = gamma.pdf(t, undershoot)
    hrf = peak - 0.16 * undershoot_peak
    norm = np.max(hrf)
    return hrf / norm if norm > 0 else hrf


def align_eeg_bold(
    eeg_signals: np.ndarray,
    fs: float,
    fmri_timeseries: np.ndarray,
    tr: float,
    band: Tuple[float, float] = (8.0, 12.0),
) -> np.ndarray:
    """
    Extract band-limited EEG envelope, convolve with HRF, and downsample to fMRI TR resolution.

    Args:
        eeg_signals: EEG signals of shape (n_channels, n_eeg_samples).
        fs: EEG sampling rate in Hz.
        fmri_timeseries: fMRI timeseries of shape (n_rois, n_tr).
        tr: Repetition time in seconds.
        band: Frequency band tuple (lowcut, highcut) in Hz.

    Returns:
        Aligned EEG envelope array of shape (n_channels, n_tr).
    """
    n_channels, n_eeg_samples = eeg_signals.shape
    n_rois, n_tr = fmri_timeseries.shape

    # 1. Bandpass filter
    nyq = 0.5 * fs
    lowcut, highcut = band
    b, a = butter(2, [lowcut / nyq, highcut / nyq], btype="band")

    t_hrf = np.linspace(0, 30, int(30 * fs))
    hrf = _canonical_hrf(t_hrf)

    time_fmri = np.arange(n_tr) * tr
    tr_indices = np.clip(np.round(time_fmri * fs).astype(int), 0, n_eeg_samples - 1)

    aligned_envelopes = np.zeros((n_channels, n_tr))

    for ch in range(n_channels):
        filtered = filtfilt(b, a, eeg_signals[ch])
        analytic = hilbert(filtered)
        envelope = np.abs(analytic)

        # Convolve with HRF
        bold_conv = np.convolve(envelope, hrf, mode="full")[:n_eeg_samples]
        aligned_envelopes[ch] = bold_conv[tr_indices]

    return aligned_envelopes


def compute_eeg_bold_cross_correlation(
    aligned_eeg_envelope: np.ndarray,
    fmri_timeseries: np.ndarray,
) -> Dict[str, Any]:
    """
    Compute cross-correlation between aligned EEG envelopes and BOLD timeseries.

    Args:
        aligned_eeg_envelope: Shape (n_channels, n_tr).
        fmri_timeseries: Shape (n_rois, n_tr).

    Returns:
        Dictionary containing correlation matrix, mean, and max correlation.
    """
    n_channels = aligned_eeg_envelope.shape[0]
    n_rois = fmri_timeseries.shape[0]

    corr_matrix = np.zeros((n_channels, n_rois))

    for ch in range(n_channels):
        for roi in range(n_rois):
            e_norm = aligned_eeg_envelope[ch] - np.mean(aligned_eeg_envelope[ch])
            f_norm = fmri_timeseries[roi] - np.mean(fmri_timeseries[roi])
            denom = (np.std(e_norm) * np.std(f_norm)) + 1e-12
            corr_matrix[ch, roi] = np.mean(e_norm * f_norm) / denom

    corr_matrix = np.nan_to_num(corr_matrix)

    return {
        "correlation_matrix": corr_matrix,
        "mean_correlation": float(np.mean(np.abs(corr_matrix))),
        "max_correlation": float(np.max(np.abs(corr_matrix))),
    }


def compute_sliding_plv(
    eeg_signals: np.ndarray,
    fs: float,
    window_size_sec: float = 10.0,
    step_sec: float = 2.0,
    band: Tuple[float, float] = (8.0, 12.0),
) -> Dict[str, Any]:
    """
    Compute sliding-window Phase Locking Value (PLV) across EEG channels.

    Args:
        eeg_signals: EEG array of shape (n_channels, n_samples).
        fs: Sampling rate in Hz.
        window_size_sec: Window length in seconds.
        step_sec: Step size in seconds.
        band: Frequency band for phase extraction.

    Returns:
        Dictionary with mean PLV time series, global mean PLV, and phase variance.
    """
    n_channels, n_samples = eeg_signals.shape
    window_samples = int(window_size_sec * fs)
    step_samples = int(step_sec * fs)

    nyq = 0.5 * fs
    lowcut, highcut = band
    b, a = butter(2, [lowcut / nyq, highcut / nyq], btype="band")

    phases = np.zeros((n_channels, n_samples))
    for ch in range(n_channels):
        filtered = filtfilt(b, a, eeg_signals[ch])
        analytic = hilbert(filtered)
        phases[ch] = np.angle(analytic)

    starts = np.arange(0, n_samples - window_samples + 1, step_samples)
    plv_timeseries = []

    for start in starts:
        win_phases = phases[:, start : start + window_samples]
        channel_plvs = []
        for i in range(n_channels):
            for j in range(i + 1, n_channels):
                phase_diff = win_phases[i] - win_phases[j]
                plv = np.abs(np.mean(np.exp(1j * phase_diff)))
                channel_plvs.append(plv)

        plv_timeseries.append(np.mean(channel_plvs) if channel_plvs else 0.0)

    plv_arr = np.array(plv_timeseries)

    return {
        "plv_timeseries": plv_arr,
        "mean_plv": float(np.mean(plv_arr)) if len(plv_arr) > 0 else 0.0,
        "plv_variance": float(np.var(plv_arr)) if len(plv_arr) > 0 else 0.0,
    }


def compute_cca_coherence(
    eeg_features: np.ndarray,
    fmri_timeseries: np.ndarray,
    n_components: int = 2,
) -> Dict[str, Any]:
    """
    Compute Canonical Correlation Analysis (CCA) / cross-modal singular correlation
    between EEG envelope/features and fMRI BOLD timeseries.

    Args:
        eeg_features: Shape (n_eeg_features, n_tr).
        fmri_timeseries: Shape (n_rois, n_tr).
        n_components: Number of canonical components.

    Returns:
        Dictionary with canonical correlation values and mean CCA coherence.
    """
    X = eeg_features.T  # (n_tr, n_eeg_features)
    Y = fmri_timeseries.T  # (n_tr, n_rois)

    n_samples, dx = X.shape
    dy = Y.shape[1]

    if n_samples < 2 or dx < 1 or dy < 1:
        return {
            "canonical_correlations": np.array([0.0]),
            "mean_cca": 0.0,
            "max_cca": 0.0,
        }

    X_centered = X - np.mean(X, axis=0)
    Y_centered = Y - np.mean(Y, axis=0)

    X_std = np.std(X_centered, axis=0) + 1e-8
    Y_std = np.std(Y_centered, axis=0) + 1e-8

    X_norm = X_centered / X_std
    Y_norm = Y_centered / Y_std

    # Cross-covariance matrix
    C_xy = np.dot(X_norm.T, Y_norm) / float(n_samples - 1)

    # Singular Value Decomposition to extract canonical singular correlations
    _, S, _ = np.linalg.svd(C_xy, full_matrices=False)
    norm_factor = np.sqrt(min(dx, dy))
    sing_corrs = np.clip(S / norm_factor, 0.0, 1.0)

    n_comp = min(n_components, len(sing_corrs))
    top_corrs = sing_corrs[:n_comp]

    return {
        "canonical_correlations": top_corrs,
        "mean_cca": float(np.mean(top_corrs)) if len(top_corrs) > 0 else 0.0,
        "max_cca": float(np.max(top_corrs)) if len(top_corrs) > 0 else 0.0,
    }


def compute_network_variance(
    fmri_timeseries: np.ndarray,
    window_size: int = 10,
    step: int = 2,
) -> Dict[str, Any]:
    """
    Compute temporal instability / variance of functional connectivity (Delta_GR).

    Args:
        fmri_timeseries: fMRI timeseries of shape (n_rois, n_tr).
        window_size: Sliding window size in TRs.
        step: Window step size in TRs.

    Returns:
        Dictionary with Delta_GR, mean connectivity, and connectivity variance.
    """
    n_rois, n_tr = fmri_timeseries.shape

    if n_tr < window_size:
        # Fallback for short timeseries
        corr = np.corrcoef(fmri_timeseries)
        triu_vals = corr[np.triu_indices(n_rois, k=1)]
        sync_var = float(np.var(triu_vals)) if len(triu_vals) > 0 else 0.0
        return {
            "delta_gr": sync_var,
            "mean_connectivity": float(np.mean(corr)),
            "connectivity_variance": sync_var,
        }

    starts = np.arange(0, n_tr - window_size + 1, step)
    conn_matrices = []

    for start in starts:
        win_data = fmri_timeseries[:, start : start + window_size]
        corr = np.corrcoef(win_data)
        corr = np.nan_to_num(corr)
        conn_matrices.append(corr)

    conn_stack = np.array(conn_matrices)  # (n_windows, n_rois, n_rois)
    triu_idx = np.triu_indices(n_rois, k=1)

    # Standard deviation across windows for each functional connection
    edge_stds = np.std(conn_stack[:, triu_idx[0], triu_idx[1]], axis=0)
    mean_edge_std = float(np.mean(edge_stds))
    # Map network connectivity instability to Delta_GR in [0, 1]
    delta_gr = float(np.clip(4.0 * mean_edge_std, 0.0, 1.0))

    return {
        "delta_gr": delta_gr,
        "mean_connectivity": float(np.mean(conn_stack)),
        "connectivity_variance": float(
            np.mean(np.var(conn_stack[:, triu_idx[0], triu_idx[1]], axis=0))
        ),
        "edge_stds": edge_stds,
    }


def compute_joint_spatiotemporal_coherence(
    eeg_signals: np.ndarray,
    fs: float,
    fmri_timeseries: np.ndarray,
    tr: float,
) -> Dict[str, Any]:
    """
    Compute unified joint EEG-fMRI spatiotemporal coherence (Lambda).

    Args:
        eeg_signals: EEG array (n_channels, n_samples).
        fs: EEG sampling rate in Hz.
        fmri_timeseries: fMRI array (n_rois, n_tr).
        tr: TR in seconds.

    Returns:
        Dictionary containing Lambda, PLV metric, cross-correlation, and CCA coherence.
    """
    # 1. Sliding PLV
    plv_res = compute_sliding_plv(eeg_signals, fs)
    plv_val = plv_res["mean_plv"]

    # 2. Aligned EEG ↔ BOLD cross-correlation
    aligned_eeg = align_eeg_bold(eeg_signals, fs, fmri_timeseries, tr)
    xcorr_res = compute_eeg_bold_cross_correlation(aligned_eeg, fmri_timeseries)
    xcorr_val = xcorr_res["mean_correlation"]

    # 3. CCA coherence
    cca_res = compute_cca_coherence(aligned_eeg, fmri_timeseries)
    cca_val = cca_res["mean_cca"]

    # Composite joint spatiotemporal coherence Lambda in [0, 1]
    lambda_val = 0.4 * plv_val + 0.3 * xcorr_val + 0.3 * cca_val
    lambda_val = float(np.clip(lambda_val, 0.0, 1.0))

    return {
        "lambda": lambda_val,
        "plv_coherence": plv_val,
        "xcorr_coherence": xcorr_val,
        "cca_coherence": cca_val,
    }


def classify_bipolar_regime(lambda_val: float, delta_gr_val: float) -> Dict[str, Any]:
    """
    Classify joint EEG-fMRI metrics (Lambda, Delta_GR) into bipolar disorder regimes.

    Working Hypotheses / Regimes:
        - Euthymic:   High Lambda (>= 0.50), Low Delta_GR (<= 0.30)
        - Manic:      Moderate Lambda (0.30 - 0.55), Elevated Delta_GR (>= 0.55)
        - Depressive: Low Lambda (<= 0.35), Moderate/Low Delta_GR (0.35 - 0.58)

    Args:
        lambda_val: Joint spatiotemporal coherence metric Lambda.
        delta_gr_val: Network connectivity variance metric Delta_GR.

    Returns:
        Dictionary with regime label, confidence score, raw metric values, and description.
    """
    # Centroids in (Lambda, Delta_GR) feature space
    centroids = {
        "euthymic": (0.80, 0.20),
        "manic": (0.40, 0.65),
        "depressive": (0.25, 0.50),
    }

    # Explicit threshold rules
    if lambda_val >= 0.50 and delta_gr_val <= 0.35:
        primary_regime = "euthymic"
    elif lambda_val <= 0.35 and delta_gr_val <= 0.55:
        primary_regime = "depressive"
    elif delta_gr_val >= 0.40:
        primary_regime = "manic"
    else:
        # Distance-based classification
        dists = {
            k: np.sqrt((lambda_val - c[0]) ** 2 + (delta_gr_val - c[1]) ** 2)
            for k, c in centroids.items()
        }
        primary_regime = min(dists, key=dists.get)

    # Confidence score based on inverse distance to regime centroid
    target_centroid = centroids[primary_regime]
    dist_to_target = np.sqrt(
        (lambda_val - target_centroid[0]) ** 2
        + (delta_gr_val - target_centroid[1]) ** 2
    )
    confidence = float(np.clip(1.0 - dist_to_target, 0.0, 1.0))

    descriptions = {
        "euthymic": "High spatiotemporal phase coherence and stable fronto-limbic/triple-network regulation.",
        "manic": "Phase instability, elevated network variance, and cross-frequency dysregulation.",
        "depressive": "Hypo-connected fronto-limbic coupling and sluggish EEG-BOLD coherence.",
    }

    return {
        "regime": primary_regime,
        "confidence": confidence,
        "lambda": float(lambda_val),
        "delta_gr": float(delta_gr_val),
        "description": descriptions[primary_regime],
    }
