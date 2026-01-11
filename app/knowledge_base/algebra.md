# Algebra

## Quadratic Equations
- General form: \( ax^2 + bx + c = 0 \), \( a \neq 0 \)
- Roots: \( x = \frac{-b \pm \sqrt{b^2 - 4ac}}{2a} \)
- Discriminant: \( D = b^2 - 4ac \)
  - \( D > 0 \): two distinct real roots
  - \( D = 0 \): two equal real roots
  - \( D < 0 \): complex conjugate roots
- Sum of roots: \( -\frac{b}{a} \)
- Product of roots: \( \frac{c}{a} \)
- Nature of roots (when coefficients rational):
  - D perfect square → rational roots
  - D not perfect square → irrational roots (conjugates)
- Condition for common root between two quadratics

## Sequences & Series

### Arithmetic Progression (AP)
- nth term: \( a_n = a + (n-1)d \)
- Sum of first n terms:  
  \( S_n = \frac{n}{2} [2a + (n-1)d] \)  
  \( S_n = \frac{n}{2} (a + l) \) (l = last term)

### Geometric Progression (GP)
- nth term: \( a_n = a r^{n-1} \)
- Sum of first n terms:  
  \( S_n = a \frac{r^n - 1}{r - 1} \) (r ≠ 1)  
  Infinite GP (|r| < 1): \( S_\infty = \frac{a}{1-r} \)

### Special Sums
- \( \sum_{k=1}^n k = \frac{n(n+1)}{2} \)
- \( \sum_{k=1}^n k^2 = \frac{n(n+1)(2n+1)}{6} \)
- \( \sum_{k=1}^n k^3 = \left( \frac{n(n+1)}{2} \right)^2 \)

### Means
- AM ≥ GM ≥ HM  
- AM = \( \frac{a+b}{2} \), GM = \( \sqrt{ab} \), HM = \( \frac{2ab}{a+b} \)  
- \( \text{GM}^2 = \text{AM} \times \text{HM} \)

## Binomial Theorem
\( (x + y)^n = \sum_{k=0}^n \binom{n}{k} x^{n-k} y^k \)

General term: \( T_{r+1} = \binom{n}{r} x^{n-r} y^r \)

Important identities:
- \( \sum \binom{n}{k} = 2^n \)
- \( \sum (-1)^k \binom{n}{k} = 0 \) (n > 0)
- \( \sum_{k=0}^n \binom{n}{k}^2 = \binom{2n}{n} \)
- \( \binom{n}{r} = \binom{n}{n-r} \)

## Permutations & Combinations
- \( ^nP_r = \frac{n!}{(n-r)!} \)
- \( ^nC_r = \binom{n}{r} = \frac{n!}{r!(n-r)!} \)
- Circular permutation of n distinct objects: (n−1)!
- Number of ways to divide 2n people in n pairs: \( \frac{(2n)!}{2^n \cdot n!} \)
- Derangement of n objects:  
  \( !n = n! \sum_{k=0}^n \frac{(-1)^k}{k!} \approx \frac{n!}{e} \)

## Complex Numbers
- \( z = a + bi \), \( i^2 = -1 \)
- Modulus: \( |z| = \sqrt{a^2 + b^2} \)
- Argument: \( \theta = \arg(z) \)
- Polar form: \( z = r (\cos\theta + i \sin\theta) \)
- De Moivre: \( [r(\cos\theta + i\sin\theta)]^n = r^n (\cos n\theta + i \sin n\theta) \)
- nth roots of unity: solutions of \( z^n = 1 \)
- Cube roots of unity: 1, ω, ω² where ω = e^(2πi/3), 1 + ω + ω² = 0

## Important Identities
- (a + b)³ = a³ + b³ + 3ab(a + b)
- a³ + b³ + c³ − 3abc = (a + b + c)(a² + b² + c² − ab − bc − ca)