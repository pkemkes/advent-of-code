from typing import List, Tuple


def main():
    with open("input.txt") as f:
        instructions = [line.strip().split(" ") for line in f.readlines()]

    # #### Puzzle 1 #### #

    instructions = normalize(instructions)
    register_states = execute(instructions)
    signal_strengths = calc_signal_strengths(register_states)
    print("Sum of signal strengths:", sum(signal_strengths))

    # #### Puzzle 2 #### #

    screen = draw(register_states)
    print("Resulting screen:")
    print(screen)


def normalize(instructions: List[Tuple]) -> List[Tuple]:
    normalized = []
    for instr in instructions:
        if instr[0] == "addx":
            normalized.append(("noop"))
        normalized.append(instr)
    return normalized


def execute(instructions: List[Tuple]) -> List[int]:
    register = 1
    register_states = [register]
    for instr in instructions:
        if instr[0] == "addx":
            register += int(instr[1])
        register_states.append(register)
    return register_states


def calc_signal_strengths(register_states: List[int]) -> List[int]:
    return [register_states[i] * (i+1)
            for i in range(19, len(register_states), 40)]


def draw(register_states: List[int]) -> str:
    screen = [["." for _ in range(40)] for _ in range(6)]
    for clk, reg in enumerate(register_states):
        if abs(reg - (clk % 40)) <= 1:
            screen[clk // 40][clk % 40] = "#"
    return "\n".join(["".join(line) for line in screen])


if __name__ == "__main__":
    main()
