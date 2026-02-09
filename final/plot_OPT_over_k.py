import csv
import matplotlib.pyplot as plt
from math import pi, sqrt
import numpy as np
from matplotlib.ticker import ScalarFormatter

# Read in data
k_vs_sod_readfile = "final/k_vs_sod.csv"

dtype = [("k", int), ("sum_of_demands", int)]
data = np.genfromtxt(k_vs_sod_readfile, delimiter=',', dtype=dtype, names=True)

ks: np.ndarray = data["k"]
sods: np.ndarray = data["sum_of_demands"]

# Value of n used
n = 1_000_000

# Calculate the formula k(n-k)
strong_est = np.sqrt(ks * (n - ks)*np.sqrt(pi*n/2))
weak_est = ks * (n - ks)

# Create the matrix of plots
fig, axs = plt.subplots(1, 3, figsize=(18, 6))

# First column: Data only (no formula values)
axs[0].scatter(ks, sods, color='grey')
axs[0].set_xlabel('k')
axs[0].set_title('Data only')
axs[0].grid(True)
axs[0].tick_params(axis='x', which='both', bottom=False, top=False, labelbottom=False)
axs[0].yaxis.set_major_formatter(ScalarFormatter(useMathText=True))
axs[0].ticklabel_format(style='sci', axis='y', scilimits=(0,0))
axs[0].set_ylim(bottom=0)

# Second column: Data with formula values
axs[1].scatter(ks, sods, color='grey', label='Sum of Demands')
axs[1].plot(ks, strong_est, color='b', linestyle='-', label='$k \cdot (n - k)$')
axs[1].plot(ks, weak_est, color='r', linestyle='-', label='$k \cdot (n - k)$')
axs[1].set_title('Linear y-scale')
axs[1].grid(True)
axs[1].tick_params(axis='x', which='both', bottom=False, top=False, labelbottom=False)
axs[1].yaxis.set_major_formatter(ScalarFormatter(useMathText=True))
axs[1].ticklabel_format(style='sci', axis='y', scilimits=(0,0))
axs[1].set_ylim(bottom=0)

# Third column: Data with formula values (log scale)
axs[2].scatter(ks, sods, color='grey', label='Sum of Demands')
axs[2].plot(ks, strong_est, color='b', linestyle='-', label='$k \cdot (n - k)$')
axs[2].plot(ks, weak_est, color='r', linestyle='-', label='$k \cdot (n - k)$')
axs[2].set_yscale('log')
axs[2].set_title('Logarithmic y-scale')
axs[2].grid(True)
axs[2].tick_params(axis='x', which='both', bottom=False, top=False, labelbottom=False)
axs[2].set_ylim(bottom=1)

# Add a single legend
# handles, labels = axs[1].get_legend_handles_labels()
# fig.legend(handles, loc='upper right')

#plt.tight_layout()
plt.show()