dial = 50

with open("input.txt", "r") as f:
    lines = [line.strip() for line in f.readlines() if line.strip() != ""]

instructions = [(line[:1], int(line[1:])) for line in lines]

total_tick_count = 0
for direction, value in instructions:
    ticks = abs(value) // 100
    remainder = abs(value) % 100
    if direction == "R":
        if remainder + dial >= 100:
            ticks += 1
        dial = (dial + remainder) % 100
    elif direction == "L":
        if dial - remainder <= 0 and dial != 0:
            ticks += 1
        dial = (dial - remainder) % 100
    total_tick_count += ticks
    print(f"{direction}{value} -> {dial} - Ticks: {ticks}")

print(f"The dial pointed to 0 a total of {total_tick_count} time(s)")
