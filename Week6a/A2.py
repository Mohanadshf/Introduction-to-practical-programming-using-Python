#a
def ack(n, m):
    if n == 0:
        return m + 1
    elif m == 0 and n != 0:
        return ack(n - 1, 1)
    else:
        return ack(n - 1, ack(n, m - 1))
#b
def f(n):
    if n <= 1:
        return 1 
    else:
        return f(n-1) + f(n-3)
    

def f_iter(n):
    if n <=1: return 1
    box_a = 1
    box_b = 1
    box_c = 1

    for i in range(2,n+1):
        akku = box_a + box_c
        box_a = box_b
        box_b = box_c 
        box_c = akku

    return akku
        
#c:
"""Recursive code can exceed the call stack and cause 
a stack-overflow error, while iterative code doesn’t 
have this risk. We also risk uncontrolled or infinite 
recursion if we dont specify a firm base case"""