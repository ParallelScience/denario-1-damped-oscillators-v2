# filename: codebase/step_1.py
import sys
import os
sys.path.insert(0, os.path.abspath("codebase"))
import numpy as np
import os

def run_sensitivity_analysis():
    """
    Performs sensitivity analysis on damped harmonic oscillators.
    Computes energy residuals and time-to-divergence metrics across a parameter grid.
    """
    data = np.load("/home/node/data/damped_oscillators.npy", allow_pickle=False)
    
    osc_ids = np.unique(data['oscillator_id'])
    num_osc = len(osc_ids)
    num_t = 500
    
    t = data['time'].reshape(num_osc, num_t)
    x = data['displacement'].reshape(num_osc, num_t)
    v = data['velocity'].reshape(num_osc, num_t)
    m_true = data['mass_kg'].reshape(num_osc, num_t)[:, 0]
    b_true = data['damping_coefficient'].reshape(num_osc, num_t)[:, 0]
    omega = data['natural_frequency'].reshape(num_osc, num_t)[:, 0]
    k_true = m_true * (omega ** 2)
    
    e_obs = 0.5 * k_true[:, np.newaxis] * (x ** 2) + 0.5 * m_true[:, np.newaxis] * (v ** 2)
    e_init = e_obs[:, 0]
    
    s_m = 1.0 + (0.5 * k_true[:, np.newaxis] * (x ** 2)) / (e_obs + 1e-15)
    s_b = - (b_true[:, np.newaxis] * t)
    
    pert = np.linspace(0.9, 1.1, 21)
    m_grid = m_true[:, np.newaxis, np.newaxis] * pert[np.newaxis, :, np.newaxis]
    b_grid = b_true[:, np.newaxis, np.newaxis] * pert[np.newaxis, np.newaxis, :]
    
    m_grid_4d = m_grid[:, :, :, np.newaxis]
    b_grid_4d = b_grid[:, :, :, np.newaxis]
    k_grid = m_grid_4d * (omega[:, np.newaxis, np.newaxis, np.newaxis] ** 2)
    
    e_model = 0.5 * k_grid * (x[:, np.newaxis, np.newaxis, :] ** 2) + 0.5 * m_grid_4d * (v[:, np.newaxis, np.newaxis, :] ** 2)
    
    residuals = np.abs(e_obs[:, np.newaxis, np.newaxis, :] - e_model)
    
    t_limit = np.full((num_osc, 21, 21), 20.0)
    for i in range(num_osc):
        for j in range(21):
            for l in range(21):
                mask = residuals[i, j, l] > (0.05 * e_init[i])
                if np.any(mask):
                    t_limit[i, j, l] = t[i, np.argmax(mask)]
                    
    np.savez_compressed(
        "data/sensitivity_analysis.npz",
        s_m=s_m,
        s_b=s_b,
        residuals=residuals,
        t_limit=t_limit,
        pert=pert
    )
    
    print("Sensitivity analysis complete. Data saved to data/sensitivity_analysis.npz")
    print("Mean t_limit across all oscillators and perturbations: " + str(np.mean(t_limit)) + " s")

if __name__ == '__main__':
    run_sensitivity_analysis()