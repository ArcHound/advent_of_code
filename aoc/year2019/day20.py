# 2019-20
import logging
from aoc_lib.map2d import Map2d
from collections import defaultdict
import networkx as nx
import matplotlib.pyplot as plt

log = logging.getLogger("aoc_logger")


def parse_data(in_data):
    data = list()
    for line in in_data.splitlines():
        data.append(line)
    first_line_space = 2
    found = False
    line_len = len(data[0])
    while not found:
        log.debug(first_line_space)
        line_check = data[first_line_space]
        log.debug(line_check)
        for j in range(2, len(line_check) - 2):
            if line_check[j] not in "#.":
                found = True
                break
        if found:
            break
        first_line_space += 1
        log.debug("----")
    found = False
    first_line_full_again = first_line_space
    while not found:
        first_line_full_again += 1
        found = True
        line_check = data[first_line_full_again]
        for j in range(2, len(line_check) - 2):
            if line_check[j] not in "#.":
                found = False
    # bounds
    log.debug(first_line_space)
    log.debug(first_line_full_again)
    portal_lines = {
        0: (0, 1),
        first_line_space - 3: (first_line_space, first_line_space + 1),
        first_line_full_again
        - 2: (first_line_full_again - 2, first_line_full_again - 1),
        len(data) - 5: (len(data) - 2, len(data) - 1),
    }

    found = False
    col_len = len(data)
    first_col_space = 2
    while not found:
        log.debug(first_col_space)
        line_check = "".join([x[first_col_space] for x in data])
        log.debug(line_check)
        for j in range(2, len(line_check) - 2):
            if line_check[j] not in "#.":
                found = True
                break
        if found:
            break
        first_col_space += 1
        log.debug("----")
    found = False
    first_col_full_again = first_col_space
    while not found:
        first_col_full_again += 1
        found = True
        line_check = "".join([x[first_col_full_again] for x in data])
        for j in range(2, len(line_check) - 2):
            if line_check[j] not in "#.":
                found = False
    # bounds
    log.debug(first_col_space)
    log.debug(first_col_full_again)
    portal_columns = {
        0: (0, 1),
        first_col_space - 3: (first_col_space, first_col_space + 1),
        first_col_full_again - 2: (first_col_full_again - 2, first_col_full_again - 1),
        len(data[0]) - 5: (len(data[0]) - 2, len(data[0]) - 1),
    }
    log.debug(portal_columns)
    portals = defaultdict(list)
    for line in portal_lines:
        # log.debug(line)
        for i in range(line_len):
            # line portals
            # log.debug(line_len)
            # log.debug(i)
            # log.debug(data[portal_lines[line][0]])
            if (
                data[portal_lines[line][0]][i] not in " #."
                and data[portal_lines[line][1]][i] not in " #."
            ):
                portals[
                    data[portal_lines[line][0]][i] + data[portal_lines[line][1]][i]
                ].append((i - 2, line))
                # log.debug(data[portal_lines[line][0]][i]+data[portal_lines[line][1]][i])
                # log.debug((i-2, line))
    for line in portal_columns:
        for i in range(len(data)):
            if (
                data[i][portal_columns[line][0]] not in " #."
                and data[i][portal_columns[line][1]] not in " #."
            ):
                portals[
                    data[i][portal_columns[line][0]] + data[i][portal_columns[line][1]]
                ].append((line, i - 2))
                # log.debug(data[i][portal_lines[line][0]]+data[i][portal_lines[line][1]])
                # log.debug((line, i-2))

            # log.debug('----')
            # column portals
    log.debug(portals)
    map_lines = "\n".join([x[2:-2] for x in data[2:-2]])
    map2d = Map2d.from_lines(map_lines)
    # log.debug(map2d.debug_draw())
    for i in range(len(map2d.obstacle_str)):
        if map2d.obstacle_str[i] not in "#.":
            map2d.set_index(i, Map2d.obstacle_sym)
    log.debug(map2d.debug_draw())
    return map2d, portals


def part1(in_data, test=False):
    map2d, portals = parse_data(in_data)
    pure_portals = {
        portals[x][0]: [portals[x][1]] for x in portals if len(portals[x]) == 2
    } | {portals[x][1]: [portals[x][0]] for x in portals if len(portals[x]) == 2}
    log.debug(pure_portals)
    map2d.set_portals_points(pure_portals)
    log.debug(map2d.bounds)
    start_point = portals["AA"][0]
    end_point = portals["ZZ"][0]
    map2d.flood(start_point)
    return map2d.get_flooded_val(end_point)


def part2(in_data, test=False):
    map2d, portals = parse_data(in_data)
    start_point = portals["AA"][0]
    end_point = portals["ZZ"][0]
    pure_portals = {
        portals[x][0]: portals[x][1] for x in portals if len(portals[x]) == 2
    } | {portals[x][1]: portals[x][0] for x in portals if len(portals[x]) == 2}
    uniq_portals = [y for x in portals for y in portals[x]]
    rev_portals = {x: [k for k in portals if x in portals[k]][0] for x in uniq_portals}
    log.debug(uniq_portals)
    log.debug(pure_portals)
    log.debug(portals)
    max_depth = len(portals) - 1  # this is a wild guess
    # give me distances between portals - I'll create a graph
    edges = list()
    for p in uniq_portals:
        map2d.flood(p)
        for q in uniq_portals:
            q_len = map2d.get_flooded_val(q)
            if q_len > 0:
                edges.append((p, q, map2d.get_flooded_val(q)))
        map2d.clear_flood()
    log.debug(start_point)
    log.debug(edges)
    G = nx.Graph()
    for i in range(max_depth):
        for p in uniq_portals:
            if (p == start_point or p == end_point) and i != 0:
                continue
            for q, val in [(q, val) for (x, q, val) in edges if x == p]:
                G.add_edge((p, i), (q, i), weight=val)
            if (
                p in pure_portals
                and p[0] != 0
                and p[1] != 0
                and p[0] != map2d.bounds[1][0] - 1
                and p[1] != map2d.bounds[1][1] - 1
            ):  # we want inner portal
                # log.debug(p)
                # log.debug(rev_portals[p])
                # log.debug(pure_portals[p])
                # log.debug('--------')
                G.add_edge((p, i), (pure_portals[p], i + 1), weight=1)
    log.debug(map2d.bounds)
    # pos = nx.spring_layout(G, seed=42)
    # nx.draw_networkx_nodes(G, pos, node_size=700)
    # nx.draw_networkx_edges(G, pos, width=4)
    # nx.draw_networkx_labels(G, pos)
    # edge_labels = nx.get_edge_attributes(G, "weight")
    # nx.draw_networkx_edge_labels(G, pos, edge_labels)
    # plt.show()

    # p = nx.shortest_path(G, source=(start_point,0), target=(end_point,0), weight="weight")
    # translated_p = [(rev_portals[a],i) for (a,i) in p]
    # log.debug(translated_p)
    p = nx.shortest_path_length(
        G, source=(start_point, 0), target=(end_point, 0), weight="weight"
    )
    return p
