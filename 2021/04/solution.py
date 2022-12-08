from typing import List, Tuple
import re


def main():
    with open("input.txt") as f:
        input = [line.strip() for line in f.readlines()]
    draws = input[0].split(",")

    # #### Puzzle 1 #### #

    boards = parse_boards(input[1:])
    board, draw = get_win_board(draws, boards)
    print("Winning score:", get_score(board, draw))

    # #### Puzzle 2 #### #

    boards = parse_boards(input[1:])
    board, draw = get_last_board(draws, boards)
    print("Winning score:", get_score(board, draw))


def parse_boards(input: List[str]) -> List[List[List[List]]]:
    boards = []
    new_board = []
    for line in input:
        if not line:
            new_board = []
        else:
            numbers = re.findall(r"\d+", line)
            new_board.append([[n, 0] for n in numbers])
            if len(new_board) == 5:
                boards.append(new_board)
    return boards


def get_win_board(draws: List[str],
                  boards: List[List[List[List]]]) -> Tuple[List[List[List]],
                                                           str]:
    for draw in draws:
        mark_boards(draw, boards)
        bingoed_boards = [b for b in boards if is_bingo(b)]
        if len(bingoed_boards) > 1:
            raise Exception("More than one board won!")
        elif len(bingoed_boards) == 1:
            return bingoed_boards[0], draw


def get_last_board(draws: List[str],
                   boards: List[List[List[List]]]) -> Tuple[List[List[List]],
                                                            str]:
    boards_to_check = boards
    boards_won = []
    for draw in draws:
        mark_boards(draw, boards)
        for board in boards_to_check:
            if is_bingo(board):
                boards_won.append((board, draw))
        boards_to_check = [b for b in boards
                           if b not in [w[0] for w in boards_won]]
        if not boards_to_check:
            break
    return boards_won[-1]


def get_score(board: List[List[List]], draw: str) -> int:
    unmarked = sum([[c[0] for c in row if c[1] == 0] for row in board], [])
    return sum(map(int, unmarked)) * int(draw)


def mark_boards(draw: str, boards: List[List[List[List]]]):
    for board in boards:
        for row in board:
            for cell in row:
                if cell[0] == draw:
                    cell[1] = 1


def is_bingo(board: List[List[List]]) -> bool:
    for row in board:
        if all([cell[1] == 1 for cell in row]):
            return True
    for c in range(len(board[0])):
        if all([row[c][1] == 1 for row in board]):
            return True
    return False


if __name__ == "__main__":
    main()
