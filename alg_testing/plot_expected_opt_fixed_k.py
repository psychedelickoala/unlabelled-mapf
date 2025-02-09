import numpy as np
import matplotlib.pyplot as plt
from math import sqrt, pi, e, log
from scipy.special import comb

def expected_OPT(n, k):
    array = np.zeros(n)
    for l in range(1, n):
        array[l] = np.sum([
            np.sum([
                (b-a)*comb(k, b)*comb(n-k, l-b)
                for b in range(a+1, min(l, k)+1)
            ])*comb(k, a)*comb(n-k, l-a)
            for a in range(max(l - (n-k), 0), min(l, k)+1)
        ]) *np.power(l/n,l-1)*np.power((n-l)/n,n-l-1)/comb(n, l)
    return np.sum(array)

def expected_OPT_upper(n, k):
    array = np.zeros(n)
    for l in range(1, n):
        array[l] = np.sum([
            np.sum([
                (b-a)*up_comb(k, b)*up_comb(n-k, l-b)
                for b in range(a+1, min(l, k)+1)
            ])*up_comb(k, a)*up_comb(n-k, l-a)
            for a in range(max(l - (n-k), 0), min(l, k)+1)
        ]) *np.power(l/n,l-1)*np.power((n-l)/n,n-l-1)/comb(n, l)
    return np.sum(array)

def expected_one_agent(n):
    return np.sum(
        [
            comb(n, l)*np.power(l/n, l)*np.power((n-l)/n, n-l)
            for l in range(1, n)
        ]
    )

def expected_sqrt_l(n):
    return np.sum(
        [
            comb(n, l)*np.power(l/n, l-0.5)*np.power((n-l)/n, n-l-0.5)
            for l in range(1, n)    
        ]
    )

def up_comb(x, y):
    return np.power(e*x/y, y) if y > 0 else 1

n=50
print(expected_OPT(n, n//2)/(n*log(log(n))))

# Plot expected_OPT for integer n between 30 and 100 with k=15 fixed
n_values = [k for k in range(10, 300, 25)]
y_values = [expected_OPT(n, n//2) for n in n_values]
y_upper = [n**2/4 for n in n_values]
y_fit = [(n/2)*sqrt(sqrt(pi*n/2) - 1)/2 for n in n_values]


print(n_values)
print(y_values)
fig, ax = plt.subplots()
plt.plot(n_values, y_values, marker='', linestyle='-', color='b')
plt.plot(n_values, y_fit, marker='', linestyle='-', color='g')
plt.plot(n_values, y_upper, marker='', linestyle='-', color='r')
plt.xlabel('k (number of agents)')
plt.ylabel('expected_OPT')
plt.title('expected_OPT for n = 100')
plt.grid(True)
plt.show()