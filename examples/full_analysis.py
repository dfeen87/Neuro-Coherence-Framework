"""Full analysis workflow with multimodal integration.

This script demonstrates a complete analysis workflow:
1. Generate synthetic multimodal data
2. Analyze EEG (PLV, coherence)
3. Analyze fMRI (connectivity)
4. Integrate modalities to calculate Ψ
5. Compare healthy vs bipolar patterns
6. Generate publication-quality figures
"""

import numpy as np
import matplotlib.pyplot as plt
from data.synthetic.generate_data import (
    generate_eeg_signals,
    generate_fmri_timeseries,
    generate_bipolar_trajectory,
    generate_healthy_controls,
)
from analysis.eeg import calculate_plv_matrix, calculate_global_coherence
from analysis.fmri import calculate_correlation_matrix, calculate_global_efficiency
from analysis.integration import MultimodalPsiCalculator


def analyze_eeg_data(signals, fs):
    """Analyze EEG signals."""
    print("  Analyzing EEG data...")

    # Calculate PLV matrix
    plv_matrix = calculate_plv_matrix(signals)
    mean_plv = np.mean(plv_matrix[np.triu_indices_from(plv_matrix, k=1)])

    # Calculate global coherence
    global_coh = calculate_global_coherence(signals, fs)

    return {
        "plv_matrix": plv_matrix,
        "mean_plv": mean_plv,
        "global_coherence": global_coh,
    }


def analyze_fmri_data(timeseries):
    """Analyze fMRI timeseries."""
    print("  Analyzing fMRI data...")

    # Calculate connectivity matrix
    conn_matrix = calculate_correlation_matrix(timeseries)

    # Calculate network variance
    upper_tri = conn_matrix[np.triu_indices_from(conn_matrix, k=1)]
    sync_variance = np.var(upper_tri)

    # Calculate global efficiency
    global_eff = calculate_global_efficiency(conn_matrix)

    return {
        "connectivity_matrix": conn_matrix,
        "sync_variance": sync_variance,
        "global_efficiency": global_eff,
    }


def compare_healthy_vs_bipolar():
    """Compare healthy controls vs bipolar patterns."""
    print("\n1. Comparing Healthy vs Bipolar Patterns...")

    states = ["euthymic", "manic", "depressive"]
    results = {}

    for state in states:
        print(f"  Processing {state} state...")

        # Generate EEG
        time_eeg, eeg_signals = generate_eeg_signals(
            n_channels=19, duration=2000, fs=250.0, state=state
        )

        # Generate fMRI
        time_fmri, fmri_timeseries = generate_fmri_timeseries(
            n_rois=90, duration=100, tr=2.0, state=state
        )

        # Analyze
        eeg_results = analyze_eeg_data(eeg_signals, 250.0)
        fmri_results = analyze_fmri_data(fmri_timeseries)

        # Calculate Ψ
        calc = MultimodalPsiCalculator()
        psi_result = calc.calculate_psi_multimodal(
            eeg_data={"plv_matrix": eeg_results["plv_matrix"]},
            fmri_data={"connectivity_matrix": fmri_results["connectivity_matrix"]},
        )

        results[state] = {
            "eeg": eeg_results,
            "fmri": fmri_results,
            "psi": psi_result["psi"],
            "psi_result": psi_result,
        }

    # Visualize comparison
    fig, axes = plt.subplots(2, 3, figsize=(15, 10))
    fig.suptitle("Healthy vs Bipolar Multimodal Comparison", fontsize=16)

    # Row 1: EEG metrics
    ax = axes[0, 0]
    plv_values = [results[s]["eeg"]["mean_plv"] for s in states]
    ax.bar(states, plv_values, color=["green", "red", "blue"], alpha=0.7)
    ax.set_ylabel("Mean PLV")
    ax.set_title("EEG Phase Locking")
    ax.grid(axis="y", alpha=0.3)

    ax = axes[0, 1]
    coh_values = [results[s]["eeg"]["global_coherence"] for s in states]
    ax.bar(states, coh_values, color=["green", "red", "blue"], alpha=0.7)
    ax.set_ylabel("Global Coherence")
    ax.set_title("EEG Coherence")
    ax.grid(axis="y", alpha=0.3)

    ax = axes[0, 2]
    variance_values = [results[s]["fmri"]["sync_variance"] for s in states]
    ax.bar(states, variance_values, color=["green", "red", "blue"], alpha=0.7)
    ax.set_ylabel("Sync Variance")
    ax.set_title("fMRI Network Variance")
    ax.grid(axis="y", alpha=0.3)

    # Row 2: Integrated metrics
    ax = axes[1, 0]
    psi_values = [results[s]["psi"] for s in states]
    bars = ax.bar(states, psi_values, color=["green", "red", "blue"], alpha=0.7)
    ax.set_ylabel("Ψ (Neuro-Coherence)")
    ax.set_title("Integrated Ψ")
    ax.grid(axis="y", alpha=0.3)

    # Add values on bars
    for bar, val in zip(bars, psi_values):
        height = bar.get_height()
        ax.text(
            bar.get_x() + bar.get_width() / 2.0,
            height,
            f"{val:.3f}",
            ha="center",
            va="bottom",
        )

    # Operator breakdown for euthymic
    ax = axes[1, 1]
    euth = results["euthymic"]["psi_result"]
    operators = ["Γ", "Θ", "1-Δ", "Λ"]
    values = [
        float(euth["gamma"]),
        float(euth["theta"]),
        1 - float(euth["delta"]),
        float(euth["lambda"]),
    ]
    ax.bar(operators, values, color=["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728"])
    ax.set_ylabel("Value")
    ax.set_title("Euthymic Operators")
    ax.set_ylim(0, 1.5)
    ax.grid(axis="y", alpha=0.3)

    # Operator breakdown for manic
    ax = axes[1, 2]
    manic = results["manic"]["psi_result"]
    values = [
        float(manic["gamma"]),
        float(manic["theta"]),
        1 - float(manic["delta"]),
        float(manic["lambda"]),
    ]
    ax.bar(operators, values, color=["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728"])
    ax.set_ylabel("Value")
    ax.set_title("Manic Operators")
    ax.set_ylim(0, 1.5)
    ax.grid(axis="y", alpha=0.3)

    plt.tight_layout()
    plt.savefig("multimodal_comparison.png", dpi=150)
    print("\nSaved: multimodal_comparison.png")

    return results


