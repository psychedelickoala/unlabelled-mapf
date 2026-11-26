"""
Plots 1 x 3 matrix of plots showing OPT vs k.

Last modified: 26/11/26
Author: Annalisa Calvi, Monash University
        Pierre Le Bodic, Monash University
"""

import matplotlib.pyplot as plt
import numpy as np
# ===== CONFIGURE =====
k_vs_sod_readfile = "final/k_vs_sod.csv"  # path to file (should have k, sum_of_demands columns)
n = 1_000_000  # value of n (for calculating formulas, should match data)
show_improved_est = False  # True to plot the improved upper bound, False to plot original upper bound
n_bins = 25
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
dtype = [("k", int), ("sum_of_demands", int)]
data = np.genfromtxt(k_vs_sod_readfile, delimiter=',', dtype=dtype, names=True)

ks: np.ndarray = data["k"]
sods: np.ndarray = data["sum_of_demands"]

# binned mean of the data (float to avoid integer overflow when summing)
mean_ks, mean_sods = binned_mean(ks, sods.astype(float), n_bins)

strong_est = np.sqrt(ks * (n - ks)*np.sqrt(np.pi*n/2))
strong_est2 = ks * (n - ks)*np.sqrt(np.pi*n/2)/(n - 1)
weak_est = ks * (n - ks)

est = strong_est if show_improved_est else weak_est
est2 = strong_est2 if show_improved_est else None
c = "b" if show_improved_est else "r"  # blue for improved estimate, red for old estimate
c2 = "g" if show_improved_est else None

# Create the matrix of plots
fig, axs = plt.subplots(1, 3, figsize=(18, 4))

# First column: Data only (no formula values)
axs[0].scatter(ks, sods, color='grey')

axs[0].plot(mean_ks, mean_sods, color=data_mean_colour, linewidth=2)
axs[0].set_xlabel('k')
axs[0].set_title('Data and mean only')
axs[0].grid(True)
axs[0].set_ylim(bottom=0)

# Second column: Data with estimate values
axs[1].scatter(ks, sods, color='grey')
axs[1].plot(ks, est, color=c)
if est2 is not None:
    axs[1].plot(ks, est2, color=c2)
axs[1].plot(mean_ks, mean_sods, color=data_mean_colour, linewidth=2, label='binned mean')
axs[1].set_xlabel('k')
axs[1].set_title('Linear y-scale')
axs[1].grid(True)
axs[1].set_ylim(bottom=0)

# Third column: Data with estimate values (log scale)
axs[2].scatter(ks, sods, color='grey', label='Sum of Demands')
axs[2].plot(ks, est, color=c)
if est2 is not None:
    axs[2].plot(ks, est2, color=c2)
axs[2].plot(mean_ks, mean_sods, color=data_mean_colour, linewidth=2)
axs[2].set_xlabel('k')
axs[2].set_yscale('log')
axs[2].set_title('Logarithmic y-scale')
axs[2].grid(True)
axs[2].set_ylim(bottom=1)

plt.savefig("plot_opt_vs_k.png")