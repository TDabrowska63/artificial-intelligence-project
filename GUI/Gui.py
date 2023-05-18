import customtkinter as ctk
from GUI.MainWindow import MainWindow
from GUI.StartWindow import StartWindow
import CustomGraph

# set modes
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class Gui:
    window: ctk.CTk = None
    start_window: StartWindow = None
    main_window: MainWindow = None

    def __init__(self, graph: CustomGraph):
        self.window = ctk.CTk()
        self.show_app(graph)

    def show_app(self, graph: CustomGraph):
        self.window.withdraw()
        self.main_window = MainWindow(self.window, graph)
        self.start_window = StartWindow(self.window, self.main_window, graph)
        self.window.mainloop()
