import tkinter as tk
import customtkinter as ctk
import CustomGraph
from GUI.MainWindow import MainWindow


class StartWindow:
    root: ctk.CTk = None
    start_window: ctk.CTkToplevel = None
    main_window: MainWindow = None
    open_main_button: ctk.CTkButton = None
    title_label: ctk.CTkLabel = None
    project_label: ctk.CTkLabel = None
    gui_width: int = 1100
    gui_height: int = 580
    density: int = 40
    number_of_cities: int = 10

    def __init__(self, root, main_window, graph: CustomGraph):
        self.root = root
        self.main_window = main_window
        self.setUpStartWindow()
        self.addContent()

    def setUpStartWindow(self):
        self.start_window = ctk.CTkToplevel()
        self.start_window.title("AI Project - Travelling from City to City")
        self.start_window.geometry(f"{self.gui_width}x{self.gui_height}")

    def addContent(self):
        # project
        self.project_label = ctk.CTkLabel(self.start_window, text="AI PROJECT",
                                        font=ctk.CTkFont(size=20, weight="bold"))
        self.project_label.pack()
        # title
        self.title_label = ctk.CTkLabel(self.start_window, text="COMPARISON OF ALGORITHMS FOR FINDING THE SHORTEST PATH",
                                        font=ctk.CTkFont(size=30, weight="bold"))
        self.title_label.pack()

        # save and go to the main window
        self.open_main_button = ctk.CTkButton(self.start_window, text="Go to main window",
                                              command=lambda: self.goToMainWindow())
        self.open_main_button.pack()

    def goToMainWindow(self):
        self.start_window.destroy()
        self.main_window.active(self.density, self.number_of_cities)
