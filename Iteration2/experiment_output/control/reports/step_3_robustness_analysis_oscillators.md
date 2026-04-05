<!-- filename: reports/step_3_robustness_analysis_oscillators.md -->
# Report: Perturbation-Based Robustness Analysis of Energy Dissipation Manifolds in Underdamped Oscillators

## 1. Introduction
The reliability of state prediction in physical systems is fundamentally constrained by the precision of parameter estimation. In the context of damped harmonic oscillators, the energy dissipation manifold is governed by the interplay between mass ($m$) and the damping coefficient ($b$). This study investigates the sensitivity of the total energy $E(t)$ to these parameters, mapping the "Information Horizon" ($T_H$)—the temporal limit beyond which the influence of damping dominates mass-related energy uncertainty. By analyzing 20 distinct underdamped oscillators, we provide a quantitative assessment of how damping ratios ($\zeta$) dictate the robustness of energy conservation models.

## 2. Sensitivity Manifold Interpretation
The sensitivity index $S(t) = \|\mathbf{J}(t)\|_2$, where $\mathbf{J}(t) = [\frac{\partial E}{\partial m}, \frac{\partial E}{\partial b}]^T$, reveals a highly non-linear manifold. The heatmap of $S(t)$ across the 20-second observation window demonstrates that sensitivity is highest during the initial transient phase ($t < 2s$). As the system approaches equilibrium, the sensitivity index decays exponentially, mirroring the energy dissipation itself.

The evolution of $S_m(t)$ and $S_b(t)$ (the partial sensitivities to mass and damping, respectively) indicates a clear regime shift. In the early stages, the energy manifold is dominated by mass-related uncertainties, likely due to the high kinetic energy contribution. As time progresses, the damping term—which dictates the rate of decay—becomes the primary driver of uncertainty in the energy model.

## 3. The Information Horizon ($T_H$) and Damping Regimes
The Information Horizon $T_H$, defined as the time at which the sensitivity ratio $R(t) = S_b(t) / S_m(t)$ crosses unity, serves as a critical metric for parameter identifiability. Our analysis shows that $T_H$ typically occurs within the first second of the observation window (ranging from $0.60s$ to $0.92s$).

### Statistical Summary of Oscillator Population
| Metric | Value |
| :--- | :--- |
| Mean $T_H$ | $\approx 0.76s$ |
| Slope ($T_H$ vs. $\zeta$) | $-0.8347$ |
| $R^2$ (Regression) | $0.3326$ |
| Correlation ($\rho_{peak, \zeta}$) | $-0.5221$ |

The negative slope of the regression between $T_H$ and the damping ratio $\zeta$ suggests that as damping increases, the Information Horizon shifts earlier in time. This implies that in more heavily damped systems, the influence of the damping coefficient on the energy manifold becomes dominant more rapidly, effectively shortening the window during which mass-related parameters can be independently identified with high confidence.

## 4. Discussion: Robustness of Energy Dissipation Models
The moderate negative correlation ($\rho = -0.5221$) between peak sensitivity and the damping ratio indicates that oscillators with lower damping ratios exhibit significantly higher peak sensitivity values. This suggests that low-damping systems are more susceptible to parameter estimation errors, as small perturbations in $m$ or $b$ lead to larger deviations in the predicted energy trajectory.

The observed $T_H$ values, consistently under $1s$, highlight a fundamental limitation: the energy conservation model is most robust to parameter uncertainty only in the immediate aftermath of the initial state. Beyond $T_H$, the model's reliance on the damping coefficient $b$ increases, making the energy prediction highly sensitive to the accuracy of the damping estimate.

## 5. Conclusion
This study establishes that the robustness of energy dissipation models in underdamped systems is intrinsically linked to the damping ratio. We have demonstrated that:
1. **Temporal Sensitivity:** The energy manifold is most sensitive to parameter perturbations in the early transient phase.
2. **Regime Dominance:** The transition from mass-dominance to damping-dominance occurs rapidly ($T_H < 1s$), defining the limit of reliable parameter estimation.
3. **Damping Vulnerability:** Higher damping ratios accelerate the arrival of the Information Horizon and reduce the peak sensitivity, suggesting that while highly damped systems may appear more "stable" in their energy decay, they are constrained by a narrower window of parameter identifiability.

These findings provide a quantitative framework for practitioners to determine the optimal time windows for parameter calibration in damped systems, ensuring that energy conservation models are utilized within their most reliable regimes. Future work should extend this analysis to include non-Gaussian noise profiles to further stress-test the robustness of the sensitivity manifold.