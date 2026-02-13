"""fMRI connectivity analysis."""

from typing import Optional, Tuple
import numpy as np


def calculate_correlation_matrix(
    timeseries: np.ndarray, method: str = "pearson"
) -> np.ndarray:
    """
    Calculate connectivity matrix from time series.

    Args:
        timeseries: 2D array (ROIs x time)
        method: Correlation method ("pearson" or "spearman")

    Returns:
        Connectivity matrix (ROIs x ROIs)
    """
    if method == "pearson":
        conn_matrix = np.corrcoef(timeseries)
    elif method == "spearman":
        from scipy.stats import spearmanr

        conn_matrix, _ = spearmanr(timeseries, axis=1)
    else:
        raise ValueError(f"Unknown method: {method}")

    return conn_matrix


def calculate_partial_correlation(timeseries: np.ndarray) -> np.ndarray:
    """
    Calculate partial correlation matrix.

    Args:
        timeseries: 2D array (ROIs x time)

    Returns:
        Partial correlation matrix
    """
    # Calculate precision matrix (inverse of covariance)
    cov_matrix = np.cov(timeseries)

    # Add small regularization for numerical stability
    regularization = 1e-6
    cov_matrix += regularization * np.eye(cov_matrix.shape[0])

    try:
        precision_matrix = np.linalg.inv(cov_matrix)
    except np.linalg.LinAlgError:
        # Fallback to pseudoinverse
        precision_matrix = np.linalg.pinv(cov_matrix)

    # Convert precision to partial correlation
    d = np.sqrt(np.diag(precision_matrix))
    partial_corr = -precision_matrix / np.outer(d, d)
    np.fill_diagonal(partial_corr, 1.0)

    return partial_corr


def calculate_dynamic_connectivity(
    timeseries: np.ndarray, window_size: int, step_size: Optional[int] = None
) -> np.ndarray:
    """
    Calculate dynamic (time-varying) connectivity.

    Args:
        timeseries: 2D array (ROIs x time)
        window_size: Size of sliding window
        step_size: Step size for window (default: window_size // 2)

    Returns:
        3D array (windows x ROIs x ROIs)
    """
    if step_size is None:
        step_size = window_size // 2

    n_rois, n_timepoints = timeseries.shape

    # Calculate number of windows
    n_windows = (n_timepoints - window_size) // step_size + 1

    # Initialize output
    dyn_conn = np.zeros((n_windows, n_rois, n_rois))

    for i in range(n_windows):
        start = i * step_size
        end = start + window_size
        window_data = timeseries[:, start:end]
        dyn_conn[i] = calculate_correlation_matrix(window_data)

    return dyn_conn


def threshold_connectivity(
    conn_matrix: np.ndarray,
    threshold: Optional[float] = None,
    density: Optional[float] = None,
) -> np.ndarray:
    """
    Threshold connectivity matrix.

    Args:
        conn_matrix: Connectivity matrix
        threshold: Absolute threshold value
        density: Keep top X% of connections (0 to 1)

    Returns:
        Thresholded connectivity matrix
    """
    thresholded = conn_matrix.copy()

    if threshold is not None:
        # Absolute threshold
        thresholded[np.abs(thresholded) < threshold] = 0
    elif density is not None:
        # Density threshold
        if density < 0 or density > 1:
            raise ValueError("density must be in [0, 1]")

        # Get upper triangle (excluding diagonal)
        n = conn_matrix.shape[0]
        triu_indices = np.triu_indices(n, k=1)
        upper_values = np.abs(conn_matrix[triu_indices])

        # Calculate threshold for desired density
        n_connections = len(upper_values)
        n_keep = int(n_connections * density)

        if n_keep > 0:
            threshold_value = np.partition(upper_values, -n_keep)[-n_keep]
            thresholded[np.abs(thresholded) < threshold_value] = 0
        else:
            thresholded[:] = 0

    return thresholded


def calculate_network_connectivity(
    timeseries: np.ndarray, network_labels: np.ndarray
) -> Tuple[np.ndarray, np.ndarray]:
    """
    Calculate within- and between-network connectivity.

    Args:
        timeseries: 2D array (ROIs x time)
        network_labels: Array of network labels for each ROI

    Returns:
        Tuple of (within_network_conn, between_network_conn)
    """
    conn_matrix = calculate_correlation_matrix(timeseries)
    unique_networks = np.unique(network_labels)
    n_networks = len(unique_networks)

    # Initialize matrices
    within_conn = np.zeros(n_networks)
    between_conn = np.zeros((n_networks, n_networks))

    for i, net1 in enumerate(unique_networks):
        mask1 = network_labels == net1

        # Within-network connectivity
        within_idx = np.ix_(mask1, mask1)
        within_values = conn_matrix[within_idx]
        # Exclude diagonal
        within_values = within_values[~np.eye(within_values.shape[0], dtype=bool)]
        within_conn[i] = np.mean(within_values) if len(within_values) > 0 else 0

        # Between-network connectivity
        for j, net2 in enumerate(unique_networks):
            if i < j:  # Only upper triangle
                mask2 = network_labels == net2
                between_idx = np.ix_(mask1, mask2)
                between_values = conn_matrix[between_idx].flatten()
                between_conn[i, j] = (
                    np.mean(between_values) if len(between_values) > 0 else 0
                )
                between_conn[j, i] = between_conn[i, j]

    return within_conn, between_conn
