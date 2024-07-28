# 2019-3
import logging
from aoc_lib.vector2d import *

log = logging.getLogger("aoc_logger")

def parse_data(in_data):
    data = list()
    for line in in_data.splitlines():
        data.append([(x[0], int(x[1:])) for x in line.split(',')])
    return data

directions = {
    "R": (1,0),
    "L": (-1,0),
    "U": (0,-1),
    "D": (0,1),
}

def verticality(a1, a2):
    if a1[0]==a2[0]:
        return True
    elif a1[1]==a2[1]:
        return False
    else:
        return None

def is_cross(a,b):
    a1, a2 = a
    b1, b2 = b
    va = verticality(a1,a2)
    vb = verticality(b1,b2)
    if va is None or vb is None:
        return None # won't deal with that
    elif va == vb:
        if va:
            if a1[0]==b1[0]:
                return (a1[0], max(min(a1[1],a2[1]),min(b1[1],b2[1])))
            else:
                return None
        else:
            if a1[1]==b1[1]:
                return (max(min(a1[0],a2[0]),min(b1[0],b2[0])), a1[1])
            else:
                return None
    else:
        if va:
            if min(b1[0], b2[0])<=a1[0] and a1[0]<=max(b1[0],b2[0]) and (min(a1[1],a2[1])<=b1[1] and b1[1]<=max(a1[1],a2[1])):
                return (a1[0], b1[1])
        else:
            if min(a1[0], a2[0])<=b1[0] and b1[0]<=max(a1[0],a2[0]) and (min(b1[1],b2[1])<=a1[1] and a1[1]<=max(b1[1],b2[1])):
                return (b1[0], a1[1])
    return None



def part1(in_data, test=False):
    data = parse_data(in_data)
    points = list()
    for line in data:
        line_points = []
        previous_point = (0,0)
        for direction, value in line:
            d = v_const_mult(directions[direction], value) 
            new_point = v_add(previous_point, d)
            previous_point = new_point
            line_points.append(new_point)
        points.append(line_points)
    log.debug(points)
    crosses = list()
    for i1 in range(len(points[0])-1):
        for i2 in range(len(points[1])-1):
            a1 = points[0][i1] 
            a2 = points[0][i1+1]
            b1 = points[1][i2]
            b2 = points[1][i2+1]
            cross = is_cross((a1,a2),(b1,b2))
            if cross is not None:
                crosses.append(cross)
    log.debug(crosses)
    return min([v_abs_val(c) for c in crosses])

def part2(in_data, test=False):
    data = parse_data(in_data)
    points = list()
    for line in data:
        line_points = []
        previous_struct = ((0,0),0)
        for direction, value in line:
            previous_point, previous_len = previous_struct
            d = v_const_mult(directions[direction], value) 
            new_struct = (v_add(previous_point, d), previous_len+value)
            previous_struct = new_struct
            line_points.append(new_struct)
        points.append(line_points)
    log.debug(points)
    crosses = list()
    for i1 in range(len(points[0])-1):
        for i2 in range(len(points[1])-1):
            a1 = points[0][i1][0]
            a2 = points[0][i1+1][0]
            a1_len = points[0][i1][1]
            a2_len = points[0][i1+1][1]
            b1 = points[1][i2][0]
            b2 = points[1][i2+1][0]
            b1_len = points[0][i2][1]
            b2_len = points[0][i2+1][1]
            cross = is_cross((a1,a2),(b1,b2))
            if cross is not None:
                ca_len = v_abs_val(v_diff(a1,cross))+a1_len
                cb_len = v_abs_val(v_diff(b1,cross))+b1_len
                crosses.append(ca_len+cb_len)
    log.debug(crosses)
    return min(crosses)
