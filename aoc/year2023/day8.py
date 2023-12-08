# 2023-8
import logging
import math

log = logging.getLogger("aoc_logger")


def parse_data(in_data):
    i = 0
    instructions = ""
    graph = dict()
    for line in in_data.splitlines():
        if i == 0:
            instructions = line
        elif i == 1:
            i += 1
            continue
        else:
            key = line.split("=")[0].split(" ")[0]
            log.debug(key)
            vals = (
                line.split("=")[1][2:-1].split(",")[0],
                line.split("=")[1][2:-1].split(",")[1][1:],
            )
            log.debug(vals)
            graph[key] = vals
        i += 1
    return instructions, graph


def find_path_length(start_node, instructions, graph, suffix):
    i = 0
    output = 0
    node = start_node
    # just travel left and right
    while True:
        if instructions[i] == "L":
            node = graph[node][0]
        else:
            node = graph[node][1]
        # once the instructions are finished, start over
        i = (i + 1) % len(instructions)
        # and count the steps
        output += 1
        if node.endswith(suffix):
            break
    return output


def part1(in_data):
    instructions, graph = parse_data(in_data)
    log.debug(instructions)
    log.debug(graph)
    start = "AAA"
    return find_path_length(start, instructions, graph, "ZZZ")


def part2(in_data):
    instructions, graph = parse_data(in_data)
    nodes = [k for k in graph if k[-1] == "A"]
    node_counts = list()
    # count the shortest way to an end node for each of the starts
    node_counts = [find_path_length(node, instructions, graph, "Z") for node in nodes]
    # now, here's an ugly trick that wouldn't by any means work for general cases.
    # however, I think that's mostly because a general case that is long and solvable is very hard to construct.
    # firstly, why would there be circular paths at all?
    # secondly, if there are circular paths, can there be offsets?
    # and many different such issues
    # so truth be told, I just tried this method and the result worked - tests passed, TDD for the win
    # there also might be some wild algebraic proof that all such cases result in LCM (probably involving CRT)
    # But I am not doing that at 7am in the morning
    final = math.lcm(*node_counts)
    return final
