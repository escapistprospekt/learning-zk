from sympy.ntheory import discrete_log
from galois import GF
import time
from sympy import nextprime

q = nextprime(10**25)
g = int(GF(q).primitive_element)

X = 100

start = time.time()
dl = discrete_log(q, X, g)
elapsed = time.time() - start

print(f"The discrete log of {X} base {g} mod {q} is {dl}")
print(f"Computation took {elapsed:.6f} seconds")
