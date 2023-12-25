from typing import Tuple, List

Coord = Tuple[int, int]
Directions = List[int]
Map = List[List[str]]

with open("input.txt") as f:
    map = [[c for c in line.strip()] for line in f.readlines()]

FLOWS = {
    #     up     right  down   left
    "|": (True,  False, True,  False),
    "-": (False, True,  False, True),
    "L": (True,  True,  False, False),
    "J": (True,  False, False, True),
    "7": (False, False, True,  True),
    "F": (False, True,  True,  False),
    ".": (False, False, False, False),
    "S": (True,  True,  True,  True),
}

FLOW_MAPPING = ((0, -1), (1, 0), (0, 1), (-1, 0))


def find_possible_flows(pos: Coord, map: Map) -> Directions:
    x, y = pos
    possibilities = (
        y > 0             and FLOWS[map[y][x]][0] and FLOWS[map[y-1][x]][2],
        x < len(map[0])-1 and FLOWS[map[y][x]][1] and FLOWS[map[y][x+1]][3],
        y < len(map)-1    and FLOWS[map[y][x]][2] and FLOWS[map[y+1][x]][0],
        x > 0             and FLOWS[map[y][x]][3] and FLOWS[map[y][x-1]][1]
    )
    return [i for i in range(4) if possibilities[i]]


def to_next_pos(pos: Coord, dir_index: int) -> Coord:
    x, y = pos
    x_add, y_add = FLOW_MAPPING[dir_index]
    return (x+x_add, y+y_add)


def find_loop(start_pos: Coord) -> List[Coord]:
    loop = [start_pos]
    while len(loop) < 2 or loop[-1] != start_pos:
        possible_posistions = [to_next_pos(loop[-1], dir)
                               for dir in find_possible_flows(loop[-1], map)]
        loop.append([p for p in possible_posistions
                     if len(loop) < 2 or p != loop[-2]][0])
    return loop


for y in range(len(map)):
    for x in range(len(map[y])):
        if map[y][x] == "S":
            start_pos = (x, y)

possible_dirs = find_possible_flows(start_pos, map)
start_symbol = [symbol for symbol, dirs in FLOWS.items()
                if dirs == tuple([i in possible_dirs for i in range(4)])][0]
map[start_pos[1]][start_pos[0]] = start_symbol

# #### Puzzle 1 #### #

loop = find_loop(start_pos)
print("Steps needed for farthest pos from start:", len(loop) // 2)


# #### Puzzle 2 #### #

OPPOSITE_CORNERS = {"L": "J", "J": "L", "7": "F", "F": "7"}

# maps previous symbol, side and next symbol to next side if - is involved
NEXT_SIDE_MAPPING = {
    ("-", "up",    "J"): "left",
    ("-", "up",    "7"): "right",
    ("-", "up",    "L"): "right",
    ("-", "up",    "F"): "left",
    ("-", "down",  "J"): "right",
    ("-", "down",  "7"): "left",
    ("-", "down",  "L"): "left",
    ("-", "down",  "F"): "right",
    ("J", "left",  "-"): "up",
    ("J", "right", "-"): "down",
    ("7", "left",  "-"): "down",
    ("7", "right", "-"): "up",
    ("L", "left",  "-"): "down",
    ("L", "right", "-"): "up",
    ("F", "left",  "-"): "up",
    ("F", "right", "-"): "down",
}


def get_next_side(prev_symbol: str, prev_side: str, symbol: str) -> str:
    if prev_symbol == OPPOSITE_CORNERS.get(symbol):
        return "right" if prev_side == "left" else "left"
    if (prev_symbol == "-" or symbol == "-") and prev_symbol != symbol:
        return NEXT_SIDE_MAPPING[(prev_symbol, prev_side, symbol)]
    return prev_side


def find_enclosed(map: Map, loop: List[Coord],
                  start_side: str = "right") -> List[Coord]:
    CORNERS = ["L", "J", "7", "F"]
    STRAIGHTS = ["|", "-"]
    all_inside = set()
    start_x, start_y = loop[0]
    symbol = "F" if map[start_y][start_x] == "-" else "|"
    side = start_side
    for x, y in loop:
        side = get_next_side(symbol, side, map[y][x])
        symbol = map[y][x]
        all_inside.add((x, y))
        if side == "right" and symbol in ["|", "7", "J"]:
            add_x, add_y = (1, 0)
        elif side == "left" and symbol in ["|", "F", "L"]:
            add_x, add_y = (-1, 0)
        elif symbol == "-":
            add_x, add_y = (0, -1) if side == "up" else (0, 1)
        else:
            continue
        next_x, next_y = (x+add_x, y+add_y)
        while True:
            if (
                next_x < 0 or next_x >= len(map[0]) or
                next_y < 0 or next_y >= len(map)
            ) and start_side == "right":
                return find_enclosed(map, loop, "left")
            if map[next_y][next_x] in CORNERS + STRAIGHTS:
                break
            all_inside.add((next_x, next_y))
            next_x, next_y = (next_x+add_x, next_y+add_y)
    return [pos for pos in all_inside if pos not in loop]


clean_map = [["." for _ in range(len(row))] for row in map]
for x, y in loop:
    clean_map[y][x] = map[y][x]
print("Number of enclosed tiles:", len(find_enclosed(clean_map, loop)))
