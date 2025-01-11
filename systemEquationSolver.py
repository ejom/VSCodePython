from sympy import *

[u, v, w] = symbols('u v w')
z=1.3
eq_z = Eq(1 - (asin(u)*acos(v))/ln(3), z)
eq_v = Eq(cos((asin(u)+asin(1-tan(1)))*(asin(u)-tan(csc(3)))**2*(w*asin(u)-z)), v)
eq_f = Eq(u+v-tan(z)+w**2, 1)

guess = [-0.1, 0.8, 3]
solutions = nsolve([eq_f, eq_v, eq_z], [u, v, w], guess)

for i in range(len(solutions)):
    print(f"Solution: {i+1} : {solutions[i]:0.15f}")
