1. **Data Preprocessing and Signal Normalization**:
   - Extract the 20 oscillators from the structured array.
   - Compute the theoretical energy $E_{model}(t)$ using ground truth parameters.
   - Calculate the regularized relative error signal $\epsilon(t) = |E_{obs}(t) - E_{model}(t)| / (E_{model}(t) + \eta)$, where $\eta$ is the estimated variance of the measurement noise to prevent division-by-zero.
   - Apply a Savitzky-Golay filter to the observed energy signals. Select window length and polynomial order to preserve the physical decay envelope; validate the filter against noise-free ground truth to ensure no phase shifts or artificial damping are introduced.

2. **Jacobian-Based Sensitivity Mapping**:
   - Implement the analytical Jacobian $\mathbf{J}(t) = [\frac{\partial E}{\partial m}, \frac{\partial E}{\partial b}]^T$ derived from the energy equation $E(t) = \frac{1}{2} m v(t)^2 + \frac{1}{2} (m \omega^2) x(t)^2$.
   - Compute the time-dependent Sensitivity Index $S(t) = \|\mathbf{J}(t)\|_2$ for each oscillator.
   - Normalize $S(t)$ by the instantaneous energy to obtain a dimensionless sensitivity profile for cross-oscillator comparison.

3. **Derivative-Based Global Sensitivity Measures (DGSM)**:
   - Approximate the variance-based sensitivity (Sobol indices) using DGSM. Leverage the analytical Jacobian $\mathbf{J}(t)$ to compute the sensitivity of the energy variance to parameters $m$ and $b$ without requiring expensive Monte Carlo sampling.
   - Quantify the first-order sensitivity contributions $S_m(t)$ and $S_b(t)$ at each time step to identify the time-varying dominance of mass versus damping.

4. **Information Horizon Identification**:
   - Define the "Information Horizon" ($T_H$) as the time index where the sensitivity ratio $R(t) = S_b(t) / S_m(t)$ crosses unity.
   - Implement a threshold condition: only compute $R(t)$ when $E(t) > \text{threshold}$ to ensure the crossover point is not driven by numerical noise as the signal decays.
   - Map $T_H$ across the population to determine the fundamental limit of parameter identifiability.

5. **Damping Regime Granularity**:
   - Sort the 20 oscillators by their `damping_ratio` ($\zeta$).
   - Divide the population into four quartiles (Very Low, Low, Medium, High damping) to capture non-linear transitions in the sensitivity manifold.
   - Compute mean sensitivity profiles $S(t)$ and DGSM indices for each quartile to identify regime-specific vulnerabilities.

6. **Sensitivity Manifold Visualization**:
   - Generate a heatmap of the Sensitivity Index $S(t)$ across the time domain $[0, 20s]$ for all 20 oscillators, ordered by $\zeta$.
   - Plot the evolution of $S_m(t)$ and $S_b(t)$ to visualize the shift in parameter influence over time.
   - Overlay the calculated Information Horizon $T_H$ on these plots to highlight transition points in parameter identifiability.

7. **Statistical Correlation and Regression**:
   - Perform a linear regression of $T_H$ against $\zeta$ to quantify the relationship between the damping regime and the duration of parameter identifiability.
   - Calculate the Pearson correlation coefficient between the peak sensitivity $S_{max}$ and the damping ratio to determine if higher damping increases susceptibility to parameter estimation errors.

8. **Robustness Assessment Summary**:
   - Aggregate findings into a sensitivity matrix mapping $(\zeta, t)$ to the dominant source of energy uncertainty.
   - Synthesize results into quantitative guidelines on time windows where parameter estimation for $m$ and $b$ is most reliable, establishing the limits of the energy conservation model in underdamped systems.