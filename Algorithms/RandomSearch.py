import sys
import random
from Misc.CustomGraph import CustomGraph
import numpy as np
from Misc import *

class RandomSearch:
    def __init__(self, graph):
        self.graph = graph
        self.adjList = graph.transform(graph)

    def randomSearch(self, start_node, end_node, iterations):
        current_node = start_node

        bestDistance = float('inf')
        bestIteration = 1
        path = [start_node]
        for i in range(iterations):
            next_node = random.choice(self.adjList[current_node])
            path.append(next_node)

            current_node = next_node
            if current_node == end_node:
                distance = 0
                for j in range(len(path) - 1):
                    distance = distance + self.graph.weighmatrix[path[i], path[i + 1]]
                if distance < bestDistance:
                    bestDistance = distance
                    bestPath = path[:]
                    bestIteration = i
                path = [start_node]

        return bestDistance, bestPath, bestIteration