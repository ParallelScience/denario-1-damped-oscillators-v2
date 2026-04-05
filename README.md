# Quantifying the Temporal Limits of Parameter Identifiability in Damped Harmonic Oscillators

**Scientist:** denario-1 (Denario AI Research Scientist)
**Date:** 2026-04-05
**Best iteration:** 2

**[View Paper & Presentation](https://ParallelScience.github.io/denario-1-damped-oscillators-v2/)**

## Abstract

The reliability of energy dissipation models for physical systems is fundamentally limited by uncertainty in key parameters like mass and damping. This study quantifies the robustness of such models by investigating the temporal sensitivity of the total energy manifold to parameter perturbations in underdamped harmonic oscillators. Analyzing a population of 20 simulated oscillators, we employ a Jacobian-based sensitivity analysis to map how uncertainty contributions from mass and damping evolve over time. Our results demonstrate that sensitivity is highest during the initial transient phase and that a rapid transition occurs where the dominant source of uncertainty shifts from mass to the damping coefficient. We define this transition as the "Information Horizon," which occurs at a mean time of 0.76 seconds across the population. We establish that higher damping ratios are linked to an earlier Information Horizon and lower peak sensitivity, indicating that while low-damping systems are more susceptible to parameter errors, high-damping systems possess a more constrained temporal window for reliable mass identification. Ultimately, this work provides a quantitative framework for understanding the time-dependent limits of parameter identifiability in damped systems.

## Repository Structure

- `paper.tex` / `paper.pdf` — Final paper (from best iteration)
- `presentation.mp3` — Audio presentation
- `docs/` — GitHub Pages site
- `Iteration*/` — Research iterations (idea → methods → results → evaluation)
- `data_description.md` — Dataset schema and documentation

---

# Damped Harmonic Oscillator Dataset

## File location

The dataset is a NumPy structured array saved at:

    /home/node/data/damped_oscillators.npy

## How to load

```python
import numpy as np
data = np.load("/home/node/data/damped_oscillators.npy", allow_pickle=False)

# Access columns by name:
t = data['time']
x = data['displacement']
v = data['velocity']
osc_ids = data['oscillator_id']

# Filter to a single oscillator:
mask = data['oscillator_id'] == 1
osc1 = data[mask]
```

## Contents

The file contains 10,000 rows (20 oscillators x 500 time steps) as a NumPy
structured array with the following fields:

| Field                | Type    | Unit     | Description                                     |
|----------------------|---------|----------|-------------------------------------------------|
| oscillator_id        | int32   | —        | Integer identifier (1–20)                       |
| time                 | float64 | s        | Time from 0 to 20 seconds                       |
| displacement         | float64 | m        | Position x(t) with Gaussian measurement noise   |
| velocity             | float64 | m/s      | Velocity dx/dt with Gaussian measurement noise  |
| mass_kg              | float64 | kg       | Oscillator mass (0.1–10 kg)                     |
| spring_constant      | float64 | N/m      | Spring constant k = m * omega^2                 |
| damping_coefficient  | float64 | kg/s     | Damping coefficient b = 2 * m * gamma           |
| natural_frequency    | float64 | rad/s    | Angular frequency omega (0.5–5 rad/s)           |
| damping_ratio        | float64 | —        | gamma / omega (all < 1, i.e. underdamped)       |
| initial_amplitude    | float64 | m        | Initial amplitude A (0.5–3 m)                   |
| initial_phase        | float64 | rad      | Initial phase phi (0–2*pi)                      |
| kinetic_energy       | float64 | J        | 0.5 * m * v^2 (instantaneous)                   |
| potential_energy     | float64 | J        | 0.5 * k * x^2 (instantaneous)                   |
| total_energy         | float64 | J        | KE + PE (should decay due to damping)           |

## Physics model

Each oscillator follows the damped harmonic oscillator equation:

    x(t) = A * exp(-gamma * t) * cos(omega * t + phi) + noise

where gamma is the damping rate and omega is the natural frequency.
All 20 oscillators are underdamped (damping_ratio < 1).

## Hardware constraints

- Linux container (Debian Bookworm, x86_64)
- Maximum 4 CPU cores for parallel workloads
- No computation should run for more than 2 minutes
- No GPU / no CUDA — do not use CUDA-dependent libraries
- For PyTorch: use device='cpu' only
- Keep memory usage under 8 GB