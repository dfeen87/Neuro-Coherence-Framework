"""
Core operators for the Neuro-Coherence Framework.

This module implements the four fundamental operators:
- Γ (Gamma): Adaptive Gain (neuroplasticity)
- Θ (Theta): Thermodynamic Stability (metabolic homeostasis)
- Δ_GR (Delta): Generalized Regional Differential (network variance)
- Λ (Lambda): Spatiotemporal Coherence Density (phase alignment)
"""

from typing import Union, Optional
import numpy as np
from dataclasses import dataclass


@dataclass
class OperatorResult:
    """Container for operator results with metadata."""
    value: Union[float, np.ndarray]
    operator_name: str
    parameters: dict
    
    def __float__(self):
        """Convert to float for numerical operations."""
        if isinstance(self.value, np.ndarray):
            return float(np.mean(self.value))
        return float(self.value)


class AdaptiveGain:
    """
    Adaptive Gain Operator (Γ)
    
    Models neuroplastic responsiveness and adaptive capacity.
    Represents the system's ability to modulate gain in response to input.
    
    Mathematical form:
        Γ(t) = γ₀ · (1 + α · tanh(β · R(t)))
    
    Where:
        γ₀: baseline gain
        α: plasticity coefficient
        β: responsiveness rate
        R(t): responsiveness signal
    """
    
    def __init__(self, baseline_gain: float = 1.0):
        """
        Initialize Adaptive Gain operator.
        
        Args:
            baseline_gain: Baseline gain coefficient (default: 1.0)
        """
        if baseline_gain <= 0:
            raise ValueError("baseline_gain must be positive")
        self.baseline_gain = baseline_gain
    
    def calculate(
        self,
        plasticity: float,
        responsiveness: Union[float, np.ndarray],
        time: Optional[np.ndarray] = None
    ) -> OperatorResult:
        """
        Calculate adaptive gain.
        
        Args:
            plasticity: Plasticity coefficient (0 to 1, typically)
            responsiveness: Responsiveness signal(s)
            time: Optional time array for temporal dynamics
            
        Returns:
            OperatorResult with gain values
            
        Raises:
            ValueError: If plasticity is negative or responsiveness invalid
        """
        if plasticity < 0:
            raise ValueError("plasticity must be non-negative")
        
        # Ensure responsiveness is numpy array
        R = np.asarray(responsiveness)
        
        # Adaptive gain with saturation
        alpha = np.clip(plasticity, 0, 2.0)  # Cap at 2.0 for stability
        beta = 1.0  # Responsiveness rate
        
        gamma = self.baseline_gain * (1.0 + alpha * np.tanh(beta * R))
        
        # Ensure non-negative
        gamma = np.maximum(gamma, 0.0)
        
        return OperatorResult(
            value=gamma,
            operator_name="AdaptiveGain",
            parameters={
                "baseline_gain": self.baseline_gain,
                "plasticity": plasticity,
                "responsiveness_mean": float(np.mean(R)),
            }
        )


