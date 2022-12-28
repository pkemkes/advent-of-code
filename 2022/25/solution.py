from math import log, floor
from typing import List

SNAFU_MAP = {"2": 2, "1": 1, "0": 0, "-": -1, "=": -2}
DEC_MAP = {v: k for k, v in SNAFU_MAP.items()}


def main():
    with open("input.txt") as f:
        snafu_nums = [line.strip() for line in f.readlines()]

    # #### Puzzle 1 #### #

    dec_nums = [snafu_to_dec(snafu_num) for snafu_num in snafu_nums]
    dec_sum = sum(dec_nums)
    print("Decimal sum of SNAFU numbers:", dec_sum)
    print("Which is in SNAFU:", dec_to_snafu(dec_sum))


def snafu_to_dec(snafu_num: str) -> int:
    return sum([SNAFU_MAP[c] * (5**i)
                for i, c in enumerate(reversed(snafu_num))])


def dec_to_snafu(dec_num: int) -> str:
    highest_exp = floor(log(dec_num, 5))
    result = [0 for _ in range(highest_exp+2)]
    for exp in range(highest_exp, -1, -1):
        if dec_num // (5**exp) > 2:
            result[exp+1] += 1
            result = check_and_adjust(result, exp+1)
            result[exp] = (dec_num // (5**exp)) - 5
        else:
            result[exp] = dec_num // (5**exp)
        dec_num %= 5**exp
    return "".join(reversed([DEC_MAP[d] for d in result])).lstrip("0")


def check_and_adjust(snafu_list: List[int], exp: int) -> List[int]:
    if snafu_list[exp] > 2:
        snafu_list[exp+1] += 1
        snafu_list[exp] = snafu_list[exp] - 5
        snafu_list = check_and_adjust(snafu_list, exp+1)
    return snafu_list


if __name__ == "__main__":
    main()
