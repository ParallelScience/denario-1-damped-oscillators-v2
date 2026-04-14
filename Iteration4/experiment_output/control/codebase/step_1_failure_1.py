# filename: codebase/step_1.py
import sys
import os
sys.path.insert(0, os.path.abspath("codebase"))
import numpy as np
from scipy.optimize import curve_fit

def model_func(t, gamma, omega, A, phi):
    """Theoretical displacement model for a damped harmonic oscillator."""
    return A * np.exp(-gamma * t) * np.cos(omega * t + phi)

def jacobian(t, gamma, omega, A, phi):
    """Analytical Jacobian for the displacement model."""
    exp_term = np.exp(-gamma * t)
    cos_term = np.cos(omega * t + phi)
    sin_term = np.sin(omega * t + phi)
    df_dgamma = -t * A * exp_term * cos_term
    df_domega = -t * A * exp_term * sin_term
    df_dA = exp_term * cos_term
    df_dphi = -A * exp_term * sin_term
    return np.stack([df_dgamma, df_domega, df_dA, df_dphi], axis=1)

if __name__ == '__main__':
    data = np.load("/home/node/data/damped_oscillators.npy", allow_pickle=False)
    osc_ids = np.unique(data['oscillator_id'])
    n_osc = len(osc_ids)
    n_t = 500
    residuals_var = np.zeros(n_osc)
    sensitivity_matrix = np.zeros((n_osc, 2, 2))
    fisher_info_rate = np.zeros((n_osc, n_t))
    energy_residuals = np.zeros((n_osc, n_t, 2, 2))
    for i, oid in enumerate(osc_ids):
        mask = data['oscillator_id'] == oid
        osc = data[mask]
        t = osc['time']
        x_obs = osc['displacement']
        p0 = [osc['damping_coefficient'][0] / (2 * osc['mass_kg'][0]), osc['natural_frequency'][0], osc['initial_amplitude'][0], osc['initial_phase'][0]]
        popt, pcov = curve_fit(model_func, t, x_obs, p0=p0, jac=jacobian)
        residuals = x_obs - model_func(t, *popt)
        residuals_var[i] = np.var(residuals)
        m_true = osc['mass_kg'][0]
        b_true = osc['damping_coefficient'][0]
        for m_idx, m_pert in enumerate([0.9 * m_true, 1.1 * m_true]):
            for b_idx, b_pert in enumerate([0.9 * b_true, 1.1 * b_true]):
                gamma_p = b_pert / (2 * m_pert)
                omega_p = np.sqrt(osc['spring_constant'][0] / m_pert)
                e_model = 0.5 * m_pert * (osc['velocity']**2) + 0.5 * osc['spring_constant'][0] * (model_func(t, gamma_p, omega_p, popt[2], popt[3])**2)
                energy_residuals[i, :, m_idx, b_idx] = np.abs(osc['total_energy'] - e_model)
        J = jacobian(t, *popt)
        F = (J.T @ J) / (residuals_var[i] + 1e-12)
        fisher_info_rate[i] = np.gradient(np.trace(F[:2, :2]))
        sensitivity_matrix[i, 0, 0] = np.mean(np.abs(np.gradient(np.log(osc['total_energy'] + 1e-9)) / np.gradient(np.log(np.full_like(t, m_true) + 1e-9))))
        sensitivity_matrix[i, 1, 1] = np.mean(np.abs(np.gradient(np.log(osc['total_energy'] + 1e-9)) / np.gradient(np.log(np.full_like(t, b_true) + 1e-9))))
    np.savez("data/analysis_results.npz", residuals_var=residuals_var, sensitivity_matrix=sensitivity_matrix, fisher_info_rate=fisher_info_rate, energy_residuals=energy_residuals)
    print("Saved to data/analysis_results.npz")