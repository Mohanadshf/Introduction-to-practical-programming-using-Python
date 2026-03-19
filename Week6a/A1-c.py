c = [(35, 59), (75, 60), (48, 25), (21, 4), (2, 100), (31, 6)]
target = int(input("What do you want to find? "))

found = False
for x, y in c:
    if x == target:
        print(y)
        found = True
        break

if not found:
    print("No tuple found with first value =", target)