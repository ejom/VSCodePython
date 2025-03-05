from sympy import *

x = symbols('x')

#2x^{4}-9x^{3}+3x^{2}+4
equation = Eq(2*x**4-9*x**3+3*x**2+4, 0)

solutions = solve(equation, x)

for i in range(len(solutions)):
    print("Solution", i+1, ":", solutions[i])
