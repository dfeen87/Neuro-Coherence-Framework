"""
Global Sensitivity Analysis Module.

MIT License

Copyright (c) 2026 Don Michael Feeney Jr.

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

This module performs Global Sensitivity Analysis (GSA) to identify critical
drivers of systemic collapse in the Neuro-Coherence Function (Ψ). The generated
heatmap allows researchers to identify which operator provides the most leverage
for therapeutic restoration, indicating where ΔΨ is maximized for a given change
in input.
"""

import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from typing import Tuple

from simulations.core.neuro_coherence import NeuroCoherence
from simulations.core.operators import Operators


def perform_parameter_sweep(
    resolution: int = 20, n_mc_samples: int = 100, phi: float = 1.0
) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """
    Perform a parameter sweep across all four operators.

    Uses a grid for Θ (Thermodynamic Stability) and Γ (Adaptive Gain)
    and Monte Carlo sampling for Δ (Connectivity Variance) and
    Λ (Spatiotemporal Coherence).

    Args:
        resolution: Grid resolution for Θ and Γ.
        n_mc_samples: Number of Monte Carlo samples for Δ and Λ per grid point.
        phi: Global modulation coefficient.

    Returns:
        Tuple containing arrays for theta values, gamma values,
        mean Ψ values, and mean partial derivative values w.r.t Θ and Γ.
    """
    nc = NeuroCoherence(phi=phi)
    ops = Operators()

    theta_vals = np.linspace(0.0, 1.0, resolution)
    gamma_vals = np.linspace(0.0, 1.0, resolution)

    psi_grid = np.zeros((resolution, resolution))
    dpsi_dtheta_grid = np.zeros((resolution, resolution))
    dpsi_dgamma_grid = np.zeros((resolution, resolution))
    dpsi_ddelta_grid = np.zeros((resolution, resolution))
    dpsi_dlambda_grid = np.zeros((resolution, resolution))

    # We use a small epsilon for finite differences
    eps = 1e-4

    for i, theta_param in enumerate(theta_vals):
        for j, gamma_param in enumerate(gamma_vals):
            psi_samples = np.zeros(n_mc_samples)
            dpsi_dtheta_samples = np.zeros(n_mc_samples)
            dpsi_dgamma_samples = np.zeros(n_mc_samples)
            dpsi_ddelta_samples = np.zeros(n_mc_samples)
            dpsi_dlambda_samples = np.zeros(n_mc_samples)

            for k in range(n_mc_samples):
                # Monte Carlo sampling for delta and lambda
                delta_param = np.random.uniform(0.0, 1.0)
                lambda_param = np.random.uniform(0.0, 1.0)

                # Base operators
                gamma_op = ops.adaptive_gain(plasticity=gamma_param)
                theta_op = ops.thermodynamic_stability(homeostasis=theta_param)
                delta_op = ops.connectivity_variance(sync_variance=delta_param)
                lambda_op = ops.spatiotemporal_coherence(phase_alignment=lambda_param)

                base_psi = nc.calculate(gamma_op, theta_op, delta_op, lambda_op).psi
                psi_samples[k] = base_psi

                # Perturb theta
                theta_param_p = min(theta_param + eps, 1.0)
                d_theta = theta_param_p - theta_param
                if d_theta > 0:
                    theta_op_p = ops.thermodynamic_stability(homeostasis=theta_param_p)
                    psi_p = nc.calculate(gamma_op, theta_op_p, delta_op, lambda_op).psi
                    dpsi_dtheta_samples[k] = (psi_p - base_psi) / d_theta

                # Perturb gamma
                gamma_param_p = min(gamma_param + eps, 1.0)
                d_gamma = gamma_param_p - gamma_param
                if d_gamma > 0:
                    gamma_op_p = ops.adaptive_gain(plasticity=gamma_param_p)
                    psi_p = nc.calculate(gamma_op_p, theta_op, delta_op, lambda_op).psi
                    dpsi_dgamma_samples[k] = (psi_p - base_psi) / d_gamma

                # Perturb delta
                delta_param_p = min(delta_param + eps, 1.0)
                d_delta = delta_param_p - delta_param
                if d_delta > 0:
                    delta_op_p = ops.connectivity_variance(sync_variance=delta_param_p)
                    psi_p = nc.calculate(gamma_op, theta_op, delta_op_p, lambda_op).psi
                    dpsi_ddelta_samples[k] = (psi_p - base_psi) / d_delta

                # Perturb lambda
                lambda_param_p = min(lambda_param + eps, 1.0)
                d_lambda = lambda_param_p - lambda_param
                if d_lambda > 0:
                    lambda_op_p = ops.spatiotemporal_coherence(
                        phase_alignment=lambda_param_p
                    )
                    psi_p = nc.calculate(gamma_op, theta_op, delta_op, lambda_op_p).psi
                    dpsi_dlambda_samples[k] = (psi_p - base_psi) / d_lambda

            psi_grid[j, i] = np.mean(
                psi_samples
            )  # Note: y-axis is gamma (j), x-axis is theta (i)
            dpsi_dtheta_grid[j, i] = np.mean(dpsi_dtheta_samples)
            dpsi_dgamma_grid[j, i] = np.mean(dpsi_dgamma_samples)
            dpsi_ddelta_grid[j, i] = np.mean(dpsi_ddelta_samples)
            dpsi_dlambda_grid[j, i] = np.mean(dpsi_dlambda_samples)

    return (
        theta_vals,
        gamma_vals,
        psi_grid,
        dpsi_dtheta_grid,
        dpsi_dgamma_grid,
        dpsi_ddelta_grid,
        dpsi_dlambda_grid,
    )


