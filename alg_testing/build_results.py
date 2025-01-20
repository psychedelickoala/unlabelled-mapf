import networkx as nx
import random
import numpy as np
import csv

from mapf_algorithm import DemandTree

# Open a CSV file to write the results
with open("alg_testing/results.csv", "w", newline="") as f:
    writer = csv.writer(f)
    # Write the header row to the CSV file
    writer.writerow(["n", "k", "diameter", "makespan", "soc", "avg_soc"])
    
    # Loop over a range of values for n
    for n in range(50, 10000, 20):
        # For each value of n, perform n iterations
        for k in range(1, n, int(n/10)):
            #k = random.randint(1, n)
            print(k)

            # Generate a random unlabeled tree graph with n nodes
            graph: nx.Graph = nx.random_unlabeled_tree(n)

            # Randomly select k agents and k targets from the nodes in the graph
            agents = random.sample(range(n), k)
            targets = random.sample(range(n), k)

            # Create a DemandTree object to run the algorithm
            calc = DemandTree(graph, agents, targets)

            # Write the results of the algorithm to the CSV file
            writer.writerow([n, k, nx.diameter(graph), calc.makespan, calc.sum_of_costs, np.round(calc.sum_of_costs/k, 2)])