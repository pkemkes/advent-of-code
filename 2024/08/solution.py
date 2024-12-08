Coordinate = tuple[int, int]
Antennas = dict[str, list[Coordinate]]
Map = list[str]


def is_in_map(coord: Coordinate, len_x: int, len_y: int) -> bool:
    x, y = coord
    return x >= 0 and y >= 0 and x < len_x and y < len_y


def find_antennas(antenna_map: Map, len_x: int, len_y: int) -> Antennas:
    antennas = {}
    for x in range(len_x):
        for y in range(len_y):
            field = antenna_map[y][x]
            if field == ".":
                continue
            if field in antennas:
                antennas[field].append((x, y))
            else:
                antennas[field] = [(x, y)]
    return antennas


def main():
    with open("input.txt") as f:
        antenna_map = [l.strip() for l in f.readlines()]
    
    len_x = len(antenna_map[0])
    len_y = len(antenna_map)

    single_antinodes = set()
    all_antinodes = set()
    antennas = find_antennas(antenna_map, len_x, len_y)
    for _, coords in antennas.items():
        for i, (x, y) in enumerate(coords):
            for other_x, other_y in coords[:i] + coords[i+1:]:
                all_antinodes.add((x, y))
                add_x, add_y = other_x - x, other_y - y
                check_x, check_y = x, y
                single_antinode_collected = False
                while True:
                    check_x += add_x
                    check_y += add_y
                    if not is_in_map((check_x, check_y), len_x, len_y):
                        break
                    all_antinodes.add((check_x, check_y))
                    if not single_antinode_collected and (check_x, check_y) != (other_x, other_y):
                        single_antinodes.add((check_x, check_y))
                        single_antinode_collected = True
    
    print("Amount of unique single antinodes locations:", len(single_antinodes))
    print("Amount of all unique antinodes locations:", len(all_antinodes))


if __name__ == "__main__":
    main()
