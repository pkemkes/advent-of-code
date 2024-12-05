def check_occurrence(
        word_to_find: str, direction: tuple[int, int], 
        position: tuple[int, int], puzzle: list[str]
    ) -> int:
    len_x = len(puzzle[0])
    len_y = len(puzzle)
    x, y = position
    for c in range(len(word_to_find)):
        new_x, new_y = x + direction[0]*c, y + direction[1]*c
        if new_x < 0 or new_x >= len_x or new_y < 0 or new_y >= len_y:
            return False
        if puzzle[new_y][new_x] != word_to_find[c]:
            return False
    return True


def count_xmas_occurrences(puzzle: list[str]) -> int:
    word_to_find = "XMAS"
    directions = [
        (0, 1), (1, 0), (0, -1), (-1, 0),
        (1, 1), (-1, 1), (1, -1), (-1, -1)
    ]
    occurrences = 0
    for x in range(len(puzzle[0])):
        for y in range(len(puzzle)):
            for direction in directions:
                if check_occurrence(word_to_find, direction, (x, y), puzzle):
                    occurrences += 1
    return occurrences


def count_x_mas_occurrences(puzzle: list[str]) -> int:
    words_to_find = [
        ("MAS", "MAS"),
        ("MAS", "SAM"),
        ("SAM", "MAS"),
        ("SAM", "SAM")
    ]
    occurrences = 0
    for x in range(len(puzzle[0]) - 2):
        for y in range(len(puzzle) - 2):
            for top_word, bottom_word in words_to_find:
                if (
                    check_occurrence(top_word, (1, 1), (x, y), puzzle) and
                    check_occurrence(bottom_word, (1, -1), (x, y+2), puzzle)
                ):
                    occurrences += 1
    return occurrences

def main():
    with open("input.txt") as f:
        puzzle = [l.strip() for l in f.readlines()]

    print("XMAS ocurrences:", count_xmas_occurrences(puzzle))
    print("X-MAS ocurrences:", count_x_mas_occurrences(puzzle))


if __name__ == "__main__":
    main()
