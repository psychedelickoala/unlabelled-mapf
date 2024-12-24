import networkx as nx
import random
import matplotlib.pyplot as plt
import numpy as np
from algorithm import DemandNode, DemandTree

n = 20
k = 5

class Window:
    class Palette:
        offwhite = np.array([246, 238, 227])/255
        citron = np.array([202, 207, 133])/255
        olivine = np.array([140, 186, 128])/255
        afblue = np.array([101, 142, 156])/255
        uviolet = np.array([77, 83, 130])/255
        eviolet = np.array([77, 83, 130])/255

    LAYOUT: dict = {
        "ax" : [0.05, 0.05, 0.85, 0.9],
        "axslider" : [0.24, 0.1, 0.02, 0.8],
    }

    def __init__(self, n: int, k: int) -> None:
        self.build_widgets()
        self.reset_graph(n, k)
        self.calc = DemandTree(self.graph, self.agents, self.targets)
        
        self.update_display()



    def reset_graph(self, n: int, k: int):
        self.graph = nx.random_unlabeled_tree(n, seed = 42)
        random.seed(42)
        self.agents = random.sample(range(n), k)
        self.targets = random.sample(range(n), k)
        self.pos_dict: dict = nx.bfs_layout(self.graph, 0, align='horizontal')

        # flip layout
        for node in self.pos_dict:
            self.pos_dict[node][1] = -self.pos_dict[node][1]

        self.target_array_x = [self.pos_dict[node][0] for node in self.targets]
        self.target_array_y = [self.pos_dict[node][1] for node in self.targets]

        self.agent_array_x = [self.pos_dict[node][0] for node in self.agents]
        self.agent_array_y = [self.pos_dict[node][1] for node in self.agents]

    def update_display(self):
        # clear axes
        self.ax.cla()

        nx.draw_networkx(
            G = self.graph, 
            pos = self.pos_dict, 
            with_labels = False, 
            ax = self.ax, 
            node_size = 30, 
            node_color = self.Palette.afblue,
            edge_color = self.Palette.afblue,
            width = 2
        )

        self.ax.plot(self.target_array_x, self.target_array_y, marker='s', color = self.Palette.afblue, markersize=18, linewidth = 0)
        self.ax.plot(self.agent_array_x, self.agent_array_y, marker='^', color = self.Palette.uviolet, markersize=18, linewidth = 0)

    def build_widgets(self):
        # figure and axes
        self.fig = plt.figure(facecolor=self.Palette.eviolet)
        self.ax = self.fig.add_axes(self.LAYOUT["ax"], facecolor = self.Palette.offwhite)

window = Window(n, k)
plt.show()