# 2024-22

import logging

log = logging.getLogger("aoc_logger")


def parse_data(in_data):
    data = list()
    for line in in_data.splitlines():
        data.append(int(line.strip()))
    return data


mod_const = 16777216


def calc_secret(a):
    b = ((a * 64) ^ a) % mod_const
    c = ((b // 32) ^ b) % mod_const
    d = ((c * 2048) ^ c) % mod_const
    return d


def part1(in_data, test=False):
    data = parse_data(in_data)
    total = 0
    for a in data:
        t = a
        for i in range(2000):
            t = calc_secret(t)
        total += t
    return total


def part2(in_data, test=False):
    data = parse_data(in_data)
    sequences = list()
    prices = list()
    for a in data:
        seq = list()
        pr = list()
        t = a
        pr.append(a % 10)
        for i in range(2000):
            t = calc_secret(t)
            pr.append(t % 10)
            seq.append(pr[i + 1] - pr[i])
        sequences.append(seq)
        prices.append(pr)
    log.error(len(sequences))
    four_sequences_seen = dict()
    four_sequences_counter = dict()
    for sequence in sequences:
        for i in range(len(sequence) - 4):
            four_sequences_seen[
                (sequence[i], sequence[i + 1], sequence[i + 2], sequence[i + 3])
            ] = False
            four_sequences_counter[
                (sequence[i], sequence[i + 1], sequence[i + 2], sequence[i + 3])
            ] = 0
    for j in range(len(sequences)):
        sequence = sequences[j]
        for k in four_sequences_seen:
            four_sequences_seen[k] = False
        for i in range(len(sequence) - 4):
            l = (sequence[i], sequence[i + 1], sequence[i + 2], sequence[i + 3])
            if not four_sequences_seen[l]:
                four_sequences_counter[l] += prices[j][i + 4]
                four_sequences_seen[l] = True
    return max([four_sequences_counter[x] for x in four_sequences_counter])
