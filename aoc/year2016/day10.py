# 2016-10

import logging

log = logging.getLogger("aoc_logger")


def parse_data(in_data):
    data = list()
    values_map = dict()
    bot_map = dict()
    output_map = dict()
    for line in in_data.splitlines():
        tokens = line.strip().split(" ")
        if tokens[0] == "value":
            assert tokens[4] == "bot"  # values always go to bots
            values_map[int(tokens[1])] = int(tokens[5])
        elif tokens[0] == "bot":
            assert (
                tokens[3] == "low" and tokens[8] == "high"
            )  # only low and high in this order
            bot_map[int(tokens[1])] = (
                (tokens[5], int(tokens[6])),
                (tokens[10], int(tokens[11])),
            )
            if tokens[5] == "output":
                output_map[int(tokens[6])] = list()
            if tokens[10] == "output":
                output_map[int(tokens[11])] = list()
    return values_map, bot_map, output_map


def process_factory(values_map, bot_map, output_map, target=None):
    bot_inventory = {x: list() for x in bot_map}
    for value in values_map:
        bot_inventory[values_map[value]].append(value)
    done = False
    result = None
    while not done:
        done = True
        for bot_id in bot_inventory:
            if len(bot_inventory[bot_id]) == 2:
                done = False
                high = max(bot_inventory[bot_id])
                low = min(bot_inventory[bot_id])
                bot_inventory[bot_id] = list()
                if bot_map[bot_id][0][0] == "bot":
                    bot_inventory[bot_map[bot_id][0][1]].append(low)
                else:
                    output_map[bot_map[bot_id][0][1]].append(low)
                if bot_map[bot_id][1][0] == "bot":
                    bot_inventory[bot_map[bot_id][1][1]].append(high)
                else:
                    output_map[bot_map[bot_id][1][1]].append(high)
                if (
                    target is not None
                    and target[0] in (low, high)
                    and target[1] in (low, high)
                ):
                    result = bot_id
    return result


def part1(in_data, test=False):
    values_map, bot_map, output_map = parse_data(in_data)
    target = (61, 17) if not test else (5, 2)
    result = process_factory(values_map, bot_map, output_map, target)
    return result


def part2(in_data, test=False):
    values_map, bot_map, output_map = parse_data(in_data)
    result = process_factory(values_map, bot_map, output_map)
    return output_map[0][0] * output_map[1][0] * output_map[2][0]
