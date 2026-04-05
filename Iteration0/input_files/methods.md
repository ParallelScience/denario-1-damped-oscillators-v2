1. **Data Preprocessing and Baseline Extraction**: Load the structured array and group data by `oscillator_id`. Extract ground truth physical parameters ($m, b, \omega, A, \phi$) and observed time-series data ($t, x, v, E_{obs}$). Calculate the baseline residual at true parameters to establish a "noise floor" caused by measurement noise, which will be subtracted from subsequent calculations to isolate parameter-induced divergence.

2. **Theoretical Energy Model Implementation**: Define a vectorized function to compute the theoretical energy $E_{model}(t; \tilde{m}, \tilde{b})$ using the analytical solution for damped harmonic oscillators. Ensure the function uses NumPy broadcasting to handle the time dimension and parameter grids efficiently.

3. **Parameter Perturbation Grid Generation**: For each oscillator, generate a 10x10 grid of perturbed parameters $(\tilde{m}, \tilde{b})$ within $\pm 10\%$ of the ground truth values. Apply clipping to ensure $\tilde{m} > 0$ and $\tilde{b} > 0$ to maintain physical validity.

4. **Vectorized Residual Energy Manifold Calculation**: Construct a 4D array of shape `(20, 10, 10, 500)` representing `(oscillator, m_grid, b_grid, time)`. Compute the relative energy residual $\Delta E_{rel} = \frac{1}{T} \int_0^T \frac{|E_{obs}(t) - E_{model}(t; \tilde{m}, \tilde{b})|}{E_{obs}(t) + \epsilon} dt$ using the trapezoidal rule, where $\epsilon$ is a small constant to prevent division by zero.

5. **Sensitivity Gradient Estimation**: Calculate the sensitivity gradients $\nabla_{\tilde{m}, \tilde{b}} \Delta E_{rel}$ using a central difference scheme across the 10x10 parameter grid for each oscillator. This yields a local sensitivity vector representing the stability of the energy conservation law.

6. **Correlation Analysis with Damping Regimes**: Aggregate the sensitivity gradients and compute the rank correlation between the magnitude of the gradient and the `damping_ratio` ($\zeta$) of each oscillator to determine if higher damping regimes are more susceptible to parameter estimation errors.

7. **Visualization of Sensitivity Manifolds**: Generate 2D heatmaps of the energy residual manifold $\Delta E_{rel}$ for two representative oscillators (one with the lowest and one with the highest damping ratio) to visually validate the non-linearities in the sensitivity matrix.

8. **Statistical Aggregation and Reporting**: Compile the sensitivity matrix, correlation coefficients, and summary statistics (mean and standard deviation of gradients) into a final report to quantify the overall robustness of the energy dissipation model against parametric uncertainty.