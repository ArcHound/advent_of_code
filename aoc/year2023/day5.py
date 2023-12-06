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
    # technique: get all of the data in some dict form
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
            num_struct.append( # could have used a dataclass
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
    # for each seed number
    for seed in data["seeds"]:
        step = seed
        # go through the mappings
        for state in states:
            log.debug(state)
            log.debug(step)
            mapped = False
            # find the applicable interval if it's special
            for entry in data[state]:
                if step >= entry["source"] and step < entry["source"] + entry["len"]:
                    log.debug(entry)
                    map_i = step - entry["source"]
                    step = entry["target"] + map_i
                    mapped = True
                    break
            if not mapped:
                pass  # if not, it's 1:1 - nothing to do
            log.debug(step)
            log.debug("-------------")
        output[step] = seed
    log.debug(output)
    return min([k for k in output]) # minimum key is our answer


def parse_data2(in_data):
    # I know copying and pasting is wrong, but it's fast
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
            # simple state machine to alternate numbers for interpretation
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


def part2(in_data):
    # the issue with the above approach is that it's slow for many seeds, so we're properly working with intervals now
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
    # the intervals that contain seeds are good, intervals without them are bad. 
    for entry in data["seeds"]:
        seeds.append(
            Interval(entry["start"], entry["start"] + entry["len"] - 1, "good")
        )
    # for the alg to work, we need to have a complete partition of the space which is (0,inf)
    n_seeds = Interval.fill_holes(Interval.normalize(seeds))
    log.debug("seeds")
    log.debug(seeds)
    log.debug(n_seeds)

    translated = n_seeds
    # We'll be translating the intervals and keeping track whether the images contain seeds (good intervals)
    for state in states:
        log.debug(state)
        # encompass the full space, fill holes of intervals and extend from 0 to inf 
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
        # we'll have a set of intervals from the previous step noting good and bad intervals and the mapping.
        # the mapping source is a set of intervals too
        # to translate our labeled intervals we need to know which parts are displayed where
        # but it might happen that one interval with labels might be displayed to two disjoint intervals (and other such cases)
        # the idea is to produce a "least common intervals" set:
        # set of intervals that for each element we can decide how it's displayed and whether it's good.
        # surprisingly hard to talk about this, here's a picture:
        # |           Good      | Bad | Good    | Bad       |
        # | maps 1:1 | maps to +x | maps 1:1   | maps to -x | 
        # the least common intervals would return:
        # |          |          | |   |        | |          |
        # so we know that first interval is good and maps 1:1, second is also good and maps to +x, third is bad and maps to +x, fourth is bad and maps 1:1, fifth is good and maps to 1:1, next is good and maps to -x and the rest is bad and maps to -x.
        # then we can just switch the starts and ends of mapped intervals and we've retained the information
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

    # since we know where the seeds are, we are looking for a minimal start of an interval. That's the global minimum as the mappings keep the direction ( (0,5) -> (5,10) never (0,5) -> (10,5) )
    output = min([x.start for x in translated if x.label == "good"])
    return output
