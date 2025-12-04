# 2015-13

import logging
import re
import networkx as nx
from itertools import combinations, permutations

log = logging.getLogger("aoc_logger")

ex_pattern = "(?P<one>[A-Z][a-z]*) would (?P<sign>(gain|lose)) (?P<num>[0-9]*) happiness units by sitting next to (?P<two>[A-Z][a-z]*)."


def parse_data(in_data):
    data = dict()
    G = nx.Graph()
    for line in in_data.splitlines():
        match = re.search(ex_pattern, line.strip())
        one = match.group("one")
        two = match.group("two")
        sign = 1 if match.group("sign") == "gain" else -1
        val = sign * int(match.group("num"))
        data[(one, two)] = (one, two, val)
    people = set([x[0] for x in data])
    for a, b in combinations(people, 2):
        G.add_edge(a, b, weight=data[(a, b)][2] + data[(b, a)][2])
    return G


def brute_force(G):
    cache = dict()
    nodes = list(G.nodes())
    for i in range(2, len(nodes) + 1):
        for p in permutations(nodes, i):
            if len(p) == 2:
                cache[p] = G[p[0]][p[1]]["weight"]
            else:
                cache[p] = G[p[0]][p[1]]["weight"] + cache[p[1:]]
    return cache


def part1(in_data, test=False):
    G = parse_data(in_data)
    log.debug(G.edges(data=True))
    cache = brute_force(G)
    # it's the same brute force for finding a path.
    # just add the last step to complete the circle
    return max(
        [
            cache[x] + G[x[0]][x[-1]]["weight"]
            for x in cache
            if len(x) == len(list(G.nodes))
        ]
    )


def part2(in_data, test=False):
    if test:
        return "part2 output 2015-13"
    G = parse_data(in_data)
    log.debug(G.edges(data=True))
    cache = brute_force(G)
    # this one is actually easier as we don't need to complete the circle since our vals are 0
    return max([cache[x] for x in cache if len(x) == len(list(G.nodes))])
