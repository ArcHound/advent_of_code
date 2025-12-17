import datetime
import click
import logging

log = logging.getLogger("aoc_logger")


def days_in_year(year):
    if year >= 2015 and year <= 2024:
        return 25
    else:
        return 12


def get_last_day(year):
    return days_in_year(year)


def validate_day(ctx, param, value):
    # kinda also validates the year
    now = datetime.datetime.now()
    if value < 0:
        raise click.BadParameter("The day must be a positive integer")
    if value <= days_in_year(ctx.params["year"]) and (
        ctx.params["year"] < now.year and ctx.params["year"] >= 2015
    ):
        return value
    elif value > 12 and days_in_year(ctx.params["year"]) == 12:
        raise click.BadParameter(f"Sadly, since 2025 there are only 12 days :(")
    elif ctx.params["year"] == now.year:
        if value < now.day and now.month == 12:
            return value
        elif value == now.day and now.month == 12 and now.hour >= 5:
            return value
        elif now.month < 12:
            raise click.BadParameter("Chill! AoC didn't start yet.")
        elif value > now.day or now.hour < 5:
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


def validate_day_simple(ctx, param, value):
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
