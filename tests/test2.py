import matplotlib.pyplot as plt

from Algorithms.Astar import Astar
from Misc.CustomGraph import *

import osmnx as ox
import threading
import time

global_lock = threading.Lock()
def mouse_event(event):
    global node1
    global node2
    global g
    global shortestRoute
    nid = ox.nearest_nodes(g.mapReference, event.xdata, event.ydata)
    node_id = list(g.mapReference.nodes)
    print('x: {} and y: {}'.format(event.xdata, event.ydata))
    for i in range(len(node_id)):
        if node_id[i] == nid:
            if node1 is None:
                with global_lock:
                    node1 = i
            elif node2 is None:
                with global_lock:
                    node2 = i
            break

    # if self.node1 is not None and self.node2 is not None:
    #     a = Astar(self.graph)
    #     distance, path, states_matrix = a.aStarAlgorithm(self.node1, self.node2)
    #     node_id = list(graph.mapReference.nodes)
    #     for p in path:
    #         shortestRoute.append(node_id[p])

def waiting():
    global node1
    global node2
    global g
    global shortestRoute
    while True:
        with global_lock:
            if node1 is not None and node2 is not None:
                break
    a = Astar(g)
    distance, path, states_matrix = a.aStarAlgorithm(node1, node2)
    node_id = list(g.mapReference.nodes)
    for p in path:
        with global_lock:
            shortestRoute.append(node_id[p])

node1 = None
node2 = None
shortestRoute = []

g = CustomGraph(place="Poland, Rumia")
colors = ["#ffffff"]
fig, ax = ox.plot_graph(g.mapReference, close=False, show=False)
cid = fig.canvas.mpl_connect('button_press_event', mouse_event)
t = threading.Thread(target=waiting, name="waitingThread", daemon=True)
t.start()
plt.show()

t.join()
fig.canvas.mpl_disconnect(cid)
ox.plot_graph_route(g.mapReference, shortestRoute)