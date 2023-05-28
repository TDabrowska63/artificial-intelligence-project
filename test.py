import matplotlib.pyplot as plt

from Algorithms.Astar import Astar
from Misc.CustomGraph import *

import osmnx as ox
import folium
import networkx as nx
from math import sin, cos, sqrt, atan2, radians



def mouse_event(event):
    print('x: {} and y: {}'.format(event.xdata, event.ydata))


g = CustomGraph(place="Poland, Rumia")
fig, ax = ox.plot_graph(g.mapReference, close=False, show=False)
cid = fig.canvas.mpl_connect('button_press_event', mouse_event)
plt.show()



# a = Astar(g)
# distance, path, states_matrix = a.aStarAlgorithm(0, 12)
# node_id = list(g.mapReference.nodes)
# shortestRoute = []
# for p in path:
#     nid = node_id[p]
#     shortestRoute.append(node_id[p])
#
# ox.plot_graph_route(g.mapReference, shortestRoute)
#g.randomize()
#r = RandomSearch(g)
#distance, path, iteration = r.randomSearch(0, 9, 100000)



