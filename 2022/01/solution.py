with open("input.txt") as f:
    input = "".join(f.readlines())

# #### Puzzle 1 #### #

elves = [e.strip().split("\n") for e in input.split("\n\n")]
elves_calories = [sum([int(c) for c in e]) for e in elves]
sorted_elves_calories = sorted(elves_calories, reverse=True)
top_elf_calories = sorted_elves_calories[0]

print("Highest amout of calories carried: ", top_elf_calories)

# #### Puzzle 2 #### #

top_three_calories = sum(sorted_elves_calories[:3])

print("Total amount of calories carried by the three elves with the most calories carried: ", top_three_calories)
