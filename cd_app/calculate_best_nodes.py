import networkx as nx
import csv
import random
from .calculate_comunitys import leiden


def calculate_best_nodes(file_path, k):
    with open(file_path) as csvfile:
        reader = csv.reader(csvfile)
        edges = [(str(rows[0]), str(rows[1])) for rows in reader]
    g = nx.Graph(edges)
    im_output = influence_maximization(g, k)
    coms, communities, count_of_community = community_have_best_node(file_path, list(im_output[0]))
    return im_output[0], coms, communities, count_of_community


def unique(list1):
    list_set = set(list1)
    unique_list = (list(list_set))
    return unique_list


def community_have_best_node(file_path, best_nodes):
    best_nodes = best_nodes
    communities, count_of_community = leiden(file_path)
    best_communities = []
    for j in best_nodes:
        for i, community in enumerate(communities):
            if int(j) in community:
                best_communities.append(i)
    best_communities = unique(best_communities)
    print(best_communities)
    return best_communities, communities, count_of_community


def influence_maximization(G, k):

    def independent_cascade(G, S, p=0.5):
        visited = {}
        for node in G.nodes():
            visited[node] = False
        for node in S:
            visited[node] = True
        while True:
            activated_nodes = []
            for node in G.nodes():
                if visited[node]:
                    continue
                neighbors = list(G.neighbors(node))
                if any(visited[neighbor] for neighbor in neighbors):
                    activated_nodes.append(node)
            if not activated_nodes:
                break
            for node in activated_nodes:
                visited[node] = True
                for neighbor in G.neighbors(node):
                    if not visited[neighbor] and random.random() < p:
                        visited[neighbor] = True
        return visited
    seeds = set()
    max_influence = 0
    marginals = {}
    for node in G.nodes():
        marginals[node] = 0
    while len(seeds) < k:
        best_node = None
        best_gain = 0
        for node in G.nodes():
            if node in seeds:
                continue
            if marginals[node] == 0:
                activated_nodes = independent_cascade(G, seeds.union({node}))
                marginals[node] = sum(activated_nodes.values()) - max_influence
            if marginals[node] > best_gain:
                best_node = node
                best_gain = marginals[node]
        seeds.add(best_node)
        max_influence += best_gain
    return seeds, max_influence
