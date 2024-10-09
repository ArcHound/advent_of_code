import logging
import pathlib

log = logging.getLogger("aoc_logger")

solution_module = "aoc"
test_module = "tests"


def make_dirs(workspace, year):
    pathlib.Path(workspace / solution_module / f"year{year}").mkdir(
        parents=True, exist_ok=True
    )
    pathlib.Path(workspace / test_module / f"year{year}").mkdir(
        parents=True, exist_ok=True
    )


def get_solution_path(workspace, year, day):
    return pathlib.Path(workspace / solution_module / f"year{year}" / f"day{day:02}.py")


def get_test_path(workspace, year, day):
    return pathlib.Path(
        workspace / test_module / f"year{year}" / f"test_year{year}_day{day:02}.py"
    )


def get_module_str(year, day):
    return f"{solution_module}.year{year}.day{day:02}"


def get_solution_f(year, day, part):
    try:
        solve_day = __import__(
            get_module_str(year, day),
            globals(),
            locals(),
            [f"part{part}"],
            0,
        )
        return vars(solve_day)[f"part{part}"]
    except ModuleNotFoundError as e:
        if f"No module named '{get_module_str(year, day)}'" in str(e):
            raise ModuleNotFoundError(
                f"Solution for {year}, day {day} part {part} not implemented!"
            )
        else:
            raise e
