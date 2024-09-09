# 2019-6
import logging
import networkx as nx
import matplotlib.pyplot as plt
import dataclasses

log = logging.getLogger("aoc_logger")


def parse_data(in_data):
    data = list()
    for line in in_data.splitlines():
        a, b = line.split(")")
        data.append((a, b))
    return data


@dataclasses.dataclass(frozen=True)
class Node:
    label: str
    weight: int


def travel_recursive(G, nodes, start, end_label):
    new_start = Node(end_label, start.weight + 1)
    nodes.append(new_start)
    for e in G.adj[end_label]:
        travel_recursive(G, nodes, new_start, e)


def part1(in_data, test=False):
    data = parse_data(in_data)
    starts = [edge[0] for edge in data if edge[0] not in [e[1] for e in data]]
    edges = [(edge[0], edge[1], 1) for edge in data]
    log.debug(edges)
    G = nx.DiGraph()
    for edge in data:
        G.add_weighted_edges_from(edges)
    # nx.draw(G, with_labels=True, node_color="silver", node_size=700)
    # plt.show()
    log.debug(starts)
    nodes = list()
    for start in starts:
        start_node = Node(start, 0)
        for e in G.adj[start]:
            travel_recursive(G, nodes, start_node, e)
    return sum([x.weight for x in nodes])


def part2(in_data, test=False):
    data = parse_data(in_data)
    starts = [edge[0] for edge in data if edge[0] not in [e[1] for e in data]]
    edges = [(edge[0], edge[1], 1) for edge in data]
    log.debug(edges)
    G = nx.Graph()
    for edge in data:
        G.add_weighted_edges_from(edges)
    return len(nx.shortest_path(G, "YOU", "SAN")) - 3  # minus you, santa and one
