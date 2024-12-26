import networkx as nx
import random
import matplotlib.pyplot as plt
from matplotlib.widgets import Button
from matplotlib.backend_bases import MouseEvent
import numpy as np
from algorithm import DemandTree

n = 35
k = 8

class Window:
    class Palette:
        # standard
        off_white = [246, 238, 227]
        light_grey = [200, 200, 200]
        mid_grey = [128, 128, 128]

        # retro palette
        chestnut = [139, 81, 62]
        spanish_orange = [230, 103, 22]
        princeton_orange = [250, 142, 16]
        orange_peel = [254, 168, 58]
        papaya_whip = [254, 242, 218]
        celadon = [180, 220, 183]

        # bright palette
        citron = [202, 207, 133]
        olivine = [140, 186, 128]
        air_force_blue = [101, 142, 156],
        english_violet = [77, 83, 130]
        ultra_violet = [77, 83, 130]

        # green/orange palette
        dark_moss_green = [96, 108, 56]
        pakistan_green = [40, 54, 24]
        cornsilk = [254, 250, 224]
        sage = [187, 180, 129]
        sunset = [238, 206, 159]
        earth_yellow = [221, 161, 94]
        tigers_eye = [188, 108, 37]

        light_bg = np.array(cornsilk)/255
        target_colour = np.array(tigers_eye)/255
        hover_colour = np.array(sunset)/255
        button_colour = np.array(earth_yellow)/255
        graph_colour = np.array(sage)/255
        agent_colour = np.array(dark_moss_green)/255
        dark_bg = np.array(pakistan_green)/255

    LAYOUT: dict = {
        "ax" : [0.03, 0.03, 0.81, 0.94],
        "axnext" : [0.87, 0.93, 0.1, 0.04],
        "axtime" : [0.87, 0.88, 0.1, 0.05],
        "axback" : [0.87, 0.84, 0.1, 0.04],
        "axnplus50" : [0.87, 0.78, 0.1, 0.04],
        "axnplus1" : [0.87, 0.74, 0.1, 0.04],
        "axntext" : [0.87, 0.69, 0.1, 0.05],
        "axnminus1": [0.87, 0.65, 0.1, 0.04],
        "axnminus50" : [0.87, 0.61, 0.1, 0.04],
        "axkplus50" : [0.87, 0.55, 0.1, 0.04],
        "axkplus1" : [0.87, 0.51, 0.1, 0.04],
        "axktext" : [0.87, 0.46, 0.1, 0.05],
        "axkminus1": [0.87, 0.42, 0.1, 0.04],
        "axkminus50": [0.87, 0.38, 0.1, 0.04],
        "axreset" : [0.87, 0.30, 0.1, 0.05],
        "axlayout" : [0.87, 0.23, 0.1, 0.05],
        "axmakespan" : [0.87, 0.13, 0.1, 0.05],
        "axsumofcosts" : [0.87, 0.03, 0.1, 0.05]
    }

    def __init__(self, n: int, k: int) -> None:
        self.n, self.k = n, k
        self.time = 0
        self.rooted = True
        self.build_widgets()

        self.reset_graph()

    def set_layout(self, new_graph = True) -> None:
        if new_graph:
            if self.rooted:
                self.pos_dict = nx.bfs_layout(self.graph, 0, align='horizontal')
                # flip layout
                for node in self.pos_dict:
                    self.pos_dict[node][1] = -self.pos_dict[node][1]
            else:
                self.pos_dict = nx.spring_layout(self.graph)

        
        self.target_array_x = [self.pos_dict[node][0] for node in self.targets]
        self.target_array_y = [self.pos_dict[node][1] for node in self.targets]

        self.agent_array_x = [self.pos_dict[node][0] for node in self.agents]
        self.agent_array_y = [self.pos_dict[node][1] for node in self.agents]

        if len(self.moves) > 0:
            self.build_agent_positions()  # translate abstract moves to exact positions


    def reset_graph(self, event = None, new_graph = True):
        if new_graph:
            self.graph = nx.random_unlabeled_tree(self.n)

        # pick agents and targets
        self.agents = random.sample(range(self.n), self.k)
        self.targets = random.sample(range(self.n), self.k)

        calc = DemandTree(self.graph, self.agents, self.targets)  # runs algorithm
        self.moves = calc.moves
        
        self.reached = calc.reached
        self.set_layout(new_graph)

        makespan = len(self.moves)
        sum_of_costs = calc.sum_of_costs

        self.ax_makespan.cla()
        self.ax_soc.cla()
        # Hide X and Y axes label marks
        self.ax_makespan.xaxis.set_tick_params(labelbottom=False)
        self.ax_makespan.yaxis.set_tick_params(labelleft=False)

        # Hide X and Y axes tick marks
        self.ax_makespan.set_xticks([])
        self.ax_makespan.set_yticks([])
        self.ax_makespan.text(0.5, 0.5, f"{makespan}", horizontalalignment='center', verticalalignment='center')

                # Hide X and Y axes label marks
        self.ax_soc.xaxis.set_tick_params(labelbottom=False)
        self.ax_soc.yaxis.set_tick_params(labelleft=False)

        # Hide X and Y axes tick marks
        self.ax_soc.set_xticks([])
        self.ax_soc.set_yticks([])
        self.ax_soc.text(0.5, 0.5, f"{sum_of_costs} ({np.round(sum_of_costs/self.k, 1)} ea)", horizontalalignment='center', verticalalignment='center')

        self.ax_makespan.set_title('MAKESPAN', color = self.Palette.light_bg, fontsize = 10)
        self.ax_soc.set_title('SUM OF COSTS', color = self.Palette.light_bg, fontsize = 10)


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
            node_color = self.Palette.graph_colour,
            edge_color = self.Palette.graph_colour,
            width = 2
        )



        self.ax.plot(self.target_array_x, self.target_array_y, marker='s', color = self.Palette.target_colour, markersize=18, linewidth = 0)
        
        self.target_reached_x = [self.pos_dict[node][0] for node in self.targets if self.reached[node] <= self.time//2]
        self.target_reached_y = [self.pos_dict[node][1] for node in self.targets if self.reached[node] <= self.time//2]
        self.ax.plot(self.target_reached_x, self.target_reached_y, marker='s', color = self.Palette.graph_colour, markersize=18, linewidth = 0)


        self.ax.plot(self.agent_array_x, self.agent_array_y, marker='^', color = self.Palette.agent_colour, markersize=18, linewidth = 0)

        self.ax_time.cla()
        self.ax_time.text(0.5, 0.5, f"t = {self.time/2}", horizontalalignment='center', verticalalignment='center')

        # Hide X and Y axes label marks
        self.ax_time.xaxis.set_tick_params(labelbottom=False)
        self.ax_time.yaxis.set_tick_params(labelleft=False)

        # Hide X and Y axes tick marks
        self.ax_time.set_xticks([])
        self.ax_time.set_yticks([])

        self.fig.canvas.draw_idle()

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

    def change_n(self, event : MouseEvent):
        if event.inaxes == self.ax_n_plus_1:
            self.n += 1
        elif event.inaxes == self.ax_n_plus_50:
            self.n += 50
        elif event.inaxes == self.ax_n_minus_1:
            if self.n > self.k + 1:
                self.n -= 1
            else:
                return
        elif event.inaxes == self.ax_n_minus_50:
            if self.n > self.k + 50:
                self.n -= 50
            else:
                return
        self.reset_graph()
        self.ax_n_text.cla()
        # Hide X and Y axes label marks
        self.ax_n_text.xaxis.set_tick_params(labelbottom=False)
        self.ax_n_text.yaxis.set_tick_params(labelleft=False)

        # Hide X and Y axes tick marks
        self.ax_n_text.set_xticks([])
        self.ax_n_text.set_yticks([])
        self.ax_n_text.text(0.5, 0.5, f"n = {self.n}", horizontalalignment='center', verticalalignment='center')
        self.update_display()

    def change_k(self, event : MouseEvent):
        if event.inaxes == self.ax_k_plus_1:
            if self.k < self.n - 1:
                self.k += 1
            else:
                return
            
        elif event.inaxes == self.ax_k_plus_50:
            if self.k < self.n - 50:
                self.k += 50
            else:
                return
            
        elif event.inaxes == self.ax_k_minus_50:
            if self.k > 50:
                self.k -= 50
            else:
                return
        else:
            if self.k > 1:
                self.k -= 1
            else:
                return
        self.reset_graph(new_graph=False)
        self.ax_k_text.cla()
        # Hide X and Y axes label marks
        self.ax_k_text.xaxis.set_tick_params(labelbottom=False)
        self.ax_k_text.yaxis.set_tick_params(labelleft=False)

        # Hide X and Y axes tick marks
        self.ax_k_text.set_xticks([])
        self.ax_k_text.set_yticks([])
        self.ax_k_text.text(0.5, 0.5, f"k = {self.k}", horizontalalignment='center', verticalalignment='center')
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

    def toggle_layout(self, event = None):
        if self.rooted:
            self.rooted = False
            self.layout_toggle.label.set_text("ROOTED")

        else:
            self.rooted = True
            self.layout_toggle.label.set_text("SPRING")

        self.set_layout()
        self.update_display()


    def build_widgets(self):
        # figure and axes
        self.fig = plt.figure(facecolor = self.Palette.dark_bg)
        self.ax = self.fig.add_axes(self.LAYOUT["ax"], facecolor = self.Palette.light_bg)

        # buttons and widgets
        self.ax_next_button = self.fig.add_axes(self.LAYOUT["axnext"])
        self.ax_time = self.fig.add_axes(self.LAYOUT["axtime"], facecolor = self.Palette.light_bg)
        self.ax_back_button = self.fig.add_axes(self.LAYOUT["axback"])
        
        self.ax_n_plus_50 = self.fig.add_axes(self.LAYOUT["axnplus50"])
        self.ax_n_plus_1 = self.fig.add_axes(self.LAYOUT["axnplus1"])
        self.ax_n_text = self.fig.add_axes(self.LAYOUT["axntext"], facecolor = self.Palette.light_bg)
        self.ax_n_minus_1 = self.fig.add_axes(self.LAYOUT["axnminus1"])
        self.ax_n_minus_50 = self.fig.add_axes(self.LAYOUT["axnminus50"])
        
        self.ax_k_plus_50 = self.fig.add_axes(self.LAYOUT["axkplus50"])
        self.ax_k_plus_1 = self.fig.add_axes(self.LAYOUT["axkplus1"])
        self.ax_k_text = self.fig.add_axes(self.LAYOUT["axktext"], facecolor = self.Palette.light_bg)
        self.ax_k_minus_1 = self.fig.add_axes(self.LAYOUT["axkminus1"])
        self.ax_k_minus_50 = self.fig.add_axes(self.LAYOUT["axkminus50"])

        self.ax_reset_button = self.fig.add_axes(self.LAYOUT["axreset"])

        self.ax_layout = self.fig.add_axes(self.LAYOUT["axlayout"], facecolor = self.Palette.light_bg)

        self.ax_makespan = self.fig.add_axes(self.LAYOUT["axmakespan"], facecolor = self.Palette.light_bg)
        self.ax_soc = self.fig.add_axes(self.LAYOUT["axsumofcosts"], facecolor = self.Palette.light_bg)

        # next and back (time) buttons
        self.next_button = Button(
            ax=self.ax_next_button,
            label = "NEXT",
            color = self.Palette.button_colour,
            hovercolor = self.Palette.hover_colour
        )
        self.next_button.on_clicked(self.next_frame)

        self.back_button = Button(
            ax=self.ax_back_button,
            label = "BACK",
            color = self.Palette.button_colour,
            hovercolor = self.Palette.hover_colour
        )
        self.back_button.on_clicked(self.prev_frame)


        self.ax_time.text(0.5, 0.5, f"t = {self.time/2}", horizontalalignment='center', verticalalignment='center')

        # reset button

        self.reset_button = Button(
            ax=self.ax_reset_button,
            label = "NEW TREE",
            color = self.Palette.button_colour,
            hovercolor = self.Palette.hover_colour
        )
        self.reset_button.on_clicked(self.reset_graph)

        # changing n

        self.n_plus_50 = Button(
            ax=self.ax_n_plus_50,
            label = "+ 50",
            color = self.Palette.button_colour,
            hovercolor = self.Palette.hover_colour
        )
        self.n_plus_50.on_clicked(self.change_n)

        self.n_plus_1 = Button(
            ax=self.ax_n_plus_1,
            label = "+ 1",
            color = self.Palette.button_colour,
            hovercolor = self.Palette.hover_colour
        )
        self.n_plus_1.on_clicked(self.change_n)

        self.n_minus_1 = Button(
            ax=self.ax_n_minus_1,
            label = "- 1",
            color = self.Palette.button_colour,
            hovercolor = self.Palette.hover_colour
        )
        self.n_minus_1.on_clicked(self.change_n)

        self.n_minus_50 = Button(
            ax=self.ax_n_minus_50,
            label = "- 50",
            color = self.Palette.button_colour,
            hovercolor = self.Palette.hover_colour
        )
        self.n_minus_50.on_clicked(self.change_n)

        # Hide X and Y axes label marks
        self.ax_n_text.xaxis.set_tick_params(labelbottom=False)
        self.ax_n_text.yaxis.set_tick_params(labelleft=False)

        # Hide X and Y axes tick marks
        self.ax_n_text.set_xticks([])
        self.ax_n_text.set_yticks([])
        self.ax_n_text.text(0.5, 0.5, f"n = {self.n}", horizontalalignment='center', verticalalignment='center')

        # change k

        self.k_plus_50 = Button(
            ax=self.ax_k_plus_50,
            label = "+ 50",
            color = self.Palette.button_colour,
            hovercolor = self.Palette.hover_colour
        )
        self.k_plus_50.on_clicked(self.change_k)

        self.k_plus_1 = Button(
            ax=self.ax_k_plus_1,
            label = "+ 1",
            color = self.Palette.button_colour,
            hovercolor = self.Palette.hover_colour
        )
        self.k_plus_1.on_clicked(self.change_k)

        self.k_minus_1 = Button(
            ax=self.ax_k_minus_1,
            label = "- 1",
            color = self.Palette.button_colour,
            hovercolor = self.Palette.hover_colour
        )
        self.k_minus_1.on_clicked(self.change_k)

        self.k_minus_50 = Button(
            ax=self.ax_k_minus_50,
            label = "- 50",
            color = self.Palette.button_colour,
            hovercolor = self.Palette.hover_colour
        )
        self.k_minus_50.on_clicked(self.change_k)

        # Hide X and Y axes label marks
        self.ax_k_text.xaxis.set_tick_params(labelbottom=False)
        self.ax_k_text.yaxis.set_tick_params(labelleft=False)

        # Hide X and Y axes tick marks
        self.ax_k_text.set_xticks([])
        self.ax_k_text.set_yticks([])
        self.ax_k_text.text(0.5, 0.5, f"k = {self.k}", horizontalalignment='center', verticalalignment='center')

        # graph layout toggle
        self.layout_toggle = Button(
            ax=self.ax_layout,
            label = "SPRING",
            color = self.Palette.button_colour,
            hovercolor = self.Palette.hover_colour
        )
        self.layout_toggle.on_clicked(self.toggle_layout)

window = Window(n, k)
plt.show()

