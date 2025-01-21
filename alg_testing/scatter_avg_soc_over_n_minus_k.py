import csv
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

# Initialize lists to store the data points
data_points = []

# Read the CSV file
with open("alg_testing/results.csv", "r") as f:
    reader = csv.DictReader(f)
    for row in reader:
        n = int(row["n"])
        k = int(row["k"])
        avg_soc = float(row["avg_soc"])
        position = int(row["position"])
        if position != 1 and n > 0 and (n - k) != 0:
            avg_soc_over_n_minus_k = avg_soc / (n - k)
            data_points.append((n, avg_soc_over_n_minus_k))

# Ensure there are enough data points to fit
if len(data_points) < 2:
    raise ValueError("Not enough data points to fit a function.")

# Separate the data points into x and y values
n_values, avg_soc_over_n_minus_k_values = zip(*data_points)

# Define the function to fit
def inverse_func(n, a):
    return a / n

# Fit the function to the data
try:
    popt, pcov = curve_fit(inverse_func, n_values, avg_soc_over_n_minus_k_values)
except RuntimeError as e:
    raise RuntimeError(f"Error fitting the function: {e}")

# Generate x values for the fitted line
x_fit = np.linspace(min(n_values), max(n_values), 500)
y_fit = inverse_func(x_fit, *popt)

# Create the scatter plot
plt.figure(figsize=(10, 6))
plt.scatter(n_values, avg_soc_over_n_minus_k_values, c='b', alpha=0.5, label='Data points')
plt.plot(x_fit, y_fit, 'r-', label='Fit: $y = a \cdot \frac{1}{n}$')
plt.xlabel('n (Number of nodes)')
plt.ylabel('Average SOC / (n - k)')
plt.title('Average SOC / (n - k) vs Number of Nodes')
plt.legend()
plt.grid(True)
plt.show()