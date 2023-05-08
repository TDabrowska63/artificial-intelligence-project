import numpy as np
import random


class CustomGraph:
    def __init__(self, numberOfNodes=10):
        self.numberOfNodes = numberOfNodes
        self.matrix = np.zeros((numberOfNodes, numberOfNodes), dtype=int)

    # Method just for debugging, ignore
    def printMe(self):
        print(self.matrix)

    def randomize(self):
        for i in range(self.numberOfNodes):
            for j in range(i + 1, self.numberOfNodes):
                tmp = random.randint(0, 1)
                self.matrix[i, j] = tmp
                self.matrix[j, i] = tmp

