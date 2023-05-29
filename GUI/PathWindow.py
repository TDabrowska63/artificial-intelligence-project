import customtkinter as ctk


class PathWindow:

    root: ctk.CTk = None
    path_window: ctk.CTkToplevel = None
    path_label: ctk.CTkLabel = None
    dist_label: ctk.CTkLabel = None
    via_label: ctk.CTkLabel = None
    gui_width: int = 290
    gui_height: int = 125
    path = []

    def __init__(self, root: ctk.CTk, distance: int, path):
        self.root = root
        self.path = path
        self.set_up_start_window()
        self.add_content(distance)

    def set_up_start_window(self):
        self.path_window = ctk.CTkToplevel()
        self.path_window.title("Found Shortest Path")
        if self.path_length >= 6:
            self.gui_width += (self.path_length - 6)*10
        self.path_window.geometry(f"{self.gui_width}x{self.gui_height}")

    def add_content(self, distance: int):
        self.path_label = ctk.CTkLabel(self.path_window,
                                       text=" SHORTEST PATH ", bg_color='#147', font=ctk.CTkFont(size=20, weight="bold"))
        self.path_label.pack(pady=(10, 5))

        if distance is not None:
            self.dist_label = ctk.CTkLabel(self.path_window,
                                           text=f"Distance: {round(distance, 2)}km", font=ctk.CTkFont(size=18))
            self.dist_label.pack(pady=(5, 5))
            self.via_label = ctk.CTkLabel(self.path_window,
                                          text=f"Path via: {self.path}", font=ctk.CTkFont(size=18))
            self.via_label.pack(pady=(5, 10))
        else:
            self.dist_label = ctk.CTkLabel(self.path_window,
                                           text="There is no path \nbetween chosen cities :(", font=ctk.CTkFont(size=18))
            self.dist_label.pack(pady=(5, 5))

    @property
    def path_length(self):
        return len(self.path)
