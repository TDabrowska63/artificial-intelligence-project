import sys


class Dijkstra:
    def __init__(self, graph):
        self.graph = graph
        self.visited = [False] * graph.numberOfNodes
        self.distances = [sys.maxsize] * graph.numberOfNodes
        self.previous = [None] * self.graph.numberOfNodes

    def dijkstraAlgorithm(self, start, end):
        self.distances[start] = 0

        while not self.visited[end]:
            min_distance = sys.maxsize
            min_index = -1
            for i in range(self.graph.numberOfNodes):
                if not self.visited[i] and self.distances[i] < min_distance:
                    min_distance = self.distances[i]
                    min_index = i

            self.visited[min_index] = True

            if min_index == end:
                path = self._build_path(end)
                return self.distances[end], path

            for j in range(self.graph.numberOfNodes):
                if (
                        not self.visited[j]
                        and self.graph.weighmatrix[min_index][j] != 0
                        and self.distances[min_index] != sys.maxsize
                        and self.distances[min_index] + self.graph.weighmatrix[min_index][j] < self.distances[j]
                ):
                    self.distances[j] = self.distances[min_index] + self.graph.weighmatrix[min_index][j]
                    self.previous[j] = min_index
        return None, None

    def _build_path(self, end):
        path = []
        current = end

        while current is not None:
            path.insert(0, current)
            current = self.previous[current]

        return path


