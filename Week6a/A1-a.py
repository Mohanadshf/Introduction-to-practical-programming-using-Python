__author__ = "Al-Ramessi, 8658986"
word_to_digit = {
    "zero": "0",
    "one": "1",
    "two": "2",
    "three": "3",
    "four": "4",
    "five": "5",
    "six": "6",
    "seven": "7",
    "eight": "8",
    "nine": "9"
}

s = input("Enter comma separated number words: ")

words = s.split(",")
digits = ""
for w in words:
    w = w.strip().lower()
    if w in word_to_digit:
        digits += word_to_digit[w]
    else:
        print(f"Invalid word: {w}")
        exit()

print(digits)