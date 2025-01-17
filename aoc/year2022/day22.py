# 2022-22

import logging
import math
from collections import defaultdict
from aoc_lib.map2d import Map2d

log = logging.getLogger("aoc_logger")

dir_pad = ">v<^"


class Node:

    def __init__(self):
        self.up = None
        self.down = None
        self.left = None
        self.right = None
        self.empty = False

    def set(
        self,
        up,
        down,
        left,
        right,
        up_dir_diff=0,
        down_dir_diff=0,
        left_dir_diff=0,
        right_dir_diff=0,
        empty=True,
    ):
        self.empty = empty
        self.up = up
        self.down = down
        self.left = left
        self.right = right
        self.up_dir_diff = up_dir_diff
        self.down_dir_diff = down_dir_diff
        self.left_dir_diff = left_dir_diff
        self.right_dir_diff = right_dir_diff

    def get_up(self):
        if self.up and self.up.empty:
            return self.up, self.up_dir_diff
        else:
            return self, 0

    def get_down(self):
        if self.down and self.down.empty:
            return self.down, self.down_dir_diff
        else:
            return self, 0

    def get_left(self):
        if self.left and self.left.empty:
            return self.left, self.left_dir_diff
        else:
            return self, 0

    def get_right(self):
        if self.right and self.right.empty:
            return self.right, self.right_dir_diff
        else:
            return self, 0


def parse_inputs(input_line):
    input_list = list()
    buf = ""
    for c in input_line:
        if c in "RL":
            if len(buf) > 0:
                input_list.append(int(buf))
                buf = ""
            input_list.append(c)
        else:
            buf += c
    if len(buf) > 0:
        input_list.append(int(buf))
    return input_list


def parse_map(map_lines):
    line_len = max([len(line) for line in map_lines])
    new_lines = list()
    for line in map_lines:
        buf = ""
        for i in range(line_len):
            if i >= len(line) or line[i] == " ":
                buf += "O"
            else:
                buf += line[i]
        new_lines.append(buf)
        buf = ""
    map2d = Map2d.from_lines("\n".join(new_lines))
    return map2d, new_lines


def fix_map(map2d):
    for i in range(len(map2d.obstacle_str)):
        if map2d.get_index(i) == "O":
            map2d.set_index(i, " ")


def flowing_graph(map2d, map_lines, new_lines):
    line_len = max([len(line) for line in map_lines])
    top_line = dict()
    bottom_line = dict()
    portals = defaultdict(list)
    for j in range(len(new_lines)):
        start = -1
        end = -1
        for i in range(line_len):
            if new_lines[j][i] == "O":
                if start != -1 and end == -1:
                    end = (i - 1, j)
                continue
            if i not in top_line:
                top_line[i] = j
            bottom_line[i] = j
            if start == -1:
                start = (i, j)
        if end == -1:
            end = (line_len - 1, j)
        log.debug(start)
        log.debug(end)
        if map2d.get_point(start) == "." and map2d.get_point(end) == ".":
            portals[start].append(end)
            portals[end].append(start)
    for i in range(line_len):
        if map2d.get_point((i, top_line[i])) == "." and map2d.get_point(
            (i, bottom_line[i])
        ):
            portals[i, top_line[i]].append((i, bottom_line[i]))
            portals[i, bottom_line[i]].append((i, top_line[i]))
    count = 0
    # log.debug(top_line)
    # log.debug(bottom_line)
    # log.debug(portals)
    # debug_map = Map2d(map2d.obstacle_str, map2d.bounds)
    # for a,b in portals:
    #     if count % 2 == 0:
    #         debug_map.set_point(a, chr(ord('a')+count//2))
    #         debug_map.set_point(b, chr(ord('a')+count//2))
    #     count += 1
    # log.debug(debug_map)
    map2d.set_portals_points(portals)
    nodes = dict()
    for i in range(len(map2d.obstacle_str)):
        if map2d.get_index(i) == ".":
            nodes[i] = Node()
    for i in nodes:
        protodict = {"down": None, "up": None, "left": None, "right": None}
        for j in map2d.nearby_indexes(i):
            u = map2d.translate_index(i)
            v = map2d.translate_index(j)
            if u[0] == v[0]:
                if u[1] == v[1] + 1 and map2d.get_point(v) == ".":
                    protodict["up"] = nodes[map2d.translate_point(v)]
                if u[1] == v[1] - 1 and map2d.get_point(v) == ".":
                    protodict["down"] = nodes[map2d.translate_point(v)]
                if u[1] - v[1] > 1 and map2d.get_point(v) == ".":
                    protodict["down"] = nodes[map2d.translate_point(v)]
                if v[1] - u[1] > 1 and map2d.get_point(v) == ".":
                    protodict["up"] = nodes[map2d.translate_point(v)]
            elif u[1] == v[1]:
                if u[0] == v[0] + 1 and map2d.get_point(v) == ".":
                    protodict["left"] = nodes[map2d.translate_point(v)]
                if u[0] == v[0] - 1 and map2d.get_point(v) == ".":
                    protodict["right"] = nodes[map2d.translate_point(v)]
                if u[0] - v[0] > 1 and map2d.get_point(v) == ".":
                    protodict["right"] = nodes[map2d.translate_point(v)]
                if v[0] - u[0] > 1 and map2d.get_point(v) == ".":
                    protodict["left"] = nodes[map2d.translate_point(v)]
        # log.debug(protodict)
        nodes[i].set(
            protodict["up"], protodict["down"], protodict["left"], protodict["right"]
        )  # now we thinking with pointers
    start = None
    for i in range(len(map2d.obstacle_str)):
        if map2d.get_index(i) == ".":
            start = i
            break
    return nodes, start


