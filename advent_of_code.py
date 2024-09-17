#!/usr/bin/env python3

import os
import json
import csv
import logging
import sys
import time
import datetime
import math
from functools import update_wrapper
import cProfile
import pstats
import importlib
import pkgutil
import pathlib
import re

import click
from dotenv import load_dotenv
import requests
import requests_cache
from bs4 import BeautifulSoup

import aoc

requests_cache.install_cache(
    cache_name="advent_of_code_requests_cache", backend="sqlite", cache_control=True
)

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler()],
)
log = logging.getLogger("aoc_logger")


log_levels = {
    "DEBUG": logging.DEBUG,
    "INFO": logging.INFO,
    "WARNING": logging.WARNING,
    "ERROR": logging.ERROR,
    "CRITICAL": logging.CRITICAL,
}


def log_decorator(f):
    @click.pass_context
    def new_func(ctx, *args, **kwargs):
        log.setLevel(log_levels[ctx.params["log_level"]])
        log.info("Starting")
        r = ctx.invoke(f, *args, **kwargs)
        log.info("Finishing")
        return r

    return update_wrapper(new_func, f)


def time_decorator(f):
    @click.pass_context
    def new_func(ctx, *args, **kwargs):
        t1 = time.perf_counter()
        try:
            r = ctx.invoke(f, *args, **kwargs)
            return r
        except Exception as e:
            raise e
        finally:
            t2 = time.perf_counter()
            mins = math.floor(t2 - t1) // 60
            hours = mins // 60
            secs = (t2 - t1) - 60 * mins - 3600 * hours
            log.info(f"Execution in {hours:02d}:{mins:02d}:{secs:0.4f}")

    return update_wrapper(new_func, f)


def profile_decorator(f):
    @click.pass_context
    def new_func(ctx, *args, **kwargs):
        if ctx.params["profiling"]:
            with cProfile.Profile() as profile:
                r = ctx.invoke(f, *args, **kwargs)
                with open(ctx.params["profiling_file"], "w") as sfs:
                    pstats.Stats(profile, stream=sfs).strip_dirs().sort_stats(
                        ctx.params["profiling_sort_key"]
                    ).print_stats()
                return r
        else:
            r = ctx.invoke(f, *args, **kwargs)
            return r

    return update_wrapper(new_func, f)


def validate_day(ctx, param, value):
    # kinda also validates the year
    now = datetime.datetime.now()
    if value < 0:
        raise click.BadParameter("The day must be a positive integer")
    if value <= 25 and (ctx.params["year"] < now.year and ctx.params["year"] >= 2015):
        return value
    elif ctx.params["year"] == now.year:
        if value <= now.day and now.month == 12:
            return value
        elif now.month < 12:
            raise click.BadParameter("Chill! AoC didn't start yet.")
        elif value > now.day:
            raise click.BadParameter(f"Chill! Day {value} is not ready yet.")
        else:
            raise click.BadParameter(
                f"Don't know what you input as a day, but it's wrong."
            )
    elif value > 25:
        raise click.BadParameter(
            f"Day must be between 1 and 25, you've entered {value}"
        )
    else:
        raise click.BadParameter("Invalid date of task")


def simpler_day(ctx, param, value):
    if value > 0 and value <= 25:
        return value
    else:
        raise click.BadParameter(
            f"Day must be between 1 and 25, you've entered {value}"
        )


def validate_year(ctx, param, value):
    now = datetime.datetime.now()
    if value <= now.year and value >= 2015:
        return value
    else:
        raise click.BadParameter(f"AoC wasn't happening in year {value}")


@click.group()
def cli():
    pass


