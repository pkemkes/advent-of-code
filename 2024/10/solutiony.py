Topomap = list[str]
Coord = tuple[int, int]
Trail = list[Coord]


def find_trailheads(topomap: Topomap) -> list[Coord]:
    trailheads = []
    x_len, y_len = len(topomap[0]), len(topomap)
    for y in range(y_len):
        for x in range(x_len):
            if topomap[y][x] == "0":
                trailheads.append((x,y))
    return trailheads


def is_complete(trail: Trail, topomap: Topomap) -> bool:
    x, y = trail[-1]
    last_pos = topomap[y][x]
    return last_pos == "9"


def find_trails(trailhead: Coord, topomap: Topomap):
    len_x, len_y = len(topomap[0]), len(topomap)
    trails = [[trailhead]]
    complete_trails = []
    while len(trails) > 0:
        trail = trails.pop()
        x, y = trail[-1]
        last_pos = topomap[y][x]
        next_pos = str(int(last_pos) + 1)
        trails_to_append = []
        if x > 0 and topomap[y][x-1] == next_pos:
            trails_to_append.append(trail + [(x-1, y)])
        if x < len_x-1 and topomap[y][x+1] == next_pos:
            trails_to_append.append(trail + [(x+1, y)])
        if y > 0 and topomap[y-1][x] == next_pos:
            trails_to_append.append(trail + [(x, y-1)])
        if y < len_y-1 and topomap[y+1][x] == next_pos:
            trails_to_append.append(trail + [(x, y+1)])
        if next_pos == "9":
            complete_trails += trails_to_append
        else:
            trails += trails_to_append
    return complete_trails


def get_trailhead_score(trailhead: Coord, trails: list[Trail]) -> int:
    relevant_trails = [trail for trail in trails if trail[0] == trailhead]
    return len(set(trail[-1] for trail in relevant_trails))


def main():
    with open("input.txt") as f:
        topomap = [l.strip() for l in f.readlines()]
    
    trailheads = find_trailheads(topomap)
    trails = sum((find_trails(trailhead, topomap) for trailhead in trailheads), [])
    trailhead_scores = [get_trailhead_score(trailhead, trails) for trailhead in trailheads]
    print("Total trailhead score:", sum(trailhead_scores))
    print("Total trailhead rating:", len(trails))
        

if __name__ == "__main__":
    main()
