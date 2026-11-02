# 2016-19

import logging
from collections import deque
from tqdm import tqdm

log = logging.getLogger("aoc_logger")


def part1(in_data, test=False):
    elves_count = int(in_data.strip())
    elves = [True for i in range(elves_count)]
    elf = 0
    done = False
    while not done:
        next_elf = -1
        # wrap
        if elf == len(elves) - 1:
            next_elf = elves.index(True)
        else:
            try:
                next_elf = elves.index(True, elf + 1)
            except ValueError:
                # wrap
                next_elf = elves.index(True)
        if next_elf == elf:
            done = True
            break
        elves[next_elf] = False
        if next_elf == len(elves) - 1:
            elf = elves.index(True)
        else:
            try:
                elf = elves.index(True, elf + 1)
            except ValueError:
                elf = elves.index(True)
    return next_elf + 1


def part2(in_data, test=False):
    elves_count = int(in_data.strip())
    # this is how to do it properly, so we can discover the pattern
    # queue = deque()
    # for i in range(elves_count):
    #     queue.append(i)
    # for i in tqdm(range(elves_count-1)):
    #     thief = queue.popleft()
    #     l = elves_count-i-1
    #     middle = l//2 if l%2==1 else (l//2)-1
    #     queue.remove(queue[middle])
    #     queue.append(thief)
    # return queue[0]+1
    # the pattern is to reach the closest power of three and then increment up to a point
    # again, we hope we're in the increment stage, if not, I'll adjust
    b = 1
    while pow(3, b) < elves_count:
        b += 1
    b -= 1
    return elves_count - pow(3, b)
