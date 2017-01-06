# coding=utf-8
import networkx as nx
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

    nodes = g.nodes()

    retweets = g.out_degree(weight='weight')
    times_retweeted = g.in_degree(weight='weight')

    retweets = [retweets[s] for s in nodes]
    retweets = _replace(retweets, 0, 1)
    times_retweeted = [times_retweeted[s] for s in nodes]

    friends = nx.get_node_attributes(g, 'friends')
    followers = nx.get_node_attributes(g, 'followers')

    friends = [friends[s] for s in nodes]
    friends = _replace(friends, 0, 1)
    followers = [followers[s] for s in nodes]

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


def parallel_dijkstra(g, k, z):
    nbors = type_ident(g, z)

    nx.set_node_attributes(g, 'Dv', 1000)
    nx.set_node_attributes(g, 'V', 0)
    nx.set_node_attributes(g, 'visit', 0)

    Q = []
    tag = []
    for ki in k:
        g.node[ki]['Dv'] = 0
        g.node[ki]['V'] = ki
        tag.append('V' + str(ki))
        heapq.heappush(Q, (0, ki))

    # Node Expansion: First find the lowest value and check not visited node
    while len(Q) != 0:
        v = heapq.heappop(Q)
        g.node[v[1]]['visit'] = 1  # Mark the node as visited

        # Visit all the neighbors of the node to be expanded
        for nbr in nbors(v[1]):
            if g.node[nbr]['visit'] == 0:
                if z == 2:
                    delta = g.node[v[1]]['Dv'] + (g.get_edge_data(nbr, v[1]))['weight']
                else:
                    delta = g.node[v[1]]['Dv'] + (g.get_edge_data(v[1], nbr))['weight']

                if g.node[nbr]['Dv'] == 1000:
                    g.node[nbr]['Dv'] = delta
                    g.node[nbr]['V'] = g.node[v[1]]['V']
                    heapq.heappush(Q, (delta, nbr))

                if (g.node[nbr]['Dv'] < 1000) and (delta < g.node[nbr]['Dv']):
                    g.node[nbr]['V'] = g.node[v[1]]['V']
                    g.node[nbr]['Dv'] = delta
    return g, tag


def groups(many_to_one):
    one_to_many = defaultdict(list)
    for v, k in many_to_one.items():
        one_to_many[k].append(v)
    return dict(one_to_many)


def type_ident(g, t):
    ginfo = nx.info(g)
    ginfo = ginfo.split('\n')
    ginfo = ginfo[1].split(':')

    if ginfo[1] == ' Graph':
        n_obj = g.neighbors
    elif t == 1:
        n_obj = g.neighbors
    elif t == 2:
        n_obj = g.predecessors
    else:
        n_obj = g.neighbors

    return n_obj


def graph_hotspots(dict_voronoi, K, g, maxdistance):
    """
    :Date: 2016-09-18
    :Version: 0.1
    :Author: Juan Camilo Campos - Pontificia Universidad Javeriana Cali
    :Copyright: To be defined
    :Organization: Centro de Excelencia y Apropiación de Big Data y Data Analytics - CAOBA

    This method establishes the existence of hotspots in a Graph. Furthermore, if there are hotspots, then it returns which are the hotspots

    :param: dict_voronoi: dictionary with the information about the voronoi segmentation
    :param: K: breaking nodes (sometimes the influentials)
    :param: g: unweighted and undirected graph
    :param: maxdistance: maximum distance between breaking point to be considered as a part of the same hotspots
    :rtype: list [hotspotboolean,c,finalhotspots]
    :return: hotspotboolean: It is True if there are hotspots in the graph
    :return: c: The percentaje of crimes or influentials when there is the 30% of the network in the accumulative distribution
    :return: finalhotspots: If there are hotspots, it contains the hotspots
    """
    cellsizes = list()
    for k in K:
        cellsizes.append([k, len(dict_voronoi[k])])

    cellsizes = sorted(cellsizes, key=lambda t: t[1])
    # cellsizes = np.array(cellsizes)

    nnodes = len(g.nodes())
    nodes_distribution = [0]
    influentials_distribution = list()
    ncells = len(K)
    c = 0
    for i in range(len(K)):
        nodes_distribution.append(nodes_distribution[-1] + cellsizes[i][1])
        [x, y] = [1.0 * (i + 1) / len(K), 1.0 * nodes_distribution[-1] / nnodes]
        influentials_distribution.append([x, y])
        if y <= 0.3:
            c = x
            px = i

    # If more than the 70% of influentials are contained in the 30% of the network, then there are hostposts and it stars to calculate them.
    if c >= 0.70:
        # Hk is the set of the breaking nodes which build the "small" voronoi cells.
        Hk = list()
        for i in range(px):
            Hk.append(cellsizes[i][0])

        final_hotspots = _hotspots_breaking_nodes(dict_voronoi, Hk, g, maxdistance)
        return [True, c, final_hotspots]
    else:
        return [False, 0, {}]


def _hotspots_breaking_nodes(dict_voronoi, Hk, g, maxdistance):
    """
    :Date: 2016-09-18
    :Version: 0.1
    :Author: Juan Camilo Campos - Pontificia Universidad Javeriana Cali
    :Copyright: Por definir
    :Organization: Centro de Excelencia y Apropiación de Big Data y Data Analytics - CAOBA

    This method finds the hotspots in a graph

    :param: dict_voronoi: dictionary with the information about the voronoi segmentation
    :param: Kh: breaking nodes which build the "small" voronoi cells (sometimes the influentials)
    :param: g: unweighted and undirected graph
    :param: maxdistance: maximum distance between breaking point to be considered as a part of the same hotspots
    :rtype: list of hotspots
    :return: finalhotspots: list with the nodes that every hotspot contains.
    """

    hotspots = list()
    for i in range(len(Hk)):
        hotspots.append(i)

    i = 0
    while i < len(Hk):
        j = i
        while j < len(Hk):
            if hotspots[i] != hotspots[j]:
                ##Here two voronoi cells are integrated in the same hotspot if their distance is less than the maxdistance
                if len(nx.shortest_path(g, source=Hk[i], target=Hk[j])) <= maxdistance:
                    gs = g.subgraph(list(set(dict_voronoi[Hk[i]]).union(set(dict_voronoi[Hk[i]]))))
                    if nx.is_connected(g):
                        hotspot_son = hotspots[j]
                        hotspot_parent = hotspots[i]
                        hotspots = _replace(hotspots, hotspot_son, hotspot_parent)

            j = j + 1
        i = i + 1

    hotspots_set = list(set(hotspots))
    final_hotspots = list()
    for h in hotspots_set:
        indices = [i for i, x in enumerate(hotspots) if x == h]
        ##This condition guarantees that an union of voronoi cells can be considered as a hotspot if it contains almost the 2% of the "small" voronoi cells.
        if (len(indices) + 1) > (0.02 * (len(Hk) + 1)):
            hotspoth = list()
            for i in indices:
                hotspoth = hotspoth + dict_voronoi[Hk[i]]

            final_hotspots.append(hotspoth)

    return final_hotspots
