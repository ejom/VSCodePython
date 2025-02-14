from sympy import *
from sympy.abc import x, y, z, a
f_x = Eq(y**2+sin(z)*exp(x*sin(z))-2*a*x, 0)
f_y = Eq(2*x*y-2*a*y, 0)
f_z = Eq(x*cos(z)*exp(x*sin(z))-2*a*z, 0)
g = Eq(x**2+y**2+z**2, 4)
solutions = solve([f_x, f_y, f_z, g], x, y, z, a, dict=True)
print(solutions)

