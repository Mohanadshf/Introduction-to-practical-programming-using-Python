""" Program Description:
Generates an n × m matrix of random integers (-2000 to 4000) stored as a dictionary 
and displays it in two formats: simple row-by-row and with right-justified columns"""

import random

def create_matrix(n, m):
    """ Creates a matrix dictionary with keys as (row, column) tuples.
    then Validates n and m ≥ 2; raises ValueError otherwise"""
    
    if n < 2 or m < 2:
        raise ValueError("n and m must be integers greater than or equal 2.")
    matrix = {}
    for i in range(n):
        for j in range(m):
            matrix[(i, j)] = random.randint(-2000, 4000)
    return matrix 

def format_matrix(mtrx, n, m):
    #Prints the matrix with columns right-justified based on the widest element in each column
    col_widths = [] # to find max width in coulumns
    for j in range(m):
        max_width = max(len(str(mtrx[(i, j)])) for i in range(n))
        col_widths.append(max_width)
    
    for i in range(n):
        row_values = []
        for j in range(m):
            row_values.append(str(mtrx[(i, j)]).rjust(col_widths[j]))
        print("(" + " ".join(row_values) + ")")
    
"""Program Flow:
 User inputs n and m.
 Matrix is created and printed in simple format.
 Matrix is printed again with formatted, right-aligned columns."""

try:
    n = int(input("Enter number of rows (n >= 2): "))
    m = int(input("Enter number of columns (m >= 2): "))
except ValueError:
    print("Invalid input! Please enter integers only.")
    exit()

try:
    matrix = create_matrix(n, m)
except ValueError as e:
    print("Error:", e)
    exit()
for i in range(n):
    row_values = [str(matrix[(i, j)]) for j in range(m)]
    print("(" + " ".join(row_values) + ")")
    
print("\nFormatted matrix output:")
format_matrix(matrix, n, m)



