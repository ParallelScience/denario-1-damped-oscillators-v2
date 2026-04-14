1. **Data Preprocessing and Global Noise Estimation**:
   - Load the structured array and compute residuals between observed $x(t), v(t)$ and the theoretical model using provided ground truth parameters for all 20 oscillators.
   - Pool these residuals across the entire population to calculate global noise variances $\sigma_x^2$ and $\sigma_v^2$.
   - Define the time-dependent energy noise floor $\sigma_E^2(t) = m^2 v(t)^2 \sigma_v^2 + k^2 x(t)^2 \sigma_x^2$, accounting for the propagation of independent measurement errors through the energy equation.

2. **Relative Residual Formulation**:
   - Define the relative energy residual as $\delta E(t, \tilde{m}, \tilde{b}) = \frac{|E_{obs}(t) - E_{model}(t, \tilde{m}, \tilde{b})|}{E_{obs}(t)}$.
   - This normalization ensures consistency across the exponential decay of the signal and allows for comparison across the 20-second duration.

3. **Vectorized Parameter Perturbation**:
   - Implement a 21x21 grid search for $m$ and $b$ perturbations ($-10\%$ to $+10\%$ of ground truth).
   - Compute the 4D array of relative residuals $\delta E$ across all oscillators, time steps, and parameter combinations using NumPy broadcasting to ensure memory efficiency and speed.

4. **Jacobian Construction and SVD Analysis**:
   - Derive analytical expressions for the partial derivatives of $E(t, m, b)$ with respect to $m$ and $b$ to construct the Jacobian matrix $J$ at each time step.
   - Perform Singular Value Decomposition (SVD) on $J$ to obtain singular values $\sigma_1$ and $\sigma_2$.
   - Calculate the condition number $\kappa = \sigma_1 / \sigma_2$ as a time-dependent metric of parameter degeneracy.

5. **Divergence Thresholding**:
   - Identify the time index $t_{crit}$ where the absolute residual $\Delta E(t, \tilde{m}, \tilde{b})$ exceeds the noise floor threshold $\sqrt{\sigma_E^2(t)}$.
   - Use this to isolate model-induced divergence from noise-dominated regimes.

6. **Sensitivity-Damping Correlation and Phase Analysis**:
   - Correlate the condition number $\kappa$ and $t_{crit}$ with the damping ratio $\zeta$ for each oscillator.
   - Calculate the analytical gradients of the phase $\phi$ with respect to $m$ and $b$ to compare the sensitivity of the phase versus the energy manifold.
   - Evaluate if phase-based sensitivity provides a mechanism to resolve parameter degeneracy where energy-based sensitivity fails.

7. **Synthesis of Robustness Mapping**:
   - Generate heatmaps of the condition number $\kappa$ and relative residuals $\delta E$ in the $(\tilde{m}, \tilde{b})$ parameter space.
   - Overlay the noise floor boundary to demarcate regions where parameter estimation is physically meaningful versus regions limited by measurement noise.