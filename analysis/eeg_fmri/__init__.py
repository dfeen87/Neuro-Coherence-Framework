# Copyright (c) 2026 Don Michael Feeney Jr.
# MIT License - see LICENSE for details.

"""
EEG-fMRI concurrent integration package for Neuro-Coherence Framework.
"""

from analysis.eeg_fmri.processor import ConcurrentEEGFMRIProcessor
from analysis.eeg_fmri.preprocessing import (
    remove_gradient_artifacts,
    remove_bcg_artifacts,
    remove_motion_and_scanner_noise,
    compute_artifact_metrics,
    detect_ecg_rpeaks,
)
from analysis.eeg_fmri.synchronization import (
    align_eeg_bold,
    compute_eeg_bold_cross_correlation,
    compute_sliding_plv,
    compute_cca_coherence,
    compute_network_variance,
    compute_joint_spatiotemporal_coherence,
    classify_bipolar_regime,
)

__all__ = [
    "ConcurrentEEGFMRIProcessor",
    "remove_gradient_artifacts",
    "remove_bcg_artifacts",
    "remove_motion_and_scanner_noise",
    "compute_artifact_metrics",
    "detect_ecg_rpeaks",
    "align_eeg_bold",
    "compute_eeg_bold_cross_correlation",
    "compute_sliding_plv",
    "compute_cca_coherence",
    "compute_network_variance",
    "compute_joint_spatiotemporal_coherence",
    "classify_bipolar_regime",
]
