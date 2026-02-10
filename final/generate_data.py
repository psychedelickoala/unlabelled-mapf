"""
Generates data for plotting.
Note generating large amounts of data takes a long time.

Last modified: 10/2/26
Author: Annalisa Calvi, Monash University
"""

import networkx as nx
import random
import csv
from math import sqrt, log
from typing import List, Optional, Iterable
from tqdm import tqdm
import numpy as np

# ============== FUNCTIONS ==============

def rand_sum_of_demands(n: int, k: int, path: bool = False, labelled: bool = True) -> int:
    """
    Calculate the sum of demands (OPT) for a random tree.
    
    :param n: Number of vertices in the tree
    :param k: Number of agents/targets in the tree
    :param path: Whether to generate a path or a random tree
    :param labelled: Whether to generate a labelled or unlabelled tree
    """
    
    # Generate random tree G
    if path:
        G: nx.Graph = nx.path_graph(n)
    elif labelled:
        G: nx.Graph = nx.random_labeled_tree(n)
    else:
        G: nx.Graph = nx.random_unlabeled_tree(n)
    
    # Set agent positions
    is_agent: List[bool] = [False] * n
    agent_positions: List[int] = random.sample(range(n), k)
    for i in agent_positions:
        is_agent[i] = True

    # Set target positions
    is_target: List[bool] = [False] * n
    target_positions: List[int] = random.sample(range(n), k)
    for i in target_positions:
        is_target[i] = True


    # Compute sum of demands via DFS
    sum_of_demands: int = 0
    
    visited: List[bool] = [False] * n
    parent: List[Optional[int]] = [None] * n
    demand: List[int] = [0] * n

    stack: List[int] = [
        0  # root node
    ]

    while len(stack) > 0:
        u = stack[-1]  # peek at top of the stack
        
        if visited[u]:  # already processed children
            stack.pop()  # remove from stack
            
            if is_agent[u]:
                demand[u] -= 1
            if is_target[u]:
                demand[u] += 1
            
            sum_of_demands += abs(demand[u])
            
            if parent[u] is not None:
                demand[parent[u]] += demand[u]  # update parent demand
        
        else:  # need to process children first
            visited[u] = True

            # add children to stack
            for v in G[u]:
                if not visited[v]:
                    parent[v] = u
                    stack.append(v)

    return sum_of_demands


def generate_n_vs_sod(path_to_csv: str, ns: Iterable, path: bool = False, seed: Optional[int] = None) -> None:
    """
    Write n vs sum of demands (OPT) data to a CSV file.
    CSV file will have columns n, k, sum_of_demands.
    
    :param path_to_csv: Path to CSV file. The contents of this file will be overwritten.
    :param ns: Values of n (number of vertices) to compute OPT for.
    :param path: Whether to generate a path or a random tree.
    :param seed: Random seed to use.
    """

    # set seed
    if seed is not None:
        random.seed(seed)
    
    # Open a CSV file to write the results
    with open(path_to_csv, "w", newline="") as f:
        writer = csv.writer(f)
        
        # Write the header row to the CSV file
        writer.writerow(["n", "k", "sum_of_demands"])

        print(f"Writing to {path_to_csv}...")
        
        # Calculate SOD for each n
        for n in tqdm(ns):
            k_values: List[int] = [1, 5, int(log(n)), int(sqrt(n)), n // 10, n // 4, n // 2]
            
            for k in k_values:
                sum_of_demands: int = rand_sum_of_demands(n, k, path=path)
                writer.writerow([n, k, sum_of_demands])

        print("Done!")


def generate_k_vs_sod(path_to_csv: str, n: int, w: Optional[int] = None, num_samples: int = 1_000, path: bool = False, seed: Optional[int] = None) -> None:
    """

    Write k vs sum of demands (OPT) data to a CSV file.
    CSV file will have columns k, sum_of_demands.
    
    :param path_to_csv: Path to CSV file. The contents of this file will be overwritten.
    :param n: Value of n (number of vertices) to use.
    :param path: Whether to generate a path or a random tree.
    :param w: Weighting of the edges when selecting values of k to use. Should be >= 1 or None.
    :num_samples: Number of values of k to use.
    :param seed: Random seed to use.
    """

    # set seed
    if seed is not None:
        random.seed(seed)

    # Open a CSV file to write the results
    with open(path_to_csv, "w", newline="") as f:
        writer = csv.writer(f)
        
        # Write the header row to the CSV file
        writer.writerow(["k", "sum_of_demands"])

        # Generate list of ks
        ks_weighted: np.ndarray = generate_k_list(n, w, num_samples//2)
        ks_uniform: np.ndarray = generate_k_list(n, None, num_samples//2)


        ks = np.concatenate([ks_weighted, ks_uniform])
        ks = np.unique(ks)

        print(f"Writing to {path_to_csv}...")

        # Calculate SOD for each k
        for k in tqdm(ks):

            sum_of_demands: int = rand_sum_of_demands(n, k, path=path)
            writer.writerow([k, sum_of_demands])

        print("Done!")


def generate_k_list(n: int, w: Optional[int], num_samples: int = 1_000) -> np.ndarray:
    """
    Generates values of k to use.
    
    :param n: Value of n (number of vertices) to use
    :param w: Weighting of the edges when selecting values of k to use. Should be >= 1 or None.
    :param num_samples: Number of values to generate.
    """
    
    if w is None:
        K = np.linspace(0, n, endpoint=True, num=num_samples)
    else:
        # space k by distribution with pdf c*(k-n/2)**(2w)
        p = 2 * w + 1
        c = 2 * ((n / 2) ** p) / p
        U = np.linspace(0, 1, endpoint = True, num=num_samples)
        inner = U * p * c - (n / 2) ** p
        K = np.sign(inner) * np.power(np.abs(inner), 1 / p) + n / 2

    # round to nearest integer and clip to valid k range [1, n-1]
    K_int = np.around(K).astype(int)
    K_int = np.clip(K_int, 1, n - 1)
    return K_int


# ============== BODY ==============
if __name__ == "__main__":
    seed = 42  # seed for reproducibility

    # Generating n vs sum of demands (OPT)
    n_vs_sod_outfile = "final/n_vs_sod.csv"
    ns = list(range(100, 100_000, 100)) + list(range(100_000, 1_001_000, 1_000))
    
    generate_n_vs_sod(n_vs_sod_outfile, ns, seed = seed)
    
    # Generating k vs sum of demands (OPT)
    k_vs_sod_outfile = "final/k_vs_sod.csv"
    n = 1_000_000
    w = 6
    num_samples = 1000

    generate_k_vs_sod(k_vs_sod_outfile, n, w, num_samples, seed=seed)

    # Generating n vs sum of demands (OPT), restricted to paths
    n_vs_sod_path_outfile = "final/n_vs_sod_paths.csv"

    generate_n_vs_sod(n_vs_sod_path_outfile, ns, path=True, seed=seed)