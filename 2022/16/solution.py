import re
from typing import List, Tuple, Dict, Set, Generator
from queue import Queue


def main():
    with open("input.txt") as f:
        input = [line.strip() for line in f.readlines()]
    tunnels, flow_rates = parse_input(input)
    functional_valves = [k for k, v in flow_rates.items()
                         if v > 0 or k == "AA"]

    # Precalculating distances between all valves with flow rate > 0

    distances_of_fv = calc_distances(functional_valves, tunnels)
    print("Calculated all important distances")

    # #### Puzzle 1 #### #

    pressure = find_highest_pressure(functional_valves, 30, "AA",
                                     distances_of_fv, flow_rates)
    print("Highest pressure:", pressure)

    # #### Puzzle 2 #### #

    pressure = find_highest_pressure_with_elephant(
        functional_valves, 26, "AA", distances_of_fv, flow_rates
    )
    print("Highest pressure with elephant:", pressure)


def parse_input(input: List[str]) -> Tuple[Dict[str, Set[str]],
                                           Dict[str, int]]:
    pattern = r"Valve (\w\w) .+ rate=(\d+); .+ valves? (.+)"
    tunnels = {}
    flow_rates = {}
    for line in input:
        info = re.search(pattern, line).groups()
        tunnels[info[0]] = set(info[-1].split(", "))
        flow_rates[info[0]] = int(info[1])
    return tunnels, flow_rates


def calc_distances(valves: List[str],
                   tunnels: Dict[str, Set[str]]) -> Dict[str, Dict[str, int]]:
    distances = {v: {} for v in valves}
    for i, v in enumerate(valves):
        for other_v in valves[i+1:]:
            if v == other_v:
                continue
            distance = find_distance(v, other_v, tunnels)
            distances[v][other_v] = distance
            distances[other_v][v] = distance
    return distances


def find_distance(start_v: str, end_v: str,
                  tunnels: Dict[str, Set[str]]) -> int:
    # Simple BFS to find shortest path between two valves
    q = Queue()
    q.put((start_v, 0))
    visited = {start_v}
    while not q.empty():
        valve, distance = q.get()
        neighbors = {n for n in tunnels[valve] if n not in visited}
        for n in neighbors:
            if n == end_v:
                return distance+1
            q.put((n, distance+1))


def find_highest_pressure(functional_valves: List[str],
                          minutes: int, start_valve: str,
                          distances_of_fv: Dict[str, Dict[str, int]],
                          flow_rates: Dict[str, int]) -> int:
    # Uses the gen_pressures method to iterate over all possible permutations
    # of valve paths and compare the resulting pressures
    highest_pressure = 0
    for _, pressure in gen_pressures(
        functional_valves, minutes, start_valve, distances_of_fv, flow_rates
    ):
        if pressure > highest_pressure:
            highest_pressure = pressure
    return highest_pressure


def find_highest_pressure_with_elephant(
    functional_valves: List[str], minutes: int, start_valve: str,
    distances_of_fv: Dict[str, Dict[str, int]], flow_rates: Dict[str, int]
) -> int:
    # Does the same as the function from Puzzle 1 but limits each runner
    # (elephant and elf) to a specific length,
    # then trying each length setting for the best paths
    highest_pressure = 0
    max_path_len = len(functional_valves)
    for len_path_elephant in range(1, round((max_path_len-1)/2)+1):
        print("Elephant path len:", len_path_elephant)
        for elephant_path, elephant_pressure in gen_pressures(
            functional_valves, minutes, start_valve, distances_of_fv,
            flow_rates, len_path_elephant
        ):
            rest_valves = [v for v in functional_valves
                           if v not in elephant_path or v == start_valve]
            for _, elf_pressure in gen_pressures(
                rest_valves, minutes, start_valve, distances_of_fv, flow_rates,
                max_path_len-len_path_elephant+1
            ):
                pressure = elephant_pressure + elf_pressure
                if pressure > highest_pressure:
                    highest_pressure = pressure
                    print(highest_pressure)
    return highest_pressure


def gen_pressures(valves: List[str], max_minutes: int,
                  start_valve: str, distances_of_fv: Dict[str, Dict[str, int]],
                  flow_rates: Dict[str, int],
                  max_length: int = None) -> Generator:
    # Generates every possible permutation of valves while not exceeding the
    # given minute limit and also not going to a valve more than once.
    # If a max_length is given, permutations can't be longer than this limit
    if max_length is None:
        max_length = len(valves)
    paths = [([start_valve], max_minutes,
              flow_rates[start_valve] * max_minutes)]
    for path, remaining_minutes, pressure in paths:
        rest_valves = [i for i in valves if i not in path]
        if not rest_valves or len(path) == max_length:
            yield path, pressure
        else:
            something_fit = False
            for valve in [v for v in valves if v not in path]:
                minutes_needed = distances_of_fv[path[-1]][valve] + 1
                new_remaining_minutes = remaining_minutes - minutes_needed
                if new_remaining_minutes > 0:
                    new_pressure = pressure + (
                        flow_rates[valve] * new_remaining_minutes
                    )
                    paths.append(
                        (path + [valve], new_remaining_minutes, new_pressure)
                    )
                    something_fit = True
            if not something_fit:
                yield path, pressure


if __name__ == "__main__":
    main()
