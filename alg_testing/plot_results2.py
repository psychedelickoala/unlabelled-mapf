import csv
import matplotlib.pyplot as plt
from math import sqrt, pi, log

# Initialize lists to store the data points
n_values = []
num_of_moves_values = []

# Read the CSV file
with open("alg_testing/results2.csv", "r") as f:
    reader = csv.reader(f)
    firstrow = True
    for row in reader:
        if not firstrow:
            n = int(row[0])
            num_of_moves = int(row[1])
            n_values.append(n)
            num_of_moves_values.append(num_of_moves)
        else:
            firstrow = False

# Function to calculate moving average
def moving_average(data, window_size):
    return [sum(data[i:i+window_size]) / window_size for i in range(len(data) - window_size + 1)]

# Apply moving average to the data
window_size = 20  # You can adjust the window size as needed
smoothed_num_of_moves_values = moving_average(num_of_moves_values, window_size)
smoothed_n_values = n_values[:len(smoothed_num_of_moves_values)]

# Create the scatter plot
plt.figure(figsize=(10, 6))
plt.plot(smoothed_n_values, smoothed_num_of_moves_values, marker='.', linestyle='', color='b', label='Number of Moves (Smoothed)')

# Calculate and plot the formula (n/2)*sqrt(sqrt(pi*n/2) - 1)
formula_values = [(n/2) * sqrt(sqrt(sqrt(pi * n / 2) - 1))*1.25 for n in smoothed_n_values]
plt.plot(smoothed_n_values, formula_values, linestyle='-', color='r', label=r'$(n/2) \cdot \sqrt{\sqrt{\pi n / 2} - 1}$')

plt.xlabel('n')
plt.ylabel('Number of Moves')
plt.title('n vs Number of Moves')
plt.legend()
plt.grid(True)
plt.show()