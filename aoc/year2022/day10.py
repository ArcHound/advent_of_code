# 2022-10
import logging

log = logging.getLogger("aoc_logger")


def process_instructions(instructions, mod, rem):
    cycle = 0
    x = 1
    profile = list()
    for ins in instructions:
        if ins.split()[0] == "noop":
            cycle += 1
            if cycle % mod == rem:
                log.debug(f"{cycle}, {x}")
                profile.append(cycle * x)
        elif ins.split()[0] == "addx":
            cycle += 1
            if cycle % mod == rem:
                log.debug(f"{cycle}, {x}")
                profile.append(cycle * x)
            cycle += 1
            val = int(ins.split()[1])
            if cycle % mod == rem:
                log.debug(f"{cycle}, {x}")
                profile.append(cycle * x)
            x += val
    return sum(profile)


def draw(cycle, x, buf):
    sprite = [x - 1, x, x + 1]
    log.debug(f"Cycle: {cycle}")
    log.debug(f"Sprite: {sprite}")
    if (cycle - 1) % 40 in sprite:
        buf += "#"
        log.debug("#")
    else:
        buf += "."
        log.debug(".")
    log.debug("----------")
    return buf


def render(buf):
    buf2 = [buf[i : i + 40] for i in range(0, len(buf), 40)]
    for b in buf2:
        log.debug(b)
    return "\n".join(buf2)


def process_instructions_2(instructions, mod, rem):
    cycle = 0
    x = 1
    buf = ""
    profile = list()
    for ins in instructions:
        if ins.split()[0] == "noop":
            cycle += 1
            buf = draw(cycle, x, buf)
        elif ins.split()[0] == "addx":
            cycle += 1
            buf = draw(cycle, x, buf)
            cycle += 1
            val = int(ins.split()[1])
            buf = draw(cycle, x, buf)
            x += val
    return render(buf)


def part1(in_data):
    return process_instructions(in_data.splitlines(), 40, 20)


def part2(in_data):
    return process_instructions_2(in_data.splitlines(), 40, 20)
