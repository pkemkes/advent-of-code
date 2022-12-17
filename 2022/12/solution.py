from typing import List, Tuple, Set, Optional
from queue import Queue


def main():
    with open("input.txt") as f:
        input = [line.strip() for line in f.readlines()]

    # #### Puzzle 1 #### #

    start = find_char(input, "S")[0]
    length = find_shortest_path(start, input)
    print("Length of shortest path from 'S':", length)

    # #### Puzzle 2 #### #

    starts = find_char(input, "a")
    lengths = [find_shortest_path(start, input) for start in starts]
    print("Length of shortest path from any 'a':", min(lengths))


def find_char(input: List[str], char: str) -> Tuple[int, int]:
    char_positions = []
    for x in range(len(input[0])):
        for y in range(len(input)):
            if input[y][x] == char:
                char_positions.append((x, y))
    return char_positions


def find_shortest_path(start: Tuple[int, int],
                       input: List[str]) -> Optional[int]:
    q = Queue()
    q.put((start, 1))
    visited = set([start])
    while not q.empty():
        position = q.get()
        last_step = position[0]
        length = position[1]
        for x, y in possible_steps(last_step, visited, input):
            if input[y][x] == "E":
                return length
            else:
                visited.add(((x, y)))
                q.put(((x, y), length+1))
    return 999999  # return long length in case path is impossible


def possible_steps(last_step: Tuple[int, int], visited: Set[Tuple[int, int]],
                   input: List[str]) -> Set[Tuple[int, int]]:
    x, y = last_step
    return {
        (x_new, y_new) for x_new, y_new
        in [(x-1, y), (x+1, y), (x, y-1), (x, y+1)]
        if (
                x_new >= 0 and y_new >= 0 and
                x_new < len(input[0]) and y_new < len(input)
        ) and
        (x_new, y_new) not in visited and
        (
            (
                ord(input[y_new][x_new]) - ord(input[y][x]) < 2 and
                input[y_new][x_new] != "E"
            ) or
            (input[y_new][x_new] == "E" and input[y][x] == "z") or
            input[y][x] == "S"
        )
    }


if __name__ == "__main__":
    main()
