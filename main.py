from CustomGraph import *
from GUI.MainWindow import MainWindow
from GUI.Gui import Gui
import customtkinter as ctk
from Astar import *
import matplotlib

g = CustomGraph(10, 99)
g.randomize()
g.printMe()
gui = Gui()
a = Astar(g)
a.printMe()
path = a.aStarAlgorithm(0, 9)
