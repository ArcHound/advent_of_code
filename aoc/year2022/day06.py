# 2022-6
import logging

log = logging.getLogger("aoc_logger")


def start_of_packet(data, marker):
    buffers = list()
    for i in range(len(data)):
        c = data[i]
        buffers += c
        if len(buffers) > marker:
            buffers = buffers[1:]
        if len(set(buffers)) == marker:
            return i + 1


def part1(in_data):
    return start_of_packet(in_data, 4)


def part2(in_data):
    return start_of_packet(in_data, 14)
