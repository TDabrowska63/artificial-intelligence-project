from CustomGraph import *
from GUI import GUI

g = CustomGraph(10)
g.randomize()
gui = GUI(g)
g.printMe()

