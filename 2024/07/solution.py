Equation = tuple[int, list[int]]


def perform_operation(curr_result: int, operator: str, value: int) -> int:
    if operator == "+":
        return curr_result + value
    elif operator == "*":
        return curr_result * value
    elif operator == "||":
        return int(str(curr_result) + str(value))
    else:
        raise Exception(f"Unknown operator {operator}")


def is_possible_result(equation: Equation, operators: list[str]):
    result, values = equation
    num_of_combinations = len(operators) ** len(values)
    for i in range(num_of_combinations):
        calc_result = values[0]
        for value in values[1:]:
            operator = operators[i % len(operators)]
            calc_result = perform_operation(calc_result, operator, value)
            if calc_result > result:
                break
            i = i // len(operators)
        if calc_result == result:
            return True
    return False


def calc_all_possible_results(
        equations: list[Equation], operators: list[str]
    ) -> list[int]:
    possible_results = []
    num_of_equations = len(equations)
    for i, equation in enumerate(equations):
        if (i+1) % 10 == 0:
            print(i+1, "/", num_of_equations)
        if is_possible_result(equation, operators):
            possible_results.append(equation[0])
    return possible_results


def main():
    with open("input.txt") as f:
        lines = [l.strip() for l in f.readlines()]
    
    equations = []
    for line in lines:
        left, right = line.split(":")
        result = int(left)
        values = [int(value.strip()) for value in right.strip().split(" ")]
        equations.append((result, values))

    operators = ["+", "*"]
    possible_results_2_ops = calc_all_possible_results(equations, operators)
    
    print(
        "Sum of possible results for + and *:", 
        sum(possible_results_2_ops)
    )

    operators.append("||")
    possible_results_3_ops = calc_all_possible_results(equations, operators)
    
    print(
        "Sum of possible results for +, * and ||:", 
        sum(possible_results_3_ops)
    )


if __name__ == "__main__":
    main()
