from typing import List, Tuple, Dict


NumberMonkeys = Dict[str, int]
MathMonkeys = Dict[str, List[int]]
ParsedMonkeys = Tuple[NumberMonkeys, MathMonkeys]

OPPOSITE_OPERATORS = {
    "+": "-",
    "-": "+",
    "*": "/",
    "/": "*"
}


def main():
    with open("input.txt") as f:
        input = [line.strip() for line in f.readlines()]
    number_monkeys, math_monkeys = parse_monkeys(input)

    # #### Puzzle 1 #### #

    root_num = eval_monkey_1("root", number_monkeys, math_monkeys)
    print("Monkey root yells", root_num)

    # #### Puzzle 2 #### #

    math_monkeys["root"][1] = "="
    equation = eval_monkey_2("root", number_monkeys, math_monkeys)
    humn = solve_for_x(equation)
    print("We need to yell", humn)


def parse_monkeys(input: List[str]) -> ParsedMonkeys:
    number_monkeys = {}
    math_monkeys = {}
    for line in input:
        name, job = line.split(": ")
        if job.isnumeric():
            number_monkeys[name] = int(job)
        else:
            math_monkeys[name] = job.split(" ")
    return number_monkeys, math_monkeys


def eval_monkey_1(monkey: str, number_monkeys: NumberMonkeys,
                  math_monkeys: MathMonkeys) -> int:
    if monkey in number_monkeys:
        return number_monkeys[monkey]
    else:
        monkey_a, operation, monkey_b = math_monkeys[monkey]
        number_a = eval_monkey_1(monkey_a, number_monkeys, math_monkeys)
        number_b = eval_monkey_1(monkey_b, number_monkeys, math_monkeys)
        return int(eval(f"{number_a} {operation} {number_b}"))


def eval_monkey_2(monkey: str, number_monkeys: NumberMonkeys,
                  math_monkeys: MathMonkeys) -> str:
    if monkey in number_monkeys:
        return str(number_monkeys[monkey]) if monkey != "humn" else "x"
    else:
        monkey_a, operation, monkey_b = math_monkeys[monkey]
        number_a = eval_monkey_2(monkey_a, number_monkeys, math_monkeys)
        number_b = eval_monkey_2(monkey_b, number_monkeys, math_monkeys)
        math = f"{number_a} {operation} {number_b}"
        return f"({math})" if monkey != "root" else math


def solve_for_x(equation: str) -> int:
    sides = equation.split(" = ")
    with_x = 0 if "x" in sides[0] else 1
    side_with_x, side_without_x = sides[with_x], sides[1-with_x]
    modified_for_x = modify_for_x(side_with_x, side_without_x)
    return int(eval(modified_for_x))


def modify_for_x(side_with_x: str, side_without_x: str) -> str:
    side_with_x = side_with_x[1:-1]
    while side_with_x != "x":
        splitted = split_at_operator(side_with_x)
        with_x_pos = 0 if "x" in splitted[0] else 2
        operator = splitted[1].strip()
        with_x, without_x = splitted[with_x_pos], splitted[2-with_x_pos]
        if operator in "/-" and with_x_pos == 2:
            side_without_x = "(" + without_x + operator + side_without_x + ")"
        else:
            side_without_x = "(" + side_without_x + \
                OPPOSITE_OPERATORS[operator] + without_x + ")"
        side_with_x = with_x[1:-1] if with_x.startswith("(") else with_x
    return side_without_x


def split_at_operator(math: str) -> List[str]:
    parantheses = 0
    splitted = ["" for _ in range(3)]
    pos = 0
    for c in math:
        if c in "()":
            parantheses += 1 if c == "(" else -1
        if pos == 0 and parantheses == 0 and c in "+-/* ":
            pos = 1
        elif pos == 1 and (c.isnumeric() or c in "(x"):
            pos = 2
        splitted[pos] += c
    return splitted


if __name__ == "__main__":
    main()
