"""Tests for core operators."""

import pytest
import numpy as np
from simulations.core.operators import (
    AdaptiveGain,
    ThermodynamicStability,
    ConnectivityVariance,
    SpatiotemporalCoherence,
    Operators,
    OperatorResult,
)


class TestAdaptiveGain:
    """Tests for Adaptive Gain operator (Γ)."""

    def test_initialization(self):
        """Test operator initialization."""
        op = AdaptiveGain()
        assert op.baseline_gain == 1.0

        op_custom = AdaptiveGain(baseline_gain=1.5)
        assert op_custom.baseline_gain == 1.5

    def test_invalid_initialization(self):
        """Test invalid initialization parameters."""
        with pytest.raises(ValueError):
            AdaptiveGain(baseline_gain=-1.0)
        with pytest.raises(ValueError):
            AdaptiveGain(baseline_gain=0.0)

    def test_calculate_basic(self):
        """Test basic calculation."""
        op = AdaptiveGain()
        result = op.calculate(plasticity=0.8, responsiveness=0.5)

        assert isinstance(result, OperatorResult)
        assert result.operator_name == "AdaptiveGain"
        assert result.value >= 0
        assert "plasticity" in result.parameters

    def test_calculate_array(self):
        """Test calculation with array input."""
        op = AdaptiveGain()
        responsiveness = np.array([0.3, 0.5, 0.7])
        result = op.calculate(plasticity=0.8, responsiveness=responsiveness)

        assert isinstance(result.value, np.ndarray)
        assert len(result.value) == 3
        assert np.all(result.value >= 0)

    def test_invalid_plasticity(self):
        """Test invalid plasticity value."""
        op = AdaptiveGain()
        with pytest.raises(ValueError):
            op.calculate(plasticity=-0.5, responsiveness=0.5)

    def test_saturation(self):
        """Test that extreme plasticity is handled."""
        op = AdaptiveGain()
        result = op.calculate(plasticity=10.0, responsiveness=0.5)
        assert result.value < 10.0  # Should saturate


class TestThermodynamicStability:
    """Tests for Thermodynamic Stability operator (Θ)."""

    def test_initialization(self):
        """Test operator initialization."""
        op = ThermodynamicStability()
        assert op.setpoint == 1.0
        assert op.stability_coeff == 1.0

    def test_calculate_basic(self):
        """Test basic calculation."""
        op = ThermodynamicStability()
        result = op.calculate(homeostasis=0.9)

        assert isinstance(result, OperatorResult)
        assert result.operator_name == "ThermodynamicStability"
        assert 0 <= result.value <= 1

    def test_calculate_with_atp(self):
        """Test calculation with ATP production."""
        op = ThermodynamicStability()
        result = op.calculate(homeostasis=0.9, atp_production=1.2)

        assert 0 <= result.value <= 1.5  # Can exceed 1 with ATP boost

    def test_invalid_homeostasis(self):
        """Test invalid homeostasis value."""
        op = ThermodynamicStability()
        with pytest.raises(ValueError):
            op.calculate(homeostasis=1.5)
        with pytest.raises(ValueError):
            op.calculate(homeostasis=-0.1)

    def test_array_input(self):
        """Test with array input."""
        op = ThermodynamicStability()
        homeostasis = np.array([0.7, 0.8, 0.9])
        result = op.calculate(homeostasis=homeostasis)

        assert isinstance(result.value, np.ndarray)
        assert len(result.value) == 3


