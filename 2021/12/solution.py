from typing import List, Dict


def main():
    with open("input.txt") as f:
        input = [line.strip() for line in f.readlines()]
    graph = parse_graph(input)

    # #### Puzzle 1 #### #

    unique_paths = get_unique_paths(graph, False)
    print(f"Found {len(unique_paths)} unique paths with every cave once.")

    # #### Puzzle 2 #### #

    unique_paths = get_unique_paths(graph, True)
    print(f"Found {len(unique_paths)} unique paths with one cave twice.")


def parse_graph(input: List[str]) -> Dict[str, List[str]]:
    graph = {}
    for cave_a, cave_b in [i.split("-") for i in input]:
        if cave_a in graph:
            graph[cave_a].append(cave_b)
        else:
            graph[cave_a] = [cave_b]
        if cave_b in graph:
            graph[cave_b].append(cave_a)
        else:
            graph[cave_b] = [cave_a]
    return graph


def get_unique_paths(graph: Dict[str, List[str]],
                     can_move_twice: bool) -> List[List[str]]:
    stack = [["start"]]
    finished = []
    while len(stack) > 0:
        path = stack.pop()
        cave = path[-1]
        if cave == "end":
            finished.append(path)
            continue
        neighbors = graph[cave]
        for n in neighbors:
            if can_move_to(n, path, can_move_twice):
                stack.append(path + [n])
    return finished


def can_move_to(cave: str, path: List[str], can_move_twice: bool) -> bool:
    return (
        not cave.islower() or
        cave == "end" or
        (
            cave not in ["start", "end"] and (
                cave not in path or
                (
                    every_small_cave_only_once_yet(path) and
                    can_move_twice
                )
            )
        )
    )


def every_small_cave_only_once_yet(path: List[str]) -> bool:
    small_caves = [c for c in path
                   if c.islower() and c not in ["start", "end"]]
    return len(small_caves) == len(set(small_caves))


if __name__ == "__main__":
    main()
