from typing import Tuple
from functools import cmp_to_key

Round = Tuple[str, int]


with open("input.txt") as f:
    rounds = [line.strip().split(" ") for line in f.readlines()]
rounds = [(hand, int(bid)) for hand, bid in rounds]

# #### Puzzle 1 #### #

CARD_ORDER = ["2", "3", "4", "5", "6", "7", "8",
              "9", "T", "J", "Q", "K", "A"]


def get_type_rank_of_hand_without_joker(hand: str) -> int:
    occurrences = [0 for _ in range(len(CARD_ORDER))]
    for card in hand:
        occurrences[CARD_ORDER.index(card)] += 1
    if 5 in occurrences:
        return 6  # five of a kind
    if 4 in occurrences:
        return 5  # four of a kind
    if 3 in occurrences and 2 in occurrences:
        return 4  # full house
    if 3 in occurrences:
        return 3  # three of a kind
    if len([o for o in occurrences if o == 2]) == 2:
        return 2  # two pair
    if 2 in occurrences:
        return 1  # one pair
    return 0  # high card


get_type_rank_of_hand = get_type_rank_of_hand_without_joker


def compare_rounds(round_a: Round, round_b: Round) -> int:
    hand_a, _ = round_a
    hand_b, _ = round_b
    type_rank_a = get_type_rank_of_hand(hand_a)
    type_rank_b = get_type_rank_of_hand(hand_b)
    if type_rank_a != type_rank_b:
        return type_rank_a - type_rank_b
    for i in range(len(hand_a)):
        card_rank_a = CARD_ORDER.index(hand_a[i])
        card_rank_b = CARD_ORDER.index(hand_b[i])
        if card_rank_a != card_rank_b:
            return card_rank_a - card_rank_b
    return 0


sorted_rounds = sorted(rounds, key=cmp_to_key(compare_rounds),
                       reverse=True)
winnings = [(len(sorted_rounds) - i) * bid
            for i, (_, bid) in enumerate(sorted_rounds)]

print("Total winnings:", sum(winnings))


# #### Puzzle 2 #### #

def get_type_rank_of_hand_with_joker(hand: str) -> int:
    occurrences = [0 for _ in range(len(CARD_ORDER))]
    for card in hand:
        occurrences[CARD_ORDER.index(card)] += 1
    if max(occurrences[1:]) + occurrences[0] == 5:
        return 6  # five of a kind
    if max(occurrences[1:]) + occurrences[0] == 4:
        return 5  # four of a kind
    if 3 in occurrences and 2 in occurrences or \
       occurrences[0] == 1 and occurrences[1:].count(2) == 2 or \
       occurrences[0] == 2 and 2 in occurrences[1:] or \
       occurrences[0] == 3:
        return 4  # full house
    if max(occurrences[1:]) + occurrences[0] == 3:
        return 3  # three of a kind
    if occurrences.count(2) == 2 or \
       occurrences[0] == 1 and 2 in occurrences[1:] or \
       occurrences[0] == 2:
        return 2  # two pair
    if max(occurrences[1:]) + occurrences[0] == 2:
        return 1  # one pair
    return 0  # high card


CARD_ORDER = ["J", "2", "3", "4", "5", "6", "7",
              "8", "9", "T", "Q", "K", "A"]
get_type_rank_of_hand = get_type_rank_of_hand_with_joker

sorted_rounds = sorted(rounds, key=cmp_to_key(compare_rounds),
                       reverse=True)
winnings = [(len(sorted_rounds) - i) * bid
            for i, (_, bid) in enumerate(sorted_rounds)]

print("Total winnings with joken rule:", sum(winnings))
