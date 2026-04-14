# filename: codebase/step_2.py
import sys
import os
sys.path.insert(0, os.path.abspath("codebase"))
import numpy as np
import matplotlib.pyplot as plt
import datetime
import os
import time

def generate_summary_and_plots():
    data_raw = np.load("/home/node/data/damped_oscillators.npy", allow_pickle=False)
    results = np.load("data/analysis_results.npz")
    sensitivity_matrix = results['sensitivity_matrix']
    fisher_info_rate = results['fisher_info_rate']
    energy_residuals = results['energy_residuals']
    osc_ids = np.unique(data_raw['oscillator_id'])
    damping_ratios = np.array([data_raw[data_raw['oscillator_id'] == oid]['damping_ratio'][0] for oid in osc_ids])
    bins = np.percentile(damping_ratios, [33.3, 66.6])
    regimes = np.digitize(damping_ratios, bins)
    print("Summary Statistics of Logarithmic Sensitivity (Mass, Damping):")
    print("Regime | Mean S_m | Std S_m | Mean S_b | Std S_b")
    for r in range(3):
        mask = regimes == r
        s_m = sensitivity_matrix[mask, 0, 0]
        s_b = sensitivity_matrix[mask, 1, 1]
        print(str(r) + " | " + str(round(np.mean(s_m), 4)) + " | " + str(round(np.std(s_m), 4)) + " | " + str(round(np.mean(s_b), 4)) + " | " + str(round(np.std(s_b), 4)))
    fig, axes = plt.subplots(2, 1, figsize=(10, 10))
    time_arr = np.linspace(0, 20, 500)
    im = axes[0].imshow(np.mean(energy_residuals, axis=(2, 3)).T, aspect='auto', extent=[0, 20, 0, 20], origin='lower', cmap='viridis')
    axes[0].set_title("Energy Residual Heatmap (Oscillator ID vs Time)")
    axes[0].set_xlabel("Time (s)")
    axes[0].set_ylabel("Oscillator ID")
    plt.colorbar(im, ax=axes[0], label="Energy Residual (J)")
    axes[1].plot(time_arr, np.mean(fisher_info_rate, axis=0), color='red', lw=2)
    axes[1].set_title("Average Fisher Information Rate Decay")
    axes[1].set_xlabel("Time (s)")
    axes[1].set_ylabel("Fisher Info Rate")
    axes[1].grid(True)
    plt.tight_layout()
    timestamp = int(time.time())
    filename = "data/sensitivity_analysis_1_" + str(timestamp) + ".png"
    plt.savefig(filename, dpi=300)
    print("Plot saved to " + filename)

if __name__ == '__main__':
    generate_summary_and_plots()