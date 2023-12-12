# 2023-12
import logging

log = logging.getLogger("aoc_logger")
import pprint

pp = pprint.PrettyPrinter(depth=4)


def parse_data(in_data):
    arrangements = list()
    for line in in_data.splitlines():
        nums = [int(x) for x in line.split(" ")[1].split(",")]
        args = line.split(" ")[0]
        arrangements.append((args, nums))
    return arrangements


# recursive approach
def recursive_solve(ar, nums, cache):
    # caching: if we calculated this value, then return what we've got
    if (ar, nums) in cache:
        return cache[(ar, nums)]
    # the end condition - no more numbers to put in
    if not nums:
        if "#" in ar:  # if there's something fixed it's impossible - 0 options
            return 0
        else:  # even if there are ?s they can be all . so there's 1 option
            return 1
    num = nums[0]  # get the first number
    i = 0  # array pointer
    while i <= len(ar):
        if i == len(ar):
            return 0
        if ar[i] == ".":  # ignore empty space
            pass
        elif ar[i] == "#":  # if we start with a rock, we need to substitute
            if i + num - 1 >= len(ar):  # check if we have enough space
                return 0
            for j in range(num - 1):
                if (
                    ar[i + 1 + j] == "."
                ):  # check if there's no forced space within our thing
                    return 0
            if i + num == len(ar) or (
                i + num + 1 == len(ar) and ar[i + num] != "#"
            ):  # check if there's remaining space for other stuff (or the end)
                if len(nums[1:]) == 0:
                    return 1
                else:
                    return 0
            if ar[i + num] == "#":  # it is too long
                return 0
            s = recursive_solve(
                ar[i + num + 1 :], nums[1:], cache
            )  # problem was reduced
            cache[(ar[i + num + 1 :], nums[1:])] = s
            return s
        elif ar[i] == "?":  # optional start
            if i + num - 1 >= len(ar):
                return 0
            s = 0
            cannot_be_one = False  # same checks as above if we assume we start here
            for j in range(num - 1):
                if ar[i + 1 + j] == ".":
                    cannot_be_one = True
            if not cannot_be_one:
                if i + num == len(ar) or (
                    i + num + 1 == len(ar) and ar[i + num] != "#"
                ):
                    if len(nums[1:]) == 0:
                        s = 1
                    else:
                        s = 0
                elif ar[i + num] == "#":
                    s = 0
                else:
                    s = recursive_solve(ar[i + num + 1 :], nums[1:], cache)
                    cache[(ar[i + num + 1 :], nums[1:])] = s
            # it can also be empty
            no_s = 0
            if i + num < len(ar):
                no_s = recursive_solve(ar[i + 1 :], nums, cache)
                cache[(ar[i + 1 :], nums)] = no_s
            return no_s + s  # sum the options and go up
        else:
            raise ValueError("wtf symbol")
        i += 1


def part1(in_data):
    arrangements = parse_data(in_data)
    valid_combinations = 0
    for ar, nums2 in arrangements:
        # need a tuple so I can use the numbers as index
        nums = tuple(nums2)
        cache = dict()
        r = recursive_solve(ar, nums, cache)
        valid_combinations += r
    return valid_combinations


def part2(in_data):
    arrangements = parse_data(in_data)
    valid_combinations = 0
    for ar2, nums2 in arrangements:
        # inflate
        nums = tuple(5 * nums2)
        ar = "?".join([ar2 for i in range(5)])
        # same as above
        cache = dict()
        r = recursive_solve(ar, nums, cache)
        valid_combinations += r
    return valid_combinations
