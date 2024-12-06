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


def main():
    with open("input.txt") as f:
        route_map = [l.strip() for l in f.readlines()]
    
    len_x = len(route_map[0])
    len_y = len(route_map)

    directions = [(0, -1), (1, 0), (0, 1), (-1, 0)]

    guard_pos = get_guard_pos(route_map, len_x, len_y)
    guard_positions = []
    current_dir = 0
    while is_in_map(guard_pos, len_x, len_y):
        guard_positions.append(guard_pos)
        changes = 0
        while is_obstacle(
            get_next_pos(guard_pos, directions, current_dir), route_map, len_x, len_y
        ):
            current_dir = (current_dir + 1) % len(directions)
            changes += 1
            if changes >= len(directions):
                raise f"Got stuck changing directions at {guard_pos}!"
        guard_pos = get_next_pos(guard_pos, directions, current_dir)
    
    distinct_guard_positions = set(guard_positions)
    print("Distinct guard positions:", len(distinct_guard_positions))


if __name__ == "__main__":
    main()
