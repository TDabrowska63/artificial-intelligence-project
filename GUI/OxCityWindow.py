import string
import tkinter as tk
import customtkinter as ctk
import networkx as nx
import time
import sys

from matplotlib import pyplot as plt
from GUI.PathWindow import PathWindow
# from test import Test
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

    # city: Test = None
    graph: CustomGraph = None
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
        print("")
        # Create graph and CityMap objects

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
