import csv
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

# Initialize a dictionary to store the data points by position
data = {}

# Read the CSV file
with open("alg_testing/results.csv", "r") as f:
    reader = csv.DictReader(f)
    for row in reader:
        n = int(row["n"])
        k = int(row["k"])
        avg_soc = float(row["avg_soc"])
        position = int(row["position"])
        if n > 0 and k > 0:
            if position not in data:
                data[position] = {"n_values": [], "avg_soc_values": [], "n_minus_1_over_sqrt_2k_values": []}
            data[position]["n_values"].append(n)
            data[position]["avg_soc_values"].append(avg_soc)
            n_minus_1_over_sqrt_2k = (n - 1) / np.sqrt(2 * k)
            data[position]["n_minus_1_over_sqrt_2k_values"].append(n_minus_1_over_sqrt_2k)

# Function to update the plot based on the slider value
def update(val):
    position = int(slider.val)
    n_values = data[position]["n_values"]
    avg_soc_values = data[position]["avg_soc_values"]
    n_minus_1_over_sqrt_2k_values = data[position]["n_minus_1_over_sqrt_2k_values"]
    
    scatter_avg_soc.set_offsets(np.c_[n_values, avg_soc_values])
    scatter_n_minus_1_over_sqrt_2k.set_offsets(np.c_[n_values, n_minus_1_over_sqrt_2k_values])
    
    ax.set_xlim(min(n_values), max(n_values))
    ax.set_ylim(min(min(avg_soc_values), min(n_minus_1_over_sqrt_2k_values)), max(max(avg_soc_values), max(n_minus_1_over_sqrt_2k_values)))
    
    fig.canvas.draw_idle()

# Initial plot
initial_position = 2
n_values = data[initial_position]["n_values"]
avg_soc_values = data[initial_position]["avg_soc_values"]
n_minus_1_over_sqrt_2k_values = data[initial_position]["n_minus_1_over_sqrt_2k_values"]

fig, ax = plt.subplots()
plt.subplots_adjust(bottom=0.35)
scatter_avg_soc = plt.scatter(n_values, avg_soc_values, c='b', alpha=0.5, label='avg_soc')
scatter_n_minus_1_over_sqrt_2k = plt.scatter(n_values, n_minus_1_over_sqrt_2k_values, c='r', alpha=0.5, label='(n - 1) / sqrt(2k)')
plt.xlabel('n (Number of nodes)')
plt.ylabel('Values')
plt.title('avg_soc and (n - 1) / sqrt(2k) vs Number of Nodes')
plt.legend()
plt.grid(True)

# Add a slider for position
ax_slider = plt.axes([0.25, 0.15, 0.65, 0.03], facecolor='lightgoldenrodyellow')
slider = Slider(ax_slider, 'Position', valmin=1, valmax=10, valinit=initial_position, valstep=1)
slider.on_changed(update)

# Add text annotation for k
ax_text = plt.axes([0.25, 0.05, 0.65, 0.03], facecolor='lightgoldenrodyellow')
ax_text.text(0.5, 0.5, 'k = 1 + (position - 1) * n / 10', horizontalalignment='center', verticalalignment='center', transform=ax_text.transAxes, fontsize=12)
ax_text.axis('off')

# Set initial axes limits
ax.set_xlim(min(n_values), max(n_values))
ax.set_ylim(min(min(avg_soc_values), min(n_minus_1_over_sqrt_2k_values)), max(max(avg_soc_values), max(n_minus_1_over_sqrt_2k_values)))

plt.show()