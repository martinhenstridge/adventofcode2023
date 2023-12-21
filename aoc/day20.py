from abc import ABC, abstractmethod
from collections import defaultdict, deque
from enum import Enum


class Pulse:
    HIGH = 1
    LOW = 2


class Module(ABC):
    def send(self, pulse):
        for destination in self.destinations:
            yield destination, pulse, self.name

    def receive(self, pulse, sender):
        pass


class Sink(Module):
    def __init__(self):
        self.name = ""
        self.destinations = []


class Broadcaster(Module):
    def __init__(self, name, destinations):
        self.name = name
        self.destinations = destinations

    def receive(self, pulse, sender):
        yield from self.send(pulse)


class FlipFlop(Module):
    def __init__(self, name, destinations):
        self.name = name
        self.destinations = destinations
        self.active = False

    def receive(self, pulse, sender):
        if pulse is Pulse.HIGH:
            return
        self.active = not self.active
        yield from self.send(Pulse.HIGH if self.active else Pulse.LOW)


class Conjunction(Module):
    def __init__(self, name, destinations):
        self.name = name
        self.destinations = destinations
        self.inputs = {}

    def receive(self, pulse, sender):
        self.inputs[sender] = pulse
        yield from self.send(
            Pulse.LOW
            if all(i is Pulse.HIGH for i in self.inputs.values())
            else Pulse.HIGH
        )


def parse_modules(data):
    for line in data.splitlines():
        name, _, *destinations = line.replace(",", "").split()
        if name == "broadcaster":
            yield Broadcaster(name, destinations)
        elif name.startswith("%"):
            yield FlipFlop(name[1:], destinations)
        elif name.startswith("&"):
            yield Conjunction(name[1:], destinations)


def push_button(modules, pulses):
    queue = deque([("broadcaster", Pulse.LOW, None)])
    while queue:
        destination, pulse, sender = queue.popleft()
        pulses[pulse] += 1

        receiver = modules.get(destination)
        if receiver is None:
            continue
        queue.extend(receiver.receive(pulse, sender))


def run(data):
    modules = defaultdict(Sink)
    for module in parse_modules(data):
        modules[module.name] = module

    for module in modules.values():
        for destination in module.destinations:
            if destination in modules and isinstance(modules[destination], Conjunction):
                modules[destination].inputs[module.name] = Pulse.LOW

    pulses = {Pulse.HIGH: 0, Pulse.LOW: 0}
    for _ in range(1000):
        push_button(modules, pulses)

    return pulses[Pulse.HIGH] * pulses[Pulse.LOW], 0


DATA1 = """\
broadcaster -> a, b, c
%a -> b
%b -> c
%c -> inv
&inv -> a"""

DATA2 = """\
broadcaster -> a
%a -> inv, con
&inv -> b
%b -> con
&con -> output"""
