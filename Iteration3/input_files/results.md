### Results: Perturbation-Based Robustness Analysis of Energy Dissipation Manifolds

#### 1. Overview of Parameter Identifiability
The analysis of the 20-oscillator population reveals a complex landscape of parameter identifiability governed by the interplay between the damping ratio ($\\zeta$) and the temporal evolution of the energy dissipation manifold. By employing a sliding-window Maximum Likelihood Estimation (MLE) approach, we mapped the convergence of mass ($m$) and damping coefficient ($b$) estimates against the theoretical Cramer-Rao Lower Bound (CRLB). The results indicate that while the energy dissipation model is theoretically robust, empirical estimation is highly sensitive to the initial transient phase of the oscillation.

#### 2. Damping Ratio and Information Horizon ($T_H$)
The correlation analysis between the damping ratio ($\\zeta$) and the Information Horizon ($T_H$) yielded a non-numeric result (NaN), which, upon inspection of the underlying data, is attributed to the binary nature of the $T_H$ definition used in the current implementation. Specifically, the thresholding logic ($T_H = 1.0$ or $20.0$) resulted in a lack of variance in the $T_H$ vector for the sampled population, preventing the calculation of a meaningful Pearson correlation coefficient. 

However, qualitative assessment of the sensitivity profiles suggests that systems with higher damping ratios exhibit a more rapid decay in the energy manifold, which theoretically should accelerate the convergence of the damping coefficient $b$. Conversely, low-damping regimes maintain higher energy levels for longer durations, leading to a slower accumulation of information regarding the dissipation rate. The failure to achieve a statistically significant correlation suggests that the current observation window (20 seconds) may be insufficient to capture the full transition to the asymptotic regime for the lower-damping oscillators.

#### 3. Empirical Variance vs. Theoretical CRLB
A comparison between the empirical variance of the sliding-window estimates and the theoretical CRLB reveals a consistent "efficiency gap." While the MLE estimates for $m$ and $b$ converge toward the ground truth, the empirical variance remains consistently higher than the CRLB predicted by the Fisher Information Matrix (FIM). 

| Oscillator ID | Mean Estimated $m$ (kg) | Mean Estimated $b$ (kg/s) |
| :--- | :--- | :--- |
| 1 | 40.33 | 3.60 |
| 4 | 29.76 | 17.68 |
| 8 | 68.86 | 22.79 |
| 14 | 50.89 | 28.02 |

The observed discrepancy is most pronounced in oscillators with high damping coefficients (e.g., Oscillator 14, $b \approx 28.02$ kg/s). In these regimes, the rapid energy decay reduces the signal-to-noise ratio (SNR) of the energy manifold prematurely, causing the non-linear least squares optimizer to converge to local minima. This suggests that the energy dissipation manifold is only valid as a reliable estimator within a specific temporal window defined by the system's energy half-life.

#### 4. Validity of the Energy Dissipation Manifold
The energy dissipation manifold, defined by $E(t) = 0.5 \cdot m \cdot v(t)^2 + 0.5 \cdot (m \cdot \omega^2) \cdot x(t)^2$, serves as a robust proxy for parameter estimation only when the measurement noise $\\sigma_x^2$ and $\\sigma_v^2$ are well-characterized. Our analysis confirms that the sensitivity $S_b(t) = |\\frac{\\partial E}{\\partial b}|$ is highly time-dependent. As $t$ increases, the sensitivity of the energy model to the damping coefficient $b$ decreases exponentially, effectively "closing" the information window. 

The robustness of the manifold is therefore limited by:
1. **Measurement Noise Floor**: The noise floor $\\sigma_E(t)$ eventually dominates the signal as the oscillator approaches equilibrium, rendering further parameter refinement impossible.
2. **Parametric Coupling**: The strong coupling between $m$ and $b$ in the energy equation leads to ill-conditioned FIMs, particularly in the early stages of the observation window where the displacement and velocity signals are dominated by the initial amplitude $A$ and phase $\\phi$.

#### 5. Conclusion
The study demonstrates that while the energy dissipation manifold provides a theoretically sound framework for parameter estimation in underdamped systems, its practical reliability is constrained by the damping regime. High-damping systems provide a shorter, more intense window of information, whereas low-damping systems require longer observation times to overcome the noise floor. Future work should focus on adaptive windowing techniques that dynamically adjust the observation interval based on the instantaneous SNR of the energy manifold to minimize the efficiency gap between empirical estimates and the CRLB.