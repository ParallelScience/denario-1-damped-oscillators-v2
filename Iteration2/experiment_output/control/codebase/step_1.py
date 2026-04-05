# filename: codebase/step_1.py
import sys
import os
sys.path.insert(0, os.path.abspath("codebase"))
import numpy as np
from scipy.signal import savgol_filter

def compute_sensitivity():
    """
    Loads damped oscillator data, computes theoretical energy, applies smoothing,
    and calculates sensitivity indices based on analytical derivatives.
    """
    data_path = "/home/node/data/damped_oscillators.npy"
    data = np.load(data_path, allow_pickle=False)
    
    osc_ids = np.unique(data['oscillator_id'])
    
    processed_data = np.zeros(len(data), dtype=[
        ('oscillator_id', 'i4'),
        ('time', 'f8'),
        ('E_model', 'f8'),
        ('epsilon', 'f8'),
        ('S_m', 'f8'),
        ('S_b', 'f8'),
        ('S_total', 'f8')
    ])
    
    eta = 1e-4
    
    for oid in osc_ids:
        mask = data['oscillator_id'] == oid
        osc = data[mask]
        
        t = osc['time']
        m = osc['mass_kg'][0]
        k = osc['spring_constant'][0]
        b = osc['damping_coefficient'][0]
        A = osc['initial_amplitude'][0]
        gamma = b / (2 * m)
        
        E_0 = 0.5 * k * (A**2)
        E_model = E_0 * np.exp(-2 * gamma * t)
        
        E_obs_raw = osc['total_energy']
        E_obs_smooth = savgol_filter(E_obs_raw, window_length=21, polyorder=3)
        
        epsilon = np.abs(E_obs_smooth - E_model) / (E_model + eta)
        
        dE_dm = (E_model / m) * (1 - 2 * gamma * t)
        dE_db = - (E_model / m) * t
        
        S_m = np.abs(dE_dm)
        S_b = np.abs(dE_db)
        S_total = np.sqrt(S_m**2 + S_b**2)
        
        processed_data['oscillator_id'][mask] = oid
        processed_data['time'][mask] = t
        processed_data['E_model'][mask] = E_model
        processed_data['epsilon'][mask] = epsilon
        processed_data['S_m'][mask] = S_m
        processed_data['S_b'][mask] = S_b
        processed_data['S_total'][mask] = S_total
        
    np.save("data/processed_sensitivity.npy", processed_data)
    print("Processed sensitivity data saved to data/processed_sensitivity.npy")

if __name__ == '__main__':
    compute_sensitivity()