@cli.command()
@click.option(
    "-y",
    "--year",
    default=datetime.datetime.now().year,
    type=int,
    show_default=True,
    help="Year of the event",
    callback=validate_year,
)
@click.option(
    "-d",
    "--day",
    default=datetime.datetime.now().day,
    type=int,
    show_default=True,
    help="Day of the event",
    callback=simpler_day,
)
@click.option(
    "--log-level",
    default="WARNING",
    type=click.Choice(["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]),
    show_default=True,
    help="Set logging level.",
    envvar="LOG_LEVEL",
)
@log_decorator
@time_decorator
def prepare(year, day, log_level):
    """Prepare the template and the test for a given day"""
    slug = f"{year}-{day}"
    current_dir = pathlib.Path(__file__).resolve().parents[0]
    log.info("Creating {}".format(current_dir / "aoc" / f"year{year}" / f"day{day}.py"))
    pathlib.Path(current_dir / "aoc" / f"year{year}").mkdir(parents=True, exist_ok=True)
    with open(current_dir / "aoc" / f"year{year}" / f"day{day}.py", "w") as f:
        f.write(
            """# {}
import logging

log = logging.getLogger(\"aoc_logger\")

def parse_data(in_data):
    data = list()
    for line in in_data.splitlines():
        data.append(line)
    return data

def part1(in_data, test=False):
    data = parse_data(in_data)
    return \"part1 output {}\"

def part2(in_data, test=False):
    data = parse_data(in_data)
    return \"part2 output {}\"
""".format(
                slug, slug, slug
            )
        )
    log.info(
        "Creating {}".format(current_dir / "tests" / f"year{year}" / f"day{day}.py")
    )
    pathlib.Path(current_dir / "tests" / f"year{year}").mkdir(
        parents=True, exist_ok=True
    )
    with open(
        current_dir / "tests" / f"year{year}" / f"test_year{year}_day{day}.py", "w"
    ) as f:
        f.write(
            """# test {}

import pytest

from aoc.year{}.day{} import part1, part2

in_data1 = \"\"\"
\"\"\"
part1_ans = \"part1 output {}\"

def test_part1():
    assert str(part1(in_data1, True)) == part1_ans

in_data2 = in_data1
part2_ans = \"part2 output {}\"

def test_part2():
    assert str(part2(in_data2, True)) == part2_ans
        
        
""".format(
                slug, year, day, slug, slug
            )
        )
    return 0


@cli.command()
@click.option(
    "--aoc-token",
    type=str,
    envvar="AOC_TOKEN",
    required=True,
    help="Token for aoc API",
)
@click.option(
    "--aoc-url",
    type=str,
    envvar="AOC_URL",
    default="https://adventofcode.com",
    help="Base URL for aoc",
)
@click.option(
    "--proxy",
    is_flag=True,
    help="Whether to use the proxy",
    envvar="PROXY",
)
@click.option(
    "--proxy-address",
    default="http://localhost:8080",
    help="Proxy address",
    envvar="PROXY_ADDRESS",
)
@click.option(
    "--profiling",
    default=False,
    is_flag=True,
    help="Profile the program - get performance data",
)
@click.option(
    "--profiling-file",
    help="Profiling output file",
    type=click.Path(writable=True, file_okay=True, dir_okay=False),
    default=f"/tmp/advent_of_code_profile.log",
    show_default=True,
)
@click.option(
    "--profiling-sort-key",
    help="Profiling sort key",
    type=click.Choice(
        [
            "calls",
            "cumulative",
            "cumtime",
            "file",
            "filename",
            "module",
            "ncalls",
            "pcalls",
            "line",
            "name",
            "nfl",
            "stdname",
            "time",
            "tottime",
        ]
    ),
    default="cumulative",
    show_default=True,
)
@click.option(
    "-y",
    "--year",
    default=datetime.datetime.now().year,
    type=int,
    show_default=True,
    help="Year of the event",
    callback=validate_year,
)
@click.option(
    "-d",
    "--day",
    default=datetime.datetime.now().day,
    type=int,
    show_default=True,
    help="Day of the event",
    callback=validate_day,
)
@click.option(
    "-s",
    "--autosubmit",
    default=False,
    type=bool,
    is_flag=True,
    help="Submit the solution right away?",
)
@click.option(
    "--log-level",
    default="WARNING",
    type=click.Choice(["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]),
    show_default=True,
    help="Set logging level.",
    envvar="LOG_LEVEL",
)
@log_decorator
@time_decorator
@profile_decorator
def solve(
    aoc_token,
    aoc_url,
    proxy,
    proxy_address,
    profiling,
    profiling_file,
    profiling_sort_key,
    year,
    day,
    autosubmit,
    log_level,
):
    """Solve for the input of a given day"""
    # ======================================================================
    #                        Your script starts here!
    # ======================================================================
    proxies = {"http": proxy_address, "https": proxy_address}

    log.info("Init service session...")
    aoc_session = requests.Session()
    aoc_session.cookies["session"] = aoc_token
    if proxy:
        log.info("Got proxy {} for service {}".format(proxies, "aoc"))
        aoc_session.proxies.update(proxies)
        aoc_session.verify = False

    log.info("Get input")
    resp = aoc_session.get(f"https://adventofcode.com/{year}/day/{day}/input")
    data = resp.text

    log.info("Get stars")
    stars = 0
    headers = {"Cache-Control": "no-cache", "Pragma": "no-cache"}
    resp = aoc_session.get(
        f"https://adventofcode.com/{year}/day/{day}", headers=headers
    )
    pattern = "Your puzzle answer was"
    stars = len(re.findall(pattern, resp.text))
    log.info(f"Got {stars} stars on this day")

    # import solution

    for part in range(1, 3):
        try:
            solve_day = __import__(
                f"aoc.year{year}.day{day}", globals(), locals(), [f"part{part}"], 0
            )
            log.info(f"Solving {year}, day {day}, part {part}...")
            output = vars(solve_day)[f"part{part}"](data)
            click.echo(output)
            send_it = False
            if autosubmit and stars < part:
                send_it = True
            elif stars < part:
                send_it = click.confirm(
                    f"Send the answer {output} for {year}, day {day}, part {part}?"
                )
            if send_it:
                resp = aoc_session.post(
                    f"https://adventofcode.com/{year}/day/{day}/answer",
                    data={"level": str(part), "answer": str(output)},
                )
                soup = BeautifulSoup(resp.text, "html.parser")
                click.echo(soup.find("article").find("p").text)
        except ModuleNotFoundError as e:
            if f"No module named 'aoc.year{year}.day{day}'" in str(e):
                log.critical(
                    f"Solution for {year}, day {day} part {part} not implemented!"
                )
            else:
                log.critical(str(e))
        except Exception as e:
            log.critical(str(e))
            raise e

    return 0


if __name__ == "__main__":
    cli()
