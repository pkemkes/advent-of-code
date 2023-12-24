from typing import List


def get_val_histories() -> List[List[int]]:
    with open("input.txt") as f:
        return [[int(val) for val in line.strip().split(" ")]
                for line in f.readlines()]


def calc_differences(val_history: List[int]) -> List[int]:
    return [val_history[i] - val_history[i-1]
            for i in range(1, len(val_history))]


# #### Puzzle 1 #### #

def extrapolate_back(val_history: List[int]) -> int:
    differences = [val_history]
    while not all(d == 0 for d in differences[-1]):
        differences.append(calc_differences(differences[-1]))
    differences[-1].append(0)
    for i in range(len(differences)-1, -1, -1):
        differences[i-1].append(
            differences[i][-1] + differences[i-1][-1]
        )
    return differences[0][-1]


val_histories = get_val_histories()
extrapolations = [extrapolate_back(vh) for vh in val_histories]
print("Sum of extrapolated values at back:",
      sum(extrapolations))


# #### Puzzle 2 #### #


def extrapolate_front(val_history: List[int]) -> int:
    differences = [val_history]
    while not all(d == 0 for d in differences[-1]):
        differences.append(calc_differences(differences[-1]))
    differences[-1].insert(0, 0)
    for i in range(len(differences)-1, -1, -1):
        differences[i-1].insert(
            0,
            differences[i-1][0] - differences[i][0]
        )
    return differences[0][0]


val_histories = get_val_histories()
extrapolations = [extrapolate_front(vh) for vh in val_histories]
print("Sum of extrapolated values at front:",
      sum(extrapolations))
