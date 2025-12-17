# 2015-22

from abc import ABC, abstractmethod
import logging
from dataclasses import dataclass
from collections import deque

log = logging.getLogger("aoc_logger")

#  Magic Missile costs 53 mana. It instantly does 4 damage.
#  Drain costs 73 mana. It instantly does 2 damage and heals you for 2 hit points.
#  Shield costs 113 mana. It starts an effect that lasts for 6 turns. While it is active, your armor is increased by 7.
#  Poison costs 173 mana. It starts an effect that lasts for 6 turns. At the start of each turn while it is active, it deals the boss 3 damage.
#  Recharge costs 229 mana. It starts an effect that lasts for 5 turns. At the start of each turn while it is active, it gives you 101 new mana.


@dataclass
class Impact:
    damage: int
    armor: int
    heal: int
    recharge_mana: int


@dataclass
class Spell:
    name: str
    mana: int
    instant: bool
    turns: int
    impact: Impact


def prepare_spells():
    n = Spell("NOP", 0, True, 0, Impact(0, 0, 0, 0))  # consistency
    m = Spell("Magic Missile", 53, True, 0, Impact(4, 0, 0, 0))
    d = Spell("Drain", 73, True, 0, Impact(2, 0, 2, 0))
    s = Spell("Shield", 113, False, 6, Impact(0, 7, 0, 0))
    p = Spell("Poison", 173, False, 6, Impact(3, 0, 0, 0))
    r = Spell("Recharge", 229, False, 5, Impact(0, 0, 0, 101))
    spells = [m, d, s, p, r]
    return spells, n


class Character(ABC):
    def __init__(self, hit_points, mana, spells):
        self.hit_points = hit_points
        self.mana = mana
        self.spells = spells
        self.armor = 0

    @abstractmethod
    def get_spell(self, turn, opponent):
        pass

    def hp_effect(self, hp):
        self.hit_points += hp

    def mana_effect(self, mana):
        self.mana += mana

    def get_mana(self):
        return self.mana

    def armor_effect(self, armor):
        # UGLYYYY
        if armor == 0:
            pass
        elif armor > 0 and self.armor == armor:
            pass
        else:
            self.armor += armor

    def get_armor(self):
        return self.armor

    def is_alive(self):
        return self.hit_points > 0

    def self_impact(self, impact):
        self.armor_effect(impact.armor)
        self.hp_effect(impact.heal)
        self.mana_effect(impact.recharge_mana)

    def other_impact(self, impact):
        potential_dmg = impact.damage - self.armor
        if impact.damage == 0:
            dmg = 0
        elif impact.damage > 0 and potential_dmg < 1:
            dmg = 1
        else:
            dmg = potential_dmg
        self.hp_effect(-1 * dmg)
        self.armor = 0  # ugly, but I need to dispel the effects


class Boss(Character):
    def __init__(self, hit_points, mana, spells):
        super().__init__(hit_points, mana, spells)

    def __repr__(self):
        return f"Boss(hit_points={self.hit_points}, spell={self.spells[0]})"

    def get_spell(self, turn, opponent):
        return self.spells[0]

    def return_copy(self):
        return Boss(self.hit_points, self.mana, self.spells)


