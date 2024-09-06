# 2023-20
from __future__ import annotations
import logging
from enum import Enum
from collections import defaultdict
import networkx as nx
import matplotlib.pyplot as plt
import math

log = logging.getLogger("aoc_logger")


# ternary logic
class Signal(Enum):
    NONE = 1
    LOW = 2
    HIGH = 3


class ElfModule:
    def __init__(
        self,
        signal_q: list[tuple[Signal, ElfModule, ElfModule]],
        totals: dict[Signal, int],
        connections: list[str],
        label: str,
        inventory: dict[str, ElfModule],
        **kwargs,
    ):
        self.totals = totals
        self.signal_q = signal_q
        self.connections = connections
        self.label = label
        self.inventory = inventory
        super().__init__(**kwargs)

    def __repr__(self):
        return f"{type(self).__name__}({self.label})"

    def get_id(self):
        return self.label

    def process_signal(self, signal: Signal, source: ElfModule) -> Signal:
        return signal

    def push_signal(self, signal: Signal, source: ElfModule):
        # log.debug(f"Pushing at {self.label}, {signal} from {source}")
        new_signal = self.process_signal(signal, source)
        for c in self.connections:
            # log.debug(f"Sending {new_signal} to {c}")
            if new_signal != Signal.NONE:
                self.totals[new_signal] += 1
                if c in self.inventory:
                    # log.debug(f"{c} is in inventory")
                    self.signal_q.append((new_signal, self, self.inventory[c]))


class OutputModule(ElfModule):
    def __init__(self, **kwargs):
        self.count = 0  # False off, True on
        super().__init__(**kwargs)

    def process_signal(self, signal: Signal, source: ElfModule) -> Signal:
        if signal == signal.LOW:
            self.count += 1
        return Signal.NONE


class BroadcastModule(ElfModule):
    pass


class FlipFlopModule(ElfModule):
    def __init__(self, **kwargs):
        self.state = False  # False off, True on
        super().__init__(**kwargs)

    def process_signal(self, signal: Signal, source: ElfModule) -> Signal:
        if signal == Signal.LOW:
            self.state = not self.state
            if self.state:
                return Signal.HIGH
            else:
                return Signal.LOW
        else:
            return Signal.NONE


class ConjunctionModule(ElfModule):
    def __init__(self, **kwargs):
        self.memory = dict()
        self.count = 0
        super().__init__(**kwargs)

    def connect(self, inputs: list[str]):
        self.memory = {c: Signal.LOW for c in inputs}

    def process_signal(self, signal: Signal, source: ElfModule) -> Signal:
        self.memory[source.get_id()] = signal
        if all([s == Signal.HIGH for k, s in self.memory.items()]):
            return Signal.LOW
        else:
            self.count += 1
            return Signal.HIGH


def module_factory(in_data):
    broadcaster = None
    signal_q = list()
    inventory = dict()
    totals = {Signal.HIGH: 0, Signal.LOW: 0}
    for line in in_data.splitlines():
        tlabel, conns = line.strip().split(" -> ")
        connections = conns.split(", ")
        if tlabel == "broadcaster":
            broadcaster = BroadcastModule(
                connections=connections,
                label=tlabel,
                signal_q=signal_q,
                inventory=inventory,
                totals=totals,
            )
            inventory[tlabel] = broadcaster
        elif tlabel[0] == "%":
            label = tlabel[1:]
            ff = FlipFlopModule(
                connections=connections,
                label=label,
                signal_q=signal_q,
                inventory=inventory,
                totals=totals,
            )
            inventory[label] = ff
        elif tlabel[0] == "&":
            label = tlabel[1:]
            con = ConjunctionModule(
                connections=connections,
                label=label,
                signal_q=signal_q,
                inventory=inventory,
                totals=totals,
            )
            inventory[label] = con
    for key, val in inventory.items():
        if type(val) == ConjunctionModule:
            inputs = [k for k in inventory if key in inventory[k].connections]
            val.connect(inputs)
    output = OutputModule(
        connections=list(),
        label="rx",
        signal_q=signal_q,
        inventory=inventory,
        totals=totals,
    )
    inventory["rx"] = output
    return broadcaster, signal_q, inventory, totals, output


def part1(in_data):
    broadcaster, signal_q, inventory, totals, output = module_factory(in_data)
    log.debug(inventory)
    for key, val in inventory.items():
        log.debug(key)
        log.debug(type(val))
        log.debug(val.connections)
        if type(val) == ConjunctionModule:
            log.debug(val.memory)
        log.debug("----------------------")
    pushes = 1000
    for push in range(pushes):
        signal_q.append((Signal.LOW, None, broadcaster))
        totals[Signal.LOW] += 1
        while len(signal_q) > 0:
            signal, source, target = signal_q.pop(0)
            target.push_signal(signal, source)
            # log.debug(signal_q)
            # log.debug('----------------------')
        # log.debug(totals)
        # log.debug('==========================')
    return totals[Signal.HIGH] * totals[Signal.LOW]


def part2(in_data):
    broadcaster, signal_q, inventory, totals, output = module_factory(in_data)
    log.debug(inventory)
    # we don't have the luxury of a general solution, we'll need to inspect our input
    graph = nx.DiGraph()
    colors = {
        BroadcastModule: "salmon",
        FlipFlopModule: "lightgreen",
        ConjunctionModule: "lightblue",
        OutputModule: "silver",
    }
    color_map = list()
    for k, v in inventory.items():
        graph.add_node(k)
        for c in v.connections:
            log.debug(f"{k} {c}")
            graph.add_edge(k, c)
    color_map = [colors[type(inventory[x])] for x in graph.nodes()]
    log.debug(graph.nodes())
    log.debug(graph.number_of_edges())
    log.debug(inventory.items())
    graph.add_nodes_from(
        [(k, {"color": colors[type(v)]}) for k, v in inventory.items()]
    )
    # I think this view is the best
    nx.draw_planar(graph, with_labels=True, node_color=color_map, node_size=700)
    plt.show()
    done = False
    count = 0
    # from the graph you can see that you need the stars to align on these four nodes
    # if each of those sends a single high signal, your output will have exactly one low signal
    # lcm those to find when they'll align
    nodes_to_check = ["ks", "pm", "dl", "vk"]
    minimums = list()
    while not done:
        signal_q.append((Signal.LOW, None, broadcaster))
        count += 1
        if len(nodes_to_check) == 0:
            break
        # reset signal counts for watched nodes in each wave
        for node in nodes_to_check:
            inventory[node].count = 0
        # propagate
        while len(signal_q) > 0:
            signal, source, target = signal_q.pop(0)
            target.push_signal(signal, source)
        # check
        for node in nodes_to_check:
            if inventory[node].count == 1:
                minimums.append(count)
                nodes_to_check.remove(node)  # if we're done, remove it
    return math.lcm(*minimums)
