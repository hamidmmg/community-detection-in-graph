import csv
import networkx as nx
import igraph as ig
import numpy as np
import time
from igraph import *


def IC(g, S, p=0.5, mc=1000):
    spread = []
    for i in range(mc):

        # Simulate propagation process
        new_active, A = S[:], S[:]
        while new_active:

            # For each newly active node, find its neighbors that become activated
            new_ones = []
            for node in new_active:
                # Determine neighbors that become infected
                np.random.seed(i)
                success = np.random.uniform(0, 1, len(g.neighbors(node, mode="out"))) < p
                new_ones += list(np.extract(success, g.neighbors(node, mode="out")))

            new_active = list(set(new_ones) - set(A))

            # Add newly activated nodes to the set of activated nodes
            A += new_active

        spread.append(len(A))
    return np.mean(spread)


def greedy(g, k, p=0.1, mc=1000):
    """
    Input:  graph object, number of seed nodes
    Output: optimal seed set, resulting spread, time for each iteration
    """

    S, spread, timelapse, start_time = [], [], [], time.time()

    # Find k nodes with the largest marginal gain
    for _ in range(k):

        # Loop over nodes that are not yet in seed set to find biggest marginal gain
        best_spread = 0
        for j in set(range(g.vcount())) - set(S):

            # Get the spread
            s = IC(g, S + [j], p, mc)

            # Update the winning node and spread so far
            if s > best_spread:
                best_spread, node = s, j

        # Add the selected node to the seed set
        S.append(node)

        # Add estimated spread and elapsed time
        spread.append(best_spread)
        timelapse.append(time.time() - start_time)

    return S, spread, timelapse


def celf(g, k, p=0.1, mc=1000):
    """
    Input:  graph object, number of seed nodes
    Output: optimal seed set, resulting spread, time for each iteration
    """

    # --------------------
    # Find the first node with greedy algorithm
    # --------------------

    # Calculate the first iteration sorted list
    start_time = time.time()
    marg_gain = [IC(g, [node], p, mc) for node in range(g.vcount())]

    # Create the sorted list of nodes and their marginal gain
    Q = sorted(zip(range(g.vcount()), marg_gain), key=lambda x: x[1], reverse=True)

    # Select the first node and remove from candidate list
    S, spread, SPREAD = [Q[0][0]], Q[0][1], [Q[0][1]]
    Q, LOOKUPS, timelapse = Q[1:], [g.vcount()], [time.time() - start_time]

    # --------------------
    # Find the next k-1 nodes using the list-sorting procedure
    # --------------------

    for _ in range(k - 1):

        check, node_lookup = False, 0

        while not check:
            # Count the number of times the spread is computed
            node_lookup += 1

            # Recalculate spread of top node
            current = Q[0][0]

            # Evaluate the spread function and store the marginal gain in the list
            Q[0] = (current, IC(g, S + [current], p, mc) - spread)

            # Re-sort the list
            Q = sorted(Q, key=lambda x: x[1], reverse=True)

            # Check if previous top node stayed on top after the sort
            check = (Q[0][0] == current)

        # Select the next node
        spread += Q[0][1]
        S.append(Q[0][0])
        SPREAD.append(spread)
        LOOKUPS.append(node_lookup)
        timelapse.append(time.time() - start_time)

        # Remove the selected node from the list
        Q = Q[1:]

    return S, SPREAD, timelapse, LOOKUPS


def make_graph_from_data(file_path):
    source = []
    target = []
    nodes = []
    with open(file_path) as csvfile:
        reader = csv.reader(csvfile)
        for rows in reader:
            row = rows
            source.append(row[0])
            target.append(row[1])
            if row[0] not in nodes:
                nodes.append(row[0])
            if row[1] not in nodes:
                nodes.append(row[1])
    g = Graph(directed=True)
    g.add_vertices(nodes)
    g.add_edges(zip(source, target))
    return g


def calculate_best_nodes(file_path):
    # Run algorithms
    g = make_graph_from_data(file_path)
    celf_output = celf(g, 12, p=0.2, mc=600)
    coms = community_have_best_node(file_path, list(celf_output[0]))
    return celf_output[0], coms


def unique(list1):
    # insert the list to the set
    list_set = set(list1)
    # convert the set to the list
    unique_list = (list(list_set))
    return unique_list


def community_have_best_node(file_path, best_nodes):
    best_nodes = best_nodes
    communities = leiden_communities(file_path)
    best_communities = []
    for j in best_nodes:
        for i in range(len(communities)):
            if j in communities[i]:
                best_communities.append(i)
    # ig.Graph.subgraph(communities, communities[0])
    best_communities = unique(best_communities)
    return best_communities


def leiden_communities(file_path):
    dictionary = {}
    with open(file_path) as csvfile:
        reader = csv.reader(csvfile)
        for rows in reader:
            key = str(rows[0])
            value = str(rows[1])
            if str(key) in dictionary:
                dictionary[str(key)].append(str(value))
            else:
                dictionary[str(key)] = [str(value)]
    H = nx.Graph(dictionary)
    h = ig.Graph.from_networkx(H)
    communities = h.community_leiden(objective_function='modularity')
    return communities