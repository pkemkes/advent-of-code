Warehouse = list[list[str]]
Coord = tuple[int, int]

DIR_DICT = {
    "v": ( 0,  1),
    ">": ( 1,  0),
    "^": ( 0, -1),
    "<": (-1,  0)
}


def draw_warehouse(warehouse: Warehouse) -> str:
    return "\n".join("".join(row) for row in warehouse)


def find_bot(warehouse: Warehouse) -> Coord:
    len_x = len(warehouse[0])
    len_y = len(warehouse)
    for y in range(len_y):
        for x in range(len_x):
            if warehouse[y][x] == "@":
                return (x, y)
    raise RuntimeError(
        "Could not find bot in warehouse:\n" + 
        draw_warehouse()
    )


def is_in_warehouse(pos: Coord, warehouse: Warehouse) -> bool:
    len_x = len(warehouse[0])
    len_y = len(warehouse)
    x, y = pos
    return x >= 0 and y >= 0 and x < len_x and y < len_y


def try_move(pos: Coord, dir: Coord, warehouse: Warehouse) -> bool:
    x, y = pos
    field = warehouse[y][x]
    add_x, add_y = dir
    next_x, next_y = x+add_x, y+add_y
    if not is_in_warehouse((next_x, next_y), warehouse):
        return False
    next_field = warehouse[next_y][next_x]
    if next_field == "#":
        return False
    if next_field == "O" and not try_move((next_x, next_y), dir, warehouse):
        return False
    warehouse[next_y][next_x] = field
    warehouse[y][x] = "."
    return True


def move(pos: Coord, dir: Coord, warehouse: Warehouse) -> Coord:
    if try_move(pos, dir, warehouse):
        return pos[0] + dir[0], pos[1] + dir[1]
    return pos


def calc_gps(pos: Coord) -> int:
    x, y = pos
    return x + (y*100)


def calc_box_gps_sum(warehouse: Warehouse) -> int:
    len_x = len(warehouse[0])
    len_y = len(warehouse)
    gps_sum = 0
    for y in range(len_y):
        for x in range(len_x):
            if warehouse[y][x] == "O":
                gps_sum += calc_gps((x, y))
    return gps_sum


def main():
    with open("input.txt") as f:
        warehouse, moves = f.read().strip().split("\n\n")

    warehouse = [
        [c for c in l.strip()] 
        for l in warehouse.strip().split("\n")
    ]
    moves = "".join(moves.strip().split("\n"))

    bot_pos = find_bot(warehouse)
    for i, move_c in enumerate(moves):
        dir = DIR_DICT[move_c]
        bot_pos = move(bot_pos, dir, warehouse)
    print(draw_warehouse(warehouse))

    print("GPS sum of boxes:", calc_box_gps_sum(warehouse))


if __name__ == "__main__":
    main()
