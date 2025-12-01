# 2022-11
import logging

log = logging.getLogger("aoc_logger")


# in the original run, I didn't bother with a parser
test_monkeys = [
    {
        "monkey_id": 0,
        "items": [79, 98],
        "operation": (lambda x: x * 19),
        "test_mod": 23,
        "monkey_true": 2,
        "monkey_false": 3,
    },
    {
        "monkey_id": 1,
        "items": [54, 65, 75, 74],
        "operation": (lambda x: x + 6),
        "test_mod": 19,
        "monkey_true": 2,
        "monkey_false": 0,
    },
    {
        "monkey_id": 2,
        "items": [79, 60, 97],
        "operation": (lambda x: x * x),
        "test_mod": 13,
        "monkey_true": 1,
        "monkey_false": 3,
    },
    {
        "monkey_id": 3,
        "items": [74],
        "operation": (lambda x: x + 3),
        "test_mod": 17,
        "monkey_true": 0,
        "monkey_false": 1,
    },
]

prod_monkeys = [
    {
        "monkey_id": 0,
        "items": [89, 73, 66, 57, 64, 80],
        "operation": (lambda x: x * 3),
        "test_mod": 13,
        "monkey_true": 6,
        "monkey_false": 2,
    },
    {
        "monkey_id": 1,
        "items": [83, 78, 81, 55, 81, 59, 69],
        "operation": (lambda x: x + 1),
        "test_mod": 3,
        "monkey_true": 7,
        "monkey_false": 4,
    },
    {
        "monkey_id": 2,
        "items": [76, 91, 58, 85],
        "operation": (lambda x: x * 13),
        "test_mod": 7,
        "monkey_true": 1,
        "monkey_false": 4,
    },
    {
        "monkey_id": 3,
        "items": [71, 72, 74, 76, 68],
        "operation": (lambda x: x * x),
        "test_mod": 2,
        "monkey_true": 6,
        "monkey_false": 0,
    },
    {
        "monkey_id": 4,
        "items": [98, 85, 84],
        "operation": (lambda x: x + 7),
        "test_mod": 19,
        "monkey_true": 5,
        "monkey_false": 7,
    },
    {
        "monkey_id": 5,
        "items": [78],
        "operation": (lambda x: x + 8),
        "test_mod": 5,
        "monkey_true": 3,
        "monkey_false": 0,
    },
    {
        "monkey_id": 6,
        "items": [86, 70, 60, 88, 88, 78, 74, 83],
        "operation": (lambda x: x + 4),
        "test_mod": 11,
        "monkey_true": 1,
        "monkey_false": 2,
    },
    {
        "monkey_id": 7,
        "items": [81, 58],
        "operation": (lambda x: x + 5),
        "test_mod": 17,
        "monkey_true": 3,
        "monkey_false": 5,
    },
]


# but now I did
def parse_data(in_data):
    c = 0
    monkeys = list()
    monkey_id = 0
    items = list()
    operation = None
    test_mod = 0
    monkey_true = 0
    monkey_false = 0
    for line in in_data.splitlines():
        if c == 0:
            monkey_id = int(line.split(" ")[1][:-1])
        elif c == 1:
            items = [int(x[1:]) for x in line.split(":")[1].split(",")]
        elif c == 2:
            # this was what I didn't want to deal with
            ops = line.split("=")[1].split(" ")
            log.debug(ops)
            if ops[3] == "old" and ops[2] == "*":
                operation = lambda x: x * x
            elif ops[3] == "old" and ops[2] == "+":
                operation = lambda x: x + x
            elif ops[2] == "*":
                operation = (
                    lambda x, bound_y=int(ops[3]): x * bound_y
                )  # critical to use this bounded variable - other approaches result in overwrites for some reason
            elif ops[2] == "+":
                operation = lambda x, bound_y=int(ops[3]): x + bound_y
            else:  # no way I am writing a full parser here
                log.critical(f"Unsupported operation: {line}")
                return None
            log.debug(operation(0))
            log.debug(operation(1))
        elif c == 3:
            test_mod = int(line.split(" ")[-1])
        elif c == 4:
            monkey_true = int(line.split(" ")[-1])
        elif c == 5:
            monkey_false = int(line.split(" ")[-1])
            monkeys.append(
                {
                    "monkey_id": monkey_id,
                    "items": items,
                    "operation": operation,
                    "test_mod": test_mod,
                    "monkey_true": monkey_true,
                    "monkey_false": monkey_false,
                }
            )
        c += 1
        c %= 7
    log.debug(monkeys)
    return monkeys


# idea - jungle consists of monkeys and items that see each other
class Jungle:
    def __init__(self):
        self.monkeys = dict()
        self.items = list()

    def add_monkey(self, monkey):
        self.monkeys[monkey.monkey_id] = monkey

    def get_monkey(self, monkey_id):
        return self.monkeys[monkey_id]

    def add_item(self, item):
        self.items.append(item)


