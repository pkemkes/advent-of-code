from typing import List, Tuple


def main():
    with open("input.txt") as f:
        input = [line.strip() for line in f.readlines()]
    lines = parse_lines(input)

    # #### Puzzle 1 #### #

    filtered_lines = only_horiz_and_vert(lines)
    field = get_field(*get_dimensions(filtered_lines))
    mark_lines(filtered_lines, field)
    print("Points where more than 2 lines overlap without diag:",
          count_points(field))

    # #### Puzzle 2 #### #

    field = get_field(*get_dimensions(lines))
    mark_lines(lines, field)
    print("Points where more than 2 lines overlap with diag:",
          count_points(field))


def parse_lines(input: List[str]) -> List[Tuple[Tuple[int, int]]]:
    lines = []
    for i in input:
        splits = [s.split(",") for s in i.split(" -> ")]
        lines.append(((int(splits[0][0]), int(splits[0][1])),
                      (int(splits[1][0]), int(splits[1][1]))))
    return lines


def only_horiz_and_vert(lines: List[Tuple[Tuple[int, int]]])\
        -> List[Tuple[Tuple[int, int]]]:
    return [((x1, y1), (x2, y2)) for ((x1, y1), (x2, y2)) in lines
            if x1 == x2 or y1 == y2]


def get_dimensions(lines: List[Tuple[Tuple[int, int]]]) -> Tuple[int, int]:
    return (
        max((max([x1 for ((x1, _), _) in lines]),
             max([x2 for (_, (x2, _)) in lines]))) + 1,
        max((max([y1 for ((_, y1), _) in lines]),
             max([y2 for (_, (_, y2)) in lines]))) + 1
    )


def get_field(max_x: int, max_y: int) -> List[List[int]]:
    return [[0 for _ in range(max_y)] for _ in range(max_x)]


def mark_lines(lines: List[Tuple[Tuple[int, int]]],
               field: List[List[int]]) -> List[List[int]]:
    for (x1, y1), (x2, y2) in lines:
        if x1 == x2:
            x = [x1] * (abs(y1 - y2) + 1)
        else:
            if x1 < x2:
                x = range(x1, x2+1)
            else:
                x = range(x1, x2-1, -1)
        if y1 == y2:
            y = [y1] * (abs(x1 - x2) + 1)
        else:
            if y1 < y2:
                y = range(y1, y2+1)
            else:
                y = range(y1, y2-1, -1)
        for x_i, y_i in zip(x, y):
            field[x_i][y_i] += 1


def count_points(field: List[List[int]]) -> int:
    count = 0
    for row in field:
        for point in row:
            count += 1 if point > 1 else 0
    return count


if __name__ == "__main__":
    main()
