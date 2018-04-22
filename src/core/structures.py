import typing as t

from . import exceptions as exc


class Node(object):
    @classmethod
    def load(cls, serialized_node):
        raise NotImplementedError

    def dump(self):
        raise NotImplementedError()


class FlatNode(Node):
    name: str = None

    @classmethod
    def load(cls, serialized_node: str):
        if not isinstance(serialized_node, str):
            raise exc.InvalidType(f'{cls.__class__} takes only string '
                                  f'as parameter for `load` method')
        instance = cls()
        instance.name = serialized_node
        return instance

    def dump(self) -> str:
        return self.name


class ListNode(Node):
    _nodes: list = []

    @classmethod
    def load(cls, serialized_node: list):
        if not isinstance(serialized_node, list):
            raise exc.InvalidType(f'{cls.__class__} takes only list '
                                  f'as parameter for `load` method')
        instance = cls()
        instance._nodes = serialized_node
        return instance

    def dump(self) -> list:
        return self._nodes

    def items(self) -> list:
        return self._nodes


class NestedNode(FlatNode, ListNode):
    _root: FlatNode

    @classmethod
    def load(cls, serialized_node: dict):
        pass

    def dump(self) -> dict:
        return {
            self.name: self._nodes
        }

    def root(self) -> FlatNode:
        return self._root


class Vertex(object):
    #: map of the another vertexes to which current one is connected
    #: key -> another vertex ID,
    #: value -> weight of the edge which connects the vertex with neighbor
    _connected_to = {}

    def __init__(self, vertex_id):
        self._id = vertex_id

    def id(self):
        """Returns vertex ID."""
        return self._id

    def add_neighbor(self, neighbor_id, weight):
        """Connects neighbor vertex with taken `neighbor_id` to current one
        by edge with taken `weight`.
        """
        self._connected_to[neighbor_id] = weight

    def get_weight(self, neighbor_id):
        """Returns weight of the edge which connects current vertex
        with taken neighbor.
        """
        return self._connected_to.get(neighbor_id)

    def get_connections(self):
        """Returns map of the current connections with neighbor vertexes.
        key -> another vertex ID
        value -> weight of the edge which connects the vertex with neighbor
        """
        return self._connected_to


class Graph(object):
    #: (injectable property) class which will be used for creating vertexes
    #: and manipulation with them.
    vertex_class = None

    #: dict for storing graph vertexes
    __vertex_map = {}

    def create_complete(self, vertex_ids):
        pass
