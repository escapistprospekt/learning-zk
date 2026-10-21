# A toy STARK, step by step: squaring over F₁₇

## The example at a glance

A prover holds four numbers that follow the rule "next value = current value squared", and shows it by passing one polynomial identity, C(X) = Q(X) · Z(X), at a random point. Every number below is worked mod 17 and was checked by script.

The pipeline, in the order this doc walks it:

1. **Field and domain.** Work in F₁₇ and index rows by the points {1, 4, 16, 13}.
2. **Trace.** Write the computation as a column, [2, 4, 16, 1], and turn it into a polynomial t(X).
3. **Constraint.** Encode the rule as C(X) = t(ωX) − t(X)², which is zero wherever the rule holds.
4. **Vanishing polynomial.** Build Z(X), which is zero exactly on the rows where the rule must hold.
5. **Quotient.** Divide C by Z. A zero remainder is what an honest trace buys.
6. **Check.** The verifier picks a random r and tests C(r) = Q(r) · Z(r).

```
            ┌─────────────┐   ┌──────────────┐   ┌───────────────────┐   ┌───────────────────┐
 Prover     │    Trace    │──▶│ Interpolate  │──▶│  Apply the rule   │──▶│    Divide by Z    │
 (private)  │[2, 4, 16, 1]│   │t(X), degree 3│   │ C = t(ωX) − t(X)² │   │ Q(X), remainder 0 │
            └─────────────┘   └──────────────┘   └───────────────────┘   └─────────┬─────────┘
                   ┌───────────────── commitments to t(X) and Q(X) ─────────────────┘
                   ▼
            ┌──────────────┐   ┌───────────────────┐   ┌──────────────┐   ┌──────────────────┐
 Verifier   │    Pick r    │──▶│    Open values    │──▶│ Compute Z(r) │──▶│      Check       │
 (public)   │off the domain│   │ t(r), t(ωr), Q(r) │   │ Z is public  │   │ C(r) = Q(r)·Z(r) │
            └──────────────┘   └───────────────────┘   └──────────────┘   └──────────────────┘
```

Only the commitments and three opened values cross from prover to verifier; the trace itself never does.

|  | What | Value in this example |
| --- | --- | --- |
| Public | Field, domain, step ω | F₁₇, {1, 4, 16, 13}, ω = 4 |
| Public | The rule | next = current² |
| Private | The witness (the trace) | [2, 4, 16, 1], i.e. starting value 2 |

## Step 0: the field and the domain

The rows live on the four points {1, 4, 16, 13}, the powers of ω = 4 in F₁₇.

**The field.** F₁₇ is the numbers 0 to 16 with arithmetic mod 17. Two shortcuts make hand work easier: 16 ≡ −1 and 13 ≡ −4.

**Why a subgroup.** The nonzero elements form a multiplicative group of 16 elements. Its subgroups have sizes that divide 16: 1, 2, 4, 8 or 16. Four rows need the subgroup of size 4.

| Row i | Point ωⁱ | How you get it |
| --- | --- | --- |
| 0 | 1 | ω⁰ |
| 1 | 4 | ω¹ |
| 2 | 16 | 4 × 4 |
| 3 | 13 | 16 × 4 = 64 ≡ 13 |
| (wraps) | 1 | 13 × 4 = 52 ≡ 1 |

**Why ω moves one row.** Multiplying the point for row i by ω gives the point for row i + 1. That is what lets t(ωX) mean "the next row" in Step 2. The last row wraps to row 0, because ω⁴ = 1.

**Why 3 is not a point.** The order of 3 is 16, so 3 generates the whole group, not the size-4 subgroup. Only 4 and 13 have order 4; either works as ω, and they give the same set of points.

**Why this matters later.** Every point x in the domain satisfies x⁴ = 1, so the polynomial X⁴ − 1 is zero on the whole domain. That makes vanishing polynomials cheap to write down and evaluate (Step 3).

## Step 1: the trace and its polynomial

