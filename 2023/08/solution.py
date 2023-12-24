from typing import List, Dict, Tuple
from math import gcd, prod

Nodes = Dict[str, Tuple[str, str]]


with open("input.txt") as f:
    lines = f.readlines()
instructions = lines[0].strip()


def extract_nodes(lines: List[str]) -> Nodes:
    nodes = {}
    for line in lines:
        node, edges = line.split(" = ")
        nodes[node] = edges.strip()[1:-1].split(", ")
    return nodes


nodes = extract_nodes(lines[2:])


def count_steps(nodes: Nodes, instructions: str,
                start: str, end: str) -> int:
    steps = 0
    position = start
    while True:
        for instruction in instructions:
            position = nodes[position][0] \
                    if instruction == "L" \
                    else nodes[position][1]
        steps += 1
        if position.endswith(end):
            break
    return steps * len(instructions)


# #### Puzzle 1 #### #

steps = count_steps(nodes, instructions, "AAA", "ZZZ")
print("It took", steps, "steps to reach the end.")


# #### Puzzle 2 #### #

starts = [pos for pos in nodes if pos.endswith("A")]
steps_for_paths = [count_steps(nodes, instructions, start, "Z")
                   for start in starts]
total_steps = steps_for_paths[0]
for steps_for_path in steps_for_paths[1:]:
    total_steps = (prod((total_steps, steps_for_path))
                   // gcd(total_steps, steps_for_path))
print(f"It takes {total_steps:.0f} steps for all paths to reach the end.")
