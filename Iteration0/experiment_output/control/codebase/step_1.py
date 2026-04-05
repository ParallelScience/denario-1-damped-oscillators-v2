# filename: codebase/step_1.py
import sys
import os
sys.path.insert(0, os.path.abspath("codebase"))
import numpy as np
import os

def get_theoretical_energy(t, m, b, omega, A, phi):
    gamma = b / (2.0 * m)
    k = m * (omega**2)
    x = A * np.exp(-gamma * t) * np.cos(omega * t + phi)
    v = -A * np.exp(-gamma * t) * (gamma * np.cos(omega * t + phi) + omega * np.sin(omega * t + phi))
    pe = 0.5 * k * (x**2)
    ke = 0.5 * m * (v**2)
    return pe + ke

if __name__ == '__main__':
    data_path = "/home/node/data/damped_oscillators.npy"
    data = np.load(data_path, allow_pickle=False)
    osc_ids = np.unique(data['oscillator_id'])
    num_oscs = len(osc_ids)
    params = {}
    baseline_residuals = np.zeros(num_oscs)
    for i, osc_id in enumerate(osc_ids):
        mask = data['oscillator_id'] == osc_id
        osc_data = data[mask]
        t = osc_data['time']
        m = osc_data['mass_kg'][0]
        b = osc_data['damping_coefficient'][0]
        omega = osc_data['natural_frequency'][0]
        A = osc_data['initial_amplitude'][0]
        phi = osc_data['initial_phase'][0]
        e_obs = osc_data['total_energy']
        e_model = get_theoretical_energy(t, m, b, omega, A, phi)
        residual = np.mean(np.abs(e_obs - e_model))
        baseline_residuals[i] = residual
        params[osc_id] = {'m': m, 'b': b, 'omega': omega, 'A': A, 'phi': phi, 'zeta': osc_data['damping_ratio'][0]}
    print("Baseline Energy Residuals (Mean Absolute Error per Oscillator):")
    for i, osc_id in enumerate(osc_ids):
        print("Oscillator " + str(osc_id) + ": " + str(baseline_residuals[i]) + " J")
    np.savez("data/processed_oscillators.npz", baseline_residuals=baseline_residuals, osc_ids=osc_ids)