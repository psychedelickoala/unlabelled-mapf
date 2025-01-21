import csv
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

# Initialize a dictionary to store the sum of avg_soc and count for each n and position
data = {}

# Read the CSV file
with open("alg_testing/results.csv", "r") as f:
    reader = csv.DictReader(f)
    for row in reader:
        n = int(row["n"])
        position = int(row["position"])
        k = int(row["k"])
        avg_soc = float(row["avg_soc"])
        
        if n not in data:
            data[n] = {}
        if position not in data[n]:
            data[n][position] = {"sum_avg_soc": 0, "count": 0, "k": k}
        
        data[n][position]["sum_avg_soc"] += avg_soc
        data[n][position]["count"] += 1

# Function to calculate moving average
def moving_average(data, window_size):
    return np.convolve(data, np.ones(window_size)/window_size, mode='valid')

# Function to update the plot based on the slider value
def update(val):
    position = int(slider.val)
    n_values = []
    avg_soc_values = []
    upper_bound_values = []
    
    for n in sorted(data.keys()):
        if position in data[n]:
            n_values.append(n)
            avg_soc_values.append(data[n][position]["sum_avg_soc"] / data[n][position]["count"])
            upper_bound_values.append(n - data[n][position]["k"])
    
    # Apply moving average
    window_size = 20  # Increased window size for smoother data
    smoothed_avg_soc_values = moving_average(avg_soc_values, window_size)
    smoothed_upper_bound_values = moving_average(upper_bound_values, window_size)
    smoothed_n_values = n_values[:len(smoothed_avg_soc_values)]
    
    line.set_xdata(smoothed_n_values)
    line.set_ydata(smoothed_avg_soc_values)
    upper_bound_line.set_xdata(smoothed_n_values)
    upper_bound_line.set_ydata(smoothed_upper_bound_values)
    
    # Adjust the axes limits
    ax.set_xlim(min(smoothed_n_values), max(smoothed_n_values))
    ax.set_ylim(min(min(smoothed_avg_soc_values), min(smoothed_upper_bound_values)), max(max(smoothed_avg_soc_values), max(smoothed_upper_bound_values)))
    
    fig.canvas.draw_idle()

# Initial plot
initial_position = 1
n_values = []
avg_soc_values = []
upper_bound_values = []

for n in sorted(data.keys()):
    if initial_position in data[n]:
        n_values.append(n)
        avg_soc_values.append(data[n][initial_position]["sum_avg_soc"] / data[n][initial_position]["count"])
        upper_bound_values.append(n - data[n][initial_position]["k"])

# Apply moving average
window_size = 20  # Increased window size for smoother data
smoothed_avg_soc_values = moving_average(avg_soc_values, window_size)
smoothed_upper_bound_values = moving_average(upper_bound_values, window_size)
smoothed_n_values = n_values[:len(smoothed_avg_soc_values)]

fig, ax = plt.subplots()
plt.subplots_adjust(bottom=0.35)
line, = plt.plot(smoothed_n_values, smoothed_avg_soc_values, marker='o', linestyle='-', color='b', label='Average SOC')
upper_bound_line, = plt.plot(smoothed_n_values, smoothed_upper_bound_values, marker='o', linestyle='-', color='r', label='Upper Bound (n - k)')
plt.xlabel('n (Number of nodes)')
plt.ylabel('Values')
plt.title('Average SOC and Upper Bound vs Number of Nodes')
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
ax.set_xlim(min(smoothed_n_values), max(smoothed_n_values))
ax.set_ylim(min(min(smoothed_avg_soc_values), min(smoothed_upper_bound_values)), max(max(smoothed_avg_soc_values), max(smoothed_upper_bound_values)))

plt.show()