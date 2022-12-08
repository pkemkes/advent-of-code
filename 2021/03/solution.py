from typing import List, Tuple


def main():
    with open("input.txt") as f:
        input = [line.strip() for line in f.readlines()]

    # #### Puzzle 1 #### #

    gamma, epsilon = get_gamma_and_epsilon(input)
    print("Power consumption:", gamma * epsilon)


def get_gamma_and_epsilon(bits: List[str]) -> Tuple[int, int]:
    summed = [0] * len(bits[0])
    for report in bits:
        summed = [summed[i] + int(report[i]) for i in range(len(report))]
    means = [s / len(bits) for s in summed]
    gamma_list = [round(m) for m in means]
    gamma = int("".join(map(str, gamma_list)), 2)
    epsilon_list = [1 - g for g in gamma_list]
    epsilon = int("".join(map(str, epsilon_list)), 2)
    return gamma, epsilon


if __name__ == "__main__":
    main()