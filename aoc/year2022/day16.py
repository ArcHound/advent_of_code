# 2022-16

import logging
import re
import networkx as nx
from collections import deque, defaultdict
from itertools import combinations

log = logging.getLogger("aoc_logger")


def parse_data(in_data):
    data = list()
    g = nx.Graph()
    node_rates = dict()
    for line in in_data.splitlines():
        match = re.search(
            "Valve (?P<node>[A-Z]+) has flow rate=(?P<rate>[0-9]+); tunnels? leads? to valves? (?P<nodes>([A-Z]+(, )?)*)",
            line,
        )
        node_rates[match["node"]] = int(match["rate"])
        for next_node in match["nodes"].split(", "):
            g.add_edge(match["node"], next_node)
    nx.set_node_attributes(g, node_rates, name="rate")
    return g


def condense_graph(g, rate_dict):
    important_nodes = [x for x in rate_dict if rate_dict[x] > 0] + ["AA"]
    imp_g = nx.Graph()
    for i in range(len(important_nodes)):
        for j in range(len(important_nodes)):
            if i == j:
                continue
            a = important_nodes[i]
            b = important_nodes[j]
            imp_g.add_edge(a, b, weight=nx.shortest_path_length(g, a, b))
    return imp_g


def max_pressure_all_possibilities(g, rate_dict):
    start_node = "AA"
    open_valves = ()
    time = 0
    total_time = 30
    queue = list()
    pressure = 0
    queue.append((start_node, open_valves, time))
    pressure_cache = defaultdict(int)
    pressure_cache[(start_node, open_valves, time)] = 0
    imp_g = condense_graph(g, rate_dict)
    weights = nx.get_edge_attributes(imp_g, "weight")
    new_weights = dict()
    for a, b in weights:
        new_weights[(b, a)] = weights[(a, b)]
        new_weights[(a, b)] = weights[(a, b)]
    weights = new_weights
    log.debug(weights)
    result = 0
    max_time = 0
    while len(queue) > 0:
        node, valves, time = queue.pop(0)
        pressure = pressure_cache[(node, valves, time)]
        increment_pressure = sum([rate_dict[x] for x in rate_dict if x in valves])
        next_minute_pressure = pressure + increment_pressure
        # if node!="AA":
        #     log.error("Inc pressure " + str(increment_pressure))
        # log.debug(next_minute_pressure)
        if time > max_time:
            log.info(time)
            max_time = time
        if time == 30 and result < pressure:
            pressure_cache[node, valves, 30] = pressure
            result = pressure
        if time >= 30:
            continue
        if node not in valves and node != "AA":
            new_valves = valves + (node,)
            new_pressure_inc = sum([rate_dict[x] for x in new_valves])
            if len(new_valves) == len(imp_g.nodes()) - 1:
                total_pressure = (
                    pressure + increment_pressure + (30 - time - 1) * new_pressure_inc
                )
                pressure_cache[node, new_valves, 30] = total_pressure
                if total_pressure > result:
                    result = total_pressure
                continue
        # log.debug([x for x in nx.all_neighbors(g, node)])
        for next_node in nx.all_neighbors(imp_g, node):
            if next_node in valves or next_node == "AA":
                continue
            time_inc = weights[(node, next_node)]
            if node not in valves and node != "AA":
                new_pressure = (
                    pressure + increment_pressure + new_pressure_inc * time_inc
                )
                if (
                    new_pressure
                    >= pressure_cache[(next_node, new_valves, time + 1 + time_inc)]
                ):
                    pressure_cache[(next_node, new_valves, time + 1 + time_inc)] = (
                        pressure + increment_pressure + new_pressure_inc * time_inc
                    )
                    if (next_node, new_valves, time + 1 + time_inc) not in queue:
                        queue.append((next_node, new_valves, time + 1 + time_inc))
            elif node == "AA":
                log.debug(next_node)
                if (next_node, (), time + time_inc) not in queue:
                    pressure_cache[(next_node, (), time + time_inc)] = 0
                    queue.append((next_node, (), time + time_inc))
            # if next_minute_pressure>=pressure_cache[(next_node, valves, time+time_inc)]:
            #     pressure_cache[(next_node, valves, time+time_inc)] = pressure + increment_pressure*time_inc
            #     if (next_node, valves, time+time_inc) not in queue:
            #         queue.append((next_node, valves, time+time_inc))
        queue.sort(key=lambda x: x[2])
        # break
        # log.debug(queue)
    return result


def rate_path(path, imp_g, rate_dict, weights, total_time=30):
    elapsed = 0
    released = 0
    path2 = ("AA",) + path
    for i in range(len(path2) - 1):
        elapsed += weights[path2[i], path2[i + 1]] + 1
        released += (total_time - elapsed) * rate_dict[path2[i + 1]]
    return released


def find_paths_under(g, weights, limit=30):
    start_node = "AA"
    open_valves = ("AA",)
    time = 0
    total_time = limit
    queue = list()
    queue.append((open_valves, time))
    paths = set()
    seen_time = 0
    while len(queue) > 0:
        valves, time = queue.pop(0)
        if time > seen_time:
            log.info(f"At {time} found {len(paths)} paths")
            seen_time = time
        if time > limit:
            continue
        else:
            paths.add(valves[1:])
        for next_node in nx.all_neighbors(g, valves[-1]):
            time_inc = weights[(valves[-1], next_node)]
            if next_node not in valves and time + 1 + time_inc <= limit:
                queue.append((valves + (next_node,), time + 1 + time_inc))
        queue.sort(key=lambda x: x[1])
    return paths


def part1(in_data, test=False):
    log.warning("WARNING! Takes more than an hour to run.")
    g = parse_data(in_data)
    rate_dict = nx.get_node_attributes(g, "rate")
    # result = max_pressure_all_possibilities(g, rate_dict)
    imp_g = condense_graph(g, rate_dict)
    weights = nx.get_edge_attributes(imp_g, "weight")
    log.debug(weights)
    new_weights = dict()
    for a, b in weights:
        new_weights[(b, a)] = weights[(a, b)]
        new_weights[(a, b)] = weights[(a, b)]
    weights = new_weights
    paths = find_paths_under(imp_g, new_weights)
    result = max([rate_path(path, imp_g, rate_dict, new_weights) for path in paths])
    return result


def part2(in_data, test=False):
    g = parse_data(in_data)
    rate_dict = nx.get_node_attributes(g, "rate")
    # result = max_pressure_all_possibilities(g, rate_dict)
    imp_g = condense_graph(g, rate_dict)
    weights = nx.get_edge_attributes(imp_g, "weight")
    log.debug(weights)
    new_weights = dict()
    for a, b in weights:
        new_weights[(b, a)] = weights[(a, b)]
        new_weights[(a, b)] = weights[(a, b)]
    weights = new_weights
    paths = find_paths_under(imp_g, new_weights, 26)
    # log.debug(paths)
    disjoint_paths = [
        (me, elephant)
        for me, elephant in combinations(paths, r=2)
        if set(me).isdisjoint(set(elephant))
    ]
    # log.debug(disjoint_paths)
    maximum = max(
        [
            rate_path(path1, imp_g, rate_dict, new_weights, 26)
            + rate_path(path2, imp_g, rate_dict, new_weights, 26)
            for path1, path2 in disjoint_paths
        ]
    )
    return maximum
