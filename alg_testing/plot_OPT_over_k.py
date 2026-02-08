import csv
import matplotlib.pyplot as plt
from math import pi, sqrt
from matplotlib.ticker import ScalarFormatter

# Initialize lists to store the data points
k_values = []
sum_of_demands_values = []

# Read the CSV file
with open("alg_testing/sum_of_demands_over_k.csv", "r") as f:
    reader = csv.reader(f)
    next(reader)  # Skip the header row
    for row in reader:
        k = int(row[0])
        sum_of_demands = float(row[1])
        k_values.append(k)
        sum_of_demands_values.append(sum_of_demands)

# Define the value of n
n = 1000000

# Calculate the formula k(n-k)
formula_values = [sqrt(k * (n - k)*sqrt(pi*n/2)) for k in k_values]
formula_values_2 = [k * (n - k) for k in k_values]

# Create the matrix of plots
fig, axs = plt.subplots(1, 3, figsize=(18, 6))

# First column: Data only (no formula values)
axs[0].scatter(k_values, sum_of_demands_values, color='grey', label='Sum of Demands')
axs[0].set_xlabel('k')
axs[0].set_title('Data only')
axs[0].grid(True)
axs[0].tick_params(axis='x', which='both', bottom=False, top=False, labelbottom=False)
axs[0].yaxis.set_major_formatter(ScalarFormatter(useMathText=True))
axs[0].ticklabel_format(style='sci', axis='y', scilimits=(0,0))
axs[0].set_ylim(bottom=0)

# Second column: Data with formula values
axs[1].scatter(k_values, sum_of_demands_values, color='grey', label='Sum of Demands')
axs[1].plot(k_values, formula_values, color='b', linestyle='-', label='$k \cdot (n - k)$')
axs[1].plot(k_values, formula_values_2, color='r', linestyle='-', label='$k \cdot (n - k)$')
axs[1].set_title('Linear y-scale')
axs[1].grid(True)
axs[1].tick_params(axis='x', which='both', bottom=False, top=False, labelbottom=False)
axs[1].yaxis.set_major_formatter(ScalarFormatter(useMathText=True))
axs[1].ticklabel_format(style='sci', axis='y', scilimits=(0,0))
axs[1].set_ylim(bottom=0)

# Third column: Data with formula values (log scale)
axs[2].scatter(k_values, sum_of_demands_values, color='grey', label='Sum of Demands')
axs[2].plot(k_values, formula_values, color='b', linestyle='-', label='$k \cdot (n - k)$')
axs[2].plot(k_values, formula_values_2, color='r', linestyle='-', label='$k \cdot (n - k)$')
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