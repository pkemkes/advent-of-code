from typing import List, Tuple
from copy import deepcopy

Image = List[List[str]]
Coord = Tuple[int, int]

with open("input.txt") as f:
    image = [[c for c in line.strip()] for line in f.readlines()]


def get_col(image: Image, x: int) -> Image:
    return [row[x] for row in image]


def all_galaxy_coords(image: Image) -> List[Coord]:
    result = []
    for y, row in enumerate(image):
        for x, c in enumerate(row):
            if c == "#":
                result.append((x, y))
    return result


def all_galaxy_pairs(image: Image) -> List[Tuple[Coord, Coord]]:
    galaxies = all_galaxy_coords(image)
    galaxy_pairs = []
    for i, galaxy_a in enumerate(galaxies):
        for galaxy_b in galaxies[i:]:
            galaxy_pairs.append((galaxy_a, galaxy_b))
    return galaxy_pairs


# #### Puzzle 1 #### #

def expand_universe_simple(image: Image) -> Image:
    expandeded_rows = []
    for row in image:
        expandeded_rows.append(deepcopy(row))
        if not any([c == "#" for c in row]):
            expandeded_rows.append(deepcopy(row))
    expanded_all = [[] for _ in range(len(expandeded_rows))]
    for x in range(len(expandeded_rows[0])):
        col = get_col(expandeded_rows, x)
        for i, c in enumerate(col):
            expanded_all[i].append(c)
        if not any([c == "#" for c in col]):
            for i, c in enumerate(col):
                expanded_all[i].append(c)
    return expanded_all


def distance_simple(coord_a: Coord, coord_b: Coord) -> int:
    ax, ay = coord_a
    bx, by = coord_b
    return abs(ax - bx) + abs(ay - by)


expanded = expand_universe_simple(image)
distances = [distance_simple(galaxy_a, galaxy_b)
             for galaxy_a, galaxy_b in all_galaxy_pairs(expanded)]
print("Sum of shortest paths with simple expansion:",
      sum(distances))


# #### Puzzle 2 #### #

def expand_universe_complex(image: Image) -> Image:
    expanded_all = [
        row if any(c == "#" for c in row) else ["E" for _ in range(len(row))]
        for row in image
    ]
    for x in range(len(expanded_all[0])):
        col = get_col(expanded_all, x)
        if not any(c == "#" for c in col):
            for y in range(len(expanded_all)):
                expanded_all[y][x] = "E"
    return expanded_all


def distance_complex(coord_a: Coord, coord_b: Coord, image: Image) -> int:
    ax, ay = coord_a
    bx, by = coord_b
    e_count = 0
    for y in range(min(ay, by), max(ay, by)+1):
        if image[y][ax] == "E":
            e_count += 1
    for x in range(min(ax, bx), max(ax, bx)+1):
        if image[by][x] == "E":
            e_count += 1
    return abs(ax - bx) + abs(ay - by) - e_count + e_count * 1000000


expanded = expand_universe_complex(image)
distances = [distance_complex(galaxy_a, galaxy_b, expanded)
             for galaxy_a, galaxy_b in all_galaxy_pairs(expanded)]
print("Sum of shortest paths with complex expansion:",
      sum(distances))
