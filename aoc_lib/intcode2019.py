import logging
import dataclasses
from enum import Enum
from typing import Callable
from collections import deque

log = logging.getLogger("aoc_logger")


@dataclasses.dataclass
class Parameter:
    value: int
    mode: int

    def point(self, data):
        if self.mode == 0:
            return data[self.value]
        elif self.mode == 1:
            return self.value
        else:
            raise ValueError(f"Unknown mode {self.mode}")


class Signal(Enum):
    OK = 0
    ERROR = 1
    HALT = 2


@dataclasses.dataclass
class OP_out:
    signal: Signal
    value: int
    address: int
    stdout: int


@dataclasses.dataclass
class OP_item:
    params: int
    function: Callable
    code: int


class Intcode2019:
    def __init__(self):
        self.ip = 0
        self.op_map = {
            1: OP_item(code=1, params=3, function=self.op_1),
            2: OP_item(code=2, params=3, function=self.op_2),
            3: OP_item(code=3, params=1, function=self.op_3),
            4: OP_item(code=4, params=1, function=self.op_4),
            5: OP_item(code=5, params=2, function=self.op_5),
            6: OP_item(code=6, params=2, function=self.op_6),
            7: OP_item(code=7, params=3, function=self.op_7),
            8: OP_item(code=8, params=3, function=self.op_8),
            99: OP_item(code=99, params=0, function=self.op_99),
        }
        self.stdout = list()

    def parse_instruction(self, instruction: int):
        log.debug("--------------------")
        log.debug(instruction)
        code = instruction % 100
        log.debug(code)
        op = self.op_map.get(code, None)
        if not op:
            raise NotImplementedError(f"Unknown opcode {code}")
        modes = [
            (instruction % pow(10, 3 + x)) // pow(10, 2 + x) for x in range(op.params)
        ]
        return op, modes

    def prepare_params(self, modes):
        params = list()
        i = 0
        for m in modes:
            params.append(Parameter(mode=m, value=self.data[self.ip + i]))
            i += 1
        return params

    def process_program(self, data, stdin=list()):
        self.ip = 0
        self.stdin = deque(stdin)
        self.data = data.copy()
        done = False
        while not done:
            log.debug("---------")
            log.debug(self.ip)
            log.debug(self.data)
            log.debug(self.data[self.ip])
            op, modes = self.parse_instruction(self.data[self.ip])
            log.debug(op)
            log.debug(modes)
            self.ip += 1
            params = self.prepare_params(modes)
            log.debug(params)
            r = op.function(*params)
            log.debug(r)
            if r.signal == Signal.HALT:
                return 0
            elif r.signal == Signal.ERROR:
                raise ValueError(f"opcode {op.code} raised error with params {params}")
            elif r.signal == Signal.OK:
                log.debug("OK")
                log.debug(r)
                if (r.value is not None) and (r.address is not None):
                    self.data[r.address] = r.value
                if r.stdout is not None:
                    self.stdout.append(r.stdout)
            log.debug("---------")

    # Add
    def op_1(self, a: Parameter, b: Parameter, c: Parameter) -> OP_out:
        self.ip += 3
        return OP_out(
            signal=Signal.OK,
            value=a.point(self.data) + b.point(self.data),
            address=c.value,
            stdout=None,
        )

    # Multiply
    def op_2(self, a: Parameter, b: Parameter, c: Parameter) -> OP_out:
        self.ip += 3
        return OP_out(
            signal=Signal.OK,
            value=a.point(self.data) * b.point(self.data),
            address=c.value,
            stdout=None,
        )

    # Read
    def op_3(self, a: Parameter) -> OP_out:
        self.ip += 1
        val = self.stdin.popleft()
        return OP_out(signal=Signal.OK, value=val, address=a.value, stdout=None)

    # Write
    def op_4(self, a: Parameter) -> OP_out:
        self.ip += 1
        return OP_out(
            signal=Signal.OK, value=None, address=None, stdout=a.point(self.data)
        )

    # Jump if True
    def op_5(self, a: Parameter, b: Parameter) -> OP_out:
        self.ip += 2
        if a.point(self.data) != 0:
            self.ip = b.point(self.data)
        return OP_out(signal=Signal.OK, value=None, address=None, stdout=None)

    # Jump if False
    def op_6(self, a: Parameter, b: Parameter) -> OP_out:
        self.ip += 2
        if a.point(self.data) == 0:
            self.ip = b.point(self.data)
        return OP_out(signal=Signal.OK, value=None, address=None, stdout=None)

    # Less than
    def op_7(self, a: Parameter, b: Parameter, c: Parameter) -> OP_out:
        self.ip += 3
        if a.point(self.data) < b.point(self.data):
            return OP_out(signal=Signal.OK, value=1, address=c.value, stdout=None)
        else:
            return OP_out(signal=Signal.OK, value=0, address=c.value, stdout=None)

    # Equals
    def op_8(self, a: Parameter, b: Parameter, c: Parameter) -> OP_out:
        self.ip += 3
        if a.point(self.data) == b.point(self.data):
            return OP_out(signal=Signal.OK, value=1, address=c.value, stdout=None)
        else:
            return OP_out(signal=Signal.OK, value=0, address=c.value, stdout=None)

    # Halt
    def op_99(self) -> OP_out:
        return OP_out(signal=Signal.HALT, value=None, address=None, stdout=None)
