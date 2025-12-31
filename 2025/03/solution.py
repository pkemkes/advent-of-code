with open("input2.txt", "r") as f:
    banks = [[int(num) for num in bank.strip()] for bank in f.readlines()]

def find_joltage(bank, iterations_left):
    if iterations_left == 0:
        return ""
    bank_to_check = bank[:-(iterations_left-1)] if iterations_left > 1 else bank
    highest = max(bank_to_check)
    i_highest = bank.index(highest)
    rest_bank = bank[i_highest+1:]
    return f"{highest}{find_joltage(rest_bank, iterations_left-1)}"

joltages = [int(find_joltage(bank, 12)) for bank in banks]

print(f"Sum of joltages: {sum(joltages)}")
