from pymongo import MongoClient
import igraph as ig
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
        self.nodes_set = list()
        self.nodes_attribute_friends = {}
        self.nodes_attribute_followers = {}
        self.edges = list()
        self.edges_weight = list()
        self.undirected_edges_weight = list()
        self.graphdi = ig.Graph(directed=True)
        self.graph = ig.Graph()
        self.indices = list()

    def create(self):
        cursor = self.coll.find({"object.objectType": 'activity'},
                                {"actor.id": 1, "actor.friendsCount": 1, "actor.followersCount": 1,
                                 "object.actor.id": 1,
                                 "object.actor.friendsCount": 1, "object.actor.followersCount": 1}, no_cursor_timeout=
                                True)

        # sorted is used to obtain the total weight in a direct graph
        for tweet in cursor:
            self.edges.append((tweet["actor"]["id"], tweet["object"]["actor"]["id"]))
            self.nodes_attribute_friends[tweet["actor"]["id"]] = tweet["actor"]["friendsCount"]
            self.nodes_attribute_followers[tweet["actor"]["id"]] = tweet["actor"]["followersCount"]
            self.nodes_attribute_friends[tweet["object"]["actor"]["id"]] = tweet["object"]["actor"]["friendsCount"]
            self.nodes_attribute_followers[tweet["object"]["actor"]["id"]] = tweet["object"]["actor"]["followersCount"]

        cursor.close()
        self.nodes = list(self.nodes_attribute_friends.keys())

        print(len(self.edges))
        self.edges_weight = Counter(self.edges).most_common()
        self.edges_weight = [(s[0][0], s[0][1], s[1]) for s in self.edges_weight]

        self.graphdi.add_vertices(self.nodes)
        self.graphdi.vs["friends"] = list(self.nodes_attribute_friends.values())
        self.graphdi.vs["followers"] = list(self.nodes_attribute_followers.values())
        self.graphdi.add_edges([(s[0], s[1]) for s in self.edges_weight])
        self.graphdi.es["weight"] = ([s[2] for s in self.edges_weight])

        self.edges = sorted(self.edges, key=lambda node: node[0])
        self.undirected_edges_weight = Counter(self.edges).most_common()
        self.undirected_edges_weight = [(s[0][0], s[0][1], (s[1])) for s in self.undirected_edges_weight]

        self.graph.add_vertices(self.nodes)
        self.graphdi.vs["friends"] = list(self.nodes_attribute_friends.values())
        self.graphdi.vs["followers"] = list(self.nodes_attribute_followers.values())
        self.graph.add_edges([(s[0], s[1]) for s in self.undirected_edges_weight])
        self.graph.es["weight"] = ([s[2] for s in self.undirected_edges_weight])

        return [self.graphdi, self.graph]
