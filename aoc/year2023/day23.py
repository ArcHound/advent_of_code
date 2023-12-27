# 2023-23
import logging
from aoc_lib.map2d import Map2d
from aoc_lib.vector2d import v_add
import networkx as nx
from functools import cache
import matplotlib.pyplot as plt

log = logging.getLogger("aoc_logger")


def parse_data(in_data):
    map2d = Map2d.from_lines(in_data)
    start = None
    end = None
    for x in range(map2d.x_len):
        if map2d.get_obstacle_from_point((x, 0)) == ".":
            start = (x, 0)
            break
    for x in range(map2d.x_len):
        if map2d.get_obstacle_from_point((x, map2d.y_len - 1)) == ".":
            end = (x, map2d.y_len - 1)
            break
    return map2d, start, end


def find_nodes(map2d, starting_point, end_point):
    nodes = [starting_point]
    start_index = map2d.translate_coordinates(starting_point)
    end_index = map2d.translate_coordinates(end_point)
    # basically, we are searching for tiles that have more than two neighbors, those are our nodes
    for i in range(len(map2d.obstacle_str)):
        if i == start_index or i == end_index or map2d.obstacle_str[i] == "#":
            continue
        nearby_points = [
            x
            for x in map2d.nearby_indexes(i)
            if (map2d.in_bounds_index(x) and map2d.obstacle_str[x] != "#")
        ]
        if len(nearby_points) > 2:  # don't need to go to dead ends
            nodes.append(map2d.translate_index(i))
    nodes.append(end_point)
    return nodes


def flood_edges(map2d, nodes, slippery=True):
    slope_dict = {
        ">": (1, 0),
        "<": (-1, 0),
        "^": (0, -1),
        "v": (0, 1),
    }
    edges = list()
    # for each node we travel until we hit another one -> flood
    for node in nodes:
        starting_point = node
        starting_index = map2d.translate_coordinates(starting_point)
        processing = [starting_index]
        map2d.clear_flood()
        map2d.flooded[starting_index] = 0
        while len(processing) > 0:
            process = processing.pop(0)
            process_point = map2d.translate_index(process)
            if process_point in nodes and map2d.flooded[process] != 0:
                edges.append((node, process_point, map2d.flooded[process]))
                continue
            ind = map2d.nearby_indexes(process)
            for p in map2d.nearby_indexes(process):
                if (
                    not map2d.in_bounds_index(p)
                    or map2d.obstacle_str[p] == Map2d.obstacle_sym
                    or map2d.flooded[p] != -1
                ):
                    continue
                elif (
                    slippery # flag to ignore the slopes or not
                    and (map2d.obstacle_str[process] in slope_dict)
                    and v_add(slope_dict[map2d.obstacle_str[process]], process_point)
                    != map2d.translate_index(p)
                ):
                    continue
                map2d.flooded[p] = map2d.flooded[process] + 1
                processing.append(p)
    return edges


def dfs_longest_len(g, start, end):
    if start == end:
        return 0
    else:
        nodes = [node for node in g[0] if node != start]  # remove the start
        edges = [edge for edge in g[1] if start not in edge]  # remove the edges
        new_g = (nodes, edges)
        neighbors = [(edge[1], edge[2]) for edge in g[1] if edge[0] == start]
        max_len = 0
        for node, edge_w in neighbors:
            glen = edge_w + dfs_longest_len(new_g, node, end)
            if glen > max_len:
                max_len = glen
        return max_len


def part1(in_data):
    map2d, start, end = parse_data(in_data)
    nodes = find_nodes(map2d, start, end)
    edges = flood_edges(map2d, nodes, True)
    G = (nodes, edges)
    return dfs_longest_len(G, start, end)  # find that path


def part2(in_data):
    map2d, start, end = parse_data(in_data)
    nodes = find_nodes(map2d, start, end)
    edges = flood_edges(map2d, nodes, False)
    G = (nodes, edges)
    return dfs_longest_len(G, start, end)
