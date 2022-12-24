from typing import List, Tuple, Set


def main():
    with open("input.txt") as f:
        coords = {tuple([int(c) for c in line.strip().split(",")])
                  for line in f.readlines()}

    # #### Puzzle 1 #### #

    surface_area = count_surface_area(coords)
    print("Surface area:", surface_area)

    # #### Puzzle 2 #### #

    ext_surface_area = count_surface_area(coords, count_air_pockets=False)
    print("Exterior surface area:", ext_surface_area)


def count_surface_area(coords: Set[Tuple[int, int, int]],
                       count_air_pockets: bool = True) -> int:
    remaining_coords = set(coords)
    surface_area = 0
    analyzed = set()
    while len(remaining_coords) != 0:
        to_analyze = set([next(iter(remaining_coords))])
        while len(to_analyze) != 0:
            drop = to_analyze.pop()
            for side in get_sides(drop):
                if side in coords:
                    if side in remaining_coords and \
                            side not in analyzed:
                        to_analyze.add(side)
                elif count_air_pockets or not is_air_pocket(side, coords):
                    surface_area += 1
            remaining_coords.remove(drop)
            analyzed.add(drop)
    return surface_area


def get_sides(drop: Tuple[int, int, int]) -> List[Tuple[int, int, int]]:
    x, y, z = drop
    return [
        (x-1, y, z),
        (x+1, y, z),
        (x, y-1, z),
        (x, y+1, z),
        (x, y, z-1),
        (x, y, z+1)
    ]


def is_air_pocket(drop: Tuple[int, int, int],
                  coords: Set[Tuple[int, int, int]]) -> bool:
    extremes = get_extremes(coords)
    to_check = set([drop])
    checked = set()
    while len(to_check) != 0:
        side = to_check.pop()
        if is_outside(side, extremes):
            return False
        for other_side in get_sides(side):
            if other_side not in coords and other_side not in checked:
                to_check.add(other_side)
        checked.add(side)
    return True


def get_extremes(coords: Set[Tuple[int, int, int]])\
        -> Tuple[int, int, int, int, int, int]:
    x_min = min(coords, key=lambda c: c[0])[0]
    x_max = max(coords, key=lambda c: c[0])[0]
    y_min = min(coords, key=lambda c: c[1])[1]
    y_max = max(coords, key=lambda c: c[1])[1]
    z_min = min(coords, key=lambda c: c[2])[2]
    z_max = max(coords, key=lambda c: c[2])[2]
    return x_min, x_max, y_min, y_max, z_min, z_max


def is_outside(drop: Tuple[int, int, int],
               extremes: Tuple[int, int, int, int, int, int]) -> bool:
    return any([drop[i] < extremes[i*2] or drop[i] > extremes[i*2+1]
               for i in range(3)])


if __name__ == "__main__":
    main()
