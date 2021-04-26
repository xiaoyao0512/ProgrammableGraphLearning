import networkx as nx
import mfa
import numpy as np

G = nx.Graph()
G.add_edge(0, 2, weight=1)
G.add_edge(0, 3, weight=1)
G.add_edge(1, 2, weight=1)
G.add_edge(1, 3, weight=1)
nodes = G.number_of_nodes()
edges = G.number_of_edges()
deg_assort = nx.degree_pearson_correlation_coefficient(G)
apl = nx.average_shortest_path_length(G)
num_cliq = nx.graph_number_of_cliques(G)
diameter = nx.diameter(G)
Q = [q for q in range(-10,11,1)]
lst = [nodes, edges, deg_assort, apl, num_cliq, diameter]
ntau = mfa.NFD(G, Q)
al_list, fal_list = mfa.nspectrum(ntau, Q)
q_list, dim_list = mfa.ndimension(ntau, Q)
lst.extend(al_list)
lst.extend(fal_list)
lst.extend(q_list)
lst.extend(dim_list)
print(lst)