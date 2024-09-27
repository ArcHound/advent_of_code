# 2019-16
import logging

log = logging.getLogger("aoc_logger")


def parse_data(in_data):
    data = list()
    for line in in_data.splitlines():
        data.append(line)
    return [int(x) for x in data[0].strip()]


def expand_pattern(pattern, element, l):
    counter = 0
    pattern_counter = 0
    phase_counter = 0
    expanded = list()
    while counter <= l:
        expanded.append(pattern[pattern_counter])
        counter += 1
        phase_counter += 1
        if phase_counter == element:
            phase_counter = 0
            pattern_counter = (pattern_counter + 1) % len(pattern)
    return expanded[1:]


def fft(data, patterns):
    new_data = list()
    for i in range(len(data)):
        new_data.append(
            abs(sum([data[j] * patterns[i][j] for j in range(len(data))])) % 10
        )
    return new_data


def part1(in_data, test=False):
    rounds = 0
    if test:
        rounds = 4
    else:
        rounds = 100
    data = parse_data(in_data)
    patterns = list()
    pattern = [0, 1, 0, -1]
    for i in range(len(data)):
        expanded = expand_pattern(pattern, i + 1, len(data))
        patterns.append(expanded)
    log.debug(patterns)
    for i in range(rounds):
        data = fft(data, patterns)
        log.debug(data)
    return "".join([str(data[i]) for i in range(8)])


def part2(in_data, test=False):
    rounds = 0
    if test:
        rounds = 4
    else:
        rounds = 100
    data = parse_data(in_data) * 10000
    offset = int(
        "".join(in_data[:7])
    )  # basically, if we're far enough, then its about counting the sum of one*digit at place
    log.debug(offset)
    for i in range(rounds):
        # also, it's a triangle, so we can count down and remove unwanted elements
        big_sum = sum([data[j] for j in range(offset, len(data))])
        for j in range(offset, len(data)):
            n = big_sum
            big_sum -= data[j]
            data[j] = abs(n) % 10
    return int("".join([str(x) for x in data[offset : offset + 8]]))
