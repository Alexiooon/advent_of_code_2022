"""Day 1 Challenges."""
import os

# Read the data
path = os.path.join('.', 'data', 'input_day1.txt')
with open(path, 'r', encoding='utf8') as f:
    calibration_data = f.read().splitlines()

# Part 1
def filter_calibration_value(line: str):
    """Cleans up a calibration value."""
    number_line = "".join(letter for letter in line if letter.isnumeric())
    return int(number_line[0] + number_line[-1])

clean_data = []
for data_line in calibration_data:
    clean_data.append(filter_calibration_value(data_line))
print(f"The sum of all calibration values is: {sum(clean_data)}")

# Part 2
NUMBERS = ["1", "2", "3", "4", "5", "6", "7", "8", "9",
           "one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]
MAP = {"1": 1, "one": 1, "2": 2, "two": 2, "3": 3, "three": 3, "4": 4, "four": 4, "5": 5, "five": 5,
       "6": 6, "six": 6, "7": 7, "seven": 7, "8": 8, "eight": 8, "9": 9, "nine": 9}
def filter_calibration_value_with_letters(line: str):
    """Cleans up a calibration value, including numbers written in letters."""
    print(line)
    first_digit = 0
    last_digit = 0
    for i in range(len(line)):
        for num in NUMBERS:
            if num in line[:i+1]:
                first_digit = MAP[num]
                break
        if first_digit > 0:
            break
    for i in range(len(line)):
        for num in NUMBERS:
            if num in line[len(line)-i-1:]:
                last_digit = MAP[num]
                break
        if last_digit > 0:
            break
    return 10*first_digit + last_digit

correct_clean_data = []
for data_line in calibration_data:
    correct_clean_data.append(filter_calibration_value_with_letters(data_line))
print(f"The correct sum of all calibration values is: {sum(correct_clean_data)}")
