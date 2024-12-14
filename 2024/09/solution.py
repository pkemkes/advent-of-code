from dataclasses import dataclass


@dataclass
class Block:
    id: int
    len: int


def parse(disk_map: list[int], use_blocks=False) -> list[int] | list[Block]:
    parsed = []
    is_file = True
    index = 0
    for entry in disk_map:
        length = int(entry)
        exp_entry = index if is_file else -1
        parsed += [Block(exp_entry, length)] if use_blocks else ([exp_entry] * length)
        if is_file:
            index += 1
        is_file = not is_file
    return parsed


def compact(parsed: list[int]) -> list[int]:
    front_cur = 0
    back_cur = len(parsed) - 1
    while front_cur < back_cur:
        if parsed[back_cur] == -1:
            back_cur -= 1
            continue
        if parsed[front_cur] == -1:
            parsed[front_cur] = parsed[back_cur]
            back_cur -= 1
        front_cur += 1
    compacted = parsed[:back_cur+1]
    return [entry for entry in compacted if entry != -1]


def compact_blocks(blocks: list[Block]) -> list[Block]:
    i_to_move = len(blocks) - 1
    while i_to_move > 0:
        if blocks[i_to_move].id != -1:
            i_target = 0
            while i_target < i_to_move:
                if blocks[i_target].id == -1 and blocks[i_target].len >= blocks[i_to_move].len:
                    to_move_len = blocks[i_to_move].len
                    target_len = blocks[i_target].len
                    blocks[i_target] = blocks[i_to_move]
                    blocks[i_to_move] = Block(-1, to_move_len)
                    if target_len > to_move_len:
                        blocks = blocks[:i_target+1] + [Block(-1, target_len - to_move_len)] + blocks[i_target+1:]
                        i_to_move + 1
                    break
                i_target += 1
        i_to_move -= 1
    return blocks


def calc_checksum(compacted: list[int]) -> int:
    return sum(i * entry for i, entry in enumerate(compacted))


def calc_block_checksum(blocks: list[Block]) -> int:
    result = 0
    index = 0
    for block in blocks:
        if block.id == -1:
            index += block.len
        else:
            for _ in range(block.len):
                result += index * block.id
                index += 1
    return result


def main():
    with open("input.txt") as f:
        disk_map = [int(c) for c in f.read().strip()]
    
    parsed = parse(disk_map)
    compacted = compact(parsed)
    checksum = calc_checksum(compacted)
    print("Checksum of compacted disk_map:", checksum)

    blocks = parse(disk_map, True)
    compated_blocks = compact_blocks(blocks)
    block_checksum = calc_block_checksum(compated_blocks)
    print("Checksum of compacted blocked disk_map:", block_checksum)


if __name__ == "__main__":
    main()
