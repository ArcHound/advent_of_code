import datetime

# vim: nomodeline
import json
from unittest.mock import patch, mock_open
import pytest

from aoc_lib.num_theory import *


def test_is_prime_simple():
    cases = [
        {
            "label": "two",
            "input": {"n": 2},
            "output": True,
            "ex": None,
        },
        {
            "label": "three",
            "input": {"n": 3},
            "output": True,
            "ex": None,
        },
        {
            "label": "ten",
            "input": {"n": 10},
            "output": False,
            "ex": None,
        },
        {
            "label": "hundred",
            "input": {"n": 100},
            "output": False,
            "ex": None,
        },
        {
            "label": "26711",
            "input": {"n": 26711},
            "output": True,
            "ex": None,
        },
    ]
    for case in cases:
        try:
            output = is_prime_simple(**case["input"])
            assert output == case["output"], "case '{}', output: exp {}, got {}".format(
                case["label"], case["output"], output
            )
        except Exception as e:
            assert type(e) == case["ex"], "case '{}', ex: exp {}, got {}".format(
                case["label"], case["ex"], type(e)
            )


def test_primes_under_n():
    cases = [
        {
            "label": "two",
            "input": {"n": 2},
            "output": [2],
            "ex": None,
        },
        {
            "label": "three",
            "input": {"n": 3},
            "output": [2, 3],
            "ex": None,
        },
        {
            "label": "ten",
            "input": {"n": 10},
            "output": [2, 3, 5, 7],
            "ex": None,
        },
        {
            "label": "hundred",
            "input": {"n": 100},
            "output": [
                2,
                3,
                5,
                7,
                11,
                13,
                17,
                19,
                23,
                29,
                31,
                37,
                41,
                43,
                47,
                53,
                59,
                61,
                67,
                71,
                73,
                79,
                83,
                89,
                97,
            ],
            "ex": None,
        },
    ]
    for case in cases:
        try:
            output = primes_under_n(**case["input"])
            assert output == case["output"], "case '{}', output: exp {}, got {}".format(
                case["label"], case["output"], output
            )
        except Exception as e:
            assert type(e) == case["ex"], "case '{}', ex: exp {}, got {}".format(
                case["label"], case["ex"], type(e)
            )


def test_factorize():
    cases = [
        {
            "label": "two",
            "input": {"n": 2},
            "output": {2: 1},
            "ex": None,
        },
        {
            "label": "three",
            "input": {"n": 3},
            "output": {3: 1},
            "ex": None,
        },
        {
            "label": "ten",
            "input": {"n": 10},
            "output": {2: 1, 5: 1},
            "ex": None,
        },
        {
            "label": "sixteen",
            "input": {"n": 16},
            "output": {2: 4},
            "ex": None,
        },
        {
            "label": "hundred",
            "input": {"n": 100},
            "output": {2: 2, 5: 2},
            "ex": None,
        },
        {
            "label": "1013",
            "input": {"n": 1013},
            "output": {1013: 1},
            "ex": None,
        },
        {
            "label": "381024",
            "input": {"n": 381024},
            "output": {2: 5, 3: 5, 7: 2},
            "ex": None,
        },
    ]
    for case in cases:
        try:
            output = factorize(**case["input"])
            assert output == case["output"], "case '{}', output: exp {}, got {}".format(
                case["label"], case["output"], output
            )
        except Exception as e:
            assert type(e) == case["ex"], "case '{}', ex: exp {}, got {}".format(
                case["label"], case["ex"], type(e)
            )


def test_sum_of_divisors():
    cases = [
        {
            "label": "two",
            "input": {"n": 2},
            "output": 3,
            "ex": None,
        },
        {
            "label": "three",
            "input": {"n": 3},
            "output": 4,
            "ex": None,
        },
        {
            "label": "ten",
            "input": {"n": 10},
            "output": 18,
            "ex": None,
        },
        {
            "label": "sixteen",
            "input": {"n": 16},
            "output": 31,
            "ex": None,
        },
        {
            "label": "hundred",
            "input": {"n": 100},
            "output": 217,
            "ex": None,
        },
        {
            "label": "1013",
            "input": {"n": 1013},
            "output": 1014,
            "ex": None,
        },
        {
            "label": "381024",
            "input": {"n": 381024},
            "output": 1307124,
            "ex": None,
        },
    ]
    for case in cases:
        try:
            output = sum_of_divisors(**case["input"])
            assert output == case["output"], "case '{}', output: exp {}, got {}".format(
                case["label"], case["output"], output
            )
        except Exception as e:
            assert type(e) == case["ex"], "case '{}', ex: exp {}, got {}".format(
                case["label"], case["ex"], type(e)
            )