The witness is the trace [2, 4, 16, 1], and it becomes the polynomial t(X) = 8X³ + 16X² + 2X + 10.

**The trace.** Start at 2 and square three times. The last value is 256 ≡ 1 mod 17.

| Row i | Point x = ωⁱ | t(x) | Check |
| --- | --- | --- | --- |
| 0 | 1 | 2 | starting value |
| 1 | 4 | 4 | 2² = 4 |
| 2 | 16 | 16 | 4² = 16 |
| 3 | 13 | 1 | 16² = 256 ≡ 1 |

**Interpolation.** Four points fix exactly one polynomial of degree at most 3. Lagrange interpolation builds it as a sum of basis polynomials, each equal to 1 on its own point and 0 on the other three:

$$
t(X) = \sum_{i=0}^{3} t_i \prod_{j \ne i} \frac{X - \omega^j}{\omega^i - \omega^j} \pmod{17}
$$

Worked out mod 17, that gives:

$$
t(X) = 8X^3 + 16X^2 + 2X + 10
$$

**Spot check at x = 4.** 4³ = 64 ≡ 13 and 4² = 16, so t(4) = 8·13 + 16·16 + 2·4 + 10 ≡ 2 + 1 + 8 + 10 = 21 ≡ 4. That matches row 1.

**Why a polynomial.** A list of values can only be checked one entry at a time. A polynomial can be committed to once and then queried at points outside the domain, which is what makes the final check (Step 5) possible.

## Step 2: the rule as a polynomial

The rule becomes C(X) = t(ωX) − t(X)², which works out to 4X⁶ + 16X⁵ + X⁴ + 16X³ + 2X + 12 and is zero on the first three rows.

$$
C(X) = t(\omega X) - t(X)^2
$$

At a domain point x = ωⁱ, t(ωx) is the next row and t(x)² is the current row squared. So C(x) = 0 exactly when that step follows the rule.

**Working it out.** Substituting 4X into t multiplies the coefficient of Xᵏ by 4ᵏ:

- t(4X) = 8·64 X³ + 16·16 X² + 2·4 X + 10 ≡ 2X³ + X² + 8X + 10
- t(X)² ≡ 13X⁶ + X⁵ + 16X⁴ + 3X³ + X² + 6X + 15

Subtracting, mod 17:

$$
C(X) = 4X^6 + 16X^5 + X^4 + 16X^3 + 2X + 12
$$

C has degree 6, twice the degree of t, because the rule squares t.

**Evaluated on the domain.**

| Row | x | Next: t(ωx) | Current²: t(x)² | C(x) |
| --- | --- | --- | --- | --- |
| 0 | 1 | 4 | 2² = 4 | 0 |
| 1 | 4 | 16 | 4² = 16 | 0 |
| 2 | 16 | 1 | 16² ≡ 1 | 0 |
| 3 | 13 | 2 (wraps to row 0) | 1² = 1 | 1 |

**The wrap-around row.** At row 3, "next" is row 0, because ω⁴ = 1. The rule was never meant to hold from the last value back to the first, so C(13) = 1 is expected, not a failure. Step 3 leaves that point out.

**Off-domain values carry no row meaning.** C(3) ≡ 8, for example, but 3 is not a row. Points off the domain only matter as random test points in Step 5.

## Step 3: the vanishing polynomial

Z(X) = X³ + 13X² + 16X + 4 is zero on rows 0, 1 and 2 and nowhere else, so C passes only if Z divides it.

**The idea.** By the factor theorem, C(a) = 0 means (X − a) divides C(X). The rule must hold at 1, 4 and 16, so C must be divisible by:

$$
Z(X) = (X - 1)(X - 4)(X - 16)
$$

**Expanding mod 17.** (X − 1)(X − 4) = X² − 5X + 4. Multiplying by (X − 16) gives X³ − 21X² + 84X − 64. Reducing each coefficient:

$$
Z(X) \equiv X^3 + 13X^2 + 16X + 4 \pmod{17}
$$

| x | 1 | 4 | 16 | 13 |
| --- | --- | --- | --- | --- |
| Z(x) | 0 | 0 | 0 | 16 |

