from copy import deepcopy

def get_guard_pos(route_map: list[str], len_x: int, len_y: int) -> tuple[int, int]:
    for x in range(len_x):
        for y in range(len_y):
            if route_map[y][x] == "^":
                return (x, y)
    return None


def is_in_map(pos: tuple[int, int], len_x: int, len_y: int) -> bool:
    x, y = pos
    return x >= 0 and y >= 0 and x < len_x and y < len_y


def get_field_value(
        pos: tuple[int, int], route_map: list[str], len_x: int, len_y: int,
    ) -> str:
        if not is_in_map(pos, len_x, len_y):
            return "."
        x, y = pos
        return route_map[y][x]


def get_next_pos(
        pos: tuple[int, int], directions: list[tuple[int, int]], current_dir: int
    ) -> tuple[int, int]:
    x, y = pos
    add_x, add_y = directions[current_dir]
    return x + add_x, y + add_y


def is_obstacle(pos: tuple[int, int], route_map: list[str], len_x: int, len_y: int) -> bool:
    return get_field_value(pos, route_map, len_x, len_y) == "#"


def calc_path_len(route_map: list[str], len_x: int, len_y: int) -> tuple[int, bool]:
    directions = [(0, -1), (1, 0), (0, 1), (-1, 0)]

    guard_pos = get_guard_pos(route_map, len_x, len_y)
    guard_positions = set()
    current_dir = 0
    looped = False
    while is_in_map(guard_pos, len_x, len_y):
        guard_positions.add((guard_pos, current_dir))
        while True:
            next_pos = get_next_pos(guard_pos, directions, current_dir)
            if not is_obstacle(next_pos, route_map, len_x, len_y):
                break
            current_dir = (current_dir + 1) % len(directions)
        guard_pos = next_pos
        if (guard_pos, current_dir) in guard_positions: 
            looped = True
            break
    distinct_guard_positions = set(pos for pos, _ in guard_positions)

    return len(distinct_guard_positions), looped


# def print_route_map(route_map: list[str])


def main():
    with open("input.txt") as f:
        route_map = [l.strip() for l in f.readlines()]
    
    len_x = len(route_map[0])
    len_y = len(route_map)

    path_len, _ = calc_path_len(route_map, len_x, len_y)

    print("Distinct guard positions:", path_len)

    looped_path_count = 0
    for x in range(len_x):
        print("working on col", x)
        for y in range(len_y):
            if get_field_value((x, y), route_map, len_x, len_y) != ".":
                continue
            new_route_map = deepcopy(route_map)
            new_route_map[y] = new_route_map[y][:x] + "#" + new_route_map[y][x+1:]
            path_len, looped = calc_path_len(new_route_map, len_x, len_y)
            if looped:
                looped_path_count += 1

    print("Number of different positions for looped paths:", looped_path_count)


if __name__ == "__main__":
    main()
