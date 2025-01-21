import csv

# Read the existing data
rows = []
with open("alg_testing/results.csv", "r") as f:
    reader = csv.reader(f)
    header = next(reader)
    rows.append(header + ["position"])
    
    position = 1
    for row in reader:
        rows.append(row + [str(position)])
        position = position % 10 + 1

# Write the updated data back to the CSV file
with open("alg_testing/results.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerows(rows)