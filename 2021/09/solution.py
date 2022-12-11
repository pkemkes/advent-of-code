from typing import List, Tuple


def main():
    with open("input.txt") as f:
        input = [line.strip() for line in f.readlines()]

    # #### Puzzle 1 #### #

    low_points = find_low_points(input)
    risk_levels = get_risk_levels(low_points, input)
    print("Sum of risk levels:", sum(risk_levels))

    # #### Puzzle 2 #### #

    basins = find_basins(low_points, input)
    basins = sorted(basins, key=lambda b: len(b), reverse=True)
    print("Product of sizes of 3 largest basins:",
          len(basins[0]) * len(basins[1]) * len(basins[2]))


def find_low_points(input: List[str]) -> List[Tuple[int, int]]:
    low_points = []
    for row in range(len(input)):
        for col in range(len(input[0])):
            if is_low_point(row, col, input):
                low_points.append((row, col))
    return low_points


def is_low_point(row: int, col: int, input: List[str]) -> bool:
    left = get_height(row, col-1, input)
    right = get_height(row, col+1, input)
    up = get_height(row-1, col, input)
    down = get_height(row+1, col, input)
    curr_height = get_height(row, col, input)
    return all([curr_height < other for other in [left, right, up, down]])


def get_height(row: int, col: int, input: List[str]) -> int:
    if row < 0 or row >= len(input):
        return 10
    if col < 0 or col >= len(input[0]):
        return 10
    return int(input[row][col])


def get_risk_levels(low_points: List[Tuple[int, int]],
                    input: List[str]) -> List[int]:
    return [get_height(r, c, input) + 1 for r, c in low_points]


def find_basins(low_points: List[Tuple[int, int]],
                input: List[str]) -> List[List[Tuple[int, int]]]:
    basins = []
    for row, col in low_points:
        basin = [(row, col)]
        expand_basin(row, col, input, basin)
        basins.append(basin)
    return basins


def expand_basin(row: int, col: int, input: List[str],
                 basin: List[Tuple[int, int]]):
    for other_row, other_col in [(row-1, col), (row+1, col),
                                 (row, col-1), (row, col+1)]:
        if (other_row, other_col) not in basin:
            h = get_height(other_row, other_col, input)
            if h < 9:
                basin += [(other_row, other_col)]
                expand_basin(other_row, other_col, input, basin)


if __name__ == "__main__":
    main()
