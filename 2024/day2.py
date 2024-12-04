"""Day 2 solutions."""

DATA_PATH = "./data/day2_reports.txt"


def read_input(path):
    """Read the input data."""
    with open(path, 'r', encoding='utf8') as f:
        return f.read().splitlines()


def is_safe(report: list[int]) -> bool:
    """Determine whether a report is safe or not."""
    diffs = [report[i] - report[i+1] for i in range(len(report)-1)]
    return all(1 <= x <= 3 for x in diffs) or all(-1 >= x >= -3 for x in diffs)


def main():
    """Solve today's puzzles."""
    reports = read_input(DATA_PATH)
    safe_reports_count = 0
    unsafe_reports = []
    for rep in reports:
        report = [int(x) for x in rep.split(" ")]
        if is_safe(report):
            safe_reports_count += 1
        else:
            unsafe_reports.append(report)  # For part 2
    print(f"There are {safe_reports_count} safe reports.")

    # Part 2: Just brute force, the input is small enough
    for report in unsafe_reports:
        for i in range(len(report)):
            if is_safe(report[:i] + report[i+1:]):
                safe_reports_count += 1
                break
    print(f"There are {safe_reports_count} safe reports after corrections.")


if __name__ == "__main__":
    main()
