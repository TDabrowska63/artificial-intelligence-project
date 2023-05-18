from CustomGraph import *
from GUI.MainWindow import MainWindow
from GUI.Gui import Gui
import customtkinter as ctk

g = CustomGraph(10, 30)
g.randomize()
gui = Gui(g)
g.printMe()

