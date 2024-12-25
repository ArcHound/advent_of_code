from __future__ import annotations
from enum import Enum
from dataclasses import dataclass
from typing import Tuple

import logging

log = logging.getLogger("aoc_logger")


class PipeType(Enum):
    TopLeft = "TopLeft"
    TopRight = "TopRight"
    TopDown = "TopDown"
    LeftRight = "LeftRight"
    LeftDown = "LeftDown"
    RightDown = "RightDown"
    NoPipe = "NoPipe"
    Hole = "Hole"


class PipeMap2d:
    pipe_parts = {
        PipeType.TopLeft: ("#.#", "..#", "###"),
        PipeType.TopRight: ("#.#", "#..", "###"),
        PipeType.TopDown: ("#.#", "#.#", "#.#"),
        PipeType.LeftRight: ("###", "...", "###"),
        PipeType.LeftDown: ("###", "..#", "#.#"),
        PipeType.RightDown: ("###", "#..", "#.#"),
        PipeType.NoPipe: ("###", "###", "###"),
        PipeType.Hole: ("...", "...", "..."),
    }

    def __init__(self, pipes, bounds=((0, 0), (200, 200))):
        self.bounds = bounds
        self.minimal = bounds[0]
        self.maximal = bounds[1]
        self.x_len = self.maximal[0] - self.minimal[0]
        self.y_len = self.maximal[1] - self.minimal[1]
        obstacle_str = ""
        for j in range(bounds[0][1], bounds[1][1]):
            lines = ["", "", ""]
            for i in range(bounds[0][0], bounds[1][0]):
                if (i, j) in pipes:
                    for k in range(3):
                        lines[k] += PipeMap2d.pipe_parts[pipes[(i, j)]][k]
                else:
                    for k in range(3):
                        lines[k] += PipeMap2d.pipe_parts[PipeType.NoPipe][k]
            obstacle_str += lines[0] + lines[1] + lines[2]
        self.inner_map = Map2d(
            obstacle_str,
            (
                (3 * bounds[0][0], 3 * bounds[0][1]),
                (3 * bounds[1][0], 3 * bounds[1][1]),
            ),
        )

    def flood(self, starting_point):
        self.inner_map.flood((starting_point[0] * 3 + 1, starting_point[1] * 3 + 1))

    def get_flooded_point(self, point):
        return (
            self.inner_map.get_flooded_point((point[0] * 3 + 1, point[1] * 3 + 1)) // 3
        )

    def clear_flood(self):
        self.inner_map.clear_flood()

    def get_flood_max_indexes(self):
        p, val = self.inner_map.get_flood_max_indexes()
        return {(x[0] // 3, x[1] // 3) for x in p}, val // 3


# points are tuples (0,1) - point[0] is x, point[1] is y
class Map2d:
    obstacle_sym = "#"
    empty_sym = "."
    obj_sym = "O"

    ### --------------------------------------------------------------------------
    ###     Constructors Methods
    ### --------------------------------------------------------------------------

    @classmethod
    def from_point_dict(
        cls,
        pointdict: dict[Tuple[int, int], chr],
        bounds: Tuple[Tuple[int, int], Tuple[int, int]] = None,
        diagonal=False,
    ) -> Map2d:
        """Constructs a map from dict of points to obstacles"""
        if not bounds:
            xs = [k[0] for k in pointdict]
            ys = [k[1] for k in pointdict]
            bounds = ((min(xs), min(ys)), (max(xs) + 1, max(ys) + 1))
        progress = cls.from_obstacle_list([], bounds, diagonal)
        for k, i in pointdict.items():
            progress.set_point(k, i)
        return progress

    @classmethod
    def from_obstacle_list(
        cls,
        obstacles: list[Tuple[int, int]],
        bounds: Tuple[Tuple[int, int], Tuple[int, int]] = None,
        diagonal=False,
    ) -> Map2d:
        """Constructs a map from list of points that are obstacles, rest are empties"""
        if not bounds:
            xs = [k[0] for k in obstacles]
            ys = [k[1] for k in obstacles]
            bounds = ((min(xs), min(ys)), (max(xs) + 1, max(ys) + 1))
        obstacle_str = ""
        for j in range(bounds[0][1], bounds[1][1]):
            for i in range(bounds[0][0], bounds[1][0]):
                if (i, j) in obstacles:
                    obstacle_str += Map2d.obstacle_sym
                else:
                    obstacle_str += Map2d.empty_sym
        return cls(obstacle_str, bounds, diagonal)

    @classmethod
    def from_lines(cls, in_data: str, diagonal=False) -> Map2d:
        """Constructs a map from the most typical AOC format - lines of strings with obstacles and empties"""
        buf = ""
        x_len = 0
        y_len = 0
        for line in in_data.splitlines():
            if line != "":
                buf += line.strip()
                y_len += 1
                x_len = len(line.strip())
        return cls(buf, ((0, 0), (x_len, y_len)), diagonal=diagonal)

    @classmethod
    def copy(cls, other: Map2d) -> Map2d:
        return Map2d(other.obstacle_str, other.bounds, other.diagonal)

    def __init__(
        self,
        obstacle_str: str,
        bounds: Tuple[Tuple[int, int], Tuple[int, int]] = ((0, 0), (200, 200)),
        diagonal=False,
    ) -> Map2d:
        """Basic constructor - good for copying as it uses bounds and obstacle_str"""
        self.obstacle_str = str(obstacle_str)
        self.diagonal = diagonal
        self.bounds = bounds
        self.minimal = bounds[0]
        self.maximal = bounds[1]
        self.portals = dict()
        self.x_len = self.maximal[0] - self.minimal[0]
        self.y_len = self.maximal[1] - self.minimal[1]
        if self.x_len * self.y_len != len(obstacle_str):
            raise ValueError(
                f"Bounds {bounds} cannot be mapped onto str of len {len(obstacle_str)}"
            )
        self.flooded = list(self.x_len * self.y_len * [-1])

    def __eq__(self, other: Map2d) -> bool:
        """Two maps are equal if they have the same obstacle layout and dimensions"""
        return (
            self.obstacle_str == other.obstacle_str
            and self.x_len == other.x_len
            and self.y_len == other.y_len
        )

    def __str__(self) -> str:
        """Represent the map via the debug draw method"""
        return self.debug_draw()

    ### --------------------------------------------------------------------------
    ###     Index/Point Methods
    ### --------------------------------------------------------------------------

    def translate_point(self, point: Tuple[int, int]) -> int:
        """returns index corresponding to that point (no safety checks)"""
        return (point[1] - self.minimal[1]) * self.x_len + (point[0] - self.minimal[0])

    def translate_index(self, index: int) -> Tuple[int, int]:
        """returns point corresponding to that index (no safety checks)"""
        return (
            index % self.x_len + self.minimal[0],
            index // self.x_len + self.minimal[1],
        )

    def get_point(self, point: Tuple[int, int]) -> chr:
        """what is on that point?"""
        return self.obstacle_str[self.translate_point(point)]

    def get_index(self, index: int) -> chr:
        """what is on that index?"""
        return self.obstacle_str[index]  # duh

    def invert_point(self, point: Tuple[int, int]):
        """sets empty to obstacle, obstacle to empty or leaves it as it is"""
        i = self.translate_point(point)
        new_c = self.obstacle_str[i]
        if self.obstacle_str[i] == Map2d.obstacle_sym:
            new_c = Map2d.empty_sym
        else:
            new_c = Map2d.obstacle_sym
        self.obstacle_str = self.obstacle_str[:i] + new_c + self.obstacle_str[i + 1 :]

    def set_point(self, point: Tuple[int, int], val: chr):
        new_c = ""
        i = self.translate_point(point)
        self.obstacle_str = self.obstacle_str[:i] + val + self.obstacle_str[i + 1 :]

    def set_index(self, index: int, val: chr):
        if 0 <= index and index < len(self.obstacle_str):
            self.obstacle_str = (
                self.obstacle_str[:index] + val + self.obstacle_str[index + 1 :]
            )
        else:
            raise ValueError(f"Index {index} out of bounds")

    def in_bounds_point(self, point: Tuple[int, int]) -> bool:
        """is that point in bounds?"""
        return (
            point[0] >= self.minimal[0]
            and point[0] < self.maximal[0]
            and point[1] >= self.minimal[1]
            and point[1] < self.maximal[1]
        )

    def in_bounds_index(self, index: int) -> bool:
        """is that index in bounds?"""
        return index >= 0 and index < len(self.obstacle_str)

    ### --------------------------------------------------------------------------
    ###     Navigating Methods
    ### --------------------------------------------------------------------------

    def set_portals_points(self, portals: dict[Tuple[int, int], list[Tuple[int, int]]]):
        # ok, this needs explaining
        # basicaly a digraph in a dict
        # point to list of points
        # by default it should return empty list, beware in nearby points
        self.portals = portals

    def nearby_points(self, point: Tuple[int, int], diagonal: bool = None):
        """Nearby points of a given point within the map (accounts for portals)"""
        if (diagonal is None and self.diagonal) or diagonal:
            return [
                (point[0] + i, point[1] + j)
                for i in range(-1, 2)
                for j in range(-1, 2)
                if (i != 0 or j != 0)
                and self.in_bounds_point((point[0] + i, point[1] + j))
            ] + self.portals.get(point, list())
        else:
            return [
                x
                for x in [
                    (point[0] - 1, point[1]),
                    (point[0] + 1, point[1]),
                    (point[0], point[1] - 1),
                    (point[0], point[1] + 1),
                ]
                if self.in_bounds_point(x)
            ] + self.portals.get(point, list())

    def nearby_indexes(self, index: int, diagonal: bool = None) -> list[int]:
        """Nearby indexes of a given point within the map (accounts for portals)"""
        point = self.translate_index(index)
        return [self.translate_point(p) for p in self.nearby_points(point, diagonal)]

    ### --------------------------------------------------------------------------
    ###     Flood Methods
    ### --------------------------------------------------------------------------

    def get_flooded_point(self, point: Tuple[int, int]) -> int:
        """The shortest distance from the start as it was on the last flood. -1 for unreachable"""
        return self.flooded[self.translate_point(point)]

    def get_flooded_index(self, index: int) -> int:
        """The shortest distance from the start as it was on the last flood. -1 for unreachable"""
        return self.flooded[index]

    def flood(self, starting_point: Tuple[int, int]):
        """Start at the point, BFS, rate every reachable point"""
        starting_index = self.translate_point(starting_point)
        processing = [starting_index]
        self.flooded[starting_index] = 0
        while len(processing) > 0:
            process = processing.pop(0)
            for p in self.nearby_indexes(process):
                if (
                    not self.in_bounds_index(p)
                    or self.obstacle_str[p] == Map2d.obstacle_sym
                    or self.flooded[p] != -1
                ):
                    continue
                self.flooded[p] = self.flooded[process] + 1
                processing.append(p)

    def iterative_flood_indexes(
        self, starting_point: Tuple[int, int], steps: int
    ) -> list[Tuple[int, int]]:
        """I don't even. Seems I needed some kind of wave?"""
        starting_index = self.translate_point(starting_point)
        processing = [starting_index]
        for i in range(steps):
            new_processing = set()
            for process in processing:
                for p in self.nearby_indexes(process):
                    if (
                        not self.in_bounds_index(p)
                        or self.obstacle_str[p] == Map2d.obstacle_sym
                    ):
                        continue
                    else:
                        new_processing.add(p)
            processing = list(new_processing)
        return processing

    def clear_flood(self):
        self.flooded = list(self.x_len * self.y_len * [-1])

    def get_flood_max_indexes(self) -> Tuple[list[int], int]:
        """Returns a list of indexes that have the maximum value after a flood + the maximum value"""
        max_val = max([self.flooded[x] for x in range(len(self.flooded))])
        return [
            self.translate_index(x)
            for x in range(len(self.flooded))
            if self.flooded[x] == max_val
        ], max_val

    ### --------------------------------------------------------------------------
    ###     Other Methods
    ### --------------------------------------------------------------------------

    @classmethod
    def empties_to_obstacles(
        cls,
        empties: list[Tuple[int, int]],
        bounds: Tuple[Tuple[int, int], Tuple[int, int]],
    ) -> list[Tuple[int, int]]:
        """Empties to obstacles, keep the rest intact (no idea what I was thinking)"""
        return [
            (i, j)
            for i in range(bounds[0][0], bounds[1][0])
            for j in range(bounds[0][1], bounds[1][1])
            if (i, j) not in empties
        ]

    def invert_obstacles(self):
        """Empties to obstacles, obstacles to empties, keep the rest intact"""
        new_obst_str = ""
        for c in self.obstacle_str:
            if c == Map2d.obstacle_sym:
                new_obst_str += Map2d.empty_sym
            else:
                new_obst_str += Map2d.obstacle_sym
        self.obstacle_str = new_obst_str

    def trace(
        self,
        start: Tuple[int, int],
        vector: Tuple[int, int],
        until_obstacle: bool = True,
    ):
        """Gets points on the grid from start with selected vector (ray trace). Might stop until an obstacle is hit or at the end of bounds"""
        point = (start[0], start[1])
        line = [point]
        while self.in_bounds_point((point[0] + vector[0], point[1] + vector[1])):
            point = (point[0] + vector[0], point[1] + vector[1])
            line.append(point)
            if until_obstacle and self.get_point(point) == Map2d.obstacle_sym:
                break
        return line

    def find_reflection_axes(self) -> Tuple[int, int]:
        """Finds if there's an x (or y) so that the map is symmetrical with respect to that axis"""
        # horizontal
        h_axis = None
        for j in range(1, self.y_len):
            match = True
            for k in range(1, min([j, self.y_len - j]) + 1):
                for i in range(0, self.x_len):
                    if self.get_point((i, j + k - 1)) != self.get_point((i, j - k)):
                        match = False
                        break
                if not match:
                    break
            if match:
                h_axis = j
                break
        # vertical
        v_axis = None
        for i in range(1, self.x_len):
            match = True
            for k in range(1, min([i, self.x_len - i]) + 1):
                for j in range(0, self.y_len):
                    if self.get_point((i + k - 1, j)) != self.get_point((i - k, j)):
                        match = False
                        break
                if not match:
                    break
            if match:
                v_axis = i
                break
        return h_axis, v_axis

    def debug_draw(self) -> str:
        """Draws the map - also draws flooded vals if it's flooded"""
        drawing = "\n"
        for j in range(self.minimal[1], self.maximal[1]):
            for i in range(self.minimal[0], self.maximal[0]):
                if (
                    self.obstacle_str[self.translate_point((i, j))]
                    == Map2d.obstacle_sym
                ):
                    drawing += Map2d.obstacle_sym
                elif self.flooded[self.translate_point((i, j))] != -1:
                    if self.flooded[self.translate_point((i, j))] < 10:
                        drawing += str(self.flooded[self.translate_point((i, j))])
                    elif (
                        self.flooded[self.translate_point((i, j))] >= 10
                        and self.flooded[self.translate_point((i, j))] < 36
                    ):
                        drawing += chr(
                            ord("a") + self.flooded[self.translate_point((i, j))] - 10
                        )
                    else:
                        drawing += "+"
                else:
                    drawing += self.obstacle_str[self.translate_point((i, j))]
            drawing += "\n"
        return drawing
