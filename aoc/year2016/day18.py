# 2016-18

import logging

log = logging.getLogger("aoc_logger")


def tile_rules(a, b, c):
    if a == "^" and b == "^" and c == ".":
        return "^"
    elif a == "." and b == "^" and c == "^":
        return "^"
    elif a == "^" and b == "." and c == ".":
        return "^"
    elif a == "." and b == "." and c == "^":
        return "^"
    else:
        return "."


def get_next_row(row):
    next_row = ""
    next_row += tile_rules(".", row[0], row[1])
    for i in range(1, len(row) - 1):
        next_row += tile_rules(row[i - 1], row[i], row[i + 1])
    next_row += tile_rules(row[-2], row[-1], ".")
    return next_row


def part1(in_data, test=False):
    first_row = in_data.strip()
    target = 40 if not test else 10
    rows = [first_row]
    next_row = first_row
    for i in range(target - 1):
        next_row = get_next_row(next_row)
        rows.append(next_row)
    return sum([1 for x in "".join(rows) if x == "."])


def part2(in_data, test=False):
    first_row = in_data.strip()
    target = 400000
    counter = sum([1 for x in first_row if x == "."])
    next_row = first_row
    for i in range(target - 1):
        next_row = get_next_row(next_row)
        counter += sum([1 for x in next_row if x == "."])
    return counter
