import networkx as nx
import random
import csv
from math import sqrt, log

def rand_sum_of_demands(n, k, labelled = True):
    if labelled:
        G = nx.random_labeled_tree(n)
    else:
        G = nx.random_unlabeled_tree(n)
    
    is_agent = [False]*n
    agent_positions = random.sample(range(n), k)
    for i in agent_positions:
        is_agent[i] = True

    is_target = [False]*n
    target_positions = random.sample(range(n), k)
    for i in target_positions:
        is_target[i] = True

    visited = [False]*n
    sum_of_demands = 0
    parent = [None]*n
    demand = [0]*n
    stack = [
        0  # node
    ]
    while len(stack) > 0: # while stack is not empty
        u = stack[-1]  # peek the top of the stack
        
        if visited[u]: # already processed children
            stack.pop()
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


# Open a CSV file to write the results
with open("alg_testing/sum_of_demands_labelled_ctd.csv", "w", newline="") as f:
    writer = csv.writer(f)
    # Write the header row to the CSV file
    writer.writerow(["n", "k", "sum_of_demands"])
    
    start = 100100
    end = 1000100
    step = 1000

    print("Generating", (end-start)//step, "data points...")

    # Loop over a range of values for n
    for n in range(start, end, step):
        if (n-start)%((end-start)//100) == 0:
            print("Progress: ", (n-start)//((end-start)//100), "%")
        k_values = [1, 5, int(log(n)), int(sqrt(n)), n//10, n//4, n//2]
        
        for k in k_values:
            sum_of_demands = rand_sum_of_demands(n, k)
            # Write the results of the algorithm to the CSV file
            writer.writerow([n, k, sum_of_demands])

    print("Done!")