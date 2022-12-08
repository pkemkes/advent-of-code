def main():
    with open("input.txt") as f:
        input = [l.strip() for l in f.readlines()]

    # #### Puzzle 1 #### #

    number_of_fully_contained = sum([1 if is_fully_contained(pair) else 0 for pair in input])
    print("Number of fully contained pairs:", number_of_fully_contained)

    # #### Puzzle 2 #### #

    number_of_overlapping_pairs = sum([1 if overlap_eachother(pair) else 0 for pair in input])
    print("Number of overlapping pairs:", number_of_overlapping_pairs)


def overlap_eachother(pair):
    list1, list2 = get_lists_of_pair(pair)
    return len(set(list1+list2)) < len(list1+list2)


def is_fully_contained(pair):
    list1, list2 = get_lists_of_pair(pair)
    larger_one = list1 if len(list1) > len(list2) else list2
    return len(set(list1+list2)) == len(larger_one)


def get_lists_of_pair(pair):
    assignment1, assignment2 = pair.split(",")
    list1 = assignment_to_list(assignment1)
    list2 = assignment_to_list(assignment2)
    return list1, list2


def assignment_to_list(assignment):
    start, end = assignment.split("-")
    return list(range(int(start), int(end)+1))


if __name__ == "__main__":
    main()