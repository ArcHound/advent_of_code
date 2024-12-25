# 2024-09

import logging
from aoc_lib.interval import Interval
from tqdm import tqdm

log = logging.getLogger("aoc_logger")


def parse_data(in_data):
    data = list()
    data_copy = list()
    trigger = True
    file_id = 0
    for line in in_data.splitlines():
        for i in range(len(line.strip())):
            n = int(line[i])
            if trigger:
                data.append((n, file_id))
                file_id += 1
                trigger = False
            else:
                data.append((n, None))
                trigger = True
    return data


def checksum(buffer):
    i = 0
    total = 0
    while len(buffer) > 0:
        process = buffer.pop(0)
        for j in range(process[0]):
            total += i * process[1]
            i += 1
    return total


def part1(in_data, test=False):
    read = parse_data(in_data)
    log.debug(read)
    write = list()
    swap = (0, 0)
    space = 0
    while len(read) > 0:
        a = read.pop(0)
        if a[1] is not None:
            write.append(a)
        else:
            space = a[0]
            while space > 0:
                if swap[0] >= space:
                    write.append((space, swap[1]))
                    swap = (swap[0] - space, swap[1])
                    space = 0
                    break
                elif swap[0] > 0:
                    write.append((swap[0], swap[1]))
                    space = space - swap[0]
                    swap = (0, 0)
                else:
                    if len(read) > 0:
                        swap = read.pop(-1)
                    else:
                        break
                    if swap[1] is None:
                        swap = read.pop(-1)
    if swap[0] > 0:
        if write[-1][1] == swap[1]:
            x = write.pop(-1)
            write.append((x[0] + swap[0], swap[1]))
        else:
            write.append(swap)
    log.debug(write)
    return checksum(write)


def checksum_int(buffer):
    total = 0
    while len(buffer) > 0:
        process = buffer.pop(0)
        for j in range(process.start, process.end):
            total += j * process.label
    return total


def part2(in_data, test=False):
    """UGLYYYYY! Somehow, I just failed to find a pretty solution, even though I think it exists"""
    read = parse_data(in_data)
    absolute_read = list()
    absolute_val = 0
    write = list()
    for length, file_id in read:
        label = "space"
        if file_id is not None:
            label = file_id
        absolute_read.append(Interval(absolute_val, absolute_val + length, label))
        absolute_val += length
    log.debug(absolute_read)
    files_reversed = [x for x in absolute_read if x.label != "space"]
    files_reversed.reverse()
    spaces = [x for x in absolute_read if x.label == "space"]
    log.debug(files_reversed)
    log.debug(spaces)
    for file_int in tqdm(files_reversed):
        new_spaces = list()
        found_space = False
        while len(spaces) > 0:
            space = spaces.pop(0)
            if (
                not found_space
                and file_int.length() <= space.length()
                and file_int.start > space.start
            ):
                write.append(
                    Interval(
                        space.start, space.start + file_int.length(), file_int.label
                    )
                )
                new_spaces.append(
                    Interval(space.start + file_int.length(), space.end, "space")
                )
                found_space = True
            else:
                new_spaces.append(space)
        if not found_space:
            write.append(file_int)
        spaces = new_spaces
    log.debug(write)
    return checksum_int(write)