def longitudinal_analysis():
    """Analyze longitudinal trajectory."""
    print("\n2. Longitudinal Trajectory Analysis...")

    # Generate bipolar trajectory
    trajectory = generate_bipolar_trajectory(
        duration=1500, n_episodes=4, episode_duration=200, noise_level=0.03
    )

    # Generate healthy controls
    controls = generate_healthy_controls(n_subjects=10, duration=1500, variability=0.08)

    # Plot
    fig, axes = plt.subplots(2, 1, figsize=(14, 8))

    # Bipolar trajectory
    ax = axes[0]
    ax.plot(trajectory["time"], trajectory["psi"], linewidth=2, color="darkblue")

    # Color-code episodes
    colors = {0: "lightgreen", 1: "lightcoral", 2: "lightblue"}
    labels = {0: "Euthymic", 1: "Manic", 2: "Depressive"}

    for state_id in [0, 1, 2]:
        mask = trajectory["state_labels"] == state_id
        if np.any(mask):
            indices = np.where(mask)[0]
            for i in range(len(indices)):
                if i == 0 or indices[i] != indices[i - 1] + 1:
                    # Start of new segment
                    start_idx = indices[i]
                    j = i
                    while j < len(indices) - 1 and indices[j + 1] == indices[j] + 1:
                        j += 1
                    end_idx = indices[j]

                    label = labels[state_id] if i == 0 else None
                    ax.axvspan(
                        start_idx,
                        end_idx,
                        alpha=0.3,
                        color=colors[state_id],
                        label=label,
                    )

    ax.set_xlabel("Time", fontsize=12)
    ax.set_ylabel("Ψ (Neuro-Coherence)", fontsize=12)
    ax.set_title("Bipolar Disorder Trajectory", fontsize=14)
    ax.legend(loc="best")
    ax.grid(alpha=0.3)

    # Healthy controls
    ax = axes[1]
    for i, traj in enumerate(controls["trajectories"]):
        alpha = 0.3 if i > 0 else 0.8
        label = "Healthy Controls" if i == 0 else None
        ax.plot(traj, alpha=alpha, color="green", linewidth=1, label=label)

    # Add mean and std
    mean_traj = np.mean(controls["trajectories"], axis=0)
    std_traj = np.std(controls["trajectories"], axis=0)
    ax.plot(mean_traj, color="darkgreen", linewidth=2, label="Mean")
    ax.fill_between(
        range(len(mean_traj)),
        mean_traj - std_traj,
        mean_traj + std_traj,
        alpha=0.2,
        color="green",
    )

    ax.set_xlabel("Time", fontsize=12)
    ax.set_ylabel("Ψ (Neuro-Coherence)", fontsize=12)
    ax.set_title("Healthy Control Trajectories", fontsize=14)
    ax.legend(loc="best")
    ax.grid(alpha=0.3)

    plt.tight_layout()
    plt.savefig("longitudinal_analysis.png", dpi=150)
    print("Saved: longitudinal_analysis.png")


def main():
    """Run full analysis workflow."""
    print("=" * 60)
    print("Neuro-Coherence Framework - Full Analysis")
    print("=" * 60)

    # Set seed for reproducibility
    np.random.seed(42)

    # Run analyses
    results = compare_healthy_vs_bipolar()
    longitudinal_analysis()

    # Summary statistics
    print("\n" + "=" * 60)
    print("Summary Statistics")
    print("=" * 60)

    for state in ["euthymic", "manic", "depressive"]:
        print(f"\n{state.upper()}:")
        print(f"  Ψ: {results[state]['psi']:.4f}")
        print(f"  Mean PLV: {results[state]['eeg']['mean_plv']:.4f}")
        print(f"  Sync Variance: {results[state]['fmri']['sync_variance']:.4f}")

    print("\n" + "=" * 60)
    print("Analysis Complete!")
    print("=" * 60)
    print("\nGenerated files:")
    print("  - multimodal_comparison.png")
    print("  - longitudinal_analysis.png")
    print()


if __name__ == "__main__":
    main()
