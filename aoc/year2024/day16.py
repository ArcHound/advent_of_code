# 2024-16

import logging
from aoc_lib.map2d import Map2d
from aoc_lib.vector2d import *
import networkx as nx
from networkx.classes.function import path_weight

log = logging.getLogger("aoc_logger")

moves = [(1, 0), (0, 1), (-1, 0), (0, -1)]
moves_map = {(1, 0): 0, (0, 1): 1, (-1, 0): 2, (0, -1): 3}
moves_diff = {(1, 1): 1, (2, 0): 2, (0, 2): 2, (0, 0): 0}


def parse_data(in_data):
    map2d = Map2d.from_lines(in_data)
    start = None
    end = None
    direction = (1, 0)
    for i in range(len(map2d.obstacle_str)):
        if map2d.get_index(i) == "S":
            start = map2d.translate_index(i)
        elif map2d.get_index(i) == "E":
            end = map2d.translate_index(i)
    return map2d, start, direction, end


def build_graph(map2d):
    G = nx.DiGraph()
    for i in range(len(map2d.obstacle_str)):
        p = map2d.translate_index(i)
        for v in moves:
            G.add_node((p, v))
        for j in range(len(moves)):
            for k in range(j):
                G.add_edge(
                    (p, moves[j]),
                    (p, moves[k]),
                    weight=moves_diff[v_abs(v_diff(moves[j], moves[k]))] * 1000,
                )
                G.add_edge(
                    (p, moves[k]),
                    (p, moves[j]),
                    weight=moves_diff[v_abs(v_diff(moves[j], moves[k]))] * 1000,
                )
    for i in range(len(map2d.obstacle_str)):
        p = map2d.translate_index(i)
        for next_p in map2d.nearby_points(p):
            if map2d.get_point(next_p) != "#":
                next_dir = v_diff(next_p, p)
                G.add_edge((p, next_dir), (next_p, next_dir), weight=1)
    return G


def part1(in_data, test=False):
    map2d, start, direction, end = parse_data(in_data)
    G = build_graph(map2d)
    start_node = (start, direction)
    end_nodes = [(end, v) for v in moves]
    return min(
        [
            nx.shortest_path_length(G, start_node, end_node, weight="weight")
            for end_node in end_nodes
        ]
    )


def part2(in_data, test=False):
    map2d, start, direction, end = parse_data(in_data)
    G = build_graph(map2d)
    start_node = (start, direction)
    end_nodes = [(end, v) for v in moves]
    nodes = set()
    best_path_len = min(
        [
            nx.shortest_path_length(G, start_node, end_node, weight="weight")
            for end_node in end_nodes
        ]
    )
    log.debug(f"Best path len: {best_path_len}")
    for e in end_nodes:
        for path in nx.all_shortest_paths(G, start_node, e, weight="weight"):
            if path_weight(G, path, weight="weight") == best_path_len:
                for node in path:
                    nodes.add(node[0])
    for node in nodes:
        map2d.set_point(node, "O")
    log.debug(map2d)
    return len(nodes)
