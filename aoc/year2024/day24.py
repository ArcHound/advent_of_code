# 2024-24

import logging
import dataclasses
from collections import defaultdict
import networkx as nx

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
    broken_rules = list()
    # the plan - draw an adder with overflow and get some properties
    for rule in rules:
        # xor rules usually end in z
        if rule.op == "XOR":
            if rule.a[0] not in "xy" and rule.b[0] not in "xy" and rule.out[0] != "z":
                broken_rules.append(rule)
            elif (rule.a[0] in "xy" or rule.b[0] in "xy") and all(
                [x.op != "XOR" for x in rules if rule.out == x.a or rule.out == x.b]
            ):
                broken_rules.append(rule)
        # or rules don't end in z (except the last one and first ones)
        if rule.op == "OR":
            if rule.out != "z45" and (
                all(
                    [x.op != "AND" for x in rules if rule.out == x.a or rule.out == x.b]
                )
                or rule.out.startswith("z")
            ):
                broken_rules.append(rule)
        # and rules are not followed by or rules + they don't end in z
        if rule.op == "AND":
            if any(
                [x.op != "OR" for x in rules if rule.out == x.a or rule.out == x.b]
            ) or rule.out.startswith("z"):
                broken_rules.append(rule)
    # fortunately, we don't need to find the correct patching, only to sort those labels
    try_2_outs = [x.out for x in broken_rules if x.a not in ["x00", "y00"]]
    please = ",".join(sorted(try_2_outs))
    return please
