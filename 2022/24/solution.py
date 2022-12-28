from typing import List, Set, Tuple
from dataclasses import dataclass, field

Coord = Tuple[int, int]
Blizzard = Tuple[Coord, str]


@dataclass(order=True)
class PathState:
    distance: int
    pos: Coord = field(compare=False)
    length: int = field(compare=False)


def main():
    with open("input.txt") as f:
        input = [line.strip() for line in f.readlines()]

    len_x, len_y = len(input[0]), len(input)
    walls, blizzards = parse_board(input)
    start = [(x, 0) for x in range(len_x) if (x, 0) not in walls][0]
    end = [(x, len_y-1) for x in range(len_x) if (x, len_y-1) not in walls][0]

    # #### Puzzle 1 #### #

    to_end_steps = find_path(start, end, blizzards, walls, len_x, len_y)
    print("Steps in shortest path to end:", to_end_steps)

    # #### Puzzle 2 #### #

    to_start_steps = find_path(end, start, blizzards, walls,
                               len_x, len_y, to_end_steps)
    print("... back to start:", to_start_steps - to_end_steps)
    to_end_again_steps = find_path(start, end, blizzards, walls,
                                   len_x, len_y, to_start_steps)
    print("... then back to end again:", to_end_again_steps - to_start_steps)
    print("... which concludes in a total step count of:", to_end_again_steps)


def parse_board(input: List[str]) -> Tuple[Set[Coord], Set[Blizzard]]:
    walls = set()
    blizzards = set()
    for y, line in enumerate(input):
        for x, c in enumerate(line):
            if c == "#":
                walls.add((x, y))
            elif c in "><v^":
                blizzards.add(((x, y), c))
    return walls, blizzards


def find_path(start: Coord, end: Coord, blizzards: Set[Blizzard],
              walls: Set[Coord], len_x: int, len_y: int,
              start_time: int = 0) -> int:
    q = [(start, start_time)]
    while len(q) != 0:
        pos, length = q.pop(0)
        if pos == end:
            return length
        positions = [(p, distance(p, end)) for p in get_positions(pos)
                     if is_legal(p, walls, blizzards, len_x, len_y, length+1)]
        positions.sort(key=lambda p: p[1])
        for new_pos, _ in positions:
            if (new_pos, length+1) in q:
                continue
            q.append((new_pos, length+1))
    return -1


def distance(a: Coord, b: Coord) -> int:
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def get_positions(pos: Coord) -> List[Coord]:
    x, y = pos
    return [(x, y-1), (x-1, y), (x, y), (x+1, y), (x, y+1)]


def is_legal(pos: Coord, walls: Set[Coord], blizzards: Set[Blizzard],
             len_x: int, len_y: int, time_passed: int) -> bool:
    x, y = pos
    if x < 0 or x >= len_x or y < 0 or y >= len_y:
        return False
    if pos in walls:
        return False
    if is_blizz(pos, blizzards, len_x, len_y, time_passed):
        return False
    return True


def is_blizz(pos: Coord, blizzards: Set[Blizzard], x_len: int, y_len: int,
             time_passed: int) -> bool:
    x, y = pos
    from_left = (((x-1) - time_passed) % (x_len-2)) + 1, y
    from_right = (((x-1) + time_passed) % (x_len-2)) + 1, y
    from_top = x, (((y-1) - time_passed) % (y_len-2)) + 1
    from_bottom = x, (((y-1) + time_passed) % (y_len-2)) + 1
    return any([
        (from_left, ">") in blizzards,
        (from_right, "<") in blizzards,
        (from_top, "v") in blizzards,
        (from_bottom, "^") in blizzards
    ])


if __name__ == "__main__":
    main()
