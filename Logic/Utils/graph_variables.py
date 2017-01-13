# coding=utf-8
import igraph as ig
import math
import heapq
from collections import defaultdict


def _replace(lista, item_to_replace, replacement_value):
    """
    :Date: 2016-09-18
    :Version: 0.1
    :Author: Juan Camilo Campos - Pontificia Universidad Javeriana Cali
    :Copyright: To be defined
    :Organization: Centro de Excelencia y Apropiación de Big Data y Data Analytics - CAOBA

    This method replaces every occurrence of the item_to_replace by the replacement value

    :param: lista: list of values
    :param: item_to_replace: value to replace.
    :param: replacement_value: replacement value
    :rtype: list
    :return: Returns the new list

    """
    for n, i in enumerate(lista):
        if i == item_to_replace:
            lista[n] = replacement_value

    return lista


def influentials(g):
    """
    :Date: 2016-09-18
    :Version: 0.1
    :Author: Juan Camilo Campos - Pontificia Universidad Javeriana Cali
    :Copyright: To be defined
    :Organization: Centro de Excelencia y Apropiación de Big Data y Data Analytics - CAOBA

    This method evaluates if each node satisfies the requirements to be considered as influential. Then it return the
    list of influentials

    :param: g:  weighted graph (V,E) of retweets where i->j belongs to E if user i retweets user j. V = {v1, ... vn},
     such that v=(name, friends, followers)
    :rtype: list
    :return: Returns the list of influential users
    """
    threshold = 1 / 10.0

    nodes = g.vs["name"]

    retweets = [sum([g.es[s]["weight"] for s in g.incident(t, mode="out")]) for t in nodes]
    times_retweeted = [sum([g.es[s]["weight"] for s in g.incident(t, mode="in")]) for t in nodes]

    retweets = _replace(retweets, 0, 1)

    friends = g.vs["friends"]
    followers = g.vs["followers"]

    friends = _replace(friends, 0, 1)

    list_influentials = []

    i = 0
    while i < len(nodes):
        if (followers[i] <= 0) or (times_retweeted[i] <= 0) or (friends[i] <= 0) or (retweets[i] <= 0):
            nodes.pop(i)
            followers.pop(i)
            friends.pop(i)
            times_retweeted.pop(i)
            retweets.pop(i)
        else:
            x = retweets[i] / float(times_retweeted[i])
            y = friends[i] / float(followers[i])

            if (x < threshold) and (y < threshold):
                list_influentials = list_influentials + [nodes[i]]

            i += 1

    return list_influentials

def _interest_entrophy(C, Hu):
    """
    :Date: 2016-09-18
    :Version: 0.1
    :Author: Juan Camilo Campos - Pontificia Universidad Javeriana Cali
    :Copyright: To be defined
    :Organization: Centro de Excelencia y Apropiación de Big Data y Data Analytics - CAOBA

    This method computes the entropy of a user's hashtags

    :param: C: Hashtags communities (topics in the hashtags co-occurrence graph).
    :param: Hu: Hashtags used by the user.
    :rtype: float
    :return: Returns value of the entrophy of a user's hashtags
    """

    Cn = C
    T = []

    for h in Hu:
        cdefined = False

        for i in range(0, len(Cn)):
            community = Cn[i]

            if h in community:
                T = T + [i]
                cdefined = True

        if cdefined == False:
            Cn = Cn + [[h]]
            T = T + [len(Cn) - 1]

    Tu = list(set(T))
    nu = float(len(Hu))
    totalu = 0
    for Tk in Tu:
        P = (T.count(Tk)) / nu
        totalu = totalu - P * math.log10(P)

    return totalu


def users_entrophy(C, H):
    """
    :Date: 2016-09-18
    :Version: 0.1
    :Author: Juan Camilo Campos - Pontificia Universidad Javeriana Cali
    :Copyright: To be defined
    :Organization: Centro de Excelencia y Apropiación de Big Data y Data Analytics - CAOBA

    This method computes the entropy of hashtags for all users.

    :param: C: Hashtags communities (topics in the hashtags co-occurence graph).
    :param: Hu: List of Hashtags used by each user.
    :rtype: list of floats
    :return: Returns a list with the values of the entrophy of hashtags for all users.
    """

    graphentrophy = list()

    for Hu in H:
        graphentrophy.append(_interest_entrophy(C, Hu))

    return graphentrophy


def parallel_dijkstra_undirected(g, k):
    nbors = {}
    nodes = g.vs["name"]
    for v in range(g.vcount()):
        nbors[v] = [s for s in g.neighbors(v)]

    ids = {}
    for i in range(g.vcount()):
        ids[nodes[i]] = i

    k = [ids[s] for s in k]
    g.vs["Dv"] = [1000]*g.vcount()
    g.vs['V'] = [0]*g.vcount()
    g.vs['visit'] = [0]*g.vcount()

    Q = []
    for ki in k:
        g.vs[ki]['Dv'] = 0
        g.vs[ki]['V'] = ki
        heapq.heappush(Q, (0, ki))

    # Node Expansion: First find the lowest value and check not visited node
    while len(Q) != 0:
        v = heapq.heappop(Q)
        g.vs[v[1]]['visit'] = 1  # Mark the node as visited

        # Visit all the neighbors of the node to be expanded
        for nbr in nbors[v[1]]:
            if g.vs[nbr]['visit'] == 0:
                delta = g.vs[v[1]]['Dv'] + g.es[g.get_eid(nbr, v[1])]['weight']

                if g.vs[nbr]['Dv'] == 1000:
                    g.vs[nbr]['Dv'] = delta
                    g.vs[nbr]['V'] = g.vs[v[1]]['V']
                    heapq.heappush(Q, (delta, nbr))

                if (g.vs[nbr]['Dv'] < 1000) and (delta < g.vs[nbr]['Dv']):
                    g.vs[nbr]['V'] = g.vs[v[1]]['V']
                    g.vs[nbr]['Dv'] = delta
    return g

def groups(many_to_one):
    one_to_many = defaultdict(list)
    for v, k in many_to_one.items():
        one_to_many[k].append(v)
    return dict(one_to_many)

