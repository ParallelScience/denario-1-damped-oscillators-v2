# filename: codebase/step_2.py
import sys
import os
sys.path.insert(0, os.path.abspath("codebase"))
import numpy as np
import json
import matplotlib.pyplot as plt
from scipy.stats import pearsonr
import time

def run_visualization():
    data = np.load("/home/node/data/damped_oscillators.npy", allow_pickle=False)
    results = np.load("data/analysis_results.npz", allow_pickle=True)
    with open("data/summary_stats.json", "r") as f:
        summary = json.load(f)
    osc_ids = np.unique(data['oscillator_id'])
    zeta_vals = []
    th_vals = []
    for oid in osc_ids:
        mask = data['oscillator_id'] == oid
        zeta = data[mask]['damping_ratio'][0]
        b_true = data[mask]['damping_coefficient'][0]
        res = results[str(oid)].item()
        crlb_b = np.array(res['crlb'])[1, 1]
        th = 0.0
        if crlb_b < 0.1 * b_true:
            th = 1.0
        else:
            th = 20.0
        zeta_vals.append(zeta)
        th_vals.append(th)
    corr, _ = pearsonr(zeta_vals, th_vals)
    print("Pearson correlation between damping ratio and Information Horizon: " + str(round(corr, 4)))
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    axes[0, 0].scatter(zeta_vals, th_vals, color='blue', alpha=0.6)
    axes[0, 0].set_xlabel("Damping Ratio")
    axes[0, 0].set_ylabel("Information Horizon (s)")
    axes[0, 0].set_title("Correlation: Damping vs Horizon")
    axes[0, 0].grid(True)
    for i, oid in enumerate(osc_ids[:5]):
        res = results[str(oid)].item()
        b_ests = res['b_est']
        axes[0, 1].plot(np.linspace(1, 20, len(b_ests)), b_ests, label="Osc " + str(oid))
    axes[0, 1].set_xlabel("Time (s)")
    axes[0, 1].set_ylabel("Estimated b (kg/s)")
    axes[0, 1].set_title("Evolution of b Estimates")
    axes[0, 1].legend(fontsize='small', ncol=2)
    axes[0, 1].grid(True)
    axes[1, 0].hist(zeta_vals, bins=10, color='green', alpha=0.7)
    axes[1, 0].set_xlabel("Damping Ratio")
    axes[1, 0].set_ylabel("Count")
    axes[1, 0].set_title("Distribution of Damping Ratios")
    axes[1, 0].grid(True)
    axes[1, 1].text(0.1, 0.5, "Correlation: " + str(round(corr, 4)), fontsize=12)
    axes[1, 1].axis('off')
    plt.tight_layout()
    plot_path = "data/sensitivity_analysis_" + str(int(time.time())) + ".png"
    plt.savefig(plot_path, dpi=300)
    print("Plot saved to " + plot_path)

if __name__ == '__main__':
    run_visualization()