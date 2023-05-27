import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg)
import random


class CustomGraph:
    # X/Ybound are the sizes of the plane
    def __init__(self, numberOfNodes=10, density=30, Xbound=20, Ybound=20):
        self.numberOfNodes = numberOfNodes
        self.adjmatrix = np.zeros((numberOfNodes, numberOfNodes), dtype=int)
        self.weighmatrix = np.zeros((numberOfNodes, numberOfNodes), dtype=int)
        self.density = density
        self.nodeCoords = []
        self.Xbound = Xbound
        self.Ybound = Ybound

    # Method just for debugging, ignore
    def printMe(self):
        print("Coordinates of nodes:")
        print(self.nodeCoords)
        print("Adjacency matrix:")
        print(self.adjmatrix)
        print("Adjacency weights:")
        print(self.weighmatrix)


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
