import galois

q = 311

GF = galois.GF(q)

regular_op = 191 * 262

print(regular_op)
print(GF(191) * 262) # 282

