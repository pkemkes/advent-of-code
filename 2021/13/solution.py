from typing import List, Tuple


def main():
    with open("input.txt") as f:
        input = f.read().split("\n\n")
    dots = [list(map(int, line.strip().split(",")))
            for line in input[0].split("\n")]
    folds = [line.strip().split("fold along ")[1]
             for line in input[1].split("\n")]
    folds = [(f.split("=")[0], int(f.split("=")[1])) for f in folds]

    # #### Puzzle 1 #### #

    paper = mark_dots(dots)
    paper = fold(folds[0][0], folds[0][1], paper)
    print("Dots after 1 fold:",
          sum([1 if c == "#" else 0 for c in sum(paper, [])]))

    # #### Puzzle 2 #### #

    paper = mark_dots(dots)
    paper = fold_all(folds, paper)
    print("Paper after folding:")
    for row in paper:
        print("".join(row))


def mark_dots(dots: List[Tuple[int, int]]) -> List[List[str]]:
    max_x = max([d[0] for d in dots])
    max_y = max([d[1] for d in dots])
    paper = [["." for _ in range(max_x+1)] for _ in range(max_y+1)]
    for x, y in dots:
        paper[y][x] = "#"
    return paper


def fold_all(folds: List[str], paper: List[List[str]]) -> List[List[str]]:
    for fold_instr in folds:
        paper = fold(*fold_instr, paper)
    return paper


def fold(dir: str, pos: int, paper: List[List[str]]) -> List[List[str]]:
    if dir == "x":
        new_paper = [row[:pos] for row in paper]
        for y in range(len(paper)):
            for x in range(pos+1, len(paper[0])):
                if paper[y][x] == "#":
                    new_paper[y][len(paper[0])-1-x] = "#"
    else:
        new_paper = [row for row in paper[:pos]]
        for y in range(pos+1, len(paper)):
            for x in range(len(paper[0])):
                if paper[y][x] == "#":
                    new_paper[len(paper)-1-y][x] = "#"
    return new_paper


if __name__ == "__main__":
    main()