Z(13) is not zero, so the wrap-around row is left out on purpose.

**The shortcut.** The whole domain vanishes on X⁴ − 1. Removing the last point gives the same Z:

$$
Z(X) = \frac{X^4 - 1}{X - \omega^3} = \frac{X^4 - 1}{X - 13}
$$

Multiplying back confirms it: (X − 13)(X³ + 13X² + 16X + 4) ≡ X⁴ − 1. Real systems use this form, because Xⁿ − 1 costs a handful of squarings to evaluate at any point, even for millions of rows.

**Why X⁴ − 1 would be wrong.** It also demands C(13) = 0, which an honest trace fails. Dividing C by X⁴ − 1 leaves the remainder 16X³ + 4X² + X + 13, so a correct trace would be rejected.

## Step 4: the quotient

C divides exactly by Z, leaving Q(X) = 4X³ + 15X² + 14X + 3 with remainder 0.

$$
Q(X) = \frac{C(X)}{Z(X)} = 4X^3 + 15X^2 + 14X + 3
$$

**Long division mod 17.** Z's leading coefficient is 1, so each new term of Q is just the leading coefficient of what is left. Every product is reduced mod 17 before subtracting.

| Step | Next term of Q | Subtract | Left over |
| --- | --- | --- | --- |
| Start |  |  | 4X⁶ + 16X⁵ + X⁴ + 16X³ + 0X² + 2X + 12 |
| 1 | 4X³ | 4X³·Z = 4X⁶ + X⁵ + 13X⁴ + 16X³ | 15X⁵ + 5X⁴ + 0X³ + 0X² + 2X + 12 |
| 2 | 15X² | 15X²·Z = 15X⁵ + 8X⁴ + 2X³ + 9X² | 14X⁴ + 15X³ + 8X² + 2X + 12 |
| 3 | 14X | 14X·Z = 14X⁴ + 12X³ + 3X² + 5X | 3X³ + 5X² + 14X + 12 |
| 4 | 3 | 3·Z = 3X³ + 5X² + 14X + 12 | 0 |

**Why the remainder is the point.** The zero remainder holds only because C really is zero at 1, 4 and 16. If any of those rows broke the rule, the division would leave a remainder and no polynomial Q would satisfy C = Q · Z (see exercise 3).

**Degree.** deg Q = deg C − deg Z = 6 − 3 = 3. In a real system the verifier also checks that Q is this low-degree, because a prover could otherwise send an arbitrary function that matches at the queried points.

## Step 5: the verifier's check

The verifier never sees t or Q whole. It asks for three values at one random point r and checks a single equation.

$$
t(\omega r) - t(r)^2 \stackrel{?}{=} Q(r) \cdot Z(r)
$$

The left side is C(r), rebuilt from two openings of t. The verifier computes Z(r) itself, because Z is public.

**Worked with r = 5.** The step ωr = 20 ≡ 3.

| Value | Who supplies it | Result mod 17 |
| --- | --- | --- |
| t(5) | prover, opened from its commitment | 9 |
| t(3) = t(ω·5) | prover, opened from its commitment | 2 |
| Q(5) | prover, opened from its commitment | 13 |
| Z(5) | verifier computes: 125 + 325 + 80 + 4 = 534 | 7 |

- Left: t(3) − t(5)² = 2 − 81 ≡ 2 − 13 ≡ 6
- Right: Q(5) · Z(5) = 13 · 7 = 91 ≡ 6

They match, so the check passes.

**Why r must be off the domain.** At r = 1, 4 or 16, Z(r) = 0 and C(r) = 0, so the equation holds whatever Q is. Those points test nothing.

**Why one point is enough.** Suppose the prover's polynomials do not satisfy C = Q · Z. Their difference is then a nonzero polynomial of degree at most 6, which has at most 6 roots. A random r lands on one with probability at most 6 / |F|. This is the Schwartz–Zippel lemma.

