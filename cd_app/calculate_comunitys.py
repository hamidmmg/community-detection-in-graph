import igraph as ig
import networkx as nx
import csv

dictionary = {}


def leiden(file_path):
    with open(file_path) as csvfile:
        reader = csv.reader(csvfile)
        for rows in reader:
            key = str(rows[0])
            value = str(rows[1])
            label = str(rows[2])
            if str(key) in dictionary:
                dictionary[str(key)].append((str(value), label))
            else:
                dictionary[str(key)] = [(str(value), str(label))]
    H = nx.Graph(dictionary)
    h = ig.Graph.from_networkx(H)
    # edge_labels = [l[1] for v, l in H.edges]
    vertex_labels = [u for u, v, l in H.edges(data='label')]
    target = 'images/myfile.svg'
    target2 = 'images/myfile_org.svg'
    communities = h.community_leiden(objective_function='modularity')
    # print(communities)
    # print(len(communities))
    # plot = ig.plot(communities, edge_label=edge_labels, vertex_label=vertex_labels, target=target)
    plot = ig.plot(communities, vertex_label=vertex_labels, target=target)
    plot = ig.plot(h, vertex_label=vertex_labels, target=target2)
    # print(len(communities))
    return communities, len(communities)
