# 2022-2


def get_score(x, y):
    score = ord(y) - ord("X") + 1  # your choice points
    if x == "A":
        if y == "X":
            score += 3
        elif y == "Y":
            score += 6
        elif y == "Z":
            score += 0
    elif x == "B":
        if y == "Y":
            score += 3
        elif y == "Z":
            score += 6
        elif y == "X":
            score += 0
    elif x == "C":
        if y == "Z":
            score += 3
        elif y == "X":
            score += 6
        elif y == "Y":
            score += 0
    return score


def get_score_2(x, y):
    score = 0
    if y == "X":
        score = 0
        if x == "A":
            score += 3
        elif x == "B":
            score += 1
        elif x == "C":
            score += 2
    elif y == "Y":
        score = 3
        if x == "A":
            score += 1
        elif x == "B":
            score += 2
        elif x == "C":
            score += 3
    elif y == "Z":
        score = 6
        if x == "A":
            score += 2
        elif x == "B":
            score += 3
        elif x == "C":
            score += 1
    return score


def part1(in_data):
    data = [(x.split(" ")[0], x.split(" ")[1]) for x in in_data.splitlines()]
    return sum([get_score(x, y) for x, y in data])


def part2(in_data):
    data = [(x.split(" ")[0], x.split(" ")[1]) for x in in_data.splitlines()]
    return sum([get_score_2(x, y) for x, y in data])
