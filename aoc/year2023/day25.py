# 2023-25
# finale - let's gooo
import logging
import networkx as nx
import matplotlib.pyplot as plt

log = logging.getLogger("aoc_logger")


def parse_data(in_data):
    nodes = list()
    edges = list()
    for line in in_data.splitlines():
        node, others_s = line.strip().split(": ")
        others = others_s.split(" ")
        nodes.append(node)
        edges += [(node, other) for other in others]
    return nodes, edges


def part1(in_data, test=False):
    # this is begging to be cheesed
    nodes, edges = parse_data(in_data)
    g = nx.Graph()
    g.add_nodes_from(nodes)
    g.add_edges_from(edges)
    log.info(g)
    # draw that graph, the edges to be cut should stick out
    # nx.draw(g, with_labels=True, node_color="silver", node_size=700)
    # plt.show()
    erase = list()
    # erase edges in both directions
    if test:
        erase = [
            ("jqt", "nvd"),
            ("bvb", "cmg"),
            ("hfx", "pzl"),
            ("nvd", "jqt"),
            ("cmg", "bvb"),
            ("pzl", "hfx"),
        ]
    else:
        erase = [
            ("grd", "hvm"),
            ("jmn", "zfk"),
            ("pmn", "kdc"),
            ("hvm", "grd"),
            ("zfk", "jmn"),
            ("kdc", "pmn"),
        ]
    log.debug(erase)
    new_edges = [e for e in edges if e not in erase]
    new_g = nx.Graph()
    new_g.add_nodes_from(nodes)
    new_g.add_edges_from(new_edges)
    # visual check - there should be two distinct groups (components)
    # nx.draw(new_g, with_labels=True, node_color="silver", node_size=700)
    # plt.show()
    comps = [comp for comp in nx.connected_components(new_g)] # count the components in both graphs
    # Can be done by BFS as well
    log.debug(comps)
    return len(comps[0]) * len(comps[1])


def part2(in_data):
    # there's no part2 - only a star count check
    return "Push that button already!"
