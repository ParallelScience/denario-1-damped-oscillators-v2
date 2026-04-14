1. **Data Preparation and Theoretical Baseline**:
   - Load the structured array and group data by `oscillator_id`.
   - Compute the observed energy $E_{obs}(t) = \frac{1}{2} m v(t)^2 + \frac{1}{2} k x(t)^2$ using the provided noisy fields and ground truth parameters.
   - Establish the theoretical energy $E_{model}(t, m, b)$ using the full expression $E(t) = \frac{1}{2} k x(t)^2 + \frac{1}{2} m v(t)^2$, accounting for the dependence $k = m \omega^2$.

2. **Analytical Sensitivity Derivation**:
   - Derive logarithmic sensitivities $\mathcal{S}_b = \frac{\partial \ln E}{\partial \ln b}$ and $\mathcal{S}_m = \frac{\partial \ln E}{\partial \ln m}$ using the full energy expression.
   - Explicitly incorporate the chain rule for $k(m) = m \omega^2$ when calculating $\mathcal{S}_m$ to ensure mass sensitivity correctly reflects the potential energy contribution.
   - Implement these dimensionless sensitivities to characterize the local stability of the energy model.

3. **Parameter Perturbation and Grid Search**:
   - Define a 21x21 perturbation grid for $m$ and $b$ (ranging from $-10\%$ to $+10\%$ of ground truth).
   - Compute the energy residual $\Delta E(t, \tilde{m}, \tilde{b}) = |E_{obs}(t) - E_{model}(t, \tilde{m}, \tilde{b})|$ using NumPy broadcasting.
   - Structure the resulting data as a 4D array (20 oscillators, 21 $m$-steps, 21 $b$-steps, 500 time steps) to ensure memory efficiency and stay within the 2-minute execution limit.

4. **Degeneracy Analysis**:
   - Calculate the correlation coefficient between $\nabla_m \Delta E$ and $\nabla_b \Delta E$ to quantify parameter coupling.
   - Visualize the residuals $\Delta E$ as a function of the ratio $\tilde{b}/\tilde{m}$ to demonstrate the "valley of degeneracy," confirming that independent estimation of $m$ and $b$ is ill-posed.

5. **Time-to-Divergence Metric Calculation**:
   - Define $t_{limit}$ as the first time index where $\Delta E$ exceeds 5% of the initial energy $E(0)$.
   - Compute $t_{limit}$ for each oscillator across the perturbation grid to quantify model reliability.

6. **Curvature Analysis of the Energy Manifold**:
   - Compute the Hessian of the energy residual surface with respect to $(\tilde{m}, \tilde{b})$ using numerical finite differences of the grid search results.
   - Identify the transition point in the damping ratio $\zeta$ where the manifold curvature shifts from linear to non-linear behavior.

7. **Synthesis of Reliability Mapping**:
   - Construct a heatmap plotting $t_{limit}$ against the damping ratio $\zeta$.
   - Overlay sensitivity gradients to highlight regions of the parameter space where the energy dissipation model is most stable versus prone to rapid divergence.