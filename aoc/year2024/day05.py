# 2024-05

import logging
from collections import defaultdict
import networkx as nx

log = logging.getLogger("aoc_logger")


def parse_data(in_data):
    breaking_rules = defaultdict(set)
    correct_rules = defaultdict(set)
    to_process = list()
    for line in in_data.splitlines():
        if "|" in line:
            a, b = line.split("|")
            breaking_rules[int(b)].add(int(a))  # turn them around
            correct_rules[int(a)].add(int(b))
        elif "," in line:
            to_process.append([int(x) for x in line.split(",")])
    return breaking_rules, correct_rules, to_process


def is_order_valid(order, breaking_rules):
    valid = True
    for i in range(len(order)):
        if len(set.intersection(set(order[i:]), breaking_rules[order[i]])) > 0:
            valid = False
            break
    return valid


def part1(in_data, test=False):
    rules, _, to_process = parse_data(in_data)
    log.debug(rules)
    log.debug(to_process)
    total = 0
    for order in to_process:
        if is_order_valid(order, rules):
            total += order[(len(order) - 1) // 2]
    return total


def toposort(correct_rules):
    G = nx.DiGraph()
    for a in correct_rules:
        for b in correct_rules[a]:
            G.add_edge(a, b)
    return list(nx.topological_sort(G))


def fix_order(order, correct_rules):
    new_order = list()
    sub_rules = defaultdict(set)
    order_set = set(order)
    for i in order:
        sub_rules[i] = set.intersection(order_set, correct_rules[i])
    toposorted = toposort(sub_rules)
    for i in toposorted:
        if i in order:
            new_order.append(i)
    return new_order


def part2(in_data, test=False):
    breaking_rules, correct_rules, to_process = parse_data(in_data)
    total = 0
    for order in to_process:
        if not is_order_valid(order, breaking_rules):
            log.debug(order)
            new_order = fix_order(order, correct_rules)
            total += new_order[(len(new_order) - 1) // 2]
    return total
