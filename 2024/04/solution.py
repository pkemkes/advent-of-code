def get_c(x: int, y: int, puzzle: list[str]):
    if x >= len(puzzle[0]) or x < 0:
        return None
    if y >= len(puzzle) or y < 0:
        return None
    return puzzle[y][x]


def count_matches(x: int, y: int, puzzle: list[str]):
    string = "XMAS"
    matches = 0
    # right
    if all(string[i] == get_c(x+i, y, puzzle) for i in range(len(string))):
        matches += 1
    # left
    if all(string[i] == get_c(x-i, y, puzzle) for i in range(len(string))):
        matches += 1
    # down
    if all(string[i] == get_c(x, y+i, puzzle) for i in range(len(string))):
        matches += 1
    # up
    if all(string[i] == get_c(x, y-i, puzzle) for i in range(len(string))):
        matches += 1
    # up-right
    if all(string[i] == get_c(x+i, y-i, puzzle) for i in range(len(string))):
        matches += 1
    # up-left
    if all(string[i] == get_c(x-i, y-i, puzzle) for i in range(len(string))):
        matches += 1
    # down-right
    if all(string[i] == get_c(x+i, y+i, puzzle) for i in range(len(string))):
        matches += 1
    # down-left
    if all(string[i] == get_c(x-i, y+i, puzzle) for i in range(len(string))):
        matches += 1
    return matches


def main():
    with open("input.txt") as f:
        puzzle = [l.strip() for l in f.readlines()]
    
    occurrences = 0
    for y in range(len(puzzle)):
        for x in range(len(puzzle[0])):
            occurrences += count_matches(x, y, puzzle)

    print("Ocurrences:", occurrences)


if __name__ == "__main__":
    main()
