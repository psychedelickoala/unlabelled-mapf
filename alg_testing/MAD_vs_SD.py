from scipy.stats import hypergeom
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
from math import comb

def mad_sd_ratio(n, l, k):
    # Create the hypergeometric distribution
    rv = hypergeom(n, l, k)
    
    # Get the support of the distribution
    x = np.arange(0, l+1)
    
    # Get the probabilities for each value in the support
    pmf = rv.pmf(x)
    
    # Calculate the mean absolute difference
    mad = np.sum([pmf[i] * pmf[j] * abs(x[i] - x[j]) for i in range(len(x)) for j in range(len(x))])
    
    return mad / rv.std()

def mean_mad_sd_ratio(n, k):
    return np.sum(
        [
            mad_sd_ratio(n, l, k)*comb(n, l)*np.power(l/n, l-1)*np.power((n-l)/n, n-l-1)
            for l in range(1, n)
        ]
    )/(2*n-2)


print(mean_mad_sd_ratio(500, 480))
# Initial plot
# x_values = np.arange(3, 50, step=100)
# k = 1
# y_values = [mean_mad_sd_ratio(n, k) for n in x_values]



# # Calculate the maximum and minimum y-values for k = 1 and l = 1
# max_y = max(y_values)
# min_y = min(y_values)

# fig, ax = plt.subplots()
# plt.subplots_adjust(bottom=0.35)
# line, = plt.plot(x_values, y_values, marker='', linestyle='-', color='b')
# plt.xlabel('n (Total number of items)')
# plt.ylabel('MAD / SD Ratio')
# plt.title('MAD / SD Ratio vs Total Number of Items (k=1, l=1)')
# plt.grid(True)

# # Set initial axes limits
# ax.set_ylim(min_y, max_y)

# plt.show()



