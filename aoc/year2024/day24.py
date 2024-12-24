# 2024-24

import logging
import dataclasses
from collections import defaultdict
import networkx as nx
import matplotlib.pyplot as plt

log = logging.getLogger("aoc_logger")


@dataclasses.dataclass
class Gate:
    a: str
    b: str
    op: str
    out: str

    def calc(self, memory):
        if self.op == "AND":
            memory[self.out] = memory[self.a] & memory[self.b]
        elif self.op == "OR":
            memory[self.out] = memory[self.a] | memory[self.b]
        elif self.op == "XOR":
            memory[self.out] = memory[self.a] ^ memory[self.b]


def parse_data(in_data):
    memory = defaultdict(lambda: None)
    rules = list()
    for line in in_data.splitlines():
        if ":" in line:
            a, v = line.strip().split(": ")
            memory[a] = int(v)
        elif "->" in line:
            a, op, b, _, out = line.strip().split(" ")
            rules.append(Gate(a, b, op, out))
    return memory, rules


def calc_all(memory, rules):
    computed = True
    while computed:
        computed = False
        for rule in rules:
            if memory[rule.a] is None or memory[rule.b] is None:
                continue
            if memory[rule.out] is None:
                rule.calc(memory)
                computed = True
    zs = [x for x in memory if x.startswith("z")]
    zs.sort(reverse=True)
    return zs


def part1(in_data, test=False):
    memory, rules = parse_data(in_data)
    zs = calc_all(memory, rules)
    return int("".join([str(memory[z]) for z in zs]), 2)


def part2(in_data, test=False):
    memory, rules = parse_data(in_data)
    g = nx.Graph()
    count = 0
    node_labels = list()
    # for rule in rules:
    #     count += 1
    #     g.add_edge(rule.a, rule.op+str(count))
    #     g.add_edge(rule.b, rule.op+str(count))
    #     g.add_edge(rule.op+str(count), rule.out)
    #     node_labels.append(rule.a)
    #     node_labels.append(rule.b)
    #     node_labels.append(rule.out)
    #     node_labels.append(rule.op+str(count))
    # for i in node_labels:
    #     if i.startswith('x'):
    #         g.nodes[i]["label"] = 'ax'
    #     elif i.startswith('y'):
    #         g.nodes[i]["label"] = 'ay'
    #     elif i.startswith('z'):
    #         g.nodes[i]["label"] = 'z'
    #     elif i[0] in "AOX":
    #         g.nodes[i]["label"] = 'k'+i[:2]
    #     else:
    #         g.nodes[i]["label"] = 'j'
    # pos = nx.multipartite_layout(g, subset_key="label")
    # nx.draw(g, pos, with_labels=True, node_color="silver", node_size=700)
    # plt.show()
    xor_rules = list()
    non_xor_rules = list()
    for rule in rules:
        if rule.out.startswith("z") and rule.op != "XOR" and rule.out != "z45":
            xor_rules.append(rule)
        if (
            not rule.out.startswith("z")
            and not rule.a.startswith("x")
            and not rule.a.startswith("y")
            and rule.op == "XOR"
        ):
            non_xor_rules.append(rule)
    log.error(xor_rules)
    log.error(non_xor_rules)
    fixed_rules = [x for x in rules if x not in xor_rules and x not in non_xor_rules]
    log.error(len(fixed_rules))
    log.error(len(xor_rules))
    log.error(len(rules))
    try_2 = list()
    for rule in rules:
        if rule.op == "XOR":
            if rule.a[0] not in "xy" and rule.b[0] not in "xy" and rule.out[0] != "z":
                try_2.append(rule)
                log.error(f"XOR {rule}")
            if (rule.a[0] in "xy" or rule.b[0] in "xy") and all(
                [x.op != "XOR" for x in rules if rule.out == x.a or rule.out == x.b]
            ):
                try_2.append(rule)
                log.error(f"XOR {rule}")
        if rule.op == "OR":
            if rule.out != "z45" and all(
                [x.op != "AND" for x in rules if rule.out == x.a or rule.out == x.b]
            ):
                try_2.append(rule)
                log.error(f"OR {rule}")
        if rule.op == "AND":
            if any([x.op != "OR" for x in rules if rule.out == x.a or rule.out == x.b]):
                try_2.append(rule)
                log.error(f"AND {rule}")
    log.error(try_2)
    try_1_outs = [x.out for x in xor_rules] + [x.out for x in non_xor_rules]
    try_2_outs = [x.out for x in try_2 if x.a not in ["x00", "y00"]]
    please = ",".join(sorted(set(try_1_outs + try_2_outs)))
    return please
