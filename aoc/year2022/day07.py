# 2022-7
import logging

log = logging.getLogger("aoc_logger")


def cd(d, dirs, path):
    current_dir = dirs
    for c in path:
        current_dir = current_dir[c]
    if d == ".":
        return dirs, path
    elif d == "..":
        return dirs, path[:-1]
    elif d == "/":
        path = ["/"]
        if d not in current_dir:
            current_dir[d] = dict()
        return dirs, path
    else:
        if d not in current_dir:
            current_dir[d] = dict()
        path.append(d)
        return dirs, path


def add_file(fname, fsize, dirs, path):
    current_dir = dirs
    for c in path:
        current_dir = current_dir[c]
    current_dir[fname] = fsize
    return dirs, path


def add_dir(d, dirs, path):
    current_dir = dirs
    for c in path:
        current_dir = current_dir[c]
    if d not in current_dir:
        current_dir[d] = dict()
    return dirs


def dirstruct(in_data):
    dirs = dict()
    path = list()
    for line in in_data.splitlines():
        log.debug(line)
        if "$ cd" in line:
            log.debug("CMD cd")
            next_dir = line.split()[2]
            dirs, path = cd(next_dir, dirs, path)
        elif "$ ls" in line:
            log.debug("CMD ls")
            pass
        elif line.startswith("dir"):
            log.debug("STDOUT dir")
            d = line.split()[1]
            dirs = add_dir(d, dirs, path)
        elif line[0].isdigit():
            log.debug("STDOUT file")
            fsize = int(line.split()[0])
            fname = line.split()[1]
            add_file(fname, fsize, dirs, path)
        log.debug(path)
        log.debug(dirs)
    return dirs


def count_sizes(dirstruct, dircounts, path):
    log.debug(path)
    size = 0
    current_dir = dirstruct
    for c in path:
        current_dir = current_dir[c]
    for k in current_dir:
        if type(current_dir[k]) == int:
            size += current_dir[k]
        else:
            in_dir_size = count_sizes(dirstruct, dircounts, path + [k])
            dircounts.append((in_dir_size, path + [k]))
            size += in_dir_size
            log.debug(f"Append {in_dir_size}, {path + [k]}")
    log.debug(size)
    return size


def dirsizes(in_data, marker):
    directories = dirstruct(in_data)
    dircounts = list()
    total = count_sizes(directories, dircounts, ["/"])
    log.debug(dircounts)
    filtered = [x[0] for x in dircounts if x[0] < marker]
    filtered_dirs = [(x[0], x[1]) for x in dircounts if x[0] < marker]
    log.debug(filtered_dirs)
    return sum(filtered)


def dirdeletes(in_data, size_needed=30000000, system_size=70000000):
    directories = dirstruct(in_data)
    dircounts = list()
    total = count_sizes(directories, dircounts, ["/"])
    need_to_delete = -1 * (system_size - size_needed - total)
    log.info(need_to_delete)
    c = min([x[0] for x in dircounts if x[0] >= need_to_delete])
    return c


def part1(in_data):
    return dirsizes(in_data, 100000)


def part2(in_data):
    return dirdeletes(in_data)
