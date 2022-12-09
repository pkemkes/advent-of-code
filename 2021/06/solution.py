from typing import List, Dict


def main():
    with open("input.txt") as f:
        fish_input = list(map(int, f.readline().strip().split(",")))

    # #### Puzzle 1 #### #

    fish = get_fish_dict(fish_input)
    for _ in range(80):
        fish = pass_day(fish)
    print("Number of fish after 80 days:", sum(fish.values()))

    # #### Puzzle 2 #### #

    fish = get_fish_dict(fish_input)
    for d in range(256):
        fish = pass_day(fish)
    print("Number of fish after 256 days:", sum(fish.values()))


def get_fish_dict(fish: List[int]) -> Dict[int, int]:
    fish_dict = {}
    for f in fish:
        if f in fish_dict:
            fish_dict[f] += 1
        else:
            fish_dict[f] = 1
    return fish_dict


def pass_day(fish: Dict[int, int]) -> Dict[int, int]:
    aged_fish = {}
    for age, number in fish.items():
        if age != 0:
            aged_fish[age-1] = number
    aged_fish[6] = fish.get(0, 0) + aged_fish.get(6, 0)
    aged_fish[8] = fish.get(0, 0)
    return aged_fish


if __name__ == "__main__":
    main()
