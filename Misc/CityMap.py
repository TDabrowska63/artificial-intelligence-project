import osmnx as ox

from Algorithms.Astar import Astar
from Algorithms.Dijkstra import Dijkstra
from Misc.Constants import Algorithms


class CityMap:
    def __init__(self, graph):
        self.node1 = None
        self.node2 = None
        self.graph = graph
        self.shortestRoute = []
        self.algorithm = Algorithms.ASTAR_A.value
        self.distance: int = 0
        self.path = []
        self.event_completed = False
        # self.window: OxCityWindow = window

    def mouse_event(self, event, window):
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
            if self.algorithm == Algorithms.ASTAR_A.value:
                a = Astar(self.graph)
                self.distance, self.path, states_matrix = a.a_star_algorithm(self.node1, self.node2)
            elif self.algorithm == Algorithms.DIJKSTRA_A.value:
                d = Dijkstra(self.graph)
                self.distance, self.path, visited_list = d.dijkstra_algorithm(self.node1, self.node2)
            node_id = list(self.graph.mapReference.nodes)

            if self.path is None:
                print(f"Cannot find the path for {self.node1} and {self.node2}")

            for p in self.path:
                self.shortestRoute.append(node_id[p])
            self.node1 = None
            self.node2 = None
            window.update_calculating_label('#090', " READY ")

    @staticmethod
    def do_nothing_event(event):
        print("clicking not active")

# exemplary usage:

# g = CustomGraph(place="Poland, Rumia")
# t = CityMap(g)
# fig, ax = ox.plot_graph(g.mapReference, close=False, show=False)
# cid = fig.canvas.mpl_connect('button_press_event', t.mouse_event)
# plt.show()
# fig.canvas.mpl_disconnect(cid)
# ox.plot_graph_route(g.mapReference, t.shortestRoute)
