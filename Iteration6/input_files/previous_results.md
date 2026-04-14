# Results: Perturbation-Based Robustness Analysis of Energy Dissipation Manifolds

## 1. Overview of Energy Dissipation Dynamics
The energy dissipation of an underdamped harmonic oscillator is governed by the interplay between the inertial mass $m$ and the damping coefficient $b$. Our analysis of the 20-oscillator population reveals that the energy manifold is highly sensitive to perturbations in these parameters. The observed energy $E_{obs}(t)$ deviates from the theoretical model $E_{model}(t, \tilde{m}, \tilde{b})$ as a function of time, with the divergence rate dictated by the accuracy of the parameter estimation. The mean time-to-divergence ($t_{limit}$), defined as the threshold where residuals exceed 5% of the initial energy, was found to be approximately 9.05 seconds across the entire parameter space.

## 2. The Valley of Degeneracy
The contour analysis of the mean energy residuals reveals a distinct "valley of degeneracy" in the $(\tilde{m}, \tilde{b})$ parameter space. This valley represents a region where the energy residual $\Delta E$ is minimized, yet the parameters $\tilde{m}$ and $\tilde{b}$ deviate significantly from their ground-truth values. 

This phenomenon indicates that the energy dissipation model is inherently ill-posed for independent parameter estimation. Specifically, the model exhibits a strong coupling between mass and damping: an increase in the estimated mass can be partially compensated by a corresponding increase in the damping coefficient to maintain a similar energy decay profile. This degeneracy is most pronounced in systems with lower damping ratios, where the energy decay is slower and the sensitivity of the total energy to instantaneous velocity fluctuations is higher.

## 3. Sensitivity Gradients and Model Reliability
The sensitivity analysis confirms that the energy model's stability is non-linearly dependent on the damping ratio $\zeta$. The Hessian analysis of the energy residual surface shows that the curvature of the manifold is shallowest along the axis of the degeneracy valley, confirming that small errors in parameter estimation lead to large, persistent residuals over time.

The relationship between the damping ratio $\zeta$ and the model reliability, quantified by $t_{limit}$, is summarized in the following table:

| Oscillator ID | Damping Ratio ($\zeta$) | Mean $t_{limit}$ (s) |
| :--- | :--- | :--- |
| 19 | 0.0065 | 8.58 |
| 8 | 0.0571 | 10.48 |
| 13 | 0.3563 | 10.48 |

As shown in the heatmap, oscillators with very low damping ratios exhibit lower $t_{limit}$ values, suggesting that highly underdamped systems are more susceptible to rapid divergence when parameters are perturbed. Conversely, as $\zeta$ increases, the system exhibits a slightly higher tolerance for parameter uncertainty, likely due to the faster decay of the transient energy components, which reduces the cumulative impact of measurement noise and parameter mismatch.

## 4. Discussion and Interpretation
The results demonstrate that the reliability of long-term state prediction in underdamped systems is fundamentally limited by the coupling between inertial and dissipative parameters. The "valley of degeneracy" confirms that without independent constraints on either mass or damping, the energy dissipation manifold cannot be uniquely inverted. 

The observed sensitivity gradients $\mathcal{S}_m$ and $\mathcal{S}_b$ suggest that the potential energy contribution, which scales with $k = m \omega^2$, dominates the mass sensitivity, while the damping sensitivity is primarily driven by the exponential decay term $\exp(-2\gamma t)$. Consequently, in regimes where the damping is low, the system remains in a high-energy state for a longer duration, making the model highly sensitive to the damping coefficient $b$. As the system approaches critical damping, the energy dissipates more rapidly, and the influence of the initial state becomes less significant compared to the dissipative parameters.

## 5. Conclusion
This study provides a rigorous assessment of the robustness of energy dissipation models in underdamped harmonic oscillators. We have identified that the energy manifold is characterized by a degeneracy that complicates parameter estimation. Our findings suggest that for reliable long-term prediction, it is insufficient to rely on energy-based estimation alone; rather, one must incorporate independent measurements of the system's inertial properties or utilize time-series fitting techniques that explicitly account for the coupling between $m$ and $b$. Future work should focus on developing regularization techniques that can break this degeneracy, particularly for systems operating in low-damping regimes where model divergence is most rapid.