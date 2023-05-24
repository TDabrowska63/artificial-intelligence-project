from enum import Enum


class Algorithms(Enum):
    DIJKSTRA_A = 0
    ASTAR_A = 1


class Colours(Enum):
    NOT_VISITED = 0
    CURRENT_NODE = 1
    NEIGHBOURING_NODE = 2
    IS_OPEN_LIST = 3
    IS_CLOSED_LIST = 4