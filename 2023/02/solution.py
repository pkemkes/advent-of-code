from typing import Dict, List
from math import prod

Game = List[List[List[str]]]
Limits = Dict[str, int]

with open("input.txt") as f:
    input = [line.strip() for line in f.readlines()]
games = [line.split(": ")[1] for line in input]
games = [
    [
        [
            cube_amount.strip().split(" ")
            for cube_amount in subset.strip().split(",")
        ]
        for subset in game.strip().split(";")
    ]
    for game in games
]


# #### Puzzle 1 #### #

def could_be_played(limits: Limits, game: Game) -> bool:
    for subset in game:
        for cube_amount in subset:
            amount, color = int(cube_amount[0]), cube_amount[1]
            if amount > limits[color]:
                return False
    return True


def calc_sum_of_playable_ids(limits: Limits, games: List[Game]) -> int:
    return sum([i+1 for i, game in enumerate(games)
                if could_be_played(limits, game)])


print("Puzzle 1:", calc_sum_of_playable_ids(
    {"red": 12, "green": 13, "blue": 14}, games
))


# #### Puzzle 2 #### #

def calc_game_power(game: Game) -> int:
    highest_amounts = {"red": 0, "green": 0, "blue": 0}
    for subset in game:
        for cube_amount in subset:
            amount, color = int(cube_amount[0]), cube_amount[1]
            highest_amounts[color] = max(amount, highest_amounts[color])
    return prod(highest_amounts.values())


print("Puzzle 2:", sum([calc_game_power(game) for game in games]))
