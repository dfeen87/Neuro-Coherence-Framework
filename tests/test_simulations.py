"""Tests for Neuro-Coherence simulations."""

import pytest
import numpy as np
from simulations.core import (
    NeuroCoherence,
    PsiResult,
    Operators,
)


class TestNeuroCoherence:
    """Tests for NeuroCoherence class."""
    
    def test_initialization(self):
        """Test initialization."""
        nc = NeuroCoherence()
        assert nc.phi == 1.0
        assert nc.integration_method == "trapezoidal"
        
        nc_custom = NeuroCoherence(phi=1.5, integration_method="mean")
        assert nc_custom.phi == 1.5
        assert nc_custom.integration_method == "mean"
    
    def test_invalid_initialization(self):
        """Test invalid initialization."""
        with pytest.raises(ValueError):
            NeuroCoherence(phi=-1.0)
        with pytest.raises(ValueError):
            NeuroCoherence(integration_method="invalid")
    
    def test_calculate_basic(self):
        """Test basic Ψ calculation."""
        nc = NeuroCoherence()
        
        gamma = Operators.adaptive_gain(plasticity=0.8)
        theta = Operators.thermodynamic_stability(homeostasis=0.9)
        delta = Operators.connectivity_variance(sync_variance=0.3)
        lambda_op = Operators.spatiotemporal_coherence(phase_alignment=0.85)
        
        result = nc.calculate(gamma, theta, delta, lambda_op)
        
        assert isinstance(result, PsiResult)
        assert result.psi >= 0
        assert result.phi == 1.0
        assert 0 <= result.gamma_mean <= 5
        assert 0 <= result.theta_mean <= 1
        assert 0 <= result.delta_mean <= 1
        assert 0 <= result.lambda_mean <= 1
    
    def test_calculate_with_scalars(self):
        """Test Ψ calculation with scalar inputs."""
        nc = NeuroCoherence()
        
        result = nc.calculate(
            gamma=1.2,
            theta=0.9,
            delta=0.3,
            lambda_op=0.85
        )
        
        assert isinstance(result, PsiResult)
        assert result.psi >= 0
    
    def test_calculate_with_arrays(self):
        """Test Ψ calculation with array inputs."""
        nc = NeuroCoherence()
        
        n = 10
        result = nc.calculate(
            gamma=np.ones(n) * 1.2,
            theta=np.ones(n) * 0.9,
            delta=np.ones(n) * 0.3,
            lambda_op=np.ones(n) * 0.85
        )
        
        assert isinstance(result, PsiResult)
        assert result.psi >= 0
    
    def test_phi_modulation(self):
        """Test that phi modulates Ψ correctly."""
        gamma = 1.0
        theta = 0.9
        delta = 0.3
        lambda_op = 0.85
        
        nc1 = NeuroCoherence(phi=1.0)
        psi1 = nc1.calculate(gamma, theta, delta, lambda_op)
        
        nc2 = NeuroCoherence(phi=2.0)
        psi2 = nc2.calculate(gamma, theta, delta, lambda_op)
        
        assert abs(psi2.psi - 2.0 * psi1.psi) < 0.01
    
    def test_invalid_operator_values(self):
        """Test that invalid operator values raise errors."""
        nc = NeuroCoherence()
        
        # Negative gamma
        with pytest.raises(ValueError):
            nc.calculate(gamma=-0.5, theta=0.9, delta=0.3, lambda_op=0.85)
        
        # Theta out of range
        with pytest.raises(ValueError):
            nc.calculate(gamma=1.0, theta=1.5, delta=0.3, lambda_op=0.85)
        
        # Delta out of range
        with pytest.raises(ValueError):
            nc.calculate(gamma=1.0, theta=0.9, delta=-0.1, lambda_op=0.85)
        
        # Lambda out of range
        with pytest.raises(ValueError):
            nc.calculate(gamma=1.0, theta=0.9, delta=0.3, lambda_op=1.5)
    
    def test_psi_result_str(self):
        """Test PsiResult string representation."""
        result = PsiResult(
            psi=0.75,
            phi=1.0,
            gamma_mean=1.2,
            theta_mean=0.9,
            delta_mean=0.3,
            lambda_mean=0.85,
            metadata={}
        )
        
        str_repr = str(result)
        assert "0.75" in str_repr
        assert "Φ=1.00" in str_repr
    
    def test_psi_result_float_conversion(self):
        """Test PsiResult conversion to float."""
        result = PsiResult(
            psi=0.75,
            phi=1.0,
            gamma_mean=1.2,
            theta_mean=0.9,
            delta_mean=0.3,
            lambda_mean=0.85,
            metadata={}
        )
        
        assert float(result) == 0.75


