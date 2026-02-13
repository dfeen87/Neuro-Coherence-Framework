"""Utility functions for Neuro-Coherence simulations."""

from typing import Union, Tuple
import numpy as np


def ensure_array(x: Union[float, np.ndarray]) -> np.ndarray:
    """Convert input to numpy array."""
    return np.atleast_1d(np.asarray(x))


def normalize_to_range(
    x: np.ndarray, lower: float = 0.0, upper: float = 1.0
) -> np.ndarray:
    """Normalize array to specified range."""
    x_min, x_max = np.min(x), np.max(x)
    if x_max == x_min:
        return np.full_like(x, (lower + upper) / 2)
    normalized = (x - x_min) / (x_max - x_min)
    return lower + normalized * (upper - lower)


def add_noise(
    signal: np.ndarray, noise_level: float = 0.1, noise_type: str = "gaussian"
) -> np.ndarray:
    """Add noise to signal."""
    if noise_type == "gaussian":
        noise = noise_level * np.random.randn(*signal.shape)
    elif noise_type == "uniform":
        noise = noise_level * (np.random.rand(*signal.shape) - 0.5) * 2
    else:
        raise ValueError(f"Unknown noise type: {noise_type}")
    return signal + noise


def sliding_window_stats(
    signal: np.ndarray, window_size: int, stat: str = "mean"
) -> np.ndarray:
    """Calculate sliding window statistics."""
    if stat not in ["mean", "std", "var", "median"]:
        raise ValueError(f"Unknown statistic: {stat}")

    result = np.zeros(len(signal))
    half_window = window_size // 2

    for i in range(len(signal)):
        start = max(0, i - half_window)
        end = min(len(signal), i + half_window + 1)
        window = signal[start:end]

        if stat == "mean":
            result[i] = np.mean(window)
        elif stat == "std":
            result[i] = np.std(window)
        elif stat == "var":
            result[i] = np.var(window)
        elif stat == "median":
            result[i] = np.median(window)

    return result


def calculate_phase_coherence(signal1: np.ndarray, signal2: np.ndarray) -> float:
    """Calculate phase coherence between two signals."""
    from scipy.signal import hilbert

    # Get analytic signals
    analytic1 = hilbert(signal1)
    analytic2 = hilbert(signal2)

    # Get phases
    phase1 = np.angle(analytic1)
    phase2 = np.angle(analytic2)

    # Calculate phase difference
    phase_diff = phase1 - phase2

    # Calculate PLV (Phase Locking Value)
    plv = np.abs(np.mean(np.exp(1j * phase_diff)))

    return float(plv)


def generate_oscillation(
    duration: int,
    frequency: float,
    amplitude: float = 1.0,
    phase: float = 0.0,
    sampling_rate: float = 100.0,
    noise_level: float = 0.0,
) -> Tuple[np.ndarray, np.ndarray]:
    """Generate oscillatory signal."""
    t = np.arange(duration) / sampling_rate
    signal = amplitude * np.sin(2 * np.pi * frequency * t + phase)

    if noise_level > 0:
        signal = add_noise(signal, noise_level)

    return t, signal


def safe_divide(
    numerator: Union[float, np.ndarray],
    denominator: Union[float, np.ndarray],
    default: float = 0.0,
) -> Union[float, np.ndarray]:
    """Safe division with default for zero denominator."""
    num = np.asarray(numerator)
    denom = np.asarray(denominator)

    result = np.full_like(num, default, dtype=float)
    mask = denom != 0
    result[mask] = num[mask] / denom[mask]

    return result if isinstance(numerator, np.ndarray) else float(result)


def exponential_decay(
    t: np.ndarray, initial_value: float, decay_rate: float, offset: float = 0.0
) -> np.ndarray:
    """Generate exponential decay curve."""
    return initial_value * np.exp(-decay_rate * t) + offset


def logistic_growth(
    t: np.ndarray, initial_value: float, carrying_capacity: float, growth_rate: float
) -> np.ndarray:
    """Generate logistic growth curve."""
    return carrying_capacity / (
        1
        + ((carrying_capacity - initial_value) / initial_value)
        * np.exp(-growth_rate * t)
    )
