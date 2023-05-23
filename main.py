from CustomGraph import *
from GUI.Gui import Gui
from Astar import *
from Dijkstra import *
from Constants import *

g = CustomGraph(10, 99)
g.randomize()
print(Colours.NOT_VISITED.value)
print(Algorithms.DIJKSTRA_A.value)
g.printMe()
gui = Gui()