class TestConnectivityVariance:
    """Tests for Connectivity Variance operator (Δ_GR)."""

    def test_initialization(self):
        """Test operator initialization."""
        op = ConnectivityVariance()
        assert op.normalization == "sigmoid"

        op_linear = ConnectivityVariance(normalization="linear")
        assert op_linear.normalization == "linear"

    def test_calculate_basic(self):
        """Test basic calculation."""
        op = ConnectivityVariance()
        result = op.calculate(sync_variance=0.3)

        assert isinstance(result, OperatorResult)
        assert result.operator_name == "ConnectivityVariance"
        assert 0 <= result.value <= 1

    def test_sigmoid_normalization(self):
        """Test sigmoid normalization."""
        op = ConnectivityVariance(normalization="sigmoid")

        result_low = op.calculate(sync_variance=0.1)
        result_high = op.calculate(sync_variance=10.0)

        assert result_low.value < result_high.value
        assert result_high.value < 1.0  # Sigmoid bounded

    def test_linear_normalization(self):
        """Test linear normalization."""
        op = ConnectivityVariance(normalization="linear")
        result = op.calculate(sync_variance=0.5)

        assert result.value == 0.5

    def test_negative_variance(self):
        """Test that negative variance raises error."""
        op = ConnectivityVariance()
        with pytest.raises(ValueError):
            op.calculate(sync_variance=-0.1)


class TestSpatiotemporalCoherence:
    """Tests for Spatiotemporal Coherence operator (Λ)."""

    def test_initialization(self):
        """Test operator initialization."""
        op = SpatiotemporalCoherence()
        assert op.coherence_threshold == 0.1

    def test_calculate_basic(self):
        """Test basic calculation."""
        op = SpatiotemporalCoherence()
        result = op.calculate(phase_alignment=0.85)

        assert isinstance(result, OperatorResult)
        assert result.operator_name == "SpatiotemporalCoherence"
        assert 0 <= result.value <= 1

    def test_calculate_with_plv(self):
        """Test calculation with PLV."""
        op = SpatiotemporalCoherence()
        result = op.calculate(phase_alignment=0.8, plv=0.9)

        # With PLV, value should be modulated
        assert 0 <= result.value <= 1

    def test_threshold_application(self):
        """Test that threshold is applied."""
        op = SpatiotemporalCoherence(coherence_threshold=0.3)
        result = op.calculate(phase_alignment=0.1)

        assert result.value >= 0.3  # Should be clipped to threshold

    def test_invalid_phase_alignment(self):
        """Test invalid phase alignment."""
        op = SpatiotemporalCoherence()
        with pytest.raises(ValueError):
            op.calculate(phase_alignment=1.5)
        with pytest.raises(ValueError):
            op.calculate(phase_alignment=-0.1)


class TestOperatorsConvenience:
    """Tests for Operators convenience class."""

    def test_adaptive_gain(self):
        """Test adaptive_gain convenience method."""
        result = Operators.adaptive_gain(plasticity=0.8)
        assert isinstance(result, OperatorResult)
        assert result.operator_name == "AdaptiveGain"

    def test_thermodynamic_stability(self):
        """Test thermodynamic_stability convenience method."""
        result = Operators.thermodynamic_stability(homeostasis=0.9)
        assert isinstance(result, OperatorResult)
        assert result.operator_name == "ThermodynamicStability"

    def test_connectivity_variance(self):
        """Test connectivity_variance convenience method."""
        result = Operators.connectivity_variance(sync_variance=0.3)
        assert isinstance(result, OperatorResult)
        assert result.operator_name == "ConnectivityVariance"

    def test_spatiotemporal_coherence(self):
        """Test spatiotemporal_coherence convenience method."""
        result = Operators.spatiotemporal_coherence(phase_alignment=0.85)
        assert isinstance(result, OperatorResult)
        assert result.operator_name == "SpatiotemporalCoherence"


class TestOperatorResult:
    """Tests for OperatorResult dataclass."""

    def test_float_conversion_scalar(self):
        """Test conversion to float for scalar value."""
        result = OperatorResult(value=0.75, operator_name="Test", parameters={})
        assert float(result) == 0.75

    def test_float_conversion_array(self):
        """Test conversion to float for array value."""
        result = OperatorResult(
            value=np.array([0.6, 0.7, 0.8]), operator_name="Test", parameters={}
        )
        assert abs(float(result) - 0.7) < 0.01  # Mean of array
