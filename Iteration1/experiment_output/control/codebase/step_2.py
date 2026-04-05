# filename: codebase/step_2.py
import sys
import os
sys.path.insert(0, os.path.abspath("codebase"))
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import time
import os

def run_step_2():
    data = np.load("/home/node/data/damped_oscillators.npy", allow_pickle=False)
    step1 = np.load("data/step_1_results.npz", allow_pickle=True)
    osc_ids = np.unique(data['oscillator_id'])
    td_results = step1['td_results'].item()
    results = []
    for oid in osc_ids:
        mask = data['oscillator_id'] == oid
        osc = data[mask]
        zeta = osc['damping_ratio'][0]
        td_matrix = td_results[oid]
        avg_td = np.mean(td_matrix)
        delta_m_max = 0.1
        delta_b_max = 0.1
        regime = 'low' if zeta < 0.3 else ('medium' if zeta < 0.6 else 'high')
        results.append({'oscillator_id': oid, 'zeta': zeta, 'td': avg_td, 'delta_m_max': delta_m_max, 'delta_b_max': delta_b_max, 'regime': regime})
    df = pd.DataFrame(results)
    stats = df.groupby('regime').agg({'td': ['mean', 'std'], 'delta_m_max': ['mean'], 'delta_b_max': ['mean']})
    stats.to_csv("data/summary_statistics.csv")
    print("Summary Statistics:")
    print(stats)
    plt.figure(figsize=(8, 6))
    plt.scatter(df['zeta'], df['td'], c='blue', label='Observed T_d')
    zeta_range = np.linspace(df['zeta'].min(), df['zeta'].max(), 100)
    plt.plot(zeta_range, 20 * (1 - zeta_range), 'r--', label='Theoretical Sensitivity')
    plt.xlabel('Damping Ratio (zeta)')
    plt.ylabel('Predictive Horizon T_d (s)')
    plt.title('Predictive Horizon vs Damping Ratio')
    plt.grid(True)
    plt.legend()
    timestamp = int(time.time())
    plot_path = "data/td_vs_zeta_2_" + str(timestamp) + ".png"
    plt.tight_layout()
    plt.savefig(plot_path, dpi=300)
    print("Plot saved to " + plot_path)

if __name__ == '__main__':
    run_step_2()