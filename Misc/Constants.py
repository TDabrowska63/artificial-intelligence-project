from enum import Enum


class GraphType(Enum):
    RANDOMIZED = 0
    MAP_BASED = 1


class Algorithms(Enum):
    ASTAR_A = 0
    DIJKSTRA_A = 1
    RANDOM_A = 2


class Colours(Enum):
    NOT_VISITED = 0
    CURRENT_NODE = 1
    NEIGHBOURING_NODE = 2
    IS_OPEN_LIST = 3
    IS_CLOSED_LIST = 4