"""EEG oscillatory analysis."""

from typing import Tuple, Optional
import numpy as np
from scipy.signal import hilbert, butter, filtfilt


def calculate_instantaneous_frequency(
    signal: np.ndarray,
    fs: float
) -> np.ndarray:
    """
    Calculate instantaneous frequency of a signal.
    
    Args:
        signal: Input signal
        fs: Sampling frequency
        
    Returns:
        Instantaneous frequency array
    """
    analytic = hilbert(signal)
    phase = np.unwrap(np.angle(analytic))
    inst_freq = np.diff(phase) / (2.0 * np.pi) * fs
    
    # Pad to match original length
    inst_freq = np.concatenate([[inst_freq[0]], inst_freq])
    
    return inst_freq


def calculate_instantaneous_amplitude(signal: np.ndarray) -> np.ndarray:
    """
    Calculate instantaneous amplitude (envelope) of a signal.
    
    Args:
        signal: Input signal
        
    Returns:
        Instantaneous amplitude array
    """
    analytic = hilbert(signal)
    amplitude = np.abs(analytic)
    return amplitude


def calculate_amplitude_modulation(
    signal: np.ndarray,
    carrier_band: Tuple[float, float],
    modulator_band: Tuple[float, float],
    fs: float
) -> float:
    """
    Calculate cross-frequency amplitude modulation.
    
    Args:
        signal: Input signal
        carrier_band: (low, high) frequency for carrier
        modulator_band: (low, high) frequency for modulator
        fs: Sampling frequency
        
    Returns:
        Modulation index
    """
    from .phase_locking import bandpass_filter
    
    # Extract carrier and modulator
    carrier = bandpass_filter(signal, carrier_band[0], carrier_band[1], fs)
    modulator = bandpass_filter(signal, modulator_band[0], modulator_band[1], fs)
    
    # Get amplitude envelope of carrier
    carrier_amp = calculate_instantaneous_amplitude(carrier)
    
    # Get phase of modulator
    modulator_analytic = hilbert(modulator)
    modulator_phase = np.angle(modulator_analytic)
    
    # Calculate modulation index using mean vector length
    complex_values = carrier_amp * np.exp(1j * modulator_phase)
    modulation_index = np.abs(np.mean(complex_values)) / np.mean(carrier_amp)
    
    return float(modulation_index)


def calculate_burst_statistics(
    signal: np.ndarray,
    threshold: float = 1.5
) -> dict:
    """
    Calculate burst statistics from signal envelope.
    
    Args:
        signal: Input signal
        threshold: Threshold (in std) for burst detection
        
    Returns:
        Dictionary with burst statistics
    """
    # Get amplitude envelope
    amplitude = calculate_instantaneous_amplitude(signal)
    
    # Normalize
    amp_norm = (amplitude - np.mean(amplitude)) / np.std(amplitude)
    
    # Detect bursts
    burst_mask = amp_norm > threshold
    
    # Find burst onsets and offsets
    burst_diff = np.diff(np.concatenate([[0], burst_mask.astype(int), [0]]))
    burst_onsets = np.where(burst_diff == 1)[0]
    burst_offsets = np.where(burst_diff == -1)[0]
    
    if len(burst_onsets) == 0:
        return {
            "n_bursts": 0,
            "mean_duration": 0.0,
            "mean_amplitude": 0.0,
            "burst_rate": 0.0,
        }
    
    # Calculate statistics
    durations = burst_offsets - burst_onsets
    amplitudes = [np.mean(amplitude[onset:offset]) 
                  for onset, offset in zip(burst_onsets, burst_offsets)]
    
    return {
        "n_bursts": len(burst_onsets),
        "mean_duration": float(np.mean(durations)),
        "mean_amplitude": float(np.mean(amplitudes)),
        "burst_rate": len(burst_onsets) / len(signal),
    }


def calculate_phase_amplitude_coupling(
    signal: np.ndarray,
    phase_band: Tuple[float, float],
    amplitude_band: Tuple[float, float],
    fs: float,
    n_bins: int = 18
) -> Tuple[float, np.ndarray]:
    """
    Calculate phase-amplitude coupling.
    
    Args:
        signal: Input signal
        phase_band: (low, high) frequency for phase
        amplitude_band: (low, high) frequency for amplitude
        fs: Sampling frequency
        n_bins: Number of phase bins
        
    Returns:
        Tuple of (modulation_index, phase_amplitude_distribution)
    """
    from .phase_locking import bandpass_filter
    
    # Extract phase and amplitude signals
    phase_sig = bandpass_filter(signal, phase_band[0], phase_band[1], fs)
    amp_sig = bandpass_filter(signal, amplitude_band[0], amplitude_band[1], fs)
    
    # Get phase and amplitude
    phase = np.angle(hilbert(phase_sig))
    amplitude = np.abs(hilbert(amp_sig))
    
    # Create phase bins
    phase_bins = np.linspace(-np.pi, np.pi, n_bins + 1)
    
    # Calculate mean amplitude in each phase bin
    mean_amps = np.zeros(n_bins)
    for i in range(n_bins):
        mask = (phase >= phase_bins[i]) & (phase < phase_bins[i + 1])
        if np.any(mask):
            mean_amps[i] = np.mean(amplitude[mask])
    
    # Calculate modulation index (Kullback-Leibler divergence from uniform)
    mean_amps = mean_amps / np.sum(mean_amps)  # Normalize
    uniform = np.ones(n_bins) / n_bins
    
    # Avoid log(0)
    mean_amps = np.maximum(mean_amps, 1e-10)
    
    mi = np.sum(mean_amps * np.log(mean_amps / uniform))
    mi_norm = mi / np.log(n_bins)  # Normalize to [0, 1]
    
    return float(mi_norm), mean_amps
