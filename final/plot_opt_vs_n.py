"""
Plots K x 3 matrix of plots showing OPT vs n.

Last modified: 26/11/26
Author: Annalisa Calvi, Monash University
        Pierre Le Bodic, Monash University
"""

import matplotlib.pyplot as plt
import numpy as np
from typing import Literal

# ===== CONFIGURE =====
n_vs_sod_readfile = "final/n_vs_sod.csv"  # path to file (should have k, sum_of_demands columns)
est_to_show: Literal["original", "improved", "conjectured"] = "improved"

k_types = [
    "$k = 1$", "$k = 5$", "$k = \log{n}$", "$k = \sqrt{n}$", "$k = n/10$", "$k = n/4$", "$k = n/2$"
]  # what each k is, in order (in relation to n)
k_types_to_show = ["$k = 1$", "$k = \sqrt{n}$", "$k = n/2$"]  # subset of k types to plot
n_bins = 25 # the number of bins to create the average of the data
data_mean_colour = "purple"
# =====================

def binned_mean(xs: np.ndarray, ys: np.ndarray, n_bins: int):
    """Average ys within equal-width bins of xs; returns (bin centres, means), skipping empty bins."""
    edges = np.linspace(xs.min(), xs.max(), n_bins + 1)
    idx = np.clip(np.digitize(xs, edges) - 1, 0, n_bins - 1)
    sums = np.bincount(idx, weights=ys, minlength=n_bins)
    counts = np.bincount(idx, minlength=n_bins)
    centres = (edges[:-1] + edges[1:]) / 2
    nonempty = counts > 0
    return centres[nonempty], sums[nonempty] / counts[nonempty]

# read in data
dtype = [("n", int), ("k", int), ("sum_of_demands", int)]
data = np.genfromtxt(n_vs_sod_readfile, delimiter=',', dtype=dtype, names=True)

global_ns: np.ndarray = data["n"]
global_ks: np.ndarray = data["k"]
global_sods: np.ndarray = data["sum_of_demands"]

k_type_to_idx = {
    k_type: i for i, k_type in enumerate(k_types)
}

# Create the matrix of plots
fig, axs = plt.subplots(len(k_types_to_show), 3, figsize=(18, 10))


for i, k_type in enumerate(k_types_to_show):
    # determine if this is the last row
    last_row: bool = (i == len(k_types_to_show) - 1)

    # Filter data for the current k_type
    start_idx: int = k_type_to_idx[k_type]
    ns: np.ndarray = global_ns[start_idx::len(k_types)]
    ks: np.ndarray = global_ks[start_idx::len(k_types)]
    sods: np.ndarray = global_sods[start_idx::len(k_types)]

    # binned mean of the data (float to avoid integer overflow when summing)
    mean_ns, mean_sods = binned_mean(ns, sods.astype(float), n_bins)

    # calculate estimate for comparison
    strong_est = np.sqrt(ks * (ns - ks)*np.sqrt(np.pi*ns/2))
    strong_est2 = ks * (ns - ks)*np.sqrt(np.pi*ns/2)/(ns - 1)
    weak_est = ks*(ns - ks)
    conj_est = np.sqrt(ns*ks*(ns - ks))

    if est_to_show == "original":
        est = weak_est
        est2 = None
        c = "red"
    elif est_to_show == "improved":
        est = strong_est
        est2 = strong_est2
        c = "blue"
        c2 = "green"
    elif est_to_show == "conjectured":
        est = conj_est
        est2 = None
        c = "black"

    # First column: Data only (no formula values)
    axs[i, 0].scatter(ns, sods, color='grey')
    axs[i, 0].grid(True)
    axs[i, 0].ticklabel_format(style='sci', axis='y', scilimits=(0,0))
    axs[i, 0].set_ylim(bottom=0)
    if last_row:  # label bottom row only
        axs[i, 0].set_xlabel('n')
    else: 
        axs[i, 0].tick_params(axis='x', which='both', bottom=False, top=False, labelbottom=False)
    axs[i, 0].plot(mean_ns, mean_sods, color=data_mean_colour, linewidth=2, label='binned mean')

    # Second column: Data with estimate values
    axs[i, 1].scatter(ns, sods, color='grey')
    axs[i, 1].plot(ns, est, color=c)
    if est2 is not None:
        axs[i, 1].plot(ns, est2, color=c2)
    axs[i, 1].grid(True)
    axs[i, 1].ticklabel_format(style='sci', axis='y', scilimits=(0,0))
    axs[i, 1].set_ylim(bottom=0)
    if last_row:  # label bottom row only
        axs[i, 1].set_xlabel('n')
    else:
        axs[i, 1].tick_params(axis='x', which='both', bottom=False, top=False, labelbottom=False)
    axs[i, 1].plot(mean_ns, mean_sods, color=data_mean_colour, linewidth=2, label='binned mean')

    # Third column: Data with estimate values (log scale)
    axs[i, 2].scatter(ns, sods, color='grey')
    axs[i, 2].plot(ns, est, color=c)
    if est2 is not None:
        axs[i, 2].plot(ns, est2, color=c2)
    axs[i, 2].set_yscale('log')
    axs[i, 2].grid(True)
    axs[i, 2].set_ylim(bottom=1)
    if last_row:
        axs[i, 2].set_xlabel('n')
    else:
        axs[i, 2].tick_params(axis='x', which='both', bottom=False, top=False, labelbottom=False)
    axs[i, 2].plot(mean_ns, mean_sods, color=data_mean_colour, linewidth=2, label='binned mean')

# Set titles for rows and columns
for ax, col in zip(axs[0], ['Data and mean only', 'Linear y-scale', 'Logarithmic y-scale']):
    ax.set_title(col)

for ax, row in zip(axs[:, 0], k_types_to_show):
    ax.set_ylabel(row, rotation=90, size='large')

# One legend for the whole figure (top-middle panel)
#axs[0, 1].legend(loc='upper left')

plt.savefig("plot_opt_vs_n.png")