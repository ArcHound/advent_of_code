# 2020-14

import logging

log = logging.getLogger("aoc_logger")


def parse_data(in_data):
    data = list()
    for line in in_data.splitlines():
        if line[:3] == "mas":
            data.append(("mask", line.strip().split(" ")[-1]))
        elif line[:3] == "mem":
            val = int(line.strip().split(" ")[-1])
            addr = int(line.strip().split(" ")[0][4:-1])
            data.append(("mem", val, addr))
    return data


def calc_val(val, mask):
    mask_mask = "".join(["1" if x == "X" else "0" for x in mask])
    mask_val = "".join([x if x != "X" else "0" for x in mask])
    return (val & int(mask_mask, 2)) | int(mask_val, 2)


def part1(in_data, test=False):
    data = parse_data(in_data)
    mem = dict()
    mask = ""
    for inst in data:
        if inst[0] == "mask":
            mask = inst[1]
        else:
            mem[inst[2]] = calc_val(inst[1], mask)
    return sum([mem[x] for x in mem])


def expand_addresses(addr, mask):
    mask_copy = [x for x in mask]
    addr_v = bin(addr)[2:]
    addr_copy = (36 - len(addr_v)) * "0" + addr_v
    log.debug(addr_copy)
    for i in range(len(mask)):
        if mask[i] == "0":
            mask_copy[i] = addr_copy[i]
    xs = sum([1 for x in mask_copy if x == "X"])
    xsi = [i for i in range(len(mask_copy)) if mask[i] == "X"]
    result = list()
    for i in range(pow(2, xs)):
        vals = (len(xsi) - len(bin(i)[2:])) * "0" + bin(i)[2:]
        for j in range(len(xsi)):
            mask_copy[xsi[j]] = vals[j]
        log.debug("".join(mask_copy))
        result.append(int("".join(mask_copy), 2))
    return result


def part2(in_data, test=False):
    data = parse_data(in_data)
    mem = dict()
    mask = ""
    for inst in data:
        if inst[0] == "mask":
            mask = inst[1]
        else:
            addresses = expand_addresses(inst[2], mask)
            for addr in addresses:
                mem[addr] = inst[1]
    return sum([mem[x] for x in mem])
