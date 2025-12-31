with open("input2.txt", "r") as file:
    data = file.read()

invalid_ids = []
ranges = [r.split("-") for r in data.strip().split(",")]
for first, last in ranges:
    for gift_id in range(int(first), int(last) + 1):
        id_str = str(gift_id)
        id_len = len(id_str)
        intervals = [i for i in range(1, id_len//2 + 1) if id_len % i == 0]
        for i in intervals:
            i_count = id_len // i
            if all(id_str[j:j+i] == id_str[0:i] for j in range(i, id_len, i)):
                invalid_ids.append(gift_id)
                break
print(sum(invalid_ids))
