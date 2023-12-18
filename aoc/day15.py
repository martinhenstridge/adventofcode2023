def parse_steps(data):
    return data.strip().split(",")


def parse_step(step):
    if step.endswith("-"):
        return step[:-1], None
    label, lens = step.split("=")
    return label, int(lens)


def hash_string(s):
    value = 0
    for c in s:
        value += ord(c)
        value *= 17
        value &= 0xFF
    return value


def run_hashmap(steps):
    boxes = [{} for _ in range(256)]
    for step in steps:
        label, lens = parse_step(step)
        box = boxes[hash_string(label)]
        if not lens:
            box.pop(label, None)
        else:
            box[label] = lens
    return boxes


def focusing_power(boxes):
    return sum(
        b * s * lens
        for b, box in enumerate(boxes, start=1)
        for s, lens in enumerate(box.values(), start=1)
    )


def run(data):
    steps = parse_steps(data)

    checksum = sum(hash_string(step) for step in steps)
    boxes = run_hashmap(steps)

    return checksum, focusing_power(boxes)
