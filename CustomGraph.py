import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
import random
from GUI import GUI


class CustomGraph:
    def __init__(self, numberOfNodes=10, density=30, Xbound = 20, Ybound = 20):
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

    #drawing graphs
    def drawGraph(self, window):
        g = nx.Graph()
        for i in range(self.numberOfNodes):
            for j in range(self.numberOfNodes):
                if self.adjmatrix[i][j] == 1:
                    g.add_edge(i, j)

        fig = plt.Figure(figsize=(5, 5), dpi=100)
        canvas = FigureCanvasTkAgg(fig, window)
        canvas.draw()
        canvas.get_tk_widget().grid(row=0, column=0)
        a = fig.add_subplot(111)
        a.cla()
        nx.draw(g, ax=a, with_labels=True)
        a.plot()
        canvas.draw()

    def randomize(self):
        for i in range(self.numberOfNodes):
            coord = (random.randint(0, self.Xbound), random.randint(0, self.Ybound))
            while coord in self.nodeCoords:
                coord = (random.randint(0, self.Xbound), random.randint(0, self.Ybound))
            self.nodeCoords.append(coord)

        for i in range(self.numberOfNodes):
            for j in range(i + 1, self.numberOfNodes):
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


