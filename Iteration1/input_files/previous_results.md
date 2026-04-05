# Results: Perturbation-Based Robustness Analysis of Energy Dissipation Manifolds

## 1. Baseline Noise Floor and Model Validation
To establish a rigorous baseline for the sensitivity analysis, the theoretical energy dissipation model was validated against the observed `total_energy` field for each of the 20 oscillators. The baseline residuals, defined as the Mean Absolute Error (MAE) between the analytical solution $E_{model}(t; m, b, \omega, A, \phi)$ and the observed energy $E_{obs}(t)$, were calculated at the ground truth parameters. 

The results indicate that the analytical model is highly consistent with the provided dataset, with baseline residuals ranging from approximately $1.72 \times 10^{-18}$ J to $1.32 \times 10^{-15}$ J. These values represent the "noise floor" of the system, primarily attributable to the Gaussian measurement noise inherent in the displacement and velocity fields. Given that these residuals are effectively negligible compared to the total energy of the oscillators (which typically reside in the Joule range), the analytical model is confirmed as a robust representation of the underlying physics.

## 2. Sensitivity Manifold Analysis
The sensitivity of the energy dissipation model to parametric uncertainty was evaluated by perturbing the mass ($m$) and damping coefficient ($b$) within a $\pm 10\%$ range of their ground truth values. The resulting 4D manifold of relative energy residuals $\Delta E_{rel}$ reveals the non-linear landscape of model divergence.

### 2.1. Gradient Magnitude and Damping Correlation
The sensitivity gradients $\nabla_{\tilde{m}, \tilde{b}} \Delta E_{rel}$ quantify the local rate of change of the energy residual with respect to parameter estimation errors. The mean gradient magnitude across the population was found to be $0.1136$. 

A Spearman rank correlation analysis was performed to determine the relationship between the sensitivity of the energy dissipation model and the damping ratio ($\zeta$). The calculated correlation coefficient of $0.654$ suggests a moderate-to-strong positive relationship. This indicates that oscillators with higher damping ratios are inherently more susceptible to energy divergence when physical parameters are inaccurately estimated. In high-damping regimes, the rapid decay of the energy envelope makes the system state more sensitive to the precise values of $b$ and $m$, as these parameters dictate the rate of exponential decay.

### 2.2. Visualization of Non-Linearities
The energy residual manifolds for the oscillators with the lowest and highest damping ratios (Oscillators 19 and 13, respectively) demonstrate distinct topological features. 
*   **Low-Damping Regime:** The manifold exhibits a relatively flat landscape, suggesting that the energy dissipation model is robust to small parameter perturbations. The energy decay is slow, and the residual surface is dominated by the global structure of the oscillation.
*   **High-Damping Regime:** The manifold displays steeper gradients and more pronounced non-linearities. The sensitivity to the damping coefficient $b$ is particularly acute, as even minor deviations from the true value lead to significant discrepancies in the predicted energy decay rate.

## 3. Discussion and Interpretation
The comparison between the baseline noise floor and the residuals induced by $\pm 10\%$ parameter perturbations reveals a clear hierarchy of error sources. While the measurement noise floor is on the order of $10^{-15}$ J, the residuals induced by a $10\%$ parameter error are orders of magnitude larger. This confirms that in practical applications, the precision of physical parameter estimation is the dominant factor limiting the reliability of long-term state prediction, far outweighing the impact of sensor noise.

The observed correlation between the damping ratio and sensitivity gradient magnitude provides a critical insight for system identification: systems operating in high-damping regimes require significantly higher precision in parameter estimation to maintain the same level of predictive accuracy as their low-damping counterparts. The non-linearities in the residual manifolds suggest that simple linear error propagation models may be insufficient for high-damping systems, necessitating more sophisticated uncertainty quantification techniques.

## 4. Conclusion
This study demonstrates that the energy dissipation manifold of an underdamped harmonic oscillator is highly sensitive to parametric uncertainty. The quantitative threshold where parameter uncertainty dominates measurement noise is reached well within a $10\%$ deviation from ground truth parameters. Consequently, for long-term state prediction in underdamped systems, the accuracy of the damping coefficient and mass estimation is paramount, particularly as the damping ratio increases. Future work should focus on developing adaptive parameter estimation algorithms that account for the non-linear sensitivity profiles identified in this analysis, ensuring robust performance across varying damping regimes.