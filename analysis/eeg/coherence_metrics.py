"""EEG coherence metrics calculations."""

from typing import Optional, Tuple
import numpy as np
from scipy.signal import coherence, welch


def calculate_coherence(
    signal1: np.ndarray, signal2: np.ndarray, fs: float, nperseg: Optional[int] = None
) -> Tuple[np.ndarray, np.ndarray]:
    """
    Calculate magnitude-squared coherence between two signals.

    Args:
        signal1: First signal
        signal2: Second signal
        fs: Sampling frequency (Hz)
        nperseg: Length of each segment for FFT

    Returns:
        Tuple of (frequencies, coherence_values)
    """
    if nperseg is None:
        nperseg = min(256, len(signal1) // 8)

    freqs, coh = coherence(signal1, signal2, fs=fs, nperseg=nperseg)
    return freqs, coh


def calculate_coherence_matrix(
    signals: np.ndarray, fs: float, freq_band: Optional[Tuple[float, float]] = None
) -> np.ndarray:
    """
    Calculate coherence matrix for multiple signals.

    Args:
        signals: 2D array (channels x time)
        fs: Sampling frequency
        freq_band: Optional (low, high) frequency range to average over

    Returns:
        Coherence matrix (channels x channels)
    """
    n_channels = signals.shape[0]
    coh_matrix = np.zeros((n_channels, n_channels))

    for i in range(n_channels):
        for j in range(i, n_channels):
            if i == j:
                coh_matrix[i, j] = 1.0
            else:
                freqs, coh = calculate_coherence(signals[i], signals[j], fs)

                # Average over frequency band if specified
                if freq_band is not None:
                    low, high = freq_band
                    mask = (freqs >= low) & (freqs <= high)
                    coh_value = np.mean(coh[mask])
                else:
                    coh_value = np.mean(coh)

                coh_matrix[i, j] = coh_value
                coh_matrix[j, i] = coh_value

    return coh_matrix


def calculate_weighted_phase_lag_index(
    signal1: np.ndarray, signal2: np.ndarray
) -> float:
    """
    Calculate weighted Phase Lag Index (wPLI).

    Args:
        signal1: First signal
        signal2: Second signal

    Returns:
        wPLI value (0 to 1)
    """
    from scipy.signal import hilbert

    # Get analytic signals
    analytic1 = hilbert(signal1)
    analytic2 = hilbert(signal2)

    # Calculate cross-spectrum
    cross_spectrum = analytic1 * np.conj(analytic2)

    # Imaginary part of cross-spectrum
    imag_cs = np.imag(cross_spectrum)

    # Calculate wPLI
    numerator = np.abs(np.mean(imag_cs))
    denominator = np.mean(np.abs(imag_cs))

    if denominator == 0:
        return 0.0

    wpli = numerator / denominator
    return float(wpli)


def calculate_global_coherence(
    signals: np.ndarray, fs: float, freq_band: Optional[Tuple[float, float]] = None
) -> float:
    """
    Calculate global coherence across all signal pairs.

    Args:
        signals: 2D array (channels x time)
        fs: Sampling frequency
        freq_band: Optional frequency range

    Returns:
        Global coherence value
    """
    coh_matrix = calculate_coherence_matrix(signals, fs, freq_band)

    # Extract upper triangle (excluding diagonal)
    n_channels = signals.shape[0]
    upper_indices = np.triu_indices(n_channels, k=1)
    coherence_values = coh_matrix[upper_indices]

    return float(np.mean(coherence_values))


def calculate_spectral_power(
    signal: np.ndarray, fs: float, freq_band: Optional[Tuple[float, float]] = None
) -> float:
    """
    Calculate spectral power in a frequency band.

    Args:
        signal: Input signal
        fs: Sampling frequency
        freq_band: Optional (low, high) frequency range

    Returns:
        Spectral power
    """
    freqs, psd = welch(signal, fs=fs)

    if freq_band is not None:
        low, high = freq_band
        mask = (freqs >= low) & (freqs <= high)
        power = np.trapz(psd[mask], freqs[mask])
    else:
        power = np.trapz(psd, freqs)

    return float(power)
