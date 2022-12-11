from typing import List, Tuple, Dict


def main():
    with open("input.txt") as f:
        input = [line.strip().split(" | ") for line in f.readlines()]
    input = split_and_sort(input)

    # #### Puzzle 1 #### #

    digits = count_uniques(input)
    print("Number of 1s, 4s, 7s and 8s in output:", sum(sum(digits, [])))

    # #### Puzzle 2 #### #

    maps = deduce_maps(input)
    sum_of_outputs = sum(parse_outputs(maps, [i[1] for i in input]))
    print("Sum of outputs:", sum_of_outputs)


def split_and_sort(input: List[Tuple[str, str]])\
        -> List[Tuple[List[str], List[str]]]:
    res = []
    for i, o in input:
        left = ["".join(sorted(d)) for d in i.split(" ")]
        right = ["".join(sorted(d)) for d in o.split(" ")]
        res.append((left, right))
    return res


def count_uniques(input: List[Tuple[str, str]]) -> int:
    return [
        [1 if len(d) in [2, 4, 3, 7] else 0 for d in line[1]]
        for line in input
    ]


def deduce_maps(input: List[Tuple[str, str]]) -> List[Dict[int, str]]:
    return [deduce_map(test_numbers) for test_numbers, _ in input]


def deduce_map(numbers: List[str]) -> Dict[int, str]:
    n_map = {}
    parse_uniques(numbers, n_map)
    for n in numbers:
        if (
            distance(n, n_map.get(8)) == 1 and
            distance(n, n_map.get(4)) == 4 and
            distance(n, n_map.get(7)) == 3
        ):
            n_map[0] = n
        elif (
            distance(n, n_map.get(8)) == 2 and
            distance(n, n_map.get(4)) == 5
        ):
            n_map[2] = n
        elif (
            distance(n, n_map.get(8)) == 2 and
            distance(n, n_map.get(1)) == 3
        ):
            n_map[3] = n
        elif (
            distance(n, n_map.get(8)) == 2 and
            distance(n, n_map.get(4)) == 3
        ):
            n_map[5] = n
        elif (
            distance(n, n_map.get(8)) == 1 and
            distance(n, n_map.get(4)) == 4 and
            distance(n, n_map.get(7)) == 5
        ):
            n_map[6] = n
        elif (
            distance(n, n_map.get(8)) == 1 and
            distance(n, n_map.get(4)) == 2
        ):
            n_map[9] = n
    if len(n_map.keys()) != 10:
        raise Exception("Could not parse all numbers.")
    n_map = {v: k for k, v in n_map.items()}
    return n_map


def parse_uniques(numbers: List[str], number_map: Dict[int, str]):
    for n in numbers:
        if len(n) == 2:
            number_map[1] = n
        elif len(n) == 4:
            number_map[4] = n
        elif len(n) == 3:
            number_map[7] = n
        elif len(n) == 7:
            number_map[8] = n
    if len(number_map.keys()) != 4:
        raise Exception("Could not find all uniques!")


def distance(a: str, b: str) -> int:
    if not a or not b:
        return -1
    distance = 0
    for segment in a:
        if segment not in b:
            distance += 1
    for segment in b:
        if segment not in a:
            distance += 1
    return distance


def parse_outputs(n_maps: List[Dict[int, str]],
                  outputs: List[List[str]]) -> List[int]:
    parsed_outputs = []
    for n_map, output in zip(n_maps, outputs):
        digits = [n_map[n] for n in output]
        parsed_outputs.append(int("".join(map(str, digits))))
    return parsed_outputs


if __name__ == "__main__":
    main()
