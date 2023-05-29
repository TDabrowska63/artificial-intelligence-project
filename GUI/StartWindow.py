import customtkinter as ctk
from GUI.MainWindow import MainWindow
from GUI.OxCityWindow import OxCityWindow


class StartWindow:
    root: ctk.CTk = None
    start_window: ctk.CTkToplevel = None
    main_window: MainWindow = None
    ox_city_window: OxCityWindow = None
    title_frame: ctk.CTkFrame = None
    city_frame: ctk.CTkFrame = None
    graph_frame: ctk.CTkFrame = None
    title_label: ctk.CTkLabel = None
    project_label: ctk.CTkLabel = None
    # graph imitating cities
    graph_title_label: ctk.CTkLabel = None
    cities_num_label: ctk.CTkLabel = None
    cities_num_entry: ctk.CTkEntry = None
    density_label: ctk.CTkLabel = None
    density_entry: ctk.CTkEntry = None
    open_main_button: ctk.CTkButton = None
    # show real city as graph
    city_title_label: ctk.CTkLabel = None
    country_name_label: ctk.CTkLabel = None
    country_name_entry: ctk.CTkEntry = None
    city_name_label: ctk.CTkLabel = None
    city_name_entry: ctk.CTkEntry = None
    open_city_map_button: ctk.CTkButton = None

    gui_width: int = 1100
    gui_height: int = 580
    density: int = 30
    number_of_cities: int = 10

    def __init__(self, root):
        self.root = root
        self.set_up_start_window()
        self.set_up_frames()
        self.add_graph_frame()
        self.add_city_frame()

    def set_up_start_window(self):
        self.start_window = ctk.CTkToplevel()
        self.start_window.title("AI Project - Travelling from City to City")
        self.start_window.geometry(f"{self.gui_width}x{self.gui_height}")
        self.start_window.grid_rowconfigure(0, weight=1)
        self.start_window.grid_rowconfigure(1, weight=4)

    def set_up_frames(self):
        self.title_frame = ctk.CTkFrame(self.start_window, width=self.gui_width - 40, corner_radius=10)
        self.title_frame.grid(row=0, column=0, columnspan=2, padx=(20, 20), pady=(10, 0), sticky="nsew")

        self.city_frame = ctk.CTkFrame(self.start_window, width=int(self.gui_width / 2) - 30, corner_radius=10)
        self.city_frame.grid(row=1, column=0, columnspan=1, padx=(20, 20), pady=(20, 20), sticky="nsew")

        self.graph_frame = ctk.CTkFrame(self.start_window, width=int(self.gui_width / 2) - 30, corner_radius=10)
        self.graph_frame.grid(row=1, column=1, columnspan=1, padx=(20, 20), pady=(20, 20), sticky="nsew")

        # project
        self.project_label = ctk.CTkLabel(self.title_frame, bg_color='#147',
                                          text="AI PROJECT", font=ctk.CTkFont(size=20, weight="bold"))
        self.project_label.grid(row=0, column=0, pady=(20, 20), sticky="nsew")
        # title
        self.title_label = ctk.CTkLabel(self.title_frame,
                                        text="Comparison Of Algorithms For Finding The Shortest Path",
                                        font=ctk.CTkFont(size=30, weight="bold"))
        self.title_label.grid(row=1, column=0, padx=120, pady=(20, 20), sticky="nsew")

    def add_city_frame(self):
        self.city_title_label = ctk.CTkLabel(self.city_frame, bg_color='#147',
                                             text=" Show searching algorithms working \n on real cities as graphs ",
                                             font=ctk.CTkFont(size=20, weight="bold"))
        self.city_title_label.grid(row=0, column=0, padx=70, pady=(20, 5))

        # number of cities
        self.country_name_label = ctk.CTkLabel(self.city_frame, text="Type name of the country:",
                                               font=ctk.CTkFont(size=15))
        self.country_name_label.grid(row=1, column=0, padx=80, pady=(20, 5))
        self.country_name_entry = ctk.CTkEntry(self.city_frame, placeholder_text="Poland")
        self.country_name_entry.grid(row=2, column=0, padx=80, pady=(5, 10))
        self.country_name_entry.focus()

        # density
        self.city_name_label = ctk.CTkLabel(self.city_frame, text="Type name of city:",
                                            font=ctk.CTkFont(size=15))
        self.city_name_label.grid(row=3, column=0, padx=80, pady=(10, 5))
        self.city_name_entry = ctk.CTkEntry(self.city_frame, placeholder_text="Sopot")
        self.city_name_entry.grid(row=4, column=0, padx=80, pady=(5, 5))
        self.city_name_entry.focus()

        # save and go to the main window
        self.open_city_map_button = ctk.CTkButton(self.city_frame, text="Save and Proceed",
                                                  font=ctk.CTkFont(size=15),
                                                  command=lambda: self.go_to_city_map(self.country_name_entry.get(),
                                                                                      self.city_name_entry.get()))
        self.open_city_map_button.grid(row=5, column=0, pady=20)

    def add_graph_frame(self):
        self.graph_title_label = ctk.CTkLabel(self.graph_frame, bg_color='#147',
                                              text=" Show searching algorithms working \n on nodes imitating cities ",
                                              font=ctk.CTkFont(size=20, weight="bold"))
        self.graph_title_label.grid(row=0, column=0, padx=70, pady=(20, 5))

        # number of cities
        self.cities_num_label = ctk.CTkLabel(self.graph_frame, text="Type number of cities to be on the map:",
                                             font=ctk.CTkFont(size=15))
        self.cities_num_label.grid(row=1, column=0, padx=80, pady=(20, 5))
        self.cities_num_entry = ctk.CTkEntry(self.graph_frame, placeholder_text="10")
        self.cities_num_entry.grid(row=2, column=0, padx=80, pady=(5, 10))
        self.cities_num_entry.focus()

        # density
        self.density_label = ctk.CTkLabel(self.graph_frame, text="Type density of roads as percentage from 0 to 100:",
                                          font=ctk.CTkFont(size=15))
        self.density_label.grid(row=3, column=0, padx=80, pady=(10, 5))
        self.density_entry = ctk.CTkEntry(self.graph_frame, placeholder_text="30")
        self.density_entry.grid(row=4, column=0, padx=80, pady=(5, 5))
        self.density_entry.focus()

        # save and go to the main window
        self.open_main_button = ctk.CTkButton(self.graph_frame, text="Save and Proceed",
                                              font=ctk.CTkFont(size=15),
                                              command=lambda: self.go_to_main_window(self.density_entry.get(),
                                                                                     self.cities_num_entry.get()))
        self.open_main_button.grid(row=5, column=0, pady=20)

    def go_to_city_map(self, country_name, city_name):
        self.start_window.destroy()
        if country_name == "":
            country_name = "Poland"
        if city_name == "":
            city_name = "Sopot"
        print(f"show map with country: {country_name} and city: {city_name}")
        self.ox_city_window = OxCityWindow(self.root, country_name, city_name)

    def go_to_main_window(self, density, number_of_cities):
        self.start_window.destroy()
        try:
            self.main_window = MainWindow(self.root, int(density), int(number_of_cities))
        except ValueError:
            den = self.density if density == '' else density
            num = self.number_of_cities if number_of_cities == '' else number_of_cities
            self.main_window = MainWindow(self.root, int(den), int(num))
