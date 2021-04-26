import networkx as nx
from random_walks import RandomWalk
import mfa
import torch

#karate_g = nx.read_edgelist('./graph/karate.edgelist')
#karate_g = karate_g.to_directed()

def multifractal(g, filename='weights', walkLength=6, walkNum=6):
    graph = g.to_networkx(edge_attrs=['weight'], node_attrs=['w'])
    #graph = graph.to_directed()
    #print(len(graph))
    #random_walk = RandomWalk(graph, walk_length=walkLength, num_walks=walkNum, p=1, q=1, workers=walkNum)

    #walklist = random_walk.walks

    #src_dest = {}
    #for w in walklist:
    #    #print(w)
    #    if (w[0] not in src_dest.keys()):
    #        src_dest[w[0]] = [w[-1]]
    #    else:
    #        #if (w[-1] not in src_dest[w[0]]):
    #        src_dest[w[0]].append(w[-1])


    #G = nx.complete_graph(4)
    #for path in nx.all_simple_paths(G, source=0, target=3):
     #   print(path)

    #paths = nx.all_simple_paths(G, source=0, target=3, cutoff=2)
    #print(list(paths))
    #print(karate_g.nodes)
    #paths = nx.all_simple_paths(karate_g, source='1', target='34', cutoff=10)
    #print(list(paths))
    #print(src_dest.keys())

    #paths_between_generator = nx.all_simple_paths(karate_g, source=1, target=34)
    src = list(graph.nodes)
    #sortedSrc = sorted(src)
    #f = open(filename+'.txt', 'w')   
    weights = torch.empty(len(graph), 1)
    #print(sortedSrc)    
    row = 0   
    graph = graph.to_undirected()
    Q = [q for q in range(-10,11,1)]
    ntau = mfa.NFD(graph, Q)
            #al_list, fal_list = mfa.nspectrum(ntau, Q)
    q_list, dim_list = mfa.ndimension(ntau, Q, len(graph))                                           
    for s in src:
        #weight = []
        #print("src = ", src)
            #print("src = ", src, ", dest = ", dest)
            #paths_between_generator = nx.all_simple_paths(graph, source=src, target=dest, cutoff=walkLength)
            #print(list(paths))       
            #nodes_between_set = {node for path in paths_between_generator for node in path}
            #SG = graph.subgraph(nodes_between_set)

            #print(col)
        weights[row][0] = dim_list[11]
        row += 1
        #s1 = ' '.join(map(str, weight))
        #print(s1)
        #weights.append(weight)
        #f.write(s1)
        #f.write('\n')
    #f.close()
    return weights.float()
