# 2025-08

import logging
from aoc_lib.vector3d import *

log = logging.getLogger("aoc_logger")


def parse_data(in_data):
    data = list()
    for line in in_data.splitlines():
        a, b, c = line.strip().split(",")
        data.append(Point3d(int(a), int(b), int(c)))
    distances = list()
    for i in range(len(data)):
        for j in range(i):
            distances.append((data[i], data[j], distance(data[i], data[j])))
    distances.sort(key=lambda x: x[2])
    return data, distances


def connect(a, b, circuits, circuit_index, circuit_map):
    if a not in circuit_map and b not in circuit_map:
        circuit_index += 1
        c_i = circuit_index
        circuit_map[a] = c_i
        circuit_map[b] = c_i
        circuits[c_i] = {a, b}
    elif a in circuit_map and b not in circuit_map:
        c_i = circuit_map[a]
        circuit_map[b] = c_i
        circuits[c_i].add(b)
    elif b in circuit_map and a not in circuit_map:
        c_i = circuit_map[b]
        circuit_map[a] = c_i
        circuits[c_i].add(a)
    elif a in circuit_map and b in circuit_map:
        log.debug("joining")
        c_i_1 = circuit_map[a]
        c_i_2 = circuit_map[b]
        if c_i_1 != c_i_2:
            circuits[c_i_1] = circuits[c_i_1].union(circuits[c_i_2])
            for x in circuits[c_i_2]:
                circuit_map[x] = c_i_1
            del circuits[c_i_2]
    return circuit_index


def part1(in_data, test=False):
    connections = 1000
    if test:
        connections = 10
    data, distances = parse_data(in_data)
    circuits = dict()
    circuit_index = 0
    circuit_map = dict()
    for i in range(connections):
        a, b, dist = distances[i]
        circuit_index = connect(a, b, circuits, circuit_index, circuit_map)
    counts = sorted([len(v) for k, v in circuits.items()], reverse=True)
    log.debug(circuits)
    return counts[0] * counts[1] * counts[2]


def part2(in_data, test=False):
    data = parse_data(in_data)
    data, distances = parse_data(in_data)
    circuits = dict()
    circuit_index = 0
    circuit_map = dict()
    i = 0
    while len(circuits.keys()) != 1 or len(circuit_map.keys()) != len(data):
        a, b, dist = distances[i]
        circuit_index = connect(a, b, circuits, circuit_index, circuit_map)
        i += 1
    return a[0] * b[0]
