from Logic.Utils.graph_retweets import GraphRetweets
import networkx as nx
import Logic.Utils.graph_variables as gv

graph_class = GraphRetweets()
[graph_directed, graph_undirected] = graph_class.create()

inf = gv.influentials(graph_directed)

edges_weight = list()
[edges_weight.append(edata['weight']) for u, v, edata in graph_undirected.edges(data=True) if 'weight' in edata]

f = open('weights-25.txt', 'w')
f.write('{')
for item in edges_weight:
    f.write("%s " % item)
    f.write(",")
f.write("0")
f.write('}')
f.close()

g = max(nx.connected_component_subgraphs(graph_undirected), key=len)  # To get the largest connected component
K = list(set(inf).intersection(g.nodes()))

g, tag = gv.parallel_dijkstra(g, K, 1)
Du = nx.get_node_attributes(g, 'Dv')
Vu = nx.get_node_attributes(g, 'V')

f = open('Dv.txt', 'w')
f.write('{')
for item in list(Du.values()):
    f.write("%s " % item)
    f.write(",")
f.write("0")
f.write('}')
f.close()

results = gv.groups(Vu)
print(len(results['id:twitter.com:100293263']))

# # # [hotspot_boolean, c, final_hotspots] = gv.graph_hotspots(results, K, g, 1.01)
# #
# [hotspot_boolean, c, weights_influentials] = gv.graph_hotspots(results, K, g, 1.01)
# print(1)
# f = open('weights-between-influentials-27.txt', 'w')
# f.write('{')
# for item in weights_influentials:
#     f.write("%s " % item)
#     f.write(",")
#
# f.write("0")
# f.write('}')
# f.close()