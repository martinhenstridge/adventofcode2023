import typing
from dataclasses import dataclass, field


@dataclass
class MappingEntry:
    start: int
    limit: int
    offset: int

    def contains_value(self, value):
        return self.start <= value < self.limit

    def map_value(self, value):
        return value + self.offset

    def overlaps_range(self, start, limit):
        if self.start >= limit:
            return False
        if start >= self.limit:
            return False
        return True

    def map_range(self, start, limit):
        unmapped = []
        if start < self.start:
            unmapped.append((start, min(limit, self.start)))
        if limit > self.limit:
            unmapped.append((max(start, self.limit), limit))

        mapped = [
            (
                max(start, self.start) + self.offset,
                min(limit, self.limit) + self.offset,
            )
        ]

        return mapped, unmapped


@dataclass
class Mapping:
    name: str
    entries: typing.List[MappingEntry] = field(default_factory=list)

    def add_entry(self, entry):
        self.entries.append(entry)

    def map_value(self, v):
        for entry in self.entries:
            if entry.contains_value(v):
                return entry.map_value(v)
        return v

    def map_range(self, r):
        mapped = []
        unmapped = [r]
        for entry in self.entries:
            still_unmapped = []
            for start, limit in unmapped:
                if not entry.overlaps_range(start, limit):
                    still_unmapped.append((start, limit))
                else:
                    m, u = entry.map_range(start, limit)
                    mapped.extend(m)
                    still_unmapped.extend(u)
            unmapped = still_unmapped
        return mapped + unmapped


def parse_data(data):
    seeds = None
    maps = []

    for line in data.splitlines():
        if not line:
            continue

        if line.startswith("seeds:"):
            seeds = [int(s) for s in line.split() if s != "seeds:"]
        elif line.endswith("map:"):
            name, _ = line.split()
            maps.append(Mapping(name))
        else:
            parts = [int(s) for s in line.split()]
            entry = MappingEntry(
                start=parts[1],
                limit=parts[1] + parts[2],
                offset=parts[0] - parts[1],
            )
            maps[-1].add_entry(entry)

    return seeds, maps


def apply_maps_to_value(maps, v0):
    v = v0
    for m in maps:
        v = m.map_value(v)
    return v


def apply_maps_to_range(maps, r0):
    ranges = [r0]
    for m in maps:
        mapped = []
        for r in ranges:
            output = m.map_range(r)
            mapped.extend(output)
        ranges = mapped
    return ranges


def as_ranges(seeds):
    for i in range(0, len(seeds), 2):
        yield seeds[i], seeds[i] + seeds[i + 1]


def run(data):
    seeds, maps = parse_data(data)

    min_value = min(apply_maps_to_value(maps, v) for v in seeds)

    min_range = 0xFFFFFFFF
    for r in as_ranges(seeds):
        for start, _ in apply_maps_to_range(maps, r):
            if start < min_range:
                min_range = start

    return min_value, min_range
