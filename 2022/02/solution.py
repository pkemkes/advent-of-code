from enum import Enum


def main():
    with open("input.txt") as f:
        input = [l.strip() for l in f.readlines()]

    # #### Puzzle 1 #### #

    p1_map = {"X": "A", "Y": "B", "Z": "C"}
    rounds = [(r.split(" ")[0], r.split(" ")[1]) for r in input]
    p1_parsed_rounds = [(o, p1_map[m]) for (o, m) in rounds]
    p1_total_points = sum([calc_points(*r) for r in p1_parsed_rounds])
    print("P1 Total points:", p1_total_points)

    # #### Puzzle 2 #### #

    p2_win_map = {"A": "B", "B": "C", "C": "A"}
    p2_lose_map = {"A": "C", "B": "A", "C": "B"}
    p2_parsed_rounds = []
    for (o, m) in rounds:
        if m == "X":
            p2_parsed_rounds.append((o, p2_lose_map[o]))
        elif m == "Y":
            p2_parsed_rounds.append((o, o))
        else:
            p2_parsed_rounds.append((o, p2_win_map[o]))
    p2_total_points = sum([calc_points(*r) for r in p2_parsed_rounds])
    print("P2 Total points:", p2_total_points)


def calc_points(o, m):
    points = 0
    if m == "A":
        points += 1
    elif m == "B":
        points += 2
    else:
        points += 3
    result = result_of_round((o, m))
    # print(f"{o} vs. {m} -> {points+result}")
    return points + result


def result_of_round(round):
    if round in [("A", "B"), ("B", "C"), ("C", "A")]:
        return 6
    elif round[0] == round[1]:
        return 3
    else:
        return 0


if __name__ == "__main__":
    main()