# 2024-12

import logging
from aoc_lib.map2d import Map2d, PipeMap2d, PipeType
from collections import defaultdict

log = logging.getLogger("aoc_logger")


def parse_plants(in_data):
    map2d = Map2d.from_lines(in_data)
    plant_set = set()
    for c in map2d.obstacle_str:
        plant_set.add(c)
    plant_map = defaultdict(str)
    # make a set of maps, for each letter one. I know they might have multiple regions
    for c in map2d.obstacle_str:
        plant_map[c] += "."
        for i in plant_set:
            if i != c:
                plant_map[i] += "#"
    plant_map_map = dict()
    for p in plant_set:
        plant_map_map[p] = Map2d(plant_map[p], map2d.bounds)
    return plant_set, plant_map_map


def part1(in_data, test=False):
    total = 0
    plant_set, plant_map_map = parse_plants(in_data)
    # now let's process those maps
    for plant in plant_map_map:
        p_map = plant_map_map[plant]
        for i in range(len(p_map.obstacle_str)):
            # find a region
            if p_map.get_index(i) == "." and p_map.get_flooded_index(i) == -1:
                # flood it
                p_map.flood(p_map.translate_index(i))
                plots = 0
                fences = 0
                # count flooded tiles
                for j in range(len(p_map.flooded)):
                    if p_map.flooded[j] != -1:
                        plots += 1
                        fences += 4 - len(
                            [
                                x
                                for x in p_map.nearby_indexes(j)
                                if p_map.flooded[x] != -1
                            ]
                        )  # check neighbors for fences
                set_count = 0
                # fill the region up so that we don't count duplicates
                for j in range(len(p_map.flooded)):
                    if p_map.flooded[j] != -1:
                        set_count += 1
                        p_map.set_index(j, "#")
                        p_map.flooded[j] = -1
                log.debug(f"{plant}: {plots} x {fences}")
                total += plots * fences
    return total


def part2(in_data, test=False):
    total = 0
    plant_set, plant_map_map = parse_plants(in_data)
    # now let's process those maps
    for plant in plant_map_map:
        p_map = plant_map_map[plant]
        for i in range(len(p_map.obstacle_str)):
            # find a region
            if p_map.get_index(i) == "." and p_map.get_flooded_index(i) == -1:
                # flood it
                p_map.flood(p_map.translate_index(i))
                plots = 0
                fences = 0
                flooded_points = dict()
                points = list()
                # plots are the same - each flooded tile corresponds to one plot
                # the fences though - idea is to count corners. The corners are more visible in expanded map as it drastically cuts down special cases of corner interactions.
                for j in range(len(p_map.flooded)):
                    if p_map.flooded[j] != -1:
                        flooded_points[p_map.translate_index(j)] = (
                            PipeType.Hole
                        )  # note down the empty area
                        plots += 1
                # expand:
                #       ...       ###
                #  . -> ...  # -> ###
                #       ...       ###
                pipe_p_map = PipeMap2d(flooded_points, p_map.bounds)
                for inner_j in range(len(pipe_p_map.inner_map.obstacle_str)):
                    if pipe_p_map.inner_map.get_index(inner_j) == ".":
                        neighbors = len(
                            [
                                x
                                for x in pipe_p_map.inner_map.nearby_indexes(
                                    inner_j, True
                                )
                                if pipe_p_map.inner_map.get_index(x) == "."
                            ]  # count the neigbors, including diagonal
                        )
                        # These are the corner cases (plus rotations):
                        #
                        # ..#   ...   .##
                        # ..#   ...   #..
                        # ###   ..#   #..
                        #
                        # the last one is when two corners touch.
                        # Fortunately, it counts them separately.
                        # as the map is tiled by 3x3, these are the rest of the tiles
                        # (if you iterate through '.' and look around them):
                        #
                        # ...   ###   ##.
                        # ...   ...   ...
                        # ...   ...   ...
                        #
                        # we can see that for corners, the neighbor nums are 3,4,7
                        if neighbors in [3, 4, 7]:
                            fences += 1

                set_count = 0
                # fill the region up so that we don't count duplicates
                for j in range(len(p_map.flooded)):
                    if p_map.flooded[j] != -1:
                        set_count += 1
                        p_map.set_index(j, "#")
                        p_map.flooded[j] = -1
                log.debug(f"{plant}: {plots} x {fences}")
                total += plots * fences
    return total
