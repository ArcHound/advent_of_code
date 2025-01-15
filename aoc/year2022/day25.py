# 2022-25

import logging

log = logging.getLogger("aoc_logger")


def parse_data(in_data):
    data = list()
    for line in in_data.splitlines():
        data.append(line)
    return data


snafu_dict = {
    "1": 1,
    "2": 2,
    "0": 0,
    "-": -1,
    "=": -2,
}

snafu_dict_inv = {
    1: "1",
    2: "2",
    0: "0",
    -1: "-",
    -2: "=",
}


def snafu_to_decimal(snafu):
    total = 0
    num_len = len(snafu)
    for i in range(num_len):
        total += pow(5, num_len - i - 1) * snafu_dict[snafu[i]]
    return total


# 1=-0-2
#  12111
# ------
# 1-111=
def add_snafu(a, b):
    if len(a) >= len(b):
        shorter = b[::-1]
        longer = a[::-1]
    else:
        shorter = a[::-1]
        longer = b[::-1]
    carry_over = 0
    added = ""
    shl = len(shorter)
    for i in range(shl, len(longer)):
        shorter = shorter + "0"
    for i in range(len(shorter)):
        new_digit = carry_over + snafu_dict[shorter[i]] + snafu_dict[longer[i]]
        if new_digit > 2:
            carry_over = 1
            new_digit = new_digit - 5
        elif new_digit < -2:
            carry_over = -1
            new_digit = new_digit + 5
        else:
            carry_over = 0
        added = snafu_dict_inv[new_digit] + added
    if carry_over != 0:
        added = snafu_dict_inv[carry_over] + added
    return added


def part1(in_data, test=False):
    data = parse_data(in_data)
    total_s = "0"
    total_d = 0
    for d in data:
        prev_s = total_s
        total_s = add_snafu(total_s, d)
        total_d = total_d + snafu_to_decimal(d)
        if snafu_to_decimal(total_s) != total_d:
            log.error(
                f"{prev_s} + {d} != {total_s} {total_d}!={snafu_to_decimal(total_s)}"
            )
            break
    return total_s


def part2(in_data, test=False):
    return 0
