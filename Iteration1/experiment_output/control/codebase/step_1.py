# filename: codebase/step_1.py
import sys
import os
sys.path.insert(0, os.path.abspath("codebase"))
import numpy as np
import os

def calculate_noise_floor(total_energy, window_size=10):
    n = len(total_energy)
    noise_floor = np.zeros(n)
    for i in range(n):
        start = max(0, i - window_size // 2)
        end = min(n, i + window_size // 2)
        noise_floor[i] = np.std(total_energy[start:end])
    return noise_floor

def get_jacobian(m, b, omega, x, v, t):
    dE_dm = 0.5 * (v**2 + (omega**2) * (x**2))
    dE_db = np.zeros_like(m)
    return np.stack([dE_dm, dE_db], axis=0)

def compute_td(osc_data, delta_m, delta_b, noise_floor):
    m = osc_data['mass_kg'][0]
    b = osc_data['damping_coefficient'][0]
    omega = osc_data['natural_frequency'][0]
    x = osc_data['displacement']
    v = osc_data['velocity']
    m_new = m * (1 + delta_m)
    e_obs = osc_data['total_energy']
    e_model = 0.5 * m_new * (v**2 + (omega**2) * (x**2))
    diff = np.abs(e_obs - e_model)
    low = 0
    high = len(osc_data) - 1
    td_idx = high
    while low <= high:
        mid = (low + high) // 2
        if diff[mid] > noise_floor[mid]:
            td_idx = mid
            high = mid - 1
        else:
            low = mid + 1
    return osc_data['time'][td_idx]

if __name__ == '__main__':
    data = np.load("/home/node/data/damped_oscillators.npy", allow_pickle=False)
    osc_ids = np.unique(data['oscillator_id'])
    noise_floors = {}
    jacobians = {}
    td_results = {}
    delta_range = np.linspace(-0.1, 0.1, 5)
    for oid in osc_ids:
        mask = data['oscillator_id'] == oid
        osc = data[mask]
        nf = calculate_noise_floor(osc['total_energy'])
        noise_floors[oid] = nf
        jac = get_jacobian(osc['mass_kg'], osc['damping_coefficient'], osc['natural_frequency'], osc['displacement'], osc['velocity'], osc['time'])
        jacobians[oid] = jac
        td_grid = np.zeros((len(delta_range), len(delta_range)))
        for i, dm in enumerate(delta_range):
            for j, db in enumerate(delta_range):
                td_grid[i, j] = compute_td(osc, dm, db, nf)
        td_results[oid] = td_grid
    np.savez("data/step_1_results.npz", noise_floors=noise_floors, jacobians=jacobians, td_results=td_results)
    print("Saved to data/step_1_results.npz")