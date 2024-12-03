import re


def calc_mul_instruction(instruction):
    left, right = re.findall(r"\d+", instruction)
    return int(left) * int(right)


def main():
    with open("input.txt") as f:
        memory = "".join(f.readlines())
    
    multiplications = re.findall(r"mul\(\d+,\d+\)", memory)
    result = sum(calc_mul_instruction(mul) for mul in multiplications)
    
    print("result:", result)

    instructions = re.findall(r"mul\(\d+,\d+\)|do(?:n't)?\(\)", memory)
    result = 0
    enabled = True
    for instruction in instructions:
        if instruction.startswith("don't"):
            enabled = False
        elif instruction.startswith("do"):
            enabled = True
        elif instruction.startswith("mul") and enabled:
            result += calc_mul_instruction(instruction)
    
    print("second result:", result)

if __name__ == "__main__":
    main()
