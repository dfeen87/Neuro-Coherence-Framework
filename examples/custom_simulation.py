"""Custom simulation example with advanced features.

This script demonstrates:
- Custom parameter configurations
- Perturbation experiments
- Parameter sensitivity analysis
- Recovery dynamics
- Advanced visualizations
"""

import numpy as np
import matplotlib.pyplot as plt
from simulations.core import NeuroCoherence, Operators


def run_perturbation_experiment():
    """Demonstrate perturbation and recovery."""
    print("Running perturbation experiment...")
    
    nc = NeuroCoherence()
    
    # Generate baseline euthymic trajectory
    baseline = nc.simulate_bipolar_episode(
        duration=500,
        episode_type="euthymic",
        dt=0.1
    )
    
    # Apply perturbations at different times
    perturbations = []
    perturbation_times = [100, 200, 300, 400]
    
    for t in perturbation_times:
        perturbed = nc.apply_perturbation(
            baseline_trajectory=baseline,
            perturbation_time=t,
            strength=0.6,
            duration=50
        )
        perturbations.append(perturbed)
    
    # Plot results
    fig, ax = plt.subplots(figsize=(12, 6))
    
    ax.plot(baseline["time"], baseline["psi"], 
            label="Baseline", linewidth=2, color="green", alpha=0.7)
    
    colors = plt.cm.Reds(np.linspace(0.4, 0.9, len(perturbations)))
    for i, (pert, t) in enumerate(zip(perturbations, perturbation_times)):
        ax.plot(pert["time"], pert["psi"], 
                label=f"Perturbation at t={t}", 
                linewidth=1.5, color=colors[i], alpha=0.8)
        ax.axvline(x=t, color=colors[i], linestyle="--", alpha=0.5)
    
    ax.set_xlabel("Time", fontsize=12)
    ax.set_ylabel("Ψ (Neuro-Coherence)", fontsize=12)
    ax.set_title("Multiple Perturbation Experiment", fontsize=14)
    ax.legend(loc="best")
    ax.grid(alpha=0.3)
    
    plt.tight_layout()
    plt.savefig("perturbation_experiment.png", dpi=150)
    print("Saved: perturbation_experiment.png\n")


def run_parameter_sensitivity():
    """Analyze parameter sensitivity."""
    print("Running parameter sensitivity analysis...")
    
    nc = NeuroCoherence()
    
    # Parameters to sweep
    parameters = {
        "plasticity": np.linspace(0.2, 1.5, 15),
        "homeostasis": np.linspace(0.5, 1.0, 15),
        "sync_variance": np.linspace(0.0, 0.8, 15),
        "phase_alignment": np.linspace(0.3, 1.0, 15),
    }
    
    # Fixed parameters for each sweep
    fixed_defaults = {
        "plasticity": 0.8,
        "responsiveness": 0.5,
        "homeostasis": 0.9,
        "sync_variance": 0.3,
        "phase_alignment": 0.85,
    }
    
    # Run sweeps
    results = {}
    for param_name, param_range in parameters.items():
        fixed_params = fixed_defaults.copy()
        result = nc.run_parameter_sweep(
            param_name=param_name,
            param_range=param_range,
            fixed_params=fixed_params
        )
        results[param_name] = result
    
    # Plot results
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    fig.suptitle("Parameter Sensitivity Analysis", fontsize=14)
    
    param_labels = {
        "plasticity": "Plasticity (Γ input)",
        "homeostasis": "Homeostasis (Θ input)",
        "sync_variance": "Sync Variance (Δ input)",
        "phase_alignment": "Phase Alignment (Λ input)",
    }
    
    for ax, (param_name, result) in zip(axes.flat, results.items()):
        ax.plot(result["param_values"], result["psi_values"], 
                linewidth=2, marker="o", markersize=4)
        ax.set_xlabel(param_labels[param_name], fontsize=11)
        ax.set_ylabel("Ψ (Neuro-Coherence)", fontsize=11)
        ax.set_title(f"Sensitivity to {param_name.capitalize()}", fontsize=12)
        ax.grid(alpha=0.3)
        
        # Mark default value
        default_val = fixed_defaults[param_name]
        default_idx = np.argmin(np.abs(result["param_values"] - default_val))
        default_psi = result["psi_values"][default_idx]
        ax.plot(default_val, default_psi, 'r*', markersize=15, 
                label=f"Default: {default_val:.2f}")
        ax.legend()
    
    plt.tight_layout()
    plt.savefig("parameter_sensitivity.png", dpi=150)
    print("Saved: parameter_sensitivity.png\n")


