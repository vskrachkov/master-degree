import csv
import random
import itertools
import time
import functools
import copy

import matplotlib.pyplot as plt
import networkx as nx
import pants


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
        self.__max_val_map = {}
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
                    attr = float(attr)
                    for e in edges:
                        self.edges[e][head_row[i]] = attr
                        _p = self.__max_val_map.get(head_row[i])
                        if _p is None or attr > _p:
                            self.__max_val_map[head_row[i]] = attr
        f.close()

    def load_relative_properties(self, csv_file_path):
        f = open(csv_file_path)
        rows = csv.reader(f, delimiter=',')
        id_col1, id_col2, *head_row = next(rows)
        for row in rows:
            from_n, to_n = row[0], row[1]
            for i, *attrs in enumerate(row[2:]):
                for attr in attrs:
                    attr = float(attr)
                    self.edges[(from_n, to_n)] [head_row[i]] = attr
                    self.edges[(to_n, from_n)] [head_row[i]] = attr
                    _p = self.__max_val_map.get(head_row[i])
                    if _p is None or attr > _p:
                        self.__max_val_map[head_row[i]] = attr
        f.close()

    def show_on_plot(self):
        pos = nx.spring_layout(self)
        nx.draw(self, pos)
        labels = nx.get_edge_attributes(self, '__weight__')
        nx.draw_networkx_edge_labels(self, pos, edge_labels=labels)
        nx.draw_networkx_labels(self, pos)
        plt.show()

    def calc_weight(self):
        for e in self.edges:
            attrs = copy.copy(self.edges[e])
            attrs.pop('__weight__', None)
            w = []
            for key, attr in attrs.items():
                w.append(attr / self.__max_val_map[key])
            weight = functools.reduce(lambda x, y: x*y, w)
            self.edges[e]['__weight__'] = round(weight, 3)

    def get_weight(self, start, end):
        return self.edges[(start, end)].get('__weight__')

    def _solve(self):
        world = pants.World(list(self.nodes), self.get_weight)
        solver = pants.Solver()
        return solver, world

    def solutions(self):
        solver, world = self._solve()
        return solver.solutions(world)

    def solution(self):
        solver, world = self._solve()
        return solver.solve(world)


if __name__ == '__main__':
    G = Graph.initialize_complete_graph('accets/csv/machine_list.csv')
    G.load_own_attrs('accets/csv/own_attrs.csv')
    G.load_relative_properties('accets/csv/related_attrs.csv')
    G.calc_weight()

    # path = G.dump_to_file()
    # G = Graph.load_from_file(path)

    print(G.solution().distance)
    for sol in G.solutions():
        print(sol.distance)

    G.show_on_plot()
