# 2022-8
import logging

log = logging.getLogger("aoc_logger")


def prepare_grid(grid):
    return [[int(c) for c in l.strip()] for l in grid.splitlines()]


def visible_trees_count(grid):
    data = prepare_grid(grid)
    count = 0
    for i in range(len(data)):
        for j in range(len(data[i])):
            tree_h = data[i][j]
            if i == 0 or i == len(data) - 1 or j == 0 or j == len(data[i]) - 1:
                count += 1
                logging.debug(f"Tree {tree_h} at {i}, {j} visible - edge")
                continue
            top_visible = True
            bottom_visible = True
            for k in range(len(data)):
                if tree_h <= data[k][j] and k != i:
                    if k < i:
                        top_visible = False
                        logging.debug(
                            f"Tree {tree_h} at {i}, {j} not top visible - inner"
                        )
                    if k > i:
                        bottom_visible = False
                        logging.debug(
                            f"Tree {tree_h} at {i}, {j} not bottom visible - inner"
                        )
            left_visible = True
            right_visible = True
            for l in range(len(data[i])):
                if tree_h <= data[i][l] and l != j:
                    if l < j:
                        left_visible = False
                        logging.debug(
                            f"Tree {tree_h} at {i}, {j} not left visible - inner"
                        )
                    if l > j:
                        right_visible = False
                        logging.debug(
                            f"Tree {tree_h} at {i}, {j} not right visible - inner"
                        )
            if top_visible or bottom_visible or left_visible or right_visible:
                count += 1
                logging.debug(f"Tree {tree_h} at {i}, {j} visible - inner")
            else:
                logging.debug(f"Tree {tree_h} at {i}, {j} not visible - inner")
    return count


def max_scenic_score(grid):
    data = prepare_grid(grid)
    max_score = 0
    for i in range(len(data)):
        for j in range(len(data[i])):
            tree_h = data[i][j]
            if i == 0 or i == len(data) - 1 or j == 0 or j == len(data[i]) - 1:
                logging.debug(f"Tree {tree_h} at {i}, {j} visible - edge")
                continue
            top_score = 0
            bottom_score = 0
            left_score = 0
            right_score = 0
            k = i + 1
            while k < len(data):
                bottom_score += 1
                if tree_h <= data[k][j]:
                    break
                k += 1
            logging.debug(f"Tree {tree_h} at {i}, {j} bottom score {bottom_score}")
            k = i - 1
            while k >= 0:
                top_score += 1
                if tree_h <= data[k][j]:
                    break
                k -= 1
            logging.debug(f"Tree {tree_h} at {i}, {j} top score {top_score}")
            k = j + 1
            while k < len(data[i]):
                right_score += 1
                if tree_h <= data[i][k]:
                    break
                k += 1
            logging.debug(f"Tree {tree_h} at {i}, {j} right score {right_score}")
            k = j - 1
            while k >= 0:
                left_score += 1
                if tree_h <= data[i][k]:
                    break
                k -= 1
            logging.debug(f"Tree {tree_h} at {i}, {j} left score {left_score}")
            tree_score = top_score * bottom_score * left_score * right_score
            if tree_score > max_score:
                logging.debug(f"New max: tree {tree_h} score {tree_score}")
                max_score = tree_score
            logging.debug("--------------------------------------")
    return max_score


def part1(in_data):
    return visible_trees_count(in_data)


def part2(in_data):
    return max_scenic_score(in_data)
