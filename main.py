from CustomGraph import *
from GUI.MainWindow import MainWindow
from GUI.Gui import Gui
import customtkinter as ctk
from Astar import *

g = CustomGraph(10, 30)
g.randomize()
g.printMe()
a = Astar(g)
a.printMe()
path = a.aStarAlgorithm(0, 9)
gui = Gui(g)
