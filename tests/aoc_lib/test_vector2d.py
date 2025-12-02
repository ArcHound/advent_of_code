import datetime
# vim: nomodeline
import json
from unittest.mock import patch, mock_open
import pytest

from aoc_lib.vector2d import *


def test_v_add():
    cases = [
        {
            "label": "simple",
            "input": {"a": (0, 1), "b": (4, -2)},
            "output": (4, -1),
            "ex": None,
        },
    ]
    for case in cases:
        try:
            output = v_add(**case["input"])
            assert output == case["output"], "case '{}', output: exp {}, got {}".format(
                case["label"], case["output"], output
            )
        except Exception as e:
            assert type(e) == case["ex"], "case '{}', ex: exp {}, got {}".format(
                case["label"], case["ex"], type(e)
            )


def test_v_diff():
    cases = [
        {
            "label": "simple",
            "input": {"a": (0, 1), "b": (4, -2)},
            "output": (-4, 3),
            "ex": None,
        },
    ]
    for case in cases:
        try:
            output = v_diff(**case["input"])
            assert output == case["output"], "case '{}', output: exp {}, got {}".format(
                case["label"], case["output"], output
            )
        except Exception as e:
            assert type(e) == case["ex"], "case '{}', ex: exp {}, got {}".format(
                case["label"], case["ex"], type(e)
            )


def test_v_abs_val():
    cases = [
        {
            "label": "simple",
            "input": {"a": (0, 1)},
            "output": 1,
            "ex": None,
        },
        {
            "label": "neg",
            "input": {"a": (0, -1)},
            "output": 1,
            "ex": None,
        },
        {
            "label": "combo",
            "input": {"a": (4, -2)},
            "output": 6,
            "ex": None,
        },
    ]
    for case in cases:
        try:
            output = v_abs_val(**case["input"])
            assert output == case["output"], "case '{}', output: exp {}, got {}".format(
                case["label"], case["output"], output
            )
        except Exception as e:
            assert type(e) == case["ex"], "case '{}', ex: exp {}, got {}".format(
                case["label"], case["ex"], type(e)
            )


def test_v_const_mult():
    cases = [
        {
            "label": "simple",
            "input": {"a": (0, 1), "c": 3},
            "output": (0, 3),
            "ex": None,
        },
        {
            "label": "neg",
            "input": {"a": (0, 4), "c": -1},
            "output": (0, -4),
            "ex": None,
        },
        {
            "label": "combo",
            "input": {"a": (4, -2), "c": -2},
            "output": (-8, 4),
            "ex": None,
        },
    ]
    for case in cases:
        try:
            output = v_const_mult(**case["input"])
            assert output == case["output"], "case '{}', output: exp {}, got {}".format(
                case["label"], case["output"], output
            )
        except Exception as e:
            assert type(e) == case["ex"], "case '{}', ex: exp {}, got {}".format(
                case["label"], case["ex"], type(e)
            )


def test_v_abs():
    cases = [
        {
            "label": "simple",
            "input": {"a": (0, 1)},
            "output": (0, 1),
            "ex": None,
        },
        {
            "label": "neg",
            "input": {"a": (0, -1)},
            "output": (0, 1),
            "ex": None,
        },
    ]
    for case in cases:
        try:
            output = v_abs(**case["input"])
            assert output == case["output"], "case '{}', output: exp {}, got {}".format(
                case["label"], case["output"], output
            )
        except Exception as e:
            assert type(e) == case["ex"], "case '{}', ex: exp {}, got {}".format(
                case["label"], case["ex"], type(e)
            )


def test_v_one():
    cases = [
        {
            "label": "simple",
            "input": {"a": (0, 4)},
            "output": (1.0, 1.0),
            "ex": None,
        },
        {
            "label": "neg",
            "input": {"a": (-2, -4)},
            "output": (-1.0, -1.0),
            "ex": None,
        },
        {
            "label": "combo",
            "input": {"a": (-2, 4)},
            "output": (-1.0, 1.0),
            "ex": None,
        },
    ]
    for case in cases:
        try:
            output = v_one(**case["input"])
            assert output == case["output"], "case '{}', output: exp {}, got {}".format(
                case["label"], case["output"], output
            )
        except Exception as e:
            assert type(e) == case["ex"], "case '{}', ex: exp {}, got {}".format(
                case["label"], case["ex"], type(e)
            )


def test_v_cp_sign():
    cases = [
        {
            "label": "simple",
            "input": {"vec": (0, 4), "sign": (1, 1)},
            "output": (0, 4),
            "ex": None,
        },
        {
            "label": "neg",
            "input": {"vec": (-2, -4), "sign": (1, -1)},
            "output": (2, -4),
            "ex": None,
        },
    ]
    for case in cases:
        try:
            output = v_cp_sign(**case["input"])
            assert output == case["output"], "case '{}', output: exp {}, got {}".format(
                case["label"], case["output"], output
            )
        except Exception as e:
            assert type(e) == case["ex"], "case '{}', ex: exp {}, got {}".format(
                case["label"], case["ex"], type(e)
            )


def test_v_nearbysquare():
    cases = [
        {
            "label": "simple",
            "input": {"a": (0, 0), "b": (1, 0)},
            "output": True,
            "ex": None,
        },
        {
            "label": "neg",
            "input": {"a": (0, 0), "b": (-1, 0)},
            "output": True,
            "ex": None,
        },
        {
            "label": "diag",
            "input": {"a": (0, 0), "b": (-1, 1)},
            "output": True,
            "ex": None,
        },
        {
            "label": "far",
            "input": {"a": (0, 0), "b": (2, 1)},
            "output": False,
            "ex": None,
        },
    ]
    for case in cases:
        try:
            output = v_nearbysquare(**case["input"])
            assert output == case["output"], "case '{}', output: exp {}, got {}".format(
                case["label"], case["output"], output
            )
        except Exception as e:
            assert type(e) == case["ex"], "case '{}', ex: exp {}, got {}".format(
                case["label"], case["ex"], type(e)
            )


def test_v_nearbysquare():
    cases = [
        {
            "label": "simple",
            "input": {"a": (0, 0), "b": (1, 0)},
            "output": True,
            "ex": None,
        },
        {
            "label": "neg",
            "input": {"a": (0, 0), "b": (-1, 0)},
            "output": True,
            "ex": None,
        },
        {
            "label": "diag",
            "input": {"a": (0, 0), "b": (-1, 1)},
            "output": True,
            "ex": None,
        },
        {
            "label": "far",
            "input": {"a": (0, 0), "b": (2, 1)},
            "output": False,
            "ex": None,
        },
    ]
    for case in cases:
        try:
            output = v_nearbysquare(**case["input"])
            assert output == case["output"], "case '{}', output: exp {}, got {}".format(
                case["label"], case["output"], output
            )
        except Exception as e:
            assert type(e) == case["ex"], "case '{}', ex: exp {}, got {}".format(
                case["label"], case["ex"], type(e)
            )
