from typing import List, Tuple


def main():
    with open("input.txt") as f:
        input = [line.strip().split(" ") for line in f.readlines()]
    moves = [(i[0], int(i[1])) for i in input]

    # #### Puzzle 1 #### #

    tail_positions = move_rope(moves, 2)
    print("Number of distinct tail positions for rope of len 2:",
          len(set(tail_positions)))

    # #### Puzzle 2 #### #

    tail_positions = move_rope(moves, 10)
    print("Number of distinct tail positions for rope of len 10:",
          len(set(tail_positions)))


def move_rope(moves: List[Tuple[str, int]],
              length: int) -> List[Tuple[int, int]]:
    rope = [(0, 0)] * length
    tail_positions = [rope[-1]]
    for dir, steps in moves:
        for _ in range(steps):
            move_rope_in_dir(dir, rope)
            tail_positions.append(rope[-1])
    return tail_positions


def move_rope_in_dir(dir: str, rope: List[Tuple[int, int]]):
    rope[0] = move_part(dir, rope[0])
    for i in range(1, len(rope)):
        while needs_to_move(rope[i-1], rope[i]):
            corrective_dirs = get_corrective_dir(rope[i-1], rope[i])
            for corrective_dir in corrective_dirs:
                rope[i] = move_part(corrective_dir, rope[i])


def move_part(dir: str, pos: Tuple[int, int]) -> Tuple[int, int]:
    if dir == "U":
        return (pos[0], pos[1] + 1)
    elif dir == "D":
        return (pos[0], pos[1] - 1)
    elif dir == "R":
        return (pos[0] + 1, pos[1])
    elif dir == "L":
        return (pos[0] - 1, pos[1])
    else:
        raise Exception(f"Invalid direction {dir}")


def needs_to_move(this: Tuple[int, int], next: Tuple[int, int]) -> bool:
    return abs(this[0] - next[0]) > 1 or abs(this[1] - next[1]) > 1


def get_corrective_dir(this: Tuple[int, int], next: Tuple[int, int]) -> str:
    dir_to_move = ""
    if this[0] > next[0]:
        dir_to_move += "R"
    elif this[0] < next[0]:
        dir_to_move += "L"
    if this[1] > next[1]:
        dir_to_move += "U"
    elif this[1] < next[1]:
        dir_to_move += "D"
    return dir_to_move


if __name__ == "__main__":
    main()
