import networkx as nx
import random
import matplotlib.pyplot as plt
from matplotlib.widgets import Button
import numpy as np
from algorithm import DemandNode, DemandTree
from time import sleep

n = 35
k = 8

class Window:
    class Palette:
        offwhite = np.array([246, 238, 227])/255
        citron = np.array([202, 207, 133])/255
        olivine = np.array([140, 186, 128])/255
        afblue = np.array([101, 142, 156])/255
        uviolet = np.array([77, 83, 130])/255
        eviolet = np.array([77, 83, 130])/255

    LAYOUT: dict = {
        "ax" : [0.05, 0.05, 0.8, 0.9],
        "axnext" : [0.87, 0.87, 0.07, 0.07],
        "axback" : [0.87, 0.77, 0.07, 0.07],
        "axreset" : [0.87, 0.67, 0.07, 0.07]
    }

    def __init__(self, n: int, k: int) -> None:
        self.build_widgets()
        self.n, self.k = n, k
        self.reset_graph()

    def reset_graph(self, event = None):
        self.graph = nx.random_unlabeled_tree(n)
        #random.seed(42)
        self.agents = random.sample(range(self.n), self.k)
        self.targets = random.sample(range(self.n), self.k)
        self.pos_dict: dict = nx.bfs_layout(self.graph, 0, align='horizontal')

        # flip layout
        for node in self.pos_dict:
            self.pos_dict[node][1] = -self.pos_dict[node][1]

        self.target_array_x = [self.pos_dict[node][0] for node in self.targets]
        self.target_array_y = [self.pos_dict[node][1] for node in self.targets]

        self.agent_array_x = [self.pos_dict[node][0] for node in self.agents]
        self.agent_array_y = [self.pos_dict[node][1] for node in self.agents]

        calc = DemandTree(self.graph, self.agents, self.targets)  # runs algorithm
        self.moves = calc.moves

        self.build_agent_positions()
        self.time = 0


        self.update_display()

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

        self.fig.canvas.draw_idle()

    def key_press(self, event):

        if event.key == "n":
            if self.time < len(self.agent_positions) - 1:
                self.time += 1
                self.agent_array_x, self.agent_array_y = self.agent_positions[self.time]
                self.update_display()

        if event.key == "b":
            if self.time > 0:
                self.time -= 1
                self.agent_array_x, self.agent_array_y = self.agent_positions[self.time]
                self.update_display()

        if event.key == "r":
            self.reset_graph()

    def next_frame(self, event = None):
        if self.time < len(self.agent_positions) - 1:
            self.time += 1
            self.agent_array_x, self.agent_array_y = self.agent_positions[self.time]
            self.update_display()

    def prev_frame(self, event = None):
        if self.time > 0:
            self.time -= 1
            self.agent_array_x, self.agent_array_y = self.agent_positions[self.time]
            self.update_display()

    def build_agent_positions(self):
        self.agent_positions = []
        
        curr_agents = [a for a in self.agents]
        for move_dict in self.moves:
            
            # determine still agents
            still_agents = []
            for a in curr_agents:
                if a not in move_dict:
                    still_agents.append(a)

            # start/end x and y arrays
            agents_start_x = np.array([self.pos_dict[a][0] for a in move_dict] + [self.pos_dict[a][0] for a in still_agents])
            agents_start_y = np.array([self.pos_dict[a][1] for a in move_dict] + [self.pos_dict[a][1] for a in still_agents])

            agents_end_x = np.array([self.pos_dict[move_dict[a]][0] for a in move_dict] + [self.pos_dict[a][0] for a in still_agents])
            agents_end_y = np.array([self.pos_dict[move_dict[a]][1] for a in move_dict] + [self.pos_dict[a][1] for a in still_agents])
            
            frames = 2
            for i in range(frames):
                agents_x = agents_start_x*(1 - i/frames) + agents_end_x*(i/frames)
                agents_y = agents_start_y*(1 - i/frames) + agents_end_y*(i/frames)
                self.agent_positions.append((agents_x, agents_y))
            
            # reset current agents
            curr_agents.clear()
            for end_node in move_dict.values():
                curr_agents.append(end_node)
            for a in still_agents:
                curr_agents.append(a)

        self.agent_positions.append((agents_end_x, agents_end_y))

    def build_widgets(self):
        # figure and axes
        self.fig = plt.figure(facecolor = self.Palette.eviolet)
        self.ax = self.fig.add_axes(self.LAYOUT["ax"], facecolor = self.Palette.offwhite)
        self.ax_next_button = self.fig.add_axes(self.LAYOUT["axnext"])
        self.ax_back_button = self.fig.add_axes(self.LAYOUT["axback"])
        self.ax_reset_button = self.fig.add_axes(self.LAYOUT["axreset"])

        self.next_button = Button(
            ax=self.ax_next_button,
            label = "NEXT",
            color = self.Palette.olivine,
            hovercolor = self.Palette.citron
        )
        self.next_button.on_clicked(self.next_frame)

        self.back_button = Button(
            ax=self.ax_back_button,
            label = "BACK",
            color = self.Palette.olivine,
            hovercolor = self.Palette.citron
        )
        self.back_button.on_clicked(self.prev_frame)

        self.reset_button = Button(
            ax=self.ax_reset_button,
            label = "NEW TREE",
            color = self.Palette.olivine,
            hovercolor = self.Palette.citron
        )
        self.reset_button.on_clicked(self.reset_graph)


        self.fig.canvas.mpl_connect("key_press_event", self.key_press)

window = Window(n, k)
plt.show()

