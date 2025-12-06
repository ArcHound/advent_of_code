# 2015-15

import logging
from dataclasses import dataclass
from itertools import combinations
from tqdm import tqdm
import re

log = logging.getLogger("aoc_logger")


@dataclass(frozen=True)
class Ingredient:
    name: str
    capacity: int
    durability: int
    flavor: int
    texture: int
    calories: int


@dataclass
class Recipe:
    ingredients: dict
    ingredient_total: int
    capacity: int
    durability: int
    flavor: int
    texture: int
    calories: int

    def part1_eval(self):
        if (
            self.capacity <= 0
            or self.durability <= 0
            or self.flavor <= 0
            or self.texture <= 0
        ):
            return 0
        else:
            return self.capacity * self.durability * self.flavor * self.texture

    def part2_eval(self):
        if (
            self.capacity <= 0
            or self.durability <= 0
            or self.flavor <= 0
            or self.texture <= 0
            or self.calories != 500
        ):
            return 0
        else:
            return self.capacity * self.durability * self.flavor * self.texture


ex_pattern = "(?P<name>[A-Z][a-z]*): capacity (?P<cap>-?[0-9]*), durability (?P<dur>-?[0-9]*), flavor (?P<fla>-?[0-9]*), texture (?P<tex>-?[0-9]*), calories (?P<cal>-?[0-9]*)"


def parse_data(in_data):
    ingredients = list()
    for line in in_data.splitlines():
        match = re.search(ex_pattern, line.strip())
        ingredients.append(
            Ingredient(
                name=match.group("name"),
                capacity=int(match.group("cap")),
                durability=int(match.group("dur")),
                flavor=int(match.group("fla")),
                texture=int(match.group("tex")),
                calories=int(match.group("cal")),
            )
        )
    return ingredients


def create_recipe_2(ingredient_dict, iid1, iid2, q1, q2):
    return Recipe(
        ingredients={iid1: q1, iid2: q2},
        ingredient_total=q1 + q2,
        capacity=(
            ingredient_dict[iid1].capacity * q1 + ingredient_dict[iid2].capacity * q2
        ),
        durability=(
            ingredient_dict[iid1].durability * q1
            + ingredient_dict[iid2].durability * q2
        ),
        flavor=(ingredient_dict[iid1].flavor * q1 + ingredient_dict[iid2].flavor * q2),
        texture=(
            ingredient_dict[iid1].texture * q1 + ingredient_dict[iid2].texture * q2
        ),
        calories=(
            ingredient_dict[iid1].calories * q1 + ingredient_dict[iid2].calories * q2
        ),
    )


def create_recipe_n_1(ingredient_dict, iid, q, other_recipe):
    new_ingredients = dict(other_recipe.ingredients)
    new_ingredients[iid] = q
    return Recipe(
        ingredients=new_ingredients,
        ingredient_total=q + other_recipe.ingredient_total,
        capacity=(ingredient_dict[iid].capacity * q + other_recipe.capacity),
        durability=(ingredient_dict[iid].durability * q + other_recipe.durability),
        flavor=(ingredient_dict[iid].flavor * q + other_recipe.flavor),
        texture=(ingredient_dict[iid].texture * q + other_recipe.texture),
        calories=(ingredient_dict[iid].calories * q + other_recipe.calories),
    )


def brute_force(ingredient_dict, total_capacity=100):
    cache = dict()
    nodes = [i for i in ingredient_dict]
    for t in tqdm(range(2, len(nodes) + 1)):
        for p in combinations(nodes, t):
            if len(p) == 2:
                pair = frozenset((p[0], p[1]))
                for i in range(total_capacity):
                    for j in range(i):
                        if j + i > total_capacity:
                            break
                        if i + j not in cache:
                            cache[i + j] = dict()
                        if pair not in cache[i + j]:
                            cache[i + j][pair] = list()
                            # log.debug(f"adding {pair} at {i+j}")
                        r1 = create_recipe_2(ingredient_dict, p[0], p[1], i, j)
                        r2 = create_recipe_2(ingredient_dict, p[0], p[1], j, i)
                        cache[i + j][pair].append(r1)
                        cache[i + j][pair].append(r2)
            else:
                for ing in p:
                    others = frozenset([x for x in p if x != ing])
                    this_set = frozenset(p)
                    # log.debug(f"{this_set} > {others}")
                    for i in range(total_capacity):
                        for j in range(len(others), total_capacity):
                            if j + i > total_capacity:
                                break
                            if j + i not in cache:
                                cache[i + j] = dict()  # shouldn't happen, but anyway
                            if this_set not in cache[i + j]:
                                cache[i + j][this_set] = list()
                                # log.debug(f"adding {this_set} at {i+j}")
                            for recipe in cache[j][others]:
                                r1 = create_recipe_n_1(ingredient_dict, ing, i, recipe)
                                cache[i + j][this_set].append(r1)
    return cache


def part1(in_data, test=False):
    total_capacity = 100
    ingredients = parse_data(in_data)
    ingredient_dict = {i: ingredients[i] for i in range(len(ingredients))}
    cache = brute_force(ingredient_dict, total_capacity=total_capacity)
    max_val = 0
    for fs in tqdm(cache[total_capacity]):
        for x in cache[total_capacity][fs]:
            if x.part1_eval() > max_val:
                max_val = x.part1_eval()
    return max_val


def part2(in_data, test=False):
    total_capacity = 100
    ingredients = parse_data(in_data)
    ingredient_dict = {i: ingredients[i] for i in range(len(ingredients))}
    cache = brute_force(ingredient_dict, total_capacity=total_capacity)
    max_val = 0
    for fs in tqdm(cache[total_capacity]):
        for x in cache[total_capacity][fs]:
            if x.part2_eval() > max_val:
                max_val = x.part2_eval()
    return max_val
