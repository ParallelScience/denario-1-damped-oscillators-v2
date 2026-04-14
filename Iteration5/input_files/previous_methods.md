1. **Data Pre-processing and Noise Characterization**:
   - Load the structured array and isolate each of the 20 oscillators.
   - Compute the theoretical displacement $x_{model}(t)$ using ground truth parameters.
   - Estimate the noise floor $\sigma_x^2$ by calculating the variance of the residuals $r(t) = x_{obs}(t) - x_{model}(t)$ across the entire time series for each oscillator to ensure a statistically robust baseline.

2. **Parameter Space Reparameterization**:
   - Define the dynamical parameters $\gamma = b/(2m)$ and $\omega = \sqrt{k/m}$.
   - Define the displacement model $x(t; \gamma, \omega, A, \phi) = A e^{-\gamma t} \cos(\omega t + \phi)$ as the objective function.
   - Prepare analytical Jacobian expressions for the parameters $(\gamma, \omega, A, \phi)$ to facilitate efficient optimization and Fisher Information calculation.

3. **MLE Parameter Estimation**:
   - Perform non-linear least squares estimation for each oscillator using the Levenberg-Marquardt algorithm.
   - Use ground truth values as initial guesses to ensure convergence.
   - Calculate the parameter covariance matrix $\mathbf{C} = (\mathbf{J}^T \mathbf{J})^{-1} \sigma_x^2$ using the analytical Jacobian $\mathbf{J}$ to quantify estimation uncertainty.

4. **Perturbation-Based Sensitivity Analysis**:
   - Systematically perturb $m$ and $b$ within a $\pm 10\%$ range of ground truth values.
   - For each perturbation, compute the energy residual $\Delta E(t) = |E_{obs}(t) - E_{model}(\tilde{m}, \tilde{b}, t)|$, where $E_{model}$ uses the perturbed parameters while keeping initial conditions $(A, \phi)$ fixed to isolate the effect of physical constant mismatch on dissipation.
   - Utilize NumPy broadcasting to perform these calculations across the population efficiently.

5. **Fisher Information Rate Calculation**:
   - Compute the $4 \times 4$ Fisher Information Matrix $\mathbf{F}(t)$ for the parameters $(\gamma, \omega, A, \phi)$.
   - Extract the $2 \times 2$ sub-matrix corresponding to $(\gamma, \omega)$ to calculate the Fisher Information Rate $\mathcal{I}(t) = \frac{d}{dt} \text{Tr}(\mathbf{F}_{\gamma, \omega}(t))$.
   - Identify the time point $t_{crit}$ where $\mathcal{I}(t)$ falls below the noise floor $\sigma_x^2$ to define the limit of parameter identifiability.

6. **Correlation of Sensitivity and Damping Regimes**:
   - Group oscillators by their damping ratio $\zeta$.
   - Correlate the sensitivity gradients of the energy residuals $\Delta E$ with $\zeta$ and $\mathcal{I}(t)$ to identify regimes most susceptible to energy divergence.

7. **Sensitivity Matrix Construction**:
   - Construct a sensitivity matrix $\mathbf{S}$ using Logarithmic Sensitivity $\frac{\partial \ln E}{\partial \ln p}$ for $p \in \{m, b\}$.
   - This dimensionless approach ensures that sensitivities to mass and damping are directly comparable across the population despite differing units and scales.

8. **Reliability Mapping**:
   - Generate a heatmap visualizing the relationship between $\zeta$, time $t$, and the magnitude of energy residuals $\Delta E$.
   - Synthesize the results into a final reliability map identifying time windows where energy dissipation models remain robust, providing a quantitative assessment of long-term state prediction reliability.