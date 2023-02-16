import matplotlib.pyplot as plt
import networkx as nx

G = nx.Graph()
G.add_nodes_from([f"A{i}" for i in range(1, 6)])



G.add_edges_from([(f"A{i}", f"A{i+1}") for i in range(1, 5)])


pos = {f"A{i}" : (i, 1) for i in range(1, 6)}



nx.draw(G, pos, with_labels=True)

plt.margins(0.2)
plt.show()