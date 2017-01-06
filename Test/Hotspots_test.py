from Logic.Utils.graph_retweets import GraphRetweets
import networkx as nx
import graphVariables as gv

graph_class = GraphRetweets()
[graph_directed, graph_undirected]= graph_class.create()

inf = gv.influentials(graph_directed)

print (len(inf))
