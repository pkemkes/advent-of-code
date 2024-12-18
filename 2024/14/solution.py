import re
from math import prod
from PIL import Image

Coord = tuple[int, int]


def parse_bot(bot_str: str) -> tuple[Coord]:
    match = re.match(r"p=(-?\d+),(-?\d+) v=(-?\d+),(-?\d+)", bot_str)
    return (int(match[1]), int(match[2])), (int(match[3]), int(match[4]))


def move_bot(pos: Coord, vel: Coord, len_x: int, len_y: int, steps=100) -> Coord:
    x, y = pos
    add_x, add_y = vel
    moved_x = (x + (add_x*steps)) % len_x
    moved_y = (y + (add_y*steps)) % len_y
    return moved_x, moved_y


def calc_safety_factor(bots: list[Coord], len_x: int, len_y: int) -> int:
    quadrant_counts = [0, 0, 0, 0]
    for x, y in bots:
        if x < len_x // 2:
            if y < len_y // 2:
                quadrant_counts[0] += 1
            elif y > len_y // 2:
                quadrant_counts[1] += 1
        elif x > len_x // 2:
            if y < len_y // 2:
                quadrant_counts[2] += 1
            elif y > len_y // 2:
                quadrant_counts[3] += 1
    return prod(quadrant_counts)


def draw_map(bots: list[Coord], len_x: int, len_y: int) -> list[str]:
    drawn_map = [[0 for _ in range(len_x)] for _ in range(len_y)]
    for x, y in bots:
        drawn_map[y][x] += 1
    return [
        "".join("." if c == 0 else str(c) for c in row)
        for row in drawn_map
    ]


def store_image(
        bots: list[Coord], len_x: int, len_y: int, name: str
    ) -> None:
    image = Image.new("RGB", (len_x, len_y))
    for bot in bots:
        image.putpixel(bot, (255, 255, 255, 255))
    image = image.resize((len_x*4, len_y*4), Image.Resampling.BOX)
    image.save(name + ".png")


def all_bots_unique(bots: list[Coord]) -> bool:
    return len(set(bots)) == len(bots)


def main():
    with open("input.txt") as f:
        size, bots = f.read().strip().split("\n\n")
    
    len_x, len_y = [int(l) for l in size.strip().split(",")]
    bot_info = [parse_bot(bot) for bot in bots.strip().split("\n")]
    moved_bots = [
        move_bot(pos, vel, len_x, len_y) for pos, vel in bot_info
    ]
    safety_factor = calc_safety_factor(moved_bots, len_x, len_y)

    print("Safety factor:", safety_factor)

    for i in range(1000000):
        if (i+1) % 100000 == 0:
            print(i+1)
        bot_info = [
            (move_bot(pos, vel, len_x, len_y, 1), vel) 
            for pos, vel in bot_info
        ]
        bots = [pos for pos, _ in bot_info]
        if all_bots_unique(bots):
            print(i + 1, "hat all unique positions!")
            drawn_map = draw_map(bots, len_x, len_y)
            for row in drawn_map:
                print(row)
            print()
            break


if __name__ == "__main__":
    main()
