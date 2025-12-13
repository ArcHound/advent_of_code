# 2015-21

import logging
from dataclasses import dataclass
from itertools import combinations
from tqdm import tqdm

log = logging.getLogger("aoc_logger")

shop_weapons = """
Dagger        8     4       0
Shortsword   10     5       0
Warhammer    25     6       0
Longsword    40     7       0
Greataxe     74     8       0
"""

shop_armors = """
Leather      13     0       1
Chainmail    31     0       2
Splintmail   53     0       3
Bandedmail   75     0       4
Platemail   102     0       5
"""

shop_rings = """
Damage +1    25     1       0
Damage +2    50     2       0
Damage +3   100     3       0
Defense +1   20     0       1
Defense +2   40     0       2
Defense +3   80     0       3
"""


@dataclass
class Item:
    item_type: str
    cost: int
    damage: int
    armor: int


@dataclass
class Outfit:
    cost: int
    damage: int
    armor: int


@dataclass
class Shop:
    weapons: list[Item]
    armors: list[Item]
    rings: list[Item]

    def generate_outfits(self):
        outfits = list()
        for w in self.weapons:
            for a in self.armors:
                for r1, r2 in combinations(self.rings, 2):
                    outfits.append(
                        Outfit(
                            cost=w.cost + a.cost + r1.cost + r2.cost,
                            damage=w.damage + a.damage + r1.damage + r2.damage,
                            armor=w.armor + a.armor + r1.armor + r2.armor,
                        )
                    )
        return outfits


@dataclass
class Player:
    hit_points: int
    damage: int
    armor: int

    @classmethod
    def fight(cls, first, second):
        hp_first = first.hit_points
        hp_second = second.hit_points
        while hp_first > 0 and hp_second > 0:
            dmg = first.damage - second.armor
            hp_second -= dmg if dmg > 0 else 1
            if hp_second <= 0:
                break
            dmg = second.damage - first.armor
            hp_first -= dmg if dmg > 0 else 1
        return hp_second <= 0


def parse_shop_item(data, item_type):
    result = list()
    for line in data.splitlines():
        if line.strip() != "":
            tokens = [x for x in line.strip().split(" ") if x != ""]
            result.append(
                Item(item_type, int(tokens[-3]), int(tokens[-2]), int(tokens[-1]))
            )
    # add none item for consistency
    if item_type == "ring":
        # add two
        result.append(Item(item_type, 0, 0, 0))
        result.append(Item(item_type, 0, 0, 0))
    elif item_type == "armor":
        # add one
        result.append(Item(item_type, 0, 0, 0))
    # none for weapons, you must buy a weapon as per the assignment
    return result


def parse_shop():
    weapons = parse_shop_item(shop_weapons, "weapon")
    armors = parse_shop_item(shop_armors, "armor")
    rings = parse_shop_item(shop_rings, "ring")
    return Shop(weapons, armors, rings)


def parse_data(in_data):
    data = list()
    hp, d, a = (0, 0, 0)
    for line in in_data.splitlines():
        if "Hit Points" in line:
            hp = int(line.strip().split(": ")[1])
        elif "Damage" in line:
            d = int(line.strip().split(": ")[1])
        elif "Armor" in line:
            a = int(line.strip().split(": ")[1])
    return Player(hp, d, a)


def part1(in_data, test=False):
    hp = 100
    if test:
        hp = 8
    boss = parse_data(in_data)
    shop = parse_shop()
    outfits = shop.generate_outfits()
    min_cost = -1
    for o in tqdm(outfits):
        p = Player(hp, o.damage, o.armor)
        if Player.fight(p, boss) and (min_cost == -1 or o.cost < min_cost):
            min_cost = o.cost
    return min_cost


def part2(in_data, test=False):
    hp = 100
    if test:
        hp = 8
    boss = parse_data(in_data)
    shop = parse_shop()
    outfits = shop.generate_outfits()
    max_cost = -1
    for o in tqdm(outfits):
        p = Player(hp, o.damage, o.armor)
        if not Player.fight(p, boss) and o.cost > max_cost:
            max_cost = o.cost
            log.error(o)
    return max_cost
