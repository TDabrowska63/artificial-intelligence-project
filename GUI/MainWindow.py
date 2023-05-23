import string
import tkinter as tk
import customtkinter as ctk
from CustomGraph import CustomGraph
from Constants import Algorithms, Colours
from Astar import Astar
from Dijkstra import Dijkstra


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
        self.graph.drawGraph(self.main_window)

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
        elif self.radio_var.get() == Algorithms.ASTAR_A.value:
            print("A* was chosen")
            a = Astar(self.graph)
            # a.printMe()
            path = a.aStarAlgorithm(int(self.chosen_start_city.get()), int(self.chosen_end_city.get()))

    def active(self, density: int, number_of_cities: int):
        self.density = density
        self.number_of_cities = number_of_cities
        self.create_map()
        self.add_map()
        # self.add_sidebar()
        # self.graph.printMe()
        self.main_window.deiconify()
