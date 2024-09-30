# 2019-7
import logging
from aoc_lib.combinatorics import permutations
from aoc_lib.intcode2019 import Intcode2019
from threading import Event

log = logging.getLogger("aoc_logger")


def try_sequence(elements, program):
    output = 0
    for i in range(5):
        computer = Intcode2019()
        computer.run_program_sync(program, stdin=[elements[i], output])
        output = computer.stdout[0]
    return output


def part1(in_data, test=False):
    data = Intcode2019.parse_int_program(in_data)
    elements = [0, 1, 2, 3, 4]
    max_output = 0
    for p in permutations(elements):
        o = try_sequence(p, data)
        if o > max_output:
            max_output = o
    return max_output


def try_sequence_feedback(elements, program):
    output = 0
    computers = [Intcode2019() for i in range(5)]
    finish_events = [Event() for i in range(5)]
    for i in range(5):
        computers[i].pipeline(computers[(i + 1) % 5])
        computers[i].send_single_input(elements[i])
    computers[0].send_single_input(0)
    for i in range(5):
        computers[i].run_program(program, finish_event=finish_events[i])
    for i in range(5):
        finish_events[i].wait()
    return computers[4].get_list_output()[-1]


def part2(in_data, test=False):
    data = Intcode2019.parse_int_program(in_data)
    elements = [5, 6, 7, 8, 9]
    max_output = 0
    for p in permutations(elements):
        o = try_sequence_feedback(p, data)
        if o > max_output:
            max_output = o
    return max_output
