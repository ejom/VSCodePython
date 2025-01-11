from sympy import *
from sympy.abc import u, v, z
eq_z = Eq(1 - (asin(u)*acos(v))/ln(3), z)
eq_v = Eq((asin(u)+asin(1-tan(1)))*(asin(u)-tan(csc(3)))**2*(z*asin(u)-z), v)
eq_f = Eq(u+v-tan(z)+z**2, 1)
solutions = solve([eq_f, eq_v, eq_z], u, v, z, dict=True)
print(solutions)

