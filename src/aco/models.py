import uuid
import networkx as nx


class Base(object):
    def get_or_create(self, pk):
        raise NotImplementedError()


class Node(Base):
    def __init__(self, pk=None, **kwargs):
        self._pk = pk if pk else uuid.uuid4()

    @property
    def pk(self):
        return self._pk

    def __repr__(self):
        return f'<Node: {self._pk}>'

    def __str__(self):
        return self.__repr__()

    @classmethod
    def get_or_create(cls, pk: int):
        instance = cls(pk=pk)
        return instance


class Edge(Base):
    def __init__(self, from_node, to_node, **kwargs):
        self._pk = uuid.uuid4()
        self.from_node = from_node
        self.to_node = to_node

    @property
    def pk(self):
        return self._pk

    def __repr__(self):
        return f'<Edge: {self.from_node} --> {self.to_node}>'


class Graph(nx.Graph):
    def __init__(self, *args, **kwargs):
        super(Graph, self).__init__(*args, **kwargs)

    def add_node(self, node_for_adding, **attr):
        """Does the same as the origin method do, but also saves
        node with it's attrs to database.
        """
        super(Graph, self).add_node(node_for_adding, **attr)
        # perform database stuff here

    def add_edge(self, from_node, to_node, **attr):
        """Does the same as the origin method do, but also saves edge
        to database.
        """
        super(Graph, self).add_edge(from_node, to_node, **attr)
