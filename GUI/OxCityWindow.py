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

    city: CityMap = None
    graph: CustomGraph = None
    figure: plt.Figure = None
    ax: plt.Axes = None
    canvas: FigureCanvasTkAgg = None
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

        # add figure, canvas and call plotting methods
        self.figure, self.ax = ox.plot_graph(self.graph.mapReference, close=False, show=False, block=False)
        self.canvas = FigureCanvasTkAgg(self.figure, self.ox_city_window)
        cid = self.canvas.mpl_connect('button_press_event', self.city.mouse_event)
        self.canvas.draw()
        self.canvas.get_tk_widget().grid(row=0, column=0)

        plt.show()
        self.canvas.draw()
        self.canvas.mpl_disconnect(cid)
        ox.plot_graph_route(self.graph.mapReference, self.city.shortestRoute)
        self.canvas.draw()

    def add_sidebar(self):
        # creating sidebar
        self.sidebar_frame = ctk.CTkFrame(self.ox_city_window, height=self.gui_height - 40, corner_radius=10)
        self.sidebar_frame.grid(row=0, column=1, padx=(20, 20), pady=(20, 0), sticky="nsew")
        # logo/title label
        self.logo_label = ctk.CTkLabel(self.sidebar_frame, text="Shortest Path",
                                       font=ctk.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 5))


