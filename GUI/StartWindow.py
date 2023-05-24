import string
import tkinter as tk
import customtkinter as ctk
import CustomGraph
from GUI.MainWindow import MainWindow


class StartWindow:
    root: ctk.CTk = None
    start_window: ctk.CTkToplevel = None
    main_window: MainWindow = None
    title_label: ctk.CTkLabel = None
    project_label: ctk.CTkLabel = None
    choose_frame: ctk.CTkFrame = None
    cities_num_label: ctk.CTkLabel = None
    cities_num_entry: ctk.CTkEntry = None
    density_label: ctk.CTkLabel = None
    density_entry:  ctk.CTkEntry = None
    open_main_button: ctk.CTkButton = None
    gui_width: int = 1100
    gui_height: int = 580
    density: int = 40
    number_of_cities: int = 10

    def __init__(self, root, main_window):
        self.root = root
        # self.main_window = main_window
        self.set_up_start_window()
        self.add_content()

    def set_up_start_window(self):
        self.start_window = ctk.CTkToplevel()
        self.start_window.title("AI Project - Travelling from City to City")
        self.start_window.geometry(f"{self.gui_width}x{self.gui_height}")

    def add_content(self):
        # project
        self.project_label = ctk.CTkLabel(self.start_window,
                                          text="AI PROJECT", font=ctk.CTkFont(size=20, weight="bold"))
        self.project_label.pack(pady=(40, 20))
        # title
        self.title_label = ctk.CTkLabel(self.start_window,
                                        text="Comparison Of Algorithms For Finding The Shortest Path",
                                        font=ctk.CTkFont(size=30, weight="bold"))
        self.title_label.pack(pady=20)

        # choose parameters of the map
        self.choose_frame = ctk.CTkFrame(self.start_window, width=self.gui_width-80, corner_radius=10)
        self.choose_frame.pack(pady=(10, 10))
        self.choose_frame.pack_propagate(False)

        # number of cities
        self.cities_num_label = ctk.CTkLabel(self.choose_frame, text="Type number of cities to be on the map:",
                                             font=ctk.CTkFont(size=15))
        self.cities_num_label.pack(padx=80, pady=(20, 5))
        self.cities_num_entry = ctk.CTkEntry(self.choose_frame, placeholder_text="10")
        self.cities_num_entry.pack(padx=80, pady=(5, 10))
        self.cities_num_entry.focus()

        # density
        self.density_label = ctk.CTkLabel(self.choose_frame, text="Type density of roads as percentage from 0 to 100:",
                                          font=ctk.CTkFont(size=15))
        self.density_label.pack(padx=80, pady=(10, 5))
        self.density_entry = ctk.CTkEntry(self.choose_frame, placeholder_text="40")
        self.density_entry.pack(padx=80, pady=(5, 5))
        self.density_entry.focus()

        # save and go to the main window
        self.open_main_button = ctk.CTkButton(self.start_window, text="Save and Proceed",
                                              font=ctk.CTkFont(size=15),
                                              command=lambda: self.go_to_main_window(self.density_entry.get(),
                                                                                     self.cities_num_entry.get()))
        self.open_main_button.pack(pady=20)

    def go_to_main_window(self, density, number_of_cities):
        self.start_window.destroy()
        try:
            self.main_window = MainWindow(self.root, int(density), int(number_of_cities))
        except ValueError:
            den = self.density if density == '' else density
            num = self.number_of_cities if number_of_cities == '' else number_of_cities
            self.main_window = MainWindow(self.root, int(den), int(num))
