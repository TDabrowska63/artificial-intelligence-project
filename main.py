from CustomGraph import *
from GUI.Gui import Gui
from Astar import *
from Dijkstra import *

g = CustomGraph(10, 99)
g.randomize()
g.printMe()
gui = Gui()
a = Astar(g)
a.printMe()
path = a.aStarAlgorithm(0, 9)
d = Dijkstra(g)
print(d.dijkstraAlgorithm(0, 9))


