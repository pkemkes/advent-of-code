def main():
    with open("input.txt") as f:
        input = f.readline()

    # #### Puzzle 1 #### #

    marker = find_marker(input, 4)
    print("Packet marker at:", marker)

    # #### Puzzle 2 #### #

    marker = find_marker(input, 14)
    print("Message marker at:", marker)


def find_marker(input: str, length: int) -> int:
    for i, c in enumerate(input):
        if i < length-1:
            continue
        marker_list = input[i-(length-1):i+1]
        if len(marker_list) == len(set(marker_list)):
            return i + 1


if __name__ == "__main__":
    main()
