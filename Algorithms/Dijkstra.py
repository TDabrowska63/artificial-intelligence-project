import sys
from collections import deque


class Dijkstra:
    def __init__(self, graph):
        self.graph = graph
        self.visited = [False] * graph.numberOfNodes
        self.distances = [sys.maxsize] * graph.numberOfNodes
        self.previous = [None] * self.graph.numberOfNodes
        self.visited_in_order = deque()

    # returns distance, path, visitedList
    def dijkstra_algorithm(self, start, end):
        self.distances[start] = 0

        while not self.visited[end]:
            min_distance = sys.maxsize
            min_index = -1
            for i in range(self.graph.numberOfNodes):
                if not self.visited[i] and self.distances[i] < min_distance:
                    self.visited_in_order.append(i)
                    min_distance = self.distances[i]
                    min_index = i

            self.visited[min_index] = True

            if min_index == end:
                path = self._build_path(end)
                unique = set()
                new_visited = deque()
                while self.visited_in_order:
                    element = self.visited_in_order.popleft()
                    if element not in unique:
                        unique.add(element)
                        new_visited.append(element)
                visited_list = list(new_visited)
                print('Path found: {}'.format(path))
                return self.distances[end], path, visited_list
            if min_distance == sys.maxsize:
                break
            for j in range(self.graph.numberOfNodes):
                if (
                        not self.visited[j]
                        and self.graph.weighmatrix[min_index][j] != 0
                        and self.distances[min_index] != sys.maxsize
                        and self.distances[min_index] + self.graph.weighmatrix[min_index][j] < self.distances[j]
                ):
                    self.distances[j] = self.distances[min_index] + self.graph.weighmatrix[min_index][j]
                    self.previous[j] = min_index
        unique = set()
        new_visited = deque()
        while self.visited_in_order:
            element = self.visited_in_order.popleft()
            if element not in unique:
                unique.add(element)
                new_visited.append(element)
        visited_list = list(new_visited)
        return None, None, visited_list

    def _build_path(self, end):
        path = []
        current = end

        while current is not None:
            path.insert(0, current)
            current = self.previous[current]

        return path
