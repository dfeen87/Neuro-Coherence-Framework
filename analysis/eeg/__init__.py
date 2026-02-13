"""EEG analysis package."""

from .phase_locking import calculate_plv, calculate_plv_matrix, calculate_phase_coherence
from .coherence_metrics import calculate_coherence, calculate_global_coherence
from .preprocessing import normalize_signal, remove_baseline, detect_artifacts

__all__ = [
    "calculate_plv",
    "calculate_plv_matrix",
    "calculate_phase_coherence",
    "calculate_coherence",
    "calculate_global_coherence",
    "normalize_signal",
    "remove_baseline",
    "detect_artifacts",
]
