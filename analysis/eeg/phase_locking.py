"""EEG analysis module - Phase Locking Value (PLV) calculations."""

from typing import Optional, Tuple
import numpy as np
from scipy.signal import hilbert, butter, filtfilt


def calculate_plv(
    signal1: np.ndarray,
    signal2: np.ndarray,
    window_size: Optional[int] = None
) -> float:
    """
    Calculate Phase Locking Value (PLV) between two signals.
    
    Args:
        signal1: First signal (1D array)
        signal2: Second signal (1D array)
        window_size: Optional sliding window size
        
    Returns:
        PLV value (0 to 1)
    """
    # Get analytic signals
    analytic1 = hilbert(signal1)
    analytic2 = hilbert(signal2)
    
    # Extract instantaneous phases
    phase1 = np.angle(analytic1)
    phase2 = np.angle(analytic2)
    
    # Calculate phase difference
    phase_diff = phase1 - phase2
    
    # Calculate PLV
    if window_size is not None:
        # Sliding window PLV
        plv_array = np.zeros(len(signal1))
        half_window = window_size // 2
        
        for i in range(len(signal1)):
            start = max(0, i - half_window)
            end = min(len(signal1), i + half_window + 1)
            window_diff = phase_diff[start:end]
            plv_array[i] = np.abs(np.mean(np.exp(1j * window_diff)))
        
        return float(np.mean(plv_array))
    else:
        # Global PLV
        plv = np.abs(np.mean(np.exp(1j * phase_diff)))
        return float(plv)


def calculate_plv_matrix(
    signals: np.ndarray,
    window_size: Optional[int] = None
) -> np.ndarray:
    """
    Calculate PLV matrix for multiple signals.
    
    Args:
        signals: 2D array (channels x time)
        window_size: Optional sliding window size
        
    Returns:
        PLV matrix (channels x channels)
    """
    n_channels = signals.shape[0]
    plv_matrix = np.zeros((n_channels, n_channels))
    
    for i in range(n_channels):
        for j in range(i, n_channels):
            if i == j:
                plv_matrix[i, j] = 1.0
            else:
                plv = calculate_plv(signals[i], signals[j], window_size)
                plv_matrix[i, j] = plv
                plv_matrix[j, i] = plv
    
    return plv_matrix


def bandpass_filter(
    signal: np.ndarray,
    lowcut: float,
    highcut: float,
    fs: float,
    order: int = 4
) -> np.ndarray:
    """
    Apply bandpass filter to signal.
    
    Args:
        signal: Input signal
        lowcut: Lower frequency bound (Hz)
        highcut: Upper frequency bound (Hz)
        fs: Sampling frequency (Hz)
        order: Filter order
        
    Returns:
        Filtered signal
    """
    nyquist = 0.5 * fs
    low = lowcut / nyquist
    high = highcut / nyquist
    
    b, a = butter(order, [low, high], btype='band')
    filtered = filtfilt(b, a, signal)
    
    return filtered


def extract_frequency_band(
    signal: np.ndarray,
    fs: float,
    band: str = "alpha"
) -> np.ndarray:
    """
    Extract specific frequency band from signal.
    
    Args:
        signal: Input signal
        fs: Sampling frequency (Hz)
        band: Frequency band ("delta", "theta", "alpha", "beta", "gamma")
        
    Returns:
        Filtered signal
    """
    bands = {
        "delta": (0.5, 4),
        "theta": (4, 8),
        "alpha": (8, 13),
        "beta": (13, 30),
        "gamma": (30, 100),
    }
    
    if band not in bands:
        raise ValueError(f"Unknown band: {band}. Choose from {list(bands.keys())}")
    
    lowcut, highcut = bands[band]
    return bandpass_filter(signal, lowcut, highcut, fs)


def calculate_phase_coherence(
    signal1: np.ndarray,
    signal2: np.ndarray,
    fs: float,
    band: Optional[str] = None
) -> float:
    """
    Calculate phase coherence between two signals.
    
    Args:
        signal1: First signal
        signal2: Second signal
        fs: Sampling frequency
        band: Optional frequency band to filter
        
    Returns:
        Phase coherence value (0 to 1)
    """
    # Filter to band if specified
    if band is not None:
        signal1 = extract_frequency_band(signal1, fs, band)
        signal2 = extract_frequency_band(signal2, fs, band)
    
    # Calculate PLV
    return calculate_plv(signal1, signal2)
