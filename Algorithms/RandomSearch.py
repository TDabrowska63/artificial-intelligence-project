import sys
import random
from Misc.CustomGraph import CustomGraph
import numpy as np
from Misc import *

class RandomSearch:
    def __init__(self, graph):
        self.graph = graph

    def randomSearch(self, start_node, end_node):
        num_nodes = self.graph.numberOfNodes
        visited = [False] * num_nodes
        visited[start_node] = True
        current_node = start_node

        while current_node != end_node:
            neighbors = []
            for i in range(num_nodes):
                if self.graph.weighmatrix[current_node][i] != 0 and not visited[i]:
                    neighbors.append(i)

            if len(neighbors) == 0:
                current_node = random.choice([i for i in range(num_nodes) if visited[i]])
            else:
                current_node = random.choice(neighbors)

            visited[current_node] = True

        path = [end_node]
        while current_node != start_node:
            for i in range(num_nodes):
                if self.graph.weighmatrix[i][current_node] != 0 and visited[i]:
                    path.append(i)
                    current_node = i
                    break

        path.reverse()
        return path


