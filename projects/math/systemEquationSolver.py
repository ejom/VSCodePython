from sympy import *
[x, y, z, a] = symbols('x y z a')
f_x = Eq(y**2+sin(z)*exp(x*sin(z))-2*a*x, 0)
f_y = Eq(2*x*y-2*a*y, 0)
f_z = Eq(x*cos(z)*exp(x*sin(z))-2*a*z, 0)
g = Eq(x**2+y**2+z**2, 4)

guess = [[-1, 0, -1, 0], [1, 1, 1, 1], [-1, -1, 1, -1], [-1, 1, 1, -1], [1, 0, -1, 0]]
solutions = []
for j in range(len(guess)):
    sol = nsolve([f_x, f_y, f_z, g], [x, y, z, a], guess[j])
    solutions.append(sol)
    print("set of solutions", j+1)
    for i in range(len(solutions[j])):
        print(f"Solution: {i+1} : {solutions[j][i]:0.15f}")
