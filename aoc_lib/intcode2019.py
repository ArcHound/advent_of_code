import logging

log = logging.getLogger("aoc_logger")


class Intcode2019:
    def __init__(self):
        self.ip = 0

    def parse_instruction(self, instruction: int):
        code = instruction % 100
        modes = [(instruction % pow(10, 3 + x)) // pow(10, 2 + x) for x in range(4)]
        return code, modes

    def process_program(self, data):
        self.ip = 0
        self.data = data.copy()
        done = False
        while not done:
            code, modes = self.parse_instruction(self.data[self.ip])
            if code == 99:
                return 0
            elif code == 1:
                self.data[self.data[self.ip + 3]] = (
                    self.data[self.data[self.ip + 1]]
                    + self.data[self.data[self.ip + 2]]
                )
                self.ip += 4
            elif code == 2:
                self.data[self.data[self.ip + 3]] = (
                    self.data[self.data[self.ip + 1]]
                    * self.data[self.data[self.ip + 2]]
                )
                self.ip += 4
            else:
                return -1  # error
