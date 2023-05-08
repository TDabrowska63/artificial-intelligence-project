import numpy as np


class CustomGraph:
    def __int__(self, type="adjmatrix", numberOfNodes=10):
        self.numberOfNodes = numberOfNodes
        if type == "adjmatrix":
            self.struct = np.zeros(numberOfNodes);
        elif type == "adjlist":
            pass
            # TODO Implement adjacency list construction
            # I still dont know if this is necessary

    def printMe(self):
        print(self.struct)
