# 2022-19

import logging
import re
import dataclasses
from functools import cache
from tqdm import tqdm

log = logging.getLogger("aoc_logger")


@dataclasses.dataclass(frozen=True)
class Robot:
    ore_cost: int = 0
    clay_cost: int = 0
    obs_cost: int = 0


@dataclasses.dataclass(frozen=True)
class Blueprint:
    bid: int
    ore_robot: Robot
    clay_robot: Robot
    obs_robot: Robot
    geode_robot: Robot


@dataclasses.dataclass(frozen=True)
class Inventory:
    ore: int = 0
    clay: int = 0
    obs: int = 0
    geode: int = 0


@dataclasses.dataclass(frozen=True)
class State:
    minerals: Inventory
    robots: Inventory
    bp: Blueprint


@cache
def possible_spends(state):
    result = list()
    max_ore_robots = state.minerals.ore // state.bp.ore_robot.ore_cost
    max_clay_robots = state.minerals.ore // state.bp.clay_robot.ore_cost
    max_obs_robots = min(
        (
            state.minerals.ore // state.bp.obs_robot.ore_cost,
            state.minerals.clay // state.bp.obs_robot.clay_cost,
        )
    )
    max_geode_robots = min(
        (
            state.minerals.ore // state.bp.geode_robot.ore_cost,
            state.minerals.obs // state.bp.geode_robot.obs_cost,
        )
    )
    for geode_robots in range(max_geode_robots + 1):
        for obs_robots in range(max_obs_robots + 1):
            for clay_robots in range(max_clay_robots + 1):
                for ore_robots in range(max_ore_robots + 1):
                    total_ore = (
                        ore_robots * state.bp.ore_robot.ore_cost
                        + clay_robots * state.bp.clay_robot.ore_cost
                        + obs_robots * state.bp.obs_robot.ore_cost
                        + geode_robots * state.bp.geode_robot.ore_cost
                    )
                    total_clay = obs_robots * state.bp.obs_robot.clay_cost
                    total_obs = geode_robots * state.bp.geode_robot.obs_cost
                    if (
                        state.minerals.ore >= total_ore
                        and state.minerals.clay >= total_clay
                        and state.minerals.obs >= total_obs
                    ):
                        new_i = Inventory(
                            ore=total_ore - state.minerals.ore,
                            clay=total_clay - state.minerals.clay,
                            obs=total_obs - state.minerals.obs,
                            geode=state.minerals.geode,
                        )
                        new_bots = Inventory(
                            ore=ore_robots + state.robots.ore,
                            clay=clay_robots + state.robots.clay,
                            obs=obs_robots + state.robots.obs,
                            geode=geode_robots + state.robots.geode,
                        )
                        result.append((new_i, new_bots))
    return result


@cache
def single_spends(minerals, bp):
    result = list()
    max_ore_robots = minerals.ore // bp.ore_robot.ore_cost
    max_clay_robots = minerals.ore // bp.clay_robot.ore_cost
    max_obs_robots = min(
        (
            minerals.ore // bp.obs_robot.ore_cost,
            minerals.clay // bp.obs_robot.clay_cost,
        )
    )
    max_geode_robots = min(
        (
            minerals.ore // bp.geode_robot.ore_cost,
            minerals.obs // bp.geode_robot.obs_cost,
        )
    )
    if (
        minerals.ore >= bp.geode_robot.ore_cost
        and minerals.obs >= bp.geode_robot.obs_cost
    ):
        new_i = dataclasses.replace(
            minerals,
            ore=minerals.ore - bp.geode_robot.ore_cost,
            obs=minerals.obs - bp.geode_robot.obs_cost,
        )
        new_b = Inventory(geode=1)
        result.append((new_i, new_b))
        return result  # if a geode robot can be build, just build it
    if (
        minerals.ore >= bp.obs_robot.ore_cost
        and minerals.clay >= bp.obs_robot.clay_cost
    ):
        new_i = dataclasses.replace(
            minerals,
            ore=minerals.ore - bp.obs_robot.ore_cost,
            clay=minerals.clay - bp.obs_robot.clay_cost,
        )
        new_b = Inventory(obs=1)
        result.append((new_i, new_b))
    if minerals.ore >= bp.clay_robot.ore_cost:
        new_i = dataclasses.replace(minerals, ore=minerals.ore - bp.clay_robot.ore_cost)
        new_b = Inventory(clay=1)
        result.append((new_i, new_b))
    if minerals.ore >= bp.ore_robot.ore_cost:
        new_i = dataclasses.replace(minerals, ore=minerals.ore - bp.ore_robot.ore_cost)
        new_b = Inventory(ore=1)
        result.append((new_i, new_b))
    result.append((dataclasses.replace(minerals), Inventory()))
    return result


