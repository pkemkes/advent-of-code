from typing import List, Callable


with open("input.txt") as f:
    input = [line.strip() for line in f.readlines()]


digits = "123456789"


def extract_sum_of_digits(extract: Callable[[str], List[str]]) -> int:
    values = []
    for line in input:
        relevant_elems = extract(line)
        values.append(int(relevant_elems[0] + relevant_elems[-1]))
    return sum(values)


# #### Puzzle 1 #### #

print("Puzzle 1:", extract_sum_of_digits(
    lambda line: [c for c in line if c in digits]
))


# #### Puzzle 2 #### #

def extract_all_numbers(line: str) -> List[str]:
    numbers = [
        "one", "two", "three", "four", "five",
        "six", "seven", "eight", "nine"
    ]
    digits_by_strings = {d: d for d in digits}
    digits_by_strings.update({n: d for n, d in zip(numbers, digits)})
    extracted = []
    for i in range(len(line)):
        for string in digits_by_strings:
            if line[i:].startswith(string):
                extracted.append(digits_by_strings[string])
    return extracted


print("Puzzle 2:", extract_sum_of_digits(extract_all_numbers))
