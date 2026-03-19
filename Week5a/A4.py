"""This program replicates Python’s str.find() function using only loops,
slicing, and indexing. It prints the lowest index where the needle occurs 
in the haystack. If the needle is not found, it prints -1."""

needle = input("Enter the needle: ")
haystack = input("Enter the haystack: ")

found = False
 
for _ in range (len(haystack) - len(needle) +1):
    if haystack[_: _ + len(needle)] == needle :
        print(_)
        found = True
        break
    
if not found:
    print(-1)
    
# i dont know to to specify test cases correctly. please show me how.
