from typing import List, Optional


def main():
    with open("input.txt") as f:
        input = f.read()
    pairs = [pair.strip().split("\n") for pair in input.split("\n\n")]
    pairs = [[split_list(left), split_list(right)] for left, right in pairs]

    # #### Puzzle 1 #### #

    correct_order = [is_correct_order(left, right) for left, right in pairs]
    indices = [i+1 for i in range(len(correct_order)) if correct_order[i]]
    print("Sum of indices of pairs with correct order:", sum(indices))

    # #### Puzzle 2 #### #

    divider_packets = [split_list("[[2]]"), split_list("[[6]]")]
    all_packets = sort(sum(pairs, []) + divider_packets)
    divider_indices = [i+1 for i in range(len(all_packets))
                       if all_packets[i] in divider_packets]
    print("Product of indices of divider packets:",
          divider_indices[0] * divider_indices[1])


def is_correct_order(left: List[str], right: List[str]) -> Optional[bool]:
    for i in range(min((len(left), len(right)))):
        cmp_res = None
        if left[i].isnumeric() and right[i].isnumeric():
            if int(left[i]) < int(right[i]):
                cmp_res = True
            if int(left[i]) > int(right[i]):
                cmp_res = False
        elif left[i].startswith("[") and right[i].startswith("["):
            cmp_res = is_correct_order(split_list(left[i]),
                                       split_list(right[i]))
        elif left[i].startswith("[") and right[i].isnumeric():
            cmp_res = is_correct_order(split_list(left[i]),
                                       split_list(f"[{right[i]}]"))
        elif left[i].isnumeric() and right[i].startswith("["):
            cmp_res = is_correct_order(split_list(f"[{left[i]}]"),
                                       split_list(right[i]))
        if cmp_res is not None:
            return cmp_res
    if len(left) < len(right):
        return True
    if len(left) > len(right):
        return False
    return None


def split_list(data: str) -> List[str]:
    result = []
    curr_elem = ""
    parantheses = 0
    for i in range(1, len(data)-1):
        if data[i] == "[":
            parantheses += 1
        elif data[i] == "]":
            parantheses -= 1
        if data[i] == "," and parantheses == 0:
            result.append(curr_elem)
            curr_elem = ""
        else:
            curr_elem += data[i]
    if curr_elem:
        result.append(curr_elem)
    return result


def sort(packets: List[List[str]]) -> List[List[str]]:
    sorted = []
    for packet in packets:
        found = False
        for s in range(len(sorted)):
            if not is_correct_order(sorted[s], packet):
                sorted = sorted[:s] + [packet] + sorted[s:]
                found = True
                break
        if not found:
            sorted = sorted + [packet]
    return sorted


if __name__ == "__main__":
    main()
