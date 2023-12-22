import math
import dataclasses


@dataclasses.dataclass
class Point3d:
    x: int
    y: int
    z: int

    def copy(self):
        return Point3d(self.x, self.y, self.z)


def v_add(a, b):
    return Point3d(a.x + b.x, a.y + b.y, a.z + b.z)


def v_diff(a, b):
    return Point3d(a.x - b.x, a.y - b.y, a.z - b.z)


def v_abs_val(a):
    return abs(a.x) + abs(a.y) + abs(a.z)


def v_const_mult(a, c):
    return Point3d(a.x * c, a.y * c, a.z * c)


def v_abs(a):
    return Point3d(abs(a.x), abs(a.y), abs(a.z))


def v_one(a):
    return (math.copysign(1, a[0]), math.copysign(1, a[1]))


def v_cp_sign(vec, sign):
    return (math.copysign(vec[0], sign[0]), math.copysign(vec[1], sign[1]))


def v_nearbysquare(a, b):
    return abs(a[0] - b[0]) <= 1 and abs(a[1] - b[1]) <= 1
