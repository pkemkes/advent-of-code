from typing import List


def main():
    with open("input.txt") as f:
        input = [line.strip() for line in f.readlines()]

    # #### Puzzle 1 #### #

    print("Power consumption:", get_power_consumption(input))

    # #### Puzzle 2 #### #

    print("Life support rating:", get_life_supp_rating(input))


def get_power_consumption(bits: List[str]) -> int:
    most_common_bits = "".join([most_common_bit(i, bits)
                                for i in range(len(bits[0]))])
    least_common_bits = invert_bits(most_common_bits)
    gamma = int(most_common_bits, 2)
    epsilon = int(least_common_bits, 2)
    return gamma * epsilon


def get_life_supp_rating(bits: List[str]) -> int:
    oxy_gen_rating = get_oxy_gen_rating(bits)
    co2_scrub_rating = get_co2_scrub_rating(bits)
    return oxy_gen_rating * co2_scrub_rating


def invert_bits(bits: str) -> str:
    return "".join(["1" if bit == "0" else "0" for bit in bits])


def get_oxy_gen_rating(bits: List[str]) -> int:
    result_bits = bits
    pos = 0
    while len(result_bits) > 1:
        mcb = most_common_bit(pos, result_bits)
        mcb = "1" if mcb == "=" else mcb
        result_bits = [b for b in result_bits if b[pos] == mcb]
        pos += 1
    if len(result_bits) == 0:
        raise Exception("Removed too many bits!")
    return int(result_bits[0], 2)


def get_co2_scrub_rating(bits: List[str]) -> int:
    result_bits = bits
    pos = 0
    while len(result_bits) > 1:
        mcb = most_common_bit(pos, result_bits)
        lcb = "0" if mcb == "1" or mcb == "=" else "1"
        result_bits = [b for b in result_bits if b[pos] == lcb]
        pos += 1
    if len(result_bits) == 0:
        raise Exception("Removed too many bits!")
    return int(result_bits[0], 2)


def most_common_bit(pos: int, bits: List[str]) -> str:
    ones = 0
    zeros = 0
    for bit_row in bits:
        if bit_row[pos] == "1":
            ones += 1
        elif bit_row[pos] == "0":
            zeros += 1
        else:
            raise Exception(f"Unknown bit {bit_row[pos]}")
    return "1" if ones > zeros else "0" if zeros > ones else "="


if __name__ == "__main__":
    main()
