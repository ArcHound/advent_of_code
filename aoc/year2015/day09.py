# 2015-09

import re
import networkx as nx
from itertools import chain, combinations, permutations
import logging

log = logging.getLogger("aoc_logger")

extract_pattern = "(?P<from>[^ ]*) to (?P<to>[^ ]*) = (?P<dist>[0-9]*)"


def powerset(iterable, start=0):
    "powerset([1,2,3]) --> () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)"
    s = list(iterable)
    return chain.from_iterable(combinations(s, r) for r in range(start, len(s) + 1))


def parse_data(in_data):
    data = list()
    G = nx.Graph()
    for line in in_data.splitlines():
        match = re.search(extract_pattern, line.strip())
        G.add_edge(
            match.group("from"), match.group("to"), weight=int(match.group("dist"))
        )
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
    cache = brute_force(G)
    return min([cache[x] for x in cache if len(x) == len(list(G.nodes))])


def part2(in_data, test=False):
    G = parse_data(in_data)
    cache = brute_force(G)
    return max([cache[x] for x in cache if len(x) == len(list(G.nodes))])
