import datetime
import json
from unittest.mock import patch, mock_open, MagicMock
from click import BadParameter
import pytest

from aoc_tools import toolbox


@patch(f"{toolbox.__name__}.datetime", wraps=datetime)
def test_validate_day(mock_datetime):
    mock_datetime.datetime.now.return_value = datetime.datetime(
        2019, 12, 5, 4, 59, 0, 0, datetime.UTC
    )
    cases = [
        {
            "label": "simple",
            "input": {
                "ctx": MagicMock(params={"year": 2019}),
                "param": "??",
                "value": 2,
            },
            "output": 2,
            "ex": None,
        },
        {
            "label": "minus",
            "input": {
                "ctx": MagicMock(params={"year": 2019}),
                "param": "??",
                "value": -1,
            },
            "output": None,
            "ex": BadParameter,
        },
        {
            "label": "plus",
            "input": {
                "ctx": MagicMock(params={"year": 2019}),
                "param": "??",
                "value": 26,
            },
            "output": None,
            "ex": BadParameter,
        },
        {
            "label": "almost",
            "input": {
                "ctx": MagicMock(params={"year": 2019}),
                "param": "??",
                "value": 5,
            },
            "output": None,
            "ex": BadParameter,
        },
    ]
    for case in cases:
        try:
            output = toolbox.validate_day(**case["input"])
            assert output == case["output"], "case '{}', output: exp {}, got {}".format(
                case["label"], case["output"], output
            )
        except Exception as e:
            assert type(e) == case["ex"], "case '{}', ex: exp {}, got {}".format(
                case["label"], case["ex"], type(e)
            )


def test_validate_day_simple():
    cases = [
        {
            "label": "simple",
            "input": {
                "ctx": MagicMock(params={"year": 2019}),
                "param": "??",
                "value": 2,
            },
            "output": 2,
            "ex": None,
        },
        {
            "label": "minus",
            "input": {
                "ctx": MagicMock(params={"year": 2019}),
                "param": "??",
                "value": -1,
            },
            "output": None,
            "ex": BadParameter,
        },
        {
            "label": "plus",
            "input": {
                "ctx": MagicMock(params={"year": 2019}),
                "param": "??",
                "value": 26,
            },
            "output": None,
            "ex": BadParameter,
        },
    ]
    for case in cases:
        try:
            output = toolbox.validate_day_simple(**case["input"])
            assert output == case["output"], "case '{}', output: exp {}, got {}".format(
                case["label"], case["output"], output
            )
        except Exception as e:
            assert type(e) == case["ex"], "case '{}', ex: exp {}, got {}".format(
                case["label"], case["ex"], type(e)
            )


@patch(f"{toolbox.__name__}.datetime", wraps=datetime)
def test_validate_year(mock_datetime):
    mock_datetime.datetime.now.return_value = datetime.datetime(
        2019, 12, 5, 4, 59, 0, 0, datetime.UTC
    )
    cases = [
        {
            "label": "simple",
            "input": {"ctx": MagicMock(), "param": "??", "value": 2018},
            "output": 2018,
            "ex": None,
        },
        {
            "label": "minus",
            "input": {"ctx": MagicMock(), "param": "??", "value": 2014},
            "output": None,
            "ex": BadParameter,
        },
        {
            "label": "plus",
            "input": {"ctx": MagicMock(), "param": "??", "value": 2600},
            "output": None,
            "ex": BadParameter,
        },
    ]
    for case in cases:
        try:
            output = toolbox.validate_year(**case["input"])
            assert output == case["output"], "case '{}', output: exp {}, got {}".format(
                case["label"], case["output"], output
            )
        except Exception as e:
            assert type(e) == case["ex"], "case '{}', ex: exp {}, got {}".format(
                case["label"], case["ex"], type(e)
            )
