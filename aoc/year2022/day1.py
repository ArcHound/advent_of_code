def part2(in_data):
    out_list = list()
    counter = 0
    for n in in_data.splitlines():
        if n == "":
            out_list.append(counter)
            counter = 0
        else:
            counter += int(n)
    out_list.append(counter)
    return sum(sorted(out_list, reverse=True)[:3])


def part1(in_data):
    out_list = list()
    counter = 0
    for n in in_data.splitlines():
        if n == "":
            out_list.append(counter)
            counter = 0
        else:
            counter += int(n)
    out_list.append(counter)
    return sorted(out_list, reverse=True)[0]
