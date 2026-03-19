a = [2, 4, 6, 8, 10, 12, 14, 16]

num = int(input("Enter a number to insert: "))
index = 0
while index < len(a) and a[index] < num:
    index += 1
a.insert(index, num)

print("Inserted at index:", index)
print("Updated list:", a)