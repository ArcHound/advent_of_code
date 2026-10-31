# 2016-16

import logging

log = logging.getLogger("aoc_logger")


def parse_data(in_data):
    data = list()
    for line in in_data.splitlines():
        data.append(line)
    return data


def build_disk(data, disk_size):
    buf = data
    inv = {"1": "0", "0": "1"}
    while len(buf) < disk_size:
        buf += "0" + "".join([inv[x] for x in buf[::-1]])
    buf = buf[:disk_size]
    return buf


def checksum(data):
    buf = data
    while len(buf) % 2 == 0:
        new_buf = ""
        for i in range(len(buf) // 2):
            new_buf += "1" if buf[2 * i] == buf[2 * i + 1] else "0"
        buf = new_buf
    return buf


def part1(in_data, test=False):
    data = in_data.strip()
    disk_size = 272 if not test else 20
    buf = build_disk(data, disk_size)
    return checksum(buf)


def part2(in_data, test=False):
    data = in_data.strip()
    disk_size = 35651584 if not test else 20
    buf = build_disk(data, disk_size)
    return checksum(buf)