class TestBipolarSimulation:
    """Tests for bipolar episode simulation."""
    
    def test_simulate_manic(self):
        """Test manic episode simulation."""
        nc = NeuroCoherence()
        result = nc.simulate_bipolar_episode(duration=100, episode_type="manic")
        
        assert "time" in result
        assert "psi" in result
        assert "gamma" in result
        assert "theta" in result
        assert "delta" in result
        assert "lambda" in result
        assert result["episode_type"] == "manic"
        assert len(result["psi"]) == 100
    
    def test_simulate_depressive(self):
        """Test depressive episode simulation."""
        nc = NeuroCoherence()
        result = nc.simulate_bipolar_episode(duration=100, episode_type="depressive")
        
        assert result["episode_type"] == "depressive"
        assert len(result["psi"]) == 100
        
        # Depressive should have generally lower Ψ than euthymic
        assert np.mean(result["psi"]) < 0.8
    
    def test_simulate_euthymic(self):
        """Test euthymic state simulation."""
        nc = NeuroCoherence()
        result = nc.simulate_bipolar_episode(duration=100, episode_type="euthymic")
        
        assert result["episode_type"] == "euthymic"
        
        # Euthymic should have stable, higher Ψ
        assert np.mean(result["psi"]) > 0.3
        assert np.std(result["psi"]) < 0.5  # Relatively stable
    
    def test_invalid_episode_type(self):
        """Test invalid episode type."""
        nc = NeuroCoherence()
        with pytest.raises(ValueError):
            nc.simulate_bipolar_episode(duration=100, episode_type="invalid")


class TestRecoverySimulation:
    """Tests for recovery curve simulation."""
    
    def test_simulate_recovery(self):
        """Test recovery simulation."""
        nc = NeuroCoherence()
        result = nc.simulate_recovery_curve(
            initial_psi=0.3,
            target_psi=0.85,
            duration=100
        )
        
        assert "time" in result
        assert "psi" in result
        assert len(result["psi"]) == 100
        
        # Should generally increase
        assert result["psi"][0] < result["psi"][-1]
    
    def test_recovery_rate_effect(self):
        """Test that recovery rate affects trajectory."""
        nc = NeuroCoherence()
        
        slow = nc.simulate_recovery_curve(
            initial_psi=0.3,
            target_psi=0.85,
            duration=100,
            recovery_rate=0.005
        )
        
        fast = nc.simulate_recovery_curve(
            initial_psi=0.3,
            target_psi=0.85,
            duration=100,
            recovery_rate=0.05
        )
        
        # Fast recovery should reach target sooner
        assert fast["psi"][50] > slow["psi"][50]


class TestPerturbation:
    """Tests for perturbation application."""
    
    def test_apply_perturbation(self):
        """Test perturbation application."""
        nc = NeuroCoherence()
        
        # Create baseline
        baseline = nc.simulate_bipolar_episode(duration=200, episode_type="euthymic")
        
        # Apply perturbation
        perturbed = nc.apply_perturbation(
            baseline_trajectory=baseline,
            perturbation_time=100,
            strength=0.5,
            duration=50
        )
        
        assert "psi" in perturbed
        assert "psi_baseline" in perturbed
        assert "perturbation_profile" in perturbed
        
        # Perturbed should be lower at perturbation time
        assert perturbed["psi"][100] < baseline["psi"][100]
    
    def test_perturbation_strength(self):
        """Test that perturbation strength affects magnitude."""
        nc = NeuroCoherence()
        baseline = nc.simulate_bipolar_episode(duration=200, episode_type="euthymic")
        
        weak = nc.apply_perturbation(
            baseline_trajectory=baseline,
            perturbation_time=100,
            strength=0.2
        )
        
        strong = nc.apply_perturbation(
            baseline_trajectory=baseline,
            perturbation_time=100,
            strength=0.8
        )
        
        # Strong perturbation should reduce Ψ more
        assert strong["psi"][100] < weak["psi"][100]


class TestParameterSweep:
    """Tests for parameter sweep."""
    
    def test_parameter_sweep(self):
        """Test parameter sweep functionality."""
        nc = NeuroCoherence()
        
        param_range = np.linspace(0, 1, 10)
        result = nc.run_parameter_sweep(
            param_name="plasticity",
            param_range=param_range,
            fixed_params={
                "responsiveness": 0.5,
                "homeostasis": 0.9,
                "sync_variance": 0.3,
                "phase_alignment": 0.85
            }
        )
        
        assert "param_name" in result
        assert "param_values" in result
        assert "psi_values" in result
        assert len(result["psi_values"]) == 10
    
    def test_parameter_sweep_monotonicity(self):
        """Test that increasing plasticity increases Ψ."""
        nc = NeuroCoherence()
        
        param_range = np.linspace(0.2, 1.0, 5)
        result = nc.run_parameter_sweep(
            param_name="plasticity",
            param_range=param_range,
            fixed_params={
                "responsiveness": 0.5,
                "homeostasis": 0.9,
                "sync_variance": 0.2,
                "phase_alignment": 0.85
            }
        )
        
        # Generally should increase
        psi_vals = result["psi_values"]
        assert psi_vals[-1] > psi_vals[0]