**Why the toy field is too small.** In F₁₇ that bound is 6/17, about 35%, so a cheater would often get through. Real systems use fields of 2⁶⁴ elements or more, or extensions of them, where the bound is negligible. The point r is also chosen after the prover commits, usually by hashing the commitments (the Fiat–Shamir transform), so the prover cannot aim for a lucky r.

## What is private, and what this toy leaves out

The private input is the trace, starting value 2. As written, though, the toy neither ties the claim to an output nor hides the trace.

|  | Item | In this example |
| --- | --- | --- |
| Private | The trace, and the polynomials built from it | [2, 4, 16, 1]; t(X), C(X), Q(X) |
| Public | Field, domain, ω, the rule, Z(X) | F₁₇; {1, 4, 16, 13}; 4; next = current²; X³ + 13X² + 16X + 4 |
| Public, once added | The claimed output | t(13) = 1 |

**How the secret leaks here.** Showing C's coefficients gives the trace away. C(13) = t(1) − t(13)² = a − a¹⁶, and a¹⁶ = 1 for any nonzero a in F₁₇, so C(13) = 1 forces a = 2. A real verifier never sees C, only a few openings.

The pieces a real STARK adds:

1. **Boundary constraints.** Without one, any start passes: [3, 9, 13, 16] also follows the rule. Fixing the output adds a second quotient, (t(X) − 1) / (X − 13), which must also be a polynomial. The claim becomes "I know x such that x⁸ = 1".
2. **Commitments.** The prover evaluates t and Q on a larger domain (the low-degree extension) and commits with a Merkle tree. Each opening comes with a Merkle path.
3. **A low-degree test.** FRI shows the committed values really come from a polynomial of the claimed degree. Without it, Step 5's argument does not hold.
4. **Zero knowledge.** Openings still leak information about t. Adding a random multiple of X⁴ − 1 to t changes nothing on the domain but masks its values everywhere else. The basic construction does not include this.
5. **A big field.** In F₁₇, x⁸ = 1 has 8 solutions (1, 2, 4, 8, 9, 13, 15, 16), so guessing the secret is trivial and the soundness bound is about 35%. Real fields make both negligible.

## Exercises

Work each one before reading its answer. All arithmetic is mod 17.

1. **Domain size.** Why can't this example use a domain of 5 rows in F₁₇?
   - *Answer:* The domain is a multiplicative subgroup, and subgroup sizes divide 16. The choices are 1, 2, 4, 8 or 16 rows.
2. **A different start.** Start the trace at 3. What is the trace, and what does C give on the domain?
   - *Answer:* [3, 9, 13, 16]. C on the domain is [0, 0, 0, 2]: rows 0 to 2 pass, and the wrap row gives 3 − 16² ≡ 3 − 1 = 2. The transition rule alone does not pin the input, which is why boundary constraints exist.
3. **A cheating trace.** The prover submits [2, 4, 15, 1]. Which rows break, and what happens in the division?
   - *Answer:* C on the domain is [0, 16, 14, 1]. Row 1 breaks (4² = 16, not 15) and row 2 breaks (15² = 225 ≡ 4, not 1). Dividing by Z leaves the remainder 7X² + 10X, so no Q exists.
4. **Another random point.** Run the Step 5 check at r = 2.
   - *Answer:* C(2) = 10. Q(2) = 32 + 60 + 28 + 3 = 123 ≡ 4. Z(2) = 8 + 52 + 32 + 4 = 96 ≡ 11. Q(2) · Z(2) = 44 ≡ 10, which matches.
5. **The other generator.** ω = 13 also has order 4. What changes if you use it?
   - *Answer:* The same four points, visited in the order 1, 13, 16, 4. The trace sits on different points, so t, C and Q change, but every step works the same way.
6. **A boundary constraint.** Show that fixing the output to 1 gives a valid quotient for this trace.
   - *Answer:* The constraint is t(13) = 1. Since t(13) − 1 = 0, the factor theorem says (X − 13) divides t(X) − 1, so (t(X) − 1) / (X − 13) is a polynomial of degree 2.
