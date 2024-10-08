# 2019-18
import logging
from aoc_lib.map2d import Map2d
from collections import deque, defaultdict

log = logging.getLogger("aoc_logger")

all_doors = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
all_keys = "abcdefghijklmnopqrstuvwxyz"
player_chr = "@"


def special_bfs(map2d, root, key_target, key_dict, door_dict):
    q = deque()
    explored = defaultdict(list)
    explored[""] = [root]
    cache = dict()
    start = (root, frozenset(), "", 0)
    q.append(start)
    while len(q) > 0:
        q = deque(sorted(q, key=lambda x: x[3]))
        # q = deque(sorted(q, key=lambda x: len(x[1])))
        # log.debug(q)
        v, inv, str_inv, steps = q.popleft()
        if all([k in inv for k in key_target]):
            return steps
        edges = keyed_flood(map2d, v, inv, key_target, key_dict, door_dict, cache)
        for k in edges:
            buffer = list()
            if k not in explored[inv]:
                explored[inv].append(k)
                buffer.append(
                    (
                        key_dict[k],
                        frozenset(list(inv) + [k]),
                        str_inv + k,
                        steps + edges[k],
                    )
                )
                # buffer.append((key_dict[k], inv+k, steps+edges[k]))
            buffer.sort(key=lambda x: x[3])
            for b in buffer:
                q.append(b)


def keyed_flood(map2d, position, keys, key_target, key_dict, door_dict, cache):
    if (position, keys) in cache:
        return cache[(position, keys)]
    # log.debug('~~~~')
    # log.debug(position)
    # log.debug(keys)
    map_copy = Map2d(map2d.obstacle_str, map2d.bounds)
    for d in door_dict:
        if d.lower() in keys:
            map_copy.set_index(door_dict[d.upper()], Map2d.empty_sym)
        else:
            map_copy.set_index(door_dict[d.upper()], Map2d.obstacle_sym)
    map_copy.flood(map_copy.translate_index(position))
    missing_keys = [x for x in key_target if x not in keys]
    cache[(position, keys)] = {
        x: map_copy.get_flooded_index(key_dict[x])
        for x in missing_keys
        if map_copy.get_flooded_index(key_dict[x]) > 0
    }
    # log.debug(map_copy.debug_draw())
    # log.debug('~~~~')
    return cache[(position, keys)]


def part1(in_data, test=False):
    map2d = Map2d.from_lines(in_data)
    log.debug(map2d.debug_draw())
    player = None
    key_dict = dict()
    door_dict = dict()
    for i in range(len(map2d.obstacle_str)):
        if map2d.obstacle_str[i] in all_keys:
            key_dict[map2d.obstacle_str[i]] = i
        elif map2d.obstacle_str[i] in all_doors:
            door_dict[map2d.obstacle_str[i]] = i
        elif map2d.obstacle_str[i] == player_chr:
            player = i
    map2d.set_index(player, Map2d.empty_sym)
    for k in key_dict:
        map2d.set_index(key_dict[k], Map2d.empty_sym)
    log.debug({x: map2d.translate_index(key_dict[x]) for x in key_dict})
    log.debug({x: map2d.translate_index(door_dict[x]) for x in door_dict})
    log.debug(map2d.translate_index(player))
    log.debug(map2d.debug_draw())
    steps = special_bfs(
        map2d, player, "".join([x for x in key_dict]), key_dict, door_dict
    )
    return steps


def part2(in_data, test=False):
    map2d = Map2d.from_lines(in_data)
    log.debug(map2d.debug_draw())
    return "part2 output 2019-18"
