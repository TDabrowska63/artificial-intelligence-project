import matplotlib.pyplot as plt

from Algorithms.Astar import Astar
from Misc.CustomGraph import *

import osmnx as ox
import threading
import time

class CityMap:
    def __init__(self, graph):
        self.node1 = None
        self.node2 = None
        self.graph = graph
        self.shortestRoute = []

    def mouse_event(self, event):
        nid = ox.nearest_nodes(self.graph.mapReference, event.xdata, event.ydata)
        node_id = list(self.graph.mapReference.nodes)
        print('x: {} and y: {}'.format(event.xdata, event.ydata))

        for i in range(len(node_id)):
            if node_id[i] == nid:
                if self.node1 is None:
                    self.node1 = i
                elif self.node2 is None:
                    self.node2 = i
                break

        if self.node1 is not None and self.node2 is not None:
            a = Astar(self.graph)
            distance, path, states_matrix = a.aStarAlgorithm(self.node1, self.node2)
            node_id = list(self.graph.mapReference.nodes)
            for p in path:
                self.shortestRoute.append(node_id[p])
            self.node1 = None
            self.node2 = None

    def getShortestRoute(self):
        return self.shortestRoute

#exemplary usage:

g = CustomGraph(place="Poland, Rumia")
t = CityMap(g)
fig, ax = ox.plot_graph(g.mapReference, close=False, show=False)
cid = fig.canvas.mpl_connect('button_press_event', t.mouse_event)
plt.show()
fig.canvas.mpl_disconnect(cid)
ox.plot_graph_route(g.mapReference, t.shortestRoute)
