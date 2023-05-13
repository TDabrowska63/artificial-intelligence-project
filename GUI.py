import tkinter as tk
import customtkinter as ctk
import CustomGraph


class GUI:
    def __init__(self, graph: CustomGraph):
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")
        self.gui_width = 1100
        self.gui_height = 580
        self.root = ctk.CTk()
        # configure window
        self.root.title("AI Project - Travelling from City to City")
        self.root.geometry(f"{self.gui_width}x{self.gui_height}")

        self.root.grid_columnconfigure(0, weight=5)
        self.root.grid_columnconfigure(1, weight=1)

        self.map_frame = ctk.CTkFrame(self.root, height=self.gui_height-40, corner_radius=10)
        self.map_frame.grid(row=0, column=0, rowspan=4, padx=(20, 0), pady=(20, 0), sticky="nsew")
        graph.drawGraph(self.root)

        self.sidebar_frame = ctk.CTkFrame(self.root, height=self.gui_height-40, corner_radius=10)
        self.sidebar_frame.grid(row=0, column=1, padx=(20, 20), pady=(20, 0), sticky="nsew")
        # self.sidebar_frame.grid_rowconfigure(5, weight=1)

        self.logo_label = ctk.CTkLabel(self.sidebar_frame, text="Shortest Way", font=ctk.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        self.cities = []
        for i in range(graph.numberOfNodes):
            self.cities.append("City " + str(i))

        self.start_label = ctk.CTkLabel(self.sidebar_frame, text="Start City:")
        self.start_label.grid(row=1, column=0, padx=20, pady=(20, 10), sticky="w")
        self.start_option = ctk.CTkOptionMenu(self.sidebar_frame, dynamic_resizing=False, values=self.cities)
        self.start_option.grid(row=2, column=0, padx=20, pady=(0, 10))

        self.end_label = ctk.CTkLabel(self.sidebar_frame, text="End City:")
        self.end_label.grid(row=3, column=0, padx=20, pady=(20, 10), sticky="w")
        self.end_option = ctk.CTkOptionMenu(self.sidebar_frame, dynamic_resizing=False, values=self.cities)
        self.end_option.grid(row=4, column=0, padx=20, pady=(0, 10))

        self.choose_algorithm_frame = ctk.CTkFrame(self.sidebar_frame)
        self.choose_algorithm_frame.grid(row=5, column=0, padx=(20, 20), pady=(20, 20), sticky="nsew")
        self.radio_var = tk.IntVar(value=0)
        self.label_choose_algorithm = ctk.CTkLabel(master=self.choose_algorithm_frame, text="Searching Algorithm:")
        self.label_choose_algorithm.grid(row=0, column=2, columnspan=1, padx=10, pady=10, sticky="")
        self.dijkstra_button = ctk.CTkRadioButton(master=self.choose_algorithm_frame, text="Dijkstra", variable=self.radio_var, value=0)
        self.dijkstra_button.grid(row=1, column=2, pady=10, padx=20, sticky="n")
        self.bfs_button = ctk.CTkRadioButton(master=self.choose_algorithm_frame, text="BFS", variable=self.radio_var, value=1)
        self.bfs_button.grid(row=2, column=2, pady=10, padx=20, sticky="n")
        self.astar_button = ctk.CTkRadioButton(master=self.choose_algorithm_frame, text="A*", variable=self.radio_var, value=2)
        self.astar_button.grid(row=3, column=2, pady=10, padx=20, sticky="n")

        self.run_button = ctk.CTkButton(self.sidebar_frame, text="Calculate Shortest Path", command=self.runEvent)
        self.run_button.grid(row=6, column=0, padx=(20, 20), pady=(20, 20), sticky="nsew")

        self.root.mainloop()


    def runEvent(self):
        print("calculating shortest path...")


