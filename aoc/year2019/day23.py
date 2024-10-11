# 2019-23

import logging
from aoc_lib.intcode2019 import Intcode2019, Router
from threading import Event

log = logging.getLogger("aoc_logger")


def part1(in_data, test=False):
    network = {}
    switches = {}
    program = Intcode2019.parse_int_program(in_data)
    for i in range(50):
        network[i] = Intcode2019(default_stdin=True)
        switches[i] = Event()
        network[i].run_program(program, switches[i])
    router = Router(network)
    router.dhcp()
    x, y = router.routing()
    return y


def part2(in_data, test=False):
    network = {}
    switches = {}
    program = Intcode2019.parse_int_program(in_data)
    for i in range(50):
        network[i] = Intcode2019(default_stdin=True)
        switches[i] = Event()
        network[i].run_program(program, switches[i])
    router = Router(network)
    router.dhcp()
    x, y = router.routing()
    return y
