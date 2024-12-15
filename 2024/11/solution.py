from math import floor, log10


def add_to_numbers(numbers: dict[int, int], number: int, amount: int):
    if number in numbers:
        numbers[number] += amount
    else:
        numbers[number] = amount


def blink(numbers: dict[int, int]) -> dict[int, int]:
    blinked = {}
    for number, amount in numbers.items():
        if number == 0:
            add_to_numbers(blinked, 1, amount)
        else:
            length = floor(log10(number)) + 1
            if length % 2 == 0:
                divider = 10 ** (length // 2)
                add_to_numbers(blinked, number // divider, amount)
                add_to_numbers(blinked, number % divider, amount)
            else:
                add_to_numbers(blinked, number * 2024, amount)
    return blinked


def main():
    with open("input.txt") as f:
        numbers_list = [int(number) for number in f.read().strip().split(" ")]

    numbers = {}
    for number in numbers_list:
        add_to_numbers(numbers, number, 1)
    
    for _ in range(25):
        numbers = blink(numbers)
    
    print("Number of stones after 25 blinks:", sum(numbers.values()))

    for _ in range(50):
        numbers = blink(numbers)
    
    print("Number of stones after 75 blinks:", sum(numbers.values()))


if __name__ == "__main__":
    main()
