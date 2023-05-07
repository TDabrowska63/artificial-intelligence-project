import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

# przykładowa macierz sąsiedztwa
adj_matrix = np.array([[0, 1, 1], [1, 0, 1], [1, 1, 0]])

# utworzenie grafu z macierzy sąsiedztwa
graph = nx.from_numpy_matrix(adj_matrix)

# rysowanie grafu
nx.draw(graph, with_labels=True)
plt.show()
