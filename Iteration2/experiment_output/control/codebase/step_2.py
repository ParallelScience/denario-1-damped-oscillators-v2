# filename: codebase/step_2.py
import sys
import os
sys.path.insert(0, os.path.abspath("codebase"))
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import linregress

def analyze_sensitivity():
    data_path = "data/processed_sensitivity.npy"
    raw_data = np.load(data_path)
    orig_data = np.load("/home/node/data/damped_oscillators.npy")
    osc_ids = np.unique(raw_data['oscillator_id'])
    n_osc = len(osc_ids)
    damping_ratios = np.array([np.mean(orig_data['damping_ratio'][orig_data['oscillator_id'] == oid]) for oid in osc_ids])
    t_h_list = []
    peak_s_list = []
    heatmap_data = np.zeros((n_osc, 500))
    for i, oid in enumerate(osc_ids):
        mask = raw_data['oscillator_id'] == oid
        osc = raw_data[mask]
        t = osc['time']
        s_m = osc['S_m']
        s_b = osc['S_b']
        s_total = osc['S_total']
        heatmap_data[i, :] = s_total
        peak_s_list.append(np.max(s_total))
        ratio = s_b / (s_m + 1e-12)
        crossings = np.where(np.diff(np.sign(ratio - 1.0)))[0]
        t_h = t[crossings[0]] if len(crossings) > 0 else t[-1]
        t_h_list.append(t_h)
    t_h_list = np.array(t_h_list)
    peak_s_list = np.array(peak_s_list)
    print("Oscillator Summary Table:")
    print("ID | Damping Ratio | T_H (s) | Peak Sensitivity")
    for i in range(n_osc):
        print(str(osc_ids[i]) + " | " + str(round(damping_ratios[i], 4)) + " | " + str(round(t_h_list[i], 2)) + " | " + str(round(peak_s_list[i], 2)))
    slope, intercept, r_val, _, _ = linregress(damping_ratios, t_h_list)
    corr_peak = np.corrcoef(damping_ratios, peak_s_list)[0, 1]
    print("\nRegression Results:")
    print("T_H vs Damping Ratio: slope=" + str(round(slope, 4)) + ", r_squared=" + str(round(r_val**2, 4)))
    print("Correlation (Peak Sensitivity vs Damping): " + str(round(corr_peak, 4)))
    plt.figure(figsize=(10, 6))
    plt.imshow(heatmap_data, aspect='auto', extent=[0, 20, 1, 20], cmap='viridis')
    plt.colorbar(label='Sensitivity Index S(t)')
    plt.xlabel('Time (s)')
    plt.ylabel('Oscillator ID')
    plt.title('Sensitivity Index Heatmap')
    plt.tight_layout()
    plt.savefig('data/sensitivity_heatmap_1739965000.png', dpi=300)
    print("Saved to data/sensitivity_heatmap_1739965000.png")
    plt.figure(figsize=(10, 6))
    for i in range(n_osc):
        mask = raw_data['oscillator_id'] == osc_ids[i]
        plt.plot(raw_data['time'][mask], raw_data['S_m'][mask], 'b-', alpha=0.1)
        plt.plot(raw_data['time'][mask], raw_data['S_b'][mask], 'r-', alpha=0.1)
    plt.xlabel('Time (s)')
    plt.ylabel('Sensitivity')
    plt.title('Evolution of S_m (blue) and S_b (red)')
    plt.tight_layout()
    plt.savefig('data/sensitivity_evolution_1739965000.png', dpi=300)
    print("Saved to data/sensitivity_evolution_1739965000.png")

if __name__ == '__main__':
    analyze_sensitivity()