# 2019-25

import logging
import click
from aoc_lib.intcode2019 import Intcode2019
from threading import Event
import time

log = logging.getLogger("aoc_logger")


def part1(in_data, test=False):
    program = Intcode2019.parse_int_program(in_data)
    computer = Intcode2019()
    finished = Event()
    # save_file = ['north', 'take mug', 'north', 'take food ration', 'south', 'east', 'north', 'north', 'south', 'east', 'take semiconductor', 'east', 'west', 'west', 'south', 'west', 'south', 'east', 'take ornament', 'north', 'take coin', 'east', 'take mutex', 'west', 'south', 'east', 'take candy cane', 'east', 'east', 'west', 'west', 'west', 'north', 'east', 'west', 'south', 'west', 'south']
    # take all useful items - molten lava, giant magnet, escape pod, photons and infinity loop are not useful and will kill you one way or another
    # then navigate to the security check
    save_file = [
        "north",
        "take mug",
        "north",
        "take food ration",
        "south",
        "east",
        "north",
        "north",
        "south",
        "east",
        "take semiconductor",
        "east",
        "west",
        "west",
        "south",
        "west",
        "south",
        "east",
        "take ornament",
        "north",
        "take coin",
        "east",
        "take mutex",
        "west",
        "south",
        "east",
        "take candy cane",
        "east",
        "east",
        "west",
        "west",
        "west",
        "north",
        "east",
        "west",
        "south",
        "west",
        "south",
        "west",
        "north",
        "south",
        "east",
        "east",
        "take mouse",
        "west",
        "east",
        "south",
        "west",
    ]
    # drop it all
    inventory = [
        "food ration",
        "candy cane",
        "mouse",
        "mug",
        "coin",
        "ornament",
        "semiconductor",
        "mutex",
    ]
    save_file += [f"drop {x}" for x in inventory]
    prompt_log = list()
    # try all combinations of items - take, move, drop all to try again
    for i in range(256):
        temp_inv = list()
        for j in range(8):
            if (i // pow(2, j)) % 2 == 1:
                temp_inv.append(f"take {inventory[j]}")
        temp_inv.append("west")
        for j in range(8):
            if (i // pow(2, j)) % 2 == 1:
                temp_inv.append(f"drop {inventory[j]}")
        save_file += list(temp_inv)
    # store the log and search through it for the password
    computer.run_program(program, finish_event=finished)
    # walk the walk
    while not finished.is_set():
        time.sleep(0.1)
        click.echo(computer.get_ascii_output())
        if len(save_file) > 0:
            s = save_file.pop(0)
        else:
            s = click.prompt("?")
        prompt_log.append(s)
        computer.send_ascii_input(s + "\n")
        click.echo(prompt_log)
    return "part1 output 2019-25"


def part2(in_data, test=False):
    return 0
