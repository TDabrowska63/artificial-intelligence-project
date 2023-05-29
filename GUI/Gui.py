import customtkinter as ctk
from GUI.StartWindow import StartWindow

# set modes
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class Gui:

    window: ctk.CTk = None
    start_window: StartWindow = None

    def __init__(self):
        self.window = ctk.CTk()
        self.show_app()

    def show_app(self):
        self.window.withdraw()
        self.start_window = StartWindow(self.window)
        self.window.mainloop()
