# 2023-21
import logging
from aoc_lib.map2d import Map2d

log = logging.getLogger("aoc_logger")


def part1(in_data, test=False):
    STEPS = 6
    if not test:
        STEPS = 64  # for prod use-case
    map2d = Map2d.from_lines(in_data)
    log.debug(map2d)
    start = None
    for i in range(len(map2d.obstacle_str)):
        if map2d.obstacle_str[i] == "S":
            start = map2d.translate_index(i)
    log.debug(start)
    return len(map2d.iterative_flood_indexes(start, STEPS))


def part2(in_data):
    # ok.
    # First thing to note is that the map is 131*131 and the start is at (65,65)
    # Second thing to note, that the number of steps is == 65 (mod 131)
    STEPS = 26501365
    steps_div = STEPS // 131
    # Then you realize that the relationship between the number of steps and the covered tiles is quadratic-ish (it's an expanding diamond)
    # proving that it's actually quadratic takes some more time - intuitive reasoning backed by experiment below (yes, not a proof)
    #
    # the maps obviously create a grid as the patterns repeat
    # due to the step numbers we first expand to touch the grid border (65) and then we traverse the full grid
    # this is made possible by the fact, that the row and column with start has no obstacles
    #
    # the maps also have a property that after 128 steps the number of reachable steps alternates
    # this means that there are only several possible tiles in our configuration as long as the number of steps is offset by 65 and then a multiple of 131
    # we have inner even tiles (iet), inner odd tiles (iot), and a set of edge tiles depending on where we entered the map
    #
    # using induction -> obvious for a single tile (duh), simple for 3x3 too -> one inner tile, bottom edge tile, left edge tile, right edge tile and top edge tile
    # from n -> n+1
    #  - we gain one "diagonal" edge tile for each diagonal
    #  - we still have bottom edge tile, left edge tile, right edge tile and top edge tile WITH THE SAME COVERAGE
    #  - in the inner tiles, the parity of tiles flips. However, we gain 4*n inner tiles -> this is our biggest term
    #    - we're actually always gaining new iet tiles (induction again, go reader!)
    #    - to count all of the inner tiles, we can use the Gauss formula multiplied by four
    #    - we need to split that count into total number of even tiles and total number of odd tiles
    #    - to get the total number of even tiles, divide the n by 2 (=n_half), count the numbers up to n_half (Gauss again) and multiply by two -> you'll get n_half*(n_half+1)
    #    - then we need to multiply that by 4 because directions -> n*(n+2)
    #    - to get the odd numbers, subtract n_half from the even numbers (send 2 -> 1, 4 -> 3 etc) and multiply by 4 - formula is n*n
    #    - those are the general formulas
    #    - don't forget to subtract one for the outer layer in both cases
    #    - (man, this proof is looking more rigid, but more messy)
    #    - say that n+1 is odd, without loss of generality
    #    - yes, there is more formal work for the opposite case (add n_half), but trust me bro
    #    - old iet tiles -> n*n  (see above)
    #    - old iot tiles are now iet tiles -> there were n*(n-2) of them (see above)
    #    - flipping iet to iot yields n*n tiles
    #    - flipping iot to iet and adding 4n tiles yields n*n -2n + 4n = n*(n+2)
    #    - so this is a nice quadratic relation
    #  - I'll say it, QED
    #
    # Since it seems to be a polynomial, we can try interpolating it using the Lagrange formula
    # we need to have points in the form of 65+k*131 though so that we stay on the grid
    # to do that, we need to extend our map to at least a 5x5 grid so we can take a look at 65, 131+65 and 2*131+65
    # Here goes:
    big_map = list()
    for line in in_data.splitlines():
        big_line = line.strip() * 5
        big_map.append(big_line)
    big_map = big_map * 5
    big_map = "\n".join(big_map)
    map2d = Map2d.from_lines(big_map)
    # we have the big map
    start = (2 * 131 + 65, 2 * 131 + 65)  # start of the big map is shifted by two tiles
    # calculate references
    point_0 = len(map2d.iterative_flood_indexes(start, 65))
    point_1 = len(map2d.iterative_flood_indexes(start, 131 + 65))
    point_2 = len(map2d.iterative_flood_indexes(start, 131 * 2 + 65))
    # if there really is y = ax^2 + bx + c satisfying this relationship, we can find it:
    # x = 0 -> steps = 0*131 + 65
    # point0 = c
    # x = 1 -> steps = 1*131 + 65
    # point1 = a + b + c
    # x = 2 -> steps = 2*131 + 65
    # point2 = 4a + 2b +c
    # three linear equations with three non-zero right-sides -> solve
    c = point_0
    b = (4 * point_1 - 3 * point_0 - point_2) // 2
    a = (point_2 + point_0 - 2 * point_1) // 2
    # since we are traversing the "big grid" our new number of steps is (STEPS-65)/131
    # and it works
    return a * steps_div * steps_div + b * steps_div + c
