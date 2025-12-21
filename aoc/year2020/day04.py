# 2020-04

import logging

log = logging.getLogger("aoc_logger")


def parse_data(in_data):
    data = list()
    buf = ""
    for line in in_data.splitlines():
        if line.strip() == "":
            passport = {
                x.split(":")[0]: x.split(":")[1] for x in buf.split(" ") if ":" in x
            }
            data.append(passport)
            buf = ""
        else:
            buf += " " + line.strip()
    passport = {x.split(":")[0]: x.split(":")[1] for x in buf.split(" ") if ":" in x}
    data.append(passport)
    return data


def part1(in_data, test=False):
    data = parse_data(in_data)
    req_fields = ["byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid"]
    count = 0
    for passport in data:
        if all([x in passport for x in req_fields]):
            count += 1
    return count


def part2(in_data, test=False):
    data = parse_data(in_data)
    count = 0
    for passport in data:
        log.debug(passport)
        try:
            if (
                "byr" not in passport
                or 1920 > int(passport["byr"])
                or 2002 < int(passport["byr"])
            ):
                log.debug("byr")
                continue
            if (
                "iyr" not in passport
                or 2010 > int(passport["iyr"])
                or 2020 < int(passport["iyr"])
            ):
                log.debug("iyr")
                continue
            if (
                "eyr" not in passport
                or 2020 > int(passport["eyr"])
                or 2030 < int(passport["eyr"])
            ):
                log.debug("eyr")
                continue
            if (
                "hgt" not in passport
                or passport["hgt"][-2:] not in ["cm", "in"]
                or (passport["hgt"][-2:] == "cm" and int(passport["hgt"][:-2]) < 150)
                or (passport["hgt"][-2:] == "cm" and int(passport["hgt"][:-2]) > 193)
                or (passport["hgt"][-2:] == "in" and int(passport["hgt"][:-2]) < 59)
                or (passport["hgt"][-2:] == "in" and int(passport["hgt"][:-2]) > 76)
            ):
                log.debug("hgt")
                continue
            if (
                "hcl" not in passport
                or passport["hcl"][0] != "#"
                or any(
                    [passport["hcl"][i] not in "0123456789abcdef" for i in range(1, 7)]
                )
            ):
                log.debug("hcl")
                continue
            if "ecl" not in passport or passport["ecl"] not in [
                "amb",
                "blu",
                "brn",
                "gry",
                "grn",
                "hzl",
                "oth",
            ]:
                log.debug("ecl")
                continue
            if (
                "pid" not in passport
                or any([passport["pid"][i] not in "0123456789" for i in range(9)])
                or len(passport["pid"]) != 9
            ):
                log.debug("pid")
                continue
            count += 1
        except Exception as e:
            log.debug(f"Exception {str(e)}")
            continue
    return count
