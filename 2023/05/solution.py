from typing import List, Tuple

Interval = Tuple[int, int]
Map = List[Tuple[Interval, int]]

with open("input.txt") as f:
    input = f.read().strip()

sections = input.split("\n\n")
seeds = [int(seed.strip())
         for seed in sections[0].split("seeds: ")[1].split(" ")]


def extract_maps(sections: List[str]) -> List[Map]:
    maps = []
    for section in sections:
        map_data = [[int(num) for num in range_nums.strip().split(" ")]
                    for range_nums in section.split("\n")[1:]]
        maps.append([((shift[1], shift[1] + shift[2] - 1), shift[0] - shift[1])
                     for shift in map_data])
    return maps


maps = extract_maps(sections[1:])


# #### Puzzle 1 #### #

def shift_by_map(to_shift: int, map: Map) -> int:
    for (start, end), shift in map:
        if start <= to_shift and to_shift <= end:
            return to_shift + shift
    return to_shift


def shift_by_maps(to_shift: int, maps: List[Map]) -> int:
    result = to_shift
    for map in maps:
        result = shift_by_map(result, map)
    return result


locations = [shift_by_maps(seed, maps) for seed in seeds]
print("Lowest location:", min(locations))


# #### Puzzle 2 #### #

def find_not_shifted(intv: Interval,
                     shifted: List[Interval]) -> List[Interval]:
    not_shifted = [(intv)]
    for s_s, s_e in shifted:
        result = []
        while len(not_shifted) != 0:
            ns_s, ns_e = not_shifted.pop(0)
            if s_s > ns_e or s_e < ns_s:
                result.append((ns_s, ns_e))
            else:
                left = (ns_s, s_s-1)
                if left[0] <= left[1]:
                    result.append(left)
                right = (s_e+1, ns_e)
                if right[0] <= right[1]:
                    result.append(right)
        not_shifted = result
    return not_shifted


def merge_intervals(intvs: List[Interval]) -> List[Interval]:
    if len(intvs) <= 1:
        return intvs
    sorted_intvs = sorted(intvs, key=lambda x: (x[0], -x[1]))
    result = [sorted_intvs.pop(0)]
    for intv in sorted_intvs:
        last = result.pop()
        if intv[0] >= last[0] and intv[1] <= last[1]:
            result.append(last)
        elif last[1] >= intv[0]-1:
            result.append((last[0], intv[1]))
        else:
            result.append(last)
            result.append(intv)
    return result


def shift_interval_by_map(intv: Interval, map: Map) -> List[Interval]:
    result = []
    shifted = []
    intv_s, intv_e = intv
    for (start, end), shift in map:
        if intv_s > end or intv_e < start:
            continue
        new_s = max(intv_s, start)
        new_e = min(intv_e, end)
        shifted.append((new_s, new_e))
        result.append((new_s+shift, new_e+shift))
    shifted = sorted(shifted)
    for i in range(1, len(shifted)):
        if shifted[i-1][1] != shifted[i][0]-1:
            result.append((shifted[i-1][1]+1, shifted[i][0]-1))
    result += find_not_shifted(intv, shifted)
    return merge_intervals(result)


def shift_intervals_by_map(intvs: List[Interval], map: Map):
    shifted_intvs = sum(
        [shift_interval_by_map(intv, map) for intv in intvs],
        start=[]
    )
    return merge_intervals(shifted_intvs)


def shift_interval_by_maps(intv: Interval,
                           maps: List[Map]) -> List[Interval]:
    result = [intv]
    for map in maps:
        result = shift_intervals_by_map(result, map)
    return result


seed_intvs = [(seeds[2*i], seeds[2*i] + seeds[2*i+1] - 1)
              for i in range(len(seeds)//2)]
shifted_seed_intvs = [shift_interval_by_maps(seed_intv, maps)
                      for seed_intv in seed_intvs]
shifted_seed_intvs = [sorted(intv) for intv in shifted_seed_intvs]
print(
    "Lowest possible location:",
    min(shifted_seed_intvs, key=lambda x: x[0][0])[0][0]
)
