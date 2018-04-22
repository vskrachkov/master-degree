import csv
import random
import itertools
import networkx as nx
import matplotlib.pyplot as plt
import time

from copy import copy

MAX_EDGE_WEIGHT = 25
MIN_EDGE_WEIGHT = 12


def create_complete_graph(n=1):
    graph = nx.Graph()
    nodes = range(n)

    # create nodes
    for node in nodes:
        graph.add_node(node, **{'attr': 122})

    # create edges
    for edge in itertools.permutations(nodes, 2):
        graph.add_edge(*edge, weight=random.randint(MIN_EDGE_WEIGHT,
                                                    MAX_EDGE_WEIGHT))

    return graph


def plot_weighted_graph(graph):
    pos = nx.spring_layout(graph)
    nx.draw(graph, pos)
    labels = nx.get_edge_attributes(graph, 'weight')
    nx.draw_networkx_edge_labels(graph, pos, edge_labels=labels)
    plt.show()


class Graph(nx.Graph):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @classmethod
    def create_complete(cls, n):
        return cls(create_complete_graph(n=n))

    @classmethod
    def load_from_file(cls, file_path):
        return nx.read_gpickle(file_path)

    def dump_to_file(self):
        file_name = f'accets/graphs/{time.time()}.gz'
        nx.write_gpickle(self, file_name)
        return file_name

    @classmethod
    def initialize_complete_graph(cls, csv_file_path):
        f = open(csv_file_path)
        rows = csv.reader(f)
        _G = cls()

        for row in rows:
            _G.add_node(row[0])

        for edge in itertools.permutations(_G.nodes, 2):
            _G.add_edge(*edge)

        f.close()
        return _G

    def load_own_attrs(self, csv_file_path):
        f = open(csv_file_path)
        rows = csv.reader(f, delimiter=',')
        id_col, *head_row = next(rows)
        for row in rows:
            n = row[0]
            for i, *attrs in enumerate(row[1:]):
                edges = [(n, neighbor) for neighbor in self.neighbors(n)]
                for attr in attrs:
                    for e in edges:
                        self.edges[e][head_row[i]] = attr
        f.close()

    def load_relative_properties(self, csv_file_path):
        f = open(csv_file_path)
        rows = csv.reader(f, delimiter=',')
        id_col1, id_col2, *head_row = next(rows)
        for row in rows:
            from_n, to_n = row[0], row[1]
            for i, *attrs in enumerate(row[2:]):
                for attr in attrs:
                    self.edges[(from_n, to_n)] [head_row[i]] = attr
                    self.edges[(to_n, from_n)] [head_row[i]] = attr
        f.close()

    def show_on_plot(self):
        pos = nx.spring_layout(self)
        nx.draw(self, pos)
        labels = nx.get_edge_attributes(self, '__weight__')
        nx.draw_networkx_edge_labels(self, pos, edge_labels=labels)
        plt.show()

    def calc_weight(self):
        for e in self.edges:
            attrs = copy(self.edges[e])
            attrs.pop('__weight__', None)
            weight = sum([int(a) for a in attrs.values()]) if attrs else 0
            self.edges[e]['__weight__'] = weight


if __name__ == '__main__':
    # G = Graph.create_complete(n=5)
    G = Graph.initialize_complete_graph('accets/csv/machine_list.csv')
    G.load_own_attrs('accets/csv/own_attrs.csv')
    G.load_relative_properties('accets/csv/related_attrs.csv')
    G.calc_weight()

    # path = G.dump_to_file()
    # G = Graph.load_from_file(path)
    G.show_on_plot()
