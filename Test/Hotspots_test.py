from Logic.Utils.graph_retweets import GraphRetweets
import igraph as ig
import Logic.Utils.graph_variables as gv

graph_class = GraphRetweets()
[graph_directed, graph_undirected] = graph_class.create()

inf = gv.influentials(graph_directed)

print(len(inf))

edges_weight = graph_undirected.es["weight"]

f = open('weights-27.txt', 'w')
f.write('{')
for item in edges_weight:
    f.write("%s " % item)
    f.write(",")
f.write("0")
f.write('}')
f.close()

g = (graph_undirected.decompose(maxcompno=1)[0])  # To get the largest connected component
print(g.vcount())
K = list(set(inf).intersection(g.vs["name"]))
g = gv.parallel_dijkstra_undirected(g, K)
Du = g.vs['Dv']
Vu = g.vs['V']

# results = gv.groups(nx.get_node_attributes(g, 'V'))