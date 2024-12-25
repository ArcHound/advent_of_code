# 2024-23

import logging
import networkx as nx

log = logging.getLogger("aoc_logger")


def parse_data(in_data):
    g = nx.Graph()
    for line in in_data.splitlines():
        u, v = line.strip().split("-")
        g.add_edge(u, v)
    return g


def part1(in_data, test=False):
    g = parse_data(in_data)
    sc = {tuple(x) for x in nx.simple_cycles(g, length_bound=3)}
    log.debug(sc)
    total = 0
    for cycle in sc:
        found = False
        for node in cycle:
            if node.startswith("t") and not found:
                total += 1
                found = True
    return total


def part2(in_data, test=False):
    g = parse_data(in_data)
    clique = [x for x in nx.find_cliques(g)]
    max_len = max([len(x) for x in clique])
    max_c = [x for x in clique if len(x) == max_len][0]
    password = sorted(max_c)
    return ",".join(password)
