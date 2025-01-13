# 2022-22

import logging
from collections import defaultdict
from aoc_lib.map2d import Map2d

log = logging.getLogger("aoc_logger")


class Node:

    def __init__(self):
        self.up = None
        self.down = None
        self.left = None
        self.right = None

    def set(self, up, down, left, right):
        self.up = up
        self.down = down
        self.left = left
        self.right = right

    def get_up(self):
        if self.up:
            return self.up
        else:
            return self

    def get_down(self):
        if self.down:
            return self.down
        else:
            return self

    def get_left(self):
        if self.left:
            return self.left
        else:
            return self

    def get_right(self):
        if self.right:
            return self.right
        else:
            return self


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
    for i in range(len(map2d.obstacle_str)):
        if map2d.get_index(i) == "O":
            map2d.set_index(i, "#")
    return map2d, nodes


def parse_data(in_data):
    data = list()
    for line in in_data.splitlines():
        data.append(line)
    map2d, nodes = parse_map(data[:-2])
    input_list = parse_inputs(data[-1])
    start = None
    for i in range(len(map2d.obstacle_str)):
        if map2d.get_index(i) == ".":
            start = i
            break
    return map2d, input_list, nodes, start


dir_pad = ">v<^"


def part1(in_data, test=False):
    map2d, input_list, nodes, start = parse_data(in_data)
    p_dir = 0
    log.debug(input_list)
    log.debug(map2d)
    pos = nodes[start]
    for inp in input_list:
        if type(inp) == int:
            for i in range(inp):
                if dir_pad[p_dir] == ">":
                    pos = pos.get_right()
                elif dir_pad[p_dir] == "<":
                    pos = pos.get_left()
                elif dir_pad[p_dir] == "^":
                    pos = pos.get_up()
                elif dir_pad[p_dir] == "v":
                    pos = pos.get_down()
        elif inp in "RL":
            if inp == "R":
                p_dir = (p_dir + 1) % 4
            else:
                p_dir = (p_dir - 1) % 4
        point = map2d.translate_index([x for x in nodes if nodes[x] == pos][0])
        map2d.set_point(point, "O")
        log.debug(map2d)
        map2d.set_point(point, ".")
    end = map2d.translate_index([x for x in nodes if nodes[x] == pos][0])
    return 1000 * (end[1] + 1) + 4 * (end[0] + 1) + p_dir


def part2(in_data, test=False):
    data = parse_data(in_data)
    return "part2 output 2022-22"
