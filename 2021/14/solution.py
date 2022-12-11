from typing import List, Dict


def main():
    with open("input.txt") as f:
        template, rules = f.read().split("\n\n")
    rules = parse_rules(rules.split("\n"))

    # #### Puzzle 1 #### #

    counts = template_to_counts(template)
    for _ in range(10):
        counts = step(counts, rules)
    print("Most common minus least common after 10 steps:",
          calc_puzzle_result(counts, template))

    # #### Puzzle 2 #### #

    counts = template_to_counts(template)
    for _ in range(40):
        counts = step(counts, rules)
    print("Most common minus least common after 40 steps:",
          calc_puzzle_result(counts, template))


def parse_rules(rule_strings: List[str]) -> Dict[str, str]:
    rules = {}
    for rule_str in rule_strings:
        pair, insert = rule_str.split(" -> ")
        rules[pair] = insert
    return rules


def template_to_counts(template: str) -> Dict[str, int]:
    counts = {}
    for i in range(len(template)-1):
        pair = template[i:i+2]
        inc_or_set(pair, 1, counts)
    return counts


def step(counts: Dict[str, int], rules: Dict[str, str]) -> str:
    new_counts = {}
    for pair, count in counts.items():
        if pair in rules:
            insert = rules[pair]
            left_new_pair = pair[0] + insert
            right_new_pair = insert + pair[1]
            inc_or_set(left_new_pair, count, new_counts)
            inc_or_set(right_new_pair, count, new_counts)
        else:
            inc_or_set(pair, count, new_counts)
    return new_counts


def calc_puzzle_result(counts: Dict[str, int], template: str) -> int:
    char_counts = {}
    # We only need to count the last char, to avoid duplicates
    for pair, count in counts.items():
        inc_or_set(pair[1], count, char_counts)
    # In the end, just add the first char,
    # as this never changes, but was previously skipped
    inc_or_set(template[0], 1, char_counts)
    values = sorted(list(char_counts.values()))
    return values[-1] - values[0]


def inc_or_set(key: str, num: int, target: Dict[str, int]):
    if key in target:
        target[key] += num
    else:
        target[key] = num


if __name__ == "__main__":
    main()
