# 2015-19

import logging
import re
from dataclasses import dataclass, field
from collections import deque

log = logging.getLogger("aoc_logger")


@dataclass
class Node:
    word: str = None
    child_nodes: dict = field(default_factory=lambda: dict())


def parse_data(in_data):
    rules = dict()
    start = ""
    for line in in_data.splitlines():
        if " => " in line:
            f, t = line.strip().split(" => ")
            if f not in rules:
                rules[f] = list()
            rules[f].append(t)
        elif len(line.strip()) > 0:
            start = line.strip()
    return rules, start


def part1(in_data, test=False):
    rules, in_line = parse_data(in_data)
    log.debug(rules)
    cache = set()
    for mark in rules:
        for pos in [match.start() for match in re.finditer(mark, in_line)]:
            for subst in rules[mark]:
                new_str = in_line[:pos] + subst + in_line[pos + len(mark) :]
                cache.add(new_str)
    return len(cache)


pattern = "[A-Z][a-z]*"


def tokenize(string):
    return [match.group() for match in re.finditer(pattern, string)]


def transforms_back(word, root):
    tokens = tokenize(word)
    transforms = list()
    for i in range(len(tokens)):
        current_node = root
        j = 0
        decided = False
        while not decided:
            if (i + j >= len(tokens)) or (
                tokens[i + j] not in current_node.child_nodes
            ):
                decided = True
                break
            current_node = current_node.child_nodes[tokens[i + j]]
            # log.debug(current_node.word)
            # if we reach a leaf, we swap
            if current_node.word is not None:
                transforms.append(
                    "".join(tokens[:i] + [current_node.word] + tokens[i + j + 1 :])
                )
                decided = True
            j += 1  # I smell off-by-one error here
    return list(set(transforms))


def coding_tree(rules):
    # build a tree from the elements
    root = Node()
    for k, v in rules.items():
        for result in v:
            current_node = root
            for token in tokenize(result):
                if token not in current_node.child_nodes:
                    current_node.child_nodes[token] = Node()
                current_node = current_node.child_nodes[token]
            current_node.word = k
    return root


def transforms(in_tokens, tokenized_rules):
    possibilities = list()
    for i in range(len(in_tokens)):
        t = in_tokens[i]
        if t in tokenized_rules:
            for x in tokenized_rules[t]:
                possibilities.append(in_tokens[:i] + x + in_tokens[i + 1 :])
    return possibilities


def observe_result(in_tokens, rules):
    observed = dict()
    for t in in_tokens:
        if t not in rules:
            if t not in observed:
                observed[t] = 0
            observed[t] += 1
    return observed


def product_sanity_check(in_tokens, out_tokens, out_observe, rules):
    possible = True
    in_observe = observe_result(in_tokens, rules)
    if len(in_tokens) >= len(out_tokens) and in_tokens != out_tokens:
        possible = False
    immutable = set([x for x in out_tokens if x not in rules])
    for c in immutable:
        if c not in out_tokens:
            possible = False
            break
        if c in in_observe and in_observe[c] > out_observe[c]:
            possible = False
            break
    return possible


def bfs(rules, tokenized_rules, out_tokens, out_observe):
    # we'll be iterating over the word again and again
    stack = deque()
    stack.append((["e"], 0))
    min_t = -1
    saw = set()
    max_tokens = 0
    while len(stack) > 0:
        line, c = stack.popleft()
        if len(line) > max_tokens:
            log.debug(len(line))
            max_tokens = len(line)
        if line == in_line:
            if min_t == -1 or c < min_t:
                min_t = c
            continue
        possibilities = transforms(line, tokenized_rules)
        for p in possibilities:
            if product_sanity_check(p, out_tokens, out_observe, rules):
                rp = "".join(p)
                if rp not in saw:
                    saw.add(rp)
                    stack.append((p, c + 1))
    return min_t


def part2(in_data, test=False):
    rules, in_line = parse_data(in_data)
    tokenized_rules = {x: [tokenize(y) for y in rules[x]] for x in rules}
    out_tokens = tokenize(in_line)
    out_observe = observe_result(out_tokens, rules)
    log.debug(tokenized_rules)
    log.debug(out_observe)
    # after trying bruteforce from the front and from the back, I took a look at the input
    # let's assume that a solution is possible.
    # specifically for this input, we have Rn, Ar and Y which cannot be mutated
    # there are couple patterns like ?Rn?Ar, ?Rn?Y?Ar, ?Rn?Y?Y?Ar
    # the rules without Rn Y Ar always reduce by 1
    # the ?Rn?Ar reduce by 3, ?Rn?Y?Ar reduce by 5, ?Rn?Y?Y?Ar reduce by 7
    # rewriting without Rn?Ar we have:
    # ?Rn?Ar maps to ?? which reduces by 1 (as it should)
    # ?Rn?Y?Ar maps to ??Y? which reduces by 1
    # ?Rn?Y?Y?Ar maps to ??Y?Y? which reduces by 1
    # look at it again
    # whenever we see Y, we can subtract 2 reductions
    # ?Rn?Y?Ar maps to ??Y? which reduces by 3-2
    # ?Rn?Y?Y?Ar maps to ??Y?Y? which reduces by 5-4
    # so just simply:
    return (
        len(out_tokens)
        - 1
        - out_observe.get("Rn", 0)
        - out_observe.get("Ar", 0)
        - out_observe.get("Y", 0) * 2
    )
