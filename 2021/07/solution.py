from typing import List


def main():
    with open("input.txt") as f:
        line = f.readline()
    positions = list(map(int, line.strip().split(",")))
    min_pos, max_pos = min(positions), max(positions)

    # #### Puzzle 1 #### #

    fuel_used = [align_const_fuel(t, positions)
                 for t in range(min_pos, max_pos+1)]
    print("Lowest fuel used (constant):", min(fuel_used))

    # #### Puzzle 2 #### #

    fuel_used = [align_dyn_fuel(t, positions)
                 for t in range(min_pos, max_pos+1)]
    print("Lowest fuel used (dynamic):", min(fuel_used))


def align_const_fuel(target: int, positions: List[int]) -> int:
    return sum([abs(p - target) for p in positions])


def align_dyn_fuel(target: int, positions: List[int]) -> int:
    return sum([sum(range(abs(p - target) + 1)) for p in positions])


if __name__ == "__main__":
    main()
