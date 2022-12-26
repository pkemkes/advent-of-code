from typing import List


def main():
    with open("input.txt") as f:
        encrypted = [int(line.strip()) for line in f.readlines()]

    # #### Puzzle 1 #### #

    decrypted = mix(encrypted)
    print("Sum of grove coordinates:", sum(get_grove_coordinates(decrypted)))

    # #### Puzzle 2 #### #

    enc_with_key = [e * 811589153 for e in encrypted]
    dec_with_key = mix(enc_with_key, 10)
    print("Sum of grove coordinates using key and mixing 10 times:",
          sum(get_grove_coordinates(dec_with_key)))


def mix(encrypted: List[int], iterations: int = 1) -> List[int]:
    positions = list(range(len(encrypted)))
    for _ in range(iterations):
        for i, number in enumerate(encrypted):
            current_pos = positions.index(i)
            positions = positions[:current_pos] + positions[current_pos+1:]
            new_pos = (current_pos + number) % len(positions)
            if new_pos != 0:
                positions = positions[:new_pos] + [i] + positions[new_pos:]
            else:
                positions = positions + [i]
    return [encrypted[i] for i in positions]


def get_grove_coordinates(decrypted: List[int]) -> List[int]:
    zero_position = decrypted.index(0)
    coord_positions = [(i*1000 + zero_position) % len(decrypted)
                       for i in range(1, 4)]
    return [decrypted[pos] for pos in coord_positions]


if __name__ == "__main__":
    main()
