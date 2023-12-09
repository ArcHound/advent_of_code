# 2023-9
import logging

log = logging.getLogger("aoc_logger")


def parse_data(in_data):
    return [[int(x) for x in line.split(" ")] for line in in_data.splitlines()]  # BANG!


# it's basically a derivative - list of differences between the points
def derivative(series):
    d = list()
    for i in range(len(series) - 1):
        d.append(series[i + 1] - series[i])
    return d


# simple enough, propagate up
def interpolate(derivatives):
    rd = derivatives
    rd.reverse()
    count = 0
    for d in rd:
        count += d[-1]
    return count


# same idea, start with zeroes and then reduce the first element
def interpolate_back(derivatives):
    rd = derivatives
    rd.reverse()
    count = 0
    for d in rd:
        count = d[0] - count
    return count


def part1(in_data):
    series = parse_data(in_data)
    c = 0
    for serie in series:
        s = serie
        ds = [serie]
        while any(s) != 0:
            s = derivative(s)
            ds.append(s)
        log.debug(ds)
        c += interpolate(ds)
        log.debug(c)
    return c


def part2(in_data):
    series = parse_data(in_data)
    c = 0
    for serie in series:
        s = serie
        ds = [serie]
        while any(s) != 0:
            s = derivative(s)
            ds.append(s)
        log.debug(ds)
        c += interpolate_back(ds)
        log.debug(c)
    return c


# I think this is the cleanest solution I have here
