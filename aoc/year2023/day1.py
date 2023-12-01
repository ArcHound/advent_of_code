# 2023-1
import logging
import re

log = logging.getLogger("aoc_logger")

def part1(in_data):
    count = 0
    for line in in_data.splitlines():
        new_line = [c for c in line if c in "0123456789"]
        count += int(new_line[0]+new_line[-1])
    return count

digit_map = {
    "0":0,
    "1":1,
    "2":2,
    "3":3,
    "4":4,
    "5":5,
    "6":6,
    "7":7,
    "8":8,
    "9":9,
    "zero":0,
    "one":1,
    "two":2,
    "three":3,
    "four":4,
    "five":5,
    "six":6,
    "seven":7,
    "eight":8,
    "nine":9,
}

def part2(in_data):
    count = 0
    for line in in_data.splitlines():
        nums = re.findall(r'(?=([0-9]|one|two|three|four|five|six|seven|eight|nine))', line) # 1twone -> last is one, not two, lookahead
        count += digit_map[nums[0]]*10+digit_map[nums[-1]]
        # log.debug(line)
        # log.debug(nums)
        # log.debug(digit_map[nums[0]]*10+digit_map[nums[-1]])
        # log.debug("---------")
    return count
