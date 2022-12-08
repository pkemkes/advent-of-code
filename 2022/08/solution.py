from typing import List
from itertools import product


def main():
    with open("input.txt") as f:
        input = [line.strip() for line in f.readlines()]
    trees = text_to_trees(input)

    # #### Puzzle 1 #### #

    visible_count = outer_count(trees) + inner_visible_count(trees)
    print("Number of visible trees:", visible_count)

    # #### Puzzle 2 #### #

    scenic_scores = calc_scenic_scores(trees)
    print("Highest scenic score:", max(scenic_scores))


def outer_count(trees: List[List[int]]) -> int:
    return len(trees)*2 + (len(trees[0])-2)*2


def inner_visible_count(trees: List[List[int]]) -> int:
    count = 0
    for row in range(1, len(trees) - 1):
        for col in range(1, len(trees[0]) - 1):
            count += 1 if is_visible(row, col, trees) else 0
    return count


def is_visible(row: int, col: int, trees: List[List[int]]) -> bool:
    curr_tree = trees[row][col]
    from_top = all([trees[r][col] < curr_tree
                    for r in range(row-1, -1, -1)])
    from_bottom = all([trees[r][col] < curr_tree
                       for r in range(row+1, len(trees))])
    from_left = all([trees[row][c] < curr_tree
                     for c in range(col-1, -1, -1)])
    from_right = all([trees[row][c] < curr_tree
                      for c in range(col+1, len(trees[row]))])
    return from_top or from_bottom or from_left or from_right


def calc_scenic_scores(trees: List[List[int]]) -> List[int]:
    return [get_scenic_score(r, c, trees)
            for r, c in product(range(len(trees)), range(len(trees[0])))]


def get_scenic_score(row: int, col: int, trees: List[List[int]]) -> int:
    if row == 0 or row == len(trees) or col == 0 or col == len(trees[0]):
        return 0
    main_tree = trees[row][col]
    top = calc_scenic_score(main_tree, [trees[r][col]
                            for r in range(row-1, -1, -1)])
    bottom = calc_scenic_score(main_tree, [trees[r][col]
                               for r in range(row+1, len(trees))])
    left = calc_scenic_score(main_tree, [trees[row][c]
                             for c in range(col-1, -1, -1)])
    right = calc_scenic_score(main_tree, [trees[row][c]
                              for c in range(col+1, len(trees[row]))])
    return top * bottom * left * right


def calc_scenic_score(main_tree: int, other_trees: List[int]) -> List[int]:
    count = 0
    for t in other_trees:
        count += 1
        if t >= main_tree:
            break
    return count


def text_to_trees(input: List[str]) -> List[List[int]]:
    return [[int(i) for i in row] for row in input]


if __name__ == "__main__":
    main()
