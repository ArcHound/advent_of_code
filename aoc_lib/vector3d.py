import math
from collections import namedtuple


Point3d = namedtuple("Point3d", ["x", "y", "z"])


def v_add(a, b):
    return Point3d(a[0] + b[0], a[1] + b[1], a[2] + b[2])


def v_diff(a, b):
    return Point3d(a[0] - b[0], a[1] - b[1], a[2] - b[2])


def v_abs_val(a):
    return abs(a[0]) + abs(a[1]) + abs(a[2])


def v_const_mult(a, c):
    return Point3d(a[0] * c, a[1] * c, a[2] * c)


def v_abs(a):
    return Point3d(abs(a[0]), abs(a[1]), abs(a[2]))


def v_one(a):
    return Point3d(
        math.copysign(1, a[0]), math.copysign(1, a[1]), math.copysign(1, a[2])
    )


def v_cp_sign(vec, sign):
    return Point3d(
        math.copysign(vec[0], sign[0]),
        math.copysign(vec[1], sign[1]),
        math.copysign(vec[2], sign[2]),
    )


def v_touches_squares(a):
    return [
        Point3d(a[0] + 1, a[1], a[2]),
        Point3d(a[0] - 1, a[1], a[2]),
        Point3d(a[0], a[1] + 1, a[2]),
        Point3d(a[0], a[1] - 1, a[2]),
        Point3d(a[0], a[1], a[2] + 1),
        Point3d(a[0], a[1], a[2] - 1),
    ]


def distance(a: Point3d, b: Point3d):
    return math.sqrt(pow(a[0] - b[0], 2) + pow(a[1] - b[1], 2) + pow(a[2] - b[2], 2))


# def v_nearbycube(a,b):
