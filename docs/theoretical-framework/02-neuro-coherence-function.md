# Neuro-Coherence Function (Ψ)

## Mathematical Formulation

The Neuro-Coherence Function is defined as:

```
Ψ = Φ · ∫∫∫ [ Θ(E) · Γ(t) · (1 − Δ_GR) · Λ(r,t) ] dE dr dt
```

Where:
- **Φ**: Global modulation coefficient
- **Θ(E)**: Thermodynamic stability operator
- **Γ(t)**: Adaptive gain (neuroplasticity)
- **Δ_GR**: Generalized regional differential (network variance)
- **Λ(r,t)**: Spatiotemporal coherence density

## Interpretation

Ψ quantifies the system's capacity to maintain **resilient, coherent information flow** across neural, metabolic, and network domains.

### High Ψ (> 0.7)
- Robust phase alignment across networks
- Stable metabolic homeostasis
- Adaptive neuroplastic response
- Low network variance
- Characteristic of euthymic states

### Low Ψ (< 0.4)
- Disrupted phase coherence
- Metabolic instability
- Impaired adaptive capacity
- High network variance
- Characteristic of mood episodes

## Operator Contributions

Each operator captures a distinct biophysical dimension:

### Θ (Thermodynamic Stability)
- **Domain**: Metabolic homeostasis
- **Range**: [0, 1]
- **Interpretation**: Energy system stability
- **Biomarkers**: ATP production, OCR, lactate levels

### Γ (Adaptive Gain)
- **Domain**: Neuroplasticity
- **Range**: [0, ∞) (typically 0-2)
- **Interpretation**: System's adaptive responsiveness
- **Biomarkers**: PLV recovery, synaptic markers

### Δ_GR (Connectivity Variance)
- **Domain**: Network synchronization
- **Range**: [0, 1]
- **Interpretation**: Deviation from optimal coherence (penalty term)
- **Biomarkers**: fMRI connectivity variance, DMN-SN-CEN metrics

### Λ (Spatiotemporal Coherence)
- **Domain**: Phase alignment
- **Range**: [0, 1]
- **Interpretation**: Information flow coordination
- **Biomarkers**: PLV, GPLI, cross-frequency coupling

## Integration Formula

The integrand represents the **instantaneous coherence capacity**:

```
I(E, r, t) = Θ(E) · Γ(t) · (1 − Δ_GR) · Λ(r,t)
```

Key properties:
- **Multiplicative**: All operators must be non-zero for coherence
- **Balanced**: No single operator dominates
- **Normalized**: Typical range [0, 1] for each operator
- **Global modulation**: Φ scales the integrated result

## Computational Implementation

### Discrete Approximation

In practice, we use discrete sampling:

```python
Ψ ≈ Φ · mean(Θ[i] · Γ[j] · (1 - Δ[k]) · Λ[l])
```

Where indices represent samples across energy, time, and space.

### Numerical Stability

- Operators are clipped to valid ranges
- Division protected against zeros
- Integration uses robust numerical methods (trapezoidal, Simpson)

## Clinical Interpretation

### Euthymia
- **Ψ**: 0.7 - 1.0
- **Characteristics**: All operators balanced and stable

### Manic Episode
- **Ψ**: 0.3 - 0.6
- **Drivers**: Elevated Γ, reduced Λ, increased Δ
- **Interpretation**: Excessive gain without coordination

### Depressive Episode
- **Ψ**: 0.1 - 0.4
- **Drivers**: Reduced Θ and Γ, variable Δ and Λ
- **Interpretation**: Energy deficit and reduced responsiveness

## Validation Strategy

Three key predictions must hold:

1. **Ψ inversely correlates with symptom severity**
   - Measured via clinical scales (YMRS, MADRS)
   - Expected r < -0.6

2. **Ψ predicts episode recovery**
   - Rising Ψ precedes clinical improvement
   - Time lag: 1-2 weeks

3. **Multi-operator integration required**
   - Single operators insufficient for prediction
   - ΔR² > 0.3 for full vs. single-operator models

## References

1. Original framework paper (see `papers/`)
2. Network neuroscience foundations
3. Phase coherence theory
4. Metabolic psychiatry literature
