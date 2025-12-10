# 2025-10

import logging
from dataclasses import dataclass
from itertools import combinations
from z3 import *
from tqdm import tqdm

log = logging.getLogger("aoc_logger")


@dataclass
class Puzzle:
    length: int
    target: int
    buttons: list[tuple[int, int]]
    joltages: list[int]

    def press_buttons(self, buttons, start=0):
        reg = start
        for b in buttons:
            reg ^= sum([pow(2, self.length - 1 - x) for x in b])
        return reg

    def solve_switches(self):
        for i in range(1 + len(self.buttons)):
            for c in combinations(self.buttons, i):
                if self.press_buttons(c) == self.target:
                    return i

    def solve_joltages(self):
        # this can be done with solving a linear equation with positive integer solutions
        # yes, z3 solver time
        # take the first example (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}
        # we are looking for integers that will note how many presses of a button we need
        # so put the buttons as vectors in the columns
        # this can be written into a matrix like so (excuse the small parentheses)
        #   0 0 0 0 1 1 | 3
        # ( 0 1 0 0 0 1 | 5 )
        #   0 0 1 1 1 0 | 4
        #   1 1 0 1 0 0 | 7
        # so let's prepare the variables
        variables = [Int(f"x_{i}") for i in range(len(self.buttons))]
        log.debug(variables)
        s = Solver()
        for v in variables:
            s.add(v >= 0)
        # now for the rows of the matrix
        for i in range(len(self.joltages)):
            j = self.joltages[i]
            expr = Sum(
                [variables[k] for k in range(len(self.buttons)) if i in self.buttons[k]]
            )
            s.add(expr == j)
        solutions = list()
        # we need to check all of the solutions, to find the minimal one
        # there is a finite number of them, I just hope there are not too many
        while s.check() == sat:
            m = s.model()
            solutions.append(m)
            s.add(
                Or(*[variables[i] != m[variables[i]] for i in range(len(self.buttons))])
            )
        # now let's just find the minimal solution by adding the applicable variables
        min_val = -1
        for solution in solutions:
            sum_var = sum([solution[var].as_long() for var in solution])
            log.debug(sum_var)
            if min_val == -1 or min_val > sum_var:
                min_val = sum_var
        return min_val


def parse_data(in_data):
    data = list()
    for line in in_data.splitlines():
        tokens = line.strip().split(" ")
        target_str = tokens[0][1:-1]
        length = len(target_str)
        target = 0
        for i in range(length):
            next_val = 1 if target_str[i] == "#" else 0
            target = target * 2 + next_val
        joltages = [int(x) for x in tokens[-1][1:-1].split(",")]
        buttons = list()
        pre_buttons = tokens[1:-1]
        for i in range(len(pre_buttons)):
            b = pre_buttons[i]
            vals = tuple([int(x) for x in b[1:-1].split(",")])
            buttons.append(vals)
        data.append(
            Puzzle(length=length, target=target, buttons=buttons, joltages=joltages)
        )
    return data


def part1(in_data, test=False):
    data = parse_data(in_data)
    total = 0
    for puzzle in tqdm(data):
        val = puzzle.solve_switches()
        total += val
    return total


def part2(in_data, test=False):
    data = parse_data(in_data)
    total = 0
    for puzzle in tqdm(data):
        val = puzzle.solve_joltages()
        total += val
    return total
