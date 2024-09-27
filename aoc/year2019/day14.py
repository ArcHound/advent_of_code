# 2019-14
import logging
import networkx as nx
import matplotlib.pyplot as plt
from collections import deque, defaultdict
import math

log = logging.getLogger("aoc_logger")


def parse_data(in_data):
    cookbook = dict()
    g = nx.DiGraph()
    nodes = list()
    for line in in_data.splitlines():
        ingredients, result = line.split(" => ")
        r_q, r_prod = result.split(" ")
        nodes.append(r_prod)
        cookbook[r_prod] = {
            "quantity": int(r_q),
            "recipe": [
                (x.split(" ")[1], int(x.split(" ")[0])) for x in ingredients.split(", ")
            ],
        }
    for node in nodes:
        g.add_node(node)
    for k, v in cookbook.items():
        for a, b in v["recipe"]:
            g.add_edge(a, k)
    return cookbook, g


def part1(in_data, test=False):
    cookbook, G = parse_data(in_data)
    log.debug(cookbook)
    log.debug(G)
    # pos = nx.spring_layout(G)
    # nx.draw(G, pos=pos)
    # nx.draw_networkx_labels(G, pos=pos)
    # plt.show()
    sort_order = list(nx.lexicographical_topological_sort(G))
    sort_order.reverse()
    log.debug(sort_order)
    need_to_make = defaultdict(int)
    need_to_make["FUEL"] = 1
    warehouse = defaultdict(int)
    while sum([need_to_make[x] for x in sort_order if x != "ORE"]) > 0:
        making = ""
        for i in sort_order:
            if need_to_make[i] > 0:
                making = i
                break
        target_q = need_to_make[making] - warehouse[making]
        need_to_make[making] = 0
        warehouse[making] = 0
        recipe = cookbook[making]["recipe"]
        quantity = cookbook[making]["quantity"]
        recipe_count = math.ceil(1.0 * target_q / quantity)
        warehouse[making] = recipe_count * quantity - target_q
        for r in recipe:
            need_to_make[r[0]] += recipe_count * r[1]
        log.debug(need_to_make)
    return need_to_make["ORE"]


def part2(in_data, test=False):
    cookbook, G = parse_data(in_data)
    log.debug(cookbook)
    log.debug(G)
    # pos = nx.spring_layout(G)
    # nx.draw(G, pos=pos)
    # nx.draw_networkx_labels(G, pos=pos)
    # plt.show()
    sort_order = list(nx.lexicographical_topological_sort(G))
    sort_order.reverse()
    log.debug(sort_order)
    need_to_make = defaultdict(int)
    warehouse = defaultdict(int)
    fuel_counter = 0
    while need_to_make["ORE"] < 1000000000000:
        need_to_make["FUEL"] = 1
        while sum([need_to_make[x] for x in sort_order if x != "ORE"]) > 0:
            making = ""
            for i in sort_order:
                if need_to_make[i] > 0:
                    making = i
                    break
            target_q = need_to_make[making] - warehouse[making]
            need_to_make[making] = 0
            warehouse[making] = 0
            recipe = cookbook[making]["recipe"]
            quantity = cookbook[making]["quantity"]
            recipe_count = math.ceil(1.0 * target_q / quantity)
            warehouse[making] = recipe_count * quantity - target_q
            for r in recipe:
                need_to_make[r[0]] += recipe_count * r[1]
        fuel_counter += 1
    return fuel_counter - 1
