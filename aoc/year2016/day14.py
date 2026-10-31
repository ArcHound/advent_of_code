# 2016-14

import logging
import hashlib

log = logging.getLogger("aoc_logger")

hex_chars = "0123456789abcdef"
quintuplets = [x * 5 for x in hex_chars]


def generate_keys(salt, no_of_keys=64, stretch_factor=0):
    index = 0
    keys = list()
    expecting = {x: list() for x in hex_chars}
    while len(keys) < no_of_keys:
        h = hashlib.md5((salt + str(index)).encode()).hexdigest()
        for i in range(stretch_factor):
            h = hashlib.md5(h.encode()).hexdigest()
        for i in range(len(h) - 2):
            if h[i] == h[i + 1] and h[i] == h[i + 2]:
                expecting[h[i]].append(index)
                break
        for q in quintuplets:
            if q in h:
                for n in expecting[q[0]]:
                    if index != n and index - n <= 1000 and n not in keys:
                        keys.append(n)
                        log.info(f"New key {n}")
        index += 1
    return keys


def part1(in_data, test=False):
    salt = in_data.strip()
    keys = generate_keys(salt, 64, 0)
    return keys[63]


def part2(in_data, test=False):
    salt = in_data.strip()
    keys = generate_keys(salt, 64, 2016)
    return keys[63]