class Item:
    def __init__(self, worry, monkey_id, reducing_worry):
        self.worry = worry
        self.monkey_id = monkey_id
        # two paths here - one with the reduction where we need absolute values, other with modulos
        self.reducing_worry = reducing_worry
        self.abs_val = worry

    def sub_to_jungle(self, jungle):
        jungle.add_item(self)
        self.jungle = jungle

    def add_views(self):
        log.debug(f"Adding views for {self.worry}")
        self.views = dict()
        for m in self.jungle.monkeys:
            # basically, you only need to remember the reminders for each monkey - these are small. Then you can do the operations without worry as the modulo arithmetic is closed on these (no division, etc)
            # rest of the code is wiring so that each item knows about the monkey and vice-versa
            self.views[m] = (
                self.worry % self.jungle.get_monkey(m).test_mod,
                self.jungle.get_monkey(m).test_mod,
            )

    def get_val(self, monkey_id):
        if self.reducing_worry:
            return self.abs_val
        else:
            return self.views[monkey_id][0]

    def update_val(self, operation):
        for m in self.views:
            self.views[m] = (
                operation(self.views[m][0]) % self.views[m][1],
                self.views[m][1],
            )
        # if we're reducing worry, we track the absolute value (also, we're reducing worry)
        if self.reducing_worry:
            self.abs_val = operation(self.abs_val) // 3

    def view_item(self):
        return ", ".join([f"{self.views[m]}" for m in self.views])


class Monkey:
    def __init__(
        self,
        monkey_id,
        items,
        operation,
        test_mod,
        monkey_true,
        monkey_false,
        reducing_worry,
    ):
        self.monkey_id = monkey_id
        self.items = [Item(item, monkey_id, reducing_worry) for item in items]
        self.operation = operation
        self.test_mod = test_mod
        self.monkey_true = monkey_true
        self.monkey_false = monkey_false
        self.inspection_counter = 0

    # def operation(self, item):
    #     # return self.operation(item)
    #     item.update_val(self.operation)

    def test(self, item):
        # return item % self.test_mod == 0
        return item.get_val(self.monkey_id) % self.test_mod == 0

    def sub_to_jungle(self, jungle):
        jungle.add_monkey(self)
        for item in self.items:
            item.sub_to_jungle(jungle)
        self.jungle = jungle

    def receive_item(self, item):
        self.items.append(item)

    def process_item(self, item):
        self.inspection_counter += 1
        # self.items.remove(item)
        # log.debug(item.view_item())
        # log.debug(f"  Monkey inspects an item with a worry level of {item.get_val(self.monkey_id)}.")
        item.update_val(self.operation)
        # log.debug(item.view_item())
        # log.debug(f"    Worry level has risen to {item.get_val(self.monkey_id)}.")
        # if reducing_worry:
        #     new_worry = new_worry // 3
        # log.debug(
        #     f"    Monkey gets bored with item. Worry level is divided by 3 to {new_worry}."
        # )
        if self.test(item):
            # log.debug(f"    Current worry level is divisible by {self.test_mod}.")
            self.jungle.get_monkey(self.monkey_true).receive_item(item)
            # log.debug(
            #     f"    Item with worry level {new_worry} is thrown to monkey {self.monkey_true}."
            # )
        else:
            # log.debug(
            #     f"    Current worry level is not divisible by {self.test_mod}"
            # )
            self.jungle.get_monkey(self.monkey_false).receive_item(item)
            # log.info(
            #     f"    Item with worry level {item.get_val(self.monkey_id)} is thrown to monkey {self.monkey_false}."
            # )

    def round(self):
        # log.debug(f"Monkey {self.monkey_id}")
        for item in self.items:
            self.process_item(item)
        self.items = list()

    def get_count(self):
        return self.inspection_counter


def monkey_business(rounds, monkeys, reduce_worry=False):
    jungle = Jungle()
    for m in monkeys:
        # since monkeys are holding the items, items are constructed within monkeys (kinda ugly, I know)
        new_m = Monkey(
            m["monkey_id"],
            m["items"],
            m["operation"],
            m["test_mod"],
            m["monkey_true"],
            m["monkey_false"],
            reduce_worry,
        )
        new_m.sub_to_jungle(jungle)
    # now that we have items, we need to calculate other moduli
    for i in jungle.items:
        i.add_views()
    # rounds loop
    for i in range(rounds):
        for m in jungle.monkeys:
            jungle.get_monkey(m).round()
        # debug and tracking purposes only, can be omitted
        if (i + 1) % 1000 == 0:
            # log.info(f"After round {i}, the monkeys are holding items with these worry levels:")
            log.info(f"== After round {i + 1} ==")
            for m in jungle.monkeys:
                log.info(
                    f"Monkey {m} inspected items {jungle.get_monkey(m).get_count()} times."
                )
    # get the top two monkeys
    counts = sorted(
        [jungle.get_monkey(m).get_count() for m in jungle.monkeys], reverse=True
    )
    return counts[0] * counts[1]


def part1(in_data):
    monkeys = parse_data(in_data)
    return monkey_business(20, monkeys, True)


def part2(in_data):
    monkeys = parse_data(in_data)
    return monkey_business(10000, monkeys)
