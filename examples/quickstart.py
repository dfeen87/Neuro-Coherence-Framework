"""Quick start example for Neuro-Coherence Framework.

This script demonstrates the basic usage of the framework:
1. Calculate operators
2. Compute Ψ
3. Simulate bipolar episode
4. Visualize results
"""

import numpy as np
import matplotlib.pyplot as plt
from simulations.core import NeuroCoherence, Operators


def main():
    """Run quick start example."""
    print("=" * 60)
    print("Neuro-Coherence Framework - Quick Start")
    print("=" * 60)
    print()
    
    # 1. Calculate individual operators
    print("1. Calculating operators...")
    gamma = Operators.adaptive_gain(plasticity=0.8, responsiveness=0.5)
    print(f"   Γ (Adaptive Gain): {float(gamma):.4f}")
    
    theta = Operators.thermodynamic_stability(homeostasis=0.9)
    print(f"   Θ (Thermodynamic Stability): {float(theta):.4f}")
    
    delta = Operators.connectivity_variance(sync_variance=0.3)
    print(f"   Δ (Connectivity Variance): {float(delta):.4f}")
    
    lambda_op = Operators.spatiotemporal_coherence(phase_alignment=0.85)
    print(f"   Λ (Spatiotemporal Coherence): {float(lambda_op):.4f}")
    print()
    
    # 2. Compute Ψ
    print("2. Computing Neuro-Coherence Function (Ψ)...")
    nc = NeuroCoherence(phi=1.0)
    psi = nc.calculate(gamma, theta, delta, lambda_op)
    print(f"   {psi}")
    print()
    
    # 3. Simulate different states
    print("3. Simulating different states...")
    
    # Euthymic (balanced)
    euthymic = nc.simulate_bipolar_episode(
        duration=200,
        episode_type="euthymic",
        dt=0.1
    )
    print(f"   Euthymic Ψ (mean): {np.mean(euthymic['psi']):.4f}")
    
    # Manic episode
    manic = nc.simulate_bipolar_episode(
        duration=200,
        episode_type="manic",
        dt=0.1
    )
    print(f"   Manic Ψ (mean): {np.mean(manic['psi']):.4f}")
    
    # Depressive episode
    depressive = nc.simulate_bipolar_episode(
        duration=200,
        episode_type="depressive",
        dt=0.1
    )
    print(f"   Depressive Ψ (mean): {np.mean(depressive['psi']):.4f}")
    print()
    
    # 4. Simulate recovery
    print("4. Simulating recovery dynamics...")
    recovery = nc.simulate_recovery_curve(
        initial_psi=0.3,
        target_psi=0.85,
        duration=200,
        recovery_rate=0.02
    )
    print(f"   Initial Ψ: {recovery['psi'][0]:.4f}")
    print(f"   Final Ψ: {recovery['psi'][-1]:.4f}")
    print()
    
    # 5. Visualize results
    print("5. Creating visualizations...")
    
    fig, axes = plt.subplots(2, 2, figsize=(12, 8))
    fig.suptitle("Neuro-Coherence Framework - Quick Start Results", fontsize=14)
    
    # Plot 1: Ψ across states
    ax1 = axes[0, 0]
    ax1.plot(euthymic["time"], euthymic["psi"], label="Euthymic", linewidth=2)
    ax1.plot(manic["time"], manic["psi"], label="Manic", linewidth=2, alpha=0.7)
    ax1.plot(depressive["time"], depressive["psi"], label="Depressive", linewidth=2, alpha=0.7)
    ax1.set_xlabel("Time")
    ax1.set_ylabel("Ψ (Neuro-Coherence)")
    ax1.set_title("Ψ Across Different States")
    ax1.legend()
    ax1.grid(alpha=0.3)
    
    # Plot 2: Recovery curve
    ax2 = axes[0, 1]
    ax2.plot(recovery["time"], recovery["psi"], linewidth=2, color="green")
    ax2.axhline(y=recovery["target_psi"], color="red", linestyle="--", label="Target")
    ax2.axhline(y=recovery["initial_psi"], color="blue", linestyle="--", label="Initial")
    ax2.set_xlabel("Time")
    ax2.set_ylabel("Ψ (Neuro-Coherence)")
    ax2.set_title("Recovery Dynamics")
    ax2.legend()
    ax2.grid(alpha=0.3)
    
    # Plot 3: Operator contributions (euthymic)
    ax3 = axes[1, 0]
    operators_labels = ["Γ", "Θ", "1-Δ", "Λ"]
    operators_values = [
        np.mean(euthymic["gamma"]),
        np.mean(euthymic["theta"]),
        1 - np.mean(euthymic["delta"]),
        np.mean(euthymic["lambda"])
    ]
    bars = ax3.bar(operators_labels, operators_values, color=["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728"])
    ax3.set_ylabel("Value")
    ax3.set_title("Operator Values (Euthymic State)")
    ax3.set_ylim(0, 1.5)
    ax3.grid(axis="y", alpha=0.3)
    
    # Add values on bars
    for bar, val in zip(bars, operators_values):
        height = bar.get_height()
        ax3.text(bar.get_x() + bar.get_width()/2., height,
                f'{val:.3f}', ha='center', va='bottom')
    
    # Plot 4: State comparison
    ax4 = axes[1, 1]
    states = ["Euthymic", "Manic", "Depressive"]
    psi_means = [
        np.mean(euthymic["psi"]),
        np.mean(manic["psi"]),
        np.mean(depressive["psi"])
    ]
    bars = ax4.bar(states, psi_means, color=["green", "red", "blue"], alpha=0.7)
    ax4.set_ylabel("Mean Ψ")
    ax4.set_title("Ψ Comparison Across States")
    ax4.grid(axis="y", alpha=0.3)
    
    # Add values on bars
    for bar, val in zip(bars, psi_means):
        height = bar.get_height()
        ax4.text(bar.get_x() + bar.get_width()/2., height,
                f'{val:.3f}', ha='center', va='bottom')
    
    plt.tight_layout()
    
    # Save figure
    output_file = "quickstart_results.png"
    plt.savefig(output_file, dpi=150, bbox_inches="tight")
    print(f"   Figure saved to: {output_file}")
    print()
    
    print("=" * 60)
    print("Quick start complete!")
    print("=" * 60)
    print()
    print("Next steps:")
    print("  - Explore custom_simulation.py for advanced usage")
    print("  - See full_analysis.py for multimodal integration")
    print("  - Check docs/ for theoretical background")
    print()


if __name__ == "__main__":
    main()
