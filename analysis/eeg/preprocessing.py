"""EEG preprocessing utilities."""

from typing import Optional, Tuple
import numpy as np
from scipy.signal import detrend


def remove_baseline(
    signal: np.ndarray,
    baseline_window: Optional[Tuple[int, int]] = None
) -> np.ndarray:
    """
    Remove baseline from signal.
    
    Args:
        signal: Input signal
        baseline_window: Optional (start, end) indices for baseline
        
    Returns:
        Baseline-corrected signal
    """
    if baseline_window is not None:
        start, end = baseline_window
        baseline_mean = np.mean(signal[start:end])
    else:
        baseline_mean = np.mean(signal)
    
    return signal - baseline_mean


def remove_trend(signal: np.ndarray, method: str = "linear") -> np.ndarray:
    """
    Remove trend from signal.
    
    Args:
        signal: Input signal
        method: Detrending method ("linear" or "constant")
        
    Returns:
        Detrended signal
    """
    if method == "linear":
        return detrend(signal, type='linear')
    elif method == "constant":
        return detrend(signal, type='constant')
    else:
        raise ValueError(f"Unknown method: {method}")


def normalize_signal(
    signal: np.ndarray,
    method: str = "zscore"
) -> np.ndarray:
    """
    Normalize signal.
    
    Args:
        signal: Input signal
        method: Normalization method ("zscore", "minmax", or "robust")
        
    Returns:
        Normalized signal
    """
    if method == "zscore":
        mean = np.mean(signal)
        std = np.std(signal)
        if std == 0:
            return signal - mean
        return (signal - mean) / std
    
    elif method == "minmax":
        min_val = np.min(signal)
        max_val = np.max(signal)
        if max_val == min_val:
            return signal - min_val
        return (signal - min_val) / (max_val - min_val)
    
    elif method == "robust":
        median = np.median(signal)
        mad = np.median(np.abs(signal - median))
        if mad == 0:
            return signal - median
        return (signal - median) / (1.4826 * mad)
    
    else:
        raise ValueError(f"Unknown method: {method}")


def detect_artifacts(
    signal: np.ndarray,
    threshold: float = 3.0
) -> np.ndarray:
    """
    Detect artifacts using threshold on z-scored signal.
    
    Args:
        signal: Input signal
        threshold: Z-score threshold for artifact detection
        
    Returns:
        Boolean array indicating artifact locations
    """
    z_signal = normalize_signal(signal, method="zscore")
    artifacts = np.abs(z_signal) > threshold
    return artifacts


def interpolate_artifacts(
    signal: np.ndarray,
    artifacts: np.ndarray
) -> np.ndarray:
    """
    Interpolate over artifact locations.
    
    Args:
        signal: Input signal
        artifacts: Boolean array indicating artifacts
        
    Returns:
        Signal with interpolated artifacts
    """
    signal_clean = signal.copy()
    
    # Find artifact indices
    artifact_indices = np.where(artifacts)[0]
    good_indices = np.where(~artifacts)[0]
    
    if len(artifact_indices) == 0:
        return signal_clean
    
    if len(good_indices) < 2:
        # Not enough good points for interpolation
        return signal_clean
    
    # Linear interpolation
    signal_clean[artifact_indices] = np.interp(
        artifact_indices,
        good_indices,
        signal[good_indices]
    )
    
    return signal_clean


def apply_notch_filter(
    signal: np.ndarray,
    fs: float,
    freq: float = 60.0,
    quality: float = 30.0
) -> np.ndarray:
    """
    Apply notch filter to remove line noise.
    
    Args:
        signal: Input signal
        fs: Sampling frequency
        freq: Frequency to notch (e.g., 50 Hz or 60 Hz)
        quality: Quality factor
        
    Returns:
        Filtered signal
    """
    from scipy.signal import iirnotch, filtfilt
    
    b, a = iirnotch(freq, quality, fs)
    filtered = filtfilt(b, a, signal)
    
    return filtered
