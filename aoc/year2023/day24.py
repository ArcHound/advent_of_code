# 2023-24
import logging
from aoc_lib.vector3d import Point3d
import numpy as np
from z3 import Int, IntVector, Solver

log = logging.getLogger("aoc_logger")


def parse_data(in_data):
    points = list()
    for line in in_data.splitlines():
        point_s, velocity_s = line.split(" @ ")
        point = [int(x) for x in point_s.split(", ")]
        velocity = [int(x) for x in velocity_s.split(", ")]
        points.append(
            (
                Point3d(point[0], point[1], point[2]),
                Point3d(velocity[0], velocity[1], velocity[2]),
            )
        )
    return points


def vague_intersection(p_a, v_a, p_b, v_b, test_area):
    output = True
    try:
        # we need to solve a system of linear equations to discover whether the two lines intersect
        # the idea is to represent it in form line(t) = start + velocity*t
        A = np.array(
            [
                [v_a.x, -1 * v_b.x],
                [v_a.y, -1 * v_b.y],
            ]
        )
        b = np.array([p_b.x - p_a.x, p_b.y - p_a.y])
        t = np.linalg.solve(A, b)
        # for negative t we know the point was there in the past
        if t[0] < 0 or t[1] < 0:
            output = False
        else:
            # the intersection exists, let's take it
            intersection = Point3d(
                p_a.x + t[0] * v_a.x, p_a.y + t[0] * v_a.y, p_a.z + t[0] * v_a.z
            )
            log.debug(f"Intersection at {intersection}")
            # rectangle check
            output = (
                test_area[0][0] <= intersection.x
                and intersection.x <= test_area[0][1]
                and test_area[1][0] <= intersection.y
                and intersection.y <= test_area[1][1]
            )
    except np.linalg.LinAlgError as e: # if no solution, we don't have that collision
        output = False
        log.debug(e)
    return output


def part1(in_data, test=False):
    points = parse_data(in_data)
    test_area = None
    if test:
        test_area = ((7, 27), (7, 27))
    else:
        test_area = (
            (200000000000000, 400000000000000),
            (200000000000000, 400000000000000),
        )
    log.debug(test_area)
    count = 0
    for i in range(len(points)):
        for j in range(i):
            p_a, v_a = points[i]
            p_b, v_b = points[j]
            if vague_intersection(p_a, v_a, p_b, v_b, test_area):
                count += 1
            log.debug("----------------------")
    return count


def part2(in_data):
    points = parse_data(in_data)
    new_points = points[:6]  # this should be enough data for the line
    # z3 is awesome and I am using every excuse to try it
    # we are finding a line that has an intersection with each of the other lines
    # can be algebraically expressed by these conditions:
    s = Solver()
    x_t, y_t, z_t, a_t, b_t, c_t = IntVector("sol", 6)
    ts = IntVector("t", len(new_points))
    for i in range(len(new_points)):
        s.add(x_t + a_t * ts[i] == points[i][0].x + points[i][1].x * ts[i])
        s.add(y_t + b_t * ts[i] == points[i][0].y + points[i][1].y * ts[i])
        s.add(z_t + c_t * ts[i] == points[i][0].z + points[i][1].z * ts[i])
    s.check()
    m = s.model()
    return sum([m[v].as_long() for v in (x_t, y_t, z_t)])