class ManWithAPlan(Character):
    def __init__(self, hit_points, mana, spells, plan, nop):
        super().__init__(hit_points, mana, spells)
        self.plan = list(plan)
        self.nop = nop

    def __repr__(self):
        return f"ManWithAPlan(hit_points={self.hit_points}, mana={self.mana}, armor={self.armor})"

    def return_copy(self):
        mwap = ManWithAPlan(
            self.hit_points, self.mana, self.spells, self.plan, self.nop
        )
        mwap.armor = self.armor
        return mwap

    def get_spell(self, turn, opponent):
        return (
            self.spells[self.plan[turn // 2]]
            if turn // 2 < len(self.plan)
            else self.nop
        )

    def get_plan_cost(self):
        return sum([self.spells[i].mana for i in self.plan])

    def set_plan(self, plan):
        self.plan = plan

    def append_plan(self, spell_id):
        self.plan.append(spell_id)


@dataclass
class Effect:
    name: str
    turns: int
    impact: Impact
    owner: str
    target: str

    def return_copy(self):
        return Effect(self.name, self.turns, self.impact, self.owner, self.target)


class Arena:
    def __init__(self, player, boss):
        self.player = player.return_copy()
        self.boss = boss.return_copy()
        self.turn = 0
        self.effects = list()

    def snapshot(self):
        a = Arena(self.player, self.boss)
        a.turn = self.turn
        a.effects = [e.return_copy() for e in self.effects]
        return a

    def is_player_turn(self):
        return self.turn % 2 == 0

    def single_turn(self):
        self.make_turn()
        self.turn += 1
        return self.player.is_alive()

    def fight(self):
        while self.player.is_alive() and self.boss.is_alive():
            self.make_turn()
            self.turn += 1
        return self.player.is_alive()  # if player won, return True

    def apply_spell(self, spell, owner, target):
        owner_inst = self.player if owner == "player" else self.boss
        target_inst = self.player if target == "player" else self.boss
        impact = spell.impact
        # here I should check if I can actually afford this
        owner_inst.mana_effect(-1 * spell.mana)
        # log.debug(f"Casted for {spell.mana}, now has {owner_inst.get_mana()}")
        # I'll leave this responsibility with the planning bureou
        # there will be enough mana *waves hand*
        if spell.instant:
            # log.debug(f"Instant impact {impact}")
            owner_inst.self_impact(impact)
            target_inst.other_impact(impact)
        else:
            effect = Effect(
                name=spell.name,
                turns=spell.turns,
                impact=impact,
                owner=owner,
                target=target,
            )
            # log.debug(f"Effect {effect}")
            if len([x for x in self.effects if x.name == effect.name]) == 0:
                self.effects.append(effect)

    def apply_effect(self, effect):
        owner_inst = self.player if effect.owner == "player" else self.boss
        target_inst = self.player if effect.target == "player" else self.boss
        owner_inst.self_impact(effect.impact)
        target_inst.other_impact(effect.impact)

    def make_turn(self):
        # log.debug(f"Turn {self.turn}")
        new_effects = list()
        # log.debug("Effects stage")
        for effect in self.effects:
            # log.debug(effect)
            effect.turns -= 1
            if effect.turns >= 0:
                self.apply_effect(effect)
            if effect.turns > 0:
                new_effects.append(effect)
        self.effects = new_effects
        # log.debug(self.player)
        # log.debug(self.boss)
        # log.debug("Spell stage")
        if not self.player.is_alive() or not self.boss.is_alive():
            # should be per effect, but in this case it's ok
            # log.debug("someone is dead!")
            # log.debug("-----------------")
            return
        if self.is_player_turn():
            spell = self.player.get_spell(self.turn, self.boss)
            # log.debug(f"Player casts {spell}")
            self.apply_spell(spell, "player", "boss")
        else:
            spell = self.boss.get_spell(self.turn, self.player)
            # log.debug(f"Boss casts {spell}")
            self.apply_spell(spell, "boss", "player")
        # log.debug("-----------------")


def parse_data(in_data):
    data = list()
    hp, d = (0, 0)
    for line in in_data.splitlines():
        if "Hit Points" in line:
            hp = int(line.strip().split(": ")[1])
        elif "Damage" in line:
            d = int(line.strip().split(": ")[1])
    return Boss(hp, 0, [Spell("Smack", 0, True, 0, Impact(d, 0, 0, 0))])


def part1(in_data, test=False):
    boss = parse_data(in_data)
    hp = 50
    mana = 500
    if test:
        hp = 10
        mana = 250
    spells, nop = prepare_spells()
    log.debug(spells)
    log.debug(boss)
    all_spells = spells + [nop]
    # if boss.hit_points == 13:
    #     plan = [3,0]
    # elif boss.hit_points == 14:
    #     plan = [4,2,1,3,0]
    # player = ManWithAPlan(hp, mana, spells, plan, nop)
    # arena = Arena(player, boss)
    # result = arena.fight()
    # log.debug(arena.player)
    # log.debug(arena.boss)
    # log.debug(f"Player won? {result}")
    # return player.get_plan_cost()
    player = ManWithAPlan(hp, mana, spells, [], nop)
    a = Arena(player, boss)
    # we'll be working with snapshots and bfs
    q = deque([([], a)])
    min_cost = -1
    while len(q) > 0:
        plan, arena = q.popleft()
        # log.debug(plan)
        if min_cost != -1 and arena.player.get_plan_cost() > min_cost:
            continue
        for s in range(len(spells)):
            # log.debug(f"spell_id: {s}")
            arena_b = arena.snapshot()
            # log.debug(arena_b.player)
            # log.debug(arena_b.boss)
            # log.debug(arena_b.effects)
            arena_b.player.append_plan(s)
            # log.debug(arena_b.player.plan)
            arena_b.single_turn()
            # log.debug(arena_b.player)
            # log.debug(arena_b.boss)
            if arena_b.player.get_mana() < 0:
                # log.debug("no mana")
                continue
            if not arena_b.boss.is_alive():
                # log.debug("boss dead")
                if min_cost == -1 or arena_b.player.get_plan_cost() < min_cost:
                    min_cost = arena_b.player.get_plan_cost()
                    log.error(arena_b.player.plan)
                    log.error(min_cost)
                continue
            arena_b.single_turn()
            if not arena_b.boss.is_alive():
                # log.debug("boss dead")
                if min_cost == -1 or arena_b.player.get_plan_cost() < min_cost:
                    min_cost = arena_b.player.get_plan_cost()
                    log.error(arena_b.player.plan)
                    log.error(min_cost)
                continue
            if not arena_b.player.is_alive():
                # log.debug("player dead")
                continue
            # log.debug(arena_b.effects)
            new_plan = plan + [s]
            q.append((new_plan, arena_b))
            # log.debug('--------')
    return min_cost


def part2(in_data, test=False):
    boss = parse_data(in_data)
    hp = 50
    mana = 500
    if test:
        hp = 10
        mana = 250
    spells, nop = prepare_spells()
    log.debug(spells)
    log.debug(boss)
    all_spells = spells + [nop]
    # if boss.hit_points == 13:
    #     plan = [3,0]
    # elif boss.hit_points == 14:
    #     plan = [4,2,1,3,0]
    # player = ManWithAPlan(hp, mana, spells, plan, nop)
    # arena = Arena(player, boss)
    # result = arena.fight()
    # log.debug(arena.player)
    # log.debug(arena.boss)
    # log.debug(f"Player won? {result}")
    # return player.get_plan_cost()
    player = ManWithAPlan(hp, mana, spells, [], nop)
    a = Arena(player, boss)
    # we'll be working with snapshots and bfs
    q = deque([([], a)])
    min_cost = -1
    while len(q) > 0:
        plan, arena = q.popleft()
        # log.debug(plan)
        if min_cost != -1 and arena.player.get_plan_cost() > min_cost:
            continue
        for s in range(len(spells)):
            # log.debug(f"spell_id: {s}")
            arena_b = arena.snapshot()
            # log.debug(arena_b.player)
            # log.debug(arena_b.boss)
            # log.debug(arena_b.effects)
            arena_b.player.append_plan(s)
            arena_b.player.hp_effect(-1)  # hard mode
            # log.debug(arena_b.player.plan)
            arena_b.single_turn()
            # log.debug(arena_b.player)
            # log.debug(arena_b.boss)
            if arena_b.player.get_mana() < 0:
                # log.debug("no mana")
                continue
            if not arena_b.boss.is_alive():
                # log.debug("boss dead")
                if min_cost == -1 or arena_b.player.get_plan_cost() < min_cost:
                    min_cost = arena_b.player.get_plan_cost()
                    log.error(arena_b.player.plan)
                    log.error(min_cost)
                continue
            arena_b.single_turn()
            if not arena_b.boss.is_alive():
                # log.debug("boss dead")
                if min_cost == -1 or arena_b.player.get_plan_cost() < min_cost:
                    min_cost = arena_b.player.get_plan_cost()
                    log.error(arena_b.player.plan)
                    log.error(min_cost)
                continue
            if not arena_b.player.is_alive():
                # log.debug("player dead")
                continue
            # log.debug(arena_b.effects)
            new_plan = plan + [s]
            q.append((new_plan, arena_b))
            # log.debug('--------')
    return min_cost
