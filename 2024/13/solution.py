import re

Coord = tuple[int, int]
Machine = tuple[Coord, Coord, Coord]


def parse_machine(machine_lines: str) -> Machine:
	line_a, line_b, line_p = machine_lines.split("\n")
	button_pattern = r"Button \w: X\+(\d+), Y\+(\d+)"
	a_match = re.match(button_pattern, line_a)
	b_match = re.match(button_pattern, line_b)
	prize_pattern = r"Prize: X=(\d+), Y=(\d+)"
	p_match = re.match(prize_pattern, line_p)
	return (
		(int(a_match[1]), int(a_match[2])),
		(int(b_match[1]), int(b_match[2])),
		(int(p_match[1]), int(p_match[2]))
	)


def is_whole_number(number: float) -> bool:
	return int(number) == number


def solve(machine: Machine) -> tuple[int, int] | None:
	(a_x, a_y), (b_x, b_y), (p_x, p_y) = machine
	presses_a = (p_x*b_y - p_y*b_x) / (a_x*b_y - a_y*b_x)
	presses_b = (p_y*a_x - p_x*a_y) / (a_x*b_y - a_y*b_x)
	if not is_whole_number(presses_a) or not is_whole_number(presses_b):
		return None
	return int(presses_a), int(presses_b)


def calc_token_costs(solution: tuple[int, int]) -> int:
	presses_a, presses_b = solution
	return presses_a * 3 + presses_b * 1


def solve_and_calc_costs(machine: Machine) -> int:
	solution = solve(machine)
	return 0 if solution is None else calc_token_costs(solution)


def adjust_machines(machines: list[Machine]) -> list[Machine]:
	addition = 10000000000000
	adjusted_machines = []
	for coords_a, coords_b, (p_x, p_y) in machines:
		adjusted_machines.append((
			coords_a, 
			coords_b, 
			(p_x+addition, p_y+addition)
		))
	return adjusted_machines


def main():
	with open("input.txt") as f:
		input_txt = f.read().strip()
	machines = [parse_machine(m) for m in input_txt.split("\n\n")]

	total_costs = sum(solve_and_calc_costs(m) for m in machines)
	print("Total token costs:", total_costs)

	machines = adjust_machines(machines)
	total_adjusted_costs = sum(solve_and_calc_costs(m) for m in machines)
	print("Total token costs after adjustion:", total_adjusted_costs)


if __name__ == "__main__":
	main()
