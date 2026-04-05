"""
Core Neuro-Coherence Function (Ψ) implementation.

This module implements the central mathematical framework:
    Ψ = Φ · ∫∫∫ [ Θ(E) · Γ(t) · (1 − Δ_GR) · Λ(r,t) ] dE dr dt
"""

from typing import Union, Optional, Dict, Any
import numpy as np
from dataclasses import dataclass
from scipy import integrate

from .operators import (
    OperatorResult,
    AdaptiveGain,
    ThermodynamicStability,
    ConnectivityVariance,
    SpatiotemporalCoherence,
)


@dataclass
class PsiResult:
    """Container for Ψ calculation results."""

    psi: float
    phi: float
    gamma_mean: float
    theta_mean: float
    delta_mean: float
    lambda_mean: float
    metadata: Dict[str, Any]

    def __float__(self):
        """Convert to float."""
        return float(self.psi)

    def __str__(self):
        return f"Ψ = {self.psi:.4f} (Φ={self.phi:.2f})"


class NeuroCoherence:
    """
    Neuro-Coherence Function (Ψ) calculator.

    Implements the core mathematical framework for quantifying
    systemic coherence across neural, metabolic, and network domains.

    The function integrates four operators:
        - Γ: Adaptive Gain (neuroplasticity)
        - Θ: Thermodynamic Stability (metabolic homeostasis)
        - Δ: Connectivity Variance (network synchronization)
        - Λ: Spatiotemporal Coherence (phase alignment)

    Example:
        >>> nc = NeuroCoherence()
        >>> gamma = nc.operators.adaptive_gain(plasticity=0.8)
        >>> theta = nc.operators.thermodynamic_stability(homeostasis=0.9)
        >>> delta = nc.operators.connectivity_variance(sync_variance=0.3)
        >>> lambda_op = nc.operators.spatiotemporal_coherence(phase_alignment=0.85)
        >>> psi = nc.calculate(gamma, theta, delta, lambda_op)
    """

    def __init__(self, phi: float = 1.0, integration_method: str = "trapezoidal"):
        """
        Initialize Neuro-Coherence calculator.

        Args:
            phi: Global modulation coefficient (default: 1.0)
            integration_method: Integration method ("trapezoidal", "simpson", or "mean")
        """
        if phi <= 0:
            raise ValueError("phi must be positive")
        if integration_method not in ["trapezoidal", "simpson", "mean"]:
            raise ValueError(
                "integration_method must be 'trapezoidal', 'simpson', or 'mean'"
            )

        self.phi = phi
        self.integration_method = integration_method

        # Initialize operators
        self.gamma_op = AdaptiveGain()
        self.theta_op = ThermodynamicStability()
        self.delta_op = ConnectivityVariance()
        self.lambda_op = SpatiotemporalCoherence()

    def calculate(
        self,
        gamma: Union[OperatorResult, float, np.ndarray],
        theta: Union[OperatorResult, float, np.ndarray],
        delta: Union[OperatorResult, float, np.ndarray],
        lambda_op: Union[OperatorResult, float, np.ndarray],
        time: Optional[np.ndarray] = None,
        space: Optional[np.ndarray] = None,
        energy: Optional[np.ndarray] = None,
    ) -> PsiResult:
        """
        Calculate the Neuro-Coherence Function (Ψ).

        Args:
            gamma: Adaptive gain (Γ) values
            theta: Thermodynamic stability (Θ) values
            delta: Connectivity variance (Δ) values
            lambda_op: Spatiotemporal coherence (Λ) values
            time: Optional time array for integration
            space: Optional spatial array for integration
            energy: Optional energy array for integration

        Returns:
            PsiResult with Ψ value and component statistics

        Raises:
            ValueError: If operator values are invalid
        """
        # Extract values from OperatorResults if needed
        gamma_val = self._extract_value(gamma)
        theta_val = self._extract_value(theta)
        delta_val = self._extract_value(delta)
        lambda_val = self._extract_value(lambda_op)

        # Ensure all values are numpy arrays
        gamma_arr = np.atleast_1d(gamma_val)
        theta_arr = np.atleast_1d(theta_val)
        delta_arr = np.atleast_1d(delta_val)
        lambda_arr = np.atleast_1d(lambda_val)

        # Validate values
        self._validate_operator_values(gamma_arr, theta_arr, delta_arr, lambda_arr)

        # Broadcast to same shape if needed
        gamma_arr, theta_arr, delta_arr, lambda_arr = np.broadcast_arrays(
            gamma_arr, theta_arr, delta_arr, lambda_arr
        )

        # Calculate integrand: Θ · Γ · (1 - Δ) · Λ
        integrand = theta_arr * gamma_arr * (1.0 - delta_arr) * lambda_arr

        # Numerical stability: clip to reasonable range
        integrand = np.clip(integrand, 0.0, 10.0)

        # Perform integration
        if time is not None or space is not None or energy is not None:
            # Multi-dimensional integration
            psi_value = self._integrate_multidim(integrand, time, space, energy)
        else:
            # Simple averaging/integration
            psi_value = self._integrate_simple(integrand)

        # Apply global modulation
        psi_value = self.phi * psi_value

        # Calculate statistics
        gamma_mean = float(np.mean(gamma_arr))
        theta_mean = float(np.mean(theta_arr))
        delta_mean = float(np.mean(delta_arr))
        lambda_mean = float(np.mean(lambda_arr))

        return PsiResult(
            psi=float(psi_value),
            phi=self.phi,
            gamma_mean=gamma_mean,
            theta_mean=theta_mean,
            delta_mean=delta_mean,
            lambda_mean=lambda_mean,
            metadata={
                "integration_method": self.integration_method,
                "shape": integrand.shape,
                "integrand_mean": float(np.mean(integrand)),
                "integrand_std": float(np.std(integrand)),
            },
        )

    def _extract_value(
        self, val: Union[OperatorResult, float, np.ndarray]
    ) -> np.ndarray:
        """Extract numerical value from OperatorResult or pass through."""
        if isinstance(val, OperatorResult):
            return val.value
        return val

    def _validate_operator_values(
        self,
        gamma: np.ndarray,
        theta: np.ndarray,
        delta: np.ndarray,
        lambda_val: np.ndarray,
    ) -> None:
        """Validate operator value ranges."""
        if np.any(gamma < 0):
            raise ValueError("Γ (gamma) must be non-negative")
        if np.any(theta < 0) or np.any(theta > 1):
            raise ValueError("Θ (theta) must be in range [0, 1]")
        if np.any(delta < 0) or np.any(delta > 1):
            raise ValueError("Δ (delta) must be in range [0, 1]")
        if np.any(lambda_val < 0) or np.any(lambda_val > 1):
            raise ValueError("Λ (lambda) must be in range [0, 1]")

    def _integrate_simple(self, integrand: np.ndarray) -> float:
        """Simple integration via averaging."""
        if self.integration_method == "mean":
            return float(np.mean(integrand))
        elif self.integration_method == "trapezoidal":
            if integrand.ndim == 1 and len(integrand) > 1:
                return float(integrate.trapezoid(integrand))
            else:
                return float(
                    np.mean(integrand)
                )  # Fallback for single value or multidim
        else:  # simpson
            if integrand.ndim == 1 and len(integrand) >= 3:
                return float(integrate.simpson(integrand))
            else:
                return float(np.mean(integrand))  # Fallback

    def _integrate_multidim(
        self,
        integrand: np.ndarray,
        time: Optional[np.ndarray],
        space: Optional[np.ndarray],
        energy: Optional[np.ndarray],
    ) -> float:
        """Multi-dimensional integration."""
        result = integrand

        # Integrate over time if provided
        if time is not None and len(time) > 1:
            if self.integration_method == "trapezoidal":
                result = integrate.trapezoid(result, time, axis=-1)
            else:
                result = np.mean(result, axis=-1)

        # Integrate over space if provided
        if space is not None and len(space) > 1:
            if self.integration_method == "trapezoidal":
                result = integrate.trapezoid(result, space, axis=-1)
            else:
                result = np.mean(result, axis=-1)

        # Integrate over energy if provided
        if energy is not None and len(energy) > 1:
            if self.integration_method == "trapezoidal":
                result = integrate.trapezoid(result, energy, axis=-1)
            else:
                result = np.mean(result, axis=-1)

        return float(np.mean(result))

    def simulate_bipolar_episode(
        self, duration: int = 1000, episode_type: str = "manic", dt: float = 0.1
    ) -> Dict[str, np.ndarray]:
        """
        Simulate a bipolar episode trajectory.

        Args:
            duration: Simulation duration (time steps)
            episode_type: Episode type ("manic", "depressive", or "euthymic")
            dt: Time step size

        Returns:
            Dictionary with time series for Ψ and all operators
        """
        if episode_type not in ["manic", "depressive", "euthymic"]:
            raise ValueError(
                "episode_type must be 'manic', 'depressive', or 'euthymic'"
            )

        time = np.arange(0, duration) * dt

        # Set parameters based on episode type
        if episode_type == "manic":
            # Manic: high gamma, unstable theta, high delta, variable lambda
            plasticity = 1.2 + 0.3 * np.random.randn(duration)
            homeostasis = (
                0.5 + 0.2 * np.sin(0.1 * time) + 0.1 * np.random.randn(duration)
            )
            sync_variance = 0.6 + 0.2 * np.random.randn(duration)
            phase_alignment = (
                0.4 + 0.3 * np.sin(0.05 * time) + 0.1 * np.random.randn(duration)
            )
        elif episode_type == "depressive":
            # Depressive: low gamma, low theta, moderate delta, low lambda
            plasticity = 0.3 + 0.1 * np.random.randn(duration)
            homeostasis = 0.4 + 0.1 * np.random.randn(duration)
            sync_variance = 0.4 + 0.15 * np.random.randn(duration)
            phase_alignment = 0.3 + 0.1 * np.random.randn(duration)
        else:  # euthymic
            # Euthymic: balanced, stable
            plasticity = 0.8 + 0.05 * np.random.randn(duration)
            homeostasis = 0.85 + 0.05 * np.random.randn(duration)
            sync_variance = 0.2 + 0.05 * np.random.randn(duration)
            phase_alignment = 0.8 + 0.05 * np.random.randn(duration)

        # Clip to valid ranges
        plasticity = np.clip(plasticity, 0, 2)
        homeostasis = np.clip(homeostasis, 0, 1)
        sync_variance = np.clip(sync_variance, 0, 1)
        phase_alignment = np.clip(phase_alignment, 0, 1)

        # Calculate operators
        gamma_vals = np.zeros(duration)
        theta_vals = np.zeros(duration)
        delta_vals = np.zeros(duration)
        lambda_vals = np.zeros(duration)
        psi_vals = np.zeros(duration)

        for i in range(duration):
            gamma_res = self.gamma_op.calculate(plasticity[i], 0.5)
            theta_res = self.theta_op.calculate(homeostasis[i])
            delta_res = self.delta_op.calculate(sync_variance[i])
            lambda_res = self.lambda_op.calculate(phase_alignment[i])

            gamma_vals[i] = float(gamma_res)
            theta_vals[i] = float(theta_res)
            delta_vals[i] = float(delta_res)
            lambda_vals[i] = float(lambda_res)

            psi_res = self.calculate(gamma_res, theta_res, delta_res, lambda_res)
            psi_vals[i] = psi_res.psi

        return {
            "time": time,
            "psi": psi_vals,
            "gamma": gamma_vals,
            "theta": theta_vals,
            "delta": delta_vals,
            "lambda": lambda_vals,
            "episode_type": episode_type,
        }

    def simulate_recovery_curve(
        self,
        initial_psi: float = 0.3,
        target_psi: float = 0.85,
        duration: int = 500,
        recovery_rate: float = 0.01,
    ) -> Dict[str, np.ndarray]:
        """
        Simulate recovery dynamics from low to high Ψ.

        Args:
            initial_psi: Starting Ψ value
            target_psi: Target Ψ value
            duration: Simulation duration
            recovery_rate: Rate of recovery (0 to 1)

        Returns:
            Dictionary with recovery trajectory
        """
        time = np.arange(duration)

        # Exponential recovery with noise
        tau = 1.0 / recovery_rate
        psi_vals = target_psi - (target_psi - initial_psi) * np.exp(-time / tau)
        psi_vals += 0.02 * np.random.randn(duration)  # Small noise
        psi_vals = np.clip(psi_vals, 0, 1)

        return {
            "time": time,
            "psi": psi_vals,
            "initial_psi": initial_psi,
            "target_psi": target_psi,
            "recovery_rate": recovery_rate,
        }

    def apply_perturbation(
        self,
        baseline_trajectory: Dict[str, np.ndarray],
        perturbation_time: int,
        strength: float = 0.5,
        duration: int = 100,
    ) -> Dict[str, np.ndarray]:
        """
        Apply a perturbation to a baseline trajectory.

        Args:
            baseline_trajectory: Baseline simulation result
            perturbation_time: Time point to apply perturbation
            strength: Perturbation strength (0 to 1)
            duration: Duration of perturbation effect

        Returns:
            Perturbed trajectory
        """
        psi = baseline_trajectory["psi"].copy()
        time = baseline_trajectory["time"]

        # Create perturbation profile (Gaussian decay)
        t_perturb = np.arange(len(psi))
        perturbation_profile = strength * np.exp(
            -((t_perturb - perturbation_time) ** 2) / (2 * (duration / 3) ** 2)
        )

        # Apply perturbation (reduce Ψ)
        psi_perturbed = psi * (1.0 - perturbation_profile)

        return {
            "time": time,
            "psi": psi_perturbed,
            "psi_baseline": psi,
            "perturbation_profile": perturbation_profile,
            "perturbation_time": perturbation_time,
            "strength": strength,
        }

    def run_parameter_sweep(
        self, param_name: str, param_range: np.ndarray, fixed_params: Dict[str, float]
    ) -> Dict[str, np.ndarray]:
        """
        Run a parameter sweep to analyze Ψ sensitivity.

        Args:
            param_name: Name of parameter to sweep
            param_range: Array of parameter values to test
            fixed_params: Dictionary of fixed parameter values

        Returns:
            Dictionary with parameter values and corresponding Ψ values
        """
        psi_vals = np.zeros(len(param_range))

        for i, param_val in enumerate(param_range):
            # Update parameter
            params = fixed_params.copy()
            params[param_name] = param_val

            # Calculate operators with current parameters
            gamma = self.gamma_op.calculate(
                params.get("plasticity", 0.8), params.get("responsiveness", 0.5)
            )
            theta = self.theta_op.calculate(params.get("homeostasis", 0.9))
            delta = self.delta_op.calculate(params.get("sync_variance", 0.3))
            lambda_op = self.lambda_op.calculate(params.get("phase_alignment", 0.85))

            # Calculate Ψ
            psi_result = self.calculate(gamma, theta, delta, lambda_op)
            psi_vals[i] = psi_result.psi

        return {
            "param_name": param_name,
            "param_values": param_range,
            "psi_values": psi_vals,
        }
