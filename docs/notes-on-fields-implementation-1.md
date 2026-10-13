## 1. A group

A group is a set with one operation satisfying four rules: the operation stays inside the set (closure), it doesn't matter how you bracket it (associativity), there's an identity element that does nothing, and every element has an inverse that undoes it.

Example: integers under addition. Identity is 0, inverse of 5 is −5.

## 2. A field

A field is a set with **two** operations — addition and multiplication — where:
- the elements form a group under addition (identity 0),
- the *nonzero* elements form a group under multiplication (identity 1),
- and multiplication distributes over addition.

Goldilocks is a field: `{0, 1, ..., p−1}` with `+` and `×` mod p. Zero is excluded from the multiplicative group because 0 has no multiplicative inverse — nothing times 0 gives 1.

## 3. The multiplicative group of a field

This is the part you asked about. Take a field, remove 0, keep multiplication. For Goldilocks, that's `{1, 2, ..., p−1}` under multiplication mod p — a group of size p − 1.

## 4. Cyclic groups and generators

A group is **cyclic** if some single element g, repeatedly combined with itself, produces every element in the group. For a multiplicative group, "repeatedly combined" means powers: g, g², g³, …

The multiplicative group of *any* finite field happens to always be cyclic — this is a theorem, not a coincidence. g is called a **generator** (or primitive root). In your code, 7 is a generator of the Goldilocks multiplicative group: g, g², g³, … eventually hits every nonzero element before looping back to 1.

## 5. Subgroups

A subgroup is a subset that is itself a group under the same operation. The key fact you're leaning on:

> In a cyclic group of size n, there is exactly one subgroup of each size d, for every d that divides n — and no subgroup of any other size.

So the available subgroup sizes are exactly the **divisors of n**, where n is the size of the whole group (p − 1 here).

## 6. Roots of unity = elements of a subgroup

A 2^k-th root of unity is an element ω with ω^(2^k) = 1. The set `{1, ω, ω², ..., ω^(2^k − 1)}` is closed under multiplication and forms a subgroup of size 2^k.

By the fact in step 5, this subgroup **exists only if 2^k divides p − 1**.

## 7. Two-adicity = "how big a power-of-two divisor does p − 1 have"

This is where your halving exercise plugs in. Write p − 1 as `2^v · (odd part)`. That v is the largest exponent such that 2^v divides p − 1. So:

- the possible power-of-two subgroup sizes are 2⁰, 2¹, …, 2^v,
- v is exactly the two-adicity,
- and you find v by halving p − 1 until you hit odd — each halving strips one factor of 2.

## 8. How you actually construct that subgroup

g generates the *whole* group (size p − 1). To get the subgroup of size 2^k, you take big, evenly-spaced steps around that cycle:

```
ω = g^((p−1) / 2^k)
```

Raising ω to the power 2^k brings you back to 1 — by construction, since you multiplied the exponent by (p − 1)/2^k and g^(p−1) = 1. That ω generates exactly the 2^k-element subgroup, your root-of-unity domain.

## 9. Why any of this matters

FFT needs an evaluation domain that halves cleanly — square every element of the 2^k subgroup and you land exactly on the 2^(k−1) subgroup. Only root-of-unity subgroups have this property. Two-adicity is the hard ceiling on how large that domain (and thus your STARK trace) can be.

**The chain, end to end:**
field → nonzero elements form a multiplicative group → that group is cyclic, size p−1 → cyclic groups have one subgroup per divisor of their size → power-of-two subgroups exist only up to 2^(2-adicity of p−1) → that's your FFT domain ceiling.