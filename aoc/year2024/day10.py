# 2024-10

import logging
from aoc_lib.map2d import Map2d
import networkx as nx

log = logging.getLogger("aoc_logger")


def parse_data(in_data):
    map2d = Map2d.from_lines(in_data)
    log.debug(map2d.debug_draw())
    G = nx.DiGraph()
    start_nodes = list()
    end_nodes = list()
    for i in range(len(map2d.obstacle_str)):
        G.add_node(i)
    for i in range(len(map2d.obstacle_str)):
        if int(map2d.get_index(i)) == 0:
            start_nodes.append(i)
        elif int(map2d.get_index(i)) == 9:
            end_nodes.append(i)
        for j in map2d.nearby_indexes(i):
            if int(map2d.get_index(j)) - int(map2d.get_index(i)) == 1:
                G.add_edge(i, j)
    return map2d, G, start_nodes, end_nodes


def part1(in_data, test=False):
    map2d, G, start_nodes, end_nodes = parse_data(in_data)
    total = 0
    for s in start_nodes:
        for e in end_nodes:
            if len([p for p in nx.all_simple_paths(G, s, e)]) > 0:
                total += 1
    return total


def part2(in_data, test=False):
    map2d, G, start_nodes, end_nodes = parse_data(in_data)
    total = 0
    for s in start_nodes:
        for e in end_nodes:
            total += len([p for p in nx.all_simple_paths(G, s, e)])
    return total
