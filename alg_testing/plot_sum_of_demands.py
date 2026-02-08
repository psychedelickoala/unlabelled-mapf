import csv
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
import numpy as np
from math import sqrt, pi, log

# Initialize lists to store the data points
n_values = []
k_values = []
sum_of_demands_values = []

# Read the CSV file
with open("alg_testing/sum_of_demands_labelled.csv", "r") as f:
    reader = csv.reader(f)
    next(reader)  # Skip the header row
    k_type = 0
    for row in reader:
        n = int(row[0])
        k = int(row[1])
        sum_of_demands = float(row[2])

        n_values.append((n, k, k_type))
        k_values.append(k)
        sum_of_demands_values.append(sum_of_demands)
        k_type = (k_type + 1) % 7

# Function to update the plot based on the slider value
def update(val):
    k_type = int(slider.val)
    filtered_n_values = [n for n, k, k_val in n_values if k_val == k_type]
    filtered_k_values = [k for n, k, k_val in n_values if k_val == k_type]
    filtered_sum_of_demands_values = [sum_of_demands_values[i] for i, (n, k, k_val) in enumerate(n_values) if k_val == k_type]
    scatter.set_offsets(np.c_[filtered_n_values, filtered_sum_of_demands_values])
    formula_values = [sqrt(k*(n-k)/(n-1))*sqrt(sqrt(pi*n/2)-1) for n, k in zip(filtered_n_values, filtered_k_values)]
    line.set_xdata(filtered_n_values)
    line.set_ydata(formula_values)
    ax.set_xlim(min(filtered_n_values), max(filtered_n_values))
    ax.set_ylim(1, max(filtered_sum_of_demands_values + formula_values))
    ax.set_yscale('log')
    fig.canvas.draw_idle()

# Initial plot
initial_k = 0
filtered_n_values = [n for n, k, k_val in n_values if k_val == initial_k]
filtered_k_values = [k for n, k, k_val in n_values if k_val == initial_k]
filtered_sum_of_demands_values = [sum_of_demands_values[i] for i, (n, k, k_val) in enumerate(n_values) if k_val == initial_k]

fig, ax = plt.subplots()
plt.subplots_adjust(bottom=0.25)
scatter = plt.scatter(filtered_n_values, filtered_sum_of_demands_values, color='b', label='$OPT$')

# Calculate and plot the formula sqrt(k*(n-k)*(sqrt(pi*n/2)-1))
formula_values = [sqrt(k * (n - k) * (sqrt(pi * n / 2) - 1)) for n, k in zip(filtered_n_values, filtered_k_values)]
line, = plt.plot(filtered_n_values, formula_values, linestyle='-', linewidth = 4, color='r', label=r'$k (n - k)$')


plt.xlabel('n')
plt.ylabel('OPT')
plt.title('n vs OPT')
plt.legend()
plt.grid(True)

# Add a slider for k
ax_slider = plt.axes([0.25, 0.1, 0.65, 0.03], facecolor='lightgoldenrodyellow')
slider = Slider(ax_slider, 'k_type', valmin=0, valmax=6, valinit=initial_k, valstep=1)
slider.on_changed(update)

# Set initial axes limits
ax.set_xlim(min(filtered_n_values), max(filtered_n_values))
ax.set_ylim(0, max(filtered_sum_of_demands_values))

plt.show()