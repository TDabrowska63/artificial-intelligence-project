import string
import tkinter as tk
import customtkinter as ctk
import networkx as nx
from matplotlib import pyplot as plt
import time

from CustomGraph import CustomGraph
from Constants import Algorithms, Colours
from Astar import Astar
from Dijkstra import Dijkstra
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg)


class MainWindow:
    root: ctk.CTk = None
    main_window: ctk.CTkToplevel = None
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
    run_button: ctk.CTkButton = None
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
        # self.graph.numberOfNodes = self.number_of_cities
        # self.graph.density = self.density
        self.graph.randomize()
        self.graph.printMe()

    def set_up_main_window(self):
        self.main_window = ctk.CTkToplevel()
        # self.main_window.withdraw()
        self.main_window.title("AI Project - Travelling from City to City")
        self.main_window.geometry(f"{self.gui_width}x{self.gui_height}")
        self.main_window.grid_columnconfigure(0, weight=5)
        self.main_window.grid_columnconfigure(1, weight=1)

    def add_map(self):
        if self.map_frame is not None:
            self.map_frame.destroy()
        self.map_frame = ctk.CTkFrame(self.main_window, height=self.gui_height - 40, corner_radius=10)
        self.map_frame.grid(row=0, column=0, rowspan=4, padx=(20, 0), pady=(20, 0), sticky="nsew")

        self.nx_graph = nx.Graph()
        self.default_cities_coloring()

        self.figure = plt.Figure(figsize=(8, 5), dpi=100)
        self.canvas = FigureCanvasTkAgg(self.figure, self.main_window)
        self.canvas.draw()
        self.canvas.get_tk_widget().grid(row=0, column=0)
        self.draw_graph()

    def default_cities_coloring(self):
        self.color_map.clear()
        for city in range(self.number_of_cities):
            self.color_map.append('grey')

    def add_sidebar(self):
        self.sidebar_frame = ctk.CTkFrame(self.main_window, height=self.gui_height - 40, corner_radius=10)
        self.sidebar_frame.grid(row=0, column=1, padx=(20, 20), pady=(20, 0), sticky="nsew")
        # self.sidebar_frame.grid_propagate(False)
        # self.sidebar_frame.grid_rowconfigure(5, weight=1)

        self.logo_label = ctk.CTkLabel(self.sidebar_frame, text="Shortest Path",
                                       font=ctk.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 5))

        self.density_label = ctk.CTkLabel(self.sidebar_frame, text=f"Density of roads: {self.density}",
                                          font=ctk.CTkFont(size=15))
        self.density_label.grid(row=1, column=0, padx=20, pady=(5, 0))

        for i in range(self.number_of_cities):
            self.cities.append(str(i))

        self.chosen_start_city = tk.StringVar(value="0")
        self.start_label = ctk.CTkLabel(self.sidebar_frame, text="Start City:")
        self.start_label.grid(row=2, column=0, padx=20, pady=(10, 10), sticky="w")
        self.start_option = ctk.CTkOptionMenu(self.sidebar_frame, dynamic_resizing=False,
                                              variable=self.chosen_start_city, values=self.cities)
        self.start_option.grid(row=3, column=0, padx=20, pady=(0, 10))

        self.chosen_end_city = tk.StringVar(value="0")
        self.end_label = ctk.CTkLabel(self.sidebar_frame, text="End City:")
        self.end_label.grid(row=4, column=0, padx=20, pady=(20, 10), sticky="w")
        self.end_option = ctk.CTkOptionMenu(self.sidebar_frame, dynamic_resizing=False,
                                            variable=self.chosen_end_city, values=self.cities)
        self.end_option.grid(row=5, column=0, padx=20, pady=(0, 10))

        self.choose_algorithm_frame = ctk.CTkFrame(self.sidebar_frame)
        self.choose_algorithm_frame.grid(row=6, column=0, padx=(20, 20), pady=(20, 20), sticky="nsew")
        self.radio_var = tk.IntVar(value=0)
        self.label_choose_algorithm = ctk.CTkLabel(master=self.choose_algorithm_frame, text="Searching Algorithm:")
        self.label_choose_algorithm.grid(row=0, column=2, columnspan=1, padx=10, pady=10, sticky="")
        self.dijkstra_button = ctk.CTkRadioButton(master=self.choose_algorithm_frame, text="Dijkstra",
                                                  variable=self.radio_var, value=0)
        self.dijkstra_button.grid(row=1, column=2, pady=10, padx=20, sticky="n")
        # self.bfs_button = ctk.CTkRadioButton(master=self.choose_algorithm_frame, text="BFS", variable=self.radio_var,
        #                                      value=1)
        # self.bfs_button.grid(row=2, column=2, pady=10, padx=20, sticky="n")
        self.astar_button = ctk.CTkRadioButton(master=self.choose_algorithm_frame, text="A*", variable=self.radio_var,
                                               value=1)
        self.astar_button.grid(row=2, column=2, pady=10, padx=20, sticky="n")

        self.run_button = ctk.CTkButton(self.sidebar_frame, text="Calculate Shortest Path", command=self.run_searching)
        self.run_button.grid(row=7, column=0, padx=(20, 20), pady=(20, 20), sticky="nsew")

    def run_searching(self):
        print(f"calculating shortest path... {self.radio_var.get()}")
        if self.radio_var.get() == Algorithms.DIJKSTRA_A.value:
            print("Dijkstra was chosen")
            d = Dijkstra(self.graph)
            distance, path, visited_list = \
                d.dijkstraAlgorithm(int(self.chosen_start_city.get()), int(self.chosen_end_city.get()))
            print(f"start city: {int(self.chosen_start_city.get())}, end city: {int(self.chosen_end_city.get())}")
            print(distance, path, visited_list)
            self.dijkstra_visualisation(distance, path, visited_list)
        elif self.radio_var.get() == Algorithms.ASTAR_A.value:
            print("A* was chosen")
            a = Astar(self.graph)
            # a.printMe()
            path, states_matrix, distance = a.aStarAlgorithm(int(self.chosen_start_city.get()), int(self.chosen_end_city.get()))
            print(f"start city: {int(self.chosen_start_city.get())}, end city: {int(self.chosen_end_city.get())}")
            self.astar_visualisation(path, states_matrix, distance)

    def update_map(self):
        # self.create_map()
        # self.add_map()
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
        # myKeys.sort()
        # sorted_pos = {i: pos[i] for i in myKeys}
        # print(sorted_pos)
        weights = nx.get_edge_attributes(self.nx_graph, 'weight')
        nx.draw(self.nx_graph, pos, ax=a, node_color=pos_colors, with_labels=True)
        # Create edge labels
        nx.draw_networkx_edge_labels(self.nx_graph, pos, ax=a, edge_labels=weights)
        a.plot()
        self.canvas.draw()

    def dijkstra_visualisation(self, distance: int, path, visited_list):
        # resetting cities colors
        self.default_cities_coloring()
        # coloring visited cities in dijkstra searching one by one
        for city in visited_list:
            self.color_map[city] = 'green'
            self.update_map()
            time.sleep(1)
        # show the shortest path
        for city in path:
            self.color_map[city] = 'red'
        # update gui
        self.update_map()

    def astar_visualisation(self, path, states_matrix, distance):
        # show the shortest path
        for city in path:
            self.color_map[city] = 'red'
        # update gui
        self.update_map()
