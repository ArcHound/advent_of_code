from enum import Enum
from dataclasses import dataclass


class PipeType(Enum):
    TopLeft = "TopLeft"
    TopRight = "TopRight"
    TopDown = "TopDown"
    LeftRight = "LeftRight"
    LeftDown = "LeftDown"
    RightDown = "RightDown"
    NoPipe = "NoPipe"


class PipeMap2d:
    pipe_parts = {
        PipeType.TopLeft: ("#.#", "..#", "###"),
        PipeType.TopRight: ("#.#", "#..", "###"),
        PipeType.TopDown: ("#.#", "#.#", "#.#"),
        PipeType.LeftRight: ("###", "...", "###"),
        PipeType.LeftDown: ("###", "..#", "#.#"),
        PipeType.RightDown: ("###", "#..", "#.#"),
        PipeType.NoPipe: ("###", "###", "###"),
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

    def get_flooded_val(self, point):
        return self.inner_map.get_flooded_val((point[0] * 3 + 1, point[1] * 3 + 1)) // 3

    def clear_flood(self):
        self.inner_map.clear_flood()

    def get_flood_max(self):
        p, val = self.inner_map.get_flood_max()
        return {(x[0] // 3, x[1] // 3) for x in p}, val // 3


# points are tuples (0,1) - point[0] is x, point[1] is y
class Map2d:
    obstacle_sym = "#"
    empty_sym = "."

    @classmethod
    def from_obstacle_list(cls, obstacles, bounds, diagonal=False):
        obstacle_str = ""
        for j in range(bounds[0][1], bounds[1][1]):
            for i in range(bounds[0][0], bounds[1][0]):
                if (i, j) in obstacles:
                    obstacle_str += Map2d.obstacle_sym
                else:
                    obstacle_str += Map2d.empty_sym
        return cls(obstacle_str, bounds, diagonal)

    def __init__(self, obstacle_str, bounds=((0, 0), (200, 200)), diagonal=False):
        self.obstacle_str = obstacle_str
        self.diagonal = diagonal
        self.minimal = bounds[0]
        self.maximal = bounds[1]
        self.x_len = self.maximal[0] - self.minimal[0]
        self.y_len = self.maximal[1] - self.minimal[1]
        if self.x_len * self.y_len != len(obstacle_str):
            raise ValueError(
                f"Bounds {bounds} cannot be mapped onto str of len {len(obstacle_str)}"
            )
        self.flooded = list(self.x_len * self.y_len * [-1])

    def translate_coordinates(self, point):
        return (point[1] - self.minimal[1]) * self.x_len + (point[0] - self.minimal[0])

    def translate_index(self, index):
        return (
            index % self.x_len + self.minimal[0],
            index // self.x_len + self.minimal[1],
        )

    @classmethod
    def empties_to_obstacles(cls, empties, bounds):
        return [
            (i, j)
            for i in range(bounds[0][0], bounds[1][0])
            for j in range(bounds[0][1], bounds[1][1])
            if (i, j) not in empties
        ]

    def in_bounds(self, point):
        return (
            point[0] >= self.minimal[0]
            and point[0] < self.maximal[0]
            and point[1] >= self.minimal[1]
            and point[1] < self.maximal[1]
        )

    def in_bounds_index(self, index):
        return index >= 0 and index < self.x_len * self.y_len

    # can't see points out of bounds
    def nearby_points(self, point):
        if self.diagonal:
            return [
                (point[0] + i, point[1] + j)
                for i in range(-1, 2)
                for j in range(-1, 2)
                if (i != 0 or j != 0) and self.in_bounds((point[0] + i, point[1] + j))
            ]
        else:
            return [
                x
                for x in [
                    (point[0] - 1, point[1]),
                    (point[0] + 1, point[1]),
                    (point[0], point[1] - 1),
                    (point[0], point[1] + 1),
                ]
                if self.in_bounds(x)
            ]

    def nearby_indexes(self, index):
        point = self.translate_index(index)
        return [self.translate_coordinates(p) for p in self.nearby_points(point)]

    def debug_draw(self):
        drawing = "\n"
        for j in range(self.minimal[1], self.maximal[1]):
            for i in range(self.minimal[0], self.maximal[0]):
                if (
                    self.obstacle_str[self.translate_coordinates((i, j))]
                    == Map2d.obstacle_sym
                ):
                    drawing += Map2d.obstacle_sym
                elif self.flooded[self.translate_coordinates((i, j))] != -1:
                    if self.flooded[self.translate_coordinates((i, j))] < 10:
                        drawing += str(self.flooded[self.translate_coordinates((i, j))])
                    elif (
                        self.flooded[self.translate_coordinates((i, j))] >= 10
                        and self.flooded[self.translate_coordinates((i, j))] < 36
                    ):
                        drawing += chr(
                            ord("a")
                            + self.flooded[self.translate_coordinates((i, j))]
                            - 10
                        )
                    else:
                        drawing += "+"
                else:
                    drawing += Map2d.empty_sym
            drawing += "\n"
        return drawing

    def get_flooded_val(self, point):
        return self.flooded[self.translate_coordinates(point)]

    def flood(self, starting_point):
        starting_index = self.translate_coordinates(starting_point)
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

    def clear_flood(self):
        self.flooded = list(self.x_len * self.y_len * [-1])

    def get_flood_max(self):
        max_val = max([self.flooded[x] for x in range(len(self.flooded))])
        return {
            self.translate_index(x)
            for x in range(len(self.flooded))
            if self.flooded[x] == max_val
        }, max_val
