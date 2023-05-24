import numpy as np
from Constants import *
class Astar:
    def __init__(self, graph):
        self.adjacency_list = self.transform(graph)
        self.graph = graph

    def getNeighbors(self, v):
        return self.adjacency_list[v]

    def h(self, n, stopNode):
        H = {}
        for i in range(self.graph.numberOfNodes):
            distance = self.graph.distance(i, stopNode)
            H[i] = distance

        return H[n]

    #returns: path, statesMatrix, distance
    def aStarAlgorithm(self, startNode, stopNode):
        # open_list is a list of nodes which have been visited, but who's neighbors
        # haven't all been inspected, starts off with the start node
        # closed_list is a list of nodes which have been visited
        # and who's neighbors have been inspected
        openList = set([startNode])
        closedList = set([])
        statesMatrix = np.full((self.graph.numberOfNodes, 2), Colours.NOT_VISITED, dtype=Colours)
        statesMatrix[startNode, 1] = Colours.IS_OPEN_LIST

        # g contains current distances from start_node to all other nodes
        # the default value (if it's not found in the map) is +infinity
        g = {}

        g[startNode] = 0

        # parents contains an adjacency map of all nodes
        parents = {}
        parents[startNode] = startNode

        newState = np.full((self.graph.numberOfNodes, 1), Colours.NOT_VISITED, dtype=Colours)
        while len(openList) > 0:
            n = None

            # find a node with the lowest value of f() - evaluation function
            for v in openList:
                if n == None or g[v] + self.h(v, stopNode) < g[n] + self.h(n, stopNode):
                    n = v

            if n == None:
                print('Path does not exist!')
                return None, statesMatrix, None

            newState[n][0] = Colours.CURRENT_NODE
            statesMatrix = np.hstack((statesMatrix, newState))

            # if the current node is the stop_node
            # then we begin reconstructing the path from it to the start_node
            if n == stopNode:
                reconstPath = []

                while parents[n] != n:
                    reconstPath.append(n)
                    n = parents[n]

                reconstPath.append(startNode)

                reconstPath.reverse()

                distance = 0
                for i in range(len(reconstPath) - 1):
                    distance = distance + self.graph.weighmatrix[reconstPath[i], reconstPath[i+1]]

                print('Path found: {}'.format(reconstPath))
                return reconstPath, statesMatrix, distance

            neighbours = self.getNeighbors(n)
            # for all neighbors of the current node do
            for (m, weight) in neighbours:
                # if the current node isn't in both open_list and closed_list
                # add it to open_list and note n as it's parent
                if m not in openList and m not in closedList:
                    openList.add(m)
                    parents[m] = n
                    g[m] = g[n] + weight
                    newState[m][0] = Colours.IS_OPEN_LIST

                # otherwise, check if it's quicker to first visit n, then m
                # and if it is, update parent data and g data
                # and if the node was in the closed_list, move it to open_list
                else:
                    if g[m] > g[n] + weight:
                        g[m] = g[n] + weight
                        parents[m] = n

                        if m in closedList:
                            closedList.remove(m)
                            openList.add(m)
                            newState[m][0] = Colours.IS_OPEN_LIST

            statesMatrix = np.hstack((statesMatrix, newState))
            # remove n from the open_list, and add it to closed_list
            # because all of his neighbors were inspected
            openList.remove(n)
            closedList.add(n)
            newState[n][0] = Colours.IS_CLOSED_LIST
            statesMatrix = np.hstack((statesMatrix, newState))

        print('Path does not exist!')
        return None, statesMatrix, None

    def transform(self, graph):
        adj_list = {}
        for i in range(graph.numberOfNodes):
            neighbours = []
            for j in range(graph.numberOfNodes):
                if graph.adjmatrix[i, j] == 1 and i != j:
                    neighbours.append((j, graph.weighmatrix[i, j]))
            adj_list[i] = neighbours
        return adj_list
    def printMe(self):
        print("Adjacency list:")
        print(self.adjacency_list)