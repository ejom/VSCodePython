from sympy import *

x = symbols('x')

#F\left(x\right)=\frac{1}{6}\ln\left(1-x^{6}\right)-\ln\left(x\right)+C
C = -(1/6)*ln(63/64)+ln(1/2)
equation = Eq((1/6)*ln(1-x**6)-ln(x)+C, 0)

solutions = solve(equation, x)

for i in range(len(solutions)):
    print("Solution", i+1, ":", solutions[i])
