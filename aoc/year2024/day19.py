# 2024-19

import logging
from tqdm import tqdm
from collections import deque, defaultdict

log = logging.getLogger("aoc_logger")


def parse_data(in_data):
    towels = list()
    orders = list()
    first = True
    for line in in_data.splitlines():
        if first:
            towels = line.strip().split(", ")
            first = False
        elif len(line.strip()) > 0:
            orders.append(line.strip())
    root = {
        "color": "",
        "w": None,
        "u": None,
        "b": None,
        "r": None,
        "g": None,
        "is_towel": False,
    }
    for t in towels:
        current_node = root
        for color in t:
            if current_node[color] is None:
                current_node[color] = {
                    "color": color,
                    "w": None,
                    "u": None,
                    "b": None,
                    "r": None,
                    "g": None,
                    "is_towel": False,
                }
            current_node = current_node[color]
        current_node["is_towel"] = True
    return towels, root, orders


def part1(in_data, test=False):
    towels, root, orders = parse_data(in_data)
    cache = dict()
    total = 0
    for o in orders:
        possible_orders = list()
        copy_order = str(o)
        to_process = deque()
        to_process.append((copy_order, 0))
        while len(to_process) > 0:
            current_node = root
            order, tokens = to_process.popleft()
            if len(order) == 0:
                possible_orders.append((order, tokens))
                break
            buf = ""
            found_something = False
            for c in order:
                if current_node[c] is None:
                    break
                elif current_node[c]["is_towel"]:
                    found_something = True
                    to_process.append((order[len(buf) + 1 :], tokens + 1))
                buf += c
                current_node = current_node[c]
            temp_dict = dict()
            for i in range(len(to_process)):
                a, b = to_process.popleft()
                if a not in temp_dict or b < temp_dict[a]:
                    temp_dict[a] = b
            for a in temp_dict:
                to_process.append((a, temp_dict[a]))
        if len(possible_orders) > 0:
            total += 1
    return total


def part2(in_data, test=False):
    towels, root, orders = parse_data(in_data)
    total = 0
    for o in tqdm(orders):
        cache = defaultdict(int)
        possible_orders = list()
        copy_order = str(o)
        to_process = deque()
        to_process.append(copy_order)
        cache[copy_order] = 1
        while len(to_process) > 0:
            # log.debug(to_process)
            current_node = root
            order = to_process.popleft()
            if len(order) == 0:
                continue
            buf = ""
            found_something = False
            for c in order:
                if current_node[c] is None:
                    break
                elif current_node[c]["is_towel"]:
                    found_something = True
                    to_process.append(order[len(buf) + 1 :])
                    cache[order[len(buf) + 1 :]] += cache[order]
                buf += c
                current_node = current_node[c]
            temp_dict = dict()
            for i in range(len(to_process)):
                a = to_process.popleft()
                if a not in temp_dict:
                    temp_dict[a] = 1
                else:
                    temp_dict[a] += 1
            for a in temp_dict:
                to_process.append(a)
            to_process = deque(sorted(to_process, key=lambda x: len(x), reverse=True))
        total += cache[""]
    return total
