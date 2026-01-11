# Calculus

## Limits – Standard Results
- \( \lim_{x\to0} \frac{\sin x}{x} = 1 \)
- \( \lim_{x\to0} \frac{\tan x}{x} = 1 \)
- \( \lim_{x\to0} \frac{1 - \cos x}{x^2} = \frac{1}{2} \)
- \( \lim_{x\to0} (1 + x)^{1/x} = e \)
- \( \lim_{x\to\infty} \left(1 + \frac{a}{x}\right)^x = e^a \)

## Differentiation
- Chain rule, product rule, quotient rule
- Derivatives of inverse trig functions:
  - \( \frac{d}{dx} \sin^{-1}x = \frac{1}{\sqrt{1-x^2}} \)
  - \( \frac{d}{dx} \tan^{-1}x = \frac{1}{1+x^2} \)
  - \( \frac{d}{dx} \sec^{-1}x = \frac{1}{|x|\sqrt{x^2-1}} \)

## Applications of Derivatives
- Rate of change
- Tangents & normals
- Monotonicity: f'(x) > 0 ⇒ increasing
- Maxima/Minima: f'(c) = 0, f''(c) > 0 ⇒ minima
- Rolle's theorem, Lagrange's Mean Value Theorem
- Concavity: f''(x) > 0 ⇒ concave up

## Indefinite Integration – Important Forms
- \( \int \frac{dx}{a^2 + x^2} = \frac{1}{a}\tan^{-1}\frac{x}{a} + C \)
- \( \int \frac{dx}{a^2 - x^2} = \frac{1}{2a}\ln\left|\frac{a+x}{a-x}\right| + C \)
- \( \int \frac{dx}{\sqrt{x^2 \pm a^2}} \), \( \int \sqrt{x^2 \pm a^2}\,dx \), \( \int \sqrt{a^2 - x^2}\,dx \)
- Integration by parts: \( \int u\,dv = uv - \int v\,du \)
- Standard order (ILATE): Inverse → Log → Algebraic → Trig → Exp

## Definite Integration – Properties
- \( \int_a^b f(x)\,dx = \int_a^b f(a+b-x)\,dx \)
- Even function: \( \int_{-a}^a f(x)\,dx = 2\int_0^a f(x)\,dx \)
- Odd function: \( \int_{-a}^a f(x)\,dx = 0 \)
- Reduction formulae for \( \int \sin^n x \, dx \), \( \int \cos^n x \, dx \)

## Beta & Gamma Functions (Advanced JEE)
- \( B(m,n) = \int_0^1 t^{m-1}(1-t)^{n-1} dt = \frac{\Gamma(m)\Gamma(n)}{\Gamma(m+n)} \)
- \( \int_0^{\pi/2} \sin^{p-1}\theta \cos^{q-1}\theta \, d\theta = \frac{1}{2} B\left(\frac{p}{2},\frac{q}{2}\right) \)