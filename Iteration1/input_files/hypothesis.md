**Title: State-Space Reconstruction via Extended Kalman Filtering (EKF) for Damping Parameter Estimation**

**Hypothesis:** The predictive horizon of high-damping ($\zeta > 0.5$) oscillators is currently limited by the sensitivity of energy-based residuals to measurement noise. By transitioning from a static energy-manifold analysis to a recursive Bayesian state-space estimation (Extended Kalman Filter), we can decouple the latent physical parameters ($m, b$) from the observed noisy state ($x, v$). 

**Rationale:** Previous iterations identified that the energy manifold becomes indistinguishable from the noise floor at $t \approx T_d$. An EKF approach treats the damped harmonic oscillator as a continuous-discrete state-space system, where the state vector $\mathbf{s} = [x, v, \omega, \gamma]^T$ is updated iteratively. This allows the model to "learn" the damping parameters dynamically as the oscillation evolves, rather than relying on a fixed analytical model that is highly sensitive to initial parameter assumptions. 

**Methodology:**
1. Define the state-space model using the damped harmonic oscillator differential equations.
2. Implement an EKF to estimate the hidden parameters ($\omega, \gamma$) alongside the state ($x, v$) using the provided noisy measurements.
3. Compare the EKF-estimated parameters against the ground-truth values in the dataset to determine if this approach yields lower parameter variance than the previous perturbation-based sensitivity analysis, particularly in the high-$\zeta$ regime.
4. Quantify the "Extended Predictive Horizon": measure how many additional seconds the EKF can accurately track the oscillator state compared to the previous $T_d$ limits.