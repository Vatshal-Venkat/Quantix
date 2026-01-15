# Unified Mathematics Domain Knowledge Base  
### Exam Level: JEE Main / EAMCET (Hard & High-Value)  
### Topics: Algebra, Probability, Basic Calculus, Linear Algebra  
### Usage: Deterministic Answer + Explanation Retrieval  
### Hallucination Policy: NONE (Domain KB Only)

---

## ALGEBRA (HARD FOCUS)

### Q1.
If the roots of the equation  
x² − (a + 2)x + a = 0  
are real and positive, then find the range of a.

**Answer:** (0, 4]

**Explanation:**  
For real roots, the discriminant must be non-negative.  
The discriminant is (a + 2)² − 4a = a² + 4.  
This is always positive, so reality is guaranteed.  
For positive roots, the sum of roots must be positive and the product must be positive.  
Sum of roots = a + 2 > 0 ⇒ a > −2.  
Product of roots = a > 0.  
Additionally, analyzing the nature of roots gives an upper bound a ≤ 4.  
Combining all conditions yields 0 < a ≤ 4.

**Source:** Algebra Domain Knowledge Base

---

### Q2.
The number of real solutions of  
|x² − 5x + 6| = |x − 2|  
is ______.

**Answer:** 3

**Explanation:**  
Factor the quadratic expression: x² − 5x + 6 = (x − 2)(x − 3).  
The absolute values change sign at x = 2 and x = 3.  
Consider intervals x < 2, 2 ≤ x < 3, and x ≥ 3.  
Solve the equation separately in each interval after removing moduli.  
Three distinct real values satisfy the original equation.  
Each must be checked in the original expression.

**Source:** Algebra Domain Knowledge Base

---

### Q3.
If α and β are the roots of  
x² − 4x + 1 = 0,  
find α³ + β³.

**Answer:** 52

**Explanation:**  
Use the identity α³ + β³ = (α + β)³ − 3αβ(α + β).  
From the given equation, α + β = 4 and αβ = 1.  
Substituting gives (4)³ − 3(1)(4).  
This evaluates to 64 − 12 = 52.  
Hence, the required value is 52.

**Source:** Algebra Domain Knowledge Base

---

### Q4.
Find the number of integral solutions of  
x² − y² = 15.

**Answer:** 8

**Explanation:**  
Rewrite the equation as (x − y)(x + y) = 15.  
List all integer factor pairs of 15 including negatives.  
For each factor pair, solve for x and y.  
Each valid factor pair gives a unique integer solution.  
Counting all such pairs gives a total of 8 solutions.

**Source:** Algebra Domain Knowledge Base

---

### Q5.
Let A = {1, 2, 3, 4}.  
Find the number of onto functions from A to A.

**Answer:** 9

**Explanation:**  
Total number of functions from A to A is 4⁴.  
To count onto functions, subtract functions that miss at least one element.  
Apply the principle of inclusion–exclusion.  
Subtract functions missing one element, add those missing two, and so on.  
Evaluating the expression gives 9 onto functions.

**Source:** Algebra Domain Knowledge Base

---

### Q6.
Solve the equation  
x² − |x| − 2 = 0.

**Answer:** x = −1, 2

**Explanation:**  
Consider two cases: x ≥ 0 and x < 0.  
For x ≥ 0, |x| = x, giving x² − x − 2 = 0.  
Solving yields x = 2 or −1, but only x = 2 is valid here.  
For x < 0, |x| = −x, giving x² + x − 2 = 0.  
Solving gives x = −1 or 2, but only x = −1 is valid.  
Hence, solutions are −1 and 2.

**Source:** Algebra Domain Knowledge Base

---

## PROBABILITY (HARD & TRICKY)

### Q7.
Two dice are thrown. Find the probability that the sum is a prime number.

**Answer:** 5/12

**Explanation:**  
Possible sums range from 2 to 12.  
Prime sums are 2, 3, 5, 7, and 11.  
Count outcomes for each prime sum.  
Total favorable outcomes = 15.  
Total outcomes = 36.  
Probability = 15/36 = 5/12.

**Source:** Probability Domain Knowledge Base

---

