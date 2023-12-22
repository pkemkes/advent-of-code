from typing import List, Tuple
from math import prod, sqrt, pow, floor, ceil


with open("input.txt") as f:
    lines = f.readlines()


def find_wait_times_for_distance(time_limit: int,
                                 distance: int) -> Tuple[int, int]:
    left = time_limit / 2
    right = sqrt(pow(time_limit, 2) - 4*distance) / 2
    return (left - right, left + right)


def calc_number_of_winning_wait_times(time_limit: int,
                                      distance: int) -> int:
    low, high = find_wait_times_for_distance(time_limit, distance)
    low, high = floor(low+1), ceil(high-1)
    return high - low + 1


# #### Puzzle 1 #### #

def extract_ints_from_line(line: str) -> List[int]:
    return [int(string.strip()) for string in line.split(" ")[1:]
            if string.strip() != ""]


time_limits = extract_ints_from_line(lines[0])
distances = extract_ints_from_line(lines[1])

number_of_winning_wait_times = [
    calc_number_of_winning_wait_times(t, d)
    for t, d in zip(time_limits, distances)
]
print("Number of winning wait times per round:", number_of_winning_wait_times)
print("Product of those:", prod(number_of_winning_wait_times))


# #### Puzzle 2 #### #

def extract_long_int_from_line(line: str) -> int:
    return int("".join([string.strip() for string in line.split(" ")[1:]
                        if string.strip() != ""]))


time_limit = extract_long_int_from_line(lines[0])
distance = extract_long_int_from_line(lines[1])

print(
    "Number of winning wait times in long race:",
    calc_number_of_winning_wait_times(time_limit, distance)
)
