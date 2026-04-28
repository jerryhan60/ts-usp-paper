# Junior Paper Math Review Changes

This file lists recommended revisions for `main.tex` after a detailed mathematical and statistical review. Items are grouped by priority.

## High Priority

1. Revise the Marsden--Hazan theorem restatement.
   - Current issue: The bound in Section 3.2 includes linear-in-`T` spectral and noise terms, but the text concludes sublinear regret merely from `L log T = o(T)`.
   - Required change: Either quote the actual theorem from Marsden--Hazan with its stated assumptions/rates, or clearly label the current display as informal intuition rather than a theorem.
   - Required change: Remove or qualify the claim that the displayed bound gives hidden-dimension-independent sublinear regret as written.

2. Fix the proof sketch for the Marsden--Hazan result.
   - Current issue: The argument uses `||C p^*(A)^t h_0||` even though the algebraic identity gives `C p^*(A) A^{t-d} h_0`, not repeated application of `p^*(A)` over time.
   - Required change: Rework the proof sketch to match the cited paper’s actual mechanism, or replace it with a short citation-backed summary.
   - Required change: Avoid claiming that the forecast for `y_t` is simply recovered by applying an inverse polynomial unless the invertibility/stability conditions are explicitly stated.

3. Weaken the spectral-compression corollary.
   - Current issue: The corollary says Chebyshev minimizes `rho(q(A))` for a fixed matrix `A`.
   - Required change: State that Chebyshev minimizes the worst-case uniform upper bound `sup_{lambda in [-rho,rho]} |q(lambda)|` over all possible spectra in the interval.
   - Required change: If discussing a fixed finite spectrum, acknowledge that another monic polynomial may be smaller on that particular set of eigenvalues.

4. Correct the frequency-response theorem.
   - Current issue: The theorem claims all local minima of `|H(omega)|^2` for even `d` occur at `omega = k/(2s)`. This is not established by the proof and is generally stronger than what the displayed argument shows.
   - Required change: Restrict the claim to the values at `z = +/-1`, or explicitly prove the full local-minima characterization.
   - Required change: Separate statements about attenuation points from statements about global/local minima.

5. Align the spectral analysis with the actual residual channel.
   - Current issue: The model receives the residual channel `(p(B_s)x - x)`, whose response is `H(omega) - 1`, but the spectral-overlap analysis uses `|H(omega)|^2`.
   - Required change: Recompute or restate spectral overlap using `|H(omega)-1|^2`, or explicitly justify why the full-filter response is the right proxy.
   - Required change: Update “passband,” “attenuation,” and “preserves signal” language to match the residual filter.

6. Fix the noise-gain lemma and asymptotics.
   - Current issue: The closed-form coefficient norm formula for unnormalized Chebyshev polynomials is incorrect at small degrees.
   - Current issue: The text calls an exponentially growing quantity “subexponential.”
   - Required change: Replace the asymptotic statement with a verified formula or remove it.
   - Required change: Keep the exact low-degree coefficient norms if independently verified, but avoid deriving unsupported asymptotics.

7. Rewrite the spectral--noise tradeoff corollary.
   - Current issue: The statement includes `T` in `d^*`, while the proof cancels `T`.
   - Current issue: The optimal regret scaling does not follow from the displayed bound.
   - Required change: Either remove the corollary or make it an informal heuristic.
   - Required change: If kept formal, derive it from a correct degree-dependent spectral term and a correct coefficient-growth model.

## Medium Priority

8. Fix Chebyshev coefficient scaling inconsistencies.
   - Current issue: The main text uses the current monic degree-4 convention `p(z)=1-z^2+z^4/8`, so the residual hint is `-x[t-32] + (1/8)x[t-64]`.
   - Current issue: The learned-FIR appendix table lists fixed Chebyshev as `[0, -2, 0, 0.5]`, which is a different scaling.
   - Required change: Standardize all degree-4 coefficients to the implementation convention, or clearly explain if a different historical scaling was used for a specific experiment.

9. Fix odd-degree effective-lag descriptions.
   - Current issue: The appendix degree table says degree 3 uses lag `3P` and degree 5 uses `P, 3P, 5P`.
   - Required change: Recompute effective residual lags under the current reciprocal-monic implementation and update the table.
   - Required change: Cross-check the table against `compute_polynomial_coefficients`.

10. Correct the synthetic LDS description.
    - Current issue: The text calls the system “marginally stable” with `rho(A)=0.99`; that is strictly stable.
    - Current issue: The text calls the system “asymmetric,” while the appendix describes real eigenvalues embedded in a random orthogonal basis, which yields a symmetric/normal matrix.
    - Required change: Either change the construction to match the description or revise the prose to “near-marginally stable symmetric/normal LDS.”

11. Correct PSD attenuation arithmetic.
    - Current issue: The text states `|H(omega_k)|^2 = 2^{2-2d}` but gives `1/16` for `d=2`.
    - Required change: Change the `d=2` PSD reduction to `1/4`, or revise the formula if a different normalization was actually used.

