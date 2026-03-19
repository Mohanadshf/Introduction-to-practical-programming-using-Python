__author__ = "8658986, Al-Ramessi"
import math
#Aufgabe 2:
# a)
def sum_between(a, b):
    if a > b:
        a, b = b, a
    total = sum(range(a, b + 1))
    return total

# Testfälle
print("Test a1:", sum_between(-1, 5))  # Erwartet: 14
print("Test a2:", sum_between(5, -1))  # Erwartet: 14
print("Test a3:", sum_between(0, 0))   # Erwartet: 0



# b)
def half_until_zero(x):
    if not math.isfinite(x):
        raise ValueError("x muss eine endliche Zahl sein.")
    if x == 0:
        raise ValueError("x darf nicht 0 sein")
    steps = 0
    while x != 0.0:
        x /= 2
        steps += 1
        if x == 0.0: 
            break
    return steps

# Testfälle
print("Test b1:", half_until_zero(10))   # Erwartet: eine große Zahl 
print("Test b2:", half_until_zero(-5))   # Erwartet: ähnlich großer Wert
#print("Test b3:", half_until_zero(0))   # Erwartet: ValueError



# c)
def print_chessboard(n, m):
    for i in range(n):
        row = []
        for j in range(m):
            row.append((i + j) % 2)
        print(" ".join(str(x) for x in row))

# Testfälle
print("Test c1: 4x4 Schachfeld")
print_chessboard(4, 4)
print("\nTest c2: 3x5 Schachfeld")
print_chessboard(3, 5)
print("\nTest c3: 1x7 Schachfeld")
print_chessboard(1, 7)

# d) 
def catalan_constant(n_terms=1000):
    if n_terms <= 0:
        raise ValueError("Die Anzahl der Summanden muss positiv sein")
    
    G = 0.0
    for k in range(n_terms):
        G += (-1)**k / (2*k + 1)**2
    return G

# Testfälle
print("Test d1:", catalan_constant(10))       # Kleine Anzahl von Summanden, ungefähre Annäherung
print("Test d2:", catalan_constant(1000))     # Mehr Summanden, genauere Annäherung 
print("Test d3:", catalan_constant(100000))   # Sehr viele Summanden, sehr präzise Annäherung 
# Problematische Testfälle: 0 oder negative Summanden sollten ValueError erzeugen.

# konnte  e) nicht verstehen
