1. **Data Preparation and Noise Characterization**:
   - Load the structured array and iterate through each of the 20 oscillators.
   - Estimate the noise variances $\sigma_x^2$ and $\sigma_v^2$ by analyzing the residuals of a preliminary fit or high-frequency components of the displacement and velocity signals.
   - Compute the instantaneous observed energy $E_{obs}(t) = 0.5 \cdot m \cdot v(t)^2 + 0.5 \cdot (m \cdot \omega^2) \cdot x(t)^2$.

2. **Fisher Information Matrix (FIM) Formulation**:
   - Derive the analytical Jacobian $\mathbf{J}(t) = [\frac{\partial E}{\partial m}, \frac{\partial E}{\partial b}]^T$ for the energy model.
   - Propagate the estimated noise variances $\sigma_x^2$ and $\sigma_v^2$ through the energy equation to define the time-varying variance $\sigma_E^2(t)$ of the energy measurement.
   - Construct the FIM $\mathbf{F}(t) = \mathbf{J}(t)^T \sigma_E(t)^{-2} \mathbf{J}(t)$ and compute the Cramer-Rao Lower Bound (CRLB) as $\mathbf{C}(t) = \mathbf{F}(t)^{-1}$ to establish the theoretical minimum variance for parameter estimates.

3. **Information Horizon Definition**:
   - Define the Information Horizon $T_H$ as the time point where the CRLB for the damping coefficient $b$ drops below 10% of the parameter's ground truth value.
   - Ensure the sensitivity $S_b(t) = |\frac{\partial E}{\partial b}|$ is compared against the noise floor $\sigma_E(t)$ to validate that information gain is physically distinguishable.

4. **Sliding-Window Parameter Estimation**:
   - Implement a sliding-window Maximum Likelihood Estimation (MLE) to estimate $\hat{m}$ and $\hat{b}$ using data segments $[0, t_{end}]$ for $t_{end} \in [1, 20]$.
   - Use a non-linear least squares optimizer, warm-starting each window with the ground truth parameters or the estimate from the previous window to ensure convergence and computational efficiency.
   - Record the estimated parameters $\hat{m}(t_{end})$ and $\hat{b}(t_{end})$ and their associated standard errors.

5. **Empirical Validation of Identifiability**:
   - Compare the empirical variance of the sliding-window estimates $\hat{b}(t_{end})$ against the theoretical CRLB calculated in Step 2.
   - Quantify the "identifiability gain" by measuring the rate of decrease in parameter variance as the observation window expands.
   - Verify if the empirical variance drop-off aligns with the theoretical $T_H$.

6. **Regime-Specific Sensitivity Analysis**:
   - Group the 20 oscillators into quartiles based on their `damping_ratio` ($\zeta$).
   - Aggregate the FIM and CRLB profiles for each quartile to characterize how the damping regime dictates the speed at which the system becomes "informative."
   - Identify if high-damping regimes exhibit faster convergence of the CRLB compared to low-damping regimes.

7. **Sensitivity Manifold Visualization**:
   - Generate a heatmap of the normalized sensitivity $S_b(t)$ across the time domain for all oscillators, sorted by $\zeta$.
   - Plot the evolution of the CRLB for $m$ and $b$ alongside the empirical variance from the sliding-window estimation.
   - Overlay the calculated $T_H$ on these plots to visualize the transition from parameter uncertainty to parameter identifiability.

8. **Robustness and Reliability Synthesis**:
   - Perform a correlation analysis between the damping ratio $\zeta$ and the time-to-convergence ($T_H$).
   - Construct a summary matrix mapping $(\zeta, t)$ to the reliability of parameter estimation, providing a quantitative assessment of the time required to achieve target precision in $m$ and $b$ for underdamped systems.