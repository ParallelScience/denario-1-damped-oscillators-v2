# filename: codebase/step_2.py
import sys
import os
sys.path.insert(0, os.path.abspath("codebase"))
import numpy as np
import matplotlib.pyplot as plt
import os
import time

def analyze_manifold():
    data_dir = "data/"
    data_path = os.path.join(data_dir, "sensitivity_analysis.npz")
    raw_data = np.load("/home/node/data/damped_oscillators.npy", allow_pickle=False)
    analysis = np.load(data_path, allow_pickle=False)
    residuals = analysis['residuals']
    t_limit = analysis['t_limit']
    pert = analysis['pert']
    osc_ids = np.unique(raw_data['oscillator_id'])
    zeta = np.array([raw_data[raw_data['oscillator_id'] == i]['damping_ratio'][0] for i in osc_ids])
    mean_residuals = np.mean(residuals, axis=3)
    hessian = np.zeros((len(osc_ids), 2, 2))
    h = pert[1] - pert[0]
    for i in range(len(osc_ids)):
        f = mean_residuals[i]
        d2f_dm2 = (f[2:, 1:-1] - 2 * f[1:-1, 1:-1] + f[:-2, 1:-1]) / (h**2)
        d2f_db2 = (f[1:-1, 2:] - 2 * f[1:-1, 1:-1] + f[1:-1, :-2]) / (h**2)
        d2f_dmd_b = (f[2:, 2:] - f[2:, :-2] - f[:-2, 2:] + f[:-2, :-2]) / (4 * h**2)
        hessian[i, 0, 0] = np.mean(d2f_dm2)
        hessian[i, 1, 1] = np.mean(d2f_db2)
        hessian[i, 0, 1] = hessian[i, 1, 0] = np.mean(d2f_dmd_b)
    timestamp = int(time.time())
    plt.figure(figsize=(8, 6))
    plt.scatter(zeta, np.mean(t_limit, axis=(1, 2)), c='blue', alpha=0.6)
    plt.xlabel("Damping Ratio (zeta)")
    plt.ylabel("Mean Time-to-Divergence (s)")
    plt.title("Model Reliability vs Damping Ratio")
    plt.grid(True)
    plt.tight_layout()
    heatmap_path = os.path.join(data_dir, "t_limit_heatmap_" + str(timestamp) + ".png")
    plt.savefig(heatmap_path, dpi=300)
    print("Saved to " + heatmap_path)
    plt.figure(figsize=(8, 6))
    plt.contourf(pert, pert, np.mean(mean_residuals, axis=0), levels=20, cmap='viridis')
    plt.colorbar(label="Mean Energy Residual (J)")
    plt.xlabel("Mass Perturbation (%)")
    plt.ylabel("Damping Perturbation (%)")
    plt.title("Valley of Degeneracy: Mean Energy Residuals")
    plt.tight_layout()
    contour_path = os.path.join(data_dir, "degeneracy_contour_" + str(timestamp) + ".png")
    plt.savefig(contour_path, dpi=300)
    print("Saved to " + contour_path)
    indices = np.argsort(zeta)
    subset = [indices[0], indices[len(indices)//2], indices[-1]]
    print("\nSummary Table: t_limit for selected oscillators")
    print("Oscillator ID | Damping Ratio | Mean t_limit (s)")
    for idx in subset:
        print(str(osc_ids[idx]) + " | " + str(round(zeta[idx], 4)) + " | " + str(round(np.mean(t_limit[idx]), 2)))

if __name__ == '__main__':
    analyze_manifold()