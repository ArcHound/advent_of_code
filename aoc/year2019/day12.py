# 2019-12
import logging
from aoc_lib.vector3d import *
import dataclasses
import math


@dataclasses.dataclass
class Moon:
    position: tuple
    velocity: tuple


log = logging.getLogger("aoc_logger")


def gravity(moons):
    for i in range(len(moons)):
        for j in range(i):
            if i == j:
                continue
            if moons[i].position.x != moons[j].position.x:
                if moons[i].position.x > moons[j].position.x:
                    moons[i].velocity = Point3d(
                        moons[i].velocity.x - 1,
                        moons[i].velocity.y,
                        moons[i].velocity.z,
                    )
                    moons[j].velocity = Point3d(
                        moons[j].velocity.x + 1,
                        moons[j].velocity.y,
                        moons[j].velocity.z,
                    )
                else:
                    moons[i].velocity = Point3d(
                        moons[i].velocity.x + 1,
                        moons[i].velocity.y,
                        moons[i].velocity.z,
                    )
                    moons[j].velocity = Point3d(
                        moons[j].velocity.x - 1,
                        moons[j].velocity.y,
                        moons[j].velocity.z,
                    )
            if moons[i].position.y != moons[j].position.y:
                if moons[i].position.y > moons[j].position.y:
                    moons[i].velocity = Point3d(
                        moons[i].velocity.x,
                        moons[i].velocity.y - 1,
                        moons[i].velocity.z,
                    )
                    moons[j].velocity = Point3d(
                        moons[j].velocity.x,
                        moons[j].velocity.y + 1,
                        moons[j].velocity.z,
                    )
                else:
                    moons[i].velocity = Point3d(
                        moons[i].velocity.x,
                        moons[i].velocity.y + 1,
                        moons[i].velocity.z,
                    )
                    moons[j].velocity = Point3d(
                        moons[j].velocity.x,
                        moons[j].velocity.y - 1,
                        moons[j].velocity.z,
                    )
            if moons[i].position.z != moons[j].position.z:
                if moons[i].position.z > moons[j].position.z:
                    moons[i].velocity = Point3d(
                        moons[i].velocity.x,
                        moons[i].velocity.y,
                        moons[i].velocity.z - 1,
                    )
                    moons[j].velocity = Point3d(
                        moons[j].velocity.x,
                        moons[j].velocity.y,
                        moons[j].velocity.z + 1,
                    )
                else:
                    moons[i].velocity = Point3d(
                        moons[i].velocity.x,
                        moons[i].velocity.y,
                        moons[i].velocity.z + 1,
                    )
                    moons[j].velocity = Point3d(
                        moons[j].velocity.x,
                        moons[j].velocity.y,
                        moons[j].velocity.z - 1,
                    )


def velocity(moons):
    for moon in moons:
        moon.position = v_add(moon.position, moon.velocity)


def parse_data(in_data):
    data = list()
    for line in in_data.splitlines():
        x, y, z = line[1:-1].split(", ")
        data.append(
            Moon(
                Point3d(
                    **{
                        x[0]: int(x.split("=")[1]),
                        y[0]: int(y.split("=")[1]),
                        z[0]: int(z.split("=")[1]),
                    }
                ),
                Point3d(0, 0, 0),
            )
        )
    return data


def part1(in_data, test=False):
    moons = parse_data(in_data)
    if test:
        steps = 100
    else:
        steps = 1000

    for i in range(steps):
        gravity(moons)
        velocity(moons)
        log.debug(moons)
    return sum([v_abs_val(moon.position) * v_abs_val(moon.velocity) for moon in moons])


def part2(in_data, test=False):
    moons = parse_data(in_data)
    first_xs = [moon.position.x for moon in moons]
    first_ys = [moon.position.y for moon in moons]
    first_zs = [moon.position.z for moon in moons]
    cycle = Point3d(0, 0, 0)
    stop = [False, False, False]
    counter = 1
    while not all(stop):
        gravity(moons)
        velocity(moons)
        counter += 1
        xs = [moon.position.x for moon in moons]
        ys = [moon.position.y for moon in moons]
        zs = [moon.position.z for moon in moons]
        if xs == first_xs and not stop[0]:
            cycle = Point3d(counter, cycle.y, cycle.z)
            stop[0] = True
        if ys == first_ys and not stop[1]:
            cycle = Point3d(cycle.x, counter, cycle.z)
            stop[1] = True
        if zs == first_zs and not stop[2]:
            cycle = Point3d(cycle.x, cycle.y, counter)
            stop[2] = True
    return math.lcm(cycle.x, cycle.y, cycle.z)
