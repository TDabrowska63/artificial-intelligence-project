import random
from math import sin, cos, sqrt, atan2, radians
import numpy as np
import osmnx as ox
import networkx as nx
from Misc.Constants import GraphType

class CustomGraph:
    # X/Ybound are the sizes of the plane
    # the graph is randomized by default
    def __init__(self, numberOfNodes=10, density=30, Xbound=20, Ybound=20, place="None"):
        self.numberOfNodes = numberOfNodes
        self.adjmatrix = np.zeros((numberOfNodes, numberOfNodes), dtype=int)
        self.weighmatrix = np.zeros((numberOfNodes, numberOfNodes), dtype=int)
        self.density = density
        self.nodeCoords = []
        self.Xbound = Xbound
        self.Ybound = Ybound
        self.place = place
        self.type = GraphType.RANDOMIZED
        self.mapReference = None
        if place != "None":
            self.type = GraphType.MAP_BASED
            self.initializeMapGraph()

    # Method just for debugging, ignore
    def printMe(self):
        print("Coordinates of nodes:")
        print(self.nodeCoords)
        print("Adjacency matrix:")
        print(self.adjmatrix)
        print("Adjacency weights:")
        print(self.weighmatrix)

    def initializeMapGraph(self):
        G = ox.graph_from_place(self.place, network_type='drive')
        self.adjmatrix = nx.adjacency_matrix(G).toarray()
        self.mapReference = G # if it was ever needed again, custom graph contains reference to the map
        node_id = list(G.nodes)
        for nid in node_id:
            self.nodeCoords.append((G.nodes[nid]['x'], G.nodes[nid]['y']))

        self.numberOfNodes = len(node_id)
        self.weighmatrix = np.zeros((self.numberOfNodes, self.numberOfNodes), dtype=float)
        for i in range(self.numberOfNodes):  # row
            for j in range(i + 1, self.numberOfNodes):  # column
                if self.adjmatrix[i, j] != 0:
                    weight = self.lonLatDistance(i, j)
                    self.weighmatrix[i, j] = weight
                    self.weighmatrix[j, i] = weight

    def randomize(self):
        for i in range(self.numberOfNodes):
            coord = (random.randint(0, self.Xbound), random.randint(0, self.Ybound))
            while coord in self.nodeCoords:
                coord = (random.randint(0, self.Xbound), random.randint(0, self.Ybound))
            self.nodeCoords.append(coord)

        for i in range(self.numberOfNodes): # row
            for j in range(i + 1, self.numberOfNodes):  # column
                adj = random.randint(0, 100)
                weight = self.distance(i, j)
                if adj <= self.density:
                    self.adjmatrix[i, j] = 1
                    self.adjmatrix[j, i] = 1
                    self.weighmatrix[i, j] = weight
                    self.weighmatrix[j, i] = weight

    def distance(self, i, j):
        x1 = self.nodeCoords[i][0]
        y1 = self.nodeCoords[i][1]
        x2 = self.nodeCoords[j][0]
        y2 = self.nodeCoords[j][1]
        return np.sqrt((x1-x2)**2 + (y1-y2)**2)

    def lonLatDistance(self, i, j):
        R = 6373.0

        lat1 = radians(self.nodeCoords[i][0])
        lon1 = radians(self.nodeCoords[i][1])
        lat2 = radians(self.nodeCoords[j][0])
        lon2 = radians(self.nodeCoords[j][1])

        dlon = lon2 - lon1
        dlat = lat2 - lat1

        a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))

        return R * c

    def standardInput(self):
        print("put in (is adjacent, weight)")
        for i in range(self.numberOfNodes):
            for j in range(i+1, self.numberOfNodes):
                    isAdj = input()
                    weight = input()
                    self.adjmatrix[i, j] = isAdj
                    if isAdj == 1:
                        self.weighmatrix[i, j] = weight
                    else:
                        self.weighmatrix[i, j] = 0

    def transform(self, graph):
        adj_list = {}
        for i in range(graph.numberOfNodes):
            neighbours = []
            for j in range(graph.numberOfNodes):
                if graph.adjmatrix[i, j] == 1 and i != j:
                    neighbours.append((j, graph.weighmatrix[i, j]))
            adj_list[i] = neighbours
        return adj_list
