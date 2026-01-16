from sympy import *
from sympy.abc import a, b, c, d, f, g, h, i, j
def fun(x):
    sumn = 0
    for n in range(x-1):
        if n:
            sumn+= 1/n**2
    return (a+b*x+c*x**2+d*x**3)/(f+g*x+h*x**2+i*x**3+j*x**4)+pi**2/6 - sumn

numEqs = 9
equations = [Eq(fun(X), 0) for X in range(1, numEqs+1)]

solutions = solve(equations, a, b, c, d, f, g, h, i, j, dict=True)
print(solutions)

