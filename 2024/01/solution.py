def main():
    with open("input.txt") as f:
        lines = [l.strip() for l in f.readlines()]
    
    left = []
    right = []
    for line in lines:
        left_elem, right_elem = line.split("   ")
        left.append(int(left_elem))
        right.append(int(right_elem))

    left = sorted(left)
    right = sorted(right)

    distances = [abs(l - r) for l, r in zip(left, right)]

    total_distance = sum(distances)

    print("Total distance:", total_distance)

    sim_score = 0
    for l in left:
        sim_score += l * right.count(l)
    
    print("Similarity score:", sim_score)
    

if __name__ == "__main__":
    main()
