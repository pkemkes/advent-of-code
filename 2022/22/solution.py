from typing import List, Tuple, Optional, Dict

Board = List[str]
Path = List[str]  # List of distances and turn, both as str
Coord = Tuple[int, int, int]  # x, y, direction (0=right, 1=down, 2=left, 3=up)
CubeMap = Dict[Coord, Tuple[int, int]]  # Maps wrapping coordinates


def main():
    with open("input.txt") as f:
        board, path = f.read().split("\n\n")
    parsed_board = parse_board(board)
    parsed_path = parse_path(path)
    start = (parsed_board[0].index("."), 0, 0)

    # #### Puzzle 1 #### #

    final_pos = walk_path(parsed_path, start, parsed_board)
    print("Final pos:", final_pos)
    print("Password:", calc_password(final_pos))

    # #### Puzzle 2 #### #

    cube_map = build_cube_map()
    cubed_final_pos = walk_path(parsed_path, start, parsed_board, cube_map)
    print("Final pos when cubed:", cubed_final_pos)
    print("Cubed Password:", calc_password(cubed_final_pos))


def parse_board(board: List[str]) -> Board:
    lines = board.split("\n")
    max_line_len = max([len(line) for line in lines])
    return [line + (" " * (max_line_len - len(line))) for line in lines]


def parse_path(path: str) -> Path:
    path = path.strip()
    parsed_path = []
    current = ""
    current_is_num = path[0].isnumeric()
    for c in path:
        if c.isnumeric() != current_is_num:
            parsed_path.append(current)
            current_is_num = c.isnumeric()
            current = ""
        current += c
    parsed_path.append(current)
    return parsed_path


def walk_path(path: Path, start: Coord, board: Board,
              cube_map: Optional[CubeMap] = None) -> Coord:
    x, y, dir = start
    for step in path:
        if step.isnumeric():
            x, y, dir = walk_distance(x, y, dir, int(step), board, cube_map)
        else:
            dir = turn(dir, step)
    return (x, y, dir)


def turn(dir: int, step: str) -> int:
    return (dir + (1 if step == "R" else -1)) % 4


def walk_distance(x: int, y: int, dir: int, distance: int, board: Board,
                  cube_map: Optional[CubeMap]) -> Tuple[int, int]:
    for _ in range(distance):
        next_x, next_y = step_in_dir(x, y, dir)
        next_dir = dir
        if is_off_board(next_x, next_y, board):
            if cube_map:
                next_x, next_y, next_dir = wrap_cubed(next_x, next_y, next_dir,
                                                      cube_map)
            else:
                next_x, next_y, next_dir = wrap_2D(next_x, next_y, next_dir,
                                                   board)
        if board[next_y][next_x] == "#":
            return x, y, dir
        else:
            x, y, dir = next_x, next_y, next_dir
    return x, y, dir


def step_in_dir(x: int, y: int, dir: int) -> Tuple[int, int]:
    x = x + 1 if dir == 0 else x - 1 if dir == 2 else x
    y = y + 1 if dir == 1 else y - 1 if dir == 3 else y
    return x, y


def is_off_board(x: int, y: int, board: Board) -> bool:
    return (
        x < 0 or x >= len(board[0]) or
        y < 0 or y >= len(board) or
        board[y][x] == " "
    )


def wrap_2D(x: int, y: int, dir: int, board: Board) -> Coord:
    if dir % 2 == 0:
        full_row = board[y]
        row = full_row.strip()
        return full_row.find(row) + (0 if dir == 0 else len(row) - 1), y, dir
    if dir % 2 == 1:
        full_col = "".join([row[x] for row in board])
        col = full_col.strip()
        return x, full_col.find(col) + (0 if dir == 1 else len(col) - 1), dir


def wrap_cubed(x: int, y: int, dir: int,
               cube_map: CubeMap) -> Coord:
    return cube_map[(x, y, dir)]


def build_cube_map() -> CubeMap:
    cube_map = {}
    for i in range(50):
        cube_map[(100+i, 50, 1)] = (99, 50+i, 2)    # 2 -> 3
        cube_map[(100, 50+i, 0)] = (100+i, 49, 3)   # 3 -> 2
        cube_map[(49, 50+i, 2)] = (i, 100, 1)       # 3 -> 4
        cube_map[(i, 99, 3)] = (50, 50+i, 0)        # 4 -> 3
        cube_map[(50+i, 150, 1)] = (49, 150+i, 2)   # 5 -> 6
        cube_map[(50, 150+i, 0)] = (50+i, 149, 3)   # 6 -> 5
        cube_map[(49, i, 2)] = (0, 149-i, 0)        # 1 -> 4
        cube_map[(-1, 100+i, 2)] = (50, 49-i, 0)    # 4 -> 1
        cube_map[(50+i, -1, 3)] = (0, 150+i, 0)     # 1 -> 6
        cube_map[(-1, 150+i, 2)] = (50+i, 0, 1)     # 6 -> 1
        cube_map[(100+i, -1, 3)] = (i, 199, 3)      # 2 -> 6
        cube_map[(i, 200, 1)] = (100+i, 0, 1)       # 6 -> 2
        cube_map[(150, i, 0)] = (99, 149-i, 2)      # 2 -> 5
        cube_map[(100, 100+i, 0)] = (149, 49-i, 2)  # 5 -> 2
    return cube_map


def calc_password(coord: Coord) -> int:
    return (1000 * (coord[1] + 1)) + (4 * (coord[0] + 1)) + coord[2]


if __name__ == "__main__":
    main()

# lower scale map
#
#      1111122222
#      1111122222
#      1111122222
#      1111122222
#      1111122222
#      33333
#      33333
#      33333
#      33333
#      33333
# 4444455555
# 4444455555
# 4444455555
# 4444455555
# 4444455555
# 66666
# 66666
# 66666
# 66666
# 66666
