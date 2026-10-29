# 2016-05

import logging
import hashlib
import click
from random import random
from math import floor

log = logging.getLogger("aoc_logger")


def part1(in_data, test=False):
    i = 0
    done = False
    result = 0
    code = in_data.strip()
    password = ""
    while not done:
        val = hashlib.md5((code + str(i)).encode()).hexdigest()
        if val.startswith("00000"):
            password += val[5]
        if len(password) == 8:
            done = True
        i += 1
    return password


def print_scr(password, done=False):
    # 98x24
    p_0 = password.get(0, chr(floor(random() * 90) + 32))
    p_1 = password.get(1, chr(floor(random() * 90) + 32))
    p_2 = password.get(2, chr(floor(random() * 90) + 32))
    p_3 = password.get(3, chr(floor(random() * 90) + 32))
    p_4 = password.get(4, chr(floor(random() * 90) + 32))
    p_5 = password.get(5, chr(floor(random() * 90) + 32))
    p_6 = password.get(6, chr(floor(random() * 90) + 32))
    p_7 = password.get(7, chr(floor(random() * 90) + 32))

    click.secho(98 * "=", fg="green")
    click.secho("|" + 96 * " " + "|", fg="green")
    click.secho(
        "|" + 30 * " " + "Advent of Code 2016, day 5 Decryptor" + 30 * " " + "|",
        fg="green",
    )
    click.secho("|" + 96 * " " + "|", fg="green")

    click.secho(98 * "=", fg="green")
    click.echo(98 * " ")
    click.echo(98 * " ")
    click.echo(98 * " ")

    if not done:
        click.secho(
            41 * " " + "!! DECRYPTING !!" + 42 * " ", fg="red", blink=True, bold=True
        )
    else:
        click.secho(
            41 * " " + "!! SUCCESSFUL !!" + 42 * " ", fg="green", blink=True, bold=True
        )
    click.echo(98 * " ")
    click.echo(98 * " ")
    # click.echo(98*' ')

    click.echo(98 * " ")
    click.secho(
        41 * " " + f"{p_0} {p_1} {p_2} {p_3} {p_4} {p_5} {p_6} {p_7} " + 41 * " ",
        fg="blue",
        bold=True,
    )
    click.echo(98 * " ")
    # click.echo(98*' ')

    click.echo(98 * " ")
    if not done:
        click.echo(98 * " ")
    click.echo(98 * " ")
    click.secho(98 * "=", fg="green")

    click.secho("|" + 96 * " " + "|", fg="green")
    click.secho(
        "|" + 36 * " " + "(c) 2026 Miloslav Homer " + 36 * " " + "|", fg="green"
    )
    click.secho("|" + 96 * " " + "|", fg="green")
    click.secho(98 * "=", fg="green")


def part2(in_data, test=False):
    i = 0
    done = False
    result = 0
    code = in_data.strip()
    password = dict()
    while not done:
        val = hashlib.md5((code + str(i)).encode()).hexdigest()
        if val.startswith("00000"):
            digit = int(val[5], 16)
            if digit not in password and 0 <= digit and digit <= 7:
                password[digit] = val[6]
        if len(password) == 8:
            done = True
        i += 1
        if i % 1000 == 0:
            print_scr(password)
    final_pass = ""
    for i in range(8):
        final_pass += password[i]
    print_scr(password, True)
    return final_pass
