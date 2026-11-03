# 2016-21

import logging
from aoc_lib.combinatorics import permutations

log = logging.getLogger("aoc_logger")


def parse_data(in_data):
    data = list()
    for line in in_data.splitlines():
        data.append(line.strip().split(" "))
    return data


def swap_position(password, p_1, p_2):
    buf = password
    a = min(p_1, p_2)
    b = max(p_1, p_2)
    if a > 0 and b < len(buf):
        buf = buf[:a] + buf[b] + buf[a + 1 : b] + buf[a] + buf[b + 1 :]
    elif a > 0:
        buf = buf[:a] + buf[b] + buf[a + 1 : b] + buf[a]
    elif b < len(buf):
        buf = buf[b] + buf[a + 1 : b] + buf[a] + buf[b + 1 :]
    else:
        buf = buf[b] + buf[a + 1 : b] + buf[a]
    return buf


def process(password, instructions):
    buf = password
    for inst in instructions:
        log.debug(buf)
        log.debug(inst)
        if inst[0] == "swap":
            if inst[1] == "letter":
                p_1 = buf.index(inst[2])
                p_2 = buf.index(inst[5])
                buf = swap_position(buf, p_1, p_2)
            elif inst[1] == "position":
                p_1 = int(inst[2])
                p_2 = int(inst[5])
                buf = swap_position(buf, p_1, p_2)
        elif inst[0] == "rotate":
            if inst[1] == "based":
                target_index = buf.index(inst[6])
                buf = buf[-1] + buf[:-1]
                for i in range(target_index):
                    buf = buf[-1] + buf[:-1]
                # the fuck is this supposed to be?
                # I guess it's to do a left-rotation, but man..
                # don't think, implement spec
                if target_index >= 4:
                    buf = buf[-1] + buf[:-1]
            elif inst[1] == "left" or inst[1] == "right":
                rotate = int(inst[2]) % len(buf)
                if inst[1] == "left":
                    rotate = (len(buf) - rotate) % len(buf)
                for i in range(rotate):
                    buf = buf[-1] + buf[:-1]
            else:
                raise ValueError(f"Invalid command {inst[0] + ' ' + inst[1]}")
        elif inst[0] == "reverse":
            buf = (
                buf[: int(inst[2])]
                + buf[int(inst[2]) : int(inst[4]) + 1][::-1]
                + buf[int(inst[4]) + 1 :]
            )
        elif inst[0] == "move":
            letter = buf[int(inst[2])]
            new_buf = buf[: int(inst[2])] + buf[int(inst[2]) + 1 :]
            log.debug(new_buf)
            new_buf = new_buf[: int(inst[5])] + letter + new_buf[int(inst[5]) :]
            buf = new_buf
        else:
            raise ValueError(f"Invalid command {inst[0]}")
        log.debug(buf)
        log.debug("----")
    return buf


def part1(in_data, test=False):
    password = "abcdefgh" if not test else "abcde"
    data = parse_data(in_data)
    log.debug(data)
    return process(password, data)


def part2(in_data, test=False):
    data = parse_data(in_data)
    # actually, before we reverse this completely, let's think for a moment
    # these operations all "preserve letters"
    # if we start with an "a" it might be somewhere else, but it will be there exactly once
    # that means we're looking for a permutation of these 8 letters
    # there are only 8! == 40320 of them
    # so let's just check them all!
    target = "fbgdceah"
    proto_pass = ["a", "b", "c", "d", "e", "f", "g", "h"]
    result = ""
    for p in permutations(proto_pass):
        if process("".join(p), data) == target:
            result = "".join(p)
            break
    return result
