import re

def main():
    with open("input.txt") as f:
        input = [l.strip() for l in f.readlines()]

    rucksacks = [(r[:(len(r)//2)], r[(len(r)//2):]) for r in input]

    # #### Puzzle 1 #### #

    total_score = sum([calc_error_score(r) for r in rucksacks])
    print("Total error score:", total_score)

    # #### Puzzle 2 #### #

    group_badges = get_group_badges(input)
    badges_score = sum([get_prio(b) for b in group_badges])
    print("Total badges score:", badges_score)


def calc_error_score(rucksack):
    (left, right) = rucksack
    for l in left:
        if l in right:
            return get_prio(l)


def get_group_badges(rucksacks):
    return [get_badge_from_group(rucksacks[i:i+3]) for i in range(0, len(rucksacks), 3)]


def get_badge_from_group(group):
    for l in group[0]:
        if l in group[1] and l in group[2]:
            return l


def get_prio(item):
    if re.match("[A-Z]", item):
        return ord(item) - 38
    elif re.match("[a-z]", item):
        return ord(item) - 96
    else:
        raise Exception(f"Illegal item: {item}")


if __name__ == "__main__":
    main()