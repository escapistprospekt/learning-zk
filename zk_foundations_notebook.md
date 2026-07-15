# ZK Foundations Notebook

> A comprehensive reference built from the "Learning ZK" conversation.
> Covers everything from first principles through elliptic curves and circuit constraints.

---

## Table of Contents

1. [Zero-Knowledge Proofs — Core Definition](#1-zero-knowledge-proofs--core-definition)
2. [Set Theory & Logic](#2-set-theory--logic)
3. [Modular Arithmetic](#3-modular-arithmetic)
4. [Finite Fields](#4-finite-fields)
5. [Binary Exponentiation & Discrete Logarithm](#5-binary-exponentiation--discrete-logarithm)
6. [Linear Algebra for ZK](#6-linear-algebra-for-zk)
7. [Abstract Algebra — Groups & Structures](#7-abstract-algebra--groups--structures)
8. [Boolean Circuits as Arithmetic Constraints](#8-boolean-circuits-as-arithmetic-constraints)
9. [Elliptic Curves](#9-elliptic-curves)
10. [Diffie-Hellman Key Exchange](#10-diffie-hellman-key-exchange)
11. [Python Toolkit for ZK Arithmetic](#11-python-toolkit-for-zk-arithmetic)

---

## 1. Zero-Knowledge Proofs — Core Definition

### Definition

A **zero-knowledge proof (ZKP)** is a cryptographic protocol in which one party (the **prover**) convinces another party (the **verifier**) that a statement is true **without revealing anything beyond the truth of the statement itself**.

### The Three Properties

| Property | Meaning |
|---|---|
| **Completeness** | If the statement is true and both parties are honest, the verifier will be convinced. |
| **Soundness** | A cheating prover cannot convince the verifier of a false statement, except with negligible probability. |
| **Zero-knowledge** | The verifier learns nothing beyond the fact that the statement is true. |

### Key Terminology

- **Statement**: The claim being proved, e.g. "I know values x, y satisfying these equations."
- **Witness**: The secret information that makes the statement true (e.g. the actual values x, y).
- **Proof**: The protocol output that convinces the verifier without revealing the witness.

### Common Misconception

> "A ZKP is a solution to a system of equations."

**Wrong.** The *solution* is the **witness**. The ZKP is the **protocol** that proves knowledge of a witness without revealing it.

### Accurate Informal Definition

> A protocol that convinces a verifier that there exists a witness satisfying a system of equations, without revealing anything useful about the witness itself.

---

## 2. Set Theory & Logic

### Sets

A **set** is an unordered collection of distinct elements.

- **Notation**: `{1, 2, 3}`, or `S = {x ∈ Z | x > 0}`
- **Membership**: `a ∈ S` means "a is an element of S"
- **∉** means "not a member of"

### Subsets

- `A ⊆ B`: every element of A is also in B (A is a **subset** of B)
- `A ⊂ B`: A ⊆ B and A ≠ B (**proper subset** — A is strictly smaller)

### Set Operations

| Operation | Symbol | Meaning |
|---|---|---|
| Union | A ∪ B | all elements in A or B (or both) |
| Intersection | A ∩ B | elements that are in both A and B |
| Difference | A \ B | elements in A but not in B |

### Set Membership as a Constraint

To encode `x ∈ {a, b, c}` as an arithmetic constraint:

```
(x - a)(x - b)(x - c) = 0
```

This polynomial is zero exactly when x equals a, b, or c.

---

## 3. Modular Arithmetic

### Congruence Modulo q — Definition

**Two integers a and b are congruent modulo q if their difference is divisible by q.**

```
a ≡ b (mod q)  ⟺  q | (a - b)  ⟺  a - b = kq for some integer k
```

This is the **fundamental definition**. The "same remainder" framing is a consequence.

**Example (mod 11):**
```
3 ≡ -8 (mod 11)  because  3 - (-8) = 11  and  11 | 11
```

### Congruence Class

The **congruence class** of `a` modulo `q` is the set of all integers congruent to `a`:

```
[a] = { x ∈ Z | x ≡ a (mod q) }
    = { ..., a - 2q, a - q, a, a + q, a + 2q, ... }
```

**Example (mod 5):**
```
[2] = { ..., -8, -3, 2, 7, 12, 17, ... }
```

Modulo q, there are exactly q distinct congruence classes: `[0], [1], ..., [q-1]`.

### Negative Integers in Python

Python's `%` operator always returns a non-negative result when the divisor is positive:

```python
-3 % 7  # → 4
```

**Why?** Python finds q and r such that `a = bq + r` with `0 ≤ r < b`:
```
-3 = 7(-1) + 4   ✓  (since -7 + 4 = -3)
```

**Mathematical intuition:** On a mod-7 number circle, going 3 steps backward from 0 lands on 4.

```
-3 + 7 = 4  (adding one full period doesn't change the congruence class)
```

### Additive Inverse (mod q)

The additive inverse of x modulo q is the value y such that `x + y ≡ 0 (mod q)`.

**Formula:**
```
-x ≡ q - x  (mod q)       for x ≠ 0
-0 ≡ 0      (mod q)
```

**Pattern:**
```
-1 ≡ q-1,   -2 ≡ q-2,   -k ≡ q-k   (mod q)
```

**Example (mod 17):**
```
-5 ≡ 12   (mod 17)   because  5 + 12 = 17 ≡ 0
-1 ≡ 16   (mod 17)   because  1 + 16 = 17 ≡ 0
```

**Python:**
```python
(-x) % q        # always gives the canonical representative in [0, q)
(q - x) % q    # equivalent
```

### Multiplicative Inverse (mod q)

The multiplicative inverse of a modulo q is the value x such that `a * x ≡ 1 (mod q)`.

**Existence condition:** The inverse exists **if and only if** `gcd(a, q) = 1` (a and q are coprime).

**Example — why 2 has no inverse mod 6:**
```
gcd(2, 6) = 2 ≠ 1   ⟹  no inverse exists
2x is always even, so 2x - 1 is always odd, never divisible by 6
```

**When q is prime**, every non-zero element has a multiplicative inverse (since gcd(a, q) = 1 for all a ≠ 0).

**Python:**
```python
pow(a, -1, q)   # returns a^{-1} mod q  (Python 3.8+)
```

### Division in Modular Arithmetic

In a finite field (q prime), division is **multiplication by the inverse**:

```
n/m  ≡  n * m^{-1}  (mod q)
```

**Python:**
```python
(n * pow(m, -1, q)) % q
```

**Negative rational -n/m mod q:**
```python
(-n * pow(m, -1, q)) % q
```

**Example:** Compute -12/17 (mod 13):
```python
# 17 ≡ 4 (mod 13), inverse of 4 mod 13 is 10 (since 4*10=40≡1)
(-12 * pow(17, -1, 13)) % 13
# → 10
```

Verify: `10 * 17 ≡ 10 * 4 = 40 ≡ 1 (mod 13)`, so `10 ≡ 17^{-1}`, then `-12 * 10 = -120 ≡ 10 (mod 13)`.

### Solving Linear Equations mod q

To solve `ax + b ≡ c (mod q)`:

```
ax ≡ c - b  (mod q)
x  ≡ (c - b) * a^{-1}  (mod q)
```

**Python:**
```python
x = (c - b) * pow(a, -1, q) % q
```

**Example:** Solve `3x + 5 ≡ 7 (mod 17)`:
```python
x = (7 - 5) * pow(3, -1, 17) % 17
# pow(3,-1,17) = 6  (since 3*6=18≡1 mod 17)
# x = 2 * 6 % 17 = 12
```

Verify: `3*12 + 5 = 41 ≡ 7 (mod 17)` ✓

### Deferred vs. Immediate Modulo Reduction

You can reduce modulo q at any intermediate step — the final result is the same. This keeps numbers small during computation, which matters in cryptography.

```python
# Both are equivalent:
(a * b + c) % q
((a % q) * (b % q) + c % q) % q
```

---

## 4. Finite Fields

### Definition (in Terms of Groups)

A **finite field** F_q is a **finite set** equipped with two binary operations (+ and ×) satisfying:

1. **(F, +) is an abelian group** — closed, associative, has additive identity 0, every element has an additive inverse, and addition is commutative.
2. **(F \ {0}, ×) is an abelian group** — closed, associative, has multiplicative identity 1, every non-zero element has a multiplicative inverse, and multiplication is commutative.
3. **Distributivity** — multiplication distributes over addition:
   ```
   a(b + c) = ab + ac
   ```

### Why Distributivity Matters

Distributivity links the two group structures. Without it, you have two separate groups — but not a field. Distributivity is what allows algebraic manipulation (factoring, expanding) that makes fields useful for polynomial arithmetic and zk-SNARKs.

### Order and Characteristic

- The **order** of a finite field is the number of elements it contains.
- A finite field of order q exists **if and only if q = p^n** for some prime p and positive integer n.
- The **characteristic** of F_{p^n} is p — the smallest positive integer such that adding the multiplicative identity to itself p times gives 0:
  ```
  1 + 1 + ... + 1  (p times) = 0
  ```

**Mathematical relationship:**
```
If field has order q = p^n, then characteristic = p
```

**Why order 15 is impossible:**
```
15 = 3 × 5   (not of the form p^n)
⟹  no finite field of order 15 exists
```

**Why order 2 is possible:**
```
2 = 2^1  (prime)
F_2 = {0, 1}
+ : 0+0=0, 0+1=1, 1+0=1, 1+1=0
× : only non-zero element is 1, and 1*1=1
Multiplicative group = {1} — a trivial group, but still a valid group of order 1
```

### The Standard Finite Field F_q (q prime)

When q is prime, F_q = {0, 1, 2, ..., q-1} with addition and multiplication modulo q.

**Example — F_17:**
```
Elements: {0, 1, 2, ..., 16}
Addition: (a + b) mod 17
Multiplication: (a * b) mod 17
Inverse of 6: pow(6, -1, 17) = 3   (since 6*3=18≡1 mod 17)
2/3 in F_17: 2 * pow(3,-1,17) % 17 = 2 * 6 % 17 = 12
```

**Python using the galois library:**
```python
import galois
GF = galois.GF(q)         # defines the field F_q
z = GF(x) / GF(y)        # field division; z holds an element of F_q
                          # z is of type galois.FieldArray (not a plain int)
```

---

## 5. Binary Exponentiation & Discrete Logarithm

### Binary Exponentiation (Repeated Squaring)

To compute `g^n (mod q)`, instead of n-1 multiplications, use the binary representation of n.

**Algorithm:**
1. Write n in binary.
2. Build powers of g by repeated squaring: g^1, g^2, g^4, g^8, ...
3. Multiply together only the powers corresponding to set bits (1s) in n's binary form.
4. Reduce mod q at every step to keep numbers small.

**Example — g^50 (mod q):**
```
50 = 110010₂ = 32 + 16 + 2

Squarings:  g¹ → g² → g⁴ → g⁸ → g¹⁶ → g³²   (5 squarings)
Result:     g^50 = g^32 * g^16 * g^2            (2 multiplications)
Total: 7 multiplications  vs  49 naive
```

**Example — g^1000 (mod q):**
```
1000 = 1111101000₂ = 512+256+128+64+32+8

Squarings: g → g² → g⁴ → ... → g^512   (9 squarings)
Multiply 6 terms: 5 multiplications
Total: 14 multiplications  vs  999 naive
```

**Example — 3^7:**
```
7 = 111₂ = 4 + 2 + 1
3¹ = 3
3² = 9
3⁴ = 81
3^7 = 81 * 9 * 3 = 2187
```

**General formula for number of multiplications:**
```
⌊log₂(n)⌋  +  (number of 1-bits in n)  -  1
```

For n=1000: 9 + 6 - 1 = 14 multiplications.

**Recursive view:**
```
a^n = (a^{n/2})²           if n is even
a^n = a * (a^{(n-1)/2})²   if n is odd
```

### Discrete Logarithm

Given `g`, `q`, and `v = g^x (mod q)`, the **discrete logarithm** is the problem of finding `x`.

**Example:** Find x such that `3^x ≡ 5 (mod 7)`:
```
3¹ ≡ 3 (mod 7)
3² ≡ 2 (mod 7)   (9 mod 7 = 2)
3³ ≡ 6 (mod 7)   (2*3=6)
3⁴ ≡ 4 (mod 7)   (6*3=18≡4)
3⁵ ≡ 5 (mod 7)   ← found it!  x = 5
3⁶ ≡ 1 (mod 7)   (order of 3 in F_7 is 6)
```

The sequence `3, 2, 6, 4, 5, 1, 3, 2, ...` cycles with period 6 — 3 is a **generator** of the multiplicative group of F_7.

### Discrete Log Assumption

> Given g, q, and v = g^x (mod q), it is computationally infeasible for a classical computer to find x.

This is the **hardness assumption** that underpins Diffie-Hellman and many ZK systems. The inverse problem (computing g^x from x) is easy; recovering x from g^x is hard.

**Common mistake:** "Discrete log" refers to the **exponent** x, not the base or the result. It's called a "log" because it's the modular analogue of a logarithm.

### Discrete Log and Quantum Computing

- **Shor's algorithm** (quantum) can compute discrete logarithms (and factor large integers) in polynomial time.
- This would break Diffie-Hellman and RSA-style systems.
- Classical computers cannot run Shor's efficiently — so the discrete log assumption holds for classical adversaries.
- This is why post-quantum cryptography is an active research area: ZK systems relying on discrete log would be vulnerable to a sufficiently powerful quantum computer.

**Order / Period (relevant to Shor's):**
- The **order** of an element g in a group is the smallest positive integer r such that `g^r = identity`.
- In F_7*, the order of 3 is 6 (since 3^6 ≡ 1 mod 7).
- Shor's algorithm finds this period r efficiently on a quantum computer.

---

## 6. Linear Algebra for ZK

### Vectors

A **vector** is an ordered list of numbers (unlike a set, order matters):

```
v = [1, 2, 3]   ≠   [3, 2, 1]
```

Vectors represent witness values, polynomial coefficients, constraint rows, etc.

**Vector addition** (element-wise):
```
[1, 2, 3] + [4, 5, 6] = [5, 7, 9]
```

**Scalar multiplication:**
```
3 * [1, 2, 3] = [3, 6, 9]
```

### Hadamard Product

The **Hadamard product** (symbol ∘) is element-wise multiplication of two vectors of the same length:

```
[1, 2, 3] ∘ [4, 5, 6] = [1*4, 2*5, 3*6] = [4, 10, 18]
```

Result is **another vector** of the same length.

**Key distinction — Hadamard vs Dot product:**

| Operation | Formula | Result |
|---|---|---|
| Hadamard | a ∘ b = [a₁b₁, a₂b₂, ..., aₙbₙ] | vector |
| Dot / inner product | a · b = Σ aᵢbᵢ | scalar |

Hadamard products are always computed between vectors (or matrices) of the same shape.

### Inner Product (Dot Product)

The inner product of two vectors is the sum of their element-wise products:

```
[1, 2, 3] · [4, 5, 6] = 1*4 + 2*5 + 3*6 = 4 + 10 + 18 = 32
```

**Relationship to Hadamard:**
> The inner product = sum of elements of the Hadamard product.
```
a · b = sum(a ∘ b)
```

### Matrix-Vector Multiplication

Multiplying a matrix M by a vector v produces a new vector where each element is the inner product of a row of M with v:

```
M * v = [ row₁ · v,  row₂ · v,  row₃ · v, ... ]
```

**Relationship to inner products:**
> Matrix-vector multiplication is a sequence of inner products — one per row of the matrix.

### R1CS (Rank-1 Constraint System)

In zk-SNARKs, constraints take the form:

```
(A * w) ∘ (B * w) = C * w
```

where A, B, C are matrices, w is the witness vector, and ∘ is the Hadamard product. This is why both matrix multiplication (inner products) and Hadamard products are foundational.

---

## 7. Abstract Algebra — Groups & Structures

### Binary Operations

A **binary operation** ★ on a set S takes two elements from S and returns one element. Key properties to check:

| Property | Definition |
|---|---|
| **Closure** | a ★ b ∈ S for all a, b ∈ S |
| **Associativity** | (a ★ b) ★ c = a ★ (b ★ c) |
| **Commutativity** | a ★ b = b ★ a |
| **Identity** | ∃ e ∈ S: e ★ a = a ★ e = a for all a |
| **Inverse** | ∀ a ∈ S, ∃ a⁻¹: a ★ a⁻¹ = e |

**Examples of non-associative operations:**
- Subtraction on integers: `(5-3)-1 = 1 ≠ 5-(3-1) = 3`
- The custom operation `a ★ b = a² + b`: `(2★3)★4 = 7★4 = 53`, but `2★(3★4) = 2★13 = 17` — not equal.

**Why addition on even integers is associative** (but subtraction is not):
- Even integers under addition: closed ✓, associative ✓ (inherited from integers), has identity 0 ✓, inverses -2n ✓.
- Subtraction is not associative on any set because `(a-b)-c ≠ a-(b-c)` in general.

### Algebraic Hierarchy

```
Magma          = set + closed binary operation
  ↓
Semigroup      = Magma + associativity
  ↓
Monoid         = Semigroup + identity element
  ↓
Group          = Monoid + inverses for every element
  ↓
Abelian Group  = Group + commutativity
```

**Magma example** — the operation `a ★ b = a² + b` on integers:
- Closed: yes (integer + integer = integer)
- Not associative: (2★3)★4 ≠ 2★(3★4)
- So it's a magma but not a semigroup.

**Subtraction on integers** — closed but not associative, so it's a magma (not a semigroup).

### Group

A **group** (G, ★) is a set G with a binary operation ★ satisfying:
1. **Closure**: a ★ b ∈ G for all a, b ∈ G
2. **Associativity**: (a ★ b) ★ c = a ★ (b ★ c)
3. **Identity**: ∃ e ∈ G such that e ★ a = a ★ e = a
4. **Inverses**: for every a ∈ G, ∃ a⁻¹ ∈ G such that a ★ a⁻¹ = e

**Size / Order:** The order of a group is the number of elements in G.

**Examples:**
- (Z, +): integers under addition — infinite abelian group
- (Z/qZ, +): integers mod q under addition — finite abelian group of order q
- (F_q*, ×): non-zero integers mod prime q under multiplication — finite abelian group of order q-1
- {1,2,3,4} under multiplication mod 5 — cyclic group of order 4

### Trivial Group

The **trivial group** ({e}, ★) contains only the identity element. It has order 1.

Example: the multiplicative group of F_2 = {1} under multiplication — just the identity.

### Group Properties

**Cancellation Law:**
> If ab = ac, then b = c.

Proof:
```
ab = ac
a⁻¹(ab) = a⁻¹(ac)     [multiply both sides by a⁻¹]
(a⁻¹a)b = (a⁻¹a)c     [associativity]
eb = ec                 [a⁻¹a = e]
b = c                   [identity]
```

**Uniqueness of Inverses:**
> Every element in a group has exactly one inverse.

Proof: Suppose b and c are both inverses of a. Then:
```
ab = e  and  ac = e
ab = ac
b = c   [cancellation law]
```

### Cyclic Groups and Generators

A **cyclic group** is a group where every element can be expressed as a power of a single element g, called a **generator**:

```
G = { g⁰, g¹, g², g³, ..., g^{n-1} }
```

**Cyclic ≠ Commutative (Abelian):**
- Every cyclic group is abelian, but not all abelian groups are cyclic.
- Commutativity means order of operation doesn't matter (a★b = b★a).
- Cyclicity means every element is a power of one generator.

**Example:** Prove {1,2,3,4} under multiplication mod 5 is cyclic:
```
g = 2:
  2¹ ≡ 2
  2² ≡ 4
  2³ ≡ 3  (8 mod 5)
  2⁴ ≡ 1  (16 mod 5)
Every element {1,2,3,4} appears → 2 is a generator ✓
```

### Coprimes and Generators

- Numbers **coprime to n** share no common factor with n (gcd = 1).
- Composite numbers (that share a factor with n) **cannot** be generators in Z/nZ under multiplication, because they lack a multiplicative inverse.
- For a prime p, every non-zero element is coprime to p → every non-zero element can potentially be a generator.

**Example (coprime to 8):** {1, 3, 5, 7} — these are coprime to 8. {2, 4, 6} are not (they share a factor of 2).

---

## 8. Boolean Circuits as Arithmetic Constraints

### Core Idea

In ZK circuits, we work over a finite field. Logical operations must be expressed as **polynomial equations**. The key insight: over F_q, multiplication is AND for binary variables.

### Forcing a Variable to be Binary

```
y(y - 1) = 0   ⟹   y ∈ {0, 1}
```

Apply this to every boolean wire in your circuit.

### Basic Boolean Gates as Arithmetic

| Logic | Arithmetic constraint |
|---|---|
| y = NOT x | y = 1 - x |
| z = x AND y | z = xy |
| z = x OR y | z = x + y - xy |
| z = x XOR y | z = x + y - 2xy |

**OR derivation:** For boolean a, b:
```
a ∨ b = a + b - ab
Verify:
  0 ∨ 0 = 0+0-0 = 0 ✓
  0 ∨ 1 = 0+1-0 = 1 ✓
  1 ∨ 0 = 1+0-0 = 1 ✓
  1 ∨ 1 = 1+1-1 = 1 ✓
```

### Is-Zero Gadget

Enforce y=1 when x=0, and y=0 when x≠0:

```
xy = 0
xz = 1 - y
```

where z is an auxiliary variable (acts as x⁻¹ when x ≠ 0).

**Analysis:**
- If x = 0: `0*z = 1-y` → y = 1. And `0*y = 0` ✓ automatically.
- If x ≠ 0: from `xy = 0` → y = 0. Then `xz = 1` → z = x⁻¹.

**Common mistake:** Only using `y(y-1)=0` and `xy=0` — this allows (x=0, y=0) as a valid assignment (doesn't force y=1 when x=0). The auxiliary constraint `xz = 1-y` is required to close this gap.

### Compound Boolean Expression: z = (x ∧ y) ∨ ¬u

Step-by-step construction:

```
// Booleanize inputs:
x(x-1) = 0
y(y-1) = 0
u(u-1) = 0

// Compute AND:
a = xy          // a = x ∧ y

// Compute NOT:
b = 1 - u       // b = ¬u

// Compute OR:
z = a + b - ab  // z = a ∨ b
```

**Simplified to one equation:**
```
z = xy + (1-u) - xy(1-u)
  = 1 - u + xyu
```

**Truth table:**
| x | y | u | z |
|---|---|---|---|
|0|0|0|1|
|0|0|1|0|
|0|1|0|1|
|0|1|1|0|
|1|0|0|1|
|1|0|1|0|
|1|1|0|1|
|1|1|1|1|

Pattern: if u=0, then z=1 always. If u=1, then z = x ∧ y.

### Indicator Function for Inverse (Binary NOT)

Enforce y is the binary inverse of x (x must itself be binary):

```
y = 1 - x   (and implicitly x(x-1) = 0)
```

### If Statements as Constraints

An if-statement `z = (cond ? a : b)` can be encoded as:

```
z = cond * a + (1 - cond) * b
```

where `cond` is a boolean variable.

### Static Single Assignment (SSA)

In ZK circuits, each variable can only be **assigned once**. To handle updates:

```
// Instead of:  x = x + 1
// Use:         x₂ = x₁ + 1
```

Every re-assignment creates a new named variable.

### Unrolling Bounded Loops

Loops must be unrolled to a fixed number of iterations (since circuits are static):

```python
# Instead of:
for i in range(n):
    x = f(x)
# Write:
x1 = f(x0)
x2 = f(x1)
...
xn = f(x_{n-1})
```

### Solving vs. Verifying

- **Solving** = finding a valid witness (hard in general)
- **Verifying** = checking that a given witness satisfies all constraints (easy — just evaluate)

This asymmetry is what makes ZKPs possible.

---

## 9. Elliptic Curves

### Definition

An **elliptic curve** over the reals is the set of points (x, y) satisfying:

```
y² = x³ + ax + b
```

for constants a, b, along with a special **point at infinity** O (the identity element).

**Non-singularity condition:** `4a³ + 27b² ≠ 0` (ensures the curve has no cusps or self-intersections).

**Why y² = x³ + ax + b?**
- The y² term makes the curve symmetric about the x-axis.
- The cubic x³ ensures three (possibly complex) roots when substituting a line, enabling a well-defined group law.
- The constraint `y² ≥ 0` over the reals naturally gives 0, 1, or 2 real intersection points with any vertical line.

**Why y = x³ + 18 is NOT an elliptic curve:**
- This is not in Weierstrass form (no y² term).
- An EC must have `y²` on the left — the square creates the symmetry needed for the group law.

### Vertical Line Intersections

For the curve `y² = x³ + b`, a vertical line `x = c` gives `y² = c³ + b`:

| Condition | Intersections |
|---|---|
| c³ + b < 0 | 0 (no real square root of a negative) |
| c³ + b = 0 | 1 (only y = 0) |
| c³ + b > 0 | 2 (y = ±√(c³+b)) |

### Point Addition on an Elliptic Curve

**Adding two distinct points P and Q:**
1. Draw the line through P and Q.
2. The line intersects the curve at a third point R'.
3. Reflect R' over the x-axis to get R.
4. R = P + Q.

**Why reflect?** The reflection ensures the operation is associative and that O (point at infinity) is the identity.

**Finding R algebraically** (for y² = x³ + ax + b, given P=(x₁,y₁) and Q=(x₂,y₂)):

```
slope:     m = (y₂ - y₁) / (x₂ - x₁)
x₃:        x₃ = m² - x₁ - x₂         [from Vieta's formula]
y₃:        y₃ = m(x₁ - x₃) - y₁      [then negate y for reflection]
```

**Vieta's formula insight:** When you substitute the line `y = mx + c` into `y² = x³ + ax + b`, you get a cubic in x. The three roots x₁, x₂, x₃ satisfy:

```
x₁ + x₂ + x₃ = m²    (for y² = x³ + x with coefficient of x² = 0 vs leading term)
```

So: `x₃ = m² - x₁ - x₂`.

**Example:** Points (2, -2) and (5, 11) on y² = x³ - 4:
```
m = (11-(-2))/(5-2) = 13/3 ≈ 4.33
x₃ = m² - x₁ - x₂ = (13/3)² - 2 - 5 ≈ 169/9 - 7 ≈ 11.78
y₃ = m(x₁ - x₃) - y₁ = (13/3)(2 - 11.78) - (-2) ≈ ...
```

### Point Doubling (Tangent Line)

When P = Q (adding a point to itself), the "line through P and Q" becomes the **tangent** to the curve at P.

**Finding the tangent slope** using implicit differentiation of `y² = x³ + ax + b`:

```
2y dy = (3x² + a) dx
dy/dx = (3x² + a) / (2y)    (the slope m at point P)
```

Then use the same formulas:
```
x₃ = m² - 2x₁
y₃ = m(x₁ - x₃) - y₁
```

**Why is there still a 3rd root for a tangent line?** When the line is tangent at P = (x₁, y₁), x₁ is a **double root** (multiplicity 2) of the cubic. By Vieta's formula, x₁ + x₁ + x₃ = m², so x₃ = m² - 2x₁. The tangent still hits the curve at a genuine second point (unless P is a point of inflection).

### Multiplicity

**Multiplicity** describes how "strongly" a curve touches another curve (or line) at a point:

- **Multiplicity 1**: the line crosses the curve transversally (ordinary intersection).
- **Multiplicity 2**: the line is tangent — it just touches the curve without crossing (double root).
- **Multiplicity 3**: the line is tangent at a point of inflection.

In terms of the cubic polynomial: if `f(x) = (x - x₁)^k * g(x)`, then x₁ is a root of multiplicity k.

### Elliptic Curves as a Group

The set of points on an EC together with the point at infinity O forms an **abelian group**:

| Property | How it's satisfied |
|---|---|
| Closure | P + Q is always another point on the curve (or O) |
| Associativity | Verified algebraically (non-trivial) |
| Identity | The point at infinity O: P + O = P |
| Inverse | -P = (x, -y): reflection over x-axis |
| Commutativity | P + Q = Q + P (the line through P,Q is the same as Q,P) |

---

## 10. Diffie-Hellman Key Exchange

### Setup

- Public parameters: generator g, prime modulus q (both known to everyone)
- Alice has private key: a
- Bob has private key: b

### Protocol

```
Alice computes:  A = g^a (mod q)    ← Alice's public value
Bob computes:    B = g^b (mod q)    ← Bob's public value

[Alice and Bob exchange A and B over an insecure channel]

Alice computes:  B^a = (g^b)^a = g^{ab} (mod q)
Bob computes:    A^b = (g^a)^b = g^{ab} (mod q)

Shared secret = g^{ab} (mod q)
```

### Why It Works

```
A^b = (g^a)^b = g^{ab}
B^a = (g^b)^a = g^{ab}
```

Both compute the same value because exponent multiplication is commutative. An eavesdropper who sees A and B cannot compute g^{ab} without solving the discrete log (finding a from A = g^a, or b from B = g^b).

### Connection to Discrete Log Assumption

The security of DH rests entirely on the hardness of the discrete logarithm. If discrete logs were easy, DH would be broken instantly (recover a from A, compute B^a).

### Is A^b == B^a (mod q)?

**Yes**, always:

```
A^b = (g^a)^b = g^{ab}
B^a = (g^b)^a = g^{ba} = g^{ab}   [exponent multiplication commutes]
```

This is not the same as saying `a^b ≡ b^a (mod q)` in general — that is **not** always true.

---

## 11. Python Toolkit for ZK Arithmetic

### Modular Inverse

```python
pow(a, -1, q)           # multiplicative inverse of a mod q (requires gcd(a,q)=1)
```

### Division in F_q

```python
# n / m  (mod q)
(n * pow(m, -1, q)) % q
```

### Negative Rational -n/m (mod q)

```python
(-n * pow(m, -1, q)) % q
```

### Additive Inverse

```python
(-x) % q
# or equivalently:
(q - x) % q
```

### Solve ax + b ≡ c (mod q)

```python
x = (c - b) * pow(a, -1, q) % q
```

### Binary Exponentiation

```python
pow(g, n, q)            # g^n mod q — Python uses binary exponentiation internally
```

### Discrete Log (Brute Force, Small Groups)

```python
def discrete_log(g, v, q):
    """Find x such that g^x ≡ v (mod q). Only feasible for small q."""
    curr = 1
    for x in range(q):
        if curr == v:
            return x
        curr = (curr * g) % q
    return None
```

### galois Library — Finite Field Arithmetic

```python
import galois

GF = galois.GF(q)       # create finite field F_q (q must be a prime power)

# Arithmetic
a = GF(x)
b = GF(y)

a + b                   # addition in F_q
a * b                   # multiplication in F_q
a / b                   # division in F_q (= a * b^{-1})
a ** n                  # exponentiation in F_q

# Result type: galois.FieldArray (wraps an integer, but behaves as a field element)
z = GF(x) / GF(y)      # z is of type galois.FieldArray
```

### Check Modular Inverse Exists

```python
from math import gcd
gcd(a, q) == 1          # True iff a^{-1} mod q exists
```

---

## Quick Reference Card

### Key Formulas

| Concept | Formula / Python |
|---|---|
| Congruence | `a ≡ b (mod q)` iff `q | (a-b)` |
| Additive inverse | `-x ≡ q-x (mod q)` |
| Multiplicative inverse | `pow(a, -1, q)` |
| Division | `(n * pow(m, -1, q)) % q` |
| Negative rational | `(-n * pow(m, -1, q)) % q` |
| Linear solve | `x = (c-b) * pow(a,-1,q) % q` |
| Fast exponentiation | `pow(g, n, q)` |
| Boolean AND | `a*b` (when a,b ∈ {0,1}) |
| Boolean OR | `a + b - ab` |
| Boolean NOT | `1 - a` |
| Force binary | `a*(a-1) = 0` |
| Is-zero gadget | `xy=0` and `xz=1-y` |
| Set membership | `(x-a)(x-b)(x-c) = 0` |
| EC point add x₃ | `m² - x₁ - x₂` |
| EC point add y₃ | `m(x₁ - x₃) - y₁` |
| EC tangent slope | `(3x² + a) / (2y)` |

### Algebraic Structures Summary

```
Magma       : closed
Semigroup   : closed, associative
Monoid      : closed, associative, identity
Group       : closed, associative, identity, inverses
Abelian Grp : + commutativity
Field       : abelian group under +, abelian group under × (excluding 0), distributivity
Finite Field: Field with finite order q = p^n
```

### ZK Circuit Construction Checklist

1. Express the computation as arithmetic over F_q.
2. For every boolean variable, add constraint: `v(v-1) = 0`.
3. Replace AND with `×`, OR with `a+b-ab`, NOT with `1-a`.
4. For is-zero: use the two-constraint gadget `{xy=0, xz=1-y}`.
5. Use SSA (new variable per assignment).
6. Unroll any loops to fixed depth.
7. Express the final statement as: "I know a witness w satisfying all constraints."
