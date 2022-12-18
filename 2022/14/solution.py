from typing import List, Tuple


def main():
    with open("input.txt") as f:
        input = [line.strip() for line in f.readlines()]

    # #### Puzzle 1 #### #

    cave, sand_x = parse_rocks(input)
    while not drop_sand(cave, sand_x):
        pass
    rested = sum(cave, []).count(2)
    print("Units of sand rested without floor:", rested)

    # #### Puzzle 2 #### #

    cave, sand_x = parse_rocks(input)
    add_floor(cave)
    while not drop_sand(cave, sand_x):
        pass
    rested = sum(cave, []).count(2)
    print("Units of sand rested with floor:", rested)


def parse_rocks(input: List[str]) -> Tuple[List[List[int]], int]:
    paths = [[list(map(int, pos.split(","))) for pos in line.split(" -> ")]
             for line in input]
    height = max([y for _, y in sum(paths, [])]) + 1
    left = min([x for x, _ in sum(paths, [])])
    left = left if left < 500 - height - 1 else 500 - height - 1
    right = max([x for x, _ in sum(paths, [])])
    right = right if right > 500 + height + 1 else 500 + height + 1
    sand_x = 500 - left
    width = right - left + 1
    cave = [[0 for _ in range(width)] for _ in range(height)]
    for path in paths:
        prev = None
        for x, y in path:
            if prev is not None:
                draw_line(cave, prev, (x-left, y))
            prev = (x-left, y)
    return cave, sand_x


def draw_line(cave: List[List[int]], start: Tuple[int, int],
              end: Tuple[int, int]):
    if start[0] == end[0]:
        if start[1] < end[1]:
            for y in range(start[1], end[1]+1):
                cave[y][start[0]] = 1
        elif start[1] > end[1]:
            for y in range(start[1], end[1]-1, -1):
                cave[y][start[0]] = 1
        else:
            raise Exception(f"Invalid path: {start} -> {end}")
    elif start[1] == end[1]:
        if start[0] < end[0]:
            for x in range(start[0], end[0]+1):
                cave[start[1]][x] = 1
        elif start[0] > end[0]:
            for x in range(start[0], end[0]-1, -1):
                cave[start[1]][x] = 1
        else:
            raise Exception(f"Invalid path: {start} -> {end}")
    else:
        raise Exception(f"Invalid path: {start} -> {end}")


def drop_sand(cave: List[List[int]], sand_x: int) -> bool:
    x, y = sand_x, 0
    while True:
        if y+1 >= len(cave) or cave[y][x] != 0:
            return True
        elif cave[y+1][x] == 0:
            y += 1
        elif cave[y+1][x-1] == 0:
            y += 1
            x -= 1
        elif cave[y+1][x+1] == 0:
            y += 1
            x += 1
        else:
            cave[y][x] = 2
            return False


def add_floor(cave: List[List[int]]):
    cave.append([0 for _ in range(len(cave[0]))])
    cave.append([1 for _ in range(len(cave[0]))])


if __name__ == "__main__":
    main()