class ThermodynamicStability:
    """
    Thermodynamic Stability Operator (Θ)
    
    Models metabolic homeostasis and bioenergetic stability.
    Represents the system's capacity to maintain stable energy dynamics.
    
    Mathematical form:
        Θ(E) = exp(-λ · |E - E₀|²)
    
    Where:
        E: current metabolic state
        E₀: homeostatic setpoint
        λ: stability coefficient
    """
    
    def __init__(self, setpoint: float = 1.0, stability_coeff: float = 1.0):
        """
        Initialize Thermodynamic Stability operator.
        
        Args:
            setpoint: Homeostatic energy setpoint
            stability_coeff: Stability decay coefficient
        """
        if setpoint <= 0:
            raise ValueError("setpoint must be positive")
        if stability_coeff <= 0:
            raise ValueError("stability_coeff must be positive")
            
        self.setpoint = setpoint
        self.stability_coeff = stability_coeff
    
    def calculate(
        self,
        homeostasis: Union[float, np.ndarray],
        atp_production: Optional[Union[float, np.ndarray]] = None,
        ocr: Optional[Union[float, np.ndarray]] = None
    ) -> OperatorResult:
        """
        Calculate thermodynamic stability.
        
        Args:
            homeostasis: Homeostatic balance metric (0 to 1)
            atp_production: Optional ATP production rate
            ocr: Optional oxygen consumption rate
            
        Returns:
            OperatorResult with stability coefficient
            
        Raises:
            ValueError: If homeostasis is outside valid range
        """
        H = np.asarray(homeostasis)
        
        if np.any(H < 0) or np.any(H > 1):
            raise ValueError("homeostasis must be in range [0, 1]")
        
        # Base stability from homeostasis
        theta = np.exp(-self.stability_coeff * (H - self.setpoint)**2)
        
        # Adjust for ATP if provided
        if atp_production is not None:
            atp = np.asarray(atp_production)
            atp_factor = np.clip(atp, 0.5, 1.5)  # Normalize around 1.0
            theta *= atp_factor
        
        # Adjust for OCR if provided
        if ocr is not None:
            ocr_arr = np.asarray(ocr)
            ocr_factor = np.clip(ocr_arr, 0.5, 1.5)
            theta *= ocr_factor
        
        # Ensure valid range
        theta = np.clip(theta, 0.0, 1.0)
        
        return OperatorResult(
            value=theta,
            operator_name="ThermodynamicStability",
            parameters={
                "setpoint": self.setpoint,
                "stability_coeff": self.stability_coeff,
                "homeostasis_mean": float(np.mean(H)),
            }
        )


class ConnectivityVariance:
    """
    Connectivity Variance Operator (Δ_GR)
    
    Models network synchronization variance across regions.
    Represents deviations from optimal network coherence.
    
    Mathematical form:
        Δ_GR = σ²(C) / (1 + σ²(C))
    
    Where:
        σ²(C): variance of connectivity across networks
    """
    
    def __init__(self, normalization: str = "sigmoid"):
        """
        Initialize Connectivity Variance operator.
        
        Args:
            normalization: Method for normalizing variance ("sigmoid" or "linear")
        """
        if normalization not in ["sigmoid", "linear"]:
            raise ValueError("normalization must be 'sigmoid' or 'linear'")
        self.normalization = normalization
    
    def calculate(
        self,
        sync_variance: Union[float, np.ndarray],
        network_metrics: Optional[dict] = None
    ) -> OperatorResult:
        """
        Calculate connectivity variance penalty.
        
        Args:
            sync_variance: Synchronization variance across regions
            network_metrics: Optional dict with DMN, SN, CEN connectivity
            
        Returns:
            OperatorResult with normalized variance
            
        Raises:
            ValueError: If sync_variance is negative
        """
        var = np.asarray(sync_variance)
        
        if np.any(var < 0):
            raise ValueError("sync_variance must be non-negative")
        
        # Normalize variance to [0, 1]
        if self.normalization == "sigmoid":
            delta = var / (1.0 + var)
        else:  # linear
            delta = np.clip(var, 0.0, 1.0)
        
        # Adjust for network metrics if provided
        if network_metrics is not None:
            # Calculate inter-network variance
            networks = []
            for net in ["DMN", "SN", "CEN"]:
                if net in network_metrics:
                    networks.append(network_metrics[net])
            
            if len(networks) >= 2:
                net_variance = np.var(networks)
                delta = delta * (1.0 + 0.5 * net_variance)  # Amplify if networks diverge
                delta = np.clip(delta, 0.0, 1.0)
        
        return OperatorResult(
            value=delta,
            operator_name="ConnectivityVariance",
            parameters={
                "normalization": self.normalization,
                "sync_variance_mean": float(np.mean(var)),
            }
        )


