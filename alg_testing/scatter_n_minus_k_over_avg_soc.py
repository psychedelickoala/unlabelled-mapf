import csv
import numpy as np
import matplotlib.pyplot as plt

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
        if position != 1 and n > 0 and avg_soc != 0:
            n_minus_k_over_avg_soc = (n - k) / avg_soc
            data_points.append((n, n_minus_k_over_avg_soc))

# Ensure there are enough data points to plot
if len(data_points) < 2:
    raise ValueError("Not enough data points to plot.")

# Separate the data points into x and y values
n_values, n_minus_k_over_avg_soc_values = zip(*data_points)

# Create the scatter plot
plt.figure(figsize=(10, 6))
plt.scatter(n_values, n_minus_k_over_avg_soc_values, c='b', alpha=0.5, label='Data points')
plt.xlabel('n (Number of nodes)')
plt.ylabel('(n - k) / avg_soc')
plt.title('(n - k) / avg_soc vs Number of Nodes')
plt.legend()
plt.grid(True)
plt.show()