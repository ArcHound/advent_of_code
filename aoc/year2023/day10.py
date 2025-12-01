# 2023-10
import logging

log = logging.getLogger("aoc_logger")

from aoc_lib.map2d import PipeMap2d, PipeType, Map2d

# imagine a 2d grid. This map corresponds to the cases, where the walls are not full tiles, but only the edges of a grid
# I've got a lib for that
# here are the options that are here - there are also T junctions, but those shouldn't be in the input
pipe_map = {
    "|": PipeType.TopDown,
    "-": PipeType.LeftRight,
    "L": PipeType.TopRight,
    "J": PipeType.TopLeft,
    "7": PipeType.LeftDown,
    "F": PipeType.RightDown,
    ".": PipeType.NoPipe,
}


def parse_data(in_data):
    x_len = len(in_data.splitlines()[0])
    y_len = len(in_data.splitlines())
    j = 0
    pipes = dict()
    bounds = ((0, 0), (x_len, y_len))  # need to know the borders
    s = None
    for line in in_data.splitlines():
        i = 0
        for c in line:
            if c == "S":
                s = (i, j)  # note the start, will be determined later
            else:
                pipes[(i, j)] = pipe_map[c]
            i += 1
        j += 1
    conns = list()
    # look for surronding tiles, we should find two connections to our starting tile
    if s[0] - 1 >= 0 and pipes[(s[0] - 1, s[1])] in [
        PipeType.LeftRight,
        PipeType.TopRight,
        PipeType.RightDown,
    ]:
        conns.append("left")
    if s[0] + 1 < x_len and pipes[(s[0] + 1, s[1])] in [
        PipeType.LeftRight,
        PipeType.TopLeft,
        PipeType.LeftDown,
    ]:
        conns.append("right")
    if s[1] - 1 >= 0 and pipes[(s[0], s[1] - 1)] in [
        PipeType.TopDown,
        PipeType.LeftDown,
        PipeType.RightDown,
    ]:
        conns.append("top")
    if s[1] + 1 < y_len and pipes[(s[0], s[1] + 1)] in [
        PipeType.TopDown,
        PipeType.TopLeft,
        PipeType.TopRight,
    ]:
        conns.append("down")
    # pray there's only two
    log.debug(conns)
    # note the pipe shape for the start
    if "left" in conns and "right" in conns:
        pipes[s] = PipeType.LeftRight
    if "left" in conns and "top" in conns:
        pipes[s] = PipeType.TopLeft
    if "left" in conns and "down" in conns:
        pipes[s] = PipeType.LeftDown
    if "top" in conns and "down" in conns:
        pipes[s] = PipeType.TopDown
    if "top" in conns and "right" in conns:
        pipes[s] = PipeType.TopRight
    if "right" in conns and "down" in conns:
        pipes[s] = PipeType.RightDown
    log.debug(pipes[s])
    return pipes, bounds, s


def part1(in_data):
    pipes, bounds, s = parse_data(in_data)
    pm = PipeMap2d(pipes, bounds)
    # just flood the pipe, 'water' will run throught the loop
    pm.flood(s)
    points, val = (
        pm.get_flood_max_indexes()
    )  # there's only one max value, get that value
    return val


def part2(in_data):
    pipes, bounds, s = parse_data(in_data)
    # we need to find that loop -> flood it
    pm = PipeMap2d(pipes, bounds)
    pm.flood(s)
    # then take flooded tiles -> that's our loop
    obstacle_str = ""
    loop_tiles = dict()
    for j in range(0, pm.y_len):
        for i in range(0, pm.x_len):
            if pm.get_flooded_point((i, j)) != -1:
                loop_tiles[(i, j)] = pipes[(i, j)]
    # extend the map, so we can flood from all edges
    bounds2 = (
        (bounds[0][0] - 1, bounds[0][1] - 1),
        (bounds[1][0] + 1, bounds[1][1] + 1),
    )
    pm2 = PipeMap2d(loop_tiles, bounds2)
    m = pm2.inner_map  # the pipe tile is represented as a 3x3 tile where walls are tiles -> easier to work with
    m.invert_obstacles()  # however, flooded tiles are our obstacles now, everything else can be passed through
    m.flood((0, 0))  # flood again, this time the dry tiles are the inner tiles
    log.debug(m.debug_draw())
    count = 0
    for i in range(bounds[0][0], bounds[1][0]):
        for j in range(bounds[0][1], bounds[1][1]):
            # find the dry tiles that are not parts of our loop
            if (i, j) not in loop_tiles and m.get_flooded_point(
                (3 * i + 1, 3 * j + 1)
            ) == -1:
                count += 1
    return count
