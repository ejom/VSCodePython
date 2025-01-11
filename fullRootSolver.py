from sympy import *

r, theta = symbols('r theta')

equation = Eq((r*cos(theta))**3 + (r*sin(theta)-5)**3 + (r*cos(theta))**2 * ((r*sin(theta))+5)**2 + (r*cos(theta)) * (r*sin(theta)+5) - 2, 0)

solutions = solve(equation, r)

for i in range(len(solutions)):
    print("Solution", i+1, ":", solutions[i])
