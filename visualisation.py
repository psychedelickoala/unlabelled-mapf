import networkx as nx
import random
import matplotlib.pyplot as plt
import numpy as np
from algorithm import DemandNode, DemandTree

n = 20
k = 5
# Create a random unlabelled tree
G = nx.random_unlabeled_tree(n, seed = 42)

random.seed(42)
agent_vertices = random.sample(range(n), k)
target_vertices = random.sample(range(n), k)

pos = nx.bfs_layout(G, 0, align='horizontal')
print(pos)

# flip layout
for node in pos:
    pos[node][1] = -pos[node][1]
# Draw the graph using Matplotlib
nx.draw_networkx(G, pos=pos, with_labels=True)
target_array_x = [pos[node][0] for node in target_vertices]
target_array_y = [pos[node][1] for node in target_vertices]
plt.plot(target_array_x, target_array_y, 'gs', markersize=18, linewidth = 0)



agent_array_x = [pos[node][0] for node in agent_vertices]
agent_array_y = [pos[node][1] for node in agent_vertices]
plt.plot(agent_array_x, agent_array_y, 'r^', markersize=18, linewidth = 0)

DemandTree(G, agent_vertices, target_vertices)

plt.show()