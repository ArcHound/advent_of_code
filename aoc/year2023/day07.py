# 2023-7
import logging
from collections import defaultdict

log = logging.getLogger("aoc_logger")


def parse(in_data):
    # order of the symbol cards
    translate = {"T": "B", "J": "C", "Q": "D", "K": "E", "A": "F"}
    vals = list()
    for line in in_data.splitlines():
        # technique
        hand = line.split(" ")[0]
        val = int(line.split(" ")[1])
        rank = defaultdict(int)
        handval = ""
        transhand = ""
        # I need to count the cards into pairs and such
        for c in hand:
            rank[c] += 1
            if c in translate:
                transhand += translate[
                    c
                ]  # I also need to translate the JQKA so that I can order the hands alphabetically
            else:
                transhand += c
        log.debug(rank)
        # now I need to work with the pairs and their symbols -> for each val I need a list of characters
        flipped = defaultdict(list)
        for c in rank:
            flipped[rank[c]].append(c)
        log.debug(flipped)
        # to keep the idea of alphabetical ordering, we need to prepend the hand with a unique symbol
        if len(flipped[1]) == 5:  # high card
            handval = "1" + transhand
        elif len(flipped[1]) == 3 and len(flipped[2]) == 1:  # one pair
            handval = "2" + transhand
        elif len(flipped[2]) == 2:  # two pair
            handval = "3" + transhand
        elif len(flipped[3]) == 1 and len(flipped[1]) == 2:  # triple
            handval = "4" + transhand
        elif len(flipped[3]) == 1 and len(flipped[2]) == 1:  # full-house
            handval = "5" + transhand
        elif len(flipped[4]) == 1:  # poker
            handval = "6" + transhand
        elif len(flipped[5]) == 1:  # poker++
            handval = "7" + transhand
        vals.append((handval, val))
    return vals


def part1(in_data):
    vals = parse(in_data)
    log.debug(vals)
    # since we worked hard before, now we need to sort alphabetically
    sorted_vals = sorted(vals, key=lambda x: x[0])
    log.debug(sorted_vals)
    count = 0
    # use the spec
    for i in range(len(sorted_vals)):
        count += (i + 1) * sorted_vals[i][1]
    return count


def parse2(in_data):
    # we have a different order
    translate = {"J": "1", "T": "C", "Q": "D", "K": "E", "A": "F"}
    vals = list()
    for line in in_data.splitlines():
        hand = line.split(" ")[0]
        val = int(line.split(" ")[1])
        rank = defaultdict(int)
        joker_count = 0
        handval = ""
        transhand = ""
        for c in hand:
            rank[c] += 1
            if c in translate:
                if c == "J":
                    joker_count += 1
                transhand += translate[c]
            else:
                transhand += c
        log.debug(rank)
        flipped = defaultdict(list)
        for c in rank:
            flipped[rank[c]].append(c)
        log.debug(flipped)
        # may I interest you in some spaghetti?
        # it's fast and fastly written
        # there are only a few combinations of card counts and jokers leading to respective hands
        # most of the time if you have jokers you're going to get higher number of kind. The only exception I recall is two pairs, one joker -> full-house
        # this would benefit from a fat test-suite
        if len(flipped[1]) == 5 and joker_count == 0:  # high card
            handval = "1" + transhand
            log.debug("High card")
        elif (len(flipped[1]) == 3 and len(flipped[2]) == 1 and joker_count == 0) or (
            len(flipped[1]) == 5 and joker_count == 1
        ):
            handval = "2" + transhand
            log.debug("one pair")
        elif len(flipped[2]) == 2 and joker_count == 0:  # two pair
            log.debug("two pair")
            handval = "3" + transhand
        elif (
            (len(flipped[3]) == 1 and len(flipped[1]) == 2 and joker_count == 0)
            or (len(flipped[2]) == 1 and joker_count == 1)
            or (len(flipped[1]) == 3 and joker_count == 2)
        ):  # triple
            log.debug("triple")
            handval = "4" + transhand
        elif (len(flipped[3]) == 1 and len(flipped[2]) == 1 and joker_count == 0) or (
            len(flipped[2]) == 2 and joker_count == 1
        ):
            log.debug("full-house")
            handval = "5" + transhand
        elif (
            (len(flipped[4]) == 1 and joker_count == 0)
            or (len(flipped[3]) == 1 and joker_count == 1)
            or (len(flipped[2]) == 2 and joker_count == 2)
            or (len(flipped[1]) == 2 and joker_count == 3)
        ):
            log.debug("poker")
            handval = "6" + transhand
        elif (
            (len(flipped[5]) == 1)
            or (len(flipped[4]) == 1 and joker_count == 1)
            or (len(flipped[3]) == 1 and joker_count == 2)
            or (len(flipped[2]) == 1 and joker_count == 3)
            or joker_count == 4
        ):
            log.debug("poker++")
            handval = "7" + transhand
        log.debug(f"hand {hand} handval {handval}")
        vals.append((handval, val))
    return vals


def part2(in_data):
    vals = parse2(in_data)
    log.debug(vals)
    # this part is the same as part1 and it's so simple that I am keeping it like this
    sorted_vals = sorted(vals, key=lambda x: x[0])
    log.debug(sorted_vals)
    count = 0
    for i in range(len(sorted_vals)):
        count += (i + 1) * sorted_vals[i][1]
    return count
