# 2020-18

import logging
from collections import deque

log = logging.getLogger("aoc_logger")


def parse_data(in_data):
    data = list()
    for line in in_data.splitlines():
        data.append([x for x in line if x != " "])
    return data


def eval_expr(a):
    if len(a) == 1 and a in "0123456789":
        return int(a)
    elif len(a) == 1 and a not in "0123456789":
        raise ValueError("one token to eval and it's not a number. Please fix.")
    elif len(a) == 2:
        raise ValueError("Somehow you got two values here? Go fix it.")
    i = 0
    total = None
    op = None
    while i < len(a):
        if a[i] in "0123456789":
            first = int(a[i])
            i += 1
            if total is None:
                total = first
            else:
                if op == "+":
                    total += first
                elif op == "*":
                    total *= first
                else:
                    raise ValueError("Plus and mult only. This ain't it chief.")
        elif a[i] == "(":
            v = 1
            j = 0
            while v != 0:
                j += 1
                if a[i + j] == "(":
                    v += 1
                elif a[i + j] == ")":
                    v -= 1
            first = eval_expr(a[i + 1 : i + j])
            if total is None:
                total = first
            else:
                if op == "+":
                    total += first
                elif op == "*":
                    total *= first
                else:
                    raise ValueError("Plus and mult only. This ain't it chief.")
            i += j + 1
        else:
            raise ValueError("It's not a number, it's not a bracket.. what is it? FIX!")
        if i < len(a):
            op = a[i]
            i += 1
    return total


def part1(in_data, test=False):
    data = parse_data(in_data)
    log.debug(data)
    total = 0
    for line in data:
        total += eval_expr(line)
    return total


def stack_eval(a):
    if len(a) == 1 and a in "0123456789":
        return int(a)
    elif len(a) == 1 and a not in "0123456789":
        raise ValueError("one token to eval and it's not a number. Please fix.")
    elif len(a) == 2:
        raise ValueError("Somehow you got two values here? Go fix it.")
    nums = deque([])
    ops = deque([])
    i = 0
    prev_i = -1
    log.debug(f"eval {a}")
    while i < len(a):
        if prev_i == i:
            log.debug("loop!")
            break
        prev_i = i
        log.debug(f"Nums: {nums}")
        log.debug(f"Ops:  {ops}")
        log.debug(f"{i}: '{a[i]}'")
        if a[i] in "0123456789":
            nums.append(int(a[i]))
            i += 1
        elif a[i] == "+":
            ops.append(a[i])
            i += 1
        elif a[i] == "*":
            log.debug(len(ops))
            # log.debug(ops[-1])
            if len(ops) == 0 or ops[-1] == "*":
                ops.append(a[i])
                i += 1
            else:
                while len(ops) >= 1 and ops[-1] == "+":
                    x = nums.pop()
                    y = nums.pop()
                    op = ops.pop()
                    nums.append(x + y)
                ops.append(a[i])
                i += 1
        elif a[i] == "(":
            v = 1
            j = 0
            while v != 0:
                j += 1
                if a[i + j] == "(":
                    v += 1
                elif a[i + j] == ")":
                    v -= 1
            num = stack_eval(a[i + 1 : i + j])
            nums.append(num)
            i += j + 1
        log.debug("--------")
    while len(ops) > 0:
        x = nums.pop()
        y = nums.pop()
        op = ops.pop()
        if op == "+":
            nums.append(x + y)
        else:
            nums.append(x * y)
    log.debug(f"returning {nums[0]}")
    return nums[0]


def part2(in_data, test=False):
    data = parse_data(in_data)
    log.debug(data)
    total = 0
    for line in data:
        total += stack_eval(line)
    return total
