# 2015-16

import logging
from dataclasses import dataclass

log = logging.getLogger("aoc_logger")

test_results = """children: 3
cats: 7
samoyeds: 2
pomeranians: 3
akitas: 0
vizslas: 0
goldfish: 5
trees: 3
cars: 2
perfumes: 1
"""


@dataclass
class SueProfile:
    children: int = -1
    cats: int = -1
    samoyeds: int = -1
    pomeranians: int = -1
    akitas: int = -1
    vizslas: int = -1
    goldfish: int = -1
    trees: int = -1
    cars: int = -1
    perfumes: int = -1


main_profile = SueProfile(
    children=3,
    cats=7,
    samoyeds=2,
    pomeranians=3,
    akitas=0,
    vizslas=0,
    goldfish=5,
    trees=3,
    cars=2,
    perfumes=1,
)


def profile_match(sue, main_profile):
    params = [
        "children",
        "cats",
        "samoyeds",
        "pomeranians",
        "akitas",
        "vizslas",
        "goldfish",
        "trees",
        "cars",
        "perfumes",
    ]
    matches = True
    log.debug(sue)
    for p in params:
        if getattr(sue, p) != getattr(main_profile, p) and getattr(sue, p) != -1:
            log.debug(f"{p} is wrong: {getattr(sue, p)} != {getattr(main_profile, p)}")
            matches = False
            break
    return matches


def parse_data(in_data):
    profiles = dict()
    count = 0
    for line in in_data.splitlines():
        count += 1
        parts = ": ".join(line.strip().split(": ")[1:])
        params = {x.split(": ")[0]: int(x.split(": ")[1]) for x in parts.split(", ")}
        profiles[count] = SueProfile(**params)
    return profiles


def part1(in_data, test=False):
    profiles = parse_data(in_data)
    match = 0
    for i in range(len(profiles)):
        if profile_match(profiles[i + 1], main_profile):
            match = i + 1
    return match


def profile_match_2(sue, main_profile):
    params = ["children", "samoyeds", "akitas", "vizslas", "cars", "perfumes"]
    matches = True
    log.debug(sue)
    for p in params:
        if getattr(sue, p) != getattr(main_profile, p) and getattr(sue, p) != -1:
            log.debug(f"{p} is wrong: {getattr(sue, p)} != {getattr(main_profile, p)}")
            matches = False
            break
    for p in ["cats", "trees"]:
        if getattr(sue, p) <= getattr(main_profile, p) and getattr(sue, p) != -1:
            log.debug(f"{p} is wrong: {getattr(sue, p)} >= {getattr(main_profile, p)}")
            matches = False
            break
    for p in ["pomeranians", "goldfish"]:
        if getattr(sue, p) >= getattr(main_profile, p) and getattr(sue, p) != -1:
            log.debug(f"{p} is wrong: {getattr(sue, p)} <= {getattr(main_profile, p)}")
            matches = False
            break
    return matches


def part2(in_data, test=False):
    profiles = parse_data(in_data)
    match = 0
    for i in range(len(profiles)):
        if profile_match_2(profiles[i + 1], main_profile):
            match = i + 1
    return match
