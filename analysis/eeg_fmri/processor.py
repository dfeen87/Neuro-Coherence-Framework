# Copyright (c) 2026 Don Michael Feeney Jr.
# MIT License - see LICENSE for details.

"""
High-level processor for concurrent EEG-fMRI integration and Neuro-Coherence calculation.
"""

from typing import Dict, Optional, Any
import numpy as np

from simulations.core import NeuroCoherence, Operators
from analysis.eeg_fmri.preprocessing import (
    remove_gradient_artifacts,
    remove_bcg_artifacts,
    remove_motion_and_scanner_noise,
    compute_artifact_metrics,
)
from analysis.eeg_fmri.synchronization import (
    compute_joint_spatiotemporal_coherence,
    compute_network_variance,
    classify_bipolar_regime,
)


class ConcurrentEEGFMRIProcessor:
    """
    First-class processor for concurrent EEG-fMRI preprocessing, cross-modal integration,
    joint coherence metric extraction (Lambda, Delta_GR), and Psi calculation.
    """

    def __init__(self, phi: float = 1.0):
        """
        Initialize the concurrent EEG-fMRI processor.

        Args:
            phi: Global modulation coefficient.
        """
        self.nc = NeuroCoherence(phi=phi)

    def preprocess_eeg_in_mri(
        self,
        eeg_signals: np.ndarray,
        fs: float,
        tr: float,
        tr_trigger_indices: Optional[np.ndarray] = None,
        r_peak_indices: Optional[np.ndarray] = None,
        ecg_signal: Optional[np.ndarray] = None,
        ground_truth_clean: Optional[np.ndarray] = None,
    ) -> Dict[str, Any]:
        """
        Execute full EEG-in-MRI preprocessing pipeline:
        Gradient Artifact Removal (AAS + OBS) -> BCG Removal (OBS) -> Motion & Noise Filtering.

        Args:
            eeg_signals: Raw/corrupted EEG signals of shape (n_channels, n_samples).
            fs: EEG sampling frequency in Hz.
            tr: fMRI repetition time in seconds.
            tr_trigger_indices: Optional TR slice/volume trigger sample indices.
            r_peak_indices: Optional ECG R-peak sample indices.
            ecg_signal: Optional ECG signal trace.
            ground_truth_clean: Optional uncorrupted ground-truth EEG signals for metric benchmarking.

        Returns:
            Dictionary containing cleaned EEG signals, artifact estimates, and performance metrics.
        """
        # 1. Gradient Artifact Removal
        ga_res = remove_gradient_artifacts(
            eeg_signals, fs, tr, tr_trigger_indices=tr_trigger_indices
        )
        eeg_after_ga = ga_res["cleaned_signals"]

        # 2. Ballistocardiogram (BCG) Artifact Removal
        bcg_res = remove_bcg_artifacts(
            eeg_after_ga,
            fs,
            r_peak_indices=r_peak_indices,
            ecg_signal=ecg_signal,
        )
        eeg_after_bcg = bcg_res["cleaned_signals"]

        # 3. Motion & Scanner Noise Removal
        motion_res = remove_motion_and_scanner_noise(eeg_after_bcg, fs)
        eeg_cleaned = motion_res["cleaned_signals"]

        # 4. Artifact Reduction Metrics
        artifact_metrics = compute_artifact_metrics(
            eeg_signals, eeg_cleaned, clean_ground_truth=ground_truth_clean
        )

        return {
            "cleaned_signals": eeg_cleaned,
            "ga_artifact": ga_res["estimated_artifact"],
            "bcg_artifact": bcg_res["estimated_artifact"],
            "motion_mask": motion_res["motion_mask"],
            "artifact_metrics": artifact_metrics,
        }

    def synchronize_and_integrate(
        self,
        eeg_signals: np.ndarray,
        fs: float,
        fmri_timeseries: np.ndarray,
        tr: float,
    ) -> Dict[str, Any]:
        """
        Compute joint spatiotemporal coherence (Lambda), network variance (Delta_GR),
        and classify the bipolar disorder regime.

        Args:
            eeg_signals: Preprocessed EEG signals (n_channels, n_samples).
            fs: EEG sampling rate in Hz.
            fmri_timeseries: fMRI timeseries (n_rois, n_tr).
            tr: Repetition time in seconds.

        Returns:
            Dictionary with Lambda, Delta_GR, and clinical regime classification.
        """
        # Spatiotemporal coherence Lambda
        lambda_res = compute_joint_spatiotemporal_coherence(
            eeg_signals, fs, fmri_timeseries, tr
        )
        lambda_val = lambda_res["lambda"]

        # Functional connectivity variance Delta_GR
        delta_res = compute_network_variance(fmri_timeseries)
        delta_gr_val = delta_res["delta_gr"]

        # Regime classification
        regime_res = classify_bipolar_regime(lambda_val, delta_gr_val)

        return {
            "lambda_details": lambda_res,
            "delta_details": delta_res,
            "regime_details": regime_res,
            "lambda": lambda_val,
            "delta_gr": delta_gr_val,
        }

    def process_dataset(self, concurrent_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process a complete concurrent EEG-fMRI dataset dictionary.

        Args:
            concurrent_data: Dataset dictionary (e.g. from generate_concurrent_eeg_fmri_data).

        Returns:
            Complete analysis results including preprocessing metrics, sync metrics, and Psi.
        """
        eeg_corrupted = concurrent_data["eeg_corrupted"]
        fs_eeg = concurrent_data["fs_eeg"]
        fmri_timeseries = concurrent_data["fmri_corrupted"]
        tr_fmri = concurrent_data["tr_fmri"]

        ecg_signal = concurrent_data.get("ecg_signal")
        tr_triggers = concurrent_data.get("tr_trigger_indices")
        r_peaks = concurrent_data.get("r_peak_indices")
        ground_truth_clean = concurrent_data.get("eeg_clean")

        # Step 1: Preprocess EEG
        preproc_results = self.preprocess_eeg_in_mri(
            eeg_corrupted,
            fs=fs_eeg,
            tr=tr_fmri,
            tr_trigger_indices=tr_triggers,
            r_peak_indices=r_peaks,
            ecg_signal=ecg_signal,
            ground_truth_clean=ground_truth_clean,
        )

        # Step 2: Cross-modal synchronization
        sync_results = self.synchronize_and_integrate(
            preproc_results["cleaned_signals"],
            fs=fs_eeg,
            fmri_timeseries=fmri_timeseries,
            tr=tr_fmri,
        )

        # Step 3: Compute Neuro-Coherence Psi
        psi_results = self.calculate_psi_from_metrics(
            sync_results["lambda"], sync_results["delta_gr"]
        )

        return {
            "preprocessing": preproc_results,
            "synchronization": sync_results,
            "neuro_coherence": psi_results,
        }

    def calculate_psi_from_metrics(
        self,
        lambda_val: float,
        delta_gr_val: float,
        plasticity: float = 0.8,
        homeostasis: float = 0.9,
    ) -> Dict[str, Any]:
        """
        Calculate Neuro-Coherence Function (Psi) using empirical Lambda and Delta_GR.

        Args:
            lambda_val: Joint spatiotemporal coherence.
            delta_gr_val: Functional network variance.
            plasticity: Adaptive gain parameter.
            homeostasis: Thermodynamic stability parameter.

        Returns:
            Dictionary with Psi value and computed operator objects.
        """
        gamma = Operators.adaptive_gain(
            plasticity=plasticity, responsiveness=lambda_val
        )
        theta = Operators.thermodynamic_stability(homeostasis=homeostasis)
        delta = Operators.connectivity_variance(sync_variance=delta_gr_val)
        lambda_op = Operators.spatiotemporal_coherence(phase_alignment=lambda_val)

        psi_result = self.nc.calculate(gamma, theta, delta, lambda_op)

        return {
            "psi": float(psi_result.psi),
            "psi_result": psi_result,
            "gamma": gamma,
            "theta": theta,
            "delta": delta,
            "lambda": lambda_op,
        }
