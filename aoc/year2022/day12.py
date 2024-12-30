# 2022-12

import logging
from aoc_lib.map2d import Map2d
import networkx as nx

log = logging.getLogger("aoc_logger")


def parse_data(in_data):
    map2d = Map2d.from_lines(in_data)
    g = nx.DiGraph()
    start, end = (0, 0)
    for i in range(len(map2d.obstacle_str)):
        if map2d.get_index(i) == "S":
            log.debug("start")
            map2d.set_index(i, "a")
            start = i
        elif map2d.get_index(i) == "E":
            log.debug("end")
            map2d.set_index(i, "z")
            end = i
        g.add_node(i, altitude=map2d.get_index(i))
    for i in range(len(map2d.obstacle_str)):
        for j in map2d.nearby_indexes(i):
            if ord(map2d.get_index(j)) - ord(map2d.get_index(i)) <= 1:
                g.add_edge(i, j)
    return g, start, end


def part1(in_data, test=False):
    g, start, end = parse_data(in_data)
    return nx.shortest_path_length(g, start, end)


def part2(in_data, test=False):
    g, start, end = parse_data(in_data)
    bottom = [p for p, d in g.nodes(data=True) if d["altitude"] == "a"]
    lengths = list()
    for x in bottom:
        try:
            l = nx.shortest_path_length(g, x, end)
            lengths.append(l)
        except nx.NetworkXNoPath as e:
            pass
    return min(lengths)