@cache
def gain(state):
    return dataclass.replace(
        state.minerals,
        ore=state.minerals.ore + state.robots.ore,
        clay=state.minerals.clay + state.robots.clay,
        obs=state.minerals.obs + state.robots.obs,
        geode=state.minerals.geode + state.robots.geode,
    )


def parse_data(in_data):
    data = list()
    for line in in_data.splitlines():
        match = re.search(
            "Blueprint (?P<bid>[0-9]+): Each ore robot costs (?P<ore_ore_cost>[0-9]+) ore. Each clay robot costs (?P<clay_ore_cost>[0-9]+) ore. Each obsidian robot costs (?P<obs_ore_cost>[0-9]+) ore and (?P<obs_clay_cost>[0-9]+) clay. Each geode robot costs (?P<geode_ore_cost>[0-9]+) ore and (?P<geode_obs_cost>[0-9]+) obsidian.",
            line.strip(),
        )
        data.append(
            Blueprint(
                int(match["bid"]),
                Robot(ore_cost=int(match["ore_ore_cost"])),
                Robot(ore_cost=int(match["clay_ore_cost"])),
                Robot(
                    ore_cost=int(match["obs_ore_cost"]),
                    clay_cost=int(match["obs_clay_cost"]),
                ),
                Robot(
                    ore_cost=int(match["geode_ore_cost"]),
                    obs_cost=int(match["geode_obs_cost"]),
                ),
            )
        )
    return data


def eval_bp(bp, max_time):
    robots = Inventory(ore=1)
    minerals = Inventory()
    state = State(minerals=minerals, robots=robots, bp=bp)
    queue = list()
    queue.append((state, 0))
    max_geodes = 0
    max_time_saw = 0
    max_ore_cost = max(
        [
            bp.ore_robot.ore_cost,
            bp.clay_robot.ore_cost,
            bp.obs_robot.ore_cost,
            bp.geode_robot.ore_cost,
        ]
    )
    while len(queue) > 0:
        state, time = queue.pop(0)
        if time > max_time_saw:
            log.debug(f"Time: {time}")
            max_time_saw = time
        if max_geodes < state.minerals.geode:
            max_geodes = state.minerals.geode
        #  log.debug(max_geodes)
        #  log.debug(state)
        if max_geodes > state.minerals.geode + sum(
            [state.robots.geode + i for i in range(0, max_time - time)]
        ):
            continue
        if time >= max_time:
            continue
        spends = single_spends(state.minerals, state.bp)
        # if len(queue)<7000-1 and time<6:
        #     log.debug(len(spends))
        for minerals, robot_increment in spends:
            new_i = Inventory(
                ore=minerals.ore + state.robots.ore,
                clay=minerals.clay + state.robots.clay,
                obs=minerals.obs + state.robots.obs,
                geode=minerals.geode + state.robots.geode,
            )
            new_b = Inventory(
                ore=state.robots.ore + robot_increment.ore,
                clay=state.robots.clay + robot_increment.clay,
                obs=state.robots.obs + robot_increment.obs,
                geode=state.robots.geode + robot_increment.geode,
            )
            if new_b.ore > max_ore_cost:
                continue  # don't build more ore robots than we can utilize
            elif new_b.clay > bp.obs_robot.clay_cost:
                continue  # same for clay
            elif new_b.obs > bp.geode_robot.obs_cost:
                continue  # same for obsidian
            new_s = State(minerals=new_i, robots=new_b, bp=bp)
            if time + 1 <= max_time:
                better = True
                for qs, qt in queue:
                    if compare_states(new_s, qs, time + 1, qt):
                        better = False
                        break
                if better:
                    queue.append((new_s, time + 1))
        # prune
        q = sorted(queue, key=lambda x: x[0].minerals.geode * x[1], reverse=True)
        queue = q[:7000]
        # for z in queue:
        #     log.debug(z[0].minerals)
        #     log.debug(z[0].robots)
        #     log.debug('--------')
        # log.debug('--------')
        # if len(queue)<7000:
        #     log.debug(len(queue))
    log.debug(f"{bp.bid}: {max_geodes}")
    return max_geodes


def compare_inventories(i1, i2):
    return (
        i2.ore >= i1.ore
        and i2.clay >= i1.clay
        and i2.obs >= i1.obs
        and i2.geode >= i1.geode
    )


def compare_states(s1, s2, t1, t2):
    return (
        compare_inventories(s1.minerals, s2.minerals)
        and compare_inventories(s1.robots, s2.robots)
        and t2 <= t1
    )


def part1(in_data, test=False):
    data = parse_data(in_data)
    total = 0
    for bp in tqdm(data):
        best_effort = eval_bp(bp, 24)
        total += bp.bid * best_effort
    return total


def part2(in_data, test=False):
    data = parse_data(in_data)
    data = parse_data(in_data)
    total = 1
    for bp in tqdm(data[:3]):
        best_effort = eval_bp(bp, 32)
        total *= best_effort
    return total
