import string
import tkinter as tk
import customtkinter as ctk
import networkx as nx
import time
import sys

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
    bfs_button: ctk.CTkRadioButton = None
    astar_button: ctk.CTkRadioButton = None
    random_search_button: ctk.CTkRadioButton = None
    run_button: ctk.CTkButton = None
    exit_button: ctk.CTkButton = None
    cities: string = []
    gui_width: int = 1100
    gui_height: int = 580
    density: int = 90
    number_of_cities: int = 20
    graph: CustomGraph = None
    figure: plt.Figure = None
    canvas: FigureCanvasTkAgg = None
    nx_graph: nx.Graph = None
    color_map: string = []
    algorithm_chosen: Algorithms = None

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
        self.graph.printMe()

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
        self.figure = plt.Figure(figsize=(8, 5), dpi=100)
        self.canvas = FigureCanvasTkAgg(self.figure, self.main_window)
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
        self.choose_algorithm_frame.grid(row=6, column=0, padx=20, pady=20, sticky="nsew")
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

    def show_buttons(self):
        self.run_button = ctk.CTkButton(self.sidebar_frame, text="Calculate Shortest Path", command=self.run_searching)
        self.run_button.grid(row=7, column=0, padx=(20, 20), pady=(20, 10), sticky="nsew")

        self.exit_button = ctk.CTkButton(self.sidebar_frame, text="Exit", command=self.exit_from_program)
        self.exit_button.grid(row=8, column=0, padx=(20, 20), pady=(5, 20), sticky="nsew")

    def run_searching(self):
        print(f"calculating shortest path... {self.radio_var.get()}")
        print(f"start city: {int(self.chosen_start_city.get())}, end city: {int(self.chosen_end_city.get())}")
        distance = 0
        path = []
        if self.radio_var.get() == Algorithms.DIJKSTRA_A.value:
            print("Dijkstra was chosen")
            self.algorithm_chosen = Algorithms.DIJKSTRA_A
            d = Dijkstra(self.graph)
            distance, path, visited_list = \
                d.dijkstra_algorithm(int(self.chosen_start_city.get()), int(self.chosen_end_city.get()))
            self.dijkstra_visualisation(path, visited_list)
        elif self.radio_var.get() == Algorithms.ASTAR_A.value:
            print("A* was chosen")
            self.algorithm_chosen = Algorithms.ASTAR_A
            a = Astar(self.graph)
            distance, path, states_matrix = \
                a.a_star_algorithm(int(self.chosen_start_city.get()), int(self.chosen_end_city.get()))
            self.astar_visualisation(path, states_matrix)
        elif self.radio_var.get() == Algorithms.RANDOM_A.value:
            print("Random Search was chosen")
            self.algorithm_chosen = Algorithms.RANDOM_A
            r = RandomSearch(self.graph)
            distance, path, best_iter = r.random_search_algorithm(
                int(self.chosen_start_city.get()), int(self.chosen_end_city.get()), 100*self.number_of_cities)
            self.random_search_visualisation(path)
        self.path_window = PathWindow(self.root, distance, path)

    def update_map(self):
        self.clear_canvas()
        if self.map_frame is not None:
            self.map_frame.destroy()
        self.map_frame = ctk.CTkFrame(self.main_window, height=self.gui_height - 40, corner_radius=10)
        self.map_frame.grid(row=0, column=0, rowspan=4, padx=(20, 0), pady=(20, 0), sticky="nsew")
        self.figure = plt.Figure(figsize=(8, 5), dpi=100)
        self.canvas = FigureCanvasTkAgg(self.figure, self.main_window)
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
        pos = nx.spring_layout(self.nx_graph, seed=100)
        myKeys = list(pos.keys())
        pos_colors = []
        for key in myKeys:
            pos_colors.append(self.color_map[key])
        weights = nx.get_edge_attributes(self.nx_graph, 'weight')
        # draw nx graph
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

    def dijkstra_visualisation(self, path, visited_list):
        # resetting cities colors
        self.default_cities_coloring()
        # coloring visited cities in dijkstra searching one by one
        for city in visited_list:
            self.color_map[city] = 'green'
            self.update_map()
            time.sleep(1)
        # show the shortest path
        if path is not None:
            for city in path:
                self.color_map[city] = 'red'
        # update gui
        self.update_map()

    def astar_visualisation(self, path, states_matrix):
        # resetting cities colors
        self.default_cities_coloring()

        # coloring cities in such order that:
        # cyan colour represents the nodes that are potential successors to current node (open list)
        # green colour represents the current node whose neighbouring nodes are being inspected (current note)
        # blue colour represents the nodes who's all neighbours have been inspected (closed list)
        # red colour represents the nodes that belong to the shortest path

        for column in range(len(states_matrix[0])):
            current_state = states_matrix[:, column]
            for city in range(len(current_state)):
                if current_state[city] == Colours.CURRENT_NODE:
                    self.color_map[city] = 'green'
                elif current_state[city] == Colours.IS_OPEN_LIST:
                    self.color_map[city] = 'cyan'
                elif current_state[city] == Colours.IS_CLOSED_LIST:
                    self.color_map[city] = 'blue'
            self.update_map()
            time.sleep(1)

        # show the shortest path
        if path is not None:
            for city in path:
                self.color_map[city] = 'red'
        # update gui
        self.update_map()

    def random_search_visualisation(self, path):
        # resetting cities colors
        self.default_cities_coloring()
        # show the shortest path
        if path is not None:
            for city in path:
                self.color_map[city] = 'red'
        self.update_map()

    @staticmethod
    def exit_from_program():
        sys.exit("Program ended successfully! \nBye :)")
