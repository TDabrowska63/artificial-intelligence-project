import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import random


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


    #maybe a way of drawing graphs?
    #you guys decide
    def drawGraph(self):
        g = nx.Graph()
        for i in range(self.numberOfNodes):
            for j in range(self.numberOfNodes):
                if self.adjmatrix[i][j] == 1:
                    g.add_edge(i, j)

        nx.draw(g)
        plt.show()


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


