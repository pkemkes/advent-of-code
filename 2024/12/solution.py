Garden = list[str]
Coord = tuple[int, int]
Plot = set[Coord]
SideSpot = tuple[Coord, Coord]
Side = set[SideSpot]


def get_plant(coord: Coord, garden: Garden) -> str | None:
	len_x = len(garden[0])
	len_y = len(garden)
	x, y = coord
	if x < 0 or x >= len_x or y < 0 or y >= len_y:
		return None
	return garden[y][x]


def find_plot(start: Coord, garden: Garden) -> Plot:
	orig_plant = get_plant(start, garden)
	to_check = [start]
	plot = set(to_check)
	while len(to_check) > 0:
		x, y = to_check.pop()
		for add_x, add_y in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
			plot_spot = (x + add_x, y + add_y)
			if plot_spot in plot:
				continue
			if get_plant(plot_spot, garden) != orig_plant:
				continue
			to_check.append(plot_spot)
			plot.add(plot_spot)
	return plot


def calc_perimeter(plot: Plot, garden: Garden) -> int:
	plant = get_plant(next(iter(plot)), garden)
	perimeter = 0
	for x, y in plot:
		for add_x, add_y in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
			if get_plant((x + add_x, y + add_y), garden) != plant:
				perimeter += 1
	return perimeter


def find_side(start: Coord, side_dir: Coord, fence_dir: Coord, garden: Garden) -> Plot:
	plant = get_plant(start, garden)
	side = set([start])
	next_side_spot = start
	side_add_x, side_add_y = side_dir
	fence_add_x, fence_add_y = fence_dir
	while True:
		next_x, next_y = next_side_spot
		next_side_spot = (next_x+side_add_x, next_y+side_add_y)
		next_fence_spot = (next_x+fence_add_x, next_y+fence_add_y)
		if get_plant(next_side_spot, garden) != plant:
			break
		if get_plant(next_fence_spot, garden) == plant:
			break
		side.add((next_side_spot, next_fence_spot))
	return side


def calc_sides(plot: Plot, garden: Garden) -> int:
	plant = get_plant(next(iter(plot)), garden)
	sides = []
	for plot_spot in plot:
		x, y = plot_spot

		# vertical
		# left
		fence_spot = (x-1, y)
		fence_is_left = get_plant(fence_spot, garden) != plant
		if fence_is_left and not any((plot_spot, fence_spot) in side for side in sides):
			down_side = find_side(plot_spot, (0, 1), (-1, 1), garden)
			up_side = find_side(plot_spot, (0, -1), (-1, -1), garden)
			sides.append(down_side.union(up_side))

		# right
		fence_spot = (x+1, y)
		fence_is_right = get_plant(fence_spot, garden) != plant
		if fence_is_right and not any((plot_spot, fence_spot) in side for side in sides):
			down_side = find_side(plot_spot, (0, 1), (1, 1), garden)
			up_side = find_side(plot_spot, (0, -1), (1, -1), garden)
			sides.append(down_side.union(up_side))

		# horizontal
		# up
		fence_spot = (x, y-1)
		fence_is_up = get_plant(fence_spot, garden) != plant
		if fence_is_up and not any((plot_spot, fence_spot) in side for side in sides):
			left_side = find_side(plot_spot, (-1, 0), (-1, -1), garden)
			right_side = find_side(plot_spot, (1, 0), (1, -1), garden)
			sides.append(left_side.union(right_side))

		# down
		fence_spot = (x, y+1)
		fence_is_down = get_plant(fence_spot, garden) != plant
		if fence_is_down and not any((plot_spot, fence_spot) in side for side in sides):
			left_side = find_side(plot_spot, (-1, 0), (-1, 1), garden)
			right_side = find_side(plot_spot, (1, 0), (1, 1), garden)
			sides.append(left_side.union(right_side))
	return len(sides)


def main():
	with open("input.txt") as f:
		garden = [l.strip() for l in f.readlines()]
	
	plots = []
	len_x = len(garden[0])
	len_y = len(garden)

	for y in range(len_y):
		for x in range(len_x):
			if any((x, y) in plot for plot in plots):
				continue
			plot = find_plot((x, y), garden)
			plots.append(plot)
	
	total_normal_price = 0
	for plot in plots:
		perimeter = calc_perimeter(plot, garden)
		price = len(plot) * perimeter
		total_normal_price += price

	print("Total normal price:", total_normal_price)

	total_bulk_price = 0
	for plot in plots:
		sides = calc_sides(plot, garden)
		price = len(plot) * sides
		total_bulk_price += price

	print("Total bulk price:", total_bulk_price)


if __name__ == "__main__":
	main()
