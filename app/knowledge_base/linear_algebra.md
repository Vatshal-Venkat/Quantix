# Linear Algebra

## Matrices
- Types: square, diagonal, scalar, identity, symmetric, skew-symmetric
- Operations: addition, scalar multiplication, matrix multiplication
- Properties of transpose: (AB)^T = B^T A^T
- Inverse exists ⇔ det ≠ 0
- For 2×2 matrix \( \begin{bmatrix} a & b \\ c & d \end{bmatrix} \):  
  inverse = \( \frac{1}{ad-bc} \begin{bmatrix} d & -b \\ -c & a \end{bmatrix} \)

## Determinants
- 3×3 expansion: along any row/column
- Properties:
  - det(A^T) = det(A)
  - det(AB) = det(A)det(B)
  - If two rows/columns identical → det = 0
  - Multiplying row by k → det multiplies by k

## System of Linear Equations
- Consistent & unique ⇔ det(A) ≠ 0
- Infinite solutions ⇔ det(A) = 0 and consistent
- No solution ⇔ det(A) = 0 and inconsistent

## Vectors (3D)
- Dot product: \( \vec{a}\cdot\vec{b} = |\vec{a}||\vec{b}|\cos\theta \)
- Cross product: magnitude = area of parallelogram
- Scalar triple product: \( [\vec{a},\vec{b},\vec{c}] = \vec{a}\cdot(\vec{b}\times\vec{c}) \)  
  = volume of parallelepiped
- Coplanar if scalar triple product = 0

## Shortest Distance (Skew Lines)
Distance between two skew lines  
\( \vec{r} = \vec{a_1} + t\vec{d_1} \) and \( \vec{r} = \vec{a_2} + s\vec{d_2} \):  
\( d = \frac{|(\vec{a_2} - \vec{a_1}) \cdot (\vec{d_1} \times \vec{d_2})|}{|\vec{d_1} \times \vec{d_2}|} \)

## Plane
General equation: ax + by + cz + d = 0  
Distance from point (x₀,y₀,z₀): \( \frac{|ax_0 + by_0 + cz_0 + d|}{\sqrt{a^2 + b^2 + c^2}} \)