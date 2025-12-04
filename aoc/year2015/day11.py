# 2015-11

import logging

log = logging.getLogger("aoc_logger")


def password_to_nums(password):
    return [ord(x) - ord("a") for x in password]


def nums_to_password(nums):
    return "".join([chr(x + ord("a")) for x in nums])


def increment_password(password):
    nums = password_to_nums(password)
    num = 0
    for n in nums:
        num = 26 * (num) + n
    num += 1
    new_nums = list()
    for i in range(len(password)):
        new_nums.append(num % 26)
        num = num // 26
    new_nums.reverse()
    return nums_to_password(new_nums)


def check_password(password):
    if "i" in password or "o" in password or "l" in password:
        return False
    tuples = []
    for i in range(len(password) - 1):
        if password[i] == password[i + 1] and password[i] + password[i] not in tuples:
            tuples.append(password[i] + password[i])
    if len(tuples) < 2:
        return False
    for i in range(len(password) - 2):
        if (
            ord(password[i]) == ord(password[i + 1]) - 1
            and ord(password[i + 1]) == ord(password[i + 2]) - 1
        ):
            return True
    return False


def part1(in_data, test=False):
    password = in_data.strip()
    done = False
    while not done:
        # log.debug(password)
        password = increment_password(password)
        if check_password(password):
            done = True
    return password


def part2(in_data, test=False):
    password = in_data.strip()
    done = False
    while not done:
        # log.debug(password)
        password = increment_password(password)
        if check_password(password):
            done = True
    password = increment_password(password)
    done = False
    while not done:
        # log.debug(password)
        password = increment_password(password)
        if check_password(password):
            done = True
    return password
