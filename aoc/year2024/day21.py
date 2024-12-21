# 2024-21

import logging
from aoc_lib.map2d import Map2d
from aoc_lib.vector2d import *
import networkx as nx
import matplotlib.pyplot as plt
from functools import cache
from tqdm import tqdm

log = logging.getLogger("aoc_logger")


def parse_data(in_data):
    data = list()
    for line in in_data.splitlines():
        data.append(line)
    return data


numpad_str = """789
456
123
#0A
"""
num_start = (2, 3)

keypad_str = """#^A
<v>
"""
key_start = (2, 0)

dir_map = {(1, 0): ">", (0, 1): "v", (-1, 0): "<", (0, -1): "^"}
edge_map = {">": 100000, "^": 10, "<": 1000, "v": 10000, "A": 100}


def make_graph_from_pad(pad_str):
    # note the symbols on how to transition between the pad buttons
    # it is in this step where we throw out the non-functioning button
    pad = Map2d.from_lines(pad_str)
    g = nx.DiGraph()
    for i in range(len(pad.obstacle_str)):
        if pad.get_index(i) != "#":
            g.add_node(pad.get_index(i))
    for i in range(len(pad.obstacle_str)):
        if pad.get_index(i) != "#":
            for j in pad.nearby_indexes(i):
                if pad.get_index(j) != "#":
                    diff = v_diff(pad.translate_index(j), pad.translate_index(i))
                    g.add_edge(
                        pad.get_index(i),
                        pad.get_index(j),
                        sym=dir_map[diff],
                        weight=edge_map[dir_map[diff]],
                    )
    return g


def make_str_connections(g, pad_str):
    # now we use that graph to create a dictionary
    # it contains all tuples of buttons and all the different shortest paths we can take
    paths = {
        (pad_str[i], pad_str[j]): [
            x for x in nx.all_shortest_paths(g, pad_str[i], pad_str[j])
        ]
        for i in range(len(pad_str))
        for j in range(len(pad_str))
        if i != j
    }
    syms = nx.get_edge_attributes(g, "sym")
    paths_sym = dict()
    for edge in paths:
        paths_sym[edge] = list()
        for path in paths[edge]:
            buf = ""
            for j in range(1, len(path)):
                n1 = path[j - 1]
                n2 = path[j]
                buf += syms[(n1, n2)]
            buf += "A"
            paths_sym[edge].append(buf)
    return paths_sym


def graphs_and_maps():
    # make the above happen for both pads
    num_g = make_graph_from_pad(numpad_str)
    key_g = make_graph_from_pad(keypad_str)
    num_str = "0123456789A"
    num_paths_sym = make_str_connections(num_g, num_str)
    key_str = "<>v^A"
    key_paths_sym = make_str_connections(key_g, key_str)
    return num_g, key_g, num_paths_sym, key_paths_sym


def translate_str(in_str, paths_sym):
    # get instructions for the string and pad
    options = list()
    old_options = list()
    options_options = list()
    # we start in A
    for i in range(0, len(in_str)):
        if i == 0:
            a1 = "A"
        else:
            a1 = in_str[i - 1]
        a2 = in_str[i]
        if a1 == a2:
            # I maybe could have avoided this if I included x<--"A"-->x edges in graph
            # but I don't like those
            options_options.append(["A"])
        else:
            # don't forget to copy, or you'll destroy your dict!
            options_options.append(list(paths_sym[(a1, a2)]))
    # we have all possibilities in each part, now we need to "multiply" them together
    for op in options_options:
        old_options = options
        options = list()
        if len(old_options) > 0:
            for i in range(len(old_options)):
                o = old_options.pop()
                for j in op:
                    x = str(o) + j
                    options.append(x)
        else:
            options = op
    # reduce - we only want the shortest options
    min_len = min([len(o) for o in options])
    final_options = {o for o in options if len(o) == min_len}
    return list(final_options)


# yay, global constants - need that to use the cache decorator below
num_g, key_g, num_paths_sym, key_paths_sym = graphs_and_maps()


@cache
def find_shortest_input_len(in_str, iterations):
    if iterations == 0:
        return len(in_str)
    else:
        # key observation is that "A" resets the robot.
        # So we can only process the small bits up to "A" - much more manageable than the looong strings
        return min(
            [
                sum(
                    [
                        find_shortest_input_len(y + "A", iterations - 1)
                        for y in x.split("A")[:-1]
                    ]
                )
                for x in translate_str(in_str, key_paths_sym)
            ]
        )


def part1(in_data, test=False):
    data = parse_data(in_data)
    total = 0
    for line in data:
        a = min([find_shortest_input_len(x, 2) for x in first])
        total += int(line.strip()[:-1]) * a
    return total


def part2(in_data, test=False):
    data = parse_data(in_data)
    total = 0
    for line in data:
        # translate from numpad
        first = translate_str(line.strip(), num_paths_sym)
        # gogogogo
        a = min([find_shortest_input_len(x, 25) for x in first])
        total += int(line.strip()[:-1]) * a
    return total
