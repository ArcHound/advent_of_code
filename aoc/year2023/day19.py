# 2023-19
import logging
from tqdm import tqdm
from aoc_lib.interval import Interval
import pprint

log = logging.getLogger("aoc_logger")


def parse_data(in_data):
    rules_read = True  # simple state machine with two states
    rules_map = dict()
    objects = list()
    for line in in_data.splitlines():
        if line == "":  # flip the state on empty line
            rules_read = False
            continue
        if rules_read:
            label, contents = line.split("{")  # ugly
            rules = list()
            for protorule in contents[:-1].split(","):  # UGLY
                if not ":" in protorule:  # either we have a condition
                    rules.append(
                        {"key": None, "sym": None, "val": None, "next_val": protorule}
                    )
                else:  # or we just paste the result
                    condition, result = protorule.split(":")
                    rules.append(
                        {
                            "key": condition[0],
                            "sym": condition[1],
                            "val": int(condition[2:]),
                            "next_val": result,
                        }
                    )
            rules_map[label] = rules
        else:
            objects.append(
                {obj[0]: int(obj[2:]) for obj in line[1:-1].split(",")}
            )  # not general, but works
    return rules_map, objects


def eval_rule(obj, key, sym, val, next_val):
    # let's eval the rule
    if sym == ">":  # we have two symbols
        if obj[key] > val:
            return next_val
    elif sym == "<":
        if obj[key] < val:
            return next_val
    elif sym is None:  # if it's an empty rule, then just return the result
        return next_val
    return None


def eval_ruleset(obj, ruleset):
    for (
        rule
    ) in ruleset:  # check all of the rules in order, when we have a result, return
        result = eval_rule(obj, **rule)
        if result:
            return result


def eval_obj(obj, rules_map):
    result = "in"
    while (
        result not in "RA"
    ):  # check all of the rules until we have either accepted or rejected
        result = eval_ruleset(obj, rules_map[result])
    return result


def part1(in_data):
    rules_map, objects = parse_data(in_data)
    count = 0
    log.debug(rules_map)
    log.debug(objects)
    for obj in objects:  # eval all objects
        r = eval_obj(obj, rules_map)
        if r == "A":
            count += sum([obj[k] for k in obj])  # count
    return count  # yay


def interval_rule(interval, key, sym, val, next_val):
    if sym == ">":  # we have two symbols
        if (
            val >= interval.start and val < interval.end
        ):  # if the val is in the interval, tear it apart
            return [
                (Interval(interval.start, val + 1), None),
                (Interval(val + 1, interval.end), next_val),
            ]
        elif val >= interval.end:  # else it missed, whole interval is ok or not
            return [(Interval(interval.start, interval.end), None)]
        elif val < interval.start:
            return [(Interval(interval.start, interval.end), next_val)]
    elif sym == "<":
        if val >= interval.start and val < interval.end:
            return [
                (Interval(interval.start, val), next_val),
                (Interval(val, interval.end), None),
            ]
        elif val >= interval.end:
            return [(Interval(interval.start, interval.end), next_val)]
        elif val < interval.start:
            return [(Interval(interval.start, interval.end), None)]


def process_interval_obj(interval_obj, rules_map):
    # checks one interval object
    # could use a refactor
    log.debug(interval_obj)
    to_process = [interval_obj]
    result = list()
    done = False
    ruleset = interval_obj["label"]  # check the rule to evaluate
    to_process = [interval_obj]
    for rule in rules_map[ruleset]:
        new_process = list()
        log.debug(rule)
        if rule["key"] is None:  # last rule is globally applicable and final
            log.debug("Final - {}".format(rule["next_val"]))
            for p_int in to_process:
                log.debug(p_int)
                new_obj = dict()
                for k in "xmas":
                    new_obj[k] = [i for i in p_int[k]]
                new_obj["label"] = rule["next_val"]
                new_obj["path"] = p_int["path"] + [ruleset]
                result.append(new_obj)
            break  # we're done
        else:
            key = rule["key"]
            log.debug(f"normal rule {key}")
            log.debug(to_process)
            for p_int in to_process:
                p = p_int[key]
                log.debug(p)
                log.debug("HELP1")
                for single_interval in p:  # take a look at the key and return all possible intervals for futher processing
                    log.debug("HELP2")
                    log.debug(single_interval)
                    ints = interval_rule(single_interval, **rule)
                    log.debug(ints)
                    for i, label in ints:
                        log.debug("new obj")
                        new_obj = dict()
                        for x in "xmas":
                            if x != key:
                                new_obj[x] = p_int[x]
                            else:
                                new_obj[x] = [i]
                        if label:
                            new_obj["label"] = label
                            new_obj["path"] = p_int["path"] + [ruleset]
                            result.append(new_obj)
                        else:
                            new_obj["path"] = p_int["path"]
                            new_process.append(new_obj)
                        log.debug(f"NEW process {new_process}")
                        log.debug(f"Result {result}")
        to_process = new_process
        log.debug(f"To process: {to_process}")
        log.debug(f"Result: {result}")

    known = list()
    unknown = list()
    for i in result:
        if i["label"] in "RA":  # if we reach A or R, we're done with the rule
            known.append(i)
        else:
            unknown.append(i)
    return known, unknown


def process_intervals(intervals, rules_map):
    new_interval = list()
    to_process = intervals
    result = list()
    i = 0
    while len(to_process) > 0:
        ints = to_process.pop(
            0
        )  # eval interval objects until we know the results (A or R)
        known, unknown = process_interval_obj(ints, rules_map)
        result += known
        to_process += unknown
        log.debug("=========================")
        log.debug(result)
        log.debug(to_process)
        log.debug("=========================")
        i += 1
        # if i == 2:
        #     break
    return result


def part2(in_data):
    # and of course, the above approach will fail horribly in part 2
    # let's try it anyway
    rules_map, objects = parse_data(in_data)
    # for giggles - this would take approximately 60 years to finish
    # count = 0
    # obj = {"x":0, "m":0, "a":0, "s":0}
    # for i in range(4000):
    #     for j in range(4000):
    #         for k in tqdm(range(4000)):
    #             for l in range(4000):
    #                 obj["x"] = i
    #                 obj["m"] = j
    #                 obj["a"] = k
    #                 obj["s"] = l
    #                 if eval_obj(obj, rules_map) == "A":
    #                     count += 1
    intervals = [
        {
            "x": [Interval(1, 4001)],
            "m": [Interval(1, 4001)],
            "a": [Interval(1, 4001)],
            "s": [Interval(1, 4001)],
            "label": "in",
            "path": [],
        }
    ]
    new_ints = process_intervals(intervals, rules_map)
    count = 0
    new_ints = [x for x in new_ints if x["label"] == "A"]  # only interested in accepted
    log.debug(pprint.pformat(new_ints))
    for x in new_ints:
        count += (
            (x["x"][0].end - x["x"][0].start)
            * (x["m"][0].end - x["m"][0].start)
            * (x["a"][0].end - x["a"][0].start)
            * (x["s"][0].end - x["s"][0].start)
        )

    return count
