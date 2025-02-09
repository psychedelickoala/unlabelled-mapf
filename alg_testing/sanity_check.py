import numpy as np
import math
from math import factorial as fc
from math import comb

def f(a, l, n, k):
    return (l**(l-1))*((n-l)**(n-l-1))*comb(n-k, l-a) if 0 < l < n else 0

def pr(l, n):
    return comb(n, l)*(l**(l-1))*((n-l)**(n-l-1))/(2*(n-1)*(n**(n-2)))

# def expected_OPT(n, k):
#     array = np.zeros(k+1)
#     denom = n**(n-2)
#     for a in range(k+1):
#         array[a] = np.sum([f(a, l, n, k) for l in range(a, n-k+a+1)])*comb(k, a)/(2*(n-1)*(denom))
#     print(array)
#     sum = 0
#     for a in range(k+1):
#         for b in range(a+1, k+1):
#             sum += (b-a)*array[a]*array[b]

#     return sum*2*(n-1)

def expected_OPT(n, k):
    array = np.zeros(n)
    for l in range(1, n):
        array[l] = np.sum([
            np.sum([
                (b-a)*comb(k, b)*comb(n-k, l-b)
                for b in range(a+1,min(l, k)+1)
            ])*comb(k, a)*comb(n-k, l-a)
            for a in range(max(l - (n-k), 0), min(l, k)+1)
        ]) *(l**(l-1))*((n-l)**(n-l-1))/(comb(n, l)*(n**(n-2)))
    return np.sum(array)



k = 100
l = 40
array = np.zeros((l, l))
for a in range(l):
    for b in range(l):
        array[a][b] = comb(k, a)*comb(k, b)*comb(k, l-a)*comb(k, l-b)#*abs(a-b)
# Write array to a CSV file
np.savetxt("array_output.csv", array, delimiter=",")