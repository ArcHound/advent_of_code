# 2015-07

from dataclasses import dataclass
import networkx as nx
import re

import logging

log = logging.getLogger("aoc_logger")

is_num = re.compile("^[0-9][0-9]*$")


@dataclass
class Node:
    label: str
    op: str
    op_val_l: int = None
    op_val_r: int = None
    op_ref_l: str = None
    op_ref_r: str = None
    value: int = None


def logic_eval(l, r, op):
    prep_l = 0xFFFF & l
    if r is not None:
        prep_r = 0xFFFF & r
    if op == "NOT":
        return 0xFFFF ^ prep_l
    elif op == "ASSIGN":
        return prep_l
    elif op == "AND":
        return prep_l & prep_r
    elif op == "OR":
        return prep_l | prep_r
    elif op == "LSHIFT":
        return 0xFFFF & (prep_l << prep_r)
    elif op == "RSHIFT":
        return 0xFFFF & (prep_l >> prep_r)
    else:
        raise ValueError(f"Invalid op {op}")


def parse_data(in_data):
    G = nx.DiGraph()
    node_map = dict()
    for line in in_data.splitlines():
        l, r = line.split(" -> ")
        to_label = r
        op = None
        from_label_1 = None
        from_label_2 = None
        # parse
        if "NOT" in l:
            op, from_label_1 = l.split(" ")
        elif "AND" in l or "OR" in l or "LSHIFT" in l or "RSHIFT" in l:
            from_label_1, op, from_label_2 = l.split(" ")
        elif " " not in l:
            from_label_1 = l
        else:
            raise ValueError(f"Unknown line format {line}")
        # clean
        op = op if op is not None else "ASSIGN"
        if is_num.match(from_label_1):
            from_label_1 = int(from_label_1)
        if from_label_2 is not None and is_num.match(from_label_2):
            from_label_2 = int(from_label_2)
        # assembly
        node = Node(to_label, op)
        node_map[to_label] = node
        if op in ["ASSIGN", "NOT"]:
            if isinstance(from_label_1, int):
                val = logic_eval(from_label_1, None, op)
                node.value = val
                node.op_val_l = from_label_1
            elif isinstance(from_label_1, str):
                node.op_ref_l = from_label_1
                G.add_edge(from_label_1, to_label)
        elif op in ["AND", "OR", "LSHIFT", "RSHIFT"]:
            if isinstance(from_label_1, int):
                node.op_val_l = from_label_1
            else:
                node.op_ref_l = from_label_1
                G.add_edge(from_label_1, to_label)
            if isinstance(from_label_2, int):
                node.op_val_r = from_label_2
            else:
                node.op_ref_r = from_label_2
                G.add_edge(from_label_2, to_label)
            if node.op_val_l is not None and node.op_val_r is not None:
                val = logic_eval(node.op_val_l, node.op_val_r, op)
    return node_map, G


def graph_eval(node_map, G):
    # it's a good day when I can use toposort
    for node_label in nx.topological_sort(G):
        node = node_map[node_label]
        log.debug(f"Processing {node}")
        lp = (
            node.op_val_l
            if node.op_val_l is not None
            else node_map[node.op_ref_l].value
        )
        log.debug(lp)
        rp = (
            node.op_val_r
            if node.op_val_r is not None
            else node_map.get(node.op_ref_r, Node("", "")).value
        )
        log.debug(rp)
        node.value = logic_eval(lp, rp, node.op)


def part1(in_data, test=False):
    node_map, G = parse_data(in_data)
    graph_eval(node_map, G)
    return node_map["a"].value


def part2(in_data, test=False):
    if test:
        return "part2 output 2015-07"
    node_map, G = parse_data(in_data)
    graph_eval(node_map, G)
    node_map["b"].op_val_l = node_map["a"].value
    graph_eval(node_map, G)
    return node_map["a"].value
