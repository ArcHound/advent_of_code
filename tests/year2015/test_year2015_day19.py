# test 2015-19
# vim: nomodeline

import pytest

from aoc.year2015.day19 import part1, part2

simple_test = """H => HO
H => OH
O => HH

HOH
"""


def test_part1():
    cases = [
        {
            "label": "simple",
            "input": {
                "in_data": simple_test,
                "test": True,
            },
            "output": "4",
            "ex": None,
        },
    ]
    for case in cases:
        try:
            output = part1(**case["input"])
            assert str(output) == str(case["output"]), (
                "case '{}', output: exp {}, got {}".format(
                    case["label"], case["output"], output
                )
            )
        except Exception as e:
            assert type(e) == case["ex"], "case '{}', ex: exp {}, got {}".format(
                case["label"], case["ex"], type(e)
            )


def test_part2():
    cases = [
        {
            "label": "RnAr",
            "input": {
                "in_data": """Al => ThF

CRnMgArMg""",
                "test": True,
            },
            "output": "2",
            "ex": None,
        },
        {
            "label": "no_Rn",
            "input": {
                "in_data": """Al => ThF

CMgMg""",
                "test": True,
            },
            "output": "2",
            "ex": None,
        },
        {
            "label": "RnYAr",
            "input": {
                "in_data": """Al => ThF

CRnMgYMgArC""",
                "test": True,
            },
            "output": "2",
            "ex": None,
        },
        {
            "label": "RnYYAr",
            "input": {
                "in_data": """Al => ThF

CRnMgYFYMgArC""",
                "test": True,
            },
            "output": "2",
            "ex": None,
        },
        {
            "label": "RnYRnArAr",
            "input": {
                "in_data": """Al => ThF

CRnMgYTiRnMgArArC""",
                "test": True,
            },
            "output": "3",
            "ex": None,
        },
        {
            "label": "RnRnArYRnArAr",
            "input": {
                "in_data": """Al => ThF

CRnMgRnTiArYTiRnMgArArTi""",
                "test": True,
            },
            "output": "4",
            "ex": None,
        },
    ]
    for case in cases:
        try:
            output = part2(**case["input"])
            assert str(output) == str(case["output"]), (
                "case '{}', output: exp {}, got {}".format(
                    case["label"], case["output"], output
                )
            )
        except Exception as e:
            assert type(e) == case["ex"], "case '{}', ex: exp {}, got {}".format(
                case["label"], case["ex"], type(e)
            )
