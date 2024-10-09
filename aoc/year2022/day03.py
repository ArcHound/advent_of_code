# 2022-3


def score_item(z):
    score = 0
    if z.islower():
        score = ord(z) - ord("a") + 1
    else:
        score = ord(z) - ord("A") + 27
    return score


def part1(in_data):
    return sum(
        [
            score_item(
                list(set.intersection(set(l[: len(l) // 2]), set(l[len(l) // 2 :])))[0]
            )
            for l in in_data.splitlines()
        ]
    )


def part2(in_data):
    counter = 0
    badges = list()
    badge_0, badge_1, badge_2 = (0, 0, 0)
    for l in in_data.splitlines():
        if counter == 0:
            badge_0 = l
        elif counter == 1:
            badge_1 = l
        elif counter == 2:
            badge_2 = l
            badges.append((badge_0, badge_1, badge_2))
        counter = (counter + 1) % 3
    result = [
        score_item(list(set.intersection(set(a), set(b), set(c)))[0])
        for a, b, c in badges
    ]
    return sum(result)
