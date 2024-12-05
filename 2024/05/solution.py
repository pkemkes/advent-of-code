from math import floor
from functools import cmp_to_key


def is_correct(update: list[int], rules_dict: dict[int, list[int]]) -> bool:
    for i in range(1, len(update)):
        for j in range(i+1):
            print_before_numbers = rules_dict.get(update[i], [])
            if update[j] in print_before_numbers:
                return False
    return True


def get_middle_number(update: list[int]) -> int:
    return update[floor(len(update)/2)]


def sort_update(update: list[int], rules_dict: dict[int, list[int]]) -> list[int]:
    return sorted(update, key=cmp_to_key(
        lambda left, right: -1 if right in rules_dict.get(left, []) else 0
    ))


def main():
    with open("input.txt") as f:
        raw_rules, raw_updates = f.read().split("\n\n")
    
    rules = [
        [int(elem) for elem in rule.split("|")] 
        for rule in raw_rules.split("\n")
        if rule != ""
    ]
    updates = [
        [int(elem) for elem in update.split(",")] 
        for update in raw_updates.split("\n")
        if update != ""
    ]

    rules_dict = {}
    for left, right in rules:
        if left not in rules_dict:
            rules_dict[left] = [right]
        else:
            rules_dict[left].append(right)
    
    middle_numbers = [
        get_middle_number(update)
        for update in updates 
        if is_correct(update, rules_dict)
    ]
    
    print("Sum of middle numbers of correct updates:", sum(middle_numbers))

    corrected_middle_numbers = [
        get_middle_number(sort_update(update, rules_dict))
        for update in updates 
        if not is_correct(update, rules_dict)
    ]
    
    print("Sum of middle numbers of corrected updates:", sum(corrected_middle_numbers))


if __name__ == "__main__":
    main()
