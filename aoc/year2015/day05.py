# 2015-05

import logging

log = logging.getLogger("aoc_logger")


def parse_data(in_data):
    data = list()
    for line in in_data.splitlines():
        data.append(line)
    return data


def is_nice(s):
    vowel_count = 0
    has_double = False
    forbidden = False
    for i in range(len(s)):
        if vowel_count < 3 and s[i] in "aeiou":
            vowel_count += 1
        if i > 0 and (not has_double) and s[i - 1] == s[i]:
            has_double = True
        if i > 0 and (not forbidden) and s[i - 1] + s[i] in ["ab", "cd", "pq", "xy"]:
            forbidden = True
            break
    if not forbidden and vowel_count >= 3 and has_double:
        return True
    else:
        return False


def part1(in_data, test=False):
    data = parse_data(in_data)
    return sum([1 for x in data if is_nice(x)])


def is_nice_v2(s):
    triplet = False
    two_pair = False
    result = False
    pair_cache = list()
    log.debug(s)
    for i in range(len(s)):
        if i >= 2 and not triplet and s[i - 2] == s[i]:
            log.debug(f"triplet {s[i - 2] + s[i - 1] + s[i]}")
            triplet = True
        if i >= 1 and not two_pair:
            pair = s[i - 1] + s[i]
            if pair in pair_cache[:-1]:
                two_pair = True
                log.debug(f"two pair {s[i - 1] + s[i]}")
            pair_cache.append(pair)
        if two_pair and triplet:
            result = True
            break
    return result


def part2(in_data, test=False):
    data = parse_data(in_data)
    return sum([1 for x in data if is_nice_v2(x)])
