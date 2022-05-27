import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
from difflib import SequenceMatcher
from pyvis.network import Network

nodes = {}
edges = {}
names = ['0']
colors = ['0']
name_col = {}
dff = None
G = None


class Node:
    def __init__(self, station_num):
        self.station_num = station_num
        self.station_name = None
        self.connections = []


class Edge:
    def __init__(self, one, two, dist):
        self.one = one
        self.two = two
        self.distance = dist


def create_nodes():
    global nodes, edges
    with open('node_values_new.txt') as file:
        fs = file.readlines()
        for i in fs:
            p = i.split()
            no = Node(int(p[1]))
            for j in range(2, len(p), 2):
                ed = Edge(int(p[j]), no.station_num, p[j + 1])
                edges[(int(p[j]), no.station_num)] = ed
                no.connections.append(ed)
            nodes[no.station_num] = no


def get_node_names():
    global names
    with open('stationcodes.txt') as file:
        names += file.readlines()
        names = [i.lower().strip('\n') for i in names]


def get_colors():
    global colors
    with open('stationcolorcodes.txt') as file:
        colors += file.readlines()
        colors = [i.lower().strip('\n') for i in colors]


def create_dataframe():
    vals = []
    global dff
    for i, j in edges.items():
        val = {}
        val['one'] = names[i[0]]
        val['two'] = names[i[1]]
        val['distance'] = float(j.distance)
        vals.append(val)
    dff = pd.DataFrame(vals)


def mapping_nodes_to_colors():
    global name_col
    for i in range(1, 249):
        name_col[names[i]] = colors[i]


def create_graph():
    plt.figure(3, figsize=(13, 13))
    nx.draw_kamada_kawai(G, node_color=[name_col[i] for i in G.nodes], with_labels=True)
    plt.show()
    net = Network(height='1500px', width='100%', bgcolor='#222222', font_color='white')
    net.from_nx(G)
    for i in net.nodes:
        i['color'] = name_col[i['id']]
    net.show("example.html")


def fuzzy_match(val):
    curr_max = float('-inf')
    curr_name = None
    for i in names:
        if SequenceMatcher(a=i,b=val).ratio() > 0.95 and SequenceMatcher(a=i,b=val).ratio() > curr_max:
            curr_name = i
    return curr_name


def get_path(fro,too):
    fuzzy_match(fro)
    path = nx.shortest_path(G, fuzzy_match(fro), fuzzy_match(too))
    ans = ['Get on ' + name_col[path[0]] + ' line at ' + path[0]]
    for i in range(1, len(path)):
        if i == len(path) - 1:
            ans.append('Drop at ' + path[i])
            break
        if name_col[path[i]] != name_col[path[i - 1]]:
            ans.append('Switch to ' + name_col[path[i]] + ' line at ' + path[i])
        else:
            ans.append(path[i])
    print(ans)
    return ans


def final(one, two):
    global G
    create_nodes()
    get_node_names()
    get_colors()
    mapping_nodes_to_colors()
    create_dataframe()
    G = nx.from_pandas_edgelist(dff, source='one', target='two', edge_attr='distance')
    create_graph()
    return get_path(one, two)


# final('noida sector 16', 'hauz khas')






