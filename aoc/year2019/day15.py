# 2019-15
import logging
from aoc_lib.intcode2019 import Intcode2019
from threading import Event
from aoc_lib.map2d import Map2d
from aoc_lib.vector2d import *

log = logging.getLogger("aoc_logger")

dir_v_map = {1: (0, -1), 2: (0, 1), 3: (-1, 0), 4: (1, 0)}

diff_map = {  # target - position
    (1, 0): 4,
    (-1, 0): 3,
    (0, 1): 2,
    (0, -1): 1,
}

out_map = {
    0: "#",
    1: ".",
    2: "O",
}


def robot_step(direction, computer):
    computer.send_single_input(direction)
    return computer.get_single_output()


def headbangin(program):
    computer = Intcode2019()
    finish = Event()
    computer.run_program(program, finish_event=finish)
    start = (0, 0)
    end = None
    position = (0, 0)
    teh_map = dict()
    teh_map[position] = "0"
    movement_stack = list()
    to_check = list()
    to_check += [((0, 0), 1), ((0, 0), 2), ((0, 0), 3), ((0, 0), 4)]
    # total_counter = 500
    try:
        while len(to_check) > 0:
            log.info("------------")
            log.info(position)
            # total_counter -= 1
            # if total_counter == 0:
            #     finish.set()
            #     break
            pos, d = to_check[-1]
            log.info(to_check[-1])
            # log.info(to_check)
            if pos != position:
                pos_diff = v_diff(pos, position)
                if pos_diff not in diff_map:
                    raise ValueError(f"robot {position}, pos {pos}")
                else:
                    o = robot_step(diff_map[pos_diff], computer)
                    position = pos
            next_step = v_add(pos, dir_v_map[d])
            if next_step in teh_map:
                to_check.pop()  # already checked
                pos_diff = v_diff(pos, position)
                if pos_diff not in diff_map:
                    # raise ValueError(f"robot {position}, pos {pos}")
                    pass
                else:
                    o = robot_step(diff_map[pos_diff], computer)
                    position = pos
                continue
            o = robot_step(d, computer)
            if o == 0:
                teh_map[next_step] = "#"
                to_check.pop()  # can't continue there, no position change
            elif o == 1 or o == 2:
                teh_map[next_step] = out_map[o]  # we can walk there, note what's up
                if o == 2:
                    end = next_step  # found
                position = next_step
                to_check += [
                    (next_step, 1),
                    (next_step, 2),
                    (next_step, 3),
                    (next_step, 4),
                ]
    except Exception as e:
        pass
        # raise e
    map2d = Map2d.from_point_dict(teh_map)
    dd = map2d.debug_draw()
    finish.set()
    robot_step(1, computer)
    log.info(dd)
    return map2d, start, end


def part1(in_data, test=False):
    program = Intcode2019.parse_int_program(in_data)
    map2d, start, end = headbangin(program)
    map2d.flood(start)
    return map2d.get_flooded_val(end)


def part2(in_data, test=False):
    program = Intcode2019.parse_int_program(in_data)
    map2d, start, end = headbangin(program)
    map2d.flood(end)
    return map2d.get_flood_max()[1]
