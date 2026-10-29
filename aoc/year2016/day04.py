# 2016-04

import logging
from collections import defaultdict

log = logging.getLogger("aoc_logger")


def parse_data(in_data):
    data = list()
    for line in in_data.splitlines():
        dashes, h = line.strip()[:-1].split("[")
        ids = dashes.split("-")[:-1]
        sector_id = int(dashes.split("-")[-1])
        data.append((ids, sector_id, h))
    return data


def room_checksum(ids):
    counter = defaultdict(int)
    for i in ids:
        for c in i:
            counter[c] += 1
    b = sorted(
        sorted([(x, counter[x]) for x in counter], key=lambda x: x[0]),
        key=lambda x: x[1],
        reverse=True,
    )  # sorts are stable
    return "".join([x[0] for x in b[:5]])


def part1(in_data, test=False):
    data = parse_data(in_data)
    counter = 0
    for ids, sector_id, h in data:
        if room_checksum(ids) == h:
            counter += sector_id
    return counter


def caesar(s, shift):
    result = ""
    for c in s:
        val = ord(c) - ord("a")
        new_val = (val + shift) % 26
        result += chr(new_val + ord("a"))
    return result


def part2(in_data, test=False):
    data = parse_data(in_data)
    wanted_sector = 0
    for ids, sector_id, h in data:
        if room_checksum(ids) == h:
            decrypted = " ".join([caesar(x, sector_id) for x in ids])
            if not test and decrypted == "northpole object storage":
                wanted_sector = sector_id
                break
            elif test and decrypted == "very encrypted name":
                wanted_sector = sector_id
                break
    return wanted_sector
