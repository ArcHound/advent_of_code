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
    map_cache = dict()
    start = (root, frozenset(), 0)
    pos_cache = dict()
    pos_cache[(root, frozenset())] = 0
    q.append(start)
    while len(q) > 0:
        q = deque(sorted(q, key=lambda x: x[2]))
        # q = deque(sorted(q, key=lambda x: len(x[1])))
        # log.debug(q)
        v, inv, steps = q.popleft()
        if all([k in inv for k in key_target]):
            continue
        edges = keyed_flood(map2d, v, inv, key_target, key_dict, door_dict, map_cache)
        for k in edges:
            buffer = list()
            new_inv = frozenset(list(inv) + [k])
            if (key_dict[k], new_inv) not in pos_cache or pos_cache[
                (key_dict[k], new_inv)
            ] > steps + edges[k]:
                buffer.append(
                    (
                        key_dict[k],
                        new_inv,
                        steps + edges[k],
                    )
                )
                pos_cache[(key_dict[k], new_inv)] = steps + edges[k]
                # buffer.append((key_dict[k], inv+k, steps+edges[k]))
            buffer.sort(key=lambda x: x[2])
            for b in buffer:
                q.append(b)
    return min(
        [pos_cache[(x, inv)] for x, inv in pos_cache if len(inv) == len(key_dict)]
    )


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


def translate_map(map2d, player):
    log.debug(map2d.debug_draw())
    map_copy = Map2d.copy(map2d)
    indexes = map_copy.nearby_indexes(player, True)
    indexes.sort()
    log.debug(indexes)
    index_map = ["@", "#", "@", "#", "#", "@", "#", "@"]
    players = list()
    map_copy.set_index(player, "#")
    for x in range(8):
        i = indexes[x]
        c = index_map[x]
        if c == "@":
            players.append(i)
            map_copy.set_index(i, ".")
        else:
            map_copy.set_index(i, "#")
    return map_copy, tuple(players)


def special_bfs_2(map2d, players, key_target, key_dict, door_dict):
    q = deque()
    map_cache = dict()
    start = (players, frozenset(), 0)
    pos_cache = dict()
    pos_cache[(players, frozenset())] = 0
    q.append(start)
    while len(q) > 0:
        q = deque(sorted(q, key=lambda x: x[2]))
        # q = deque(sorted(q, key=lambda x: len(x[1])))
        # log.debug(q)
        players, inv, steps = q.popleft()
        if all([k in inv for k in key_target]):
            continue
        for i in range(len(players)):
            edges = keyed_flood(
                map2d, players[i], inv, key_target, key_dict, door_dict, map_cache
            )
            for k in edges:
                new_players = list(players)
                new_players[i] = key_dict[k]
                new_players = tuple(new_players)
                buffer = list()
                new_inv = frozenset(list(inv) + [k])
                if (new_players, new_inv) not in pos_cache or pos_cache[
                    (new_players, new_inv)
                ] > steps + edges[k]:
                    buffer.append(
                        (
                            new_players,
                            new_inv,
                            steps + edges[k],
                        )
                    )
                    pos_cache[(new_players, new_inv)] = steps + edges[k]
                    # buffer.append((key_dict[k], inv+k, steps+edges[k]))
                buffer.sort(key=lambda x: x[2])
                for b in buffer:
                    q.append(b)
    return min(
        [pos_cache[(x, inv)] for x, inv in pos_cache if len(inv) == len(key_dict)]
    )


def part2(in_data, test=False):
    map2d = Map2d.from_lines(in_data)
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
    map2d, players = translate_map(map2d, player)
    log.debug(map2d.debug_draw())
    log.debug([map2d.translate_index(p) for p in players])
    for k in key_dict:
        map2d.set_index(key_dict[k], Map2d.empty_sym)
    steps = special_bfs_2(
        map2d, players, "".join([x for x in key_dict]), key_dict, door_dict
    )
    return steps
