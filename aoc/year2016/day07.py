# 2016-07

import logging

log = logging.getLogger("aoc_logger")


def parse_data(in_data):
    data = list()
    for line in in_data.splitlines():
        open_tokens = list()
        closed_tokens = list()
        state = "open"
        token = ""
        for c in line.strip():
            if state == "open" and c != "[":
                token += c
            elif state == "open" and c == "[":
                open_tokens.append(token)
                token = ""
                state = "closed"
            elif state == "closed" and c != "]":
                token += c
            elif state == "closed" and c == "]":
                state = "open"
                closed_tokens.append(token)
                token = ""
        open_tokens.append(token)
        data.append((open_tokens, closed_tokens))
    return data


def abba(token):
    log.debug(token)
    any_abba = False
    if len(token) < 4:
        return False
    for i in range(len(token) - 3):
        any_abba = (
            token[i] == token[i + 3]
            and token[i + 1] == token[i + 2]
            and token[i] != token[i + 1]
        )
        if any_abba:
            break
    log.debug(any_abba)
    return any_abba


def part1(in_data, test=False):
    data = parse_data(in_data)
    counter = 0
    for open_tokens, closed_tokens in data:
        if any([abba(token) for token in open_tokens]) and all(
            [not abba(token) for token in closed_tokens]
        ):
            counter += 1
    return counter


def get_abas(token):
    any_aba = False
    if len(token) < 3:
        return False
    abas = list()
    for i in range(len(token) - 2):
        if token[i] == token[i + 2] and token[i] != token[i + 1]:
            abas.append(token[i] + token[i + 1] + token[i + 2])
    return abas


def part2(in_data, test=False):
    data = parse_data(in_data)
    counter = 0
    for open_tokens, closed_tokens in data:
        open_abas = list()
        closed_abas = list()
        for t in open_tokens:
            open_abas += get_abas(t)
        for t in closed_tokens:
            closed_abas += get_abas(t)
        for a in open_abas:
            inv_a = a[1] + a[0] + a[1]
            if inv_a in closed_abas:
                counter += 1
                break
    return counter
