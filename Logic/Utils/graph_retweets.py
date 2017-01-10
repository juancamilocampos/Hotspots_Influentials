from pymongo import MongoClient
import networkx as nx
from Logic.Utils.config import Configuration
from collections import Counter


class GraphRetweets:
    """ Networkx allows to use a list of repeated elements as nodes
    it will not repeat the node in the node list, instead it will just
    create a unique node"""

    def __init__(self):
        self.ConfigApi = Configuration()
        self.client = MongoClient(self.ConfigApi.MONGO_URL())
        self.db = self.client['local']
        self.coll = self.db[self.ConfigApi.MONGO_COLL_TweetsGnip()]
        self.nodes = list()
        self.edges = list()
        self.edges_weight = list()
        self.undirected_edges_weight = list()
        self.graphdi = nx.DiGraph()
        self.graph = nx.Graph()

    def create(self):
        cursor = self.coll.find({"object.objectType": 'activity'},
                                {"actor.id": 1, "actor.friendsCount": 1, "actor.followersCount": 1,
                                 "object.actor.id": 1,
                                 "object.actor.friendsCount": 1, "object.actor.followersCount": 1})

        # sorted is used to obtain the total weight in a direct graph
        for tweet in cursor:
            self.edges.append((tweet["actor"]["id"], tweet["object"]["actor"]["id"]))
            self.nodes.append((tweet["actor"]["id"], {'friends': tweet["actor"]["friendsCount"],
                                                      'followers': tweet["actor"]["followersCount"]}))
            self.nodes.append((tweet["object"]["actor"]["id"], {'friends': tweet["object"]["actor"]["friendsCount"],
                                                                'followers': tweet["object"]["actor"][
                                                                    "followersCount"]}))

        print(len(self.edges))
        self.edges_weight = Counter(self.edges).most_common()
        self.edges_weight = [(s[0][0], s[0][1], s[1]) for s in self.edges_weight]

        self.graphdi.add_nodes_from(self.nodes)
        self.graphdi.add_weighted_edges_from(self.edges_weight)

        self.edges = sorted(self.edges, key=lambda node: node[0])
        self.undirected_edges_weight = Counter(self.edges).most_common()
        self.undirected_edges_weight = [(s[0][0], s[0][1], (s[1])) for s in self.undirected_edges_weight]
        self.graph.add_nodes_from(self.nodes)
        self.graph.add_weighted_edges_from(self.undirected_edges_weight)

        return [self.graphdi, self.graph]
