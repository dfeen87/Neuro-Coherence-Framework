"""fMRI network metrics."""

import numpy as np


def calculate_degree(conn_matrix: np.ndarray, weighted: bool = True) -> np.ndarray:
    """
    Calculate node degree.

    Args:
        conn_matrix: Connectivity matrix
        weighted: If True, calculate weighted degree

    Returns:
        Degree for each node
    """
    if weighted:
        # Weighted degree (sum of connection weights)
        degree = np.sum(np.abs(conn_matrix), axis=1)
    else:
        # Binary degree (number of connections)
        binary_matrix = (conn_matrix != 0).astype(int)
        degree = np.sum(binary_matrix, axis=1)

    # Subtract self-connections
    degree -= np.diag(conn_matrix)

    return degree


def calculate_clustering_coefficient(
    conn_matrix: np.ndarray, weighted: bool = True
) -> np.ndarray:
    """
    Calculate clustering coefficient for each node.

    Args:
        conn_matrix: Connectivity matrix
        weighted: If True, calculate weighted clustering

    Returns:
        Clustering coefficient for each node
    """
    n = conn_matrix.shape[0]
    clustering = np.zeros(n)

    for i in range(n):
        # Get neighbors
        neighbors = np.where(conn_matrix[i] != 0)[0]
        neighbors = neighbors[neighbors != i]

        k = len(neighbors)
        if k < 2:
            clustering[i] = 0
            continue

        if weighted:
            # Weighted clustering
            w = np.abs(conn_matrix)
            subgraph = w[np.ix_(neighbors, neighbors)]
            degree_i = np.sum(w[i, neighbors])

            if degree_i == 0:
                clustering[i] = 0
            else:
                # Onnela et al. formula
                numerator = np.sum(
                    (
                        w[i, neighbors].reshape(-1, 1)
                        * subgraph
                        * w[neighbors, i].reshape(1, -1)
                    )
                    ** (1 / 3)
                )
                denominator = degree_i * (k - 1)
                clustering[i] = numerator / denominator if denominator > 0 else 0
        else:
            # Binary clustering
            subgraph = conn_matrix[np.ix_(neighbors, neighbors)]
            actual_edges = np.sum(subgraph != 0)
            possible_edges = k * (k - 1)
            clustering[i] = actual_edges / possible_edges if possible_edges > 0 else 0

    return clustering


def calculate_betweenness_centrality(conn_matrix: np.ndarray) -> np.ndarray:
    """
    Calculate betweenness centrality (simplified version).

    Args:
        conn_matrix: Connectivity matrix

    Returns:
        Betweenness centrality for each node
    """
    n = conn_matrix.shape[0]
    betweenness = np.zeros(n)

    # Convert to distance matrix (inverse of weights)
    dist_matrix = np.zeros_like(conn_matrix)
    mask = conn_matrix != 0
    dist_matrix[mask] = 1.0 / np.abs(conn_matrix[mask])
    dist_matrix[~mask] = np.inf
    np.fill_diagonal(dist_matrix, 0)

    # Floyd-Warshall for all-pairs shortest paths
    for k in range(n):
        for i in range(n):
            for j in range(n):
                if dist_matrix[i, k] + dist_matrix[k, j] < dist_matrix[i, j]:
                    dist_matrix[i, j] = dist_matrix[i, k] + dist_matrix[k, j]

    # Count shortest paths through each node (simplified)
    for i in range(n):
        for j in range(n):
            if i != j:
                for k in range(n):
                    if k != i and k != j:
                        # Check if k is on shortest path from i to j
                        if (
                            np.isfinite(dist_matrix[i, k])
                            and np.isfinite(dist_matrix[k, j])
                            and abs(
                                dist_matrix[i, j]
                                - (dist_matrix[i, k] + dist_matrix[k, j])
                            )
                            < 1e-10
                        ):
                            betweenness[k] += 1

    # Normalize
    if n > 2:
        betweenness /= (n - 1) * (n - 2)

    return betweenness


def calculate_global_efficiency(conn_matrix: np.ndarray) -> float:
    """
    Calculate global efficiency.

    Args:
        conn_matrix: Connectivity matrix

    Returns:
        Global efficiency
    """
    n = conn_matrix.shape[0]

    # Convert to distance matrix
    dist_matrix = np.zeros_like(conn_matrix)
    mask = conn_matrix != 0
    dist_matrix[mask] = 1.0 / np.abs(conn_matrix[mask])
    dist_matrix[~mask] = np.inf
    np.fill_diagonal(dist_matrix, 0)

    # Floyd-Warshall
    for k in range(n):
        for i in range(n):
            for j in range(n):
                if dist_matrix[i, k] + dist_matrix[k, j] < dist_matrix[i, j]:
                    dist_matrix[i, j] = dist_matrix[i, k] + dist_matrix[k, j]

    # Calculate efficiency
    efficiency = 0
    count = 0
    for i in range(n):
        for j in range(i + 1, n):
            if np.isfinite(dist_matrix[i, j]) and dist_matrix[i, j] > 0:
                efficiency += 1.0 / dist_matrix[i, j]
                count += 1

    if count > 0:
        efficiency /= count

    return float(efficiency)


def calculate_modularity(
    conn_matrix: np.ndarray, community_labels: np.ndarray
) -> float:
    """
    Calculate Newman's modularity.

    Args:
        conn_matrix: Connectivity matrix
        community_labels: Community assignment for each node

    Returns:
        Modularity value
    """
    n = conn_matrix.shape[0]

    # Total edge weight
    m = np.sum(np.abs(conn_matrix)) / 2

    if m == 0:
        return 0.0

    # Calculate modularity
    Q = 0
    for i in range(n):
        for j in range(n):
            if community_labels[i] == community_labels[j]:
                ki = np.sum(np.abs(conn_matrix[i]))
                kj = np.sum(np.abs(conn_matrix[j]))
                Q += conn_matrix[i, j] - (ki * kj) / (2 * m)

    Q /= 2 * m

    return float(Q)


def calculate_rich_club_coefficient(conn_matrix: np.ndarray, k: int) -> float:
    """
    Calculate rich club coefficient for degree k.

    Args:
        conn_matrix: Connectivity matrix
        k: Degree threshold

    Returns:
        Rich club coefficient
    """
    # Calculate degree
    degree = calculate_degree(conn_matrix, weighted=False)

    # Find nodes with degree > k
    rich_nodes = np.where(degree > k)[0]

    if len(rich_nodes) < 2:
        return 0.0

    # Count connections among rich nodes
    subgraph = conn_matrix[np.ix_(rich_nodes, rich_nodes)]
    actual_connections = np.sum(subgraph != 0)

    # Possible connections
    n_rich = len(rich_nodes)
    possible_connections = n_rich * (n_rich - 1)

    if possible_connections == 0:
        return 0.0

    phi = actual_connections / possible_connections

    return float(phi)
