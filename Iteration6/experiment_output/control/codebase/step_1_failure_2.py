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
    m_true = data['mass_kg'].reshape(20, 1)
    k_true = data['spring_constant'].reshape(20, 1)
    b_true = data['damping_coefficient'].reshape(20, 1)
    omega = data['natural_frequency'].reshape(20, 1)
    gamma = b_true / (2 * m_true)
    A = data['initial_amplitude'].reshape(20, 1)
    phi = data['initial_phase'].reshape(20, 1)
    x_model = A * np.exp(-gamma * t) * np.cos(omega * t + phi)
    v_model = A * np.exp(-gamma * t) * (-gamma * np.cos(omega * t + phi) - omega * np.sin(omega * t + phi))
    res_x = x_obs - x_model
    res_v = v_obs - v_model
    var_x = np.var(res_x)
    var_v = np.var(res_v)
    sigma_E = np.sqrt((m_true * v_model)**2 * var_v + (k_true * x_model)**2 * var_x)
    m_grid = np.linspace(0.9, 1.1, 21)
    b_grid = np.linspace(0.9, 1.1, 21)
    m_vals = m_true[:, np.newaxis, :, np.newaxis] * m_grid[np.newaxis, np.newaxis, :, np.newaxis]
    b_vals = b_true[:, np.newaxis, np.newaxis, :] * b_grid[np.newaxis, np.newaxis, np.newaxis, :]
    k_vals = m_vals * (omega[:, np.newaxis, np.newaxis, np.newaxis]**2)
    E_obs = data['total_energy'].reshape(20, 500, 1, 1)
    E_model = 0.5 * m_vals * v_model[:, :, np.newaxis, np.newaxis]**2 + 0.5 * k_vals * x_model[:, :, np.newaxis, np.newaxis]**2
    rel_res = np.abs(E_obs - E_model) / (E_obs + 1e-12)
    dE_dm = 0.5 * v_model[:, :, np.newaxis, np.newaxis]**2 + 0.5 * (omega[:, np.newaxis, np.newaxis, np.newaxis]**2) * x_model[:, :, np.newaxis, np.newaxis]**2
    dE_db = np.zeros_like(dE_dm)
    J = np.stack([dE_dm, dE_db], axis=-1)
    U, S, Vh = np.linalg.svd(J, full_matrices=False)
    cond_num = S[..., 0] / (S[..., 1] + 1e-12)
    t_crit = np.zeros((20, 21, 21))
    for i in range(20):
        for j in range(21):
            for k in range(21):
                exceed = np.abs(E_obs[i, :, j, k] - E_model[i, :, j, k]) > sigma_E[i, :]
                idx = np.where(exceed)[0]
                t_crit[i, j, k] = t[i, idx[0]] if len(idx) > 0 else 20.0
    np.savez("data/sensitivity_analysis.npz", rel_res=rel_res, cond_num=cond_num, t_crit=t_crit, sigma_E=sigma_E)
    print("Analysis complete.")
    print("Global displacement variance: " + str(var_x))
    print("Global velocity variance: " + str(var_v))
    print("Mean condition number: " + str(np.mean(cond_num)))
    print("Mean critical time: " + str(np.mean(t_crit)))

if __name__ == '__main__':
    run_sensitivity_analysis()