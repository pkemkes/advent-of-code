from typing import List, Tuple, Set, Optional


Coord = Tuple[int, int]


class Elf:
    def __init__(self, x: int, y: int) -> None:
        self.x, self.y = (x, y)
        self.proposed = None

    def coord_in_dir(self, direction: str = "") -> None:
        if direction == "N":
            return (self.x, self.y-1)
        if direction == "S":
            return (self.x, self.y+1)
        if direction == "W":
            return (self.x-1, self.y)
        if direction == "E":
            return (self.x+1, self.y)

    def propose(self, pos: Optional[Coord] = None):
        self.proposed = pos

    def move_to_proposed(self):
        self.x, self.y = self.proposed

    def pos_in_direction(self, direction: str) -> Set[Coord]:
        if direction == "N":
            return {
                (self.x-1, self.y-1),
                (self.x, self.y-1),
                (self.x+1, self.y-1)
            }
        if direction == "S":
            return {
                (self.x-1, self.y+1),
                (self.x, self.y+1),
                (self.x+1, self.y+1)
            }
        if direction == "W":
            return {
                (self.x-1, self.y-1),
                (self.x-1, self.y),
                (self.x-1, self.y+1)
            }
        if direction == "E":
            return {
                (self.x+1, self.y-1),
                (self.x+1, self.y),
                (self.x+1, self.y+1)
            }

    def all_surrounding(self) -> Set[Coord]:
        return {
            (self.x+1, self.y+1),
            (self.x, self.y+1),
            (self.x-1, self.y+1),
            (self.x+1, self.y),
            (self.x-1, self.y),
            (self.x+1, self.y-1),
            (self.x, self.y-1),
            (self.x-1, self.y-1),
        }


def main():
    with open("input.txt") as f:
        input = [line.strip() for line in f.readlines()]

    # #### Puzzle 1 #### #

    elves = parse_elves(input)
    shuffle(elves, 10)
    print("Amount of empty ground tiles:", calc_empty_ground_tiles(elves))

    # #### Puzzle 2 #### #

    elves = parse_elves(input)
    shuffle(elves, None, True)


def parse_elves(input: List[str]) -> List[Elf]:
    elves = []
    for y, line in enumerate(input):
        for x, c in enumerate(line):
            if c == "#":
                elves.append(Elf(x, y))
    return elves


def shuffle(elves: List[Elf], iterations: Optional[int],
            break_if_not_moved: bool = False):
    directions = ["N", "S", "W", "E"]
    positions = {(e.x, e.y) for e in elves}
    iteration = 0
    while break_if_not_moved or iteration < iterations:
        if (iteration+1) % 10 == 0:
            print("Iteration:", iteration + 1)
        dir_prio = directions[iteration % 4:] + directions[:iteration % 4]
        propositions = set()
        blocked_props = set()
        for elf in elves:
            if no_one_around(elf, positions):
                elf.propose()  # don't move
                continue
            did_propose = False
            for direction in dir_prio:
                if all(pos not in positions
                       for pos in elf.pos_in_direction(direction)):
                    pos = elf.coord_in_dir(direction)
                    if pos not in propositions:
                        elf.propose(pos)
                        did_propose = True
                        propositions.add(pos)
                    else:
                        blocked_props.add(pos)
                    break
            if not did_propose:
                elf.propose()
        for elf in [e for e in elves if e.proposed is not None and
                    e.proposed not in blocked_props]:
            elf.move_to_proposed()
        new_positions = {(e.x, e.y) for e in elves}
        if positions == new_positions and break_if_not_moved:
            print(f"No elf moved after round {iteration+1}")
            break
        positions = new_positions
        iteration += 1


def no_one_around(elf: Elf, elf_positions: Set[Coord]) -> bool:
    return all(pos not in elf_positions for pos in elf.all_surrounding())


def calc_empty_ground_tiles(elves: List[Elf]):
    min_x = min([e.x for e in elves])
    max_x = max([e.x for e in elves])
    min_y = min([e.y for e in elves])
    max_y = max([e.y for e in elves])
    return (max_x - min_x + 1) * (max_y - min_y + 1) - len(elves)


if __name__ == "__main__":
    main()
