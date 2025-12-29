from queue import PriorityQueue
from time import sleep

Lab = list[str]
Coord = tuple[int, int]
PosAndDir = tuple[Coord, Coord]


def find_in_lab(c_to_find: str, lab: Lab) -> Coord:
    for y, row in enumerate(lab):
        for x, c in enumerate(row):
            if c == c_to_find:
                return (x, y)
    raise KeyError(f"Could not find {c_to_find} in the lab.")


def dist(from_pos: Coord, to_pos: Coord) -> int:
    from_x, from_y = from_pos
    to_x, to_y = to_pos
    return abs(to_x - from_x) + abs(to_y - from_y)


def is_in_lab(pos: Coord, lab: Lab) -> bool:
    len_x = len(lab[0])
    len_y = len(lab)
    x, y = pos
    return x >= 0 and y >= 0 and x < len_x and y < len_y


def find_steps(
        pos: Coord, dir: Coord, lab: Lab, visited: set[PosAndDir]
    ) -> list[tuple[int, Coord, Coord]]:
    x, y = pos
    steps = []
    for next_x, next_y in [(x+1, y), (x-1, y), (x, y+1), (x, y-1)]:
        next_pos = (next_x, next_y)
        next_dir = (next_x-x, next_y-y)
        if not is_in_lab((next_x, next_y), lab):
            continue
        if ((next_x, next_y), next_dir) in visited:
            continue
        if lab[next_y][next_x] not in [".", "E"]:
            continue
        if dir[0]+next_dir[0] == 0 and dir[1]+next_dir[1] == 0:
            continue
        next_visited = visited.union({(next_pos, next_dir)})
        if dir == next_dir:
            steps.append((0, next_pos, next_dir, next_visited))
        else:
            steps.append((1000, next_pos, next_dir, next_visited))
    return steps


def draw_lab(steps: set[PosAndDir], lab: Lab) -> str:
    dir_dict = {
        ( 0, -1): "^",
        ( 0,  1): "v",
        (-1,  0): "<",
        ( 1,  0): ">"
    }
    drawn_lab = [[c for c in row] for row in lab]
    for (x, y), dir in steps:
        drawn_lab[y][x] = dir_dict[dir]
    return "\n".join("".join(row) for row in drawn_lab) + "\n"


def find_cheapest_path(lab: Lab) -> int:
    start = find_in_lab("S", lab)
    end = find_in_lab("E", lab)
    q = PriorityQueue()
    q.put((0, start, (1, 0), set()))
    while not q.empty():
        costs, pos, dir, visited = q.get()
        # print(costs)
        # print(draw_lab(visited, lab))
        # sleep(0.1)
        steps = find_steps(pos, dir, lab, visited)
        for add_costs, next_pos, next_dir, next_visited in steps:
            next_costs = costs+add_costs+1
            if next_pos == end:
                return next_costs
            q.put((costs+add_costs+1, next_pos, next_dir, next_visited))


def main():
    with open("input.txt") as f:
        lab = [l.strip() for l in f.readlines()]
    
    costs = find_cheapest_path(lab)
    print("Costs of cheapest path:", costs)


if __name__ == "__main__":
    main()
