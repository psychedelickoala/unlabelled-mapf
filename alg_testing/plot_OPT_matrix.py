import csv
import matplotlib.pyplot as plt
import numpy as np
from math import sqrt, pi, log, e
from matplotlib.ticker import ScalarFormatter

# Initialize lists to store the data points
n_values = []
k_values = []
sum_of_demands_values = []
k_types = []
k_type = 0

# Read the CSV file
with open("alg_testing/sum_of_demands_labelled_path.csv", "r") as f:
    reader = csv.reader(f)
    next(reader)  # Skip the header row
    for row in reader:
        n = int(row[0])
        k = int(row[1])
        sum_of_demands = float(row[2])
        # k_type = int(row[3])  # Assuming k_type is in the fourth column
        n_values.append(n)
        k_values.append(k)
        sum_of_demands_values.append(sum_of_demands)
        k_types.append(k_type)
        k_type = (k_type + 1) % 7


# Create the matrix of plots
fig, axs = plt.subplots(3, 3, figsize=(18, 18))

k_type_values = [0, 3, 6]

for i, k_type in enumerate(k_type_values):
    # Filter data for the current k_type
    filtered_n_values = [n for n, kt in zip(n_values, k_types) if kt == k_type]
    filtered_k_values = [k for k, kt in zip(k_values, k_types) if kt == k_type]
    filtered_sum_of_demands_values = [s for s, kt in zip(sum_of_demands_values, k_types) if kt == k_type]

    # First column: No formula comparison
    axs[i, 0].scatter(filtered_n_values, filtered_sum_of_demands_values, color='grey')
    axs[i, 0].grid(True)
    axs[i, 0].tick_params(axis='x', which='both', bottom=False, top=False, labelbottom=False)
    axs[i, 0].yaxis.set_major_formatter(ScalarFormatter(useMathText=True))
    axs[i, 0].ticklabel_format(style='sci', axis='y', scilimits=(0,0))
    axs[i, 0].set_ylim(bottom=0)

    # Second column: Linear scale with formula comparison
    formula_values = [sqrt(k * (n - k)*sqrt(pi*n/2)) for k, n in zip(filtered_k_values, filtered_n_values)]

    # trying stuff
    formula_values_2 = [sqrt(k * (n - k)*(n-1)) for k, n in zip(filtered_k_values, filtered_n_values)]
    axs[i, 1].scatter(filtered_n_values, filtered_sum_of_demands_values, color='grey')
    #axs[i, 1].plot(filtered_n_values, formula_values, linestyle='-', color='b')
    axs[i, 1].plot(filtered_n_values, formula_values_2, linestyle='-', color='r')
    axs[i, 1].grid(True)
    axs[i, 1].yaxis.set_major_formatter(ScalarFormatter(useMathText=True))
    axs[i, 1].ticklabel_format(style='sci', axis='y', scilimits=(0,0))
    axs[i, 1].tick_params(axis='x', which='both', bottom=False, top=False, labelbottom=False)
    axs[i, 1].set_ylim(bottom=0)

    # Third column: Logarithmic scale with formula comparison
    axs[i, 2].scatter(filtered_n_values, filtered_sum_of_demands_values, color='grey')
    #axs[i, 2].plot(filtered_n_values, formula_values, linestyle='-', color='b')
    axs[i, 2].plot(filtered_n_values, formula_values_2, linestyle='-', color='r')
    axs[i, 2].set_yscale('log')
    axs[i, 2].grid(True)
    axs[i, 2].tick_params(axis='x', which='both', bottom=False, top=False, labelbottom=False)
    axs[i, 2].set_ylim(bottom=1)

# Set titles for rows and columns
for ax, col in zip(axs[0], ['Data only', 'Linear y-scale', 'Logarithmic y-scale']):
    ax.set_title(col)

for ax, row in zip(axs[:, 0], ['$k = 1$', '$k = \sqrt{n}$', '$k = n/2$']):
    ax.set_ylabel(row, rotation=90, size='large')

# Add a single legend
#handles, labels = axs[0, 1].get_legend_handles_labels()
#fig.legend(handles, ['Sum of Demands', r'$\sqrt{k \cdot (n - k) \cdot (\sqrt{\pi n / 2} - 1)}$'], loc='upper right')
#plt.tight_layout()
plt.show()