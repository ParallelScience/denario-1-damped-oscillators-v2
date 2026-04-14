# filename: codebase/step_1.py
import sys
import os
sys.path.insert(0, os.path.abspath("codebase"))
import numpy as np
import os

def run_sensitivity_analysis():
    data = np.load("/home/node/data/damped_oscillators.npy", allow_pickle=False)
    t = data['time'].reshape(20, 500)
    x_obs = data['displacement'].reshape(20, 500)
    v_obs = data['velocity'].reshape(20, 500)
    params = data[::500]
    m_true = params['mass_kg'].reshape(20, 1, 1, 1)
    k_true = params['spring_constant'].reshape(20, 1, 1, 1)
    b_true = params['damping_coefficient'].reshape(20, 1, 1, 1)
    omega = params['natural_frequency'].reshape(20, 1, 1, 1)
    gamma = b_true / (2 * m_true)
    A = params['initial_amplitude'].reshape(20, 1, 1, 1)
    phi = params['initial_phase'].reshape(20, 1, 1, 1)
    exp_term = np.exp(-gamma * t[:, :, np.newaxis, np.newaxis])
    cos_term = np.cos(omega * t[:, :, np.newaxis, np.newaxis] + phi)
    sin_term = np.sin(omega * t[:, :, np.newaxis, np.newaxis] + phi)
    x_model = A * exp_term * cos_term
    v_model = A * exp_term * (-gamma * cos_term - omega * sin_term)
    dE_dm = 0.5 * v_model**2 + 0.5 * (omega**2) * x_model**2
    dE_db = -0.5 * t[:, :, np.newaxis, np.newaxis] * v_model**2 / m_true
    m_grid = np.linspace(0.9, 1.1, 21).reshape(1, 1, 21, 1)
    b_grid = np.linspace(0.9, 1.1, 21).reshape(1, 1, 1, 21)
    m_vals = m_true * m_grid
    b_vals = b_true * b_grid
    k_vals = m_vals * (omega**2)
    E_obs = data['total_energy'].reshape(20, 500, 1, 1)
    E_model = 0.5 * m_vals * v_model**2 + 0.5 * k_vals * x_model**2
    rel_res = np.abs(E_obs - E_model) / (E_obs + 1e-12)
    a = dE_dm**2
    b = dE_dm * dE_db
    c = dE_db**2
    det = a * c - b**2
    trace = a + c
    l1 = (trace + np.sqrt(np.maximum(trace**2 - 4 * det, 0))) / 2
    l2 = (trace - np.sqrt(np.maximum(trace**2 - 4 * det, 0))) / 2
    cond_num = np.sqrt(l1 / (l2 + 1e-12))
    sigma_E = np.sqrt((m_true.reshape(20, 1) * v_model.reshape(20, 500))**2 * np.var(x_obs - x_model.reshape(20, 500)) + (k_true.reshape(20, 1) * x_model.reshape(20, 500))**2 * np.var(v_obs - v_model.reshape(20, 500)))
    t_crit = np.zeros((20, 21, 21))
    for i in range(20):
        for j in range(21):
            for k in range(21):
                exceed = np.abs(E_obs[i, :, j, k] - E_model[i, :, j, k]) > sigma_E[i, :]
                idx = np.where(exceed)[0]
                t_crit[i, j, k] = t[i, idx[0]] if len(idx) > 0 else 20.0
    np.savez("data/sensitivity_analysis.npz", rel_res=rel_res, cond_num=cond_num, t_crit=t_crit)
    print("Analysis complete.")
    print("Mean condition number: " + str(np.mean(cond_num)))
    print("Mean critical time: " + str(np.mean(t_crit)))

if __name__ == '__main__':
    run_sensitivity_analysis()