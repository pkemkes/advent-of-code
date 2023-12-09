from typing import List, Tuple
from math import prod

NUMBERS = "0123456789"

Schematic = List[str]
Coord = Tuple[int, int]
NumberCoordsCollection = List[List[Tuple[int, int]]]

with open("input.txt") as f:
    schematic = [line.strip() for line in f.readlines()]


# #### Puzzle 1 #### #

def is_part_number(schematic: Schematic, start_x: int, end_x: int,
                   curr_y: int) -> bool:
    to_check = [[(x, y) for x in range(start_x-1, end_x+2)
                 if x >= 0 and x < len(schematic[0])]
                for y in range(curr_y-1, curr_y+2)
                if y >= 0 and y < len(schematic)]
    to_check = [[schematic[y][x] for x, y in line] for line in to_check]
    to_check = sum(to_check, [])
    for char in to_check:
        if char not in NUMBERS + ".":
            return True
    return False


def extract_part_numbers(schematic: Schematic) -> List[int]:
    part_numbers = []
    for y, line in enumerate(schematic):
        num = ""
        start = 0
        for x, char in enumerate(line):
            if char in NUMBERS:
                if num == "":
                    start = x
                num += char
            if num != "" and (x == len(line)-1 or line[x+1] not in NUMBERS):
                if is_part_number(schematic, start, x, y):
                    part_numbers.append(int("".join(line[start:x+1])))
                num = ""
    return part_numbers


sum_of_part_numbers = sum(extract_part_numbers(schematic))
print("Sum of all part numbers:", sum_of_part_numbers)


# #### Puzzle 2 #### #

def extract_number_coords(schematic: Schematic,
                          start_x: int, y: int) -> List[Coord]:
    extracted_x = [start_x]
    next_l = start_x - 1
    while next_l >= 0 and schematic[y][next_l] in NUMBERS:
        extracted_x = [next_l] + extracted_x
        next_l -= 1
    next_r = start_x + 1
    while next_r < len(schematic[0]) and schematic[y][next_r] in NUMBERS:
        extracted_x.append(next_r)
        next_r += 1
    return [(x, y) for x in extracted_x]


def dedup_number_coords_collection(collection: NumberCoordsCollection
                                   ) -> NumberCoordsCollection:
    deduped = []
    for number_coords in collection:
        if number_coords not in deduped:
            deduped.append(number_coords)
    return deduped


def extract_surrounding_numbers(schematic: Schematic,
                                gear_x: int, gear_y: int) -> List[int]:
    potential_coords = sum([[(x, y) for x in [gear_x-1, gear_x, gear_x+1]]
                            for y in [gear_y-1, gear_y, gear_y+1]], [])
    potential_coords = [(x, y) for x, y in potential_coords
                        if x >= 0 and y >= 0
                        and x < len(schematic[0]) and x < len(schematic)
                        and schematic[y][x] in NUMBERS]
    number_coords_collection = [extract_number_coords(schematic, x, y)
                                for x, y in potential_coords]
    number_coords_collection = dedup_number_coords_collection(
        number_coords_collection
    )
    if len(number_coords_collection) != 2:
        return []
    return [int("".join([schematic[y][x] for x, y in number_coords]))
            for number_coords in number_coords_collection]


def extract_gear_ratios(schematic: Schematic) -> List[int]:
    gear_ratios = []
    for y, line in enumerate(schematic):
        for x, char in enumerate(line):
            if char == "*":
                numbers = extract_surrounding_numbers(schematic, x, y)
                if numbers:
                    gear_ratios.append(prod(numbers))
    return gear_ratios


sum_of_gear_ratios = sum(extract_gear_ratios(schematic))
print("Sum of all gear ratios:", sum_of_gear_ratios)
