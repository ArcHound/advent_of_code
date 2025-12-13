# 2015-20

import logging
from aoc_lib.num_theory import primes_under_n, factorize, sum_of_divisors
from itertools import combinations
from tqdm import tqdm

log = logging.getLogger("aoc_logger")


def part1(in_data, test=False):
    target = int(in_data.strip()) // 10  # excess zero, all are divisible by 1
    log.debug(target)
    stop_h = 1000000
    primes = primes_under_n(stop_h)
    sieve = [1 for i in range(stop_h)]
    result = 0
    for p in tqdm(range(2, stop_h)):
        for i in range(p, len(sieve), p):
            sieve[i] += p
    for i in range(len(sieve)):
        if sieve[i] >= target:
            result = i
            break
    return result


def part2(in_data, test=False):
    target = int(in_data.strip())
    log.debug(target)
    stop_h = 1000000
    primes = primes_under_n(stop_h)
    sieve = [0 for i in range(stop_h)]
    result = 0
    for p in tqdm(range(1, stop_h)):
        max_range = min((50 * p + 1, stop_h))
        for i in range(p, max_range, p):
            sieve[i] += p * 11
    for i in range(len(sieve)):
        if sieve[i] >= target:
            result = i
            break
    return result
