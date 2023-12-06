import math


def v_add(a, b):
    return (a[0] + b[0], a[1] + b[1])


def v_diff(a, b):
    return (a[0] - b[0], a[1] - b[1])


def v_abs_val(a):
    return abs(a[0]) + abs(a[1])


def v_abs(a):
    return (abs(a[0]), abs(a[1]))


def v_one(a):
    return (math.copysign(1, a[0]), math.copysign(1, a[1]))


def v_cp_sign(vec, sign):
    return (math.copysign(vec[0], sign[0]), math.copysign(vec[1], sign[1]))


def v_nearbysquare(a, b):
    return abs(a[0] - b[0]) <= 1 and abs(a[1] - b[1]) <= 1
