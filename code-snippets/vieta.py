import numpy as np

coefficients = [2, 6, -4, 10]
roots = np.roots(coefficients)
sum = 0

for v in roots:
  sum += v

print(roots)
print(sum)