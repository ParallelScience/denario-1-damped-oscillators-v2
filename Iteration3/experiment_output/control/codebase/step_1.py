# filename: codebase/step_1.py
import sys
import os
sys.path.insert(0, os.path.abspath("codebase"))
import numpy as np
import json
from scipy.optimize import minimize

def estimate_noise(data):
    dx = np.diff(data['displacement'])
    dv = np.diff(data['velocity'])
    sigma_x = 1.4826 * np.median(np.abs(dx - np.median(dx)))
    sigma_v = 1.4826 * np.median(np.abs(dv - np.median(dv)))
    return sigma_x**2, sigma_v**2

def energy_model(t, m, b, omega, A, phi):
    gamma = b / (2.0 * m)
    return 0.5 * m * (A**2) * np.exp(-2.0 * gamma * t)

def run_analysis():
    data = np.load("/home/node/data/damped_oscillators.npy", allow_pickle=False)
    sig2_x, sig2_v = estimate_noise(data)
    osc_ids = np.unique(data['oscillator_id'])
    results = {}
    summary = {}
    for oid in osc_ids:
        mask = data['oscillator_id'] == oid
        d = data[mask]
        t, x, v = d['time'], d['displacement'], d['velocity']
        m_true, b_true, omega = d['mass_kg'][0], d['damping_coefficient'][0], d['natural_frequency'][0]
        E_obs = 0.5 * m_true * v**2 + 0.5 * (m_true * omega**2) * x**2
        sig2_E = (m_true * v)**2 * sig2_v + (m_true * omega**2 * x)**2 * sig2_x
        dE_dm = 0.5 * (v**2 + omega**2 * x**2)
        dE_db = - (t / m_true) * E_obs
        fim = np.zeros((2, 2))
        fim[0, 0] = np.sum(dE_dm**2 / sig2_E)
        fim[0, 1] = np.sum((dE_dm * dE_db) / sig2_E)
        fim[1, 0] = fim[0, 1]
        fim[1, 1] = np.sum(dE_db**2 / sig2_E)
        crlb = np.linalg.inv(fim + 1e-12 * np.eye(2))
        m_ests, b_ests = [], []
        for i in range(10, len(t), 10):
            def obj(params):
                m, b = params
                if m <= 0 or b <= 0: return 1e9
                pred = energy_model(t[:i], m, b, omega, d['initial_amplitude'][0], d['initial_phase'][0])
                return np.sum((E_obs[:i] - pred)**2)
            res = minimize(obj, [m_true, b_true], method='Nelder-Mead', tol=1e-3)
            m_ests.append(res.x[0])
            b_ests.append(res.x[1])
        results[str(oid)] = {'crlb': crlb.tolist(), 'm_est': m_ests, 'b_est': b_ests}
        summary[str(oid)] = {'mean_m': np.mean(m_ests), 'std_m': np.std(m_ests), 'mean_b': np.mean(b_ests), 'std_b': np.std(b_ests)}
    np.savez("data/analysis_results.npz", **results)
    with open("data/summary_stats.json", "w") as f:
        json.dump(summary, f)
    print("Analysis complete. Summary statistics:")
    for oid, stats in summary.items():
        print("Oscillator " + oid + ": Mean m=" + str(round(stats['mean_m'], 4)) + ", Mean b=" + str(round(stats['mean_b'], 4)))

if __name__ == '__main__':
    run_analysis()