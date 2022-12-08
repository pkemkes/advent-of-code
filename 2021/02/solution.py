from typing import List, Tuple


def main():
    with open("input.txt") as f:
        input = [line.strip().split(" ") for line in f]
    input = [(dir, int(steps)) for dir, steps in input]

    # #### Puzzle 1 #### #

    horiz, depth = get_positions_simple(input)
    print("Horizontal pos * Depth =", horiz * depth)

    # #### Puzzle 2 #### #

    horiz, depth = get_positions_complex(input)
    print("Horizontal pos * Depth =", horiz * depth)


def get_positions_simple(moves: List[Tuple[str, int]]) -> Tuple[int, int]:
    horiz = 0
    depth = 0
    for dir, steps in moves:
        if dir == "forward":
            horiz += steps
        elif dir == "down":
            depth += steps
        elif dir == "up":
            depth -= steps
        else:
            raise Exception(f"Unknown direction {dir}")
    return horiz, depth


def get_positions_complex(moves: List[Tuple[str, int]]) -> Tuple[int]:
    horiz = 0
    depth = 0
    aim = 0
    for dir, steps in moves:
        if dir == "forward":
            horiz += steps
            depth += aim * steps
        elif dir == "down":
            aim += steps
        elif dir == "up":
            aim -= steps
        else:
            raise Exception(f"Unknown direction {dir}")
    return horiz, depth


if __name__ == "__main__":
    main()
