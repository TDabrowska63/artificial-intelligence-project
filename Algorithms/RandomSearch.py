import sys
import random
import numpy as np

class RandomSearch:
    def __init__(self, graph):
        self.graph = graph

    def random_search(self,start_node, end_node, max_iterations):
        current_node = start_node
        path = [current_node]
        total_weight = 0

        for i in range(max_iterations):
            if current_node == end_node:
                return path, total_weight

            neighbors = self.graph[current_node]
            neighbor_nodes = [i for i in range(len(neighbors)) if neighbors[i] != 0]
            neighbor_weights = [neighbors[i] for i in neighbor_nodes]

            random_index = random.randint(0, len(neighbor_nodes) - 1)
            next_node = neighbor_nodes[random_index]
            next_weight = neighbor_weights[random_index]
            path.append(next_node)
            total_weight += next_weight

            current_node = next_node

        return None


