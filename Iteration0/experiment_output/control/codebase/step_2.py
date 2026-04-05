# filename: codebase/step_2.py
import sys
import os
sys.path.insert(0, os.path.abspath("codebase"))
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import spearmanr
from step_1 import get_theoretical_energy

def compute_sensitivity():
    data = np.load("/home/node/data/damped_oscillators.npy", allow_pickle=False)
    processed = np.load("data/processed_oscillators.npz")
    osc_ids = processed['osc_ids']
    num_oscs = len(osc_ids)
    grid_size = 10
    all_gradients = []
    damping_ratios = []
    min_zeta_idx = -1
    max_zeta_idx = -1
    min_zeta = 2.0
    max_zeta = -1.0
    results_manifold = np.zeros((num_oscs, grid_size, grid_size))
    for i, osc_id in enumerate(osc_ids):
        mask = data['oscillator_id'] == osc_id
        osc_data = data[mask]
        t = osc_data['time']
        e_obs = osc_data['total_energy']
        m_true = osc_data['mass_kg'][0]
        b_true = osc_data['damping_coefficient'][0]
        omega = osc_data['natural_frequency'][0]
        A = osc_data['initial_amplitude'][0]
        phi = osc_data['initial_phase'][0]
        zeta = osc_data['damping_ratio'][0]
        damping_ratios.append(zeta)
        if zeta < min_zeta:
            min_zeta = zeta
            min_zeta_idx = i
        if zeta > max_zeta:
            max_zeta = zeta
            max_zeta_idx = i
        m_range = np.linspace(0.9 * m_true, 1.1 * m_true, grid_size)
        b_range = np.linspace(0.9 * b_true, 1.1 * b_true, grid_size)
        residuals = np.zeros((grid_size, grid_size))
        for mi, m_val in enumerate(m_range):
            for bi, b_val in enumerate(b_range):
                e_model = get_theoretical_energy(t, m_val, b_val, omega, A, phi)
                residuals[mi, bi] = np.mean(np.abs(e_obs - e_model) / (e_obs + 1e-9))
        results_manifold[i] = residuals
        grad_m, grad_b = np.gradient(residuals)
        grad_mag = np.sqrt(grad_m**2 + grad_b**2).mean()
        all_gradients.append(grad_mag)
    corr, _ = spearmanr(all_gradients, damping_ratios)
    print("Sensitivity Analysis Results:")
    print("Spearman Rank Correlation (Gradient Magnitude vs Damping Ratio): " + str(corr))
    print("Mean Gradient Magnitude: " + str(np.mean(all_gradients)))
    for idx in [min_zeta_idx, max_zeta_idx]:
        plt.figure(figsize=(8, 6))
        plt.imshow(results_manifold[idx], extent=[0.9*b_true, 1.1*b_true, 0.9*m_true, 1.1*m_true], origin='lower', aspect='auto')
        plt.colorbar(label='Relative Energy Residual')
        plt.xlabel('Damping Coefficient (kg/s)')
        plt.ylabel('Mass (kg)')
        plt.title('Energy Residual Manifold (Oscillator ' + str(osc_ids[idx]) + ', Zeta=' + str(round(damping_ratios[idx], 4)) + ')')
        plt.tight_layout()
        fname = "data/sensitivity_heatmap_" + str(idx) + "_1.png"
        plt.savefig(fname, dpi=300)
        print("Heatmap saved to " + fname)

if __name__ == '__main__':
    compute_sensitivity()