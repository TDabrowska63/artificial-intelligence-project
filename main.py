from CustomGraph import *
from GUI import GUI

g = CustomGraph(10, 30)
g.randomize()
gui = GUI(g)
g.printMe()

