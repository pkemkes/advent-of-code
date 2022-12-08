import re


def main():
    with open("input.txt") as f:
        input = [l[:-1] for l in f.readlines()]
    move_lines = input[10:]
    moves = get_moves_from_lines(move_lines)
    stack_lines = input[:8]

    # #### Puzzle 1 #### #

    stacks = get_stacks_from_lines(stack_lines)
    for move in moves:
        modify_stacks_with_move_single(stacks, move)
    top_level = [s[-1] for s in stacks]
    print("Top level of the stacks is:", "".join(top_level))

    # #### Puzzle 2 #### #

    stacks = get_stacks_from_lines(stack_lines)
    for move in moves:
        modify_stacks_with_move_multi(stacks, move)
    top_level = [s[-1] for s in stacks]
    print("Top level of the stacks is:", "".join(top_level))


def get_stacks_from_lines(stack_lines):
    stacks = [[] for _ in range(9)]
    for layer in reversed(stack_lines):
        for i in range(9):
            index = (i*4)+1
            if layer[index] != " ":
                stacks[i].append(layer[index])
    return stacks


def get_moves_from_lines(move_lines):
    moves = []
    for line in move_lines:
        matches = re.findall(r"move (\d+) from (\d+) to (\d+)", line)[0]
        if len(matches) != 3:
            raise Exception("Did not find enough matches")
        moves.append((int(matches[0]), int(matches[1])-1, int(matches[2])-1))
    return moves


def modify_stacks_with_move_single(stacks, move):
    amount, from_stack, to_stack = move
    for _ in range(amount):
        crate = stacks[from_stack].pop()
        stacks[to_stack].append(crate)


def modify_stacks_with_move_multi(stacks, move):
    amount, from_stack, to_stack = move
    moved = []
    for _ in range(amount):
        crate = stacks[from_stack].pop()
        moved.append(crate)
    stacks[to_stack] += list(reversed(moved))


if __name__ == "__main__":
    main()
