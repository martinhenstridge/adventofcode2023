import math
import re


def parse_path_network(data):
    lines = data.splitlines()
    path = tuple(0 if char == "L" else 1 for char in lines[0])

    network = {}
    for line in lines[1:]:
        if not line:
            continue
        match = re.fullmatch(r"(\w{3}) = \((\w{3}), (\w{3})\)", line)
        network[match[1]] = (match[2], match[3])

    return path, network


def steps(path):
    while True:
        yield from path


def traverse(network, path, start, terminate):
    node = start
    count = 0

    for step in steps(path):
        node = network[node][step]
        count += 1
        if terminate(node):
            return count


def run(data):
    path, network = parse_path_network(data)

    count_single = traverse(network, path, "AAA", lambda n: n == "ZZZ")
    counts_multi = [
        traverse(network, path, node, lambda n: n.endswith("Z"))
        for node in network
        if node.endswith("A")
    ]

    return count_single, math.lcm(*counts_multi)
