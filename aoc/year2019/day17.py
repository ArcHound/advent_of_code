# 2019-17
import logging
from aoc_lib.intcode2019 import Intcode2019
from threading import Event
from aoc_lib.map2d import Map2d

log = logging.getLogger("aoc_logger")


def parse_data(in_data):
    data = list()
    for line in in_data.splitlines():
        data.append(line)
    return [int(x) for x in data[0].split(",")]


def find_crosses(map2d):
    bounds = (map2d.minimal, map2d.maximal)
    log.info(bounds)
    crosses = list()
    for i in range(map2d.minimal[0], map2d.maximal[0]):
        for j in range(map2d.minimal[1], map2d.maximal[1]):
            if map2d.get_obstacle_from_point((i, j)) != "#":
                continue
            p = map2d.nearby_points((i, j))
            if (
                all([map2d.get_obstacle_from_point(x) == "#" for x in p])
                and len(p) == 4
            ):
                crosses.append((i, j))
    return crosses


def part1(in_data, test=False):
    program = parse_data(in_data)
    computer = Intcode2019()
    computer.run_program_sync(program)
    output = computer.get_list_output()
    log.info(output)
    map_str = ""
    first = True
    counter = 0
    map_str = ""
    for i in output:
        map_str += chr(i)
    log.info("\n" + map_str)
    map2d = Map2d.from_lines(map_str)
    log.info(map2d.debug_draw())
    crosses = find_crosses(map2d)
    log.info(crosses)
    for c in crosses:
        map2d.set_point(c, "X")
    log.info(map2d.debug_draw())
    return sum([c[0] * c[1] for c in crosses])


# ..........................#####..................
# ..........................#...#..................
# ..........................#...#..................
# ..........................#...#..................
# ..........................#...#..................
# ..........................#...#..................
# ..........................####X##................
# ..............................#.#................
# ............................##X#X######..........
# ............................#.#.#.....#..........
# ..................##########X##.#.....#..........
# ..................#.........#...#.....#..........
# ..................#.........####X##...#..........
# ..................#.............#.#...#..........
# ..................#.............#.#...#..........
# ..................#.............#.#...#..........
# ......#############.............#.#...#..........
# ......#.........................#.#...#..........
# ######X####.....................##X####..........
# #.....#...#.......................#..............
# #.....#...#.......................#...#######....
# #.....#...#.......................#...#.....#....
# #######...#.......................#...#.....#....
# ..........#.......................#...#.....#....
# ..........#.......................####X######....
# ..........#...........................#..........
# ..........#...........................#...#######
# ..........#...........................#...#.....#
# ..........#.........................##X##.#.....#
# ..........#.........................#.#.#.#.....#
# ..........#######...................#.##X#X######
# ................#...................#...#.#......
# ................#.............######X###X##......
# ................#.............#.....#...#........
# ................#.............#.....#...#........
# ................#.............#.........#........
# ................#.............#.........#........
# ................#.............#.........#........
# ................#.............###########........
# ................#................................
# ................#................................
# ................#................................
# ................######^..........................

# L6, R12, L6, R12, L10, L4, L6, L6, R12, L6, R12, L10, L4, L6, L6, R12, L6, L10, L10, L4, L6, R12, L10, L4, L6, L10, L10, L4, L6, L6, R12, L6, L10, L10, L4, L6

# a b a b (c d a) a b a b (c d a) a b a c (c d a) b (c d a) c (c d a) a b a c (c d a)

# (a b a) (b c d a) (a b a) (b c d a) (a b a) (c c d a) (b c d a) (c c d a) (a b a) (c c d a)

# A B A B A C B C A C
# A = L6, R12, L6
# B = R12, L10, L4, L6
# C = L10, L10, L4, L6


def part2(in_data, test=False):
    program = parse_data(in_data)
    program[0] = 2
    computer = Intcode2019()
    code = [
        "A,B,A,B,A,C,B,C,A,C",
        "L,6,R,12,L,6",
        "R,12,L,10,L,4,L,6",
        "L,10,L,10,L,4,L,6",
        "n",
        "",
    ]
    log.info("\n".join(code))
    compiled = [ord(x) for x in "\n".join(code)]
    log.info(compiled)
    data = parse_data(in_data)
    computer.run_program_sync(program, compiled)
    output = computer.get_list_output()
    return output[-1]
