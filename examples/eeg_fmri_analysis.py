# Copyright (c) 2026 Don Michael Feeney Jr.
# MIT License - see LICENSE for details.

"""
Concurrent EEG-fMRI Analysis Workflow Example (v2.0.0).

Demonstrates:
1. Synthetic concurrent EEG-fMRI data generation with scanner artifacts (GA, BCG, motion)
2. Artifact removal using Average Artifact Subtraction (AAS) and Optimal Basis Sets (OBS/PCA)
3. Cross-modal synchronization, joint coherence (Lambda), and network connectivity variance (Delta_GR)
4. Bipolar disorder regime stratification (Euthymic, Manic, Depressive)
5. Multimodal Neuro-Coherence Function (Psi) computation
"""

import os
import sys
import numpy as np
import matplotlib.pyplot as plt

# Ensure repo root is on python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from data.synthetic.generate_data import generate_concurrent_eeg_fmri_data  # noqa: E402
from analysis.integration import MultimodalPsiCalculator  # noqa: E402


def run_concurrent_eeg_fmri_workflow():
    """Execute complete concurrent EEG-fMRI workflow across clinical states."""
    print("=" * 70)
    print("Neuro-Coherence Framework v2.0.0 - Concurrent EEG-fMRI Integration")
    print("=" * 70)

    states = ["euthymic", "manic", "depressive"]
    calculator = MultimodalPsiCalculator(phi=1.0)

    state_results = {}

    for state in states:
        print(f"\n---> Generating synthetic dataset for state: {state.upper()}")
        # 1. Generate synthetic dataset
        dataset = generate_concurrent_eeg_fmri_data(
            n_eeg_channels=19,
            n_rois=12,
            duration_sec=60.0,
            fs_eeg=250.0,
            tr_fmri=2.0,
            state=state,
            add_gradient_artifact=True,
            add_bcg_artifact=True,
            add_motion_artifact=True,
            random_seed=42,
        )

        # 2. Process concurrent dataset
        print("  [1/3] Preprocessing EEG-in-MRI (AAS + OBS/PCA)...")
        print("  [2/3] Computing cross-modal synchronization & network variance...")
        print("  [3/3] Calculating Neuro-Coherence Psi & classifying regime...")

        full_res = calculator.calculate_from_concurrent_eeg_fmri(dataset)
        preproc = full_res["concurrent_results"]["preprocessing"]["artifact_metrics"]
        sync = full_res["concurrent_results"]["synchronization"]
        regime = full_res["bipolar_regime"]

        state_results[state] = {
            "dataset": dataset,
            "full_results": full_res,
            "preproc": preproc,
            "sync": sync,
            "regime": regime,
            "psi": full_res["psi"],
        }

        print(f"  Results for {state.upper()}:")
        print(
            f"    - Artifact Reduction Ratio (ARR): {preproc['artifact_reduction_ratio_db']:.2f} dB"
        )
        print(
            f"    - SAR Improvement:               {preproc.get('sar_improvement_db', 0.0):.2f} dB"
        )
        print(
            f"    - Ground Truth Correlation:       {preproc.get('ground_truth_correlation', 0.0):.4f}"
        )
        print(f"    - Spatiotemporal Coherence (Λ):  {sync['lambda']:.4f}")
        print(f"    - Network Connectivity Var (Δ_GR): {sync['delta_gr']:.4f}")
        print(f"    - Neuro-Coherence Function (Ψ):   {full_res['psi']:.4f}")
        print(
            f"    - Classified Regime:              {regime['regime'].upper()} (confidence: {regime['confidence']:.2f})"
        )

    # 3. Generate summary visualization
    plot_eeg_fmri_results(state_results)

    return state_results


