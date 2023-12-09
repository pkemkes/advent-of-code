from typing import List, Tuple

Card = Tuple[List[str]]

with open("input.txt") as f:
    input = [line.strip() for line in f.readlines()]


def preprocess_input(input: List[str]) -> List[Card]:
    cards = []
    for line in input:
        winning_numbers = [
            num.strip() for num in line.split(" | ")[0]
                                       .split(": ")[1]
                                       .split(" ")
            if num.strip() != ""
        ]
        numbers_we_have = [
            num.strip() for num in line.split(" | ")[1]
                                       .split(" ")
            if num.strip() != ""
        ]
        cards.append((winning_numbers, numbers_we_have))
    return cards


cards = preprocess_input(input)


def calculate_num_of_matches(card: Card) -> int:
    return len([num for num in card[1] if num in card[0]])


# #### Puzzle 1 #### #

def calculate_points(card: Card) -> int:
    matches = calculate_num_of_matches(card)
    if matches == 0:
        return 0
    return 2 ** (matches-1)


points = [calculate_points(card) for card in cards]
print("Total points:", sum(points))


# #### Puzzle 2 #### #

def count_cards(cards: List[Card]) -> int:
    number_of_cards = [1] * len(cards)
    for i, card in enumerate(cards):
        matches = calculate_num_of_matches(card)
        for j in range(matches):
            if i+j+1 >= len(number_of_cards):
                break
            number_of_cards[i+j+1] += number_of_cards[i]
    return sum(number_of_cards)


number_of_cards_after_playing = count_cards(cards)
print("Number of cards:", number_of_cards_after_playing)
