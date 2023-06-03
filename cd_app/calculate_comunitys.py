import igraph as ig
import networkx as nx
import csv

from unicodedata import numeric

dictionary = {}


def leiden(file_path, best_nodes):
    with open(file_path) as csvfile:
        reader = csv.reader(csvfile)
        for rows in reader:
            key = str(rows[0])
            value = str(rows[1])
            label = str(rows[2])
            if str(key) in dictionary:
                dictionary[str(key)].append((str(value)))
            else:
                dictionary[str(key)] = [(str(value))]
            # if str(key) in dictionary:
            #     dictionary[str(key)].append((str(value), label))
            # else:
            #     dictionary[str(key)] = [(str(value), str(label))]
    H = nx.Graph(dictionary)

    h = ig.Graph(directed=False)
    vertex_list = []
    for node, edges in dictionary.items():
        if node not in vertex_list:
            vertex_list.append(node)

        for edge in edges:
            if edge not in vertex_list:
                vertex_list.append(edge)
    # h.add_vertices(vertex_list)
    for i in vertex_list:
        h.add_vertex(name=i, label=i)
    for node, edges in dictionary.items():
        for edge in edges:
            h.add_edge(node, edge)
    # edge_labels = [l[1] for v, l in H.edges]
    vertex_labels = [u for u, v, l in H.edges(data='label')]
    target = 'images/myfile.svg'
    target2 = 'images/myfile_org.svg'
    target3 = 'images/myfile_subg.svg'
    communities = h.community_leiden(objective_function='modularity')
    # print(vertices)
    int_vertices = []
    for i in best_nodes:
        int_vertices.append(int(i))
    shortest_paths = []
    for i in range(len(int_vertices)):
        for j in range(len(int_vertices)):
            shortest_paths.append(h.get_shortest_paths(int_vertices[i], to=int_vertices[j]))
    path_vertices = set()
    for path in shortest_paths:
        for v in path:
            for p in v:
                path_vertices.add(p)
    subgraph_vertices = int_vertices + list(path_vertices - set(int_vertices))
    subgraphs = h.subgraph(subgraph_vertices)
    ig.plot(h, vertex_label=h.vs['name'], target=target)
    vertex_colors = ['red' if node in int_vertices else 'blue' for node in subgraph_vertices]
    ig.plot(communities, vertex_label=h.vs['name'], target=target2)
    ig.plot(subgraphs, vertex_label=h.vs['name'], vertex_color=vertex_colors, target=target3)
    return communities, len(communities)