### Q8.
A die is thrown repeatedly until a six appears.  
Find the probability that the first six appears on the third throw.

**Answer:** 25/216

**Explanation:**  
The first two throws must not be six, and the third must be six.  
Probability = (5/6) × (5/6) × (1/6).  
This equals 25/216.

**Source:** Probability Domain Knowledge Base

---

### Q9.
Three cards are drawn from a standard deck.  
Find the probability that all are face cards.

**Answer:** 11/850

**Explanation:**  
There are 12 face cards in a deck of 52.  
Ways to choose 3 face cards = C(12,3).  
Total ways to choose any 3 cards = C(52,3).  
The ratio simplifies to 11/850.

**Source:** Probability Domain Knowledge Base

---

### Q10.
A coin is tossed 5 times.  
Find the probability of getting at least one head.

**Answer:** 31/32

**Explanation:**  
Use the complement method.  
Probability of no head (all tails) = (1/2)⁵ = 1/32.  
Thus, probability of at least one head = 1 − 1/32 = 31/32.

**Source:** Probability Domain Knowledge Base

---

## BASIC CALCULUS  
*(Limits, Derivatives, Simple Optimization)*

### Q11.
Evaluate  
limₓ→0 (sin 3x) / (x cos 2x).

**Answer:** 3

**Explanation:**  
Rewrite as (sin 3x / 3x) × (3 / cos 2x).  
As x → 0, sin 3x / 3x → 1.  
Also, cos 2x → 1.  
Thus, the limit evaluates to 3.

**Source:** Basic Calculus Domain Knowledge Base

---

### Q12.
If f(x) = x³ − 3x² + 4, find the number of local extrema.

**Answer:** 2

**Explanation:**  
Differentiate f(x) to get f′(x) = 3x² − 6x.  
Set f′(x) = 0 to find critical points.  
This gives x = 0 and x = 2.  
Since there are two distinct critical points, there are two local extrema.

**Source:** Basic Calculus Domain Knowledge Base

---

### Q13.
Find the minimum value of  
x² + 1/x², x ≠ 0.

**Answer:** 2

**Explanation:**  
Apply the AM–GM inequality.  
x² + 1/x² ≥ 2√(x² · 1/x²) = 2.  
Equality holds when x² = 1/x² ⇒ x = ±1.  
Hence, the minimum value is 2.

**Source:** Basic Calculus Domain Knowledge Base

---

### Q14.
Find the maximum value of  
y = −x² + 4x + 1.

**Answer:** 5

**Explanation:**  
This is a downward opening parabola.  
The maximum occurs at x = −b / (2a).  
Here a = −1, b = 4, so x = 2.  
Substitute x = 2 to get y = 5.

**Source:** Basic Calculus Domain Knowledge Base

---

## LINEAR ALGEBRA (CORE JEE)

### Q15.
If  
| 2  1 |  
| 4  2 |  
represents matrix A, find |A|.

**Answer:** 0

**Explanation:**  
Determinant of a 2×2 matrix is ad − bc.  
Here ad = 4 and bc = 4.  
Thus determinant = 0, meaning the matrix is singular.

**Source:** Linear Algebra Domain Knowledge Base

---

### Q16.
If A is a 3×3 matrix and |A| = 5, find |2A|.

**Answer:** 40

**Explanation:**  
For an n×n matrix, |kA| = kⁿ|A|.  
Here n = 3 and k = 2.  
Thus |2A| = 2³ × 5 = 40.

**Source:** Linear Algebra Domain Knowledge Base

---

### Q17.
The number of solutions of the system  
x + y + z = 3  
2x + 2y + 2z = 6  
is ______.

**Answer:** Infinitely many

**Explanation:**  
The second equation is a multiple of the first.  
Thus both represent the same plane.  
Hence, the system has infinitely many solutions.

**Source:** Linear Algebra Domain Knowledge Base

---

### Q18.
If A² = A for a square matrix A, identify the type of matrix.

**Answer:** Idempotent

**Explanation:**  
A matrix satisfying A² = A is, by definition, idempotent.  
Such matrices often represent projection transformations.

**Source:** Linear Algebra Domain Knowledge Base

---

## END OF UNIFIED KNOWLEDGE BASE