def run_recovery_comparison():
    """Compare recovery rates."""
    print("Running recovery rate comparison...")
    
    nc = NeuroCoherence()
    
    recovery_rates = [0.005, 0.01, 0.02, 0.05]
    colors = plt.cm.viridis(np.linspace(0.2, 0.9, len(recovery_rates)))
    
    fig, ax = plt.subplots(figsize=(10, 6))
    
    for rate, color in zip(recovery_rates, colors):
        recovery = nc.simulate_recovery_curve(
            initial_psi=0.25,
            target_psi=0.85,
            duration=300,
            recovery_rate=rate
        )
        
        ax.plot(recovery["time"], recovery["psi"], 
                label=f"Rate = {rate}", linewidth=2, color=color)
    
    ax.axhline(y=0.85, color="red", linestyle="--", 
               linewidth=1, alpha=0.5, label="Target")
    ax.axhline(y=0.25, color="blue", linestyle="--", 
               linewidth=1, alpha=0.5, label="Initial")
    
    ax.set_xlabel("Time", fontsize=12)
    ax.set_ylabel("Ψ (Neuro-Coherence)", fontsize=12)
    ax.set_title("Recovery Rate Comparison", fontsize=14)
    ax.legend(loc="best")
    ax.grid(alpha=0.3)
    
    plt.tight_layout()
    plt.savefig("recovery_comparison.png", dpi=150)
    print("Saved: recovery_comparison.png\n")


def run_operator_correlation():
    """Analyze operator correlations with Ψ."""
    print("Running operator correlation analysis...")
    
    nc = NeuroCoherence()
    
    # Generate varied parameter sets
    n_samples = 100
    plasticity = np.random.uniform(0.3, 1.2, n_samples)
    homeostasis = np.random.uniform(0.5, 1.0, n_samples)
    sync_variance = np.random.uniform(0.0, 0.7, n_samples)
    phase_alignment = np.random.uniform(0.4, 1.0, n_samples)
    
    # Calculate Ψ for each parameter set
    psi_values = np.zeros(n_samples)
    gamma_values = np.zeros(n_samples)
    theta_values = np.zeros(n_samples)
    delta_values = np.zeros(n_samples)
    lambda_values = np.zeros(n_samples)
    
    for i in range(n_samples):
        gamma = Operators.adaptive_gain(plasticity[i], 0.5)
        theta = Operators.thermodynamic_stability(homeostasis[i])
        delta = Operators.connectivity_variance(sync_variance[i])
        lambda_op = Operators.spatiotemporal_coherence(phase_alignment[i])
        
        psi = nc.calculate(gamma, theta, delta, lambda_op)
        
        psi_values[i] = psi.psi
        gamma_values[i] = float(gamma)
        theta_values[i] = float(theta)
        delta_values[i] = float(delta)
        lambda_values[i] = float(lambda_op)
    
    # Plot correlations
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    fig.suptitle("Operator vs Ψ Correlations", fontsize=14)
    
    operators = [
        ("Γ (Adaptive Gain)", gamma_values),
        ("Θ (Thermodynamic Stability)", theta_values),
        ("Δ (Connectivity Variance)", delta_values),
        ("Λ (Spatiotemporal Coherence)", lambda_values),
    ]
    
    for ax, (name, values) in zip(axes.flat, operators):
        ax.scatter(values, psi_values, alpha=0.6, s=30)
        
        # Add correlation coefficient
        corr = np.corrcoef(values, psi_values)[0, 1]
        ax.text(0.05, 0.95, f"r = {corr:.3f}", 
                transform=ax.transAxes, fontsize=11,
                verticalalignment='top',
                bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
        
        # Add trend line
        z = np.polyfit(values, psi_values, 1)
        p = np.poly1d(z)
        ax.plot(values, p(values), "r--", alpha=0.8, linewidth=2)
        
        ax.set_xlabel(name, fontsize=11)
        ax.set_ylabel("Ψ", fontsize=11)
        ax.grid(alpha=0.3)
    
    plt.tight_layout()
    plt.savefig("operator_correlations.png", dpi=150)
    print("Saved: operator_correlations.png\n")


def main():
    """Run all custom simulations."""
    print("=" * 60)
    print("Neuro-Coherence Framework - Custom Simulations")
    print("=" * 60)
    print()
    
    run_perturbation_experiment()
    run_parameter_sensitivity()
    run_recovery_comparison()
    run_operator_correlation()
    
    print("=" * 60)
    print("All simulations complete!")
    print("=" * 60)
    print()
    print("Generated files:")
    print("  - perturbation_experiment.png")
    print("  - parameter_sensitivity.png")
    print("  - recovery_comparison.png")
    print("  - operator_correlations.png")
    print()


if __name__ == "__main__":
    main()
