"""Multimodal integration for Ψ calculation from empirical data."""

from typing import Dict, Optional, Any
import numpy as np
from simulations.core import NeuroCoherence, Operators


class MultimodalPsiCalculator:
    """
    Calculate Ψ from multimodal empirical data.

    Integrates EEG, fMRI, and metabolic measurements to compute
    the Neuro-Coherence Function from real or synthetic data.
    """

    def __init__(self, phi: float = 1.0):
        """
        Initialize calculator.

        Args:
            phi: Global modulation coefficient
        """
        self.nc = NeuroCoherence(phi=phi)

    def calculate_from_eeg(
        self, plv_matrix: np.ndarray, recovery_plv: Optional[float] = None
    ) -> Dict[str, Any]:
        """
        Calculate Γ (adaptive gain) and Λ (coherence) from EEG.

        Args:
            plv_matrix: Phase locking value matrix
            recovery_plv: Optional PLV recovery metric

        Returns:
            Dictionary with operator values
        """
        # Calculate Λ from PLV
        mean_plv = np.mean(plv_matrix[np.triu_indices_from(plv_matrix, k=1)])
        phase_alignment = np.clip(mean_plv, 0, 1)

        lambda_op = Operators.spatiotemporal_coherence(
            phase_alignment=phase_alignment, plv=mean_plv
        )

        # Calculate Γ from recovery if available
        if recovery_plv is not None:
            plasticity = np.clip(recovery_plv, 0, 1)
            gamma_op = Operators.adaptive_gain(
                plasticity=plasticity, responsiveness=mean_plv
            )
        else:
            # Default based on current coherence
            gamma_op = Operators.adaptive_gain(plasticity=0.8, responsiveness=mean_plv)

        return {
            "gamma": gamma_op,
            "lambda": lambda_op,
            "plv_mean": mean_plv,
        }

    def calculate_from_fmri(
        self,
        connectivity_matrix: np.ndarray,
        network_labels: Optional[np.ndarray] = None,
    ) -> Dict[str, Any]:
        """
        Calculate Δ (connectivity variance) from fMRI.

        Args:
            connectivity_matrix: Functional connectivity matrix
            network_labels: Optional network labels for DMN/SN/CEN

        Returns:
            Dictionary with operator values
        """
        # Calculate network variance
        upper_tri = connectivity_matrix[np.triu_indices_from(connectivity_matrix, k=1)]
        sync_variance = np.var(upper_tri)

        # Network-specific metrics if labels provided
        network_metrics = None
        if network_labels is not None:
            from ..fmri.connectivity import calculate_network_connectivity

            # Dummy timeseries for network calculation
            # In real use, this would use actual timeseries
            within_conn, between_conn = self._calculate_network_stats(
                connectivity_matrix, network_labels
            )

            network_metrics = {
                "DMN": within_conn[0] if len(within_conn) > 0 else 0.5,
                "SN": within_conn[1] if len(within_conn) > 1 else 0.5,
                "CEN": within_conn[2] if len(within_conn) > 2 else 0.5,
            }

        delta_op = Operators.connectivity_variance(
            sync_variance=sync_variance, network_metrics=network_metrics
        )

        return {
            "delta": delta_op,
            "sync_variance": sync_variance,
            "network_metrics": network_metrics,
        }

    def _calculate_network_stats(
        self, conn_matrix: np.ndarray, network_labels: np.ndarray
    ) -> tuple:
        """Helper to calculate network statistics."""
        unique_networks = np.unique(network_labels)
        n_networks = len(unique_networks)
        within_conn = np.zeros(n_networks)

        for i, net in enumerate(unique_networks):
            mask = network_labels == net
            submatrix = conn_matrix[np.ix_(mask, mask)]
            # Exclude diagonal
            upper = submatrix[np.triu_indices_from(submatrix, k=1)]
            within_conn[i] = np.mean(upper) if len(upper) > 0 else 0

        return within_conn, None

    def calculate_from_metabolic(
        self,
        atp_level: float,
        ocr: Optional[float] = None,
        lactate: Optional[float] = None,
    ) -> Dict[str, Any]:
        """
        Calculate Θ (thermodynamic stability) from metabolic data.

        Args:
            atp_level: ATP production level (normalized 0-1)
            ocr: Optional oxygen consumption rate
            lactate: Optional lactate level

        Returns:
            Dictionary with operator values
        """
        # Homeostasis based on ATP
        homeostasis = np.clip(atp_level, 0, 1)

        # Adjust for OCR if available
        if ocr is not None:
            ocr_normalized = np.clip(ocr, 0, 2)
        else:
            ocr_normalized = None

        theta_op = Operators.thermodynamic_stability(
            homeostasis=homeostasis, atp_production=atp_level, ocr=ocr_normalized
        )

        return {
            "theta": theta_op,
            "homeostasis": homeostasis,
            "atp_level": atp_level,
        }

    def calculate_psi_multimodal(
        self,
        eeg_data: Optional[Dict[str, Any]] = None,
        fmri_data: Optional[Dict[str, Any]] = None,
        metabolic_data: Optional[Dict[str, Any]] = None,
        default_plasticity: float = 0.8,
        default_homeostasis: float = 0.9,
        default_sync_variance: float = 0.3,
        default_phase_alignment: float = 0.85,
    ) -> Dict[str, Any]:
        """
        Calculate Ψ from multimodal data.

        Args:
            eeg_data: EEG measurements (PLV matrix, etc.)
            fmri_data: fMRI measurements (connectivity, etc.)
            metabolic_data: Metabolic measurements (ATP, OCR, etc.)
            default_*: Default values if data not provided

        Returns:
            Dictionary with Ψ and all operator values
        """
        # Process EEG data
        if eeg_data is not None:
            eeg_results = self.calculate_from_eeg(**eeg_data)
            gamma = eeg_results["gamma"]
            lambda_op = eeg_results["lambda"]
        else:
            gamma = Operators.adaptive_gain(
                plasticity=default_plasticity, responsiveness=0.5
            )
            lambda_op = Operators.spatiotemporal_coherence(
                phase_alignment=default_phase_alignment
            )

        # Process fMRI data
        if fmri_data is not None:
            fmri_results = self.calculate_from_fmri(**fmri_data)
            delta = fmri_results["delta"]
        else:
            delta = Operators.connectivity_variance(sync_variance=default_sync_variance)

        # Process metabolic data
        if metabolic_data is not None:
            metabolic_results = self.calculate_from_metabolic(**metabolic_data)
            theta = metabolic_results["theta"]
        else:
            theta = Operators.thermodynamic_stability(homeostasis=default_homeostasis)

        # Calculate Ψ
        psi_result = self.nc.calculate(gamma, theta, delta, lambda_op)

        return {
            "psi": psi_result.psi,
            "psi_result": psi_result,
            "gamma": gamma,
            "theta": theta,
            "delta": delta,
            "lambda": lambda_op,
        }
