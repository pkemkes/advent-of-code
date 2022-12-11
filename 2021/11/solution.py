from typing import List


def main():
    with open("input.txt") as f:
        input = [line.strip() for line in f.readlines()]

    # #### Puzzle 1 #### #

    octopi = parse_octopi(input)
    flash_count = 0
    for _ in range(100):
        flash_count += step(octopi)
    print("Flash count after 100 steps:", flash_count)

    # #### Puzzle 1 #### #

    octopi = parse_octopi(input)
    step_num = 0
    while not is_sync(octopi):
        step(octopi)
        step_num += 1
    print(f"Synced after {step_num} steps")


def parse_octopi(input: List[str]) -> List[List[int]]:
    return [[int(o) for o in line] for line in input]


def step(octopi: List[List[int]]) -> int:
    for r in range(len(octopi)):
        for c in range(len(octopi[0])):
            octopi[r][c] += 1
    flashes = [[False for _ in row] for row in octopi]
    for r in range(len(octopi)):
        for c in range(len(octopi[0])):
            if octopi[r][c] > 9 and not flashes[r][c]:
                flash(r, c, octopi, flashes)
    for r in range(len(octopi)):
        for c in range(len(octopi[0])):
            if octopi[r][c] > 9:
                octopi[r][c] = 0
    flashes = [1 for f in sum(flashes, []) if f]
    return sum(flashes)


def flash(r: int, c: int, octopi: List[List[int]], flashes: List[List[bool]]):
    flashes[r][c] = True
    for r_i, c_i in [(r-1, c-1), (r-1, c), (r-1, c+1),
                     (r, c-1), (r, c+1),
                     (r+1, c-1), (r+1, c), (r+1, c+1)]:
        if r_i < 0 or r_i >= len(octopi) or c_i < 0 or c_i >= len(octopi[0]):
            continue
        octopi[r_i][c_i] += 1
        if octopi[r_i][c_i] > 9 and not flashes[r_i][c_i]:
            flash(r_i, c_i, octopi, flashes)


def is_sync(octopi: List[List[int]]) -> bool:
    return all([o == 0 for o in sum(octopi, [])])


if __name__ == "__main__":
    main()
