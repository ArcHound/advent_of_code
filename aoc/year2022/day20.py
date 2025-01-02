# 2022-20

import logging

log = logging.getLogger("aoc_logger")


def parse_data(in_data):
    data = list()
    for line in in_data.splitlines():
        data.append(int(line.strip()))
    return data


def mix_array(data, mult=1):
    data_len = len(data)
    array = list(data)
    for entry in data * mult:
        old_place = array.index(entry)
        array.remove(entry)
        new_place = (old_place + entry[0] + data_len - 1) % (data_len - 1)
        array.insert(new_place, entry)
        log.debug(f"Moving {entry} from {old_place} to {new_place}")
    return array


def calc_coordinates(array, zero):
    zero_index = array.index(zero)
    coordinates = [(zero_index + i * 1000) % len(array) for i in range(1, 4)]
    return sum([array[c][0] for c in coordinates])


def part1(in_data, test=False):
    data = parse_data(in_data)
    data = [(data[i], i) for i in range(len(data))]
    zero = [data[i] for i in range(len(data)) if data[i][0] == 0][0]
    array = mix_array(data)
    return calc_coordinates(array, zero)


def part2(in_data, test=False):
    data = parse_data(in_data)
    key = 811589153
    data = [(data[i] * key, i) for i in range(len(data))]
    zero = [data[i] for i in range(len(data)) if data[i][0] == 0][0]
    array = mix_array(data, 10)
    return calc_coordinates(array, zero)
