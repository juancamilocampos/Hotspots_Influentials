from Logic.Utils.graph_retweets import GraphRetweets
import networkx as nx
import Logic.Utils.graph_variables as gv

graph_class = GraphRetweets()
[graph_directed, graph_undirected] = graph_class.create()

inf = gv.influentials(graph_directed)

print(len(inf))

edges_weight = list()
[edges_weight.append(edata['weight']) for u, v, edata in graph_undirected.edges(data=True) if 'weight' in edata]

f = open('weights-27.txt', 'w')
f.write('{')
for item in edges_weight:
    f.write("%s " % item)
    f.write(",")

f.write("0")
f.write('}')
f.close()

# g = max(nx.connected_component_subgraphs(graph_undirected), key=len)  # To get the largest connected component
#
# K = list(set(inf).intersection(g.nodes()))
# g, tag = gv.parallel_dijkstra(g, K, 1)
# Du = nx.get_node_attributes(g, 'Dv')
# Vu = nx.get_node_attributes(g, 'V')
#
# results = gv.groups(nx.get_node_attributes(g, 'V'))
#
# [hotspot_boolean, c, final_hotspots] = gv.graph_hotspots(results, K, g, 1.01)