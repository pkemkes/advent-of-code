from typing import List
import re
import math


class Monkey:
    def __init__(self, items: List[int], operation: str,
                 test_div: int, true_monkey: int,
                 false_monkey: int, relief: bool, monkeys) -> None:
        self.items = items
        self.operation = operation
        self.test_div = test_div
        self.true_monkey = true_monkey
        self.false_monkey = false_monkey
        self.relief = relief
        self.monkeys: List[Monkey] = monkeys
        self.inspection_counter = 0

    def inspect_items(self):
        while len(self.items) > 0:
            self.inspection_counter += 1
            item = self.items.pop()
            item = self.modify(item)
            if self.relief:
                item = item // 3
            if item % self.test_div == 0:
                self.monkeys[self.true_monkey].catch(item)
            else:
                self.monkeys[self.false_monkey].catch(item)

    def modify(self, item: int) -> int:
        operator = self.operation.split(" ")[0]
        number = self.operation.split(" ")[1]
        if operator == "+":
            result = item + int(number)
        else:
            if number.isnumeric():
                result = item * int(number)
            else:
                result = item * item
        # we only need to check if the worry level is divisable
        # we don't care about the actual worry level
        # so using the modulo of the product of all divisors is enough
        return result % math.prod([m.test_div for m in self.monkeys])

    def catch(self, item: int):
        self.items.append(item)


def main():
    with open("input.txt") as f:
        input = f.read()

    # #### Puzzle 1 #### #

    monkeys = parse_monkeys(input, True)
    for _ in range(20):
        for m in monkeys:
            m.inspect_items()
    print("Monkey business with relief:", calc_monkey_business(monkeys))

    # #### Puzzle 2 #### #

    monkeys = parse_monkeys(input, False)
    for round in range(10000):
        for m in monkeys:
            m.inspect_items()
    print("Monkey business without relief:", calc_monkey_business(monkeys))


def parse_monkeys(input: List[str], relief: bool) -> List[Monkey]:
    monkeys = []
    for monkey_str in input.split("\n\n"):
        items = re.search(r"Starting items: ([^\n]+)\n",
                          monkey_str).groups()[0]
        items = list(map(int, items.split(", ")))
        operation = re.search(r"Operation: new = old ([^\n]+)\n",
                              monkey_str).groups()[0]
        test_div = int(re.search(r"Test: divisible by ([^\n]+)\n",
                                 monkey_str).groups()[0])
        true_monkey = int(re.search(r"If true: throw to monkey ([^\n]+)\n",
                                    monkey_str).groups()[0])
        false_monkey = int(re.search(r"If false: throw to monkey ([^\n]+)\n?",
                                     monkey_str).groups()[0])
        monkeys.append(Monkey(items, operation, test_div, true_monkey,
                              false_monkey, relief, monkeys))
    return monkeys


def calc_monkey_business(monkeys: List[Monkey]) -> int:
    counters = [m.inspection_counter for m in monkeys]
    counters = sorted(counters, reverse=True)
    return counters[0] * counters[1]


if __name__ == "__main__":
    main()
