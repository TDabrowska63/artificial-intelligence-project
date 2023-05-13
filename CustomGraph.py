import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
import random
from GUI import GUI


class CustomGraph:
    def __init__(self, numberOfNodes=10):
        self.numberOfNodes = numberOfNodes
        self.adjmatrix = np.zeros((numberOfNodes, numberOfNodes), dtype=int)
        self.weighmatrix = np.zeros((numberOfNodes,numberOfNodes), dtype=int)

    # Method just for debugging, ignore
    def printMe(self):
        print("Adjacency matrix:")
        print(self.adjmatrix)
        print("Adjacency weights:")
        print(self.weighmatrix)

    # maybe a way of drawing graphs?
    # you guys decide
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
            for j in range(i + 1, self.numberOfNodes):
                adj = random.randint(0, 1)
                weight = random.randint(1, 20)
                self.adjmatrix[i, j] = adj
                self.adjmatrix[j, i] = adj
                if adj == 1:
                    self.weighmatrix[i, j] = weight
                    self.weighmatrix[j, i] = weight

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


