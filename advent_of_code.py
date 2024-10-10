#!/usr/bin/env python3

import logging
import time
import datetime
import math
from functools import update_wrapper
import cProfile
import pstats
import pathlib

import click
from dotenv import load_dotenv
from jinja2 import Environment, FileSystemLoader

import aoc
from aoc_tools.validators import validate_day, validate_year, validate_day_simple
from aoc_tools.pathing import (
    make_dirs,
    get_solution_path,
    get_test_path,
    get_module_str,
    get_solution_f,
)
from aoc_tools.aoc_service import AOC_Service

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
    callback=validate_day_simple,
)
@click.option(
    "-w",
    "--workspace",
    default=pathlib.Path(__file__).resolve().parents[0],
    type=click.Path(exists=True, dir_okay=True, file_okay=False, readable=True),
    show_default=True,
    help="Target dir",
)
@click.option(
    "-t",
    "--templates",
    default=pathlib.Path(__file__).resolve().parents[0] / "templates",
    type=click.Path(exists=True, dir_okay=True, file_okay=False, readable=True),
    show_default=True,
    help="Template dir",
)
@click.option(
    "--solution-template",
    default="solution.py.jinja",
    type=str,
    show_default=True,
    help="Solution template filename",
)
@click.option(
    "--test-template",
    default="test.py.jinja",
    type=str,
    show_default=True,
    help="Test template filename",
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
def prepare(
    year, day, workspace, templates, solution_template, test_template, log_level
):
    """Prepare the template and the test for a given day"""
    j_env = Environment(auto_reload=False)
    j_env.loader = FileSystemLoader(searchpath=templates)
    make_dirs(workspace, year)
    solution_path = get_solution_path(workspace, year, day)
    test_path = get_test_path(workspace, year, day)
    module = get_module_str(year, day)
    slug = f"{year}-{day:02}"
    data = {"slug": slug, "year": year, "day": day, "module": module}
    log.info("Creating {}".format(solution_path))
    try:
        with open(solution_path, "w") as f:
            f.write(j_env.get_template(solution_template).render(data=data))
    except OSError as e:
        log.critical(f"Couldn't write to {solution_path} - check file permissions")
    log.info("Creating {}".format(test_path))
    try:
        with open(test_path, "w") as f:
            f.write(j_env.get_template(test_template).render(data=data))
    except OSError as e:
        log.critical(f"Couldn't write to {test_path} - check file permissions")
    return 0


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
    "-l",
    "--list-leaderboards",
    default=False,
    type=bool,
    is_flag=True,
    help="List private leaderboards?",
)
@click.option(
    "-i",
    "--leaderboard-id",
    default=None,
    type=str,
    show_default=True,
    help="Leaderboard id (None for global leaderboard)",
)
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
    "--log-level",
    default="WARNING",
    type=click.Choice(["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]),
    show_default=True,
    help="Set logging level.",
    envvar="LOG_LEVEL",
)
@log_decorator
@time_decorator
def leaderboard(
    year,
    list_leaderboards,
    leaderboard_id,
    aoc_token,
    aoc_url,
    proxy,
    proxy_address,
    log_level,
):
    """Show leaderboard (global or private (also lists those))"""
    proxies = {"http": proxy_address, "https": proxy_address}
    aoc_svc = AOC_Service(aoc_token, aoc_url, proxy, proxies)
    username = aoc_svc.get_user()

    leaderboard_output = ""
    lids = list()
    if list_leaderboards:
        lids = aoc_svc.get_private_leaderboards()
        if len(lids) > 0:
            click.echo("Here are your private leaderboard ids:")
            for lid in lids:
                click.echo(lid)
        else:
            click.echo("You are not a member of any private leaderboard :(")
        return 0
    if leaderboard_id:
        leaderboard = aoc_svc.get_private_leaderboard(year, leaderboard_id)
        leaderboard.sort(key=lambda x: x.points, reverse=True)
        star_dict = {
            0: click.style("*", fg="black"),
            1: click.style("*", fg="white"),
            2: click.style("*", fg="yellow"),
        }
        for i in range(len(leaderboard)):
            line = f"{str(i): >3}) "
            entry = leaderboard[i]
            line += f"{str(entry.points): >4} "
            for j in range(25):
                line += star_dict[entry.completed.get(j+1, 0)]
            line += " " + str(entry.name)
            leaderboard_output += line + "\n"
    else:
        leaderboard = aoc_svc.get_global_leaderboard(year)
        leaderboard.sort(key=lambda x: x.points, reverse=True)
        leaderboard_output = "\n".join(
            [
                f"{str(i): >3}) {str(leaderboard[i].points): >4} {leaderboard[i].name}"
                for i in range(len(leaderboard))
            ]
        )
    click.echo_via_pager(leaderboard_output)
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

    aoc_svc = AOC_Service(aoc_token, aoc_url, proxy, proxies)
    puzzle_input = aoc_svc.get_input(year, day)
    stars = aoc_svc.get_stars(year, day)
    stars_to_parts = {0: [1], 1: [2], 2: [1, 2]}

    for part in stars_to_parts[stars]:
        try:
            log.info(f"Solving {year}, day {day}, part {part}...")
            solution = get_solution_f(year, day, part)
            output = solution(puzzle_input)
            click.echo(output)
            send_it = False
            if autosubmit and stars < part:
                send_it = True
            elif stars == part - 1 and not autosubmit:
                send_it = click.confirm(
                    f"Send the answer {output} for {year}, day {day}, part {part}?"
                )
            if send_it:
                success, msg = aoc_svc.send_solution(year, day, part, output)
                if success:
                    click.secho(msg, fg="green")
                else:
                    click.secho(msg, fg="red")
        except Exception as e:
            log.critical(str(e))
            raise e
    return 0


if __name__ == "__main__":
    cli()