12. Revisit claims about attenuation frequencies and daily cycles.
    - Current issue: The example says the attenuation minima for `s=16` correspond to periods `infinity, 8h, 4h, ...` on 15-minute data, while the domain discussion says daily and half-daily cycles align with 32- and 64-step lookbacks.
    - Required change: Separate lookback lags from frequency-response attenuation points.
    - Required change: Avoid implying that an 8h/16h lookback is direct evidence of daily/half-daily frequency alignment unless supported by a precise frequency calculation.

13. Tighten the statistical dependence assumptions.
    - Current issue: The sign-test section treats 485 seed-configuration wins as independent Bernoulli draws despite repeated configurations, shared datasets, and shared training/evaluation structure.
    - Required change: Present the pooled sign test as a useful paired descriptive/inferential test with potential dependence caveats.
    - Required change: Add a cluster-robust sensitivity analysis by configuration and/or seed if available, or emphasize per-seed tests and config-level bootstrap intervals.

14. Fix the power-analysis mismatch.
    - Current issue: The text uses Cohen’s `d` in a formula described as a one-sided sign-test power calculation.
    - Required change: Either call it a rough normal-approximation heuristic or replace it with a sign-test/binomial power calculation based on observed win probability.

15. Qualify causal language around controls.
    - Current issue: The text describes an ATE of polynomial content, but zero/duplicate/Chebyshev interventions may also differ in optimization dynamics and input distribution.
    - Required change: Replace strong causal language with “capacity-matched controlled comparison” unless a causal identification argument is added.

16. Adjust FEV-Bench uncertainty claims.
    - Current issue: The FEV-Bench table uses a five-seed HD mean but a single-seed baseline.
    - Required change: Avoid overclaiming cross-benchmark statistical validation unless baseline seed variability is available.
    - Required change: State clearly that FEV-Bench is supportive external validation, not a fully seed-matched inferential test.

## Low Priority

17. Weaken spectral-correlate conclusions.
    - Current issue: The paper reports `r=0.10` and `p=0.54`, but later says the spectral-correlate analysis “empirically confirms” the mechanism.
    - Required change: Replace “confirms” with “is directionally consistent with” or “does not falsify.”
    - Required change: Avoid presenting this as strong evidence unless a stronger proxy or larger dataset-level test is added.

18. Remove “filter zeros” language.
    - Current issue: The frequency-response theorem states the filter has no unit-circle zeros, but the discussion refers to spectra aligning with filter zeros.
    - Required change: Replace “zeros” with “attenuation minima” or “low-gain bands.”

19. Fix Legendre comparison details.
    - Current issue: The ratio is said to be strictly less than 1 for all `d >= 1`, but it equals 1 at `d=1`.
    - Current issue: The asymptotic ratio appears inconsistent: the displayed formula gives `2/sqrt(pi d)`, while the proof says `1/sqrt(pi d)`.
    - Required change: Correct the inequality and asymptotic constant.

20. Recheck Chebyshev second-kind sup-norm statement.
    - Current issue: The claimed monic `U_d` sup norm should be independently verified before being used to predict performance.
    - Required change: Either cite the exact formula or remove the quantitative prediction.

21. Clarify whether the filter is `T_d`, reciprocal `T_d^*`, full preconditioned signal, or residual hint in each section.
    - Current issue: The notation switches between these objects, which makes several claims ambiguous.
    - Required change: Add a notation table:
      - `T_d`: classical Chebyshev polynomial.
      - `\tilde T_d`: monic Chebyshev polynomial.
      - `p(z)=\tilde T_d^*(z)`: reciprocal monic FIR polynomial.
      - `H(omega)`: full-filter frequency response.
      - `\widetilde H(omega)=H(omega)-1`: residual-channel response.

22. Check appendix consistency with main text.
    - Current issue: Some appendix tables use seed-0 ablation values while the main text reports five-seed means.
    - Required change: Label single-seed vs five-seed results consistently wherever values are compared.
    - Required change: Avoid mixing seed-0 “best” values with headline five-seed values without explicit caveats.

23. Reframe synthetic AR results.
    - Current issue: The text interprets MSE ratios as quantitatively confirming the spectral-residual benefit, but the setup does not isolate noise gain cleanly enough to support that exact decomposition.
    - Required change: Present the AR result as qualitatively consistent with a noise-amplification tradeoff rather than as a quantitative confirmation of the corollary.

## Suggested Revision Order

1. First fix notation and coefficient conventions across the paper.
2. Then replace or weaken the Marsden--Hazan theorem section.
3. Then correct the frequency-response and residual-filter sections.
4. Then remove or rewrite the noise-gain asymptotics and tradeoff corollary.
5. Then revise empirical interpretation language to match the corrected mathematics.
6. Finally clean up appendix table labels, statistics caveats, and wording consistency.
