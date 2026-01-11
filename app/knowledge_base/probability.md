# Probability

## Basic Concepts
- Classical: P(A) = favorable / total (equally likely)
- Axiomatic: 0 ≤ P(A) ≤ 1, P(S) = 1, P(A∪B) = P(A) + P(B) − P(A∩B)

## Important Theorems
- Addition: P(A∪B) = P(A) + P(B) − P(A∩B)
- Multiplication: P(A∩B) = P(A)·P(B|A)
- Independent events: P(A∩B) = P(A)·P(B) ⇔ P(A|B) = P(A)
- Bayes' Theorem:  
  \( P(B_i|A) = \frac{P(A|B_i) P(B_i)}{\sum P(A|B_j) P(B_j)} \)

## Random Variables
### Discrete
- Binomial: n trials, success probability p  
  P(X = k) = \( \binom{n}{k} p^k (1-p)^{n-k} \)  
  Mean = np, Variance = np(1-p)

### Continuous (JEE Advanced level)
- Uniform, Exponential, Normal (properties only)

## Expectation & Variance
- E(X) = ∑ x·P(x)   or   ∫ x·f(x) dx
- Var(X) = E(X²) − [E(X)]²
- For independent X,Y:  
  E(XY) = E(X)E(Y)  
  Var(X+Y) = Var(X) + Var(Y)

## Common Inequalities (Advanced)
- Markov: P(X ≥ a) ≤ E(X)/a  (X ≥ 0)
- Chebyshev: P(|X − μ| ≥ kσ) ≤ 1/k²