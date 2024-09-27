from __future__ import annotations

import logging
import dataclasses
from enum import Enum
from typing import Callable, Iterable
from collections import deque, defaultdict
from threading import Thread, Semaphore, Event

log = logging.getLogger("aoc_logger")


@dataclasses.dataclass
class Parameter:
    value: int
    mode: int
    computer: Intcode2019

    def point_interpreted(self):
        if self.mode == 0:
            return self.computer.data[self.value]
        elif self.mode == 1:
            return self.value
        elif self.mode == 2:
            return self.computer.data[self.value + self.computer.relative_base]
        else:
            raise ValueError(f"Unknown mode {self.mode}")

    def point_literal(self):
        if self.mode == 0 or self.mode == 1:
            return self.value
        elif self.mode == 2:
            return self.value + self.computer.relative_base
        else:
            raise ValueError(f"Unknown mode {self.mode}")


class Signal(Enum):
    OK = 0
    ERROR = 1
    HALT = 2
    INPUT_WAIT = 3


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
            9: OP_item(code=9, params=1, function=self.op_9),
            99: OP_item(code=99, params=0, function=self.op_99),
        }
        self.stdout = deque()
        self.stdin = deque()
        self.stdin_semaphore = Semaphore(value=0)
        self.stdout_semaphore = Semaphore(value=0)
        self.send_stdout_to = None
        self.relative_base = 0
        self.timeout = 10

    def parse_instruction(self, instruction: int):
        # log.debug("--------------------")
        # log.debug(instruction)
        code = instruction % 100
        # log.debug(code)
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
            params.append(
                Parameter(mode=m, value=self.data[self.ip + i], computer=self)
            )
            i += 1
        return params

    def cpu(self, finish_event):
        while True:
            # log.debug("---------")
            # log.debug(self.ip)
            # log.debug(self.data)
            # log.debug(self.data[self.ip])
            if finish_event and finish_event.is_set():
                return 0
            op, modes = self.parse_instruction(self.data[self.ip])
            # log.debug(op)
            # log.debug(modes)
            self.ip += 1
            params = self.prepare_params(modes)
            # log.debug(params)
            r = op.function(*params)
            # log.debug(r)
            if r.signal == Signal.HALT:
                if self.current_process_finish_event:
                    self.current_process_finish_event.set()
                return 0
            elif r.signal == Signal.ERROR:
                raise ValueError(f"opcode {op.code} raised error with params {params}")
            elif r.signal == Signal.OK:
                # log.debug("OK")
                # log.debug(r)
                if (r.value is not None) and (r.address is not None):
                    self.data[r.address] = r.value
                if r.stdout is not None:
                    self.stdout_semaphore.release()
                    self.set_output(r.stdout)
            elif r.signal == Signal.INPUT_WAIT:
                s = self.stdin_semaphore.acquire(blocking=True, timeout=self.timeout)
                if (
                    not s
                    and self.current_process_finish_event
                    and not self.current_process_finish_event.is_set()
                ):  # no more stdin, but I need it
                    self.current_process_finish_event.set()
                    raise ValueError("STDIN REQUIRED")
                elif (
                    self.current_process_finish_event
                    and not s
                    and self.current_process_finish_event.is_set()
                ):
                    return 0
                val = self.stdin.popleft()
                addr = r.address
                self.data[addr] = val
            # log.debug("---------")

    def run_program(self, data, finish_event=None, stdin=list()):
        self.ip = 0
        self.data = defaultdict(int)
        self.current_process_finish_event = finish_event
        for i in range(len(data)):
            self.data[i] = data[i]
        self.send_list_input(stdin)  # this might be a problem for leftover input
        cpu_thread = Thread(target=self.cpu, args=(finish_event,))
        cpu_thread.start()

    def run_program_sync(self, data, stdin=list()):
        finish_event = Event()
        self.run_program(data, finish_event=finish_event, stdin=stdin)
        finish_event.wait()

    def send_single_input(self, a: int):
        self.stdin.append(a)
        self.stdin_semaphore.release()

    def send_list_input(self, l: Iterable[int]):
        for a in l:
            self.stdin.append(a)
            self.stdin_semaphore.release()

    def get_single_output(self):
        s = self.stdout_semaphore.acquire(blocking=True, timeout=self.timeout)
        if (
            not s
            and self.current_process_finish_event
            and not self.current_process_finish_event.is_set()
        ):  # no more stdout, but I need it
            self.current_process_finish_event.set()
            raise ValueError("NO STDOUT")
        elif (
            not s
            and self.current_process_finish_event
            and self.current_process_finish_event.is_set()
        ):
            return None
        return self.stdout.popleft()

    def get_list_output(self):
        output = list()
        for i in range(len(self.stdout)):
            self.stdout_semaphore.acquire(blocking=True, timeout=self.timeout)
            output.append(self.stdout.popleft())
        return output

    def set_output(self, val):
        if self.send_stdout_to:
            self.send_stdout_to.send_single_input(val)
        self.stdout.append(val)

    def pipeline(self, source: Intcode2019):
        self.send_stdout_to = source

    # Add
    def op_1(self, a: Parameter, b: Parameter, c: Parameter) -> OP_out:
        self.ip += 3
        return OP_out(
            signal=Signal.OK,
            value=a.point_interpreted() + b.point_interpreted(),
            address=c.point_literal(),
            stdout=None,
        )

    # Multiply
    def op_2(self, a: Parameter, b: Parameter, c: Parameter) -> OP_out:
        self.ip += 3
        return OP_out(
            signal=Signal.OK,
            value=a.point_interpreted() * b.point_interpreted(),
            address=c.point_literal(),
            stdout=None,
        )

    # Read
    def op_3(self, a: Parameter) -> OP_out:
        self.ip += 1
        return OP_out(
            signal=Signal.INPUT_WAIT, value=None, address=a.point_literal(), stdout=None
        )

    # Write
    def op_4(self, a: Parameter) -> OP_out:
        self.ip += 1
        return OP_out(
            signal=Signal.OK, value=None, address=None, stdout=a.point_interpreted()
        )

    # Jump if True
    def op_5(self, a: Parameter, b: Parameter) -> OP_out:
        self.ip += 2
        if a.point_interpreted() != 0:
            self.ip = b.point_interpreted()
        return OP_out(signal=Signal.OK, value=None, address=None, stdout=None)

    # Jump if False
    def op_6(self, a: Parameter, b: Parameter) -> OP_out:
        self.ip += 2
        if a.point_interpreted() == 0:
            self.ip = b.point_interpreted()
        return OP_out(signal=Signal.OK, value=None, address=None, stdout=None)

    # Less than
    def op_7(self, a: Parameter, b: Parameter, c: Parameter) -> OP_out:
        self.ip += 3
        if a.point_interpreted() < b.point_interpreted():
            return OP_out(
                signal=Signal.OK, value=1, address=c.point_literal(), stdout=None
            )
        else:
            return OP_out(
                signal=Signal.OK, value=0, address=c.point_literal(), stdout=None
            )

    # Equals
    def op_8(self, a: Parameter, b: Parameter, c: Parameter) -> OP_out:
        self.ip += 3
        if a.point_interpreted() == b.point_interpreted():
            return OP_out(
                signal=Signal.OK, value=1, address=c.point_literal(), stdout=None
            )
        else:
            return OP_out(
                signal=Signal.OK, value=0, address=c.point_literal(), stdout=None
            )

    # Move Relative Base
    def op_9(self, a: Parameter) -> OP_out:
        self.ip += 1
        self.relative_base += a.point_interpreted()
        return OP_out(signal=Signal.OK, value=None, address=None, stdout=None)

    # Halt
    def op_99(self) -> OP_out:
        return OP_out(signal=Signal.HALT, value=None, address=None, stdout=None)
