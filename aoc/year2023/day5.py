# 2023-5
import logging
from collections import defaultdict
import dataclasses
import json
from functools import lru_cache
from aoc_lib.interval import Interval
import math

log = logging.getLogger("aoc_logger")

states = [
    "seeds",
    "seed-to-soil",
    "nums",
    "soil-to-fertilizer",
    "nums",
    "fertilizer-to-water",
    "nums",
    "water-to-light",
    "nums",
    "light-to-temperature",
    "nums",
    "temperature-to-humidity",
    "nums",
    "humidity-to-location",
    "nums",
]


def parse_data(in_data):
    state = states[0]
    output = defaultdict(list)
    num_struct = list()
    state_pointer = 0
    for line in in_data.splitlines():
        state = states[state_pointer]
        if state == states[0]:
            output["seeds"] = [
                int(num) for num in line.split(":")[1].split(" ") if num != ""
            ]
            state_pointer += 1
        elif state == "nums":
            if line == "":
                state_pointer += 1
                continue
            num_struct.append(
                {
                    "source": int(line.split(" ")[1]),
                    "target": int(line.split(" ")[0]),
                    "len": int(line.split(" ")[2]),
                }
            )
        elif line.startswith(states[state_pointer]):
            output[states[state_pointer - 2]] = num_struct
            num_struct = list()
            state_pointer += 1
    output[states[state_pointer - 1]] = num_struct
    log.debug(json.dumps(output, indent=2))
    return output


def part1(in_data):
    states = [
        "seed-to-soil",
        "soil-to-fertilizer",
        "fertilizer-to-water",
        "water-to-light",
        "light-to-temperature",
        "temperature-to-humidity",
        "humidity-to-location",
    ]
    data = parse_data(in_data)
    output = dict()
    for seed in data["seeds"]:
        step = seed
        for state in states:
            log.debug(state)
            log.debug(step)
            mapped = False
            for entry in data[state]:
                if step >= entry["source"] and step < entry["source"] + entry["len"]:
                    log.debug(entry)
                    map_i = step - entry["source"]
                    step = entry["target"] + map_i
                    mapped = True
                    break
            if not mapped:
                pass  # nothing to do
            log.debug(step)
            log.debug("-------------")
        output[step] = seed
    log.debug(output)
    return min([k for k in output])


def parse_data2(in_data):
    state = states[0]
    output = defaultdict(list)
    num_struct = list()
    state_pointer = 0
    for line in in_data.splitlines():
        state = states[state_pointer]
        if state == states[0]:
            switch = 0
            start = 0
            rang = 0
            seeds = list()
            for n in [int(num) for num in line.split(":")[1].split(" ") if num != ""]:
                if switch == 0:
                    start = n
                    switch = 1
                elif switch == 1:
                    rang = n
                    switch = 0
                    seeds.append({"start": start, "len": rang})
            state_pointer += 1
            output["seeds"] = seeds
        elif state == "nums":
            if line == "":
                state_pointer += 1
                continue
            num_struct.append(
                {
                    "source": int(line.split(" ")[1]),
                    "target": int(line.split(" ")[0]),
                    "len": int(line.split(" ")[2]),
                }
            )
        elif line.startswith(states[state_pointer]):
            output[states[state_pointer - 2]] = num_struct
            num_struct = list()
            state_pointer += 1
    output[states[state_pointer - 1]] = num_struct
    log.debug(json.dumps(output, indent=2))
    return output


def pass_function(seed, data):
    step = seed
    for state in data:
        mapped = False
        for entry in state:
            if step >= entry[0] and step < entry[0] + entry[1]:
                log.debug(entry)
                map_i = step - entry[0]
                step = entry[2] + map_i
                mapped = True
                break
    return step


def part2(in_data):
    states = [
        "seed-to-soil",
        "soil-to-fertilizer",
        "fertilizer-to-water",
        "water-to-light",
        "light-to-temperature",
        "temperature-to-humidity",
        "humidity-to-location",
    ]
    # states.reverse()
    data = parse_data2(in_data)
    interval_map = dict()
    intervals = list()
    seeds = list()
    for entry in data["seeds"]:
        seeds.append(
            Interval(entry["start"], entry["start"] + entry["len"] - 1, "good")
        )
    n_seeds = Interval.fill_holes(Interval.normalize(seeds))
    log.debug("seeds")
    log.debug(seeds)
    log.debug(n_seeds)

    translated = n_seeds
    for state in states:
        log.debug(state)
        n_source_intervals = Interval.fill_holes(
            Interval.normalize(
                [
                    Interval(entry["source"], entry["source"] + entry["len"] - 1)
                    for entry in data[state]
                ]
            )
        )
        source_intervals = [
            Interval(entry["source"], entry["source"] + entry["len"] - 1)
            for entry in data[state]
        ]
        olaps = Interval.least_common_intervals(translated, n_source_intervals)
        Interval.label_mask(olaps, translated)
        log.debug("translate")
        translated = list()
        for i in olaps:
            accounted = False
            log.debug(f"Checking {i}")
            for s in source_intervals:
                if s.contains(i):
                    log.debug(f"Matches {s}")
                    t = [
                        Interval(entry["target"], entry["target"] + entry["len"] - 1)
                        for entry in data[state]
                        if entry["source"] == s.start
                    ][0]
                    log.debug(f"Translate to {t}")
                    diff = t.start - s.start
                    log.debug(f"diff {diff}")
                    translated.append(Interval(i.start + diff, i.end + diff, i.label))
                    accounted = True
            if not accounted:
                log.debug("Unnacounted")
                translated.append(i)
        log.debug(translated)
        log.debug("-------------------")

    output = min([x.start for x in translated if x.label == "good"])
    return output
