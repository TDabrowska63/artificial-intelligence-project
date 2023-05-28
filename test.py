import matplotlib.pyplot as plt

from Algorithms.Astar import Astar
from Misc.CustomGraph import *

import osmnx as ox


class Test:
    def __init__(self, g):
        self.node1 = None
        self.node2 = None
        self.g = g
        self.shortestRoute = []

    def mouse_event(self, event):
        nid = ox.nearest_nodes(self.g.mapReference, event.xdata, event.ydata)
        node_id = list(self.g.mapReference.nodes)
        print('x: {} and y: {}'.format(event.xdata, event.ydata))
        for i in range(len(node_id)):
            if node_id[i] == nid:
                if self.node1 is None:
                    self.node1 = i
                elif self.node2 is None:
                    self.node2 = i
                break

        if self.node1 is not None and self.node2 is not None:
            a = Astar(self.g)
            distance, path, states_matrix = a.aStarAlgorithm(self.node1, self.node2)
            node_id = list(self.g.mapReference.nodes)
            for p in path:
                self.shortestRoute.append(node_id[p])

    def getShortestRoute(self):
        return self.shortestRoute




g = CustomGraph(place="Santa Monica, California")
t = Test(g)
fig, ax = ox.plot_graph(g.mapReference, close=False, show=False)
cid = fig.canvas.mpl_connect('button_press_event', t.mouse_event)
plt.show()
ox.plot_graph_route(g.mapReference, t.shortestRoute)


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



