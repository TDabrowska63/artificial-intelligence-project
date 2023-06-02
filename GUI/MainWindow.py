import string
import tkinter as tk
import customtkinter as ctk
import networkx as nx
import time
import sys
import numpy as np

from matplotlib import pyplot as plt
from GUI.PathWindow import PathWindow
from Misc.CustomGraph import CustomGraph
from Misc.Constants import Algorithms, Colours
from Algorithms.Astar import Astar
from Algorithms.Dijkstra import Dijkstra
from Algorithms.RandomSearch import RandomSearch
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg)


class MainWindow:
    root: ctk.CTk = None
    main_window: ctk.CTkToplevel = None
    path_window: PathWindow = None
    open_main_button: ctk.CTkButton = None
    map_frame: ctk.CTkFrame = None
    sidebar_frame: ctk.CTkFrame = None
    logo_label: ctk.CTkLabel = None
    density_label: ctk.CTkLabel = None
    chosen_start_city: tk.StringVar = None
    start_label: ctk.CTkLabel = None
    start_option: ctk.CTkOptionMenu = None
    chosen_end_city: tk.StringVar = None
    end_label: ctk.CTkLabel = None
    end_option: ctk.CTkOptionMenu = None
    choose_algorithm_frame: ctk.CTkFrame = None
    radio_var: tk.IntVar = None
    label_choose_algorithm: ctk.CTkLabel = None
    dijkstra_button: ctk.CTkRadioButton = None
    astar_button: ctk.CTkRadioButton = None
    random_search_button: ctk.CTkRadioButton = None

    choose_type_frame: ctk.CTkFrame = None
    radio_type: tk.IntVar = None
    label_choose_type: ctk.CTkLabel = None
    automatic_button: ctk.CTkRadioButton = None
    manual_button: ctk.CTkRadioButton = None

    run_button: ctk.CTkButton = None
    prev_button: ctk.CTkButton = None
    next_button: ctk.CTkButton = None
    exit_button: ctk.CTkButton = None
    cities: string = []
    gui_width: int = 1300
    gui_height: int = 880
    fig_size = (11, 8)
    density: int = 90
    number_of_cities: int = 20
    graph: CustomGraph = None
    figure: plt.Figure = None
    canvas: FigureCanvasTkAgg = None
    nx_graph: nx.Graph = None
    color_map: string = []
    algorithm_chosen: Algorithms = None
    heuristic = None
    state = 0
    states_matrix = None
    visited_list = None
    path = None
    distance: int = 0
    def __init__(self, root, density: int, number_of_cities: int):
        self.root = root
        self.density = density
        self.number_of_cities = number_of_cities
        self.create_map()
        self.set_up_main_window()
        self.add_map()
        self.add_sidebar()

    def create_map(self):
        self.graph = CustomGraph(self.number_of_cities, self.density)
        self.graph.randomize()
        # self.graph.printMe()

    def set_up_main_window(self):
        self.main_window = ctk.CTkToplevel()
        self.main_window.title("AI Project - Travelling from City to City")
        self.main_window.geometry(f"{self.gui_width}x{self.gui_height}")
        self.main_window.grid_columnconfigure(0, weight=5)
        self.main_window.grid_columnconfigure(1, weight=1)

    def add_map(self):
        if self.map_frame is not None:
            self.map_frame.destroy()
        self.map_frame = ctk.CTkFrame(self.main_window, height=self.gui_height - 40, corner_radius=10)
        self.map_frame.grid(row=0, column=0, rowspan=4, padx=(20, 0), pady=(20, 0), sticky="nsew")
        # creating networkx graph with grey nodes
        self.nx_graph = nx.Graph()
        self.default_cities_coloring()
        # creating figure and canvas to draw on
        self.figure = plt.Figure(figsize=self.fig_size, dpi=100)
        self.canvas = FigureCanvasTkAgg(self.figure, self.map_frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().grid(row=0, column=0)
        # draw graph
        self.draw_graph()

    def default_cities_coloring(self):
        # default coloring - all cities to gray
        self.color_map.clear()
        for city in range(self.number_of_cities):
            self.color_map.append('grey')

    def add_sidebar(self):
        # creating sidebar
        self.sidebar_frame = ctk.CTkFrame(self.main_window, height=self.gui_height - 40, corner_radius=10)
        self.sidebar_frame.grid(row=0, column=1, padx=(20, 20), pady=(20, 0), sticky="nsew")
        # adding sidebar content
        self.show_sidebar_labels()
        self.show_cities_to_choose()
        self.show_algorithms_to_choose()
        self.show_view_type_to_choose()
        self.show_buttons()

    def show_sidebar_labels(self):
        # logo/title label
        self.logo_label = ctk.CTkLabel(self.sidebar_frame, text="Shortest Path",
                                       font=ctk.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(10, 5))
        # show chosen density from start window
        self.density_label = ctk.CTkLabel(self.sidebar_frame, bg_color='#147',
                                          text=f" Density of roads: {self.density} ",
                                          font=ctk.CTkFont(size=15))
        self.density_label.grid(row=1, column=0, padx=20, pady=(5, 0))

    def show_cities_to_choose(self):
        for i in range(self.number_of_cities):
            self.cities.append(str(i))

        self.chosen_start_city = tk.StringVar(value="0")
        self.start_label = ctk.CTkLabel(self.sidebar_frame, text="Start City:")
        self.start_label.grid(row=2, column=0, padx=20, pady=(10, 5), sticky="w")
        self.start_option = ctk.CTkOptionMenu(self.sidebar_frame, dynamic_resizing=False,
                                              variable=self.chosen_start_city, values=self.cities)
        self.start_option.grid(row=3, column=0, padx=20, pady=(0, 10))

        self.chosen_end_city = tk.StringVar(value="0")
        self.end_label = ctk.CTkLabel(self.sidebar_frame, text="End City:")
        self.end_label.grid(row=4, column=0, padx=20, pady=(10, 5), sticky="w")
        self.end_option = ctk.CTkOptionMenu(self.sidebar_frame, dynamic_resizing=False,
                                            variable=self.chosen_end_city, values=self.cities)
        self.end_option.grid(row=5, column=0, padx=20, pady=(0, 5))

    def show_algorithms_to_choose(self):
        self.choose_algorithm_frame = ctk.CTkFrame(self.sidebar_frame)
        self.choose_algorithm_frame.grid(row=6, column=0, padx=20, pady=(20, 5), sticky="nsew")
        self.radio_var = tk.IntVar(value=0)
        self.label_choose_algorithm = ctk.CTkLabel(master=self.choose_algorithm_frame, text="Searching Algorithm:")
        self.label_choose_algorithm.grid(row=0, column=2, columnspan=1, padx=10, pady=5, sticky="")
        self.astar_button = ctk.CTkRadioButton(master=self.choose_algorithm_frame, text="A*", variable=self.radio_var,
                                               value=0)
        self.astar_button.grid(row=1, column=2, pady=10, padx=10, sticky="nw")
        self.dijkstra_button = ctk.CTkRadioButton(master=self.choose_algorithm_frame, text="Dijkstra",
                                                  variable=self.radio_var, value=1)
        self.dijkstra_button.grid(row=2, column=2, pady=10, padx=10, sticky="nw")
        self.random_search_button = ctk.CTkRadioButton(master=self.choose_algorithm_frame, text="Random Search",
                                                       variable=self.radio_var, value=2)
        self.random_search_button.grid(row=3, column=2, pady=10, padx=10, sticky="nw")

    def show_view_type_to_choose(self):
        self.choose_type_frame = ctk.CTkFrame(self.sidebar_frame)
        self.choose_type_frame.grid(row=7, column=0, padx=20, pady=(5, 10), sticky="nsew")
        self.radio_type = tk.IntVar(value=0)
        self.label_choose_type = ctk.CTkLabel(master=self.choose_type_frame, text="Viewing Type:")
        self.label_choose_type.grid(row=0, column=2, columnspan=1, padx=10, pady=5, sticky="")
        self.automatic_button = ctk.CTkRadioButton(master=self.choose_type_frame, text="Automatic",
                                                   variable=self.radio_type,
                                                   value=0)
        self.automatic_button.grid(row=1, column=2, pady=10, padx=10, sticky="nw")
        self.manual_button = ctk.CTkRadioButton(master=self.choose_type_frame, text="Manual",
                                                variable=self.radio_type, value=1)
        self.manual_button.grid(row=2, column=2, pady=10, padx=10, sticky="nw")

    def show_buttons(self):
        self.run_button = ctk.CTkButton(self.sidebar_frame, text="Calculate Shortest Path", command=self.run_searching)
        self.run_button.grid(row=8, column=0, padx=(20, 20), pady=(10, 10), sticky="nsew")

        self.prev_button = ctk.CTkButton(self.sidebar_frame, text="Prev", command=lambda: self.change_state(-1))
        self.prev_button.grid(row=9, column=0, padx=20, pady=(10, 5), sticky="nsew")
        self.prev_button.configure(state="disabled")
        self.next_button = ctk.CTkButton(self.sidebar_frame, text="Next", command=lambda: self.change_state(1))
        self.next_button.grid(row=10, column=0, padx=20, pady=(0, 10), sticky="nsew")
        self.next_button.configure(state="disabled")

        self.exit_button = ctk.CTkButton(self.sidebar_frame, text="Exit", command=self.exit_from_program)
        self.exit_button.grid(row=11, column=0, padx=(20, 20), pady=(10, 20), sticky="nsew")

    def change_state(self, change: int):
        if self.state + change <= 0:
            self.prev_button.configure(state="disabled")
        elif self.state + change > 0:
            self.prev_button.configure(state="normal")

        maxi = 0
        if self.algorithm_chosen == Algorithms.ASTAR_A:
            maxi = len(self.states_matrix[1, :])
        elif self.algorithm_chosen == Algorithms.DIJKSTRA_A:
            maxi = len(self.visited_list)

        if self.state + change >= maxi:
            self.next_button.configure(state="disabled")
        elif self.state + change < maxi:
            self.next_button.configure(state="normal")

        self.state += change

        if self.algorithm_chosen == Algorithms.ASTAR_A:
            self.astar_visualisation_extended()
        elif self.algorithm_chosen == Algorithms.DIJKSTRA_A:
            self.dijkstra_visualisation_extended()


    def run_searching(self):
        print(f"calculating shortest path... {self.radio_var.get()}")
        print(f"start city: {int(self.chosen_start_city.get())}, end city: {int(self.chosen_end_city.get())}")
        distance = 0
        self.path = []
        if self.radio_var.get() == Algorithms.DIJKSTRA_A.value:
            print("Dijkstra was chosen")
            self.algorithm_chosen = Algorithms.DIJKSTRA_A
            d = Dijkstra(self.graph)
            self.distance, self.path, self.visited_list = \
                d.dijkstra_algorithm(int(self.chosen_start_city.get()), int(self.chosen_end_city.get()))
            # print(visited_list)
            # print(path)
            if self.radio_type.get() == 0:
                self.dijkstra_visualisation()
        elif self.radio_var.get() == Algorithms.ASTAR_A.value:
            print("A* was chosen")
            self.algorithm_chosen = Algorithms.ASTAR_A
            a = Astar(self.graph)
            self.distance, self.path, self.states_matrix, self.heuristic = \
                a.a_star_algorithm(int(self.chosen_start_city.get()), int(self.chosen_end_city.get()))
            if self.radio_type.get() == 0:
                self.astar_visualisation()
        elif self.radio_var.get() == Algorithms.RANDOM_A.value:
            print("Random Search was chosen")
            self.algorithm_chosen = Algorithms.RANDOM_A
            r = RandomSearch(self.graph)
            self.distance, self.path, best_iter = r.random_search_algorithm(
                int(self.chosen_start_city.get()), int(self.chosen_end_city.get()), 100 * self.number_of_cities)
            if self.radio_type.get() == 0:
                self.random_search_visualisation()
        if self.radio_type.get() == 0:
            self.path_window = PathWindow(self.root, self.distance, self.path)
        else:
            # self.prev_button.configure(state="normal")
            self.next_button.configure(state="normal")

    def update_map(self):
        self.clear_canvas()
        if self.map_frame is not None:
            self.map_frame.destroy()
        self.map_frame = ctk.CTkFrame(self.main_window, height=self.gui_height - 40, corner_radius=10)
        self.map_frame.grid(row=0, column=0, rowspan=4, padx=(20, 0), pady=(20, 0), sticky="nsew")
        self.figure = plt.Figure(figsize=self.fig_size, dpi=100)
        self.canvas = FigureCanvasTkAgg(self.figure, self.map_frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().grid(row=0, column=0)
        self.draw_graph()
        self.main_window.update()

    def clear_canvas(self):
        for item in self.canvas.get_tk_widget().find_all():
            self.canvas.get_tk_widget().delete(item)

    def draw_graph(self):
        self.nx_graph.add_nodes_from([city for city in range(self.number_of_cities)])
        for i in range(self.number_of_cities):
            for j in range(self.number_of_cities):
                if self.graph.adjmatrix[i][j] == 1:
                    self.nx_graph.add_edge(i, j, weight=self.graph.weighmatrix[i][j])

        a = self.figure.add_subplot(111)
        a.cla()
        # Create positions of all nodes and save them
        pos = nx.circular_layout(self.nx_graph)
        # pos = nx.spring_layout(self.nx_graph, seed=100)
        # print(self.graph.nodeCoords)
        pos = self.create_node_positions(pos)
        # print(pos)

        myKeys = list(pos.keys())
        pos_colors = []
        for key in myKeys:
            pos_colors.append(self.color_map[key])
        weights = nx.get_edge_attributes(self.nx_graph, 'weight')
        # draw nx graph
        if self.algorithm_chosen == Algorithms.ASTAR_A:
            # if the chosen algorithm is astar, draw it so that instead of numbered nodes
            # we have nodes with labels that represent the heuristic value.
            node_labels = {}
            for i in range(len(self.heuristic)):
                node_labels[i] = int(self.heuristic[i])
            nx.draw(self.nx_graph, pos, ax=a, labels=node_labels, node_color=pos_colors, with_labels=True)
        else:
            nx.draw(self.nx_graph, pos, ax=a, node_color=pos_colors, with_labels=True)
        # nx.draw_networkx_nodes(self.nx_graph, pos, ax=a, node_size=500, node_color=pos_colors)
        # Create edge labels
        nx.draw_networkx_edge_labels(self.nx_graph, pos, ax=a, edge_labels=weights)
        if self.algorithm_chosen is None:
            pass
        elif self.algorithm_chosen == Algorithms.DIJKSTRA_A:
            legend_labels = ['Not Visited', 'Visited', 'Shortest Path']
            legend_colors = ['gray', 'green', 'red']
            legend_elements = [plt.Line2D([0], [0], marker='o', color=color, label=label, markersize=10) for
                               color, label in zip(legend_colors, legend_labels)]
            a.legend(handles=legend_elements)
        elif self.algorithm_chosen == Algorithms.ASTAR_A:
            legend_labels = ['Not Visited', 'Open List', 'Closed List', 'Current Node', 'Shortest Path']
            legend_colors = ['gray', 'cyan', 'blue', 'green', 'red']
            legend_elements = [plt.Line2D([0], [0], marker='o', color=color, label=label, markersize=10) for
                               color, label in zip(legend_colors, legend_labels)]
            a.legend(handles=legend_elements)
        elif self.algorithm_chosen == Algorithms.RANDOM_A:
            legend_labels = ['Not Visited', 'Visited', 'Shortest Path']
            legend_colors = ['gray', 'green', 'red']
            legend_elements = [plt.Line2D([0], [0], marker='o', color=color, label=label, markersize=10) for
                               color, label in zip(legend_colors, legend_labels)]
            a.legend(handles=legend_elements)
        a.plot()
        self.canvas.draw()

    def create_node_positions(self, pos):
        myKeys = list(pos.keys())
        # pos_with_cords = []
        for i in myKeys:
            pos[i] = np.array([self.graph.nodeCoords[i][0], self.graph.nodeCoords[i][1]])
        return pos
        # for i in range(self.number_of_cities):
        #     pos[i] = np.array([self.graph.nodeCoords[i][0], self.graph.nodeCoords[i][0]])
        # return pos

    def dijkstra_visualisation_extended(self):
        self.default_cities_coloring()
        i = 0
        for city in self.visited_list:
            self.color_map[city] = 'green'
            if i >= self.state:
                break
            i += 1
        if self.state == len(self.visited_list):
            self.the_end()
        # update gui
        self.update_map()

    def dijkstra_visualisation(self):
        # resetting cities colors
        self.default_cities_coloring()
        # coloring visited cities in dijkstra searching one by one
        for city in self.visited_list:
            self.color_map[city] = 'green'
            self.update_map()
            time.sleep(1)
        # show the shortest path
        if self.path is not None:
            for city in self.path:
                self.color_map[city] = 'red'
        # update gui
        self.update_map()

    def colour_astar(self, current_state):
        for city in range(len(current_state)):
            if current_state[city] == Colours.CURRENT_NODE:
                self.color_map[city] = 'green'
            elif current_state[city] == Colours.IS_OPEN_LIST:
                self.color_map[city] = 'cyan'
            elif current_state[city] == Colours.IS_CLOSED_LIST:
                self.color_map[city] = 'blue'

    def astar_visualisation_extended(self):
        self.default_cities_coloring()
        current_state = self.states_matrix[:, self.state]
        self.colour_astar(current_state)
        if self.state == len(self.states_matrix[1, :]):
            self.the_end()
        self.update_map()

    def the_end(self):
        # show the shortest path
        if self.path is not None:
            for city in self.path:
                self.color_map[city] = 'red'
            self.path_window = PathWindow(self.root, self.distance, self.path)
            self.state = 0
            self.next_button.configure(state="disabled")
            self.prev_button.configure(state="disabled")
        # update gui
        self.update_map()

    def astar_visualisation(self):
        # resetting cities colors
        self.default_cities_coloring()

        # coloring cities in such order that:
        # cyan colour represents the nodes that are potential successors to current node (open list)
        # green colour represents the current node whose neighbouring nodes are being inspected (current note)
        # blue colour represents the nodes who's all neighbours have been inspected (closed list)
        # red colour represents the nodes that belong to the shortest path

        for column in range(len(self.states_matrix[0])):
            current_state = self.states_matrix[:, column]
            self.colour_astar(current_state)
            self.update_map()
            time.sleep(1)

        # show the shortest path
        if self.path is not None:
            for city in self.path:
                self.color_map[city] = 'red'
        # update gui
        self.update_map()

    def random_search_visualisation(self):
        # resetting cities colors
        self.default_cities_coloring()
        # show the shortest path
        if self.path is not None:
            for city in self.path:
                self.color_map[city] = 'red'
        self.update_map()

    @staticmethod
    def exit_from_program():
        sys.exit("Program ended successfully! \nBye :)")