class SpatiotemporalCoherence:
    """
    Spatiotemporal Coherence Density Operator (Λ)
    
    Models phase alignment and coherence across space and time.
    Represents the system's capacity for synchronized information flow.
    
    Mathematical form:
        Λ(r,t) = ⟨PLV(r,t)⟩ · (1 - GPLI_variance)
    
    Where:
        PLV: Phase Locking Value
        GPLI: Generalized Phase Lag Index
    """
    
    def __init__(self, coherence_threshold: float = 0.1):
        """
        Initialize Spatiotemporal Coherence operator.
        
        Args:
            coherence_threshold: Minimum coherence threshold
        """
        if coherence_threshold < 0 or coherence_threshold > 1:
            raise ValueError("coherence_threshold must be in [0, 1]")
        self.coherence_threshold = coherence_threshold
    
    def calculate(
        self,
        phase_alignment: Union[float, np.ndarray],
        plv: Optional[Union[float, np.ndarray]] = None,
        gpli: Optional[Union[float, np.ndarray]] = None
    ) -> OperatorResult:
        """
        Calculate spatiotemporal coherence density.
        
        Args:
            phase_alignment: Phase alignment metric (0 to 1)
            plv: Optional Phase Locking Value array
            gpli: Optional Generalized Phase Lag Index array
            
        Returns:
            OperatorResult with coherence density
            
        Raises:
            ValueError: If phase_alignment outside valid range
        """
        PA = np.asarray(phase_alignment)
        
        if np.any(PA < 0) or np.any(PA > 1):
            raise ValueError("phase_alignment must be in range [0, 1]")
        
        # Base coherence from phase alignment
        lambda_val = PA
        
        # Enhance with PLV if provided
        if plv is not None:
            plv_arr = np.asarray(plv)
            plv_mean = np.mean(plv_arr)
            lambda_val = lambda_val * plv_mean
        
        # Adjust for GPLI variance if provided
        if gpli is not None:
            gpli_arr = np.asarray(gpli)
            gpli_var = np.var(gpli_arr)
            lambda_val = lambda_val * (1.0 - np.clip(gpli_var, 0, 0.5))
        
        # Apply threshold
        lambda_val = np.where(lambda_val < self.coherence_threshold, 
                             self.coherence_threshold, 
                             lambda_val)
        
        # Ensure valid range
        lambda_val = np.clip(lambda_val, 0.0, 1.0)
        
        return OperatorResult(
            value=lambda_val,
            operator_name="SpatiotemporalCoherence",
            parameters={
                "coherence_threshold": self.coherence_threshold,
                "phase_alignment_mean": float(np.mean(PA)),
            }
        )


class Operators:
    """
    Convenience class for accessing all operators.
    
    Example:
        >>> ops = Operators()
        >>> gamma = ops.adaptive_gain(plasticity=0.8, responsiveness=0.5)
        >>> theta = ops.thermodynamic_stability(homeostasis=0.9)
    """
    
    @staticmethod
    def adaptive_gain(
        plasticity: float,
        responsiveness: Union[float, np.ndarray] = 0.5,
        baseline_gain: float = 1.0,
        time: Optional[np.ndarray] = None
    ) -> OperatorResult:
        """Calculate adaptive gain (Γ)."""
        op = AdaptiveGain(baseline_gain=baseline_gain)
        return op.calculate(plasticity, responsiveness, time)
    
    @staticmethod
    def thermodynamic_stability(
        homeostasis: Union[float, np.ndarray],
        atp_production: Optional[Union[float, np.ndarray]] = None,
        ocr: Optional[Union[float, np.ndarray]] = None,
        setpoint: float = 1.0,
        stability_coeff: float = 1.0
    ) -> OperatorResult:
        """Calculate thermodynamic stability (Θ)."""
        op = ThermodynamicStability(setpoint=setpoint, stability_coeff=stability_coeff)
        return op.calculate(homeostasis, atp_production, ocr)
    
    @staticmethod
    def connectivity_variance(
        sync_variance: Union[float, np.ndarray],
        network_metrics: Optional[dict] = None,
        normalization: str = "sigmoid"
    ) -> OperatorResult:
        """Calculate connectivity variance (Δ_GR)."""
        op = ConnectivityVariance(normalization=normalization)
        return op.calculate(sync_variance, network_metrics)
    
    @staticmethod
    def spatiotemporal_coherence(
        phase_alignment: Union[float, np.ndarray],
        plv: Optional[Union[float, np.ndarray]] = None,
        gpli: Optional[Union[float, np.ndarray]] = None,
        coherence_threshold: float = 0.1
    ) -> OperatorResult:
        """Calculate spatiotemporal coherence density (Λ)."""
        op = SpatiotemporalCoherence(coherence_threshold=coherence_threshold)
        return op.calculate(phase_alignment, plv, gpli)
