# 2023-4
import logging
from collections import defaultdict

log = logging.getLogger("aoc_logger")

def parse(in_data):
    winning = list()
    playing = list()
    for line in in_data.splitlines():
        nums = line.split(':')[1]
        winning.append({int(x) for x in nums.split('|')[0].split(' ') if x!=''})
        playing.append({int(x) for x in nums.split('|')[1].split(' ') if x!=''})
    return winning, playing

def part1(in_data):
    count = 0
    winning, playing = parse(in_data)
    for i in range(len(winning)):
        w = len(winning[i] & playing[i])
        if w>=1:
            count += pow(2,w-1)
    return count

def part2(in_data):
    cards = defaultdict(lambda: 1)
    winning, playing = parse(in_data)
    for i in range(len(winning)):
        _ = cards[i]
        w = len(winning[i] & playing[i])
        if w>=1:
            for j in range(i+1, i+w+1):
                cards[j]+=cards[i]
    log.debug(cards)
    return sum([cards[x] for x in cards])
