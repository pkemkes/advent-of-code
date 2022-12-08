from typing import List


def main():
    with open("input.txt") as f:
        input = [int(line.strip()) for line in f.readlines()]

    # #### Puzzle 1 #### #

    incs = get_num_of_increases(input)
    print("Number of increases:", incs)

    # #### Puzzle 2 #### #
    
    sums = [sum(input[i:i+3]) for i in range(len(input)-2)]
    incs = get_num_of_increases(sums)
    print("Number of sliding window increases:", incs)


def get_num_of_increases(measurements: List[int]) -> int:
    increases = 0
    for i in range(1, len(measurements)):
        if measurements[i] > measurements[i-1]:
            increases += 1
    return increases


if __name__ == "__main__":
    main()
