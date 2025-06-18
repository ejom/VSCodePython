from sympy import *

[x, y] = symbols('x y')

#2\cos\left(x\right)\left(\sec^{2}\left(\sin\left(x\right)\right)\tan\left(\sin\left(x\right)\right)+6e^{\sin\left(x\right)}\right)
equation = Eq(2*cos(x)*((sec(sin(x)))**2*tan(sin(x))+6*exp(sin(x))), 0)

solutions = solve(equation, x)

for i in range(len(solutions)):
    print("Solution", i+1, ":", solutions[i])
