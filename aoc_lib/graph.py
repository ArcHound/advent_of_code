import dataclasses


@dataclasses.dataclass
class GraphNode:
    node_id: str
    value: int


@dataclasses.dataclass
class GraphConnection:
    a: str
    b: str
    cost: int = 1


class Graph:
    def __init__(self, connections, nodes=list(), weighted=True, bidirectional=False):
        self.weighted = weighted
        self.bidirectional = bidirectional
        self.connections = list()
        self.nodes = nodes
        for p in connections:
            if p.a not in [g.node_id for g in self.nodes]:
                self.nodes.append(GraphNode(node_id=p.a, value=1))
            if p.b not in [g.node_id for g in self.nodes]:
                self.nodes.append(GraphNode(node_id=p.b, value=1))
            if weighted:
                self.connections.append(p)
            else:
                self.connections.append(GraphConnection(p.a, p.b, 1))
            if bidirectional:
                if weighted:
                    self.connections.append(GraphConnection(p.b, p.a, p.cost))
                else:
                    self.connections.append(GraphConnection(p.b, p.a, 1))
