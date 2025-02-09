import networkx as nx
import random
import numpy as np
import csv

from mapf_algorithm import DemandTree

# Open a CSV file to write the results
with open("alg_testing/results3.csv", "w", newline="") as f:
    writer = csv.writer(f)
    # Write the header row to the CSV file
    writer.writerow(["n", "num_of_moves"])
    
    # Loop over a range of values for n
    for n in range(50, 1000000, 100):
        # k = n//2
        k = n//2
        #k = random.randint(1, n)
        print(n)

        # Generate a random labeled tree graph with n nodes
        graph: nx.Graph = nx.random_labeled_tree(n)

        # Randomly select k agents and k targets from the nodes in the graph
        agents = random.sample(range(n), k)
        targets = random.sample(range(n), k)

        # Create a DemandTree object to run the algorithm
        calc = DemandTree(graph, agents, targets)

        # Write the results of the algorithm to the CSV file
        writer.writerow([n, calc.num_of_moves])