def test_egcd():
    cases = [
        {
            "label": "two, three",
            "input": {"a": 2, "b": 3},
            "output": (1, (-1, 1)),
            "ex": None,
        },
        {
            "label": "two, four",
            "input": {"a": 2, "b": 4},
            "output": (2, (1, 0)),
            "ex": None,
        },
        {
            "label": "seven, thirteen",
            "input": {"a": 7, "b": 13},
            "output": (1, (2, -1)),
            "ex": None,
        },
        {
            "label": "two primes",
            "input": {"a": 26711, "b": 25523},
            "output": (1, (10076, -10545)),
            "ex": None,
        },
        {
            "label": "powers of two",
            "input": {"a": pow(2, 15), "b": pow(2, 20)},
            "output": (pow(2, 15), (1, 0)),
            "ex": None,
        },
        {
            "label": "non-coprime",
            "input": {"a": 2345 * 15, "b": 2345 * 32},
            "output": (2345, (15, -7)),
            "ex": None,
        },
    ]
    for case in cases:
        try:
            output = egcd(**case["input"])
            assert output == case["output"], "case '{}', output: exp {}, got {}".format(
                case["label"], case["output"], output
            )
        except Exception as e:
            assert type(e) == case["ex"], "case '{}', ex: exp {}, got {}".format(
                case["label"], case["ex"], type(e)
            )


def test_mod_inv():
    cases = [
        {
            "label": "two, three",
            "input": {"a": 2, "n": 3},
            "output": 2,
            "ex": None,
        },
        {
            "label": "two, four",
            "input": {"a": 2, "n": 4},
            "output": None,
            "ex": ValueError,
        },
        {
            "label": "seven, thirteen",
            "input": {"a": 7, "n": 13},
            "output": 2,
            "ex": None,
        },
        {
            "label": "two primes",
            "input": {"a": 26711, "n": 25523},
            "output": 10076,
            "ex": None,
        },
    ]
    for case in cases:
        try:
            output = mod_inv(**case["input"])
            assert output == case["output"], "case '{}', output: exp {}, got {}".format(
                case["label"], case["output"], output
            )
        except Exception as e:
            assert type(e) == case["ex"], "case '{}', ex: exp {}, got {}".format(
                case["label"], case["ex"], type(e)
            )


def test_tuple_crt():
    cases = [
        {
            "label": "1 (mod 2), 1 (mod 3)",
            "input": {"c1": (1, 2), "c2": (1, 3)},
            "output": 1,
            "ex": None,
        },
        {
            "label": "5 (mod 7), 1 (mod 3)",
            "input": {"c1": (5, 7), "c2": (1, 3)},
            "output": 19,
            "ex": None,
        },
    ]
    for case in cases:
        try:
            output = tuple_crt(**case["input"])
            assert output == case["output"], "case '{}', output: exp {}, got {}".format(
                case["label"], case["output"], output
            )
        except Exception as e:
            assert type(e) == case["ex"], "case '{}', ex: exp {}, got {}".format(
                case["label"], case["ex"], type(e)
            )


def test_iterative_crt():
    cases = [
        {
            "label": "1 (mod 2), 1 (mod 3)",
            "input": {"l": [(1, 2), (1, 3)]},
            "output": 1,
            "ex": None,
        },
        {
            "label": "5 (mod 7), 1 (mod 3)",
            "input": {"l": [(5, 7), (1, 3)]},
            "output": 19,
            "ex": None,
        },
        {
            "label": "famous: 2 (mod 3), 3 (mod 5), 2 (mod 7)",
            "input": {"l": [(2, 3), (3, 5), (2, 7)]},
            "output": 23,
            "ex": None,
        },
    ]
    for case in cases:
        try:
            output = iterative_crt(**case["input"])
            assert output == case["output"], "case '{}', output: exp {}, got {}".format(
                case["label"], case["output"], output
            )
        except Exception as e:
            assert type(e) == case["ex"], "case '{}', ex: exp {}, got {}".format(
                case["label"], case["ex"], type(e)
            )
