# 2020-16

import logging
from aoc_lib.interval import Interval
from z3 import *

log = logging.getLogger("aoc_logger")


def parse_data(in_data):
    nearby = list()
    ticket = list()
    state = "params"  # "your", "nearby"
    params = dict()
    for line in in_data.splitlines():
        if line.strip() == "":
            continue
        elif line.strip() == "your ticket:":
            state = "your"
        elif line.strip() == "nearby tickets:":
            state = "nearby"
        elif state == "params":
            key, val = line.strip().split(": ")
            f, s = val.split(" or ")
            params[key] = (
                Interval(int(f.split("-")[0]), int(f.split("-")[1]) + 1, key),
                Interval(int(s.split("-")[0]), int(s.split("-")[1]) + 1, key),
            )
        elif state == "your":
            ticket = [int(x) for x in line.strip().split(",")]
        elif state == "nearby":
            nearby.append([int(x) for x in line.strip().split(",")])
    return params, ticket, nearby


def part1(in_data, test=False):
    params, ticket, nearby = parse_data(in_data)
    ints = list()
    invalid_values = list()
    for key in params:
        ints.append(params[key][0])
        ints.append(params[key][1])
    for t in nearby:
        for v in t:
            valid = False
            for interval in ints:
                if interval.contains_val(v):
                    valid = True
                    break
            if not valid:
                invalid_values.append(v)
    return sum(invalid_values)


def part2(in_data, test=False):
    params, ticket, nearby = parse_data(in_data)
    ints = list()
    invalid_values = list()
    for key in params:
        ints.append(params[key][0])
        ints.append(params[key][1])
    labels = list({x.label for x in ints})
    valid_tickets = list()
    for t in nearby:
        valid_ticket = True
        for v in t:
            valid = False
            for interval in ints:
                if interval.contains_val(v):
                    valid = True
                    break
            if not valid:
                valid_ticket = False
                break
        if valid_ticket:
            valid_tickets.append(t)
    log.debug(labels)
    possible_fields = [set(labels) for i in range(len(ticket))]
    for t in valid_tickets:
        for i in range(len(t)):
            v = t[i]
            notes = set()
            for interval in ints:
                if interval.contains_val(v):
                    notes.add(interval.label)
            new_set = set()
            for l in labels:
                if l in notes and l in possible_fields[i]:
                    new_set.add(l)
            possible_fields[i] = new_set
    variables = [Int(f"x_{i}") for i in range(len(labels))]
    rang = [And(0 <= x, x <= len(labels)) for x in variables]
    uniq = [Distinct(variables)]  # each var should have unique label
    poss = list()
    for i in range(len(labels)):
        poss.append(
            Or(
                [
                    variables[i] == j
                    for j in range(len(labels))
                    if labels[i] in possible_fields[j]
                ]
            )
        )
    s = Solver()
    s.add(rang + uniq + poss)
    if s.check() == sat:
        m = s.model()
    else:
        log.error("Failed to solve")
    # let's just assume it's uniq
    dep_indexes = [i for i in range(len(labels)) if "departure" in labels[i]]
    col_map = {i: m[variables[i]].as_long() for i in range(len(labels))}
    nums = [ticket[col_map[i]] for i in dep_indexes]
    prod = 1
    for n in nums:
        prod *= n
    return prod
