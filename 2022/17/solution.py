from typing import List, Tuple, Set

ROCKS = [
    [(0, 0), (1, 0), (2, 0), (3, 0)],
    [(1, 0), (0, 1), (1, 1), (2, 1), (1, 2)],
    [(0, 0), (1, 0), (2, 0), (2, 1), (2, 2)],
    [(0, 0), (0, 1), (0, 2), (0, 3)],
    [(0, 0), (1, 0), (0, 1), (1, 1)]
]


def main():
    with open("input.txt") as f:
        jets = f.readline().strip()

    # #### Puzzle 1 #### #

    iterations = 2022
    height, _ = let_rocks_fall(iterations, jets)
    print(f"Highest block after {iterations} iterations:", height)

    # #### Puzzle 2 #### #

    iterations = 1000000000000
    height, _ = let_rocks_fall(iterations, jets)
    print(f"Highest block after {iterations} iterations:", height)


def let_rocks_fall(iterations: int, jets: str) -> Tuple[int, List[Set[int]]]:
    field = [set([0]) for _ in range(7)]
    jet_i = 0
    last_rocks_i = None
    last_highest_y = None
    last_iteration = None
    iteration = 0
    while iteration < iterations:
        if iteration % 500 == 0:
            field = shorten_field(field)
        rocks_i = iteration % len(ROCKS)
        rock = ROCKS[rocks_i]
        if jet_i == 0:
            if rocks_i == last_rocks_i:
                field, iteration = skip_periods(
                    field, iteration, iterations,
                    last_iteration, last_highest_y
                )
            last_rocks_i = rocks_i
            last_highest_y = get_highest_block(field)
            last_iteration = iteration
        highest_point = get_highest_block(field)
        rock_pos = [(x+2, y+highest_point+4) for x, y in rock]
        while True:
            rock_pushed_by_jet = push_with_jet(jets[jet_i], rock_pos, field)
            jet_i = (jet_i + 1) % len(jets)
            rock_moved_down = move_down(rock_pushed_by_jet, field)
            # If the rock could not move down, settle it in field
            if rock_moved_down == rock_pushed_by_jet:
                settle_rock(rock_moved_down, field)
                break
            else:
                rock_pos = rock_moved_down
        iteration += 1
    return get_highest_block(field), field


def get_highest_block(field: List[Set[int]]) -> int:
    return max([max(col) for col in field])


def push_with_jet(jet: str, rock_pos: List[Tuple[int, int]],
                  field: List[Set[int]]) -> List[Tuple[int, int]]:
    if jet == "<":
        rock_moved_left = [(x-1, y) for x, y in rock_pos]
        return rock_moved_left \
            if can_be_moved_left(rock_moved_left, field) \
            else rock_pos
    elif jet == ">":
        rock_moved_right = [(x+1, y) for x, y in rock_pos]
        return rock_moved_right \
            if can_be_moved_right(rock_moved_right, field) \
            else rock_pos
    else:
        raise Exception(f"Illegal jet: {jet}")


def move_down(rock_pos: List[Tuple[int, int]],
              field: List[Set[int]]) -> List[Tuple[int, int]]:
    rock_moved_down = [(x, y-1) for x, y in rock_pos]
    return rock_moved_down \
        if can_be_moved_down(rock_moved_down, field) \
        else rock_pos


def can_be_moved_left(rock_moved_left: List[Tuple[int, int]],
                      field: List[Set[int]]) -> bool:
    return not any([x < 0 for x, _ in rock_moved_left]) and \
        not any([y in field[x] for x, y in rock_moved_left])


def can_be_moved_right(rock_moved_right: List[Tuple[int, int]],
                       field: List[Set[int]]) -> bool:
    return not any([x >= len(field) for x, _ in rock_moved_right]) and \
        not any([y in field[x] for x, y in rock_moved_right])


def can_be_moved_down(rock_moved_down: List[Tuple[int, int]],
                      field: List[Set[int]]) -> bool:
    return not any([y <= 0 for _, y in rock_moved_down]) and \
        not any([y in field[x] for x, y in rock_moved_down])


def settle_rock(rock_pos: List[Tuple[int, int]],
                field: List[Set[int]]):
    for x, y in rock_pos:
        field[x].add(y)


def shorten_field(field: List[Set[int]]) -> List[Set[int]]:
    max_needed_y = find_max_needed_y(field)
    field = [{pos for pos in col if pos >= max_needed_y} for col in field]
    return field


def find_max_needed_y(field: List[Set[int]]) -> int:
    highest = get_highest_block(field)
    found_block = [False for _ in range(len(field))]
    for y in range(highest, -1, -1):
        for x in range(len(field)):
            if y in field[x]:
                found_block[x] = True
        if all(found_block):
            return y


def skip_periods(field: List[Set[int]], iteration: int, iterations: int,
                 last_iteration: int,
                 last_highest_y: int) -> Tuple[List[Set[int]], int]:
    height_diff = get_highest_block(field) - last_highest_y
    iteration_diff = iteration - last_iteration
    to_skip = int((iterations - iteration) / iteration_diff)
    iteration += to_skip * iteration_diff
    field = [{y + (height_diff*to_skip) for y in col}
             for col in field]
    return field, iteration


if __name__ == "__main__":
    main()
