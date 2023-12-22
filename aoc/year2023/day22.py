# 2023-22
import logging
from aoc_lib.vector3d import Point3d, v_add
from aoc_lib.interval import Interval
from tqdm import tqdm


log = logging.getLogger("aoc_logger")


def parse_data(in_data):
    bricks = list()
    bounds = (Point3d(0, 0, 0), Point3d(0, 0, 0))
    for line in in_data.splitlines():
        brick1, brick2 = (
            [int(x) for x in line.strip().split("~")[0].split(",")],
            [int(y) for y in line.strip().split("~")[1].split(",")],
        )
        brick = (
            Point3d(brick1[0], brick1[1], brick1[2]),
            Point3d(brick2[0], brick2[1], brick2[2]),
        )
        # probably not required, but I like having the bounds of the objects
        if bounds[0].x >= brick[0].x:
            bounds[0].x = brick[0].x
        if bounds[0].y >= brick[0].y:
            bounds[0].y = brick[0].y
        if bounds[0].z >= brick[0].z:
            bounds[0].z = brick[0].z
        if bounds[1].x < brick[1].x + 1:
            bounds[1].x = brick[1].x + 1  # half-open intervals
        if bounds[1].y < brick[1].y + 1:
            bounds[1].y = brick[1].y + 1  # half-open intervals
        if bounds[1].z < brick[1].z + 1:
            bounds[1].z = brick[1].z + 1  # half-open intervals
        bricks.append(brick)
    return bricks, bounds


def move_brick(brick, vector):
    # keeping it simple
    return (v_add(brick[0], vector), v_add(brick[1], vector))


def collision(brick, fixed_bricks):
    # idea - check the lowest brick level and then compare rectangles as two intervals
    brick_floor = (
        Interval(brick[0].x, brick[1].x + 1),
        Interval(brick[0].y, brick[1].y + 1),
    )
    brick_level = brick[0].z
    # log.debug("Collision?")
    # log.debug(f"Inbrick floor {brick_floor}")
    # log.debug(f"Inbrick level {brick_level}")
    # log.debug(fixed_bricks)
    for fbrick in fixed_bricks:
        # log.debug(f"Fbrick {fbrick}")
        if fbrick[0].z <= brick_level and brick_level <= fbrick[1].z:
            fbrick_floor = (
                Interval(fbrick[0].x, fbrick[1].x + 1),
                Interval(fbrick[0].y, fbrick[1].y + 1),
            )
            # log.debug(f"Fbrick floor {fbrick_floor}")
            if Interval.overlap(brick_floor[0], fbrick_floor[0]) and Interval.overlap(
                brick_floor[1], fbrick_floor[1]
            ):
                # log.debug("collision!")
                return True
            # log.debug("nope")

    return False


def gravity(bricks, bounds, motion_detect_only=False):
    vector = Point3d(0, 0, -1)
    min_vector = Point3d(0, 0, 1)
    floor_z = bounds[0].z
    sorted_bricks = sorted(
        bricks, key=lambda x: x[0].z
    )  # starting from the lowest bricks, this is enough as those shapes are simple
    fixed_bricks = list()
    all_motion = False
    moved_bricks = 0
    # general idea - evaluate the next step - if it collides with either floor or one of the fixed bricks, it's a collision and we need to move a step back
    for brick in sorted_bricks:
        motion = True
        moving_brick = (brick[0].copy(), brick[1].copy())
        moved_that_brick = False
        log.debug(f"Processing {moving_brick}")
        tolerance = 0
        while motion:
            if collision(moving_brick, fixed_bricks):
                log.debug("Collision")
                fixed_bricks.append(
                    move_brick(moving_brick, min_vector)
                )  # step back from the collision
                motion = False
            elif floor_z - 1 == moving_brick[0].z:  # hit the floor
                log.debug("Floor")
                fixed_bricks.append(move_brick(moving_brick, min_vector))
                motion = False

            else:
                moving_brick = move_brick(moving_brick, vector)
                if tolerance >= 1:  # first movement for checking
                    all_motion = True
                    if (
                        not moved_that_brick
                    ):  # also record how many bricks moved for part2
                        moved_that_brick = True
                        moved_bricks += 1
                    if motion_detect_only:
                        return list(), all_motion, moved_bricks
                tolerance += 1
        log.debug(fixed_bricks)
        log.debug("-------------------------")
    return fixed_bricks, all_motion, moved_bricks


def part1(in_data):
    bricks, bounds = parse_data(in_data)
    # simple - load bricks, let them fall
    log.debug(bricks)
    log.debug(bounds)
    log.debug("First gravity round")
    down_bricks, all_motion, _ = gravity(bricks, bounds)
    log.debug("=====================")
    count = 0
    # then erase a brick and let them fall again
    for brick in tqdm(down_bricks):
        log.debug(f"Gravity when {brick} is erased")
        new_bricks = [b for b in down_bricks if b != brick]  # erase
        new_down_bricks, all_motion, _ = gravity(
            new_bricks, bounds, motion_detect_only=True
        )
        if not all_motion:
            log.debug("No motion")
            count += 1
    return count


def part2(in_data):
    bricks, bounds = parse_data(in_data)
    down_bricks, all_motion, _ = gravity(bricks, bounds)
    count = 0
    # same as part 1
    for brick in tqdm(down_bricks):
        log.debug(f"Gravity when {brick} is erased")
        new_bricks = [b for b in down_bricks if b != brick]  # erase
        new_down_bricks, all_motion, moved_bricks = gravity(new_bricks, bounds)
        count += moved_bricks  # count how many bricks moved
    return count
