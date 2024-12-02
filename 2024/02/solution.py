def check_safety(report: list):
    curr_level = report[0]
    inc = (report[0] - report[1]) < 0
    for i, level in enumerate(report):
        if i == 0:
            continue
        diff = curr_level - level
        if inc and (diff < -3 or diff > -1):
            return False
        if (not inc) and (diff > 3 or diff < 1):
            return False
        curr_level = level
    return True


def main():
    with open("input.txt") as f:
        reports = [
            [int(level) for level in line.strip().split(" ")]
            for line in f.readlines()
        ]
    
    number_of_safe_reports = sum(
        1 if check_safety(report) else 0 for report in reports
    )
    
    print("Number of safe reports:", number_of_safe_reports)

    number_of_safe_reports = 0
    for report in reports:
        if check_safety(report):
            number_of_safe_reports += 1
            continue
        for i in range(len(report)):
            if check_safety(report[:i] + report[i+1:]):
                number_of_safe_reports += 1
                break
    
    print("Number of safe reports with dampener:", number_of_safe_reports)


if __name__ == "__main__":
    main()
