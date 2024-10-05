# 2019-21
import logging
from aoc_lib.intcode2019 import Intcode2019
from threading import Event

log = logging.getLogger("aoc_logger")

# OK, so
#
# @
###ABCD#####
#
# @
############
#  ABCD
# no jump
#
# @
###.########
#  ABCD
# jump
#
# @
###..#######
#  ABCD
# jump
#
# @
###...######
#  ABCD
# jump
#
# @
####..######
#  ABCD
# jump
#
# @
#####.######
#  ABCD
# jump


def part1(in_data, test=False):
    program = Intcode2019.parse_int_program(in_data)
    computer = Intcode2019()
    script = """NOT A T
OR T J
NOT B T
OR T J
NOT C T
OR T J
AND D J
WALK
"""
    finish_event = Event()
    computer.run_program(program, finish_event=finish_event)
    computer.send_ascii_input(script)
    finish_event.wait()
    o = computer.get_list_output()
    log.error("".join([chr(x) for x in o if x < 256]))
    return o[-1]


#
# @
###...##.#.####
#  ABCDEFGHI
# jump


def part2(in_data, test=False):
    program = Intcode2019.parse_int_program(in_data)
    computer = Intcode2019()
    script = """NOT B J
NOT C T
OR T J
AND D J
AND H J
NOT A T
OR T J
RUN
"""
    finish_event = Event()
    computer.run_program(program, finish_event=finish_event)
    computer.send_ascii_input(script)
    finish_event.wait()
    o = computer.get_list_output()
    log.error("".join([chr(x) for x in o if x < 256]))
    return o[-1]
