# 2022-21

import logging
import networkx as nx
import dataclasses
import sympy

log = logging.getLogger("aoc_logger")


@dataclasses.dataclass
class Entry:
    a: str = None
    op: str = None
    b: str = None
    val: int = None


def parse_data(in_data):
    node_dict = dict()
    g = nx.DiGraph()
    for line in in_data.splitlines():
        target, val = line.strip().split(": ")
        if " " in val:
            a, op, b = val.split(" ")
            node_dict[target] = Entry(a=a, op=op, b=b)
            g.add_edge(a, target)
            g.add_edge(b, target)
        else:
            node_dict[target] = Entry(val=int(val))
    order = list(nx.topological_sort(g))
    return node_dict, order


def easy_eval(a, b, op):
    if op == "+":
        return a + b
    elif op == "-":
        return a - b
    elif op == "*":
        return a * b
    elif op == "/":
        return a // b
    else:
        log.error(f"Unsupported op {op}")
        return None


def part1(in_data, test=False):
    node_dict, order = parse_data(in_data)
    log.debug(node_dict)
    log.debug(order)
    for entry_key in order:
        entry = node_dict[entry_key]
        if entry.val is None:
            entry.val = easy_eval(
                node_dict[entry.a].val, node_dict[entry.b].val, entry.op
            )
    return node_dict["root"].val


def parse_data2(in_data):
    node_dict = dict()
    me = None
    for line in in_data.splitlines():
        target, val = line.strip().split(": ")
        if " " in val:
            a, op, b = val.split(" ")
            if target == "root":
                op = "="
            node_dict[target] = Entry(a=a, op=op, b=b)
        else:
            if target != "humn":
                node_dict[target] = Entry(val=int(val))
            else:
                node_dict[target] = Entry(val="h")
    return node_dict


def return_thing(node_dict, root):
    if root.val is not None:
        return str(root.val)
    else:
        return f"({return_thing(node_dict, node_dict[root.a])} {root.op} {return_thing(node_dict, node_dict[root.b])})"


def part2(in_data, test=False):
    node_dict = parse_data2(in_data)
    left = node_dict["root"].a
    right = node_dict["root"].b
    log.debug(left)
    left_side = return_thing(node_dict, node_dict[left])
    log.debug(left_side)
    right_side = return_thing(node_dict, node_dict[right])
    log.debug(right_side)
    eq = sympy.sympify(f"Eq({left_side[1:-1]}, {right_side[1:-1]})")
    h = sympy.symbols("h")
    humn = sympy.solveset(eq, h)
    return humn.args[0]