def parse_data(in_data):
    data = list()
    for line in in_data.splitlines():
        data.append(line)
    map2d, new_lines = parse_map(data[:-2])
    input_list = parse_inputs(data[-1])
    return map2d, input_list, data[:-2], new_lines


def change_dir(p_dir, dir_diff):
    return (p_dir + dir_diff) % 4


def move(pos, p_dir):
    new_pos = None
    if dir_pad[p_dir] == ">":
        new_pos, dir_diff = pos.get_right()
    elif dir_pad[p_dir] == "<":
        new_pos, dir_diff = pos.get_left()
    elif dir_pad[p_dir] == "^":
        new_pos, dir_diff = pos.get_up()
    elif dir_pad[p_dir] == "v":
        new_pos, dir_diff = pos.get_down()
    return new_pos, change_dir(p_dir, dir_diff)


def process_input(inp, in_pos, in_p_dir):
    pos = in_pos
    p_dir = in_p_dir
    if type(inp) == int:
        for i in range(inp):
            pos, p_dir = move(pos, p_dir)
    elif inp in "RL":
        if inp == "R":
            p_dir = change_dir(p_dir, 1)
        else:
            p_dir = change_dir(p_dir, -1)
    return pos, p_dir


def log_debug_position(map2d, point, p_dir):
    map2d.set_point(point, p_dir)
    log.debug(map2d)
    map2d.set_point(point, ".")


def part1(in_data, test=False):
    map2d, input_list, map_lines, new_lines = parse_data(in_data)
    nodes, start = flowing_graph(map2d, map_lines, new_lines)
    p_dir = 0
    pos = nodes[start]
    for inp in input_list:
        pos, p_dir = process_input(inp, pos, p_dir)
        point = map2d.translate_index([x for x in nodes if nodes[x] == pos][0])
        log_debug_position(map2d, point)
    end = map2d.translate_index([x for x in nodes if nodes[x] == pos][0])
    return 1000 * (end[1] + 1) + 4 * (end[0] + 1) + p_dir


