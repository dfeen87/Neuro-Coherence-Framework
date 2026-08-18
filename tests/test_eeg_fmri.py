# Copyright (c) 2026 Don Michael Feeney Jr.
# MIT License - see LICENSE for details.

"""
Unit tests for concurrent EEG-fMRI preprocessing, cross-modal synchronization,
joint metrics, and bipolar disorder regime classification.
"""

import pytest
import numpy as np

from data.synthetic.generate_data import generate_concurrent_eeg_fmri_data
from analysis.eeg_fmri.preprocessing import (
    remove_gradient_artifacts,
    remove_bcg_artifacts,
    remove_motion_and_scanner_noise,
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
from analysis.eeg_fmri.processor import ConcurrentEEGFMRIProcessor
from analysis.integration.multimodal_fusion import MultimodalPsiCalculator


class TestSyntheticConcurrentData:
    """Tests for synthetic concurrent EEG-fMRI dataset generation."""

    def test_generate_data_structure(self):
        data = generate_concurrent_eeg_fmri_data(
            n_eeg_channels=19,
            n_rois=12,
            duration_sec=30.0,
            fs_eeg=250.0,
            tr_fmri=2.0,
            state="euthymic",
        )

        assert "eeg_clean" in data
        assert "eeg_corrupted" in data
        assert "fmri_clean" in data
        assert "fmri_corrupted" in data
        assert "ecg_signal" in data
        assert "ground_truth" in data

        assert data["eeg_corrupted"].shape == (19, 7500)
        assert data["fmri_corrupted"].shape == (12, 15)

    @pytest.mark.parametrize("state", ["euthymic", "manic", "depressive"])
    def test_data_generation_states(self, state):
        data = generate_concurrent_eeg_fmri_data(duration_sec=20.0, state=state)
        assert data["ground_truth"]["state"] == state
        assert 0.0 <= data["ground_truth"]["expected_lambda"] <= 1.0
        assert 0.0 <= data["ground_truth"]["expected_delta_gr"] <= 1.0


class TestEEGInMRIPreprocessing:
    """Tests for EEG-in-MRI artifact correction algorithms."""

    def setup_method(self):
        self.data = generate_concurrent_eeg_fmri_data(
            n_eeg_channels=8,
            n_rois=6,
            duration_sec=20.0,
            fs_eeg=250.0,
            tr_fmri=2.0,
            random_seed=123,
        )

    def test_rpeak_detection(self):
        ecg = self.data["ecg_signal"]
        fs = self.data["fs_eeg"]
        peaks = detect_ecg_rpeaks(ecg, fs)
        assert len(peaks) > 0
        assert np.all(peaks < len(ecg))

    def test_gradient_artifact_removal(self):
        eeg_corrupted = self.data["eeg_corrupted"]
        fs = self.data["fs_eeg"]
        tr = self.data["tr_fmri"]
        triggers = self.data["tr_trigger_indices"]

        res = remove_gradient_artifacts(
            eeg_corrupted, fs, tr, tr_trigger_indices=triggers
        )
        cleaned = res["cleaned_signals"]

        assert cleaned.shape == eeg_corrupted.shape
        # Gradient artifact reduction should reduce overall signal variance
        assert np.var(cleaned) < np.var(eeg_corrupted)

    def test_bcg_artifact_removal(self):
        eeg_corrupted = self.data["eeg_corrupted"]
        fs = self.data["fs_eeg"]
        r_peaks = self.data["r_peak_indices"]

        res = remove_bcg_artifacts(eeg_corrupted, fs, r_peak_indices=r_peaks)
        cleaned = res["cleaned_signals"]

        assert cleaned.shape == eeg_corrupted.shape
        assert np.var(cleaned) < np.var(eeg_corrupted)

    def test_motion_and_noise_removal(self):
        eeg_corrupted = self.data["eeg_corrupted"]
        fs = self.data["fs_eeg"]

        res = remove_motion_and_scanner_noise(eeg_corrupted, fs)
        cleaned = res["cleaned_signals"]

        assert cleaned.shape == eeg_corrupted.shape
        assert "motion_mask" in res

    def test_artifact_metrics_calculation(self):
        corrupted = self.data["eeg_corrupted"]
        clean_gt = self.data["eeg_clean"]

        proc = ConcurrentEEGFMRIProcessor()
        preproc_res = proc.preprocess_eeg_in_mri(
            corrupted,
            fs=self.data["fs_eeg"],
            tr=self.data["tr_fmri"],
            tr_trigger_indices=self.data["tr_trigger_indices"],
            r_peak_indices=self.data["r_peak_indices"],
            ground_truth_clean=clean_gt,
        )

        metrics = preproc_res["artifact_metrics"]
        assert "artifact_reduction_ratio_db" in metrics
        assert metrics["artifact_reduction_ratio_db"] > 0.0
        assert "sar_improvement_db" in metrics
        assert metrics["sar_improvement_db"] > 0.0
        assert metrics["ground_truth_correlation"] > 0.0


class TestCrossModalSynchronization:
    """Tests for cross-modal synchronization, coherence, and regime classification."""

    def setup_method(self):
        self.data_euthymic = generate_concurrent_eeg_fmri_data(
            duration_sec=60.0, state="euthymic", random_seed=42
        )
        self.data_manic = generate_concurrent_eeg_fmri_data(
            duration_sec=60.0, state="manic", random_seed=42
        )
        self.data_depressive = generate_concurrent_eeg_fmri_data(
            duration_sec=60.0, state="depressive", random_seed=42
        )

    def test_align_eeg_bold(self):
        eeg = self.data_euthymic["eeg_clean"]
        fs = self.data_euthymic["fs_eeg"]
        fmri = self.data_euthymic["fmri_clean"]
        tr = self.data_euthymic["tr_fmri"]

        aligned = align_eeg_bold(eeg, fs, fmri, tr)
        assert aligned.shape == (eeg.shape[0], fmri.shape[1])

    def test_eeg_bold_cross_correlation(self):
        aligned = align_eeg_bold(
            self.data_euthymic["eeg_clean"],
            self.data_euthymic["fs_eeg"],
            self.data_euthymic["fmri_clean"],
            self.data_euthymic["tr_fmri"],
        )
        xcorr = compute_eeg_bold_cross_correlation(
            aligned, self.data_euthymic["fmri_clean"]
        )
        assert 0.0 <= xcorr["mean_correlation"] <= 1.0

    def test_sliding_plv(self):
        plv_res = compute_sliding_plv(
            self.data_euthymic["eeg_clean"], self.data_euthymic["fs_eeg"]
        )
        assert 0.0 <= plv_res["mean_plv"] <= 1.0

    def test_cca_coherence(self):
        aligned = align_eeg_bold(
            self.data_euthymic["eeg_clean"],
            self.data_euthymic["fs_eeg"],
            self.data_euthymic["fmri_clean"],
            self.data_euthymic["tr_fmri"],
        )
        cca_res = compute_cca_coherence(aligned, self.data_euthymic["fmri_clean"])
        assert 0.0 <= cca_res["mean_cca"] <= 1.0

    def test_network_variance_delta_gr(self):
        net_var_euthymic = compute_network_variance(self.data_euthymic["fmri_clean"])
        net_var_manic = compute_network_variance(self.data_manic["fmri_clean"])

        assert net_var_euthymic["delta_gr"] >= 0.0
        assert net_var_manic["delta_gr"] >= 0.0
        # Manic state should exhibit higher network connectivity variance Delta_GR
        assert net_var_manic["delta_gr"] > net_var_euthymic["delta_gr"]

    def test_joint_spatiotemporal_coherence_lambda(self):
        lambda_euthymic = compute_joint_spatiotemporal_coherence(
            self.data_euthymic["eeg_clean"],
            self.data_euthymic["fs_eeg"],
            self.data_euthymic["fmri_clean"],
            self.data_euthymic["tr_fmri"],
        )
        lambda_depressive = compute_joint_spatiotemporal_coherence(
            self.data_depressive["eeg_clean"],
            self.data_depressive["fs_eeg"],
            self.data_depressive["fmri_clean"],
            self.data_depressive["tr_fmri"],
        )

        assert 0.0 <= lambda_euthymic["lambda"] <= 1.0
        assert 0.0 <= lambda_depressive["lambda"] <= 1.0
        # Euthymic state should produce higher joint coherence Lambda than Depressive state
        assert lambda_euthymic["lambda"] > lambda_depressive["lambda"]

    def test_bipolar_regime_classification(self):
        reg_euthymic = classify_bipolar_regime(lambda_val=0.8, delta_gr_val=0.2)
        assert reg_euthymic["regime"] == "euthymic"

        reg_manic = classify_bipolar_regime(lambda_val=0.4, delta_gr_val=0.65)
        assert reg_manic["regime"] == "manic"

        reg_depressive = classify_bipolar_regime(lambda_val=0.25, delta_gr_val=0.5)
        assert reg_depressive["regime"] == "depressive"


class TestConcurrentProcessorAndMultimodalIntegration:
    """End-to-end integration tests using ConcurrentEEGFMRIProcessor & MultimodalPsiCalculator."""

    def test_processor_end_to_end(self):
        data = generate_concurrent_eeg_fmri_data(
            duration_sec=30.0, state="euthymic", random_seed=100
        )
        processor = ConcurrentEEGFMRIProcessor()
        results = processor.process_dataset(data)

        assert "preprocessing" in results
        assert "synchronization" in results
        assert "neuro_coherence" in results

        assert 0.0 <= results["neuro_coherence"]["psi"] <= 2.0
        assert results["synchronization"]["regime_details"]["regime"] == "euthymic"

    def test_multimodal_psi_calculator_concurrent_integration(self):
        data = generate_concurrent_eeg_fmri_data(
            duration_sec=30.0, state="manic", random_seed=101
        )
        calc = MultimodalPsiCalculator()
        res = calc.calculate_from_concurrent_eeg_fmri(data)

        assert "psi" in res
        assert "bipolar_regime" in res
        assert res["bipolar_regime"]["regime"] == "manic"
        assert "concurrent_results" in res

    def test_distinguishable_bipolar_metric_profiles(self):
        calc = MultimodalPsiCalculator()

        data_euth = generate_concurrent_eeg_fmri_data(
            duration_sec=60.0, state="euthymic", random_seed=200
        )
        data_manic = generate_concurrent_eeg_fmri_data(
            duration_sec=60.0, state="manic", random_seed=200
        )
        data_depr = generate_concurrent_eeg_fmri_data(
            duration_sec=60.0, state="depressive", random_seed=200
        )

        res_euth = calc.calculate_from_concurrent_eeg_fmri(data_euth)
        res_manic = calc.calculate_from_concurrent_eeg_fmri(data_manic)
        res_depr = calc.calculate_from_concurrent_eeg_fmri(data_depr)

        # Confirm distinguishable states
        assert res_euth["bipolar_regime"]["regime"] == "euthymic"
        assert res_manic["bipolar_regime"]["regime"] == "manic"
        assert res_depr["bipolar_regime"]["regime"] == "depressive"

        # Check Psi ordering: Euthymic > Manic / Depressive
        assert res_euth["psi"] > res_manic["psi"]
        assert res_euth["psi"] > res_depr["psi"]
