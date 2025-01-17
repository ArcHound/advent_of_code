# 2022-17

import logging
from tqdm import tqdm

log = logging.getLogger("aoc_logger")

# we bit map this one
# rocks start falling so that the edge is in third place, index 2
# the bottom of the shape is at index 0

shapes = [
    (0b11110,),
    (0b1000, 0b11100, 0b1000),
    (0b11100, 0b100, 0b100),
    (0b10000, 0b10000, 0b10000, 0b10000),
    (0b11000, 0b11000),
]


def shift_shape(shape, inst):
    new_shape = shape
    if inst == "<" and max(shape) < 0b111111:
        new_shape = tuple(x << 1 for x in shape)
    elif inst == ">" and all(x % 2 == 0 for x in shape):
        new_shape = tuple(x >> 1 for x in shape)
    return new_shape


def is_collision(stack, stack_offset, shape, shape_h):
    result = False
    for i in range(len(shape)):
        if i + shape_h - stack_offset >= len(stack):
            continue
        if shape[i] & stack[i + shape_h - stack_offset] > 0:
            result = True
            break
    return result


def apply_shape(stack, stack_offset, shape, shape_h):
    while len(shape) + shape_h - stack_offset > len(stack) - 1:
        stack.append(0)
    for i in range(len(shape)):
        stack[i + shape_h - stack_offset] = stack[i + shape_h - stack_offset] | shape[i]


def calc_stack_max(stack):
    stack_max = -1
    for j in range(len(stack)):
        if stack[j] != 0:
            stack_max = j
    return stack_max


def debug_stack(stack, stack_offset):
    return "\n" + "\n".join(
        [
            bin(stack[len(stack) - i - 1])[2:]
            .zfill(7)
            .replace("0", ".")
            .replace("1", "#")
            for i in range(len(stack))
        ]
    )


def part1(in_data, test=False):
    vectors = in_data.strip()  # there's no parsing
    loop_len_vector = len(vectors)
    loop_len_shape = len(shapes)
    p_vector = 0
    p_shape = 0
    stack_offset = 0
    stack = [0b1111111]
    profile = [0, 0, 0, 0, 0, 0, 0]
    for i in range(2022):
        active_shape = shapes[p_shape]
        p_shape = (p_shape + 1) % loop_len_shape
        moving = True
        stack_max = calc_stack_max(stack)
        shape_h = stack_offset + stack_max + 4
        while moving:
            try_shape = shift_shape(active_shape, vectors[p_vector])
            p_vector = (p_vector + 1) % loop_len_vector
            if is_collision(stack, stack_offset, try_shape, shape_h):
                try_shape = active_shape
            if is_collision(stack, stack_offset, try_shape, shape_h - 1):
                moving = False
                apply_shape(stack, stack_offset, try_shape, shape_h)
            else:
                shape_h -= 1
                active_shape = try_shape
        old_profile = tuple(profile)
        for pos in range(7):
            for j in range(len(stack)):
                if stack[len(stack) - j - 1] & (1 << pos) > 0:
                    profile[pos] = len(stack) - j - 1
                    break
        new_profile = tuple(profile)
        shifted = min(new_profile)
        if min(old_profile) < shifted:
            stack_offset += shifted
            stack = stack[shifted:]
            for j in range(len(profile)):
                profile[j] -= shifted
            new_profile = tuple(profile)
        # log.debug(debug_stack(stack, stack_offset))
        # log.debug('--------------')
    log.debug(stack_offset)
    return stack_offset + calc_stack_max(stack)


def part2(in_data, test=False):
    vectors = in_data.strip()  # there's no parsing
    loop_len_vector = len(vectors)
    loop_len_shape = len(shapes)
    p_vector = 0
    p_shape = 0
    stack_offset = 0
    stack = [0b1111111]
    profile = [0, 0, 0, 0, 0, 0, 0]
    profile_cache = dict()
    result = 0
    how_many = 1000000000000
    for i in range(how_many):
        active_shape = shapes[p_shape]
        p_shape = (p_shape + 1) % loop_len_shape
        moving = True
        stack_max = calc_stack_max(stack)
        shape_h = stack_offset + stack_max + 4
        while moving:
            try_shape = shift_shape(active_shape, vectors[p_vector])
            p_vector = (p_vector + 1) % loop_len_vector
            if is_collision(stack, stack_offset, try_shape, shape_h):
                try_shape = active_shape
            if is_collision(stack, stack_offset, try_shape, shape_h - 1):
                moving = False
                apply_shape(stack, stack_offset, try_shape, shape_h)
            else:
                shape_h -= 1
                active_shape = try_shape
        old_profile = tuple(profile)
        for pos in range(7):
            for j in range(len(stack)):
                if stack[len(stack) - j - 1] & (1 << pos) > 0:
                    profile[pos] = len(stack) - j - 1
                    break
        new_profile = tuple(profile)
        shifted = min(new_profile)
        if min(old_profile) < shifted:
            stack_offset += shifted
            stack = stack[shifted:]
            for j in range(len(profile)):
                profile[j] -= shifted
            new_profile = tuple(profile)
        total_profile = (p_shape, p_vector, new_profile)
        if (p_shape, p_vector) not in profile_cache:
            profile_cache[(p_shape, p_vector)] = {
                new_profile: (i, stack_offset + calc_stack_max(stack))
            }
        elif new_profile in profile_cache[(p_shape, p_vector)]:
            first_i, first_len = profile_cache[(p_shape, p_vector)][new_profile]
            s_len = stack_offset + calc_stack_max(stack)
            cycles = (how_many - first_i) // (i - first_i)
            leftover = how_many - cycles * (i - first_i)
            leftover_h = [
                profile_cache[x][y][1]
                for x in profile_cache
                for y in profile_cache[x]
                if profile_cache[x][y][0] == leftover
            ][0]
            last_diff = leftover_h - first_len
            # log.error(f"cycles {cycles}")
            # log.error(f"leftover {leftover}")
            # log.error(f"leftover h {leftover_h}")
            # log.error(f"i {i}")
            # log.error(f"first i {first_i}")
            # log.error(f"s_len {s_len}")
            # log.error(f"first_len {first_len}")
            result = cycles * (s_len - first_len) + first_len + last_diff - 1
            break
        else:
            profile_cache[(p_shape, p_vector)][new_profile] = (
                i,
                stack_offset + calc_stack_max(stack),
            )
    return result
