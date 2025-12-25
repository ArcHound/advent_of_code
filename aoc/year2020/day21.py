# 2020-21

import logging

log = logging.getLogger("aoc_logger")


def parse_data(in_data):
    data = list()
    for line in in_data.splitlines():
        l = line.strip()[:-1]
        f, t = l.split(" (contains ")
        data.append((set(f.split(" ")), t.split(", ")))
    allergens = {y for x in data for y in x[1]}
    allergen_map = {x: [y[0] for y in data if x in y[1]] for x in allergens}
    return data, allergens, allergen_map


def get_alergens(data, allergens, allergen_map):
    reduced_map = {x: set.intersection(*allergen_map[x]) for x in allergen_map}
    final_map = dict()
    while len(final_map) < len(allergens):
        for al in reduced_map:
            if len(reduced_map[al]) == 1:
                final_map[al] = list(reduced_map[al])[0]
        for al in reduced_map:
            for x in final_map:
                if final_map[x] in reduced_map[al]:
                    reduced_map[al].remove(final_map[x])
    return final_map


def part1(in_data, test=False):
    data, allergens, allergen_map = parse_data(in_data)
    final_map = get_alergens(data, allergens, allergen_map)
    final_allergens = [v for k, v in final_map.items()]
    total = 0
    for a, n in data:
        for s in a:
            if s not in final_allergens:
                total += 1
    return total


def part2(in_data, test=False):
    data, allergens, allergen_map = parse_data(in_data)
    final_map = get_alergens(data, allergens, allergen_map)
    r = [final_map[x] for x in sorted([k for k in final_map])]
    return ",".join(r)
