# 2015-08

import logging

log = logging.getLogger("aoc_logger")


def parse_data(in_data):
    data = list()
    for line in in_data.splitlines():
        data.append(line.strip())
    return data


def custom_unescape(line):
    l = ""
    if line[0] == '"' and line[-1] == '"':
        l = line[1:-1]
    else:
        raise ValueError("unescaped string exists")
    new_l = ""
    state = "normal"
    hex_buf = ""
    i = 0
    for c in l:
        if state == "normal":
            if c != "\\":
                new_l += c
            else:
                state = "escaping"
        elif state == "escaping":
            if c == "\\":
                new_l += "\\"
                state = "normal"
            elif c == '"':
                new_l += '"'
                state = "normal"
            elif c == "x":
                state = "hex"
            else:
                raise ValueError(f"Invalid escape character {c} at {i}")
        elif state == "hex":
            if c in "0123456789abcdef":
                hex_buf += c
            else:
                raise ValueError(f"Invalid hex character {c} at {i}")
            if len(hex_buf) == 2:
                new_l += chr(int("0x" + hex_buf, 16))
                hex_buf = ""
                state = "normal"
        i += 1
    return new_l


def part1(in_data, test=False):
    data = parse_data(in_data)
    total = 0
    for line in data:
        char_len = len(line)
        ul = custom_unescape(line)
        str_len = len(ul)
        log.debug(line)
        log.debug(ul)
        log.debug(f"{char_len} - {str_len} = {char_len - str_len}")
        total += char_len - str_len
    return total


def custom_escape(line):
    new_l = ""
    for c in line:
        if c == '"':
            new_l += '\\"'
        elif c == "\\":
            new_l += "\\\\"
        else:
            new_l += c
    return '"' + new_l + '"'


def part2(in_data, test=False):
    data = parse_data(in_data)
    total = 0
    for line in data:
        str_len = len(line)
        el = custom_escape(line)
        char_len = len(el)
        log.debug(line)
        log.debug(el)
        log.debug(f"{char_len} - {str_len} = {char_len - str_len}")
        total += char_len - str_len
    return total