def identify_tipping_points(
    psi_grid: np.ndarray, threshold: float = 0.05
) -> np.ndarray:
    """
    Identify the 'tipping point' where Ψ approaches zero and the system
    enters oscillatory divergence.

    Args:
        psi_grid: The grid of Ψ values.
        threshold: The threshold below which Ψ is considered near zero.

    Returns:
        Boolean mask indicating the tipping point regions.
    """
    # Find points where psi is below the threshold, indicating collapse
    return psi_grid < threshold


def generate_sensitivity_heatmap(
    theta_vals: np.ndarray,
    gamma_vals: np.ndarray,
    sensitivity_grid: np.ndarray,
    tipping_points: np.ndarray,
    output_path: str = "docs/figures/sensitivity_heatmap.png",
) -> None:
    """
    Generate a high-resolution Seaborn Heatmap illustrating sensitivity.

    The heatmap displays the gradient magnitude (sensitivity) of Ψ with respect
    to Θ and Γ. It also visually marks the tipping points.

    Args:
        theta_vals: Array of Θ values (x-axis).
        gamma_vals: Array of Γ values (y-axis).
        sensitivity_grid: 2D array of sensitivity values to plot.
        tipping_points: Boolean mask of tipping points.
        output_path: Path to save the generated image.
    """
    plt.figure(figsize=(10, 8))

    # Create a DataFrame for seaborn
    df = pd.DataFrame(
        sensitivity_grid, index=np.round(gamma_vals, 2), columns=np.round(theta_vals, 2)
    )

    # Plot the heatmap
    ax = sns.heatmap(
        df,
        cmap="viridis",
        cbar_kws={"label": r"Sensitivity Magnitude ($||\nabla \Psi||$)"},
        linewidths=0.0,
    )

    # Optionally overlay tipping points
    # Where tipping_points is True, overlay a marker or different color
    y_idx, x_idx = np.where(tipping_points)
    plt.scatter(
        x_idx + 0.5,
        y_idx + 0.5,
        marker="x",
        color="red",
        s=20,
        alpha=0.5,
        label=r"Tipping Point ($\Psi \approx 0$)",
    )

    ax.invert_yaxis()  # Ensure low Gamma is at the bottom

    plt.title(
        "Sensitivity of Systemic Coherence (Ψ) to Operator Variance",
        pad=20,
        fontsize=14,
    )
    plt.xlabel(r"Thermodynamic Stability ($\Theta$)", fontsize=12)
    plt.ylabel(r"Adaptive Gain ($\Gamma$)", fontsize=12)
    plt.legend(loc="upper left")

    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches="tight")
    plt.close()


def main():
    """Run the sensitivity analysis and generate the heatmap."""
    print("Running Global Sensitivity Analysis...")
    resolution = 20
    n_samples = 50  # Lowered slightly for reasonable execution time

    results = perform_parameter_sweep(resolution=resolution, n_mc_samples=n_samples)

    theta_vals, gamma_vals, psi_grid, d_theta, d_gamma, d_delta, d_lambda = results

    # Calculate overall sensitivity (magnitude of gradient)
    # The gradient vector is [dPsi/dGamma, dPsi/dTheta, dPsi/dDelta, dPsi/dLambda]
    # We want to identify the total leverage at each point
    sensitivity_grid = np.sqrt(d_theta**2 + d_gamma**2 + d_delta**2 + d_lambda**2)

    # Identify tipping points where Psi approaches 0
    tipping_points = identify_tipping_points(psi_grid, threshold=0.05)

    print("Generating visualization...")
    generate_sensitivity_heatmap(
        theta_vals=theta_vals,
        gamma_vals=gamma_vals,
        sensitivity_grid=sensitivity_grid,
        tipping_points=tipping_points,
    )
    print("GSA complete. Results saved to docs/figures/sensitivity_heatmap.png")


if __name__ == "__main__":
    main()