def plot_eeg_fmri_results(state_results):
    """Generate and save publication-quality visualization for concurrent EEG-fMRI integration."""
    fig, axes = plt.subplots(2, 3, figsize=(16, 10))
    fig.suptitle(
        "Concurrent EEG-fMRI Multimodal Integration (v2.0.0)",
        fontsize=16,
        fontweight="bold",
    )

    states = ["euthymic", "manic", "depressive"]
    colors = ["#2ca02c", "#d62728", "#1f77b4"]

    # 1. Artifact Reduction Ratio (ARR)
    ax = axes[0, 0]
    arr_vals = [
        state_results[s]["preproc"]["artifact_reduction_ratio_db"] for s in states
    ]
    bars = ax.bar(states, arr_vals, color=colors, alpha=0.8)
    ax.set_ylabel("ARR (dB)")
    ax.set_title("EEG Gradient/BCG Artifact Reduction")
    ax.grid(axis="y", linestyle="--", alpha=0.5)
    for bar, val in zip(bars, arr_vals):
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            val + 0.5,
            f"{val:.1f} dB",
            ha="center",
            va="bottom",
            fontsize=10,
        )

    # 2. Joint Spatiotemporal Coherence Lambda
    ax = axes[0, 1]
    lambda_vals = [state_results[s]["sync"]["lambda"] for s in states]
    bars = ax.bar(states, lambda_vals, color=colors, alpha=0.8)
    ax.set_ylabel("Spatiotemporal Coherence (Λ)")
    ax.set_title("Cross-Modal Joint Coherence (Λ)")
    ax.set_ylim(0, 1.0)
    ax.grid(axis="y", linestyle="--", alpha=0.5)
    for bar, val in zip(bars, lambda_vals):
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            val + 0.02,
            f"{val:.3f}",
            ha="center",
            va="bottom",
            fontsize=10,
        )

    # 3. Network Connectivity Variance Delta_GR
    ax = axes[0, 2]
    delta_vals = [state_results[s]["sync"]["delta_gr"] for s in states]
    bars = ax.bar(states, delta_vals, color=colors, alpha=0.8)
    ax.set_ylabel("Network Variance (Δ_GR)")
    ax.set_title("fMRI Fronto-Limbic Instability (Δ_GR)")
    ax.set_ylim(0, 1.0)
    ax.grid(axis="y", linestyle="--", alpha=0.5)
    for bar, val in zip(bars, delta_vals):
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            val + 0.02,
            f"{val:.3f}",
            ha="center",
            va="bottom",
            fontsize=10,
        )

    # 4. Integrated Neuro-Coherence Psi
    ax = axes[1, 0]
    psi_vals = [state_results[s]["psi"] for s in states]
    bars = ax.bar(states, psi_vals, color=colors, alpha=0.8)
    ax.set_ylabel("Neuro-Coherence (Ψ)")
    ax.set_title("Global Neuro-Coherence Function (Ψ)")
    ax.set_ylim(0, 1.5)
    ax.grid(axis="y", linestyle="--", alpha=0.5)
    for bar, val in zip(bars, psi_vals):
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            val + 0.03,
            f"{val:.3f}",
            ha="center",
            va="bottom",
            fontsize=10,
            fontweight="bold",
        )

    # 5. Clean vs Corrupted EEG Signals (Euthymic)
    ax = axes[1, 1]
    euth_data = state_results["euthymic"]["dataset"]
    time_eeg = euth_data["time_eeg"][:1000]
    ax.plot(
        time_eeg,
        euth_data["eeg_corrupted"][0, :1000],
        label="Corrupted EEG (with GA/BCG)",
        color="red",
        alpha=0.6,
        linewidth=1,
    )
    ax.plot(
        time_eeg,
        euth_data["eeg_clean"][0, :1000],
        label="Clean Ground Truth",
        color="green",
        linewidth=1.5,
    )
    ax.set_xlabel("Time (seconds)")
    ax.set_ylabel("Amplitude (μV)")
    ax.set_title("Euthymic EEG Signal & Artifact Suppression")
    ax.legend(loc="upper right", fontsize=8)
    ax.grid(alpha=0.3)

    # 6. Clinical Regime Stratification Matrix
    ax = axes[1, 2]
    ax.axis("off")
    table_data = [
        ["State", "Lambda (Λ)", "Delta_GR (Δ)", "Classified Regime"],
        [
            "Euthymic",
            f"{lambda_vals[0]:.3f}",
            f"{delta_vals[0]:.3f}",
            state_results["euthymic"]["regime"]["regime"].upper(),
        ],
        [
            "Manic",
            f"{lambda_vals[1]:.3f}",
            f"{delta_vals[1]:.3f}",
            state_results["manic"]["regime"]["regime"].upper(),
        ],
        [
            "Depressive",
            f"{lambda_vals[2]:.3f}",
            f"{delta_vals[2]:.3f}",
            state_results["depressive"]["regime"]["regime"].upper(),
        ],
    ]
    table = ax.table(cellText=table_data, loc="center", cellLoc="center")
    table.scale(1.2, 2.0)
    table.set_fontsize(11)
    ax.set_title("Clinical Stratification Summary", fontsize=12)

    plt.tight_layout()
    output_path = "docs/figures/eeg_fmri_integration.png"
    plt.savefig(output_path, dpi=150)
    print(f"\nSaved visualization figure: {output_path}")


def main():
    """Main execution entry point."""
    np.random.seed(42)
    run_concurrent_eeg_fmri_workflow()
    print("\n" + "=" * 70)
    print("Concurrent EEG-fMRI Analysis Workflow Complete!")
    print("=" * 70)


if __name__ == "__main__":
    main()
