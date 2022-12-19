import re
from typing import List, Tuple, Set, Optional


def main():
    with open("input.txt") as f:
        input = [line.strip() for line in f.readlines()]
    sensors, beacons = parse_input(input)

    # #### Puzzle 1 #### #

    y = 2000000
    coverage = check_coverage(y, sensors)
    covered_cells = calc_covered_cells(coverage, y, beacons)
    print("Coverage in y=2000000:", covered_cells)

    # #### Puzzle 2 #### #

    limit = 4000000
    x, y = find_first_possible_beacon_pos(sensors, limit)
    print("Tuning frequency of possible beacon position:", x * limit + y)


def parse_input(input: List[str]) -> Tuple[List[Tuple[Tuple[int, int], int]],
                                           Set[Tuple[int, int]]]:
    pattern = r"Sensor at x=(-?\d+), y=(-?\d+).+x=(-?\d+), y=(-?\d+)"
    sensors = []
    beacons = []
    for line in input:
        points = re.search(pattern, line).groups()
        sensor = (int(points[0]), int(points[1]))
        beacon = (int(points[2]), int(points[3]))
        sensors.append((sensor, distance(sensor, beacon)))
        beacons.append(beacon)
    return (sensors, set(beacons))


def check_coverage(y: int, sensors: List[Tuple[Tuple[int, int], int]],
                   limit: Optional[int] = None) -> List[Tuple[int, int]]:
    coverage = []
    for sensor, distance in sensors:
        vert_dist = abs(y - sensor[1])
        if vert_dist > distance:
            continue
        vert_diff = distance - vert_dist
        coverage.append((sensor[0] - vert_diff, sensor[0] + vert_diff))
    coverage = join_overlapping(coverage)
    if limit is not None:
        for i in range(len(coverage)):
            s, e = coverage[i]
            s = max(0, s)
            e = min(limit, e)
            coverage[i] = (s, e)
    return coverage


def calc_covered_cells(coverage: List[Tuple[int, int]], y: int,
                       beacons: Optional[Set[Tuple[int, int]]] = None) -> int:
    covered_beacons = 0
    if beacons is not None:
        for b in [b for b in beacons if b[1] == y]:
            for start, end in coverage:
                if start <= b[0] and end >= b[0]:
                    covered_beacons += 1
                break
    return sum([e - s + 1 for s, e in coverage]) - covered_beacons


def find_first_possible_beacon_pos(sensors: List[Tuple[Tuple[int, int], int]],
                                   limit: int) -> Tuple[int, int]:
    for y in range(limit+1):
        coverage = check_coverage(y, sensors, limit)
        covered_cells = calc_covered_cells(coverage, y)
        if covered_cells != limit+1:
            pos = [(p, y) for p in range(limit+1)
                   if not any([s <= p and p <= e for s, e in coverage])]
            return pos[0]


def distance(a: Tuple[int, int], b: Tuple[int, int]) -> int:
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def join_overlapping(covered: List[Tuple[int, int]]) -> List[Tuple[int, int]]:
    covered = sorted(covered)
    result = []
    current = covered[0]
    for c in covered[1:]:
        if c[0] <= current[1]:
            current = (current[0], max(current[1], c[1]))
        else:
            result.append(current)
            current = c
    result.append(current)
    return result


if __name__ == "__main__":
    main()
