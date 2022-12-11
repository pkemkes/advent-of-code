from typing import List, Tuple

PARA_MAP = {
    ")": "(",
    "]": "[",
    ">": "<",
    "}": "{"
}

INV_PARA_MAP = {v: k for k, v in PARA_MAP.items()}

ERROR_SCORE_MAP = {
    ")": 3,
    "]": 57,
    "}": 1197,
    ">": 25137
}

COMPL_SCORE_MAP = {
    ")": 1,
    "]": 2,
    "}": 3,
    ">": 4
}


def main():
    with open("input.txt") as f:
        input = [line.strip() for line in f.readlines()]

    # #### Puzzle 1 #### #

    bad_chars = find_bad_chars(input)
    print("Error score:", calc_error_score(bad_chars))

    # #### Puzzle 2 #### #

    compl_strings = find_compl_strings(input)
    print("Middle completion score:", calc_compl_score(compl_strings))


def find_bad_chars(input: List[str]) -> str:
    return "".join([check_corruption(line)[0] for line in input])


def check_corruption(line: str) -> Tuple[str, str]:
    stack = []
    for char in line:
        if char in "([<{":
            stack.append(char)
        else:
            last_char = stack.pop()
            if last_char != PARA_MAP[char]:
                return char, []
    stack.reverse()
    stack = [INV_PARA_MAP[p] for p in stack]
    return "", "".join(stack)


def find_compl_strings(input: List[str]) -> List[str]:
    compl_strings = []
    for line in input:
        compl_string = check_corruption(line)[1]
        if compl_string:
            compl_strings.append(compl_string)
    return compl_strings


def calc_error_score(bad_chars: str) -> int:
    return sum([ERROR_SCORE_MAP[char] for char in bad_chars])


def calc_compl_score(compl_strings: List[str]) -> int:
    scores = []
    for compl_string in compl_strings:
        score = 0
        for c in compl_string:
            score *= 5
            score += COMPL_SCORE_MAP[c]
        scores.append(score)
    scores.sort()
    return scores[len(scores)//2]


if __name__ == "__main__":
    main()
