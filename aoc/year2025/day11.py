# 2025-11

import logging
import networkx as nx
from tqdm import tqdm
import matplotlib.pyplot as plt

log = logging.getLogger("aoc_logger")


def parse_data(in_data):
    data = list()
    G = nx.DiGraph()
    for line in in_data.splitlines():
        f, t = line.strip().split(": ")
        for node in t.split(" "):
            G.add_edge(f, node)
    return G


def part1(in_data, test=False):
    G = parse_data(in_data)
    start = "you"
    end = "out"
    if not nx.has_path(G, start, end):
        raise ValueError(f"No path from {start} to {end}")
    return len([x for x in nx.all_simple_paths(G, start, end)])


def draw_graph(G, start, end, stop_1, stop_2):
    color_map = list()
    for n in G:
        if n == start:
            color_map.append("green")
        elif n == end:
            color_map.append("red")
        elif n in (stop_1, stop_2):
            color_map.append("blue")
        else:
            color_map.append("silver")
    nx.draw(G, with_labels=True, node_color=color_map, node_size=700)
    plt.show()


def part2(in_data, test=False):
    G = parse_data(in_data)
    start = "svr"
    end = "out"
    stop_1 = "fft"
    stop_2 = "dac"
    if not nx.has_path(G, start, end):
        raise ValueError(f"No path from {start} to {end}")
    # sanity checks
    assert nx.is_directed_acyclic_graph(G)
    if stop_2 in nx.ancestors(G, stop_1):
        sw = stop_2
        stop_2 = stop_1
        stop_1 = sw
    anc_1 = nx.ancestors(G, stop_1)
    anc_1.add(stop_1)
    log.info(f"Ancestors {stop_1}: {anc_1}")
    anc_2 = {x for x in nx.ancestors(G, stop_2) if x not in anc_1}
    anc_2.add(stop_1)
    anc_2.add(stop_2)
    log.info(f"Ancestors {stop_2}: {anc_2}")
    anc_3 = {x for x in nx.ancestors(G, end) if x not in anc_1 and x not in anc_2}
    anc_3.add(stop_2)
    anc_3.add(end)
    log.info(f"Ancestors {end}: {anc_3}")
    assert stop_2 not in anc_1
    assert end not in anc_2
    c_1 = len(list(nx.all_simple_paths(G.subgraph(anc_1), start, stop_1)))
    log.info(f"Paths {start}->{stop_1}: {c_1}")
    c_2 = len(list(nx.all_simple_paths(G.subgraph(anc_2), stop_1, stop_2)))
    log.info(f"Paths {stop_1}->{stop_2}: {c_2}")
    c_3 = len(list(nx.all_simple_paths(G.subgraph(anc_3), stop_2, end)))
    log.info(f"Paths {stop_2}->{end}: {c_3}")
    return c_1 * c_2 * c_3