def cube_graph(map2d, map_lines, new_lines, side_dict, dir_diff_dict):
    nodes = dict()
    start = None
    cube_edge_len = int(
        math.sqrt(
            sum(
                [
                    1
                    for x in range(len(map2d.obstacle_str))
                    if map2d.get_index(x) in "#."
                ]
            )
            // 6
        )
    )
    sides = defaultdict(list)
    nodes = dict()
    for i in range(len(map2d.obstacle_str)):
        p = map2d.translate_index(i)
        if (p[0] // cube_edge_len, p[1] // cube_edge_len) in side_dict:
            sides[side_dict[(p[0] // cube_edge_len, p[1] // cube_edge_len)]].append(p)
            nodes[i] = Node()
    # sanity check
    assert (
        sum([len(sides[side]) for side in sides]) == 6 * cube_edge_len * cube_edge_len
    )
    edges = {
        1: defaultdict(list),
        2: defaultdict(list),
        3: defaultdict(list),
        4: defaultdict(list),
        5: defaultdict(list),
        6: defaultdict(list),
    }
    for side in range(1, 7):
        min_x = min([p[0] for p in sides[side]])
        min_y = min([p[1] for p in sides[side]])
        max_x = max([p[0] for p in sides[side]])
        max_y = max([p[1] for p in sides[side]])
        side_orient_dict = {
            "left": ((min_x, min_y), (min_x, max_y)),
            "right": ((max_x, min_y), (max_x, max_y)),
            "up": ((min_x, min_y), (max_x, min_y)),
            "down": ((min_x, max_y), (max_x, max_y)),
        }
        for side_edge in side_orient_dict:
            for x in range(
                side_orient_dict[side_edge][0][0], side_orient_dict[side_edge][1][0] + 1
            ):
                for y in range(
                    side_orient_dict[side_edge][0][1],
                    side_orient_dict[side_edge][1][1] + 1,
                ):
                    edges[side][side_edge].append((x, y))
    # Ok, we have the sides, now we need to connect them
    for i in nodes:
        if map2d.get_index(i) != ".":
            continue
        p = map2d.translate_index(i)
        p_side = [s for s in sides if p in sides[s]][0]
        p_edges = list()
        for edge in edges[p_side]:
            if p in edges[p_side][edge]:
                p_edges.append(edge)
        protodict = {
            "down": (None, 0),
            "up": (None, 0),
            "left": (None, 0),
            "right": (None, 0),
        }
        for q in map2d.nearby_points(p):
            if q not in sides[p_side]:
                continue  # skip points from other sides, we need to process them differently
            if p[0] == q[0]:
                if p[1] == q[1] + 1 and map2d.get_point(q) == ".":
                    protodict["up"] = (nodes[map2d.translate_point(q)], 0)
                if p[1] == q[1] - 1 and map2d.get_point(q) == ".":
                    protodict["down"] = (nodes[map2d.translate_point(q)], 0)
            elif p[1] == q[1]:
                if p[0] == q[0] + 1 and map2d.get_point(q) == ".":
                    protodict["left"] = (nodes[map2d.translate_point(q)], 0)
                if p[0] == q[0] - 1 and map2d.get_point(q) == ".":
                    protodict["right"] = (nodes[map2d.translate_point(q)], 0)
        if len(p_edges) > 0:
            # now's the time to connect it up
            for edge in p_edges:
                n_side, n_edge, dir_diff, is_inverse = dir_diff_dict[p_side][edge]
                starting_edge = edges[p_side][edge]
                target_edge = edges[n_side][n_edge]
                edge_index = starting_edge.index(p)
                if is_inverse:
                    target_point = cube_edge_len - 1 - edge_index
                else:
                    target_point = edge_index
                if map2d.get_point(target_edge[target_point]) == ".":
                    protodict[edge] = (
                        nodes[map2d.translate_point(target_edge[target_point])],
                        dir_diff,
                    )
        nodes[i].set(
            protodict["up"][0],
            protodict["down"][0],
            protodict["left"][0],
            protodict["right"][0],
            protodict["up"][1],
            protodict["down"][1],
            protodict["left"][1],
            protodict["right"][1],
            True,
        )  # now we thinking with pointers
    start = None
    for i in range(len(map2d.obstacle_str)):
        if map2d.get_index(i) == ".":
            start = i
            break
    return nodes, start


# this will work only for the layout in my input:
# make a playing die - opposite sides add up to 7
# sort the points into sides
#
# .12
# .3.
# 56.
# 4..
#
prod_side_dict = {
    (1, 0): 1,
    (2, 0): 2,
    (1, 1): 3,
    (0, 3): 4,
    (0, 2): 5,
    (1, 2): 6,
}

#
# .12
# .3.
# 56.
# 4..
#
# dir_pad = ">v<^"
#
# I am mapping the sides of the squares above
# side, edge, dir_diff, is_inverse (side starts from the smaller point to the bigger one)
prod_dir_diff_dict = {
    1: {
        "right": (2, "left", 0, False),
        "down": (3, "up", 0, False),
        "up": (4, "left", -3, False),
        "left": (5, "left", -2, True),
    },
    2: {
        "right": (6, "right", 2, True),
        "down": (3, "right", 1, False),
        "up": (4, "down", 0, False),
        "left": (1, "right", 0, False),
    },
    3: {
        "right": (2, "down", 3, False),
        "down": (6, "up", 0, False),
        "up": (1, "down", 0, False),
        "left": (5, "up", -1, False),
    },
    4: {
        "right": (6, "down", 3, False),
        "down": (2, "up", 0, False),
        "up": (5, "down", 0, False),
        "left": (1, "up", -1, False),
    },
    5: {
        "right": (6, "left", 0, False),
        "down": (4, "up", 0, False),
        "up": (3, "left", -3, False),
        "left": (1, "left", -2, True),
    },
    6: {
        "right": (2, "right", 2, True),
        "down": (4, "right", 1, False),
        "up": (3, "down", 0, False),
        "left": (5, "right", 0, False),
    },
}  # that was painful, would love to see a general solution
# holy shit, it works.


def part2(in_data, test=False):
    map2d, input_list, map_lines, new_lines = parse_data(in_data)
    nodes, start = cube_graph(
        map2d, map_lines, new_lines, prod_side_dict, prod_dir_diff_dict
    )
    p_dir = 0
    fix_map(map2d)
    pos = nodes[start]
    for inp in input_list:
        # log.debug(inp)
        pos, p_dir = process_input(inp, pos, p_dir)
        point = map2d.translate_index([x for x in nodes if nodes[x] == pos][0])
        # log_debug_position(map2d, point, dir_pad[p_dir%4])
    end = map2d.translate_index([x for x in nodes if nodes[x] == pos][0])
    return 1000 * (end[1] + 1) + 4 * (end[0] + 1) + p_dir
