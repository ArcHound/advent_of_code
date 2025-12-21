# 2020-07

import logging
import networkx as nx

log = logging.getLogger("aoc_logger")


def parse_data(in_data):
    G = nx.DiGraph()
    for line in in_data.splitlines():
        f, t = line.strip()[:-1].split(" contain ")
        from_color = f.split(" ")[0] + " " + f.split(" ")[1]
        for g in t.split(", "):
            tokens = g.split(" ")
            if len(tokens) != 4:
                continue
            value = int(tokens[0])
            to_color = tokens[1] + " " + tokens[2]
            G.add_edge(from_color, to_color, weight=value)
    return G


def part1(in_data, test=False):
    G = parse_data(in_data)
    return len(list(nx.ancestors(G, "shiny gold")))


def recursive_bags(G, color):
    log.debug(f"Examining {color}")
    nb = list(nx.neighbors(G, color))
    log.debug(f"Neighbors {nb}")
    if len(nb) == 0:
        log.debug(f"returning up single")
        return 0
    else:
        total_bags = 0
        for d in nb:
            log.debug(f"Check neighbor {d}")
            log.debug(G[color][d]["weight"])
            total_bags += G[color][d]["weight"] * (recursive_bags(G, d) + 1)
        log.debug(f"returning up {total_bags}")
        return total_bags


def part2(in_data, test=False):
    G = parse_data(in_data)
    log.debug(G.edges)
    return recursive_bags(G, "shiny gold")
