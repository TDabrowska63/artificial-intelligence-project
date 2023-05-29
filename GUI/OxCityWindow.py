import string
import tkinter as tk
import customtkinter as ctk
import osmnx as ox
import networkx as nx
import time
import sys

from matplotlib import pyplot as plt
from GUI.PathWindow import PathWindow
from CityMap import CityMap
from Misc.CustomGraph import CustomGraph
from Misc.Constants import Algorithms, Colours
from Algorithms.Astar import Astar
from Algorithms.Dijkstra import Dijkstra
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg)


class OxCityWindow:
    root: ctk.CTk = None
    ox_city_window: ctk.CTkToplevel = None
    path_window: PathWindow = None
    map_frame: ctk.CTkFrame = None

    sidebar_frame: ctk.CTkFrame = None
    logo_label: ctk.CTkLabel = None
    first_step_label: ctk.CTkLabel = None
    choose_algorithm_frame: ctk.CTkFrame = None
    radio_var: tk.IntVar = None
    label_choose_algorithm: ctk.CTkLabel = None
    dijkstra_button: ctk.CTkRadioButton = None
    bfs_button: ctk.CTkRadioButton = None
    astar_button: ctk.CTkRadioButton = None
    random_search_button: ctk.CTkRadioButton = None
    second_step_label: ctk.CTkLabel = None
    to_clickable_button: ctk.CTkButton = None
    how_to_label: ctk.CTkLabel = None
    run_button: ctk.CTkButton = None
    exit_button: ctk.CTkButton = None

    city: CityMap = None
    graph: CustomGraph = None
    figure: plt.Figure = None
    ax: plt.Axes = None
    canvas: FigureCanvasTkAgg = None
    cid = None
    country_name: string = None
    city_name: string = None
    gui_width: int = 1100
    gui_height: int = 580

    def __init__(self, root, country_name: string, city_name: string):
        self.root = root
        self.country_name = country_name
        self.city_name = city_name
        self.create_map()
        self.set_up_main_window()
        self.add_map()
        self.add_sidebar()

    def create_map(self):
        # Create graph and CityMap objects
        self.graph = CustomGraph(place=f"{self.country_name}, {self.city_name}")
        self.city = CityMap(self.graph)

    def set_up_main_window(self):
        self.ox_city_window = ctk.CTkToplevel()
        self.ox_city_window.title("AI Project - Travelling from City to City")
        self.ox_city_window.geometry(f"{self.gui_width}x{self.gui_height}")
        self.ox_city_window.grid_columnconfigure(0, weight=5)
        self.ox_city_window.grid_columnconfigure(1, weight=1)

    def add_map(self):
        if self.map_frame is not None:
            self.map_frame.destroy()
        self.map_frame = ctk.CTkFrame(self.ox_city_window, height=self.gui_height - 40, corner_radius=10)
        self.map_frame.grid(row=0, column=0, rowspan=4, padx=(20, 0), pady=(20, 0), sticky="nsew")
        self.figure, self.ax = ox.plot_graph(self.graph.mapReference, figsize=(9, 7), close=False, show=False, dpi=100)
        self.canvas = FigureCanvasTkAgg(self.figure, self.map_frame)
        self.cid = self.canvas.mpl_connect('button_press_event', self.city.do_nothing_event)
        self.canvas.draw()
        self.canvas.get_tk_widget().grid(row=0, column=0)
        self.ax.plot()
        self.canvas.draw()
        self.ox_city_window.update()

    def make_map_clickable(self):
        self.city.algorithm = self.radio_var.get()
        self.canvas.mpl_disconnect(self.cid)
        self.cid = self.canvas.mpl_connect('button_press_event', self.city.mouse_event)
        self.canvas.draw()

    def update_window(self):
        if self.map_frame is not None:
            self.map_frame.destroy()
        self.map_frame = ctk.CTkFrame(self.ox_city_window, height=self.gui_height - 40, corner_radius=10)
        self.map_frame.grid(row=0, column=0, rowspan=4, padx=(20, 0), pady=(20, 0), sticky="nsew")
        self.canvas = FigureCanvasTkAgg(self.figure, self.map_frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().grid(row=0, column=0)
        self.ax.plot()
        self.canvas.draw()
        self.ox_city_window.update()

    def add_sidebar(self):
        # creating sidebar
        self.sidebar_frame = ctk.CTkFrame(self.ox_city_window, height=self.gui_height - 40, corner_radius=10)
        self.sidebar_frame.grid(row=0, column=1, padx=(20, 20), pady=(20, 0), sticky="nsew")
        # logo/title label
        self.logo_label = ctk.CTkLabel(self.sidebar_frame, text="Shortest Path",
                                       font=ctk.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 5))
        self.first_step_label = ctk.CTkLabel(self.sidebar_frame, bg_color='#147', text=" FIRST STEP ",
                                             font=ctk.CTkFont(size=15))
        self.first_step_label.grid(row=1, column=0, padx=20, pady=(5, 0), sticky="nw")
        self.show_algorithms_to_choose()
        self.second_step_label = ctk.CTkLabel(self.sidebar_frame, bg_color='#147', text=" SECOND STEP ",
                                              font=ctk.CTkFont(size=15))
        self.second_step_label.grid(row=3, column=0, padx=20, pady=(5, 0), sticky="nw")
        self.to_clickable_button = ctk.CTkButton(self.sidebar_frame, text="Make Map Clickable",
                                                 command=self.make_map_clickable)
        self.to_clickable_button.grid(row=4, column=0, padx=(20, 20), pady=(20, 10), sticky="nsew")
        self.how_to_label = ctk.CTkLabel(master=self.sidebar_frame,
                                         text="Choose intersections on\nthe map by clicking on it")
        self.how_to_label.grid(row=5, column=0, padx=20, pady=10, sticky="nw")
        self.show_buttons()

    def show_algorithms_to_choose(self):
        self.choose_algorithm_frame = ctk.CTkFrame(self.sidebar_frame)
        self.choose_algorithm_frame.grid(row=2, column=0, padx=(20, 20), pady=(20, 20), sticky="nsew")
        self.radio_var = tk.IntVar(value=0)
        self.label_choose_algorithm = ctk.CTkLabel(master=self.choose_algorithm_frame, text="Searching Algorithm:")
        self.label_choose_algorithm.grid(row=0, column=2, columnspan=1, padx=10, pady=10, sticky="")
        self.dijkstra_button = ctk.CTkRadioButton(master=self.choose_algorithm_frame, text="Dijkstra",
                                                  variable=self.radio_var, value=0)
        self.dijkstra_button.grid(row=1, column=2, pady=10, padx=10, sticky="nw")
        self.astar_button = ctk.CTkRadioButton(master=self.choose_algorithm_frame, text="A*", variable=self.radio_var,
                                               value=1)
        self.astar_button.grid(row=2, column=2, pady=10, padx=10, sticky="nw")

    def show_buttons(self):
        self.run_button = ctk.CTkButton(self.sidebar_frame, text="Calculate Shortest Path", command=self.run_searching)
        self.run_button.grid(row=6, column=0, padx=(20, 20), pady=(20, 10), sticky="nsew")

        self.exit_button = ctk.CTkButton(self.sidebar_frame, text="Exit", command=self.exit_from_program)
        self.exit_button.grid(row=7, column=0, padx=(20, 20), pady=(5, 20), sticky="nsew")

    def run_searching(self):
        print("searching")
        plt.close(self.figure)
        self.canvas.mpl_disconnect(self.cid)
        self.figure, self.ax = ox.plot_graph_route(self.graph.mapReference, self.city.shortestRoute, ax=self.ax)
        self.update_window()
        self.path_window = PathWindow(self.root, self.city.distance, self.city.path)

    @staticmethod
    def exit_from_program():
        sys.exit("Program ended successfully! \nBye :)